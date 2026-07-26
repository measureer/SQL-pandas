// 把 js/datasets.js 中的内置数据集导出为 tools/datasets.json，供 tools/verify.py 使用
// 用法（cwd 为项目根）：node tools/dump_datasets.mjs
import { DATASETS } from '../js/datasets.js';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const out = {};
for (const [table, def] of Object.entries(DATASETS)) {
  out[table] = {
    columns: def.columns.map((c) => ({ name: c.name, type: c.type })),
    rows: def.rows,
  };
}

const target = fileURLToPath(new URL('./datasets.json', import.meta.url));
writeFileSync(target, JSON.stringify(out, null, 2) + '\n', 'utf8');
console.log(`written: ${target}`);
console.log(`tables: ${Object.keys(out).join(', ')}`);
