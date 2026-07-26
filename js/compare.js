// 结果比对：忽略行序，数值容差 1e-6，列名不敏感（按位置比对值，但提示列名差异）

const EPS = 1e-6;

function valuesEqual(a, b) {
  if (a === null || a === undefined) return b === null || b === undefined;
  if (b === null || b === undefined) return false;
  const na = Number(a);
  const nb = Number(b);
  if (!Number.isNaN(na) && !Number.isNaN(nb) && a !== '' && b !== '') {
    return Math.abs(na - nb) < EPS;
  }
  return String(a) === String(b);
}

function rowKey(row) {
  return row.map((v) => (v === null || v === undefined ? '␀' : String(v))).join('␁');
}

// 返回 { pass, message, diffs: Set<"r-c">, matchedExpected: [...] }
export function compareResults(actual, expected) {
  if (!actual || !expected) {
    return { pass: false, message: '结果为空', diffs: new Set() };
  }
  if (actual.rows.length === 0 && expected.rows.length > 0) {
    return { pass: false, message: '你的查询没有返回任何行', diffs: new Set() };
  }
  if (actual.columns.length !== expected.columns.length) {
    return {
      pass: false,
      message: `列数不一致：期望 ${expected.columns.length} 列，实际 ${actual.columns.length} 列`,
      diffs: new Set(),
    };
  }
  if (actual.rows.length !== expected.rows.length) {
    return {
      pass: false,
      message: `行数不一致：期望 ${expected.rows.length} 行，实际 ${actual.rows.length} 行`,
      diffs: new Set(),
    };
  }

  // 忽略行序：将双方行按字符串键排序后逐格比对
  const sortWithIndex = (tbl) =>
    tbl.rows
      .map((row, i) => ({ row, i }))
      .sort((x, y) => (rowKey(x.row) < rowKey(y.row) ? -1 : 1));

  const aSorted = sortWithIndex(actual);
  const eSorted = sortWithIndex(expected);

  const diffs = new Set();
  let firstDiff = null;
  for (let r = 0; r < aSorted.length; r++) {
    for (let c = 0; c < actual.columns.length; c++) {
      if (!valuesEqual(aSorted[r].row[c], eSorted[r].row[c])) {
        diffs.add(`${aSorted[r].i}-${c}`);
        if (!firstDiff) {
          firstDiff = {
            row: r + 1,
            col: expected.columns[c] || `#${c + 1}`,
            expected: eSorted[r].row[c],
            actual: aSorted[r].row[c],
          };
        }
      }
    }
  }

  if (diffs.size > 0) {
    return {
      pass: false,
      message: `有 ${diffs.size} 个单元格不一致（忽略行序比对）。首个差异：第 ${firstDiff.row} 行「${firstDiff.col}」列，期望 ${fmt(firstDiff.expected)}，实际 ${fmt(firstDiff.actual)}`,
      diffs,
    };
  }

  // 列名提示（不影响通过）
  const nameMismatch = actual.columns.some(
    (c, i) => String(c).toLowerCase() !== String(expected.columns[i] || '').toLowerCase()
  );
  return {
    pass: true,
    message: nameMismatch
      ? '结果正确！（提示：列名与参考答案不完全一致，建议用 AS 别名对齐）'
      : '结果正确！',
    diffs,
  };
}

function fmt(v) {
  return v === null || v === undefined ? 'NULL' : JSON.stringify(v);
}
