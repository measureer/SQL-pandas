# 校验 data/exercises.json 中 50 道题的参考答案：
#   1. 结构完整性（必填字段、id/level/topics 合法、起始代码非空等）
#   2. solutionSql 能在 SQLite 内存库执行
#   3. solutionPandas 能在 pandas 执行且产出 DataFrame 变量 result
#   4. 两侧结果一致（列名一致；忽略行序；数值容差 1e-6；None/NaN 统一；Timestamp -> 'YYYY-MM-DD'）
# 用法（cwd 为项目根）：.venv/Scripts/python.exe tools/verify.py
import json
import math
import re
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EPS = 1e-6

REQUIRED_FIELDS = [
    "id", "level", "title", "topics", "description",
    "starterSql", "starterPandas", "solutionSql", "solutionPandas", "explanation",
]
EXPECTED_IDS = (
    [f"B{i:02d}" for i in range(1, 16)]
    + [f"I{i:02d}" for i in range(1, 16)]
    + [f"A{i:02d}" for i in range(1, 21)]
)
LEVEL_OF = {"B": "beginner", "I": "intermediate", "A": "advanced"}


# ---------- 数据加载 ----------

def load_datasets():
    with open(ROOT / "tools" / "datasets.json", encoding="utf-8") as f:
        return json.load(f)


def build_sqlite(datasets):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    for table, defn in datasets.items():
        cols = ", ".join(f"{c['name']} {c['type']}" for c in defn["columns"])
        cur.execute(f"CREATE TABLE {table} ({cols});")
        placeholders = ", ".join("?" for _ in defn["columns"])
        cur.executemany(f"INSERT INTO {table} VALUES ({placeholders});", defn["rows"])
    conn.commit()
    return conn


def build_pandas(datasets):
    frames = {}
    for table, defn in datasets.items():
        names = [c["name"] for c in defn["columns"]]
        df = pd.DataFrame(defn["rows"], columns=names)
        for c in names:
            if c.endswith("_date"):
                df[c] = pd.to_datetime(df[c])
        frames[table] = df
    return frames


# ---------- 结果规范化与比对 ----------

def norm_cell(v):
    """统一单元格表示：None 表示空；数值统一 float；Timestamp 转 'YYYY-MM-DD'；其余转 str。"""
    if v is None:
        return None
    if isinstance(v, pd.Timestamp):
        return None if pd.isna(v) else v.strftime("%Y-%m-%d")
    if isinstance(v, float) and math.isnan(v):
        return None
    if isinstance(v, (np.bool_, bool)):
        return bool(v)
    if isinstance(v, (int, float, np.integer, np.floating)):
        return float(v)
    return v if isinstance(v, str) else str(v)


def sort_key_cell(v):
    if v is None:
        return (0, "")
    if isinstance(v, float):
        return (1, repr(v))
    return (2, str(v))


def sort_rows(rows):
    return sorted(rows, key=lambda r: tuple(sort_key_cell(c) for c in r))


def cells_equal(a, b):
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, float) and isinstance(b, float):
        return math.isclose(a, b, abs_tol=EPS)
    # 一侧数值一侧非数值：尝试按数值比较（如 '0' vs 0.0 不允许，必须严格）
    return str(a) == str(b)


def run_sql(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    columns = [d[0] for d in cur.description] if cur.description else []
    rows = [[norm_cell(v) for v in row] for row in cur.fetchall()]
    return columns, rows


def run_pandas(code, frames):
    ns = {
        "pd": pd,
        "np": np,
        # 每题使用独立副本，防止题目间相互污染
        **{name: df.copy() for name, df in frames.items()},
    }
    exec(compile(code, "<solutionPandas>", "exec"), ns)
    if "result" not in ns:
        raise AssertionError("solutionPandas 未定义变量 result")
    result = ns["result"]
    if not isinstance(result, pd.DataFrame):
        raise AssertionError(f"result 应为 DataFrame，实际为 {type(result).__name__}")
    result = result.reset_index(drop=True)
    columns = [str(c) for c in result.columns]
    rows = [[norm_cell(v) for v in row] for row in result.itertuples(index=False, name=None)]
    return columns, rows


def compare(sql_cols, sql_rows, pd_cols, pd_rows):
    problems = []
    if sql_cols != pd_cols:
        problems.append(f"列名不一致：SQL={sql_cols} pandas={pd_cols}")
    if len(sql_cols) != len(pd_cols):
        problems.append(f"列数不一致：SQL={len(sql_cols)} pandas={len(pd_cols)}")
        return problems
    if len(sql_rows) != len(pd_rows):
        problems.append(f"行数不一致：SQL={len(sql_rows)} pandas={len(pd_rows)}")
        return problems
    a = sort_rows(sql_rows)
    b = sort_rows(pd_rows)
    for i, (ra, rb) in enumerate(zip(a, b)):
        for j, (ca, cb) in enumerate(zip(ra, rb)):
            if not cells_equal(ca, cb):
                problems.append(
                    f"单元格不一致（排序后第 {i + 1} 行第 {j + 1} 列「{sql_cols[j]}」）："
                    f"SQL={ca!r} pandas={cb!r}"
                )
                return problems  # 报一处足够定位
    return problems


# ---------- 结构校验 ----------

def check_structure(ex, errors):
    for f in REQUIRED_FIELDS:
        if f not in ex:
            errors.append(f"缺少字段 {f}")
        elif isinstance(ex[f], str) and not ex[f].strip():
            errors.append(f"字段 {f} 为空")
    if errors:
        return
    if not re.fullmatch(r"[BIA]\d{2}", ex["id"]):
        errors.append(f"id 格式非法：{ex['id']!r}")
    elif ex["level"] != LEVEL_OF[ex["id"][0]]:
        errors.append(f"level 与 id 前缀不符：id={ex['id']} level={ex['level']}")
    if not isinstance(ex["topics"], list) or not (2 <= len(ex["topics"]) <= 3):
        errors.append(f"topics 应为 2-3 个标签，实际：{ex['topics']!r}")
    if "result" not in ex["solutionPandas"]:
        errors.append("solutionPandas 中未出现 result 变量")


# ---------- 主流程 ----------

def main():
    with open(ROOT / "data" / "exercises.json", encoding="utf-8") as f:
        exercises = json.load(f)

    datasets = load_datasets()
    conn = build_sqlite(datasets)
    frames = build_pandas(datasets)

    failures = 0

    # 全局结构
    ids = [e.get("id") for e in exercises]
    if len(exercises) != 50:
        print(f"FAIL [global] 题目数量应为 50，实际 {len(exercises)}")
        failures += 1
    if len(set(ids)) != len(ids):
        print("FAIL [global] 存在重复 id")
        failures += 1
    if sorted(ids) != sorted(EXPECTED_IDS):
        print(f"FAIL [global] id 集合不符，缺少 {sorted(set(EXPECTED_IDS) - set(ids))}，"
              f"多出 {sorted(set(ids) - set(EXPECTED_IDS))}")
        failures += 1

    for ex in exercises:
        eid = ex.get("id", "<无 id>")
        errors = []
        check_structure(ex, errors)

        if not errors:
            try:
                sql_cols, sql_rows = run_sql(conn, ex["solutionSql"])
            except Exception as e:
                errors.append(f"solutionSql 执行失败：{e}")
                sql_cols = sql_rows = None

            try:
                pd_cols, pd_rows = run_pandas(ex["solutionPandas"], frames)
            except Exception as e:
                errors.append(f"solutionPandas 执行失败：{type(e).__name__}: {e}")
                pd_cols = pd_rows = None

            if sql_cols is not None and pd_cols is not None:
                errors.extend(compare(sql_cols, sql_rows, pd_cols, pd_rows))

        if errors:
            failures += 1
            print(f"FAIL [{eid}]")
            for err in errors:
                print(f"      - {err}")
        else:
            print(f"PASS [{eid}] {ex['title']}")

    total = len(exercises)
    passed = total - failures
    print("-" * 60)
    print(f"汇总：{passed}/{total} PASS" + (f"，{failures} 个 FAIL" if failures else "，全部通过"))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
