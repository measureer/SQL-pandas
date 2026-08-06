# 生成 data/exercises.json（50 道题）与 data/exercises.js（供 js/app.js import）
# 用法（cwd 为项目根）：.venv/Scripts/python.exe tools/build_exercises.py
#
# starterPandas 编写原则：样板代码（最终选列、result 赋值、reset_index 等）全部预填，
# 只把本题考察的核心逻辑留空（用 ... 或空列表 + TODO 注释标记）。
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

E = []  # exercises


def ex(**kw):
    E.append(kw)


# ============ 入门 Beginner B01-B15 ============

ex(
    id="B01", level="beginner", title="选择指定列",
    topics=["SELECT", "列选择"],
    description="从 <code>employees</code> 表中查询所有员工的姓名和部门。<br>输出两列，列名依次为 <code>name</code>、<code>dept</code>。",
    starterSql="SELECT\n    -- 在这里填写要查询的列名\nFROM employees;",
    starterPandas="# 用双方括号选择需要的列，结果赋值给 result\nresult = employees[['name']]  # TODO: 还需要 dept 列",
    solutionSql="SELECT name, dept\nFROM employees;",
    solutionPandas="result = employees[['name', 'dept']].reset_index(drop=True)",
    explanation="SQL 用 <code>SELECT name, dept</code> 指定要输出的列；pandas 用双方括号 <code>employees[['name', 'dept']]</code> 选列，得到的就是一个只含这两列的 DataFrame。",
)

ex(
    id="B02", level="beginner", title="WHERE 过滤行",
    topics=["WHERE", "过滤"],
    description="查询 Engineering 部门的所有员工，输出<b>全部列</b>（列顺序与表结构一致）。",
    starterSql="SELECT *\nFROM employees\n-- 在这里补全 WHERE 条件;",
    starterPandas="# 布尔过滤：先构造条件 mask，再用 employees[mask] 筛行\nmask = ...  # TODO: dept 等于 'Engineering' 的条件\nresult = employees[mask].reset_index(drop=True)",
    solutionSql="SELECT *\nFROM employees\nWHERE dept = 'Engineering';",
    solutionPandas="result = employees[employees['dept'] == 'Engineering'].reset_index(drop=True)",
    explanation="SQL 的 <code>WHERE dept = 'Engineering'</code> 对应 pandas 的布尔索引 <code>employees[employees['dept'] == 'Engineering']</code>。注意 pandas 中判断相等要用 <code>==</code>。",
)

ex(
    id="B03", level="beginner", title="ORDER BY 与 LIMIT",
    topics=["ORDER BY", "LIMIT", "排序"],
    description="查询薪资最高的 3 名员工。<br>输出两列：<code>name</code>、<code>salary</code>，按薪资从高到低排列。",
    starterSql="SELECT name, salary\nFROM employees\n-- 在这里补全排序和行数限制;",
    starterPandas="# sort_values 排序 + head 取前 N 行\ntop = ...  # TODO: 按 salary 降序排序并取前 3 行\nresult = top[['name', 'salary']].reset_index(drop=True)",
    solutionSql="SELECT name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT 3;",
    solutionPandas="result = (employees.sort_values('salary', ascending=False)\n          .head(3)\n          [['name', 'salary']]\n          .reset_index(drop=True))",
    explanation="<code>ORDER BY salary DESC LIMIT 3</code> 对应 pandas 的 <code>sort_values('salary', ascending=False).head(3)</code>。pandas 排序时 NaN 默认排在最后，与 SQLite 中 NULL 在 DESC 时排最后一致。",
)

ex(
    id="B04", level="beginner", title="DISTINCT 去重",
    topics=["DISTINCT", "去重"],
    description="查询公司一共有哪些部门（去重）。<br>输出单列 <code>dept</code>。",
    starterSql="SELECT -- 在这里补全去重关键字\n    dept\nFROM employees;",
    starterPandas="result = employees[['dept']]  # TODO: 补上去重（drop_duplicates）\nresult = result.reset_index(drop=True)",
    solutionSql="SELECT DISTINCT dept\nFROM employees;",
    solutionPandas="result = employees[['dept']].drop_duplicates().reset_index(drop=True)",
    explanation="<code>SELECT DISTINCT dept</code> 对应 pandas 的 <code>employees[['dept']].drop_duplicates()</code>。判题忽略行序，所以不需要额外排序。",
)

ex(
    id="B05", level="beginner", title="AND 与 OR 组合条件",
    topics=["WHERE", "AND/OR", "逻辑运算"],
    description="查询 Sales 部门中薪资低于 65000 <b>或</b>高于 70000 的员工。<br>输出三列：<code>name</code>、<code>dept</code>、<code>salary</code>。<br>注意 AND 优先级高于 OR，请用括号明确分组。",
    starterSql="SELECT name, dept, salary\nFROM employees\nWHERE dept = 'Sales'\n  -- 在这里补全 AND/OR 组合条件（记得加括号）;",
    starterPandas="# pandas 中 & 表示 AND，| 表示 OR，每个比较条件都要加括号\nmask = (employees['dept'] == 'Sales')  # TODO: 再 & 上一个 (薪资<65000 | 薪资>70000) 的条件\nresult = employees[mask][['name', 'dept', 'salary']].reset_index(drop=True)",
    solutionSql="SELECT name, dept, salary\nFROM employees\nWHERE dept = 'Sales'\n  AND (salary < 65000 OR salary > 70000);",
    solutionPandas="result = (employees[(employees['dept'] == 'Sales')\n          & ((employees['salary'] < 65000) | (employees['salary'] > 70000))]\n          [['name', 'dept', 'salary']]\n          .reset_index(drop=True))",
    explanation="SQL 用 <code>AND</code>/<code>OR</code>，pandas 用 <code>&amp;</code>/<code>|</code>，且 pandas 中每个比较条件都必须用括号包起来，否则运算符优先级会出错。",
)

ex(
    id="B06", level="beginner", title="IN 集合匹配",
    topics=["IN", "集合匹配"],
    description="查询位于 Beijing 或 Shanghai 的客户。<br>输出两列：<code>name</code>、<code>city</code>。",
    starterSql="SELECT name, city\nFROM customers\n-- 用 IN 补全条件;",
    starterPandas="# 用 isin 判断是否在集合中\nmask = customers['city'].isin([])  # TODO: 在列表中填入两个城市名\nresult = customers[mask][['name', 'city']].reset_index(drop=True)",
    solutionSql="SELECT name, city\nFROM customers\nWHERE city IN ('Beijing', 'Shanghai');",
    solutionPandas="result = (customers[customers['city'].isin(['Beijing', 'Shanghai'])]\n          [['name', 'city']]\n          .reset_index(drop=True))",
    explanation="<code>WHERE city IN ('Beijing', 'Shanghai')</code> 对应 pandas 的 <code>customers['city'].isin(['Beijing', 'Shanghai'])</code>，比写多个 OR 更简洁。",
)

ex(
    id="B07", level="beginner", title="BETWEEN 范围过滤",
    topics=["BETWEEN", "范围过滤"],
    description="查询金额（amount）在 100 到 500 之间（含边界）的订单。<br>输出三列：<code>order_id</code>、<code>product</code>、<code>amount</code>。<br>注意：金额为 NULL 的订单会被条件自动排除。",
    starterSql="SELECT order_id, product, amount\nFROM orders\n-- 用 BETWEEN 补全条件;",
    starterPandas="# 用 between 判断范围（含边界）\nmask = ...  # TODO: amount 在 100~500 之间的条件\nresult = orders[mask][['order_id', 'product', 'amount']].reset_index(drop=True)",
    solutionSql="SELECT order_id, product, amount\nFROM orders\nWHERE amount BETWEEN 100 AND 500;",
    solutionPandas="result = (orders[orders['amount'].between(100, 500)]\n          [['order_id', 'product', 'amount']]\n          .reset_index(drop=True))",
    explanation="<code>amount BETWEEN 100 AND 500</code> 等价于 <code>amount &gt;= 100 AND amount &lt;= 500</code>，对应 pandas 的 <code>orders['amount'].between(100, 500)</code>。两侧对 NULL/NaN 的比较结果都是「不满足条件」，行为一致。",
)

ex(
    id="B08", level="beginner", title="LIKE 模糊匹配",
    topics=["LIKE", "模式匹配"],
    description="查询姓名以字母 Z 开头的客户。<br>输出两列：<code>name</code>、<code>city</code>。<br>提示：SQL 中 <code>%</code> 匹配任意多个字符。",
    starterSql="SELECT name, city\nFROM customers\n-- 用 LIKE 补全条件;",
    starterPandas="# 用 str.startswith 判断前缀\nmask = customers['name'].str.startswith('')  # TODO: 填入前缀\nresult = customers[mask][['name', 'city']].reset_index(drop=True)",
    solutionSql="SELECT name, city\nFROM customers\nWHERE name LIKE 'Z%';",
    solutionPandas="result = (customers[customers['name'].str.startswith('Z')]\n          [['name', 'city']]\n          .reset_index(drop=True))",
    explanation="<code>name LIKE 'Z%'</code> 对应 pandas 的 <code>customers['name'].str.startswith('Z')</code>。更复杂的模式（如含中间字符）可以用 <code>str.contains</code>。",
)

ex(
    id="B09", level="beginner", title="NULL 值判断",
    topics=["NULL", "IS NULL"],
    description="查询还没有分配经理的员工（manager_id 为 NULL）。<br>输出两列：<code>name</code>、<code>dept</code>。<br>注意：判断 NULL 不能用 <code>= NULL</code>。",
    starterSql="SELECT name, dept\nFROM employees\n-- 用 IS NULL 补全条件;",
    starterPandas="# 用 isna() 判断缺失值\nmask = ...  # TODO: manager_id 为缺失值的条件\nresult = employees[mask][['name', 'dept']].reset_index(drop=True)",
    solutionSql="SELECT name, dept\nFROM employees\nWHERE manager_id IS NULL;",
    solutionPandas="result = (employees[employees['manager_id'].isna()]\n          [['name', 'dept']]\n          .reset_index(drop=True))",
    explanation="SQL 用 <code>IS NULL</code> / <code>IS NOT NULL</code> 判断空值（<code>= NULL</code> 永远不为真）；pandas 对应 <code>.isna()</code> / <code>.notna()</code>。",
)

ex(
    id="B10", level="beginner", title="简单聚合 COUNT / SUM",
    topics=["聚合", "COUNT", "SUM"],
    description="统计订单表的总订单数和所有订单的总金额（amount 求和时自动忽略 NULL）。<br>输出两列：<code>order_count</code>、<code>total_amount</code>，结果只有一行。",
    starterSql="SELECT\n    -- 在这里写聚合表达式，并用 AS 起别名\nFROM orders;",
    starterPandas="# len() 统计行数，sum() 求和（自动跳过 NaN）\nresult = pd.DataFrame({\n    'order_count': [...],   # TODO: 订单总行数\n    'total_amount': [...],  # TODO: amount 求和\n})",
    solutionSql="SELECT COUNT(*) AS order_count,\n       SUM(amount) AS total_amount\nFROM orders;",
    solutionPandas="result = pd.DataFrame({\n    'order_count': [len(orders)],\n    'total_amount': [orders['amount'].sum()],\n})",
    explanation="SQL 的 <code>COUNT(*)</code> 统计行数、<code>SUM(amount)</code> 忽略 NULL；pandas 对应 <code>len(orders)</code> 和 <code>orders['amount'].sum()</code>（默认 skipna=True）。单行结果可以用 <code>pd.DataFrame({...})</code> 直接构造。",
)

ex(
    id="B11", level="beginner", title="计算列与别名",
    topics=["计算列", "别名", "算术运算"],
    description="查询每笔订单的编号、产品，并计算单笔总额（amount × quantity）。<br>输出三列：<code>order_id</code>、<code>product</code>、<code>total_price</code>。<br>注意：amount 为 NULL 的订单，总额也是 NULL。",
    starterSql="SELECT order_id,\n       product,\n       -- 在这里补全计算列，并用 AS 起别名 total_price\nFROM orders;",
    starterPandas="result = orders[['order_id', 'product']].copy()\nresult['total_price'] = ...  # TODO: amount 列乘以 quantity 列",
    solutionSql="SELECT order_id,\n       product,\n       amount * quantity AS total_price\nFROM orders;",
    solutionPandas="result = orders[['order_id', 'product']].copy()\nresult['total_price'] = orders['amount'] * orders['quantity']",
    explanation="SQL 里算术表达式可以直接写在 SELECT 中并用 <code>AS</code> 起别名；pandas 里用列与列的运算生成新列 <code>orders['amount'] * orders['quantity']</code>。两侧遇到 NULL/NaN 都会得到空值。",
)

ex(
    id="B12", level="beginner", title="不等于过滤",
    topics=["WHERE", "不等于", "过滤"],
    description="查询<b>不在</b> Engineering 部门的员工。<br>输出两列：<code>name</code>、<code>dept</code>。",
    starterSql="SELECT name, dept\nFROM employees\n-- 用 <> 补全「不等于」条件;",
    starterPandas="# pandas 中不等于用 !=\nmask = ...  # TODO: dept 不等于 'Engineering' 的条件\nresult = employees[mask][['name', 'dept']].reset_index(drop=True)",
    solutionSql="SELECT name, dept\nFROM employees\nWHERE dept <> 'Engineering';",
    solutionPandas="result = (employees[employees['dept'] != 'Engineering']\n          [['name', 'dept']]\n          .reset_index(drop=True))",
    explanation="SQL 中「不等于」写作 <code>&lt;&gt;</code>（或 <code>!=</code>）；pandas 中写作 <code>!=</code>。文本比较在两侧都是区分大小写的精确匹配。",
)

ex(
    id="B13", level="beginner", title="按表达式排序",
    topics=["ORDER BY", "表达式排序"],
    description="查询所有订单，按单笔总额（amount × quantity）从高到低排列。<br>输出四列：<code>order_id</code>、<code>product</code>、<code>amount</code>、<code>quantity</code>。",
    starterSql="SELECT order_id, product, amount, quantity\nFROM orders\n-- ORDER BY 里可以直接写表达式，补全按总额降序排序;",
    starterPandas="d = orders.copy()\nd['total_price'] = ...  # TODO: amount * quantity\nd = ...  # TODO: 按 total_price 降序排序（sort_values）\nresult = d[['order_id', 'product', 'amount', 'quantity']].reset_index(drop=True)",
    solutionSql="SELECT order_id, product, amount, quantity\nFROM orders\nORDER BY amount * quantity DESC;",
    solutionPandas="d = orders.copy()\nd['total_price'] = d['amount'] * d['quantity']\nd = d.sort_values('total_price', ascending=False)\nresult = d[['order_id', 'product', 'amount', 'quantity']].reset_index(drop=True)",
    explanation="SQL 的 ORDER BY 可以直接写表达式 <code>ORDER BY amount * quantity DESC</code>；pandas 的 <code>sort_values</code> 只能按列排序，所以要先用 <code>assign</code> 或直接赋值造出计算列再排序。",
)

ex(
    id="B14", level="beginner", title="COUNT(*) 统计行数",
    topics=["聚合", "COUNT"],
    description="统计公司一共有多少名员工。<br>输出单列 <code>emp_count</code>，结果只有一行。",
    starterSql="SELECT\n    -- 用 COUNT(*) 统计行数，别名 emp_count\nFROM employees;",
    starterPandas="result = pd.DataFrame({\n    'emp_count': [...],  # TODO: 员工总数（len）\n})",
    solutionSql="SELECT COUNT(*) AS emp_count\nFROM employees;",
    solutionPandas="result = pd.DataFrame({'emp_count': [len(employees)]})",
    explanation="<code>COUNT(*)</code> 统计所有行（不忽略 NULL），对应 pandas 的 <code>len(employees)</code>；而 <code>COUNT(某列)</code> 会忽略该列为 NULL 的行，对应 <code>df['某列'].count()</code>。",
)

ex(
    id="B15", level="beginner", title="LIMIT 与 OFFSET 分页",
    topics=["LIMIT", "OFFSET", "分页"],
    description="查询金额第 4 到第 6 高的订单（即跳过前 3 名，再取 3 行）。<br>输出三列：<code>order_id</code>、<code>product</code>、<code>amount</code>。",
    starterSql="SELECT order_id, product, amount\nFROM orders\nORDER BY amount DESC\n-- 用 LIMIT ... OFFSET ... 跳过前 3 行再取 3 行;",
    starterPandas="# iloc 按位置切片：第 4~6 行即 iloc[3:6]\nd = ...  # TODO: 按 amount 降序排序（NaN 会自动排在最后）\nresult = d.iloc[3:6][['order_id', 'product', 'amount']].reset_index(drop=True)",
    solutionSql="SELECT order_id, product, amount\nFROM orders\nORDER BY amount DESC\nLIMIT 3 OFFSET 3;",
    solutionPandas="d = orders.sort_values('amount', ascending=False)\nresult = d.iloc[3:6][['order_id', 'product', 'amount']].reset_index(drop=True)",
    explanation="<code>LIMIT 3 OFFSET 3</code> 表示跳过前 3 行再取 3 行，是分页查询的基础；pandas 对应位置切片 <code>.iloc[3:6]</code>。排序后金额并列的两笔 1200 都在第 4、5 名，不影响结果集。",
)

# ============ 进阶 Intermediate I01-I15 ============

ex(
    id="I01", level="intermediate", title="GROUP BY 分组聚合",
    topics=["GROUP BY", "聚合", "AVG"],
    description="统计每个部门的员工人数和平均薪资。<br>输出三列：<code>dept</code>、<code>emp_count</code>、<code>avg_salary</code>。<br>（AVG 会自动忽略 salary 为 NULL 的员工。）",
    starterSql="SELECT dept,\n       -- 在这里补全聚合表达式与别名\nFROM employees\n-- 补全分组;",
    starterPandas="# 命名聚合：agg(新列名=('原列名', '聚合函数'))\nresult = employees.groupby('dept', as_index=False).agg(\n    emp_count=('id', 'count'),  # 示例：按 id 计数\n    avg_salary=...,             # TODO: salary 的平均值\n)",
    solutionSql="SELECT dept,\n       COUNT(*) AS emp_count,\n       AVG(salary) AS avg_salary\nFROM employees\nGROUP BY dept;",
    solutionPandas="result = (employees.groupby('dept', as_index=False)\n          .agg(emp_count=('id', 'count'),\n               avg_salary=('salary', 'mean')))",
    explanation="<code>GROUP BY dept</code> 对应 <code>groupby('dept')</code>；SQL 的 <code>AVG(salary)</code> 忽略 NULL，pandas 的 <code>mean</code> 默认跳过 NaN，结果一致。用命名聚合 <code>agg(别名=('列', '函数'))</code> 可以直接得到与 SQL 别名一致的列名。",
)

ex(
    id="I02", level="intermediate", title="HAVING 过滤分组",
    topics=["HAVING", "GROUP BY"],
    description="找出累计消费金额（amount 之和）超过 1500 的客户。<br>输出两列：<code>customer_id</code>、<code>total_amount</code>。",
    starterSql="SELECT customer_id,\n       SUM(amount) AS total_amount\nFROM orders\nGROUP BY customer_id\n-- 补全对分组结果的过滤条件;",
    starterPandas="# 先聚合，再按聚合结果过滤（pandas 没有 HAVING）\ng = (orders.groupby('customer_id', as_index=False)['amount'].sum()\n     .rename(columns={'amount': 'total_amount'}))\nmask = ...  # TODO: total_amount 大于 1500 的条件\nresult = g[mask].reset_index(drop=True)",
    solutionSql="SELECT customer_id,\n       SUM(amount) AS total_amount\nFROM orders\nGROUP BY customer_id\nHAVING SUM(amount) > 1500;",
    solutionPandas="g = (orders.groupby('customer_id', as_index=False)['amount'].sum()\n     .rename(columns={'amount': 'total_amount'}))\nresult = g[g['total_amount'] > 1500].reset_index(drop=True)",
    explanation="WHERE 过滤的是行，HAVING 过滤的是分组后的结果。pandas 没有 HAVING 的概念，做法就是「先聚合、再按聚合结果过滤」两步走。",
)

ex(
    id="I03", level="intermediate", title="多列排序",
    topics=["ORDER BY", "多列排序"],
    description="查询所有员工的 <code>name</code>、<code>dept</code>、<code>salary</code> 三列。<br>排序要求：先按部门升序，部门内部再按薪资降序。",
    starterSql="SELECT name, dept, salary\nFROM employees\n-- 补全多列排序;",
    starterPandas="# sort_values 可以传列名列表和升降序列表，两个列表按位置一一对应\nd = employees.sort_values(['dept'], ascending=[True])  # TODO: 补上第二个排序键：salary 降序\nresult = d[['name', 'dept', 'salary']].reset_index(drop=True)",
    solutionSql="SELECT name, dept, salary\nFROM employees\nORDER BY dept ASC, salary DESC;",
    solutionPandas="result = (employees.sort_values(['dept', 'salary'], ascending=[True, False])\n          [['name', 'dept', 'salary']]\n          .reset_index(drop=True))",
    explanation="<code>ORDER BY dept ASC, salary DESC</code> 对应 <code>sort_values(['dept', 'salary'], ascending=[True, False])</code>，两个列表按位置一一对应。",
)

ex(
    id="I04", level="intermediate", title="INNER JOIN 内连接",
    topics=["JOIN", "INNER JOIN"],
    description="查询每笔订单对应的客户姓名。<br>输出四列：<code>order_id</code>、<code>customer_name</code>、<code>product</code>、<code>amount</code>。",
    starterSql="SELECT o.order_id,\n       c.name AS customer_name,\n       o.product,\n       o.amount\nFROM orders o\n-- 补全 JOIN 子句;",
    starterPandas="# 用 merge 连接两张表（连接键：customer_id），customers 侧只带 name 列\nm = ...  # TODO: orders.merge(customers[[...]], on=..., how='inner')\nm = m.rename(columns={'name': 'customer_name'})\nresult = m[['order_id', 'customer_name', 'product', 'amount']].reset_index(drop=True)",
    solutionSql="SELECT o.order_id,\n       c.name AS customer_name,\n       o.product,\n       o.amount\nFROM orders o\nINNER JOIN customers c ON o.customer_id = c.customer_id;",
    solutionPandas="m = orders.merge(customers[['customer_id', 'name']], on='customer_id', how='inner')\nm = m.rename(columns={'name': 'customer_name'})\nresult = m[['order_id', 'customer_name', 'product', 'amount']].reset_index(drop=True)",
    explanation="<code>INNER JOIN ... ON</code> 对应 <code>merge(..., on='customer_id', how='inner')</code>。SQL 里用 <code>AS</code> 给列起别名，pandas 里用 <code>rename(columns={...})</code>。",
)

ex(
    id="I05", level="intermediate", title="LEFT JOIN 保留未匹配行",
    topics=["LEFT JOIN", "聚合"],
    description="统计每位客户购买 Laptop 的订单数，<b>包括一次都没买过的客户（显示 0）</b>。<br>输出两列：<code>name</code>、<code>laptop_orders</code>（共 10 行）。<br>提示：把 <code>product = 'Laptop'</code> 放在 JOIN 条件里而不是 WHERE 里，才能保留没买过 Laptop 的客户——这正是 LEFT JOIN 与 INNER JOIN 的差别。",
    starterSql="SELECT c.name,\n       COUNT(o.order_id) AS laptop_orders\nFROM customers c\n-- 补全 LEFT JOIN（注意 product 条件的位置）\nGROUP BY c.customer_id, c.name;",
    starterPandas="# 第一步：先统计每个客户的 Laptop 订单数（已给出）\nlaptop = (orders[orders['product'] == 'Laptop']\n          .groupby('customer_id').size().rename('laptop_orders'))\n# 第二步：LEFT 连接回客户表，没买过的填 0\nresult = customers[['customer_id', 'name']].merge(laptop, on='customer_id', how=...)  # TODO: 指定连接方式\nresult['laptop_orders'] = ...  # TODO: 缺失值填 0 并转为整数（fillna + astype）\nresult = result[['name', 'laptop_orders']]",
    solutionSql="SELECT c.name,\n       COUNT(o.order_id) AS laptop_orders\nFROM customers c\nLEFT JOIN orders o\n  ON o.customer_id = c.customer_id\n AND o.product = 'Laptop'\nGROUP BY c.customer_id, c.name;",
    solutionPandas="laptop = (orders[orders['product'] == 'Laptop']\n          .groupby('customer_id')\n          .size()\n          .rename('laptop_orders'))\nresult = (customers[['customer_id', 'name']]\n          .merge(laptop, on='customer_id', how='left'))\nresult['laptop_orders'] = result['laptop_orders'].fillna(0).astype(int)\nresult = result[['name', 'laptop_orders']]",
    explanation="SQL 中把 <code>o.product = 'Laptop'</code> 写在 ON 里，左表客户全部保留，没匹配上的计数为 0；若写在 WHERE 里就会退化成 INNER JOIN。pandas 的做法是「先按条件聚合出右表，再 <code>merge(how='left')</code> + <code>fillna(0)</code>」，语义完全对应。",
)

ex(
    id="I06", level="intermediate", title="子查询",
    topics=["子查询", "WHERE"],
    description="查询薪资高于全公司平均薪资的员工。<br>输出两列：<code>name</code>、<code>salary</code>。",
    starterSql="SELECT name, salary\nFROM employees\nWHERE salary > (\n    -- 在这里写计算平均薪资的子查询\n);",
    starterPandas="# 先算平均值（mean 自动跳过 NaN），再过滤\navg_salary = employees['salary'].mean()\nmask = ...  # TODO: salary 高于 avg_salary 的条件\nresult = employees[mask][['name', 'salary']].reset_index(drop=True)",
    solutionSql="SELECT name, salary\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);",
    solutionPandas="avg_salary = employees['salary'].mean()\nresult = (employees[employees['salary'] > avg_salary]\n          [['name', 'salary']]\n          .reset_index(drop=True))",
    explanation="SQL 的子查询 <code>(SELECT AVG(salary) FROM employees)</code> 在 pandas 里就是先算出一个标量 <code>employees['salary'].mean()</code>，再拿它做过滤——子查询往往对应 pandas 里的「中间变量」。",
)

ex(
    id="I07", level="intermediate", title="CASE WHEN 条件分支",
    topics=["CASE WHEN", "条件逻辑"],
    description="为员工打薪资等级标签：<br>· 薪资 &gt;= 80000 → <code>High</code><br>· 薪资 &gt;= 60000 → <code>Mid</code><br>· 其余 → <code>Low</code><br>· 薪资为 NULL → <code>Unknown</code><br>输出三列：<code>name</code>、<code>salary</code>、<code>salary_level</code>。",
    starterSql="SELECT name,\n       salary,\n       CASE\n         -- 在这里补全 WHEN 分支（注意先判断 NULL）\n       END AS salary_level\nFROM employees;",
    starterPandas="# 用 np.select(条件列表, 取值列表, default=...) 实现多分支\nconditions = []  # TODO: 三个条件，按优先级排列（先判 isna，再 >=80000，再 >=60000）\nchoices = []     # TODO: 对应的 'Unknown' / 'High' / 'Mid'\nresult = employees[['name', 'salary']].copy()\nresult['salary_level'] = np.select(conditions, choices, default='Low')",
    solutionSql="SELECT name,\n       salary,\n       CASE\n         WHEN salary IS NULL THEN 'Unknown'\n         WHEN salary >= 80000 THEN 'High'\n         WHEN salary >= 60000 THEN 'Mid'\n         ELSE 'Low'\n       END AS salary_level\nFROM employees;",
    solutionPandas="conditions = [\n    employees['salary'].isna(),\n    employees['salary'] >= 80000,\n    employees['salary'] >= 60000,\n]\nchoices = ['Unknown', 'High', 'Mid']\nresult = employees[['name', 'salary']].copy()\nresult['salary_level'] = np.select(conditions, choices, default='Low')",
    explanation="SQL 的 <code>CASE WHEN ... END</code> 按顺序匹配第一个为真的分支；pandas 的 <code>np.select(conditions, choices, default=...)</code> 同样按顺序取第一个满足的条件，两者一一对应。注意 NULL/NaN 的判断要放在最前面，因为 <code>NULL &gt;= 80000</code> 和 <code>NaN &gt;= 80000</code> 都不为真。",
)

ex(
    id="I08", level="intermediate", title="字符串处理",
    topics=["字符串", "UPPER", "LENGTH"],
    description="将客户姓名转为大写，并计算姓名的字符数。<br>输出两列：<code>name_upper</code>、<code>name_length</code>。",
    starterSql="SELECT\n    -- 用 UPPER() 和 LENGTH() 补全，并起别名\nFROM customers;",
    starterPandas="# pandas 字符串方法在 .str 命名空间下\nresult = pd.DataFrame({\n    'name_upper': customers['name'],   # TODO: 转为大写\n    'name_length': customers['name'],  # TODO: 计算字符数\n})",
    solutionSql="SELECT UPPER(name) AS name_upper,\n       LENGTH(name) AS name_length\nFROM customers;",
    solutionPandas="result = pd.DataFrame({\n    'name_upper': customers['name'].str.upper(),\n    'name_length': customers['name'].str.len(),\n}).reset_index(drop=True)",
    explanation="SQL 的字符串函数 <code>UPPER()</code>、<code>LENGTH()</code> 在 pandas 中对应 <code>.str.upper()</code>、<code>.str.len()</code>。pandas 的字符串方法统一挂在 <code>.str</code> 访问器下。",
)

ex(
    id="I09", level="intermediate", title="日期过滤",
    topics=["日期", "WHERE", ".dt"],
    description="查询 2023 年第二季度（2023-04-01 至 2023-06-30）的订单。<br>输出四列：<code>order_id</code>、<code>product</code>、<code>amount</code>、<code>order_date</code>。<br>提示：SQL 中日期是 TEXT，可直接按字符串比较；pandas 中 order_date 已是 datetime64，也可以直接与日期字符串比较。",
    starterSql="SELECT order_id, product, amount, order_date\nFROM orders\n-- 用日期范围条件补全（也可用 strftime）;",
    starterPandas="# order_date 已是 datetime64，可与 'YYYY-MM-DD' 字符串直接比较\nmask = (orders['order_date'] >= '2023-04-01')  # TODO: 用 & 补上上界条件（< '2023-07-01'）\nresult = orders[mask][['order_id', 'product', 'amount', 'order_date']].reset_index(drop=True)",
    solutionSql="SELECT order_id, product, amount, order_date\nFROM orders\nWHERE order_date >= '2023-04-01'\n  AND order_date <  '2023-07-01';",
    solutionPandas="mask = (orders['order_date'] >= '2023-04-01') & (orders['order_date'] < '2023-07-01')\nresult = (orders[mask]\n          [['order_id', 'product', 'amount', 'order_date']]\n          .reset_index(drop=True))",
    explanation="ISO 格式（YYYY-MM-DD）的日期字符串按字典序比较等价于按时间比较，所以 SQL 里可以直接写 <code>order_date &gt;= '2023-04-01'</code>；若要按月份提取，SQL 用 <code>strftime('%m', order_date)</code>，pandas 用 <code>orders['order_date'].dt.month</code>。本题用「&gt;= 下界 且 &lt; 上界」的半开区间写法最稳妥。",
)

ex(
    id="I10", level="intermediate", title="每组 Top-1（相关子查询）",
    topics=["Top-N", "子查询", "GROUP BY"],
    description="找出每个部门薪资最高的员工（每个部门恰好一人，无并列）。<br>输出三列：<code>dept</code>、<code>name</code>、<code>salary</code>。",
    starterSql="SELECT dept, name, salary\nFROM employees e\nWHERE salary = (\n    -- 在这里写「该员工所在部门的最高薪资」子查询\n);",
    starterPandas="# 用 groupby + idxmax 找到每组最大值所在的行索引\nidx = ...  # TODO: 每个部门最高薪资所在的行索引\nresult = employees.loc[idx, ['dept', 'name', 'salary']].reset_index(drop=True)",
    solutionSql="SELECT dept, name, salary\nFROM employees e\nWHERE salary = (SELECT MAX(salary)\n                FROM employees\n                WHERE dept = e.dept);",
    solutionPandas="idx = employees.groupby('dept')['salary'].idxmax()\nresult = (employees.loc[idx, ['dept', 'name', 'salary']]\n          .reset_index(drop=True))",
    explanation="SQL 用相关子查询「本部门最高薪资」来定位每组的 Top-1；pandas 里 <code>groupby('dept')['salary'].idxmax()</code> 直接返回每组最大值所在的行索引，再用 <code>loc</code> 取整行。有并列时两种写法的行为会不同（子查询返回多行，idxmax 只取一行），本题数据无并列。进阶玩法是窗口函数（见 A01/A07）。",
)

ex(
    id="I11", level="intermediate", title="COUNT(DISTINCT) 去重计数",
    topics=["COUNT DISTINCT", "去重计数", "聚合"],
    description="统计有订单的客户一共有多少位（同一客户的多笔订单只算一次）。<br>输出单列 <code>distinct_customers</code>，结果只有一行。",
    starterSql="SELECT\n    -- 用 COUNT(DISTINCT ...) 补全，别名 distinct_customers\nFROM orders;",
    starterPandas="# nunique() 统计去重后的个数\nresult = pd.DataFrame({\n    'distinct_customers': [...],  # TODO: customer_id 的去重计数\n})",
    solutionSql="SELECT COUNT(DISTINCT customer_id) AS distinct_customers\nFROM orders;",
    solutionPandas="result = pd.DataFrame({'distinct_customers': [orders['customer_id'].nunique()]})",
    explanation="<code>COUNT(DISTINCT customer_id)</code> 先对列去重再计数，对应 pandas 的 <code>orders['customer_id'].nunique()</code>（默认忽略 NaN，与 COUNT 忽略 NULL 一致）。",
)

ex(
    id="I12", level="intermediate", title="按月分组汇总",
    topics=["日期", "GROUP BY", "月度汇总"],
    description="统计 2023 年每个月的订单数和销售额（amount 之和，忽略 NULL）。<br>输出三列：<code>month</code>（格式 <code>YYYY-MM</code>）、<code>order_count</code>、<code>total_amount</code>。",
    starterSql="SELECT strftime('%Y-%m', order_date) AS month,\n       -- 补全两个聚合：订单数、销售额\nFROM orders\n-- 补全分组;",
    starterPandas="d = orders.copy()\nd['month'] = ...  # TODO: 用 dt.strftime('%Y-%m') 提取月份\nresult = d.groupby('month', as_index=False).agg(\n    order_count=...,   # TODO: ('order_id', 'count')\n    total_amount=...,  # TODO: ('amount', 'sum')\n)",
    solutionSql="SELECT strftime('%Y-%m', order_date) AS month,\n       COUNT(*) AS order_count,\n       SUM(amount) AS total_amount\nFROM orders\nGROUP BY month;",
    solutionPandas="d = orders.copy()\nd['month'] = d['order_date'].dt.strftime('%Y-%m')\nresult = (d.groupby('month', as_index=False)\n          .agg(order_count=('order_id', 'count'),\n               total_amount=('amount', 'sum')))",
    explanation="按月分组的关键是先把日期截断成「月」：SQL 用 <code>strftime('%Y-%m', order_date)</code>，pandas 用 <code>.dt.strftime('%Y-%m')</code>（也可以用 <code>.dt.to_period('M')</code>）。之后就是普通的 GROUP BY 聚合。",
)

ex(
    id="I13", level="intermediate", title="字符串拼接",
    topics=["字符串", "拼接", "CONCAT"],
    description="为每位客户生成标签，格式为 <code>姓名 (城市)</code>，例如 <code>Zhang Wei (Beijing)</code>。<br>输出单列 <code>label</code>。",
    starterSql="SELECT\n    -- 用 || 拼接 name、' ('、city、')'，别名 label\nFROM customers;",
    starterPandas="# pandas 里字符串列直接用 + 拼接\nresult = pd.DataFrame({\n    'label': ...,  # TODO: name + ' (' + city + ')'\n})",
    solutionSql="SELECT name || ' (' || city || ')' AS label\nFROM customers;",
    solutionPandas="result = pd.DataFrame({\n    'label': customers['name'] + ' (' + customers['city'] + ')',\n})",
    explanation="SQLite 的字符串拼接运算符是 <code>||</code>（其他数据库可能用 <code>CONCAT()</code>）；pandas 中字符串 Series 直接用 <code>+</code> 拼接，也可以用 <code>.str.cat()</code>。",
)

ex(
    id="I14", level="intermediate", title="IN 子查询",
    topics=["IN", "子查询", "集合匹配"],
    description="查询买过 Laptop 的客户的姓名和城市。<br>输出两列：<code>name</code>、<code>city</code>（每位客户只出现一次）。",
    starterSql="SELECT name, city\nFROM customers\nWHERE customer_id IN (\n    -- 在这里写「买过 Laptop 的客户 id」子查询\n);",
    starterPandas="# 先取出买过 Laptop 的客户 id，再用 isin 过滤客户表\nlaptop_buyers = orders.loc[orders['product'] == 'Laptop', 'customer_id']\nmask = ...  # TODO: customer_id 在 laptop_buyers 中的条件\nresult = customers[mask][['name', 'city']].reset_index(drop=True)",
    solutionSql="SELECT name, city\nFROM customers\nWHERE customer_id IN (SELECT customer_id\n                      FROM orders\n                      WHERE product = 'Laptop');",
    solutionPandas="laptop_buyers = orders.loc[orders['product'] == 'Laptop', 'customer_id']\nresult = (customers[customers['customer_id'].isin(laptop_buyers)]\n          [['name', 'city']]\n          .reset_index(drop=True))",
    explanation="<code>WHERE x IN (子查询)</code> 是「半连接」：只过滤、不展开右表，所以不会产生重复行；pandas 对应 <code>isin(另一个表筛出来的一列)</code>。如果改用 JOIN 实现，还需要额外去重。",
)

ex(
    id="I15", level="intermediate", title="分组后排序取第一",
    topics=["GROUP BY", "ORDER BY", "LIMIT"],
    description="统计每种产品的平均订单金额，找出平均金额最高的产品。<br>输出两列：<code>product</code>、<code>avg_amount</code>，结果只有一行。",
    starterSql="SELECT product,\n       AVG(amount) AS avg_amount\nFROM orders\nGROUP BY product\n-- 补全排序与取第一行;",
    starterPandas="# 先分组求平均，再排序取第一行\ng = ...  # TODO: 按 product 分组求 amount 平均值，列名改为 avg_amount\nresult = ...  # TODO: 按 avg_amount 降序排序并取第 1 行\nresult = result.reset_index(drop=True)",
    solutionSql="SELECT product,\n       AVG(amount) AS avg_amount\nFROM orders\nGROUP BY product\nORDER BY avg_amount DESC\nLIMIT 1;",
    solutionPandas="g = (orders.groupby('product', as_index=False)['amount'].mean()\n     .rename(columns={'amount': 'avg_amount'}))\nresult = (g.sort_values('avg_amount', ascending=False)\n          .head(1)\n          .reset_index(drop=True))",
    explanation="「先聚合、再对聚合结果排序取第一」是报表里的常见组合拳：SQL 在 GROUP BY 后直接 <code>ORDER BY ... LIMIT 1</code>（SQLite 允许按别名排序）；pandas 是 <code>groupby().mean()</code> 后接 <code>sort_values().head(1)</code>。",
)

# ============ 精通 Advanced A01-A20 ============

ex(
    id="A01", level="advanced", title="窗口函数 ROW_NUMBER",
    topics=["窗口函数", "ROW_NUMBER", "排名"],
    description="在每个部门内部按薪资从高到低编号。<br>输出四列：<code>dept</code>、<code>name</code>、<code>salary</code>、<code>salary_rank</code>（每个部门从 1 开始；薪资为 NULL 的排在该部门最后）。",
    starterSql="SELECT dept, name, salary,\n       ROW_NUMBER() OVER (\n         -- 补全 PARTITION BY 和 ORDER BY\n       ) AS salary_rank\nFROM employees;",
    starterPandas="# 思路：先排序，再用 groupby().cumcount() 生成组内序号\nd = employees.sort_values(['dept', 'salary'], ascending=[True, False])\nd['salary_rank'] = ...  # TODO: 用 groupby('dept').cumcount() 生成组内序号（从 1 开始）\nresult = d[['dept', 'name', 'salary', 'salary_rank']].reset_index(drop=True)",
    solutionSql="SELECT dept,\n       name,\n       salary,\n       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS salary_rank\nFROM employees;",
    solutionPandas="d = employees.sort_values(['dept', 'salary'], ascending=[True, False])\nd['salary_rank'] = d.groupby('dept').cumcount() + 1\nresult = d[['dept', 'name', 'salary', 'salary_rank']].reset_index(drop=True)",
    explanation="<code>ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)</code> 在 pandas 里可拆成「排序 + <code>groupby().cumcount() + 1</code>」。若允许并列同名次，SQL 用 <code>RANK()</code>，pandas 对应 <code>groupby(...).rank(method='min', ascending=False)</code>。",
)

ex(
    id="A02", level="advanced", title="窗口函数累计求和",
    topics=["窗口函数", "累计和", "SUM OVER"],
    description="忽略金额为 NULL 的订单，按日期统计每日销售额以及截至当日的累计销售额。<br>输出三列：<code>order_date</code>、<code>daily_amount</code>、<code>running_total</code>。",
    starterSql="SELECT order_date,\n       SUM(amount) AS daily_amount,\n       -- 补全：对每日金额做窗口累计求和\nFROM orders\nWHERE amount IS NOT NULL\nGROUP BY order_date;",
    starterPandas="# 思路：dropna -> groupby 求和 -> cumsum\nd = orders.dropna(subset=['amount'])\ndaily = ...  # TODO: 按 order_date 分组求和，列名 daily_amount，并按日期排序\ndaily['running_total'] = ...  # TODO: 对 daily_amount 做累计和（cumsum）\nresult = daily.reset_index(drop=True)",
    solutionSql="SELECT order_date,\n       SUM(amount) AS daily_amount,\n       SUM(SUM(amount)) OVER (ORDER BY order_date) AS running_total\nFROM orders\nWHERE amount IS NOT NULL\nGROUP BY order_date;",
    solutionPandas="d = (orders.dropna(subset=['amount'])\n     .groupby('order_date', as_index=False)['amount'].sum()\n     .rename(columns={'amount': 'daily_amount'})\n     .sort_values('order_date'))\nd['running_total'] = d['daily_amount'].cumsum()\nresult = d.reset_index(drop=True)",
    explanation="SQL 里 <code>SUM(SUM(amount)) OVER (ORDER BY order_date)</code> 是「聚合之上再开窗」；pandas 里对应 <code>groupby().sum()</code> 之后再 <code>.cumsum()</code>。先过滤 NULL 金额是为了避免「SQL 全 NULL 组 SUM 得 NULL 而 pandas 得 0」的边界差异。",
)

ex(
    id="A03", level="advanced", title="自连接查经理",
    topics=["自连接", "JOIN"],
    description="employees 表的 <code>manager_id</code> 指向本表的 <code>id</code>。查询每位员工及其直属经理的姓名（只保留有经理的员工）。<br>输出两列：<code>emp_name</code>、<code>manager_name</code>。",
    starterSql="SELECT e.name AS emp_name,\n       m.name AS manager_name\nFROM employees e\n-- 补全：把 employees 再 JOIN 一次，起别名 m;",
    starterPandas="# 思路：employees 与自身 merge，suffixes 区分两侧同名列\nm = employees.merge(employees[['id', 'name']],\n                    left_on=..., right_on=...,  # TODO: 左表 manager_id 对右表 id\n                    suffixes=('', '_mgr'))\nresult = (m[['name', 'name_mgr']]\n          .rename(columns={'name': 'emp_name', 'name_mgr': 'manager_name'})\n          .reset_index(drop=True))",
    solutionSql="SELECT e.name AS emp_name,\n       m.name AS manager_name\nFROM employees e\nJOIN employees m ON e.manager_id = m.id;",
    solutionPandas="m = employees.merge(employees[['id', 'name']],\n                    left_on='manager_id', right_on='id',\n                    how='inner', suffixes=('', '_mgr'))\nresult = (m[['name', 'name_mgr']]\n          .rename(columns={'name': 'emp_name', 'name_mgr': 'manager_name'})\n          .reset_index(drop=True))",
    explanation="自连接就是「同一张表起两个别名各当一张表用」：SQL 用 <code>employees e JOIN employees m</code>；pandas 用 <code>merge(..., left_on='manager_id', right_on='id')</code>，靠 <code>suffixes</code> 区分两侧的同名列。manager_id 为 NULL 的行在内连接中自然被丢弃。",
)

ex(
    id="A04", level="advanced", title="透视表（条件聚合）",
    topics=["透视表", "CASE WHEN", "pivot_table"],
    description="统计每个城市 VIP（vip=1）与非 VIP（vip=0）客户的数量。<br>输出三列：<code>city</code>、<code>vip_count</code>、<code>non_vip_count</code>。",
    starterSql="SELECT city,\n       -- 用 SUM(CASE WHEN ...) 分别统计两类客户\nFROM customers\nGROUP BY city;",
    starterPandas="# 用 pivot_table 做透视，再重命名列\np = customers.pivot_table(index=..., columns=...,  # TODO: 行是 city，列是 vip\n                          values='name', aggfunc='count', fill_value=0)\np = p.rename(columns={1: 'vip_count', 0: 'non_vip_count'}).reset_index()\nresult = p[['city', 'vip_count', 'non_vip_count']]",
    solutionSql="SELECT city,\n       SUM(CASE WHEN vip = 1 THEN 1 ELSE 0 END) AS vip_count,\n       SUM(CASE WHEN vip = 0 THEN 1 ELSE 0 END) AS non_vip_count\nFROM customers\nGROUP BY city;",
    solutionPandas="p = customers.pivot_table(index='city', columns='vip',\n                          values='name', aggfunc='count', fill_value=0)\np = p.rename(columns={1: 'vip_count', 0: 'non_vip_count'}).reset_index()\nresult = p[['city', 'vip_count', 'non_vip_count']]",
    explanation="SQL 没有 PIVOT 关键字，通用做法是 <code>SUM(CASE WHEN ... THEN 1 ELSE 0 END)</code> 条件聚合，每个输出列一个表达式；pandas 的 <code>pivot_table(index=..., columns=..., aggfunc='count', fill_value=0)</code> 一步生成宽表，再按需重命名列。",
)

ex(
    id="A05", level="advanced", title="melt 宽表转长表",
    topics=["melt", "UNION ALL", "宽转长"],
    description="先统计每个产品（product）的订单数与总销量，得到宽表：<br><pre>product | order_count | total_quantity</pre>再把它转成长表，输出三列：<code>product</code>、<code>metric</code>（取值为 <code>order_count</code> 或 <code>total_quantity</code>）、<code>value</code>，共 8 行。<br>提示：SQL 侧用 UNION ALL 把两次分组结果纵向拼起来；pandas 侧用 melt。",
    starterSql="SELECT product, 'order_count' AS metric, COUNT(*) AS value\nFROM orders\nGROUP BY product\n-- 补全：UNION ALL 第二个 SELECT（total_quantity）;",
    starterPandas="# 宽表已给出，用 melt 转长\nwide = (orders.groupby('product', as_index=False)\n        .agg(order_count=('order_id', 'count'),\n             total_quantity=('quantity', 'sum')))\nresult = wide  # TODO: 用 melt(id_vars=..., var_name='metric', value_name='value') 转成长表",
    solutionSql="SELECT product, 'order_count' AS metric, COUNT(*) AS value\nFROM orders\nGROUP BY product\nUNION ALL\nSELECT product, 'total_quantity', SUM(quantity)\nFROM orders\nGROUP BY product;",
    solutionPandas="wide = (orders.groupby('product', as_index=False)\n        .agg(order_count=('order_id', 'count'),\n             total_quantity=('quantity', 'sum')))\nresult = wide.melt(id_vars='product', var_name='metric', value_name='value')",
    explanation="宽转长：SQL 里用 <code>UNION ALL</code> 把每个指标各查一遍再纵向拼接，metric 列用字符串字面量生成；pandas 的 <code>melt(id_vars='product', var_name='metric', value_name='value')</code> 把 order_count、total_quantity 两列「融化」成行，语义一致。",
)

ex(
    id="A06", level="advanced", title="缺失值填充",
    topics=["COALESCE", "fillna", "NULL"],
    description="查询所有订单，金额（amount）为 NULL 的以 0 显示。<br>输出三列：<code>order_id</code>、<code>product</code>、<code>amount_filled</code>。",
    starterSql="SELECT order_id,\n       product,\n       -- 用 COALESCE 补全\nFROM orders;",
    starterPandas="result = orders[['order_id', 'product']].copy()\nresult['amount_filled'] = ...  # TODO: amount 的缺失值填 0（fillna）",
    solutionSql="SELECT order_id,\n       product,\n       COALESCE(amount, 0) AS amount_filled\nFROM orders;",
    solutionPandas="result = orders[['order_id', 'product']].copy()\nresult['amount_filled'] = orders['amount'].fillna(0)",
    explanation="SQL 的 <code>COALESCE(amount, 0)</code> 返回第一个非 NULL 参数；pandas 的 <code>.fillna(0)</code> 把 NaN 替换为 0。SQL 中还有 <code>IFNULL()</code>（两个参数版本），pandas 中还有 <code>.fillna(method=...)</code> 等填充策略。",
)

ex(
    id="A07", level="advanced", title="去重保留最新",
    topics=["ROW_NUMBER", "去重", "窗口函数"],
    description="找出每个客户最近的一笔订单（按 order_date，无并列）。<br>输出四列：<code>customer_id</code>、<code>order_id</code>、<code>product</code>、<code>order_date</code>。",
    starterSql="SELECT customer_id, order_id, product, order_date\nFROM (\n  SELECT *,\n         ROW_NUMBER() OVER (\n           -- 补全：按客户分区、按日期倒序\n         ) AS rn\n  FROM orders\n)\n-- 补全：只保留每个客户的第一名;",
    starterPandas="# 思路：按日期排序后，drop_duplicates 保留每个客户的最后一行\nd = orders.sort_values('order_date')\nd = ...  # TODO: 按 customer_id 去重，保留日期最新的一行\nresult = d[['customer_id', 'order_id', 'product', 'order_date']].reset_index(drop=True)",
    solutionSql="SELECT customer_id, order_id, product, order_date\nFROM (\n  SELECT *,\n         ROW_NUMBER() OVER (PARTITION BY customer_id\n                            ORDER BY order_date DESC) AS rn\n  FROM orders\n)\nWHERE rn = 1;",
    solutionPandas="d = orders.sort_values('order_date')\nresult = (d.drop_duplicates('customer_id', keep='last')\n          [['customer_id', 'order_id', 'product', 'order_date']]\n          .reset_index(drop=True))",
    explanation="「每组取最新一行」的经典 SQL 写法是 ROW_NUMBER 窗口 + 外层 <code>WHERE rn = 1</code>；pandas 的等价写法是排序后 <code>drop_duplicates('customer_id', keep='last')</code>。也可以用 <code>groupby('customer_id')['order_date'].idxmax()</code>（类似 I10）。",
)

ex(
    id="A08", level="advanced", title="条件分组统计",
    topics=["CASE WHEN", "条件分组", "聚合"],
    description="按订单金额分档统计订单数：<br>· amount &lt; 100 → <code>small</code><br>· 100 &lt;= amount &lt;= 500 → <code>medium</code><br>· amount &gt; 500 → <code>large</code><br>· amount 为 NULL → <code>unknown</code><br>输出两列：<code>amount_range</code>、<code>order_count</code>（共 4 行）。",
    starterSql="SELECT CASE\n         -- 补全分档逻辑\n       END AS amount_range,\n       COUNT(*) AS order_count\nFROM orders\nGROUP BY amount_range;",
    starterPandas="# 用 np.select 生成标签列，再 groupby 计数\nconditions = []  # TODO: isna / <100 / <=500（按此顺序）\nchoices = []     # TODO: 对应的标签\nd = orders.copy()\nd['amount_range'] = np.select(conditions, choices, default='large')\nresult = ...  # TODO: 按 amount_range 分组计数（size），列名改为 order_count",
    solutionSql="SELECT CASE\n         WHEN amount IS NULL THEN 'unknown'\n         WHEN amount < 100 THEN 'small'\n         WHEN amount <= 500 THEN 'medium'\n         ELSE 'large'\n       END AS amount_range,\n       COUNT(*) AS order_count\nFROM orders\nGROUP BY amount_range;",
    solutionPandas="conditions = [\n    orders['amount'].isna(),\n    orders['amount'] < 100,\n    orders['amount'] <= 500,\n]\nchoices = ['unknown', 'small', 'medium']\nd = orders.copy()\nd['amount_range'] = np.select(conditions, choices, default='large')\nresult = (d.groupby('amount_range', as_index=False)\n          .size()\n          .rename(columns={'size': 'order_count'}))",
    explanation="「先打标签再聚合」是条件分组的通用套路：SQL 用 CASE 生成标签列并直接 GROUP BY（SQLite 允许按别名分组）；pandas 用 <code>np.select</code> 生成标签列，再 <code>groupby(...).size()</code> 计数。NULL/NaN 的判断都要放最前面。",
)

ex(
    id="A09", level="advanced", title="连接后聚合",
    topics=["JOIN", "GROUP BY", "聚合"],
    description="统计每个城市的客户消费总额（amount 之和，忽略 NULL；只统计有订单的城市）。<br>输出两列：<code>city</code>、<code>total_spent</code>。",
    starterSql="SELECT c.city,\n       -- 补全聚合表达式\nFROM customers c\n-- 补全 JOIN 与 GROUP BY;",
    starterPandas="# 先 merge 再 groupby 求和\nm = ...  # TODO: orders 连接 customers 的 city 列（键 customer_id，how='inner'）\nresult = ...  # TODO: 按 city 分组对 amount 求和，列名改为 total_spent",
    solutionSql="SELECT c.city,\n       SUM(o.amount) AS total_spent\nFROM customers c\nJOIN orders o ON o.customer_id = c.customer_id\nGROUP BY c.city;",
    solutionPandas="m = orders.merge(customers[['customer_id', 'city']], on='customer_id', how='inner')\nresult = (m.groupby('city', as_index=False)['amount'].sum()\n          .rename(columns={'amount': 'total_spent'}))",
    explanation="「连接 + 分组 + 聚合」是最常见的分析组合：SQL 一条语句完成 <code>JOIN ... GROUP BY ... SUM()</code>；pandas 对应 <code>merge</code> → <code>groupby().sum()</code> → <code>rename</code> 三步。两侧的 SUM/sum 都自动忽略空值。",
)

ex(
    id="A10", level="advanced", title="综合报表：城市消费分层",
    topics=["综合报表", "多层聚合", "CTE"],
    description="生成城市消费报表：<br>第一步：算出每个客户的消费总额（连接 orders 与 customers，忽略 NULL 金额）；<br>第二步：按城市汇总，输出 <code>city</code>、<code>buyer_count</code>（有消费的客户数）、<code>avg_spent</code>（客户平均消费）、<code>max_spent</code>（单客户最高消费）。<br>提示：SQL 可用 CTE（WITH）或子查询实现多层聚合。",
    starterSql="WITH cust AS (\n  -- 第一层：每个客户的消费总额\n)\n-- 第二层：按城市汇总\nSELECT city FROM cust;",
    starterPandas="# 第一层：merge 后按 城市+客户 分组求和\nm = orders.merge(customers[['customer_id', 'city']], on='customer_id')\ncust = ...  # TODO: 按 city + customer_id 求 amount 之和（列名 total）\n# 第二层：按城市再聚合\nresult = ...  # TODO: 聚合出 buyer_count / avg_spent / max_spent",
    solutionSql="WITH cust AS (\n  SELECT c.city,\n         c.customer_id,\n         SUM(o.amount) AS total\n  FROM customers c\n  JOIN orders o ON o.customer_id = c.customer_id\n  GROUP BY c.city, c.customer_id\n)\nSELECT city,\n       COUNT(*) AS buyer_count,\n       AVG(total) AS avg_spent,\n       MAX(total) AS max_spent\nFROM cust\nGROUP BY city;",
    solutionPandas="m = orders.merge(customers[['customer_id', 'city']], on='customer_id', how='inner')\ncust = (m.groupby(['city', 'customer_id'], as_index=False)['amount'].sum()\n        .rename(columns={'amount': 'total'}))\nresult = (cust.groupby('city', as_index=False)\n          .agg(buyer_count=('customer_id', 'count'),\n               avg_spent=('total', 'mean'),\n               max_spent=('total', 'max')))",
    explanation="多层聚合 = 对聚合结果再聚合。SQL 用 CTE 把「每客户总额」固化为中间表，再 <code>GROUP BY city</code> 做第二层；pandas 完全同构：先 <code>groupby(['city','customer_id']).sum()</code>，再 <code>groupby('city').agg(...)</code>。中间结果取个名字（CTE / 变量），是两侧共同的工程实践。",
)

ex(
    id="A11", level="advanced", title="反连接：找出没买过某产品的客户",
    topics=["反连接", "LEFT JOIN", "isin"],
    description="找出<b>从未买过 Laptop</b> 的客户。<br>输出三列：<code>customer_id</code>、<code>name</code>、<code>city</code>。<br>提示：SQL 侧把 product 条件放在 LEFT JOIN 的 ON 里，再用 WHERE 保留没匹配上的行；pandas 侧用 <code>~</code> 对 isin 取反。",
    starterSql="SELECT c.customer_id, c.name, c.city\nFROM customers c\n-- 补全 LEFT JOIN（把 product 条件放在 ON 里）\n-- 再用 WHERE 保留「没匹配上」的客户;",
    starterPandas="# 先取出买过 Laptop 的客户 id，再取反过滤\nlaptop_buyers = orders.loc[orders['product'] == 'Laptop', 'customer_id']\nmask = ...  # TODO: 用 ~ 和 isin 找出没买过 Laptop 的客户\nresult = customers[mask][['customer_id', 'name', 'city']].reset_index(drop=True)",
    solutionSql="SELECT c.customer_id, c.name, c.city\nFROM customers c\nLEFT JOIN orders o\n  ON o.customer_id = c.customer_id\n AND o.product = 'Laptop'\nWHERE o.order_id IS NULL;",
    solutionPandas="laptop_buyers = orders.loc[orders['product'] == 'Laptop', 'customer_id']\nresult = (customers[~customers['customer_id'].isin(laptop_buyers)]\n          [['customer_id', 'name', 'city']]\n          .reset_index(drop=True))",
    explanation="反连接（anti-join）找的是「在右表中没有对应行」的左表行：SQL 的经典写法是 <code>LEFT JOIN ... WHERE 右表键 IS NULL</code>（也可用 NOT EXISTS / NOT IN）；pandas 用 <code>~df['键'].isin(另一列)</code>。注意 NOT IN 遇到子查询含 NULL 会有坑，LEFT JOIN 写法更稳。",
)

ex(
    id="A12", level="advanced", title="每组 Top-2",
    topics=["窗口函数", "Top-N", "groupby"],
    description="找出每个客户最近的两笔订单（按 order_date，无并列）。<br>输出四列：<code>customer_id</code>、<code>order_id</code>、<code>product</code>、<code>order_date</code>。",
    starterSql="SELECT customer_id, order_id, product, order_date\nFROM (\n  SELECT *,\n         ROW_NUMBER() OVER (\n           -- 补全：按客户分区、按日期倒序\n         ) AS rn\n  FROM orders\n)\n-- 补全：每个客户保留前两名;",
    starterPandas="# 思路：按日期倒序排序后，用 groupby().head(2) 取每个客户的前 2 行\nd = orders.sort_values('order_date', ascending=False)\ntop2 = ...  # TODO: 按 customer_id 分组取前 2 行（group_keys=False）\nresult = top2[['customer_id', 'order_id', 'product', 'order_date']].reset_index(drop=True)",
    solutionSql="SELECT customer_id, order_id, product, order_date\nFROM (\n  SELECT *,\n         ROW_NUMBER() OVER (PARTITION BY customer_id\n                            ORDER BY order_date DESC) AS rn\n  FROM orders\n)\nWHERE rn <= 2;",
    solutionPandas="d = orders.sort_values('order_date', ascending=False)\nresult = (d.groupby('customer_id', group_keys=False)\n          .head(2)\n          [['customer_id', 'order_id', 'product', 'order_date']]\n          .reset_index(drop=True))",
    explanation="A07 的「保留第一名」推广到「保留前 N 名」：SQL 只需把 <code>WHERE rn = 1</code> 改成 <code>rn &lt;= 2</code>；pandas 对应 <code>groupby('customer_id', group_keys=False).head(2)</code>——它按组在原顺序中取前 N 行，所以要先排好序。",
)

ex(
    id="A13", level="advanced", title="LAG 环比分析",
    topics=["窗口函数", "LAG", "环比"],
    description="忽略金额为 NULL 的订单，按日期统计每日销售额，并给出前一交易日的销售额。<br>输出三列：<code>order_date</code>、<code>daily_amount</code>、<code>prev_day_amount</code>（首日的前值为 NULL）。",
    starterSql="SELECT order_date,\n       SUM(amount) AS daily_amount,\n       -- 补全：用 LAG 窗口取前一行的合计金额\nFROM orders\nWHERE amount IS NOT NULL\nGROUP BY order_date;",
    starterPandas="# 日销售额已给出，用 shift 取上一行\ndaily = (orders.dropna(subset=['amount'])\n         .groupby('order_date', as_index=False)['amount'].sum()\n         .rename(columns={'amount': 'daily_amount'})\n         .sort_values('order_date'))\ndaily['prev_day_amount'] = ...  # TODO: 取上一行的 daily_amount（shift）\nresult = daily.reset_index(drop=True)",
    solutionSql="SELECT order_date,\n       SUM(amount) AS daily_amount,\n       LAG(SUM(amount)) OVER (ORDER BY order_date) AS prev_day_amount\nFROM orders\nWHERE amount IS NOT NULL\nGROUP BY order_date;",
    solutionPandas="daily = (orders.dropna(subset=['amount'])\n         .groupby('order_date', as_index=False)['amount'].sum()\n         .rename(columns={'amount': 'daily_amount'})\n         .sort_values('order_date'))\ndaily['prev_day_amount'] = daily['daily_amount'].shift(1)\nresult = daily.reset_index(drop=True)",
    explanation="<code>LAG(x) OVER (ORDER BY ...)</code> 取「上一行的 x」，对应 pandas 的 <code>shift(1)</code>；同理 <code>LEAD</code> 对应 <code>shift(-1)</code>。想做环比增长率，再算 <code>(daily_amount - prev_day_amount) / prev_day_amount</code> 即可。",
)

ex(
    id="A14", level="advanced", title="组内占比",
    topics=["窗口函数", "transform", "占比"],
    description="计算每位员工的薪资占本部门薪资总额的比例。<br>输出四列：<code>name</code>、<code>dept</code>、<code>salary</code>、<code>dept_salary_share</code>（薪资为 NULL 的员工占比也是 NULL）。",
    starterSql="SELECT name, dept, salary,\n       -- 补全：salary 除以本部门薪资总额（窗口求和，PARTITION BY dept）\nFROM employees;",
    starterPandas="# transform('sum') 把「组内合计」广播回每一行，对应 SQL 的窗口求和\ndept_total = ...  # TODO: 每位员工所在部门的薪资总额\nresult = employees[['name', 'dept', 'salary']].copy()\nresult['dept_salary_share'] = employees['salary'] / dept_total",
    solutionSql="SELECT name,\n       dept,\n       salary,\n       salary / SUM(salary) OVER (PARTITION BY dept) AS dept_salary_share\nFROM employees;",
    solutionPandas="dept_total = employees.groupby('dept')['salary'].transform('sum')\nresult = employees[['name', 'dept', 'salary']].copy()\nresult['dept_salary_share'] = employees['salary'] / dept_total",
    explanation="「聚合结果对齐回每一行」是窗口函数的典型用途：SQL 用 <code>SUM(salary) OVER (PARTITION BY dept)</code>，pandas 用 <code>groupby('dept')['salary'].transform('sum')</code>——transform 返回与原表等长的 Series，可以直接做列运算。",
)

ex(
    id="A15", level="advanced", title="高于组内平均的行",
    topics=["相关子查询", "transform", "GROUP BY"],
    description="查询薪资高于<b>本部门</b>平均薪资的员工。<br>输出三列：<code>name</code>、<code>dept</code>、<code>salary</code>。",
    starterSql="SELECT name, dept, salary\nFROM employees e\nWHERE salary > (\n    -- 补全：本部门平均薪资的相关子查询\n);",
    starterPandas="# 先用 transform 把组内平均值对齐到每一行，再逐行比较\ndept_avg = ...  # TODO: 每位员工所在部门的平均薪资\nresult = employees[employees['salary'] > dept_avg][['name', 'dept', 'salary']].reset_index(drop=True)",
    solutionSql="SELECT name, dept, salary\nFROM employees e\nWHERE salary > (SELECT AVG(salary)\n                FROM employees\n                WHERE dept = e.dept);",
    solutionPandas="dept_avg = employees.groupby('dept')['salary'].transform('mean')\nresult = (employees[employees['salary'] > dept_avg]\n          [['name', 'dept', 'salary']]\n          .reset_index(drop=True))",
    explanation="I06 是「高于全公司平均」（子查询得出一个标量），本题是「高于本组平均」：SQL 用相关子查询逐组计算；pandas 用 <code>transform('mean')</code> 把每组平均值对齐到每行后再比较。薪资为 NULL 的员工在两侧都会被条件排除。",
)

ex(
    id="A16", level="advanced", title="滑动平均",
    topics=["窗口函数", "滑动平均", "rolling"],
    description="忽略金额为 NULL 的订单，按日期统计每日销售额，并计算 3 日滑动平均（当前行与前两行的平均值，不足 3 行时有多少算多少）。<br>输出三列：<code>order_date</code>、<code>daily_amount</code>、<code>ma_3d</code>。",
    starterSql="SELECT order_date,\n       SUM(amount) AS daily_amount,\n       -- 补全：窗口加 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW 做 3 日滑动平均\nFROM orders\nWHERE amount IS NOT NULL\nGROUP BY order_date;",
    starterPandas="# 日销售额已给出，用 rolling 做滑动平均\ndaily = (orders.dropna(subset=['amount'])\n         .groupby('order_date', as_index=False)['amount'].sum()\n         .rename(columns={'amount': 'daily_amount'})\n         .sort_values('order_date'))\ndaily['ma_3d'] = ...  # TODO: 3 日滑动平均（rolling，窗口不足 3 时也算）\nresult = daily.reset_index(drop=True)",
    solutionSql="SELECT order_date,\n       SUM(amount) AS daily_amount,\n       AVG(SUM(amount)) OVER (ORDER BY order_date\n                              ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS ma_3d\nFROM orders\nWHERE amount IS NOT NULL\nGROUP BY order_date;",
    solutionPandas="daily = (orders.dropna(subset=['amount'])\n         .groupby('order_date', as_index=False)['amount'].sum()\n         .rename(columns={'amount': 'daily_amount'})\n         .sort_values('order_date'))\ndaily['ma_3d'] = daily['daily_amount'].rolling(3, min_periods=1).mean()\nresult = daily.reset_index(drop=True)",
    explanation="滑动窗口用「窗口帧」指定范围：SQL 的 <code>ROWS BETWEEN 2 PRECEDING AND CURRENT ROW</code> 表示当前行加前两行，窗口不足时自动取已有行；pandas 的 <code>rolling(3, min_periods=1).mean()</code> 中 <code>min_periods=1</code> 起到同样的作用。",
)

ex(
    id="A17", level="advanced", title="累计客户数报表",
    topics=["CTE", "窗口函数", "累计"],
    description="按注册月份统计每月新增客户数，以及截至当月的累计客户总数。<br>输出三列：<code>month</code>（格式 <code>YYYY-MM</code>）、<code>new_customers</code>、<code>total_customers</code>。",
    starterSql="WITH m AS (\n  SELECT strftime('%Y-%m', signup_date) AS month,\n         COUNT(*) AS new_customers\n  FROM customers\n  GROUP BY month\n)\n-- 补全：输出 month、new_customers，并用窗口累计出 total_customers\nSELECT month FROM m;",
    starterPandas="# 第一层：按月计数；第二层：累计求和\nm = customers.copy()\nm['month'] = ...  # TODO: 用 dt.strftime('%Y-%m') 提取注册月份\nmonthly = ...  # TODO: 按 month 分组计数，列名 new_customers\nmonthly['total_customers'] = ...  # TODO: 对 new_customers 做累计和\nresult = monthly.reset_index(drop=True)",
    solutionSql="WITH m AS (\n  SELECT strftime('%Y-%m', signup_date) AS month,\n         COUNT(*) AS new_customers\n  FROM customers\n  GROUP BY month\n)\nSELECT month,\n       new_customers,\n       SUM(new_customers) OVER (ORDER BY month) AS total_customers\nFROM m;",
    solutionPandas="m = customers.copy()\nm['month'] = m['signup_date'].dt.strftime('%Y-%m')\nmonthly = (m.groupby('month', as_index=False)\n           .size()\n           .rename(columns={'size': 'new_customers'}))\nmonthly['total_customers'] = monthly['new_customers'].cumsum()\nresult = monthly.reset_index(drop=True)",
    explanation="这是「聚合 + 窗口累计」的又一种组合：SQL 先用 CTE 按月计数，再 <code>SUM(new_customers) OVER (ORDER BY month)</code>；pandas 用 <code>groupby().size()</code> 后接 <code>cumsum()</code>。结构上与 A02 完全一致，只是数据换成了注册日期。",
)

ex(
    id="A18", level="advanced", title="并列排名 RANK",
    topics=["RANK", "排名", "窗口函数"],
    description="按消费总额给客户排名（总额从高到低；若总额相同则名次相同，后续名次跳号）。<br>输出三列：<code>customer_id</code>、<code>total_spent</code>、<code>spent_rank</code>。",
    starterSql="WITH t AS (\n  -- 第一层：每个客户的消费总额 total_spent\n)\n-- 第二层：对 total_spent 降序排名（并列同名次用 RANK）\nSELECT customer_id FROM t;",
    starterPandas="# 先求每个客户的消费总额，再排名\nt = ...  # TODO: 按 customer_id 分组求 amount 之和，列名 total_spent\nt['spent_rank'] = ...  # TODO: 对 total_spent 降序排名，并列同名次（rank，method='min'）\nresult = t.reset_index(drop=True)",
    solutionSql="WITH t AS (\n  SELECT customer_id, SUM(amount) AS total_spent\n  FROM orders\n  GROUP BY customer_id\n)\nSELECT customer_id,\n       total_spent,\n       RANK() OVER (ORDER BY total_spent DESC) AS spent_rank\nFROM t;",
    solutionPandas="t = (orders.groupby('customer_id', as_index=False)['amount'].sum()\n     .rename(columns={'amount': 'total_spent'}))\nt['spent_rank'] = t['total_spent'].rank(method='min', ascending=False)\nresult = t.reset_index(drop=True)",
    explanation="排名函数三种：ROW_NUMBER 不管并列、RANK 并列后跳号、DENSE_RANK 并列后不跳号；pandas 对应 <code>rank(method='first'/'min'/'dense', ascending=False)</code>。本题要求并列同名次且跳号，所以是 RANK 与 <code>method='min'</code>。",
)

ex(
    id="A19", level="advanced", title="每个城市的最大消费客户",
    topics=["窗口函数", "JOIN", "综合"],
    description="找出每个城市消费总额最高的客户（无并列）。<br>输出三列：<code>city</code>、<code>name</code>、<code>total_spent</code>。",
    starterSql="WITH t AS (\n  -- 第一层：连接 customers 与 orders，按 城市+客户 求消费总额\n)\n-- 第二层：每个城市取总额最高的客户（可用 ROW_NUMBER 窗口）\nSELECT city FROM t;",
    starterPandas="# 先连接并聚合出 城市+客户 的消费总额，再取每个城市的最大值所在行\nm = orders.merge(customers[['customer_id', 'city', 'name']], on='customer_id')\nt = ...  # TODO: 按 city + name 分组求 amount 之和，列名 total_spent\nidx = ...  # TODO: 每个城市 total_spent 最大值所在的行索引（idxmax）\nresult = t.loc[idx, ['city', 'name', 'total_spent']].reset_index(drop=True)",
    solutionSql="WITH t AS (\n  SELECT c.city,\n         c.name,\n         SUM(o.amount) AS total_spent\n  FROM customers c\n  JOIN orders o ON o.customer_id = c.customer_id\n  GROUP BY c.city, c.name\n),\nranked AS (\n  SELECT *,\n         ROW_NUMBER() OVER (PARTITION BY city ORDER BY total_spent DESC) AS rn\n  FROM t\n)\nSELECT city, name, total_spent\nFROM ranked\nWHERE rn = 1;",
    solutionPandas="m = orders.merge(customers[['customer_id', 'city', 'name']], on='customer_id', how='inner')\nt = (m.groupby(['city', 'name'], as_index=False)['amount'].sum()\n     .rename(columns={'amount': 'total_spent'}))\nidx = t.groupby('city')['total_spent'].idxmax()\nresult = t.loc[idx, ['city', 'name', 'total_spent']].reset_index(drop=True)",
    explanation="I10 是「单表每组 Top-1」，本题升级为「连接 + 聚合之后再每组 Top-1」：SQL 需要两层 CTE（先聚合、再窗口编号筛选）；pandas 同样可以分两步，groupby 后 <code>idxmax + loc</code> 取行，思路完全同构。",
)

ex(
    id="A20", level="advanced", title="综合报表：复购客户分析",
    topics=["CTE", "多层聚合", "COUNT DISTINCT"],
    description="按城市统计客户结构与复购情况：<br>输出三列：<code>city</code>、<code>customer_count</code>（有订单的客户数）、<code>multi_product_count</code>（买过 2 种及以上不同产品的客户数）。<br>提示：先按「城市+客户」统计不同产品数（COUNT DISTINCT / nunique），再按城市做第二层聚合。",
    starterSql="WITH pc AS (\n  -- 第一层：连接后按 城市+客户 统计不同产品数 product_kinds\n)\n-- 第二层：按城市汇总客户数与「产品数 >= 2」的客户数\nSELECT city FROM pc;",
    starterPandas="# 第一层：连接后按 城市+客户 统计不同产品数\nm = orders.merge(customers[['customer_id', 'city']], on='customer_id')\npc = ...  # TODO: 按 city + customer_id 分组，统计 product 的 nunique（列名 product_kinds）\npc['is_multi'] = ...  # TODO: product_kinds >= 2 记为 1，否则 0\nresult = pc.groupby('city', as_index=False).agg(\n    customer_count=('customer_id', 'count'),\n    multi_product_count=('is_multi', 'sum'),\n)",
    solutionSql="WITH pc AS (\n  SELECT c.city,\n         o.customer_id,\n         COUNT(DISTINCT o.product) AS product_kinds\n  FROM customers c\n  JOIN orders o ON o.customer_id = c.customer_id\n  GROUP BY c.city, o.customer_id\n)\nSELECT city,\n       COUNT(*) AS customer_count,\n       SUM(CASE WHEN product_kinds >= 2 THEN 1 ELSE 0 END) AS multi_product_count\nFROM pc\nGROUP BY city;",
    solutionPandas="m = orders.merge(customers[['customer_id', 'city']], on='customer_id', how='inner')\npc = (m.groupby(['city', 'customer_id'], as_index=False)['product'].nunique()\n      .rename(columns={'product': 'product_kinds'}))\npc['is_multi'] = (pc['product_kinds'] >= 2).astype(int)\nresult = (pc.groupby('city', as_index=False)\n          .agg(customer_count=('customer_id', 'count'),\n               multi_product_count=('is_multi', 'sum')))",
    explanation="两层聚合各用一个技巧：第一层 <code>COUNT(DISTINCT product)</code> 对应 <code>nunique</code>，得到「每客户买过几种产品」；第二层把「&gt;= 2」这个布尔条件转成计数——SQL 用 <code>SUM(CASE WHEN ... THEN 1 ELSE 0 END)</code>，pandas 用 <code>.astype(int)</code> 后 <code>sum</code>。这是 A04 条件聚合与 A10 多层聚合的组合运用。",
)

# ============ pandas 函数用法提示 ============
# 在该题首次出现的 pandas 函数，给出简短用法说明（HTML），前端以可折叠块展示。
PANDAS_TIPS = {
    "B15": "<code>.iloc[3:6]</code>：按行<b>位置</b>切片（从 0 开始、左闭右开），即第 4~6 行，对应 <code>LIMIT 3 OFFSET 3</code>。",
    "I11": "<code>s.nunique()</code>：统计一列去重后的取值个数（默认忽略 NaN），对应 <code>COUNT(DISTINCT 列)</code>。",
    "I12": "<code>s.dt.strftime('%Y-%m')</code>：把 datetime 列格式化为 <code>YYYY-MM</code> 字符串，对应 SQL 的 <code>strftime('%Y-%m', 列)</code>。<br><code>.dt</code> 是日期时间访问器，地位类似字符串的 <code>.str</code>。",
    "I13": "字符串 Series 可以直接用 <code>+</code> 逐行拼接，如 <code>df['a'] + '-' + df['b']</code>；也可用 <code>df['a'].str.cat(df['b'], sep='-')</code>。",
    "A11": "<code>~</code>：对布尔 Series 逐元素取反，<code>~s.isin(v)</code> 即「不在集合 v 中」。注意取反用 <code>~</code> 而不是 <code>not</code>。",
    "A12": "<code>df.groupby('列', group_keys=False).head(n)</code>：保留每个分组的前 n 行（按 DataFrame 当前顺序），配合先排序即可实现「每组 Top-N」。",
    "A13": "<code>s.shift(1)</code>：整列向下平移 1 行、首行补 NaN，对应 <code>LAG</code>；<code>s.shift(-1)</code> 向上平移，对应 <code>LEAD</code>。",
    "A14": "<code>df.groupby('列')['x'].transform('sum')</code>：先按组聚合，再把结果<b>广播回每一行</b>（返回值与原表等长），对应窗口函数 <code>SUM(x) OVER (PARTITION BY 列)</code>。",
    "A15": "<code>df.groupby('列')['x'].transform('mean')</code>：把「每组的平均值」对齐到每一行，之后可直接与原列逐行比较，对应窗口函数 / 相关子查询。",
    "A16": "<code>s.rolling(窗口, min_periods=1).mean()</code>：滑动窗口平均，<code>rolling(3)</code> 表示当前行加前 2 行；<code>min_periods=1</code> 让窗口不足 3 行时也照常计算，对应 <code>ROWS BETWEEN 2 PRECEDING AND CURRENT ROW</code>。",
    "A18": "<code>s.rank(method='min', ascending=False)</code>：降序排名，并列取共同的最小名次（之后跳号），对应 <code>RANK()</code>；<code>method='dense'</code> 对应 <code>DENSE_RANK</code>，<code>method='first'</code> 对应 <code>ROW_NUMBER</code>。",
    "A20": "<code>df.groupby('列')['x'].nunique()</code>：每组内的去重计数，对应 <code>COUNT(DISTINCT x)</code>。<br><code>(s &gt;= 2).astype(int)</code>：把布尔列转成 0/1，之后 <code>sum</code> 即「满足条件的行数」，对应 <code>SUM(CASE WHEN ... THEN 1 ELSE 0 END)</code>。",
}
for _e in E:
    if _e["id"] in PANDAS_TIPS:
        _e["pandasTips"] = PANDAS_TIPS[_e["id"]]

# ============ 输出 ============

assert len(E) == 50, f"expected 50 exercises, got {len(E)}"

data_dir = ROOT / "data"
data_dir.mkdir(exist_ok=True)

json_text = json.dumps(E, ensure_ascii=False, indent=2) + "\n"
(data_dir / "exercises.json").write_text(json_text, encoding="utf-8")

# js/app.js 从 ../data/exercises.js import { EXERCISES }
js_text = "// 由 tools/build_exercises.py 生成，内容与 data/exercises.json 一致\nexport const EXERCISES = " + json_text.rstrip() + ";\n"
(data_dir / "exercises.js").write_text(js_text, encoding="utf-8")

print(f"written: {data_dir / 'exercises.json'}")
print(f"written: {data_dir / 'exercises.js'}")
print(f"exercises: {len(E)}")
