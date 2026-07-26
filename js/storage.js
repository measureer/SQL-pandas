// localStorage 持久化：进度、笔记、收藏；支持导出/导入 JSON

const KEY = 'sql-pandas-lab:v1';

const DEFAULT_STATE = {
  // progress[exerciseId] = { sqlPassed: bool, pandasPassed: bool, starred: bool,
  //                          sqlCode: string, pandasCode: string, attempts: number }
  progress: {},
  // notes[exerciseId] = string
  notes: {},
};

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return structuredClone(DEFAULT_STATE);
    const parsed = JSON.parse(raw);
    return { ...structuredClone(DEFAULT_STATE), ...parsed };
  } catch {
    return structuredClone(DEFAULT_STATE);
  }
}

let state = load();

function save() {
  localStorage.setItem(KEY, JSON.stringify(state));
}

export function getProgress(id) {
  return state.progress[id] || null;
}

export function updateProgress(id, patch) {
  state.progress[id] = { ...(state.progress[id] || {}), ...patch };
  save();
}

export function getAllProgress() {
  return state.progress;
}

export function getNote(id) {
  return state.notes[id] || '';
}

export function setNote(id, text) {
  state.notes[id] = text;
  save();
}

export function exportJSON() {
  return JSON.stringify(state, null, 2);
}

export function importJSON(text) {
  const parsed = JSON.parse(text);
  if (typeof parsed !== 'object' || parsed === null) {
    throw new Error('无效的备份文件');
  }
  state = {
    progress: parsed.progress || {},
    notes: parsed.notes || {},
  };
  save();
}
