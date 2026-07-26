// 内置数据集：一份数据同时用于 SQLite 建表和 pandas DataFrame
// 每列定义 { name, type }，type 仅用于 SQLite 建表；rows 为原始 JS 值（null 表示 NULL/NaN）

export const DATASETS = {
  employees: {
    columns: [
      { name: 'id', type: 'INTEGER' },
      { name: 'name', type: 'TEXT' },
      { name: 'dept', type: 'TEXT' },
      { name: 'salary', type: 'REAL' },
      { name: 'hire_date', type: 'TEXT' },
      { name: 'manager_id', type: 'INTEGER' },
    ],
    rows: [
      [1,  'Alice',   'Engineering', 95000, '2019-03-15', null],
      [2,  'Bob',     'Engineering', 82000, '2020-07-01', 1],
      [3,  'Carol',   'Engineering', 78000, '2021-01-20', 1],
      [4,  'David',   'Sales',       72000, '2018-11-05', null],
      [5,  'Eva',     'Sales',       68000, '2021-06-12', 4],
      [6,  'Frank',   'Sales',       61000, '2022-02-28', 4],
      [7,  'Grace',   'Marketing',   70000, '2020-04-18', null],
      [8,  'Henry',   'Marketing',   55000, '2022-09-03', 7],
      [9,  'Ivy',     'Marketing',   58000, '2023-01-10', 7],
      [10, 'Jack',    'Engineering', 88000, '2017-08-22', 1],
      [11, 'Karen',   'HR',          62000, '2021-10-15', null],
      [12, 'Leo',     'HR',          null,  '2023-05-06', 11],
    ],
  },

  customers: {
    columns: [
      { name: 'customer_id', type: 'INTEGER' },
      { name: 'name', type: 'TEXT' },
      { name: 'city', type: 'TEXT' },
      { name: 'signup_date', type: 'TEXT' },
      { name: 'vip', type: 'INTEGER' },
    ],
    rows: [
      [101, 'Zhang Wei',  'Beijing',   '2022-01-15', 1],
      [102, 'Li Na',      'Shanghai',  '2022-03-22', 0],
      [103, 'Wang Fang',  'Beijing',   '2022-05-30', 1],
      [104, 'Chen Jie',   'Guangzhou', '2022-08-11', 0],
      [105, 'Liu Yang',   'Shanghai',  '2022-11-05', 1],
      [106, 'Zhao Min',   'Shenzhen',  '2023-02-14', 0],
      [107, 'Sun Li',     'Beijing',   '2023-04-01', 0],
      [108, 'Zhou Tao',   'Hangzhou',  '2023-06-19', 1],
      [109, 'Wu Qian',    'Shanghai',  '2023-09-27', 0],
      [110, 'Zheng Hao',  'Shenzhen',  '2023-12-08', 0],
    ],
  },

  orders: {
    columns: [
      { name: 'order_id', type: 'INTEGER' },
      { name: 'customer_id', type: 'INTEGER' },
      { name: 'product', type: 'TEXT' },
      { name: 'amount', type: 'REAL' },
      { name: 'quantity', type: 'INTEGER' },
      { name: 'order_date', type: 'TEXT' },
    ],
    rows: [
      [1001, 101, 'Laptop',     1200.00, 1, '2023-01-05'],
      [1002, 102, 'Mouse',      25.50,   2, '2023-01-08'],
      [1003, 101, 'Keyboard',   75.00,   1, '2023-01-15'],
      [1004, 103, 'Monitor',    300.00, 2, '2023-02-02'],
      [1005, 104, 'Mouse',      25.50,   1, '2023-02-10'],
      [1006, 105, 'Laptop',     1150.00, 1, '2023-02-14'],
      [1007, 101, 'Monitor',    280.00, 1, '2023-03-01'],
      [1008, 106, 'Keyboard',   75.00,   3, '2023-03-05'],
      [1009, 102, 'Laptop',     1200.00, 1, '2023-03-12'],
      [1010, 107, 'Mouse',      null,    2, '2023-03-20'],
      [1011, 103, 'Laptop',     1180.00, 1, '2023-04-02'],
      [1012, 108, 'Monitor',    300.00, 1, '2023-04-11'],
      [1013, 105, 'Keyboard',   72.50,   2, '2023-04-18'],
      [1014, 109, 'Mouse',      25.50,   4, '2023-05-01'],
      [1015, 101, 'Mouse',      24.90,   1, '2023-05-09'],
      [1016, 104, 'Laptop',     1250.00, 1, '2023-05-15'],
      [1017, 110, 'Keyboard',   75.00,   1, '2023-05-22'],
      [1018, 106, 'Monitor',    295.00, 2, '2023-06-03'],
      [1019, 102, 'Monitor',    300.00,  1, '2023-06-14'],
      [1020, 103, 'Mouse',      26.00,   2, '2023-06-21'],
      [1021, 108, 'Laptop',     1190.00, 1, '2023-07-07'],
      [1022, 105, 'Monitor',    305.00,  1, '2023-07-19'],
      [1023, 101, 'Keyboard',   75.00,   2, '2023-08-08'],
      [1024, 107, 'Laptop',     1220.00, 1, '2023-08-16'],
      [1025, 109, 'Monitor',    290.00,  1, '2023-09-02'],
      [1026, 110, 'Mouse',      25.50,   3, '2023-09-13'],
      [1027, 104, 'Keyboard',   null,    1, '2023-10-01'],
      [1028, 106, 'Laptop',     1160.00, 1, '2023-10-12'],
      [1029, 108, 'Mouse',      25.50,   2, '2023-11-05'],
      [1030, 105, 'Laptop',     1210.00, 1, '2023-11-20'],
      [1031, 101, 'Monitor',    300.00,  1, '2023-12-01'],
      [1032, 102, 'Keyboard',   74.00,   1, '2023-12-15'],
    ],
  },
};

// 生成 SQLite 建表 + 插入语句
export function buildSqliteDDL() {
  const stmts = [];
  for (const [table, def] of Object.entries(DATASETS)) {
    const cols = def.columns.map((c) => `${c.name} ${c.type}`).join(', ');
    stmts.push(`CREATE TABLE ${table} (${cols});`);
    for (const row of def.rows) {
      const vals = row
        .map((v) => {
          if (v === null || v === undefined) return 'NULL';
          if (typeof v === 'number') return String(v);
          return `'${String(v).replace(/'/g, "''")}'`;
        })
        .join(', ');
      stmts.push(`INSERT INTO ${table} VALUES (${vals});`);
    }
  }
  return stmts;
}

// 生成 Python 代码：将数据构建为 pandas DataFrame（在 Pyodide 内执行）
export function buildPandasSetupCode() {
  const lines = ['import pandas as pd', 'import numpy as np', ''];
  for (const [table, def] of Object.entries(DATASETS)) {
    const colNames = def.columns.map((c) => c.name);
    const data = def.rows.map((row) =>
      row.map((v) => {
        if (v === null || v === undefined) return 'None';
        if (typeof v === 'number') return String(v);
        return JSON.stringify(String(v));
      })
    );
    lines.push(`${table} = pd.DataFrame(`);
    lines.push(`    [${data.map((r) => '[' + r.join(', ') + ']').join(',\n     ')}],`);
    lines.push(`    columns=${JSON.stringify(colNames)})`);
    // 日期列统一转为 datetime，保证两种引擎行为一致
    for (const c of def.columns) {
      if (c.name.endsWith('_date')) {
        lines.push(`${table}['${c.name}'] = pd.to_datetime(${table}['${c.name}'])`);
      }
    }
    lines.push('');
  }
  return lines.join('\n');
}
