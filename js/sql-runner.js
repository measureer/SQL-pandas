// sql.js (SQLite WASM) 执行封装
import { buildSqliteDDL } from './datasets.js';

const SQL_JS_BASE = 'https://cdn.jsdelivr.net/npm/sql.js@1.10.3/dist/';

let SQL = null;
let db = null;

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src;
    s.onload = resolve;
    s.onerror = () => reject(new Error(`加载失败: ${src}`));
    document.head.appendChild(s);
  });
}

async function ensureInit(onStatus) {
  if (SQL) return;
  onStatus?.('正在加载 SQL 引擎 (sql.js)…');
  if (!window.initSqlJs) {
    await loadScript(`${SQL_JS_BASE}sql-wasm.js`);
  }
  SQL = await window.initSqlJs({
    locateFile: (file) => `${SQL_JS_BASE}${file}`,
  });
  onStatus?.('');
}

// 每次运行前重建内存数据库，保证运行互不污染
export async function resetDatabase(onStatus) {
  await ensureInit(onStatus);
  if (db) db.close();
  db = new SQL.Database();
  for (const stmt of buildSqliteDDL()) {
    db.run(stmt);
  }
}

// 执行 SQL，返回 { columns: [...], rows: [[...], ...] }
// 出错时抛出 Error
export async function runSql(sqlText, onStatus) {
  await resetDatabase(onStatus);
  const res = db.exec(sqlText);
  if (!res || res.length === 0) {
    return { columns: [], rows: [] };
  }
  const last = res[res.length - 1];
  return { columns: last.columns, rows: last.values };
}
