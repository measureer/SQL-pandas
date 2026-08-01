// 主逻辑：题目列表、编辑器、运行判题、进度、笔记
import { EXERCISES } from '../data/exercises.js';
import { DATASETS } from './datasets.js';
import { runSql } from './sql-runner.js';
import { runPandas } from './pandas-runner.js';
import { compareResults } from './compare.js';
import * as store from './storage.js';
import * as webdav from './webdav.js';

const LEVELS = [
  { key: 'beginner', label: '入门 Beginner' },
  { key: 'intermediate', label: '进阶 Intermediate' },
  { key: 'advanced', label: '精通 Advanced' },
];
const LEVEL_SHORT = { beginner: '入门', intermediate: '进阶', advanced: '精通' };

const $ = (sel) => document.querySelector(sel);

let currentId = null;
let activeTab = 'sql';
let cmSql = null;
let cmPandas = null;
// 期望结果缓存：`${id}:${engine}` -> {columns, rows}
const expectedCache = new Map();
// 每个语言 Tab 独立的结果区元素：{ sql: {panel,banner,actual,expected}, pandas: {...} }
const resultEls = {};

// SQLite 方言的类型 + 常用函数 + 窗口子句词（CodeMirror builtin，着色为 .cm-builtin）
// 默认 text/x-sql 的关键字表不含这些词，导致函数与专有词无颜色
const SQL_BUILTIN = (
  'bool boolean bit blob decimal double float long text clob bigint int int2 int8 integer char varchar date datetime year unsigned signed numeric real ' +
  'sum avg min max count total round abs length upper lower replace substr instr trim ltrim rtrim coalesce ifnull nullif group_concat ' +
  'strftime julianday printf typeof hex quote random changes last_insert_rowid ' +
  'row_number rank dense_rank lag lead first_value last_value nth_value ntile ' +
  'over partition filter within'
).split(' ').reduce((m, w) => ((m[w] = true), m), {});

/* ---------------- 初始化 ---------------- */
function init() {
  cmSql = CodeMirror.fromTextArea($('#editor-sql'), {
    mode: { name: 'text/x-sqlite', builtin: SQL_BUILTIN },
    theme: 'material-darker',
    lineNumbers: true,
    indentWithTabs: false,
  });
  cmPandas = CodeMirror.fromTextArea($('#editor-pandas'), {
    mode: 'python',
    theme: 'material-darker',
    lineNumbers: true,
    indentUnit: 4,
  });

  cmSql.on('change', () => saveDraft());
  cmPandas.on('change', () => saveDraft());

  for (const tab of ['sql', 'pandas']) {
    resultEls[tab] = {
      panel: $(`#result-panel-${tab}`),
      banner: $(`#judge-banner-${tab}`),
      actual: $(`#actual-table-${tab}`),
      expected: $(`#expected-table-${tab}`),
    };
  }

  document.querySelectorAll('.tab').forEach((t) =>
    t.addEventListener('click', () => switchTab(t.dataset.tab))
  );
  $('#btn-run').addEventListener('click', onRun);
  $('#btn-solution').addEventListener('click', onShowSolution);
  $('#btn-solution-close').addEventListener('click', () => $('#solution-view').classList.add('hidden'));
  $('#btn-reset').addEventListener('click', onResetCode);
  $('#btn-star').addEventListener('click', onToggleStar);
  $('#search').addEventListener('input', renderList);
  $('#filter-level').addEventListener('change', renderList);
  $('#filter-status').addEventListener('change', renderList);
  $('#btn-export').addEventListener('click', onExport);
  $('#btn-import').addEventListener('click', () => $('#import-file').click());
  $('#import-file').addEventListener('change', onImport);
  initWebdav();

  let noteTimer = null;
  const saveNoteNow = (id, text) => {
    if (!id) return;
    store.setNote(id, text);
    $('#notes-saved').textContent = '已自动保存 ✓';
    setTimeout(() => ($('#notes-saved').textContent = ''), 1500);
  };
  $('#notes').addEventListener('input', () => {
    // 捕获当前题目与内容，避免 400ms 防抖窗口内切换题目导致笔记串题或丢失
    const id = currentId;
    const text = $('#notes').value;
    clearTimeout(noteTimer);
    noteTimer = setTimeout(() => saveNoteNow(id, text), 400);
  });
  $('#notes').addEventListener('blur', () => {
    clearTimeout(noteTimer);
    saveNoteNow(currentId, $('#notes').value);
  });

  renderSchema();
  renderDashboard();
  renderList();
  selectExercise(EXERCISES[0].id);
  switchTab('sql'); // 初始只显示 SQL 编辑器
}

/* ---------------- 题目列表 ---------------- */
function currentFilters() {
  return {
    q: $('#search').value.trim().toLowerCase(),
    level: $('#filter-level').value,
    status: $('#filter-status').value,
  };
}

function matchFilter(ex, f) {
  const p = store.getProgress(ex.id) || {};
  if (f.level && ex.level !== f.level) return false;
  if (f.q) {
    const hay = `${ex.title} ${ex.topics.join(' ')}`.toLowerCase();
    if (!hay.includes(f.q)) return false;
  }
  if (f.status === 'done' && !(p.sqlPassed && p.pandasPassed)) return false;
  if (f.status === 'undone' && p.sqlPassed && p.pandasPassed) return false;
  if (f.status === 'starred' && !p.starred) return false;
  return true;
}

function renderList() {
  const f = currentFilters();
  const nav = $('#exercise-list');
  nav.innerHTML = '';
  for (const lv of LEVELS) {
    const items = EXERCISES.filter((e) => e.level === lv.key && matchFilter(e, f));
    if (items.length === 0) continue;
    const group = document.createElement('div');
    group.className = 'level-group';
    const done = EXERCISES.filter((e) => {
      const p = store.getProgress(e.id);
      return e.level === lv.key && p && p.sqlPassed && p.pandasPassed;
    }).length;
    const total = EXERCISES.filter((e) => e.level === lv.key).length;
    group.innerHTML = `<div class="level-group-title"><span>${lv.label}</span><span>${done}/${total}</span></div>`;
    for (const ex of items) {
      const p = store.getProgress(ex.id) || {};
      const el = document.createElement('div');
      el.className = 'exercise-item' + (ex.id === currentId ? ' active' : '');
      if (p.sqlPassed && p.pandasPassed) el.classList.add('done');
      el.innerHTML = `
        <span class="item-title">${ex.id}. ${ex.title}</span>
        <span class="status-icons">
          ${p.sqlPassed ? '<span class="s-sql" title="SQL 已通过">S✓</span>' : ''}
          ${p.pandasPassed ? '<span class="s-pd" title="pandas 已通过">P✓</span>' : ''}
          ${p.starred ? '<span class="s-star">★</span>' : ''}
        </span>`;
      el.addEventListener('click', () => selectExercise(ex.id));
      group.appendChild(el);
    }
    nav.appendChild(group);
  }
}

/* ---------------- 题目切换 ---------------- */
function selectExercise(id) {
  currentId = id;
  const ex = EXERCISES.find((e) => e.id === id);
  const p = store.getProgress(id) || {};

  $('#exercise-title').textContent = `${ex.id}. ${ex.title}`;
  $('#exercise-meta').innerHTML = `
    <span class="badge level-${ex.level}">${LEVEL_SHORT[ex.level]}</span>
    ${ex.topics.map((t) => `<span class="badge">${t}</span>`).join('')}`;
  $('#exercise-desc').innerHTML = ex.description;
  $('#explanation').innerHTML = ex.explanation;

  $('#btn-star').textContent = p.starred ? '★' : '☆';
  $('#btn-star').classList.toggle('starred', !!p.starred);

  cmSql.setValue(p.sqlCode ?? ex.starterSql);
  cmPandas.setValue(p.pandasCode ?? ex.starterPandas);
  updateTabDots();

  $('#notes').value = store.getNote(id);
  $('#solution-view').classList.add('hidden');
  for (const tab of ['sql', 'pandas']) {
    const r = resultEls[tab];
    r.banner.className = 'judge-banner hidden';
    r.actual.innerHTML = '<div class="table-empty">点击「运行」查看结果</div>';
    r.expected.innerHTML = '<div class="table-empty">运行后显示期望结果</div>';
  }

  document.querySelectorAll('.exercise-item').forEach((el) => el.classList.remove('active'));
  renderList();
}

function updateTabDots() {
  const p = store.getProgress(currentId) || {};
  document.querySelector('.tab[data-tab="sql"]').innerHTML =
    `SQL${p.sqlPassed ? '<span class="dot sql-passed"> ●</span>' : ''}`;
  document.querySelector('.tab[data-tab="pandas"]').innerHTML =
    `pandas${p.pandasPassed ? '<span class="dot pd-passed"> ●</span>' : ''}`;
}

function switchTab(tab) {
  activeTab = tab;
  document.querySelectorAll('.tab').forEach((t) => t.classList.toggle('active', t.dataset.tab === tab));
  cmSql.getWrapperElement().style.display = tab === 'sql' ? '' : 'none';
  cmPandas.getWrapperElement().style.display = tab === 'pandas' ? '' : 'none';
  (tab === 'sql' ? cmSql : cmPandas).refresh();
  // 结果区随 Tab 切换：两个语言各自保留自己的结果与判题横幅
  resultEls.sql.panel.classList.toggle('hidden', tab !== 'sql');
  resultEls.pandas.panel.classList.toggle('hidden', tab !== 'pandas');
  // 答案块展开时，切换 Tab 同步刷新为对应语言的参考答案
  if (!$('#solution-view').classList.contains('hidden')) renderSolution();
}

function saveDraft() {
  if (!currentId) return;
  store.updateProgress(currentId, {
    sqlCode: cmSql.getValue(),
    pandasCode: cmPandas.getValue(),
  });
}

/* ---------------- 运行与判题 ---------------- */
function setStatus(text) {
  $('#engine-status').textContent = text || '';
  $('#loading-text').textContent = text || '';
  $('#loading-mask').classList.toggle('hidden', !text);
}

async function getExpected(ex, engine) {
  const key = `${ex.id}:${engine}`;
  if (!expectedCache.has(key)) {
    const result =
      engine === 'sql'
        ? await runSql(ex.solutionSql, setStatus)
        : await runPandas(ex.solutionPandas, setStatus);
    expectedCache.set(key, result);
  }
  return expectedCache.get(key);
}

async function onRun() {
  const ex = EXERCISES.find((e) => e.id === currentId);
  const btn = $('#btn-run');
  btn.disabled = true;
  const engine = activeTab;
  const result = resultEls[engine];
  const banner = result.banner;
  banner.className = 'judge-banner hidden';
  try {
    const code = engine === 'sql' ? cmSql.getValue() : cmPandas.getValue();
    const runner = engine === 'sql' ? runSql : runPandas;

    const [actual, expected] = await Promise.all([
      runner(code, setStatus),
      getExpected(ex, engine),
    ]);

    renderTable(result.actual, actual);
    renderTable(result.expected, expected);

    const verdict = compareResults(actual, expected);
    banner.className = `judge-banner ${verdict.pass ? 'pass' : 'fail'}`;
    banner.textContent = verdict.pass ? `✓ ${verdict.message}` : `✗ ${verdict.message}`;
    if (verdict.diffs && verdict.diffs.size > 0) {
      highlightDiffs(result.actual, verdict.diffs);
    }

    const p = store.getProgress(currentId) || {};
    store.updateProgress(currentId, {
      attempts: (p.attempts || 0) + 1,
      ...(engine === 'sql' ? { sqlPassed: verdict.pass || p.sqlPassed } : {}),
      ...(engine === 'pandas' ? { pandasPassed: verdict.pass || p.pandasPassed } : {}),
    });
    updateTabDots();
    renderList();
    renderDashboard();
  } catch (err) {
    banner.className = 'judge-banner error';
    banner.textContent = `运行出错：\n${err.message}`;
    result.actual.innerHTML = '<div class="table-empty">—</div>';
  } finally {
    setStatus('');
    btn.disabled = false;
  }
}

function renderTable(container, data) {
  if (!data || data.rows.length === 0) {
    container.innerHTML = '<div class="table-empty">（空结果）</div>';
    return;
  }
  const head = data.columns.map((c) => `<th>${escapeHtml(c)}</th>`).join('');
  const body = data.rows
    .map(
      (row, r) =>
        `<tr>${row
          .map(
            (v, c) =>
              `<td data-cell="${r}-${c}">${v === null || v === undefined ? '<i>NULL</i>' : escapeHtml(String(v))}</td>`
          )
          .join('')}</tr>`
    )
    .join('');
  container.innerHTML = `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

function highlightDiffs(container, diffs) {
  for (const key of diffs) {
    const td = container.querySelector(`[data-cell="${key}"]`);
    if (td) td.classList.add('diff');
  }
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/* ---------------- 答案 / 重置 / 收藏 ---------------- */
function renderSolution() {
  const ex = EXERCISES.find((e) => e.id === currentId);
  const target = activeTab === 'sql' ? ex.solutionSql : ex.solutionPandas;
  $('#solution-lang').textContent = activeTab === 'sql' ? 'SQL' : 'pandas';
  $('#solution-code').textContent = target;
}

function onShowSolution() {
  const view = $('#solution-view');
  if (view.classList.contains('hidden')) {
    renderSolution();
    view.classList.remove('hidden');
  } else {
    view.classList.add('hidden');
  }
}

function onResetCode() {
  const ex = EXERCISES.find((e) => e.id === currentId);
  const isSql = activeTab === 'sql';
  if (!confirm(`重置${isSql ? ' SQL ' : ' pandas '}为初始代码？`)) return;
  if (isSql) cmSql.setValue(ex.starterSql);
  else cmPandas.setValue(ex.starterPandas);
}

function onToggleStar() {
  const p = store.getProgress(currentId) || {};
  store.updateProgress(currentId, { starred: !p.starred });
  $('#btn-star').textContent = p.starred ? '☆' : '★';
  $('#btn-star').classList.toggle('starred', !p.starred);
  renderList();
}

/* ---------------- 仪表盘 / 导入导出 ---------------- */
function renderDashboard() {
  const all = store.getAllProgress();
  const parts = LEVELS.map((lv) => {
    const total = EXERCISES.filter((e) => e.level === lv.key).length;
    const done = EXERCISES.filter((e) => {
      const p = all[e.id];
      return e.level === lv.key && p && p.sqlPassed && p.pandasPassed;
    }).length;
    return `<span>${LEVEL_SHORT[lv.key]} <b class="done">${done}</b>/<b>${total}</b></span>`;
  });
  const totalDone = EXERCISES.filter((e) => {
    const p = all[e.id];
    return p && p.sqlPassed && p.pandasPassed;
  }).length;
  parts.push(`<span>总进度 <b class="done">${totalDone}</b>/<b>${EXERCISES.length}</b></span>`);
  $('#dashboard').innerHTML = parts.join('');
}

function onExport() {
  const blob = new Blob([store.exportJSON()], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `sql-pandas-progress-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
}

function onImport(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      store.importJSON(reader.result);
      renderList();
      renderDashboard();
      selectExercise(currentId);
      alert('导入成功！');
    } catch (err) {
      alert(`导入失败：${err.message}`);
    }
  };
  reader.readAsText(file);
  e.target.value = '';
}

/* ---------------- WebDAV 同步 ---------------- */
function setWebdavStatus(text, isError = false) {
  const el = $('#webdav-status');
  el.textContent = text || '';
  el.classList.toggle('error', isError);
}

function readWebdavForm() {
  return {
    url: $('#webdav-url').value,
    username: $('#webdav-user').value,
    password: $('#webdav-pass').value,
    filename: $('#webdav-filename').value,
    autoUpload: $('#webdav-auto-upload').checked,
  };
}

function fillWebdavForm(cfg) {
  $('#webdav-url').value = cfg.url;
  $('#webdav-user').value = cfg.username;
  $('#webdav-pass').value = cfg.password;
  $('#webdav-filename').value = cfg.filename;
  $('#webdav-auto-upload').checked = cfg.autoUpload;
}

async function webdavAction(action, okText) {
  const cfg = readWebdavForm();
  webdav.saveConfig(cfg);
  if (!webdav.isConfigured(cfg)) {
    setWebdavStatus('请先填写服务器地址', true);
    return;
  }
  setWebdavStatus('进行中…');
  try {
    await action(cfg);
    setWebdavStatus(`${okText}（${new Date().toLocaleTimeString()}）`);
  } catch (err) {
    setWebdavStatus(err.message, true);
  }
}

function applyImportedState() {
  renderList();
  renderDashboard();
  selectExercise(currentId);
}

function initWebdav() {
  fillWebdavForm(webdav.getConfig());

  $('#btn-webdav').addEventListener('click', () => $('#webdav-modal').classList.remove('hidden'));
  $('#webdav-close').addEventListener('click', () => $('#webdav-modal').classList.add('hidden'));
  $('#webdav-modal').addEventListener('click', (e) => {
    if (e.target.id === 'webdav-modal') $('#webdav-modal').classList.add('hidden');
  });

  $('#webdav-save').addEventListener('click', () => {
    webdav.saveConfig(readWebdavForm());
    setWebdavStatus('设置已保存');
  });
  $('#webdav-test').addEventListener('click', () =>
    webdavAction((cfg) => webdav.testConnection(cfg), '连接成功')
  );
  $('#webdav-upload').addEventListener('click', () =>
    webdavAction((cfg) => webdav.upload(cfg, store.exportJSON()), '上传成功')
  );
  $('#webdav-download').addEventListener('click', () =>
    webdavAction(async (cfg) => {
      const text = await webdav.download(cfg);
      store.importJSON(text);
      applyImportedState();
    }, '已从云端恢复')
  );

  // 自动上传：本地任何持久化变更后 2 秒防抖推送
  let autoTimer = null;
  store.onChange(() => {
    const cfg = webdav.getConfig();
    if (!cfg.autoUpload || !webdav.isConfigured(cfg)) return;
    clearTimeout(autoTimer);
    autoTimer = setTimeout(async () => {
      try {
        await webdav.upload(cfg, store.exportJSON());
        setWebdavStatus(`已自动上传（${new Date().toLocaleTimeString()}）`);
      } catch (err) {
        setWebdavStatus(`自动上传失败：${err.message}`, true);
      }
    }, 2000);
  });
}

/* ---------------- Schema 视图 ---------------- */
function renderSchema() {
  $('#schema-view').innerHTML = Object.entries(DATASETS)
    .map(([table, def]) => {
      const cols = def.columns
        .map((c) => `<tr><td>${c.name}</td><td>${c.type}</td></tr>`)
        .join('');
      return `<details>
        <summary>${table} (${def.rows.length} 行)</summary>
        <table><thead><tr><th>列</th><th>类型</th></tr></thead><tbody>${cols}</tbody></table>
      </details>`;
    })
    .join('');
}

init();

// 调试/测试钩子（控制台可用）
window.__lab = {
  selectExercise,
  getEditors: () => ({ sql: cmSql, pandas: cmPandas }),
  run: onRun,
  switchTab,
  store,
  EXERCISES,
  getCurrentId: () => currentId,
};
