# SQL × Pandas 对照练习

一个纯前端的对照练习网站：同一道题，分别用 **SQL** 和 **pandas** 各写一遍，加深对两种数据处理方式的对应理解。无需后端、无需安装数据库，所有计算都在浏览器里完成。

## 功能

- **50 道练习题**：入门 15 道、进阶 15 道、精通 20 道，覆盖过滤、聚合、连接、窗口函数等常见知识点
- **双引擎对照**：SQL 由 [sql.js](https://github.com/sql-js/sql.js)（SQLite WASM）执行，pandas 由 [Pyodide](https://pyodide.org/)（Python WASM，本地 vendor，可离线）执行
- **自动判题**：运行后与期望结果逐格对比，不一致的单元格高亮标出
- **查看答案**：参考答案在编辑器下方独立展示，不覆盖你的代码
- **分语言重置**：在 SQL 标签页点"重置代码"只重置 SQL，pandas 代码不受影响（反之亦然）
- **进度持久化**：代码草稿、通过状态、收藏、笔记均保存在浏览器 localStorage，支持导出 / 导入 JSON
- **WebDAV 云端同步**：可把进度与笔记备份到 WebDAV 服务器（顶栏「WebDAV」按钮），支持手动上传 / 恢复与本地保存后自动上传
- **内置数据集**：employees、departments、orders 三张示例表，右栏可查看 Schema

## 快速开始

由于使用了 ES Module 和 WASM，需要通过 HTTP 服务访问（不能直接双击打开 `index.html`）：

```bash
# 方式一：Python
python -m http.server 8765

# 方式二：Node
npx serve .
```

Windows 用户也可以直接双击 `启动网站.bat`（macOS / Linux 用 `启动网站.sh`），然后访问 http://localhost:8765/ 。

## 目录结构

```
├── index.html          # 页面结构
├── css/style.css       # 样式
├── js/
│   ├── app.js          # 主逻辑：题目列表、编辑器、判题、进度、笔记
│   ├── sql-runner.js   # sql.js 执行封装
│   ├── pandas-runner.js# Pyodide 执行封装
│   ├── compare.js      # 结果对比
│   ├── datasets.js     # 数据集定义与建表代码生成
│   ├── storage.js      # localStorage 进度 / 笔记
│   └── webdav.js       # WebDAV 云端同步
├── data/exercises.js   # 题库（由 data/exercises.json 生成）
├── tools/              # 题库构建、数据集导出、校验脚本
└── vendor/pyodide/     # 本地 Pyodide（离线可用）
```

## 维护题库

题目维护在 `data/exercises.json`，修改后重新生成 JS 并校验：

```bash
python tools/build_exercises.py   # 生成 data/exercises.js
python tools/verify.py            # 校验答案与期望结果一致
```

## WebDAV 同步说明

浏览器直连 WebDAV 要求服务端返回 CORS 头（`Access-Control-Allow-Origin` 等），并放行
`PROPFIND`、`PUT`、`GET` 方法与 `Authorization`、`Depth`、`Content-Type` 请求头。
坚果云等常见服务不支持浏览器跨域，可用 Alist / Cloudreve 自建网盘，或用 Nginx 反代为
WebDAV 服务附加 CORS 头。服务器地址应填到目录级（如 `https://example.com/dav/backup/`），
备份文件名默认 `sql-pandas-progress.json`。密码仅保存在本机浏览器 localStorage。

## 技术栈

- 原生 HTML / CSS / JavaScript（ES Module），无构建步骤
- [CodeMirror 5](https://codemirror.net/5/)（CDN）：SQL / Python 编辑器
- [sql.js](https://github.com/sql-js/sql.js)（CDN）：浏览器内 SQLite
- [Pyodide](https://pyodide.org/)（本地 vendor）：浏览器内 Python + pandas
