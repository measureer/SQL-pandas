// Pyodide (Python WASM) 执行封装，懒加载
import { buildPandasSetupCode } from './datasets.js';

// 本地 vendor（离线可用）；如不存在可改回 CDN：https://cdn.jsdelivr.net/pyodide/v0.26.4/full/
const PYODIDE_BASE = new URL('../vendor/pyodide/', import.meta.url).href;

let pyodide = null;
let loadingPromise = null;

async function ensureInit(onStatus) {
  if (pyodide) return;
  if (!loadingPromise) {
    loadingPromise = (async () => {
      onStatus?.('正在加载 Python 引擎 (Pyodide)，首次约需 5-15 秒…');
      const { loadPyodide } = await import(`${PYODIDE_BASE}pyodide.mjs`);
      const py = await loadPyodide({ indexURL: PYODIDE_BASE });
      onStatus?.('正在安装 pandas…');
      await py.loadPackage(['pandas']);
      pyodide = py;
      onStatus?.('');
    })();
  }
  await loadingPromise;
}

// 每次运行前重建数据命名空间，保证运行互不污染
async function resetNamespace(onStatus) {
  await ensureInit(onStatus);
  // 清空用户全局命名空间后重建数据
  pyodide.runPython('globals().clear()');
  pyodide.runPython(buildPandasSetupCode());
}

// 执行用户 pandas 代码，约定最终结果赋给变量 result (DataFrame)
// 返回 { columns: [...], rows: [[...], ...] }；出错抛出 Error
export async function runPandas(userCode, onStatus) {
  await resetNamespace(onStatus);
  const py = pyodide;

  try {
    py.runPython(userCode);
  } catch (e) {
    throw new Error(cleanPythonError(e.message));
  }

  const hasResult = py.runPython("'result' in dir()");
  if (!hasResult) {
    throw new Error('未找到变量 result —— 请将最终结果赋值给 result (DataFrame)');
  }

  // 在 Python 侧将 result 规整为 {columns, rows} 的 JSON
  py.globals.set('__extract_code__', `
import json
import numpy as np

def __extract(df):
    df = df.reset_index(drop=True)
    cols = [str(c) for c in df.columns]
    rows = []
    for _, r in df.iterrows():
        row = []
        for v in r:
            if pd.isna(v):
                row.append(None)
            elif isinstance(v, (np.integer,)):
                row.append(int(v))
            elif isinstance(v, (np.floating,)):
                row.append(float(v))
            elif isinstance(v, (np.bool_,)):
                row.append(bool(v))
            elif isinstance(v, pd.Timestamp):
                row.append(v.strftime('%Y-%m-%d'))
            else:
                row.append(str(v) if not isinstance(v, str) else v)
        rows.append(row)
    return json.dumps({'columns': cols, 'rows': rows})

__result_json__ = __extract(result)
`);
  py.runPython(py.globals.get('__extract_code__'));
  const json = py.globals.get('__result_json__');
  return JSON.parse(json);
}

function cleanPythonError(msg) {
  // 只保留最后几行有效错误信息
  const lines = String(msg).split('\n').filter((l) => l.trim());
  return lines.slice(-6).join('\n');
}
