# 生成 data/exercises.json（30 道题）与 data/exercises.js（供 js/app.js import）
# 用法（cwd 为项目根）：.venv/Scripts/python.exe tools/build_exercises.py
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

E = []  # exercises


def ex(**kw):
    E.append(kw)


# ============ 入门 Beginner B01-B10 ============

ex(
    id="B01", level="beginner", title="选择指定列",
    topics=["SELECT", "列选择"],
    description="从 <code>employees</code> 表中查询所有员工的姓名和部门。<br>输出两列，列名依次为 <code>name</code>、<code>dept</code>。",
    starterSql="SELECT\n    -- 在这里填写要查询的列名\nFROM employees;",
    starterPandas="# 用双方括号选择需要的列\nresult = employees[['name']]  # 补全：还需要 dept 列\n# 将最终结果赋值给 result",
    solutionSql="SELECT name, dept\nFROM employees;",
    solutionPandas="result = employees[['name', 'dept']].reset_index(drop=True)",
    explanation="SQL 用 <code>SELECT name, dept</code> 指定要输出的列；pandas 用双方括号 <code>employees[['name', 'dept']]</code> 选列，得到的就是一个只含这两列的 DataFrame。",
)

ex(
    id="B02", level="beginner", title="WHERE 过滤行",
    topics=["WHERE", "过滤"],
    description="查询 Engineering 部门的所有员工，输出<b>全部列</b>（列顺序与表结构一致）。",
    starterSql="SELECT *\nFROM employees\n-- 在这里补全 WHERE 条件;",
    starterPandas="# 用布尔条件过滤行\nresult = employees[employees['dept'] == 'TODO']\n# 将最终结果赋值给 result",
    solutionSql="SELECT *\nFROM employees\nWHERE dept = 'Engineering';",
    solutionPandas="result = employees[employees['dept'] == 'Engineering'].reset_index(drop=True)",
    explanation="SQL 的 <code>WHERE dept = 'Engineering'</code> 对应 pandas 的布尔索引 <code>employees[employees['dept'] == 'Engineering']</code>。注意 pandas 中判断相等要用 <code>==</code>。",
)

ex(
    id="B03", level="beginner", title="ORDER BY 与 LIMIT",
    topics=["ORDER BY", "LIMIT", "排序"],
    description="查询薪资最高的 3 名员工。<br>输出两列：<code>name</code>、<code>salary</code>，按薪资从高到低排列。",
    starterSql="SELECT name, salary\nFROM employees\n-- 在这里补全排序和行数限制;",
    starterPandas="# 用 sort_values 排序，再用 head 取前 N 行\nresult = employees  # 补全排序、取前 3 行、选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT 3;",
    solutionPandas="result = (employees.sort_values('salary', ascending=False)\n          .head(3)\n          [['name', 'salary']]\n          .reset_index(drop=True))",
    explanation="<code>ORDER BY salary DESC LIMIT 3</code> 对应 pandas 的 <code>sort_values('salary', ascending=False).head(3)</code>。pandas 排序时 NaN 默认排在最后，与 SQLite 中 NULL 在 DESC 时排最后一致。",
)

ex(
    id="B04", level="beginner", title="DISTINCT 去重",
    topics=["DISTINCT", "去重"],
    description="查询公司一共有哪些部门（去重）。<br>输出单列 <code>dept</code>。",
    starterSql="SELECT -- 在这里补全去重关键字\n    dept\nFROM employees;",
    starterPandas="# 用 drop_duplicates 去重\nresult = employees[['dept']]  # 补全去重逻辑\n# 将最终结果赋值给 result",
    solutionSql="SELECT DISTINCT dept\nFROM employees;",
    solutionPandas="result = employees[['dept']].drop_duplicates().reset_index(drop=True)",
    explanation="<code>SELECT DISTINCT dept</code> 对应 pandas 的 <code>employees[['dept']].drop_duplicates()</code>。判题忽略行序，所以不需要额外排序。",
)

ex(
    id="B05", level="beginner", title="AND 与 OR 组合条件",
    topics=["WHERE", "AND/OR", "逻辑运算"],
    description="查询 Sales 部门中薪资低于 65000 <b>或</b>高于 70000 的员工。<br>输出三列：<code>name</code>、<code>dept</code>、<code>salary</code>。<br>注意 AND 优先级高于 OR，请用括号明确分组。",
    starterSql="SELECT name, dept, salary\nFROM employees\nWHERE dept = 'Sales'\n  -- 在这里补全 AND/OR 组合条件（记得加括号）;",
    starterPandas="# pandas 中 & 表示 AND，| 表示 OR，每个条件都要加括号\nresult = employees[(employees['dept'] == 'Sales')]\n# 补全薪资条件，并选出 name/dept/salary 三列\n# 将最终结果赋值给 result",
    solutionSql="SELECT name, dept, salary\nFROM employees\nWHERE dept = 'Sales'\n  AND (salary < 65000 OR salary > 70000);",
    solutionPandas="result = (employees[(employees['dept'] == 'Sales')\n          & ((employees['salary'] < 65000) | (employees['salary'] > 70000))]\n          [['name', 'dept', 'salary']]\n          .reset_index(drop=True))",
    explanation="SQL 用 <code>AND</code>/<code>OR</code>，pandas 用 <code>&amp;</code>/<code>|</code>，且 pandas 中每个比较条件都必须用括号包起来，否则运算符优先级会出错。",
)

ex(
    id="B06", level="beginner", title="IN 集合匹配",
    topics=["IN", "集合匹配"],
    description="查询位于 Beijing 或 Shanghai 的客户。<br>输出两列：<code>name</code>、<code>city</code>。",
    starterSql="SELECT name, city\nFROM customers\n-- 用 IN 补全条件;",
    starterPandas="# 用 isin 判断是否在集合中\nresult = customers[customers['city'].isin([])]  # 在列表中填入城市名\n# 补全选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT name, city\nFROM customers\nWHERE city IN ('Beijing', 'Shanghai');",
    solutionPandas="result = (customers[customers['city'].isin(['Beijing', 'Shanghai'])]\n          [['name', 'city']]\n          .reset_index(drop=True))",
    explanation="<code>WHERE city IN ('Beijing', 'Shanghai')</code> 对应 pandas 的 <code>customers['city'].isin(['Beijing', 'Shanghai'])</code>，比写多个 OR 更简洁。",
)

ex(
    id="B07", level="beginner", title="BETWEEN 范围过滤",
    topics=["BETWEEN", "范围过滤"],
    description="查询金额（amount）在 100 到 500 之间（含边界）的订单。<br>输出三列：<code>order_id</code>、<code>product</code>、<code>amount</code>。<br>注意：金额为 NULL 的订单会被条件自动排除。",
    starterSql="SELECT order_id, product, amount\nFROM orders\n-- 用 BETWEEN 补全条件;",
    starterPandas="# 用 between 判断范围（含边界）\nresult = orders[orders['amount'].between(100, 500)]\n# 补全选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT order_id, product, amount\nFROM orders\nWHERE amount BETWEEN 100 AND 500;",
    solutionPandas="result = (orders[orders['amount'].between(100, 500)]\n          [['order_id', 'product', 'amount']]\n          .reset_index(drop=True))",
    explanation="<code>amount BETWEEN 100 AND 500</code> 等价于 <code>amount &gt;= 100 AND amount &lt;= 500</code>，对应 pandas 的 <code>orders['amount'].between(100, 500)</code>。两侧对 NULL/NaN 的比较结果都是「不满足条件」，行为一致。",
)

ex(
    id="B08", level="beginner", title="LIKE 模糊匹配",
    topics=["LIKE", "模式匹配"],
    description="查询姓名以字母 Z 开头的客户。<br>输出两列：<code>name</code>、<code>city</code>。<br>提示：SQL 中 <code>%</code> 匹配任意多个字符。",
    starterSql="SELECT name, city\nFROM customers\n-- 用 LIKE 补全条件;",
    starterPandas="# 用 str.startswith 判断前缀\nresult = customers[customers['name'].str.startswith('')]\n# 补全参数与选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT name, city\nFROM customers\nWHERE name LIKE 'Z%';",
    solutionPandas="result = (customers[customers['name'].str.startswith('Z')]\n          [['name', 'city']]\n          .reset_index(drop=True))",
    explanation="<code>name LIKE 'Z%'</code> 对应 pandas 的 <code>customers['name'].str.startswith('Z')</code>。更复杂的模式（如含中间字符）可以用 <code>str.contains</code>。",
)

ex(
    id="B09", level="beginner", title="NULL 值判断",
    topics=["NULL", "IS NULL"],
    description="查询还没有分配经理的员工（manager_id 为 NULL）。<br>输出两列：<code>name</code>、<code>dept</code>。<br>注意：判断 NULL 不能用 <code>= NULL</code>。",
    starterSql="SELECT name, dept\nFROM employees\n-- 用 IS NULL 补全条件;",
    starterPandas="# 用 isna() 判断缺失值\nresult = employees[employees['manager_id'].isna()]\n# 补全选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT name, dept\nFROM employees\nWHERE manager_id IS NULL;",
    solutionPandas="result = (employees[employees['manager_id'].isna()]\n          [['name', 'dept']]\n          .reset_index(drop=True))",
    explanation="SQL 用 <code>IS NULL</code> / <code>IS NOT NULL</code> 判断空值（<code>= NULL</code> 永远不为真）；pandas 对应 <code>.isna()</code> / <code>.notna()</code>。",
)

ex(
    id="B10", level="beginner", title="简单聚合 COUNT / SUM",
    topics=["聚合", "COUNT", "SUM"],
    description="统计订单表的总订单数和所有订单的总金额（amount 求和时自动忽略 NULL）。<br>输出两列：<code>order_count</code>、<code>total_amount</code>，结果只有一行。",
    starterSql="SELECT\n    -- 在这里写聚合表达式，并用 AS 起别名\nFROM orders;",
    starterPandas="# len() 统计行数，sum() 求和（自动跳过 NaN）\nresult = pd.DataFrame({\n    'order_count': [0],   # 补全\n    'total_amount': [0],  # 补全\n})\n# 将最终结果赋值给 result",
    solutionSql="SELECT COUNT(*) AS order_count,\n       SUM(amount) AS total_amount\nFROM orders;",
    solutionPandas="result = pd.DataFrame({\n    'order_count': [len(orders)],\n    'total_amount': [orders['amount'].sum()],\n})",
    explanation="SQL 的 <code>COUNT(*)</code> 统计行数、<code>SUM(amount)</code> 忽略 NULL；pandas 对应 <code>len(orders)</code> 和 <code>orders['amount'].sum()</code>（默认 skipna=True）。单行结果可以用 <code>pd.DataFrame({...})</code> 直接构造。",
)

# ============ 进阶 Intermediate I01-I10 ============

ex(
    id="I01", level="intermediate", title="GROUP BY 分组聚合",
    topics=["GROUP BY", "聚合", "AVG"],
    description="统计每个部门的员工人数和平均薪资。<br>输出三列：<code>dept</code>、<code>emp_count</code>、<code>avg_salary</code>。<br>（AVG 会自动忽略 salary 为 NULL 的员工。）",
    starterSql="SELECT dept,\n       -- 在这里补全聚合表达式与别名\nFROM employees\n-- 补全分组;",
    starterPandas="# groupby 后用 agg 做命名聚合，列名与 SQL 别名对齐\nresult = employees.groupby('dept', as_index=False).agg(\n    emp_count=('id', 'count'),\n    # 补全 avg_salary\n)\n# 将最终结果赋值给 result",
    solutionSql="SELECT dept,\n       COUNT(*) AS emp_count,\n       AVG(salary) AS avg_salary\nFROM employees\nGROUP BY dept;",
    solutionPandas="result = (employees.groupby('dept', as_index=False)\n          .agg(emp_count=('id', 'count'),\n               avg_salary=('salary', 'mean')))",
    explanation="<code>GROUP BY dept</code> 对应 <code>groupby('dept')</code>；SQL 的 <code>AVG(salary)</code> 忽略 NULL，pandas 的 <code>mean</code> 默认跳过 NaN，结果一致。用命名聚合 <code>agg(别名=('列', '函数'))</code> 可以直接得到与 SQL 别名一致的列名。",
)

ex(
    id="I02", level="intermediate", title="HAVING 过滤分组",
    topics=["HAVING", "GROUP BY"],
    description="找出累计消费金额（amount 之和）超过 1500 的客户。<br>输出两列：<code>customer_id</code>、<code>total_amount</code>。",
    starterSql="SELECT customer_id,\n       SUM(amount) AS total_amount\nFROM orders\nGROUP BY customer_id\n-- 补全对分组结果的过滤条件;",
    starterPandas="# 先 groupby 求和，再用布尔条件过滤\ng = orders.groupby('customer_id', as_index=False)['amount'].sum()\ng.columns = ['customer_id', 'total_amount']\nresult = g  # 补全过滤\n# 将最终结果赋值给 result",
    solutionSql="SELECT customer_id,\n       SUM(amount) AS total_amount\nFROM orders\nGROUP BY customer_id\nHAVING SUM(amount) > 1500;",
    solutionPandas="g = (orders.groupby('customer_id', as_index=False)['amount'].sum()\n     .rename(columns={'amount': 'total_amount'}))\nresult = g[g['total_amount'] > 1500].reset_index(drop=True)",
    explanation="WHERE 过滤的是行，HAVING 过滤的是分组后的结果。pandas 没有 HAVING 的概念，做法就是「先聚合、再按聚合结果过滤」两步走。",
)

ex(
    id="I03", level="intermediate", title="多列排序",
    topics=["ORDER BY", "多列排序"],
    description="查询所有员工的 <code>name</code>、<code>dept</code>、<code>salary</code> 三列。<br>排序要求：先按部门升序，部门内部再按薪资降序。",
    starterSql="SELECT name, dept, salary\nFROM employees\n-- 补全多列排序;",
    starterPandas="# sort_values 可以传列名列表和升降序列表\nresult = employees.sort_values(['dept'], ascending=[True])\n# 补全第二个排序键与选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT name, dept, salary\nFROM employees\nORDER BY dept ASC, salary DESC;",
    solutionPandas="result = (employees.sort_values(['dept', 'salary'], ascending=[True, False])\n          [['name', 'dept', 'salary']]\n          .reset_index(drop=True))",
    explanation="<code>ORDER BY dept ASC, salary DESC</code> 对应 <code>sort_values(['dept', 'salary'], ascending=[True, False])</code>，两个列表按位置一一对应。",
)

ex(
    id="I04", level="intermediate", title="INNER JOIN 内连接",
    topics=["JOIN", "INNER JOIN"],
    description="查询每笔订单对应的客户姓名。<br>输出四列：<code>order_id</code>、<code>customer_name</code>、<code>product</code>、<code>amount</code>。",
    starterSql="SELECT o.order_id,\n       c.name AS customer_name,\n       o.product,\n       o.amount\nFROM orders o\n-- 补全 JOIN 子句;",
    starterPandas="# 用 merge 连接两张表，再把 name 重命名为 customer_name\nm = orders.merge(customers[['customer_id', 'name']], on='customer_id')\nresult = m  # 补全重命名与选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT o.order_id,\n       c.name AS customer_name,\n       o.product,\n       o.amount\nFROM orders o\nINNER JOIN customers c ON o.customer_id = c.customer_id;",
    solutionPandas="m = orders.merge(customers[['customer_id', 'name']], on='customer_id', how='inner')\nm = m.rename(columns={'name': 'customer_name'})\nresult = m[['order_id', 'customer_name', 'product', 'amount']].reset_index(drop=True)",
    explanation="<code>INNER JOIN ... ON</code> 对应 <code>merge(..., on='customer_id', how='inner')</code>。SQL 里用 <code>AS</code> 给列起别名，pandas 里用 <code>rename(columns={...})</code>。",
)

ex(
    id="I05", level="intermediate", title="LEFT JOIN 保留未匹配行",
    topics=["LEFT JOIN", "聚合"],
    description="统计每位客户购买 Laptop 的订单数，<b>包括一次都没买过的客户（显示 0）</b>。<br>输出两列：<code>name</code>、<code>laptop_orders</code>（共 10 行）。<br>提示：把 <code>product = 'Laptop'</code> 放在 JOIN 条件里而不是 WHERE 里，才能保留没买过 Laptop 的客户——这正是 LEFT JOIN 与 INNER JOIN 的差别。",
    starterSql="SELECT c.name,\n       COUNT(o.order_id) AS laptop_orders\nFROM customers c\n-- 补全 LEFT JOIN（注意 product 条件的位置）\nGROUP BY c.customer_id, c.name;",
    starterPandas="# 思路：先统计每个客户的 Laptop 订单数，再 LEFT 连接回客户表并填 0\nlaptop = orders[orders['product'] == 'Laptop'].groupby('customer_id').size()\nresult = customers  # 补全连接、fillna、选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT c.name,\n       COUNT(o.order_id) AS laptop_orders\nFROM customers c\nLEFT JOIN orders o\n  ON o.customer_id = c.customer_id\n AND o.product = 'Laptop'\nGROUP BY c.customer_id, c.name;",
    solutionPandas="laptop = (orders[orders['product'] == 'Laptop']\n          .groupby('customer_id')\n          .size()\n          .rename('laptop_orders'))\nresult = (customers[['customer_id', 'name']]\n          .merge(laptop, on='customer_id', how='left'))\nresult['laptop_orders'] = result['laptop_orders'].fillna(0).astype(int)\nresult = result[['name', 'laptop_orders']]",
    explanation="SQL 中把 <code>o.product = 'Laptop'</code> 写在 ON 里，左表客户全部保留，没匹配上的计数为 0；若写在 WHERE 里就会退化成 INNER JOIN。pandas 的做法是「先按条件聚合出右表，再 <code>merge(how='left')</code> + <code>fillna(0)</code>」，语义完全对应。",
)

ex(
    id="I06", level="intermediate", title="子查询",
    topics=["子查询", "WHERE"],
    description="查询薪资高于全公司平均薪资的员工。<br>输出两列：<code>name</code>、<code>salary</code>。",
    starterSql="SELECT name, salary\nFROM employees\nWHERE salary > (\n    -- 在这里写计算平均薪资的子查询\n);",
    starterPandas="# 先算平均值（mean 自动跳过 NaN），再过滤\navg_salary = employees['salary'].mean()\nresult = employees  # 补全过滤与选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT name, salary\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);",
    solutionPandas="avg_salary = employees['salary'].mean()\nresult = (employees[employees['salary'] > avg_salary]\n          [['name', 'salary']]\n          .reset_index(drop=True))",
    explanation="SQL 的子查询 <code>(SELECT AVG(salary) FROM employees)</code> 在 pandas 里就是先算出一个标量 <code>employees['salary'].mean()</code>，再拿它做过滤——子查询往往对应 pandas 里的「中间变量」。",
)

ex(
    id="I07", level="intermediate", title="CASE WHEN 条件分支",
    topics=["CASE WHEN", "条件逻辑"],
    description="为员工打薪资等级标签：<br>· 薪资 &gt;= 80000 → <code>High</code><br>· 薪资 &gt;= 60000 → <code>Mid</code><br>· 其余 → <code>Low</code><br>· 薪资为 NULL → <code>Unknown</code><br>输出三列：<code>name</code>、<code>salary</code>、<code>salary_level</code>。",
    starterSql="SELECT name,\n       salary,\n       CASE\n         -- 在这里补全 WHEN 分支（注意先判断 NULL）\n       END AS salary_level\nFROM employees;",
    starterPandas="# 用 np.select(条件列表, 取值列表, default=...) 实现多分支\nresult = employees[['name', 'salary']].copy()\nresult['salary_level'] = np.select([], [], default='Low')  # 补全条件与取值\n# 将最终结果赋值给 result",
    solutionSql="SELECT name,\n       salary,\n       CASE\n         WHEN salary IS NULL THEN 'Unknown'\n         WHEN salary >= 80000 THEN 'High'\n         WHEN salary >= 60000 THEN 'Mid'\n         ELSE 'Low'\n       END AS salary_level\nFROM employees;",
    solutionPandas="conditions = [\n    employees['salary'].isna(),\n    employees['salary'] >= 80000,\n    employees['salary'] >= 60000,\n]\nchoices = ['Unknown', 'High', 'Mid']\nresult = employees[['name', 'salary']].copy()\nresult['salary_level'] = np.select(conditions, choices, default='Low')",
    explanation="SQL 的 <code>CASE WHEN ... END</code> 按顺序匹配第一个为真的分支；pandas 的 <code>np.select(conditions, choices, default=...)</code> 同样按顺序取第一个满足的条件，两者一一对应。注意 NULL/NaN 的判断要放在最前面，因为 <code>NULL &gt;= 80000</code> 和 <code>NaN &gt;= 80000</code> 都不为真。",
)

ex(
    id="I08", level="intermediate", title="字符串处理",
    topics=["字符串", "UPPER", "LENGTH"],
    description="将客户姓名转为大写，并计算姓名的字符数。<br>输出两列：<code>name_upper</code>、<code>name_length</code>。",
    starterSql="SELECT\n    -- 用 UPPER() 和 LENGTH() 补全，并起别名\nFROM customers;",
    starterPandas="# pandas 字符串方法在 .str 命名空间下\nresult = pd.DataFrame({\n    'name_upper': customers['name'].str.upper(),\n    'name_length': None,  # 补全\n})\n# 将最终结果赋值给 result",
    solutionSql="SELECT UPPER(name) AS name_upper,\n       LENGTH(name) AS name_length\nFROM customers;",
    solutionPandas="result = pd.DataFrame({\n    'name_upper': customers['name'].str.upper(),\n    'name_length': customers['name'].str.len(),\n}).reset_index(drop=True)",
    explanation="SQL 的字符串函数 <code>UPPER()</code>、<code>LENGTH()</code> 在 pandas 中对应 <code>.str.upper()</code>、<code>.str.len()</code>。pandas 的字符串方法统一挂在 <code>.str</code> 访问器下。",
)

ex(
    id="I09", level="intermediate", title="日期过滤",
    topics=["日期", "WHERE", ".dt"],
    description="查询 2023 年第二季度（2023-04-01 至 2023-06-30）的订单。<br>输出四列：<code>order_id</code>、<code>product</code>、<code>amount</code>、<code>order_date</code>。<br>提示：SQL 中日期是 TEXT，可直接按字符串比较；pandas 中 order_date 已是 datetime64，也可以直接与日期字符串比较。",
    starterSql="SELECT order_id, product, amount, order_date\nFROM orders\n-- 用日期范围条件补全（也可用 strftime）;",
    starterPandas="# order_date 已是 datetime64，可与 'YYYY-MM-DD' 字符串直接比较\nmask = (orders['order_date'] >= '2023-04-01')  # 补全上界条件\nresult = orders  # 补全过滤与选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT order_id, product, amount, order_date\nFROM orders\nWHERE order_date >= '2023-04-01'\n  AND order_date <  '2023-07-01';",
    solutionPandas="mask = (orders['order_date'] >= '2023-04-01') & (orders['order_date'] < '2023-07-01')\nresult = (orders[mask]\n          [['order_id', 'product', 'amount', 'order_date']]\n          .reset_index(drop=True))",
    explanation="ISO 格式（YYYY-MM-DD）的日期字符串按字典序比较等价于按时间比较，所以 SQL 里可以直接写 <code>order_date &gt;= '2023-04-01'</code>；若要按月份提取，SQL 用 <code>strftime('%m', order_date)</code>，pandas 用 <code>orders['order_date'].dt.month</code>。本题用「&gt;= 下界 且 &lt; 上界」的半开区间写法最稳妥。",
)

ex(
    id="I10", level="intermediate", title="每组 Top-1（相关子查询）",
    topics=["Top-N", "子查询", "GROUP BY"],
    description="找出每个部门薪资最高的员工（每个部门恰好一人，无并列）。<br>输出三列：<code>dept</code>、<code>name</code>、<code>salary</code>。",
    starterSql="SELECT dept, name, salary\nFROM employees e\nWHERE salary = (\n    -- 在这里写「该员工所在部门的最高薪资」子查询\n);",
    starterPandas="# 用 groupby + idxmax 找到每组最大值所在的行索引\nidx = employees.groupby('dept')['salary'].idxmax()\nresult = employees  # 用 loc 按 idx 取行并选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT dept, name, salary\nFROM employees e\nWHERE salary = (SELECT MAX(salary)\n                FROM employees\n                WHERE dept = e.dept);",
    solutionPandas="idx = employees.groupby('dept')['salary'].idxmax()\nresult = (employees.loc[idx, ['dept', 'name', 'salary']]\n          .reset_index(drop=True))",
    explanation="SQL 用相关子查询「本部门最高薪资」来定位每组的 Top-1；pandas 里 <code>groupby('dept')['salary'].idxmax()</code> 直接返回每组最大值所在的行索引，再用 <code>loc</code> 取整行。有并列时两种写法的行为会不同（子查询返回多行，idxmax 只取一行），本题数据无并列。进阶玩法是窗口函数（见 A01/A07）。",
)

# ============ 精通 Advanced A01-A10 ============

ex(
    id="A01", level="advanced", title="窗口函数 ROW_NUMBER",
    topics=["窗口函数", "ROW_NUMBER", "排名"],
    description="在每个部门内部按薪资从高到低编号。<br>输出四列：<code>dept</code>、<code>name</code>、<code>salary</code>、<code>salary_rank</code>（每个部门从 1 开始；薪资为 NULL 的排在该部门最后）。",
    starterSql="SELECT dept, name, salary,\n       ROW_NUMBER() OVER (\n         -- 补全 PARTITION BY 和 ORDER BY\n       ) AS salary_rank\nFROM employees;",
    starterPandas="# 思路：先排序，再用 groupby().cumcount() 生成组内序号\nd = employees.sort_values(['dept', 'salary'], ascending=[True, False])\nd['salary_rank'] = 0  # 补全\nd = d[['dept', 'name', 'salary', 'salary_rank']]\nresult = d\n# 将最终结果赋值给 result",
    solutionSql="SELECT dept,\n       name,\n       salary,\n       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS salary_rank\nFROM employees;",
    solutionPandas="d = employees.sort_values(['dept', 'salary'], ascending=[True, False])\nd['salary_rank'] = d.groupby('dept').cumcount() + 1\nresult = d[['dept', 'name', 'salary', 'salary_rank']].reset_index(drop=True)",
    explanation="<code>ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)</code> 在 pandas 里可拆成「排序 + <code>groupby().cumcount() + 1</code>」。若允许并列同名次，SQL 用 <code>RANK()</code>，pandas 对应 <code>groupby(...).rank(method='min', ascending=False)</code>。",
)

ex(
    id="A02", level="advanced", title="窗口函数累计求和",
    topics=["窗口函数", "累计和", "SUM OVER"],
    description="忽略金额为 NULL 的订单，按日期统计每日销售额以及截至当日的累计销售额。<br>输出三列：<code>order_date</code>、<code>daily_amount</code>、<code>running_total</code>。",
    starterSql="SELECT order_date,\n       SUM(amount) AS daily_amount,\n       -- 补全：对每日金额做窗口累计求和\nFROM orders\nWHERE amount IS NOT NULL\nGROUP BY order_date;",
    starterPandas="# 思路：dropna -> groupby 求和 -> cumsum\nd = orders.dropna(subset=['amount'])\nresult = d  # 补全分组求和、排序、累计和\n# 将最终结果赋值给 result",
    solutionSql="SELECT order_date,\n       SUM(amount) AS daily_amount,\n       SUM(SUM(amount)) OVER (ORDER BY order_date) AS running_total\nFROM orders\nWHERE amount IS NOT NULL\nGROUP BY order_date;",
    solutionPandas="d = (orders.dropna(subset=['amount'])\n     .groupby('order_date', as_index=False)['amount'].sum()\n     .rename(columns={'amount': 'daily_amount'})\n     .sort_values('order_date'))\nd['running_total'] = d['daily_amount'].cumsum()\nresult = d.reset_index(drop=True)",
    explanation="SQL 里 <code>SUM(SUM(amount)) OVER (ORDER BY order_date)</code> 是「聚合之上再开窗」；pandas 里对应 <code>groupby().sum()</code> 之后再 <code>.cumsum()</code>。先过滤 NULL 金额是为了避免「SQL 全 NULL 组 SUM 得 NULL 而 pandas 得 0」的边界差异。",
)

ex(
    id="A03", level="advanced", title="自连接查经理",
    topics=["自连接", "JOIN"],
    description="employees 表的 <code>manager_id</code> 指向本表的 <code>id</code>。查询每位员工及其直属经理的姓名（只保留有经理的员工）。<br>输出两列：<code>emp_name</code>、<code>manager_name</code>。",
    starterSql="SELECT e.name AS emp_name,\n       m.name AS manager_name\nFROM employees e\n-- 补全：把 employees 再 JOIN 一次，起别名 m;",
    starterPandas="# 思路：employees 与自身 merge，左键 manager_id，右键 id\nm = employees.merge(employees[['id', 'name']],\n                    left_on='manager_id', right_on='id',\n                    suffixes=('', '_mgr'))\nresult = m  # 补全选列与重命名\n# 将最终结果赋值给 result",
    solutionSql="SELECT e.name AS emp_name,\n       m.name AS manager_name\nFROM employees e\nJOIN employees m ON e.manager_id = m.id;",
    solutionPandas="m = employees.merge(employees[['id', 'name']],\n                    left_on='manager_id', right_on='id',\n                    how='inner', suffixes=('', '_mgr'))\nresult = (m[['name', 'name_mgr']]\n          .rename(columns={'name': 'emp_name', 'name_mgr': 'manager_name'})\n          .reset_index(drop=True))",
    explanation="自连接就是「同一张表起两个别名各当一张表用」：SQL 用 <code>employees e JOIN employees m</code>；pandas 用 <code>merge(..., left_on='manager_id', right_on='id')</code>，靠 <code>suffixes</code> 区分两侧的同名列。manager_id 为 NULL 的行在内连接中自然被丢弃。",
)

ex(
    id="A04", level="advanced", title="透视表（条件聚合）",
    topics=["透视表", "CASE WHEN", "pivot_table"],
    description="统计每个城市 VIP（vip=1）与非 VIP（vip=0）客户的数量。<br>输出三列：<code>city</code>、<code>vip_count</code>、<code>non_vip_count</code>。",
    starterSql="SELECT city,\n       -- 用 SUM(CASE WHEN ...) 分别统计两类客户\nFROM customers\nGROUP BY city;",
    starterPandas="# 用 pivot_table 做透视，再重命名列\np = customers.pivot_table(index='city', columns='vip',\n                          values='name', aggfunc='count', fill_value=0)\nresult = p  # 补全重命名、reset_index、选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT city,\n       SUM(CASE WHEN vip = 1 THEN 1 ELSE 0 END) AS vip_count,\n       SUM(CASE WHEN vip = 0 THEN 1 ELSE 0 END) AS non_vip_count\nFROM customers\nGROUP BY city;",
    solutionPandas="p = customers.pivot_table(index='city', columns='vip',\n                          values='name', aggfunc='count', fill_value=0)\np = p.rename(columns={1: 'vip_count', 0: 'non_vip_count'}).reset_index()\nresult = p[['city', 'vip_count', 'non_vip_count']]",
    explanation="SQL 没有 PIVOT 关键字，通用做法是 <code>SUM(CASE WHEN ... THEN 1 ELSE 0 END)</code> 条件聚合，每个输出列一个表达式；pandas 的 <code>pivot_table(index=..., columns=..., aggfunc='count', fill_value=0)</code> 一步生成宽表，再按需重命名列。",
)

ex(
    id="A05", level="advanced", title="melt 宽表转长表",
    topics=["melt", "UNION ALL", "宽转长"],
    description="先统计每个产品（product）的订单数与总销量，得到宽表：<br><pre>product | order_count | total_quantity</pre>再把它转成长表，输出三列：<code>product</code>、<code>metric</code>（取值为 <code>order_count</code> 或 <code>total_quantity</code>）、<code>value</code>，共 8 行。<br>提示：SQL 侧用 UNION ALL 把两次分组结果纵向拼起来；pandas 侧用 melt。",
    starterSql="SELECT product, 'order_count' AS metric, COUNT(*) AS value\nFROM orders\nGROUP BY product\n-- 补全：UNION ALL 第二个 SELECT（total_quantity）;",
    starterPandas="# 先构造宽表，再用 melt 转长\nwide = orders.groupby('product', as_index=False).agg(\n    order_count=('order_id', 'count'),\n    total_quantity=('quantity', 'sum'),\n)\nresult = wide  # 补全 melt\n# 将最终结果赋值给 result",
    solutionSql="SELECT product, 'order_count' AS metric, COUNT(*) AS value\nFROM orders\nGROUP BY product\nUNION ALL\nSELECT product, 'total_quantity', SUM(quantity)\nFROM orders\nGROUP BY product;",
    solutionPandas="wide = (orders.groupby('product', as_index=False)\n        .agg(order_count=('order_id', 'count'),\n             total_quantity=('quantity', 'sum')))\nresult = wide.melt(id_vars='product', var_name='metric', value_name='value')",
    explanation="宽转长：SQL 里用 <code>UNION ALL</code> 把每个指标各查一遍再纵向拼接，metric 列用字符串字面量生成；pandas 的 <code>melt(id_vars='product', var_name='metric', value_name='value')</code> 把 order_count、total_quantity 两列「融化」成行，语义一致。",
)

ex(
    id="A06", level="advanced", title="缺失值填充",
    topics=["COALESCE", "fillna", "NULL"],
    description="查询所有订单，金额（amount）为 NULL 的以 0 显示。<br>输出三列：<code>order_id</code>、<code>product</code>、<code>amount_filled</code>。",
    starterSql="SELECT order_id,\n       product,\n       -- 用 COALESCE 补全\nFROM orders;",
    starterPandas="# 用 fillna 填充缺失值\nresult = orders[['order_id', 'product']].copy()\nresult['amount_filled'] = orders['amount']  # 补全 fillna\n# 将最终结果赋值给 result",
    solutionSql="SELECT order_id,\n       product,\n       COALESCE(amount, 0) AS amount_filled\nFROM orders;",
    solutionPandas="result = orders[['order_id', 'product']].copy()\nresult['amount_filled'] = orders['amount'].fillna(0)",
    explanation="SQL 的 <code>COALESCE(amount, 0)</code> 返回第一个非 NULL 参数；pandas 的 <code>.fillna(0)</code> 把 NaN 替换为 0。SQL 中还有 <code>IFNULL()</code>（两个参数版本），pandas 中还有 <code>.fillna(method=...)</code> 等填充策略。",
)

ex(
    id="A07", level="advanced", title="去重保留最新",
    topics=["ROW_NUMBER", "去重", "窗口函数"],
    description="找出每个客户最近的一笔订单（按 order_date，无并列）。<br>输出四列：<code>customer_id</code>、<code>order_id</code>、<code>product</code>、<code>order_date</code>。",
    starterSql="SELECT customer_id, order_id, product, order_date\nFROM (\n  SELECT *,\n         ROW_NUMBER() OVER (\n           -- 补全：按客户分区、按日期倒序\n         ) AS rn\n  FROM orders\n)\n-- 补全：只保留每个客户的第一名;",
    starterPandas="# 思路：按日期排序后，drop_duplicates 保留每个客户的最后一行\nd = orders.sort_values('order_date')\nresult = d  # 补全去重与选列\n# 将最终结果赋值给 result",
    solutionSql="SELECT customer_id, order_id, product, order_date\nFROM (\n  SELECT *,\n         ROW_NUMBER() OVER (PARTITION BY customer_id\n                            ORDER BY order_date DESC) AS rn\n  FROM orders\n)\nWHERE rn = 1;",
    solutionPandas="d = orders.sort_values('order_date')\nresult = (d.drop_duplicates('customer_id', keep='last')\n          [['customer_id', 'order_id', 'product', 'order_date']]\n          .reset_index(drop=True))",
    explanation="「每组取最新一行」的经典 SQL 写法是 ROW_NUMBER 窗口 + 外层 <code>WHERE rn = 1</code>；pandas 的等价写法是排序后 <code>drop_duplicates('customer_id', keep='last')</code>。也可以用 <code>groupby('customer_id')['order_date'].idxmax()</code>（类似 I10）。",
)

ex(
    id="A08", level="advanced", title="条件分组统计",
    topics=["CASE WHEN", "条件分组", "聚合"],
    description="按订单金额分档统计订单数：<br>· amount &lt; 100 → <code>small</code><br>· 100 &lt;= amount &lt;= 500 → <code>medium</code><br>· amount &gt; 500 → <code>large</code><br>· amount 为 NULL → <code>unknown</code><br>输出两列：<code>amount_range</code>、<code>order_count</code>（共 4 行）。",
    starterSql="SELECT CASE\n         -- 补全分档逻辑\n       END AS amount_range,\n       COUNT(*) AS order_count\nFROM orders\nGROUP BY amount_range;",
    starterPandas="# 用 np.select 生成标签列，再 groupby 计数\nd = orders.copy()\nd['amount_range'] = np.select([], [], default='large')  # 补全\nresult = d  # 补全分组计数\n# 将最终结果赋值给 result",
    solutionSql="SELECT CASE\n         WHEN amount IS NULL THEN 'unknown'\n         WHEN amount < 100 THEN 'small'\n         WHEN amount <= 500 THEN 'medium'\n         ELSE 'large'\n       END AS amount_range,\n       COUNT(*) AS order_count\nFROM orders\nGROUP BY amount_range;",
    solutionPandas="conditions = [\n    orders['amount'].isna(),\n    orders['amount'] < 100,\n    orders['amount'] <= 500,\n]\nchoices = ['unknown', 'small', 'medium']\nd = orders.copy()\nd['amount_range'] = np.select(conditions, choices, default='large')\nresult = (d.groupby('amount_range', as_index=False)\n          .size()\n          .rename(columns={'size': 'order_count'}))",
    explanation="「先打标签再聚合」是条件分组的通用套路：SQL 用 CASE 生成标签列并直接 GROUP BY（SQLite 允许按别名分组）；pandas 用 <code>np.select</code> 生成标签列，再 <code>groupby(...).size()</code> 计数。NULL/NaN 的判断都要放最前面。",
)

ex(
    id="A09", level="advanced", title="连接后聚合",
    topics=["JOIN", "GROUP BY", "聚合"],
    description="统计每个城市的客户消费总额（amount 之和，忽略 NULL；只统计有订单的城市）。<br>输出两列：<code>city</code>、<code>total_spent</code>。",
    starterSql="SELECT c.city,\n       -- 补全聚合表达式\nFROM customers c\n-- 补全 JOIN 与 GROUP BY;",
    starterPandas="# 先 merge 再 groupby 求和，最后把列名改为 total_spent\nm = orders.merge(customers[['customer_id', 'city']], on='customer_id')\nresult = m  # 补全分组聚合\n# 将最终结果赋值给 result",
    solutionSql="SELECT c.city,\n       SUM(o.amount) AS total_spent\nFROM customers c\nJOIN orders o ON o.customer_id = c.customer_id\nGROUP BY c.city;",
    solutionPandas="m = orders.merge(customers[['customer_id', 'city']], on='customer_id', how='inner')\nresult = (m.groupby('city', as_index=False)['amount'].sum()\n          .rename(columns={'amount': 'total_spent'}))",
    explanation="「连接 + 分组 + 聚合」是最常见的分析组合：SQL 一条语句完成 <code>JOIN ... GROUP BY ... SUM()</code>；pandas 对应 <code>merge</code> → <code>groupby().sum()</code> → <code>rename</code> 三步。两侧的 SUM/sum 都自动忽略空值。",
)

ex(
    id="A10", level="advanced", title="综合报表：城市消费分层",
    topics=["综合报表", "多层聚合", "CTE"],
    description="生成城市消费报表：<br>第一步：算出每个客户的消费总额（连接 orders 与 customers，忽略 NULL 金额）；<br>第二步：按城市汇总，输出 <code>city</code>、<code>buyer_count</code>（有消费的客户数）、<code>avg_spent</code>（客户平均消费）、<code>max_spent</code>（单客户最高消费）。<br>提示：SQL 可用 CTE（WITH）或子查询实现多层聚合。",
    starterSql="WITH cust AS (\n  -- 第一层：每个客户的消费总额\n)\n-- 第二层：按城市汇总\nSELECT city FROM cust;",
    starterPandas="# 第一层：merge 后按 城市+客户 分组求和\nm = orders.merge(customers[['customer_id', 'city']], on='customer_id')\ncust = m  # 补全第一层聚合\n# 第二层：按城市再聚合\nresult = cust  # 补全第二层聚合\n# 将最终结果赋值给 result",
    solutionSql="WITH cust AS (\n  SELECT c.city,\n         c.customer_id,\n         SUM(o.amount) AS total\n  FROM customers c\n  JOIN orders o ON o.customer_id = c.customer_id\n  GROUP BY c.city, c.customer_id\n)\nSELECT city,\n       COUNT(*) AS buyer_count,\n       AVG(total) AS avg_spent,\n       MAX(total) AS max_spent\nFROM cust\nGROUP BY city;",
    solutionPandas="m = orders.merge(customers[['customer_id', 'city']], on='customer_id', how='inner')\ncust = (m.groupby(['city', 'customer_id'], as_index=False)['amount'].sum()\n        .rename(columns={'amount': 'total'}))\nresult = (cust.groupby('city', as_index=False)\n          .agg(buyer_count=('customer_id', 'count'),\n               avg_spent=('total', 'mean'),\n               max_spent=('total', 'max')))",
    explanation="多层聚合 = 对聚合结果再聚合。SQL 用 CTE 把「每客户总额」固化为中间表，再 <code>GROUP BY city</code> 做第二层；pandas 完全同构：先 <code>groupby(['city','customer_id']).sum()</code>，再 <code>groupby('city').agg(...)</code>。中间结果取个名字（CTE / 变量），是两侧共同的工程实践。",
)

# ============ 输出 ============

assert len(E) == 30, f"expected 30 exercises, got {len(E)}"

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
