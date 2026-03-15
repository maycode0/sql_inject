# SQL 注入学习手册

## 1. 手册说明

这是一份围绕 SQL 注入的完整学习手册，适合从入门到进阶系统学习。

手册目标：

- 帮你理解 SQL 注入的原理
- 帮你建立分阶段学习路径
- 帮你通过程序示例理解脆弱写法与安全写法
- 帮你通过练习题完成自测与巩固

本手册内容仅用于安全学习、开发防御与授权环境中的教学演示。

---

## 2. 学习目标

完成本手册内容后，你应该能够：

1. 理解 SQL 注入的定义、成因与危害。
2. 看懂常见易受攻击的 SQL 拼接代码。
3. 掌握参数化查询、白名单、最小权限等核心防御手段。
4. 能用本地程序示例看懂脆弱写法与安全写法的差异。
5. 具备基础代码审计和风险识别思维。

---

## 3. 什么是 SQL 注入

SQL 注入是指：应用程序将用户输入直接拼接进 SQL 语句，导致输入不再只是数据，而是可能影响 SQL 的执行逻辑，从而造成绕过验证、读取敏感数据、篡改数据甚至破坏业务的风险。

### 3.1 本质原因

本质就是一句话：

- 程序把用户输入当成了 SQL 代码结构的一部分。

更具体地说，通常有以下原因：

- 开发者通过字符串拼接构造 SQL
- 没有正确使用参数化查询
- 对动态结构位置缺少白名单控制

### 3.2 常见危害

- 绕过登录验证
- 查询敏感数据
- 修改或删除数据
- 影响业务可用性
- 在复杂系统中扩大攻击面

---

## 4. 学习路线总览

建议按三阶段推进：

- 初级阶段：理解原理，能看懂基础漏洞
- 中级阶段：识别风险点，能完成基础防护
- 高级阶段：进行代码审计，处理复杂动态场景

建议学习周期：

- 初级：3 到 5 天
- 中级：5 到 7 天
- 高级：7 到 14 天

---

## 5. 初级阶段：建立基础认知

### 5.1 学习目标

完成初级阶段后，你应该能够：

1. 说清 SQL 注入的定义。
2. 理解用户输入如何进入 SQL 查询。
3. 看懂最基础的拼接式漏洞代码。
4. 理解参数化查询为什么更安全。

### 5.2 必学知识点

- SQL 基础语法：`SELECT`、`WHERE`、`INSERT`、`UPDATE`、`DELETE`
- Web 应用与数据库交互流程
- 用户输入如何进入后端查询逻辑
- 字符串拼接 SQL 的风险
- 参数化查询 / 预编译语句

### 5.3 实践任务

1. 建一个简单的 `users` 表。
2. 写一个普通登录查询。
3. 再写一个参数化版本。
4. 观察两种写法的结构差异。

### 5.4 阶段验收标准

- 能解释 SQL 注入的根本原因
- 能指出拼接 SQL 的危险点
- 能独立写一个参数化查询示例

---

## 6. 中级阶段：识别风险与完成基础防护

### 6.1 学习目标

完成中级阶段后，你应该能够：

1. 在业务代码中识别常见注入风险点。
2. 理解搜索、分页、排序等场景同样可能有风险。
3. 知道哪些位置适合参数化，哪些位置要使用白名单。
4. 能设计基础防御方案。

### 6.2 必学知识点

- 常见输入入口：表单、URL、API、报表筛选
- 常见风险场景：登录、搜索、ID 查询、排序、动态列名、动态表名
- 黑名单过滤为什么不可靠
- 输入校验与类型约束
- 最小权限原则
- 异常处理与日志审计

### 6.3 实践任务

1. 写一个搜索功能，并比较拼接版与参数化版。
2. 写一个带排序参数的列表功能。
3. 给排序字段做白名单映射。
4. 对分页参数做整数校验。
5. 模拟异常并统一处理错误返回。

### 6.4 阶段验收标准

- 能指出业务代码中的潜在注入入口
- 知道参数化和白名单分别解决什么问题
- 能写出更完整的基础防护代码

---

## 7. 高级阶段：审计、复杂场景与系统化安全思维

### 7.1 学习目标

完成高级阶段后，你应该能够：

1. 在较大项目中定位高风险 SQL 构造点。
2. 理解 ORM、查询构造器与原生 SQL 混用时的风险。
3. 识别复杂动态查询中的结构性风险。
4. 建立开发、测试、审计一体化安全思维。

### 7.2 必学知识点

- 代码审计中的危险模式识别
- 字符串拼接 SQL 与模板字符串拼接
- 动态 `ORDER BY`
- 动态列名、表名
- ORM 中执行原生 SQL 的风险
- 多层架构中的输入传递链
- 安全测试环境中的验证思路
- 日志、告警与审计思路

### 7.3 实践任务

1. 选一个小型项目，找出所有 SQL 构造位置。
2. 区分值位置风险和结构位置风险。
3. 为每个风险点给出修复方案。
4. 汇总成 SQL 安全检查清单。
5. 设计上线前数据库访问代码审查流程。

### 7.4 阶段验收标准

- 能系统分析一个模块的 SQL 风险
- 能区分理论危险和实际影响
- 能提出兼顾安全与可维护性的修复建议

---

## 8. 重点知识讲解

### 8.1 一个典型的脆弱场景

例如登录查询写成：

```sql
SELECT * FROM users WHERE username = '用户输入' AND password = '用户输入';
```

如果程序通过字符串拼接生成这条 SQL，那么用户输入一旦被混入查询文本，就可能改变原始逻辑。

### 8.2 为什么参数化查询有效

参数化查询会把 SQL 模板和参数分开传给数据库驱动，参数只作为值处理，不参与 SQL 结构解释。

例如：

```sql
SELECT * FROM users WHERE username = ? AND password = ?
```

### 8.3 为什么只过滤特殊字符不够

因为：

- 数据库语法复杂
- 黑名单无法覆盖所有情况
- 业务中的风险入口很多，不止是单引号

正确思路是：

- 值位置用参数化
- 结构位置用白名单

### 8.4 哪些位置也可能有风险

除了登录表单，还包括：

- 搜索框
- URL 参数
- 分页参数
- 排序字段
- 后台筛选条件
- API 查询条件

特别注意：

- 表名、字段名、排序字段、排序方向通常要通过白名单控制

---

## 9. 防御清单

### 必做项

- 所有查询默认使用参数化语句
- 禁止直接拼接用户输入构造 SQL
- 数据库账号按最小权限配置
- 异常统一处理，避免数据库原始报错直接暴露
- 关键失败行为写入日志，便于审计

### 强烈建议

- 使用成熟驱动与 ORM
- 对输入做类型约束和长度约束
- 对动态排序字段做白名单
- 把安全测试纳入开发流程

### 不推荐依赖

- 单纯关键字过滤
- 单纯转义字符
- 只依赖前端校验

---

## 10. 程序示例演示

下面给出一个本地教学示例，帮助你观察脆弱写法与安全写法的区别。

### 10.1 演示目标

通过同一组输入，对比：

1. `vulnerable_login`：直接拼接 SQL
2. `safe_login`：使用参数化查询
3. `vulnerable_list_users`：直接拼接排序字段
4. `safe_list_users`：使用白名单映射排序字段

### 10.2 演示代码

可直接运行的代码文件：`docs/sql_injection_demo.py`

这个演示现在包含两类教学场景：

- 登录查询场景：演示值位置为什么要参数化
- 排序字段场景：演示结构位置为什么要白名单

核心代码如下：

```python
import sqlite3


def setup_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    cursor.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        [
            ("admin", "admin123"),
            ("alice", "alice123"),
            ("bob", "bob123"),
        ],
    )

    conn.commit()
    return conn


def vulnerable_login(conn, username, password):
    cursor = conn.cursor()
    query = (
        "SELECT id, username FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    print("[Vulnerable SQL]")
    print(query)

    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as exc:
        return [f"SQL error: {exc}"]


def safe_login(conn, username, password):
    cursor = conn.cursor()
    query = "SELECT id, username FROM users WHERE username = ? AND password = ?"

    print("[Safe SQL]")
    print(query)
    print("[Params]", (username, password))

    cursor.execute(query, (username, password))
    return cursor.fetchall()


def vulnerable_list_users(conn, order_by):
    cursor = conn.cursor()
    query = f"SELECT id, username FROM users ORDER BY {order_by}"

    print("[Vulnerable Sort SQL]")
    print(query)

    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as exc:
        return [f"SQL error: {exc}"]


def safe_list_users(conn, order_by):
    cursor = conn.cursor()
    allowed_fields = {
        "id": "id",
        "username": "username",
    }

    safe_field = allowed_fields.get(order_by, "id")
    query = f"SELECT id, username FROM users ORDER BY {safe_field}"

    print("[Safe Sort SQL]")
    print(query)
    print("[Allowed field]", safe_field)

    cursor.execute(query)
    return cursor.fetchall()


def run_case(conn, title, username, password):
    print(f"\n=== {title} ===")
    print("Input username =", repr(username))
    print("Input password =", repr(password))
    print("Vulnerable result:", vulnerable_login(conn, username, password))
    print("Safe result:", safe_login(conn, username, password))


def run_sort_case(conn, title, order_by):
    print(f"\n=== {title} ===")
    print("Input order_by =", repr(order_by))
    print("Vulnerable sort result:", vulnerable_list_users(conn, order_by))
    print("Safe sort result:", safe_list_users(conn, order_by))


def main():
    conn = setup_database()

    run_case(conn, "Normal login", "alice", "alice123")
    run_case(conn, "Teaching-only invalid input", "alice", "' OR '1'='1")
    run_sort_case(conn, "Normal sort", "username")
    run_sort_case(conn, "Sort whitelist fallback", "username DESC, id")

    conn.close()


if __name__ == "__main__":
    main()
```

### 10.3 运行方式

```bash
python docs/sql_injection_demo.py
```

如果你的环境中 `python` 不可用，也可以尝试：

```bash
py docs/sql_injection_demo.py
```

### 10.4 观察重点

- 脆弱写法会把输入直接放进 SQL 文本
- 安全写法会保持 SQL 模板不变
- 真正危险的是拼接方式，而不是某个字符本身

进一步理解：

- 登录示例强调“值位置”要用参数化查询
- 排序示例强调“结构位置”通常要用白名单控制
- 参数化和白名单不是互相替代，而是分别处理不同类型的风险

---

## 11. 每周学习安排建议

### 第 1 周

- 学习 SQL 基础查询
- 阅读本手册前半部分
- 运行 `docs/sql_injection_demo.py`
- 看懂拼接式 SQL 与参数化 SQL 的区别

### 第 2 周

- 学习搜索、分页、排序场景风险
- 实现类型校验与字段白名单
- 总结自己的基础防御清单

### 第 3 周及以后

- 对一个小项目做静态检查
- 搜索所有 SQL 构造位置
- 记录风险点与修复方案
- 形成自己的审计模板

---

## 12. 自测练习题

### 基础题

1. SQL 注入的根本原因是什么？
2. 为什么字符串拼接 SQL 有风险？
3. 参数化查询的核心作用是什么？
4. 为什么黑名单过滤通常不可靠？
5. 除了登录框，还有哪些常见输入入口？

### 理解题

1. 什么是值位置？什么是结构位置？
2. 为什么排序字段通常需要白名单？
3. 最小权限原则在防御中有什么价值？
4. 为什么不能把数据库原始报错直接返回前端？

### 代码分析题

请分析以下代码为什么有风险：

```python
def get_user(conn, user_id):
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()
```

```python
def search_user(conn, keyword):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username LIKE '%" + keyword + "%'"
    cursor.execute(query)
    return cursor.fetchall()
```

```python
def list_users(conn, order_by):
    cursor = conn.cursor()
    query = f"SELECT id, username FROM users ORDER BY {order_by}"
    cursor.execute(query)
    return cursor.fetchall()
```

### 场景题

1. 如果你在项目里发现大量拼接 SQL，应如何系统整改？
2. 如果业务必须支持 `name`、`created_at`、`id` 排序，你会如何设计白名单？

---

## 13. 练习题参考答案

### 基础题答案

1. 根本原因是程序把用户输入当成 SQL 代码的一部分处理。
2. 因为拼接会让输入直接进入 SQL 结构。
3. 参数化查询会把输入作为数据而不是 SQL 代码处理。
4. 因为数据库语法复杂，黑名单难以覆盖全部情况。
5. 常见入口包括搜索框、URL 参数、分页参数、排序字段、API 查询条件、报表筛选条件。

### 理解题答案

1. 值位置通常指查询条件中的参数值，适合参数化；结构位置通常指表名、列名、排序字段、排序方向等，更适合白名单。
2. 因为排序字段通常属于 SQL 结构的一部分。
3. 最小权限原则可以在漏洞存在时减少破坏范围。
4. 因为原始报错可能泄露数据库表结构、字段名和实现细节。

### 代码分析题答案

1. `get_user` 的风险在于把 `user_id` 直接拼接进 SQL，应改为参数化：

```python
def get_user(conn, user_id):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()
```

2. `search_user` 的风险在于 `LIKE` 语句仍然使用了拼接，应改为参数化：

```python
def search_user(conn, keyword):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username LIKE ?"
    cursor.execute(query, (f"%{keyword}%",))
    return cursor.fetchall()
```

3. `list_users` 的风险在于 `order_by` 会直接影响 SQL 结构，应使用白名单映射，例如：

```python
def list_users(conn, order_by):
    allowed_fields = {
        "id": "id",
        "name": "username",
        "created": "created_at",
    }

    order_field = allowed_fields.get(order_by, "id")
    query = f"SELECT id, username FROM users ORDER BY {order_field}"

    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
```

### 场景题答案

1. 系统整改步骤可以是：搜索所有拼接 SQL、区分值位置和结构位置、值位置改参数化、结构位置改白名单、检查数据库权限、补异常处理和日志、在测试环境验证修复结果。
2. 可以为 `name`、`created_at`、`id` 建立一个固定映射表，只允许这些预定义字段参与排序，不在白名单中的输入统一回退到默认字段。

---

## 14. 一页结论

记住这三句话：

- SQL 注入的本质，是把用户输入当成 SQL 代码执行了。
- 基础防御核心，是参数化查询。
- 动态结构位置，要用白名单；数据库权限，要坚持最小权限。

如果你在开发中看到字符串拼接 SQL，就应该立刻提高警惕。
