# SQL 注入学习内容与程序示例演示

## 1. 学习目标

完成本学习内容后，你应该能够：

1. 理解 SQL 注入的定义、成因与常见危害。
2. 识别常见的易受攻击代码写法。
3. 掌握参数化查询、输入校验、最小权限等核心防护方法。
4. 能通过一个本地示例看懂“脆弱写法”与“安全写法”的区别。
5. 建立合法合规的安全测试意识，只在授权环境中进行验证。

---

## 2. 什么是 SQL 注入

SQL 注入（SQL Injection）是指：应用程序把用户输入直接拼接进 SQL 语句，导致攻击者可以改变原本 SQL 的语义，从而达到绕过登录、读取敏感数据、篡改数据，甚至进一步控制系统的目的。

### 2.1 本质原因

本质上是：

- 程序把“数据”当成了“SQL 代码”的一部分。
- 开发者使用字符串拼接构造 SQL。
- 输入没有经过正确的参数绑定。

### 2.2 常见危害

- 绕过登录验证。
- 查询本不该公开的数据。
- 修改或删除数据库内容。
- 影响业务可用性。
- 在某些场景下配合数据库特性扩大攻击面。

---

## 3. 学习路线

建议按下面顺序学习：

### 第一阶段：基础认知

- SQL 基本语法：`SELECT`、`WHERE`、`INSERT`、`UPDATE`、`DELETE`
- Web 应用与数据库交互流程
- 用户输入如何进入 SQL 查询

### 第二阶段：漏洞形成原理

- 字符串拼接为什么危险
- 单引号、注释符、逻辑条件在 SQL 中的作用
- “预期查询”如何被“恶意输入”改变语义

### 第三阶段：注入类型认知

- 登录绕过类注入
- 联合查询类注入（仅理解原理）
- 布尔盲注、时间盲注（理解概念即可）
- 报错型注入（理解概念即可）

说明：学习时重点是理解漏洞机理与修复方案，不建议把精力放在攻击技巧堆砌上。

### 第四阶段：防御实践

- 参数化查询 / 预编译语句
- ORM 的安全使用方式
- 输入校验
- 输出最小化
- 数据库账号最小权限
- 错误信息控制与日志审计

### 第五阶段：代码审计与验证

- 看到字符串拼接 SQL 时保持警惕
- 识别常见危险模式，如：
  - `"SELECT ... '" + userInput + "'"`
  - 模板字符串直接拼接查询条件
  - 动态拼接排序、表名、字段名
- 使用安全测试环境验证修复是否有效

---

## 4. 重点知识讲解

### 4.1 一个典型的脆弱场景

假设登录查询写成：

```sql
SELECT * FROM users WHERE username = '用户输入' AND password = '用户输入';
```

如果程序是直接拼接字符串，那么用户输入一旦包含 SQL 语义，就可能改变整个查询逻辑。

问题不在于“输入里有特殊字符”，而在于“程序没有把输入当作纯数据处理”。

### 4.2 为什么参数化查询有效

参数化查询会把 SQL 模板和参数值分开传递，数据库驱动会把参数当成数据，而不是可执行 SQL 片段。

例如：

```sql
SELECT * FROM users WHERE username = ? AND password = ?
```

此时无论输入内容如何，都会被作为值处理，不会轻易改变查询结构。

### 4.3 仅靠过滤特殊字符为什么不够

很多初学者会尝试：

- 替换单引号
- 删除关键字
- 黑名单拦截某些字符

这类方式通常不可靠，因为：

- 数据库语法复杂，绕过方式多。
- 黑名单很难穷尽全部情况。
- 业务中还有数字、排序字段、模糊搜索等多种注入入口。

正确做法是：

- 优先使用参数化查询。
- 对无法参数化的位置使用白名单。

### 4.4 哪些位置也可能有风险

除了登录表单，还包括：

- 搜索框
- URL 参数
- 分页参数
- 排序字段
- 后台报表筛选条件
- API 查询条件

特别注意：表名、字段名、排序方向这类标识符通常不能直接参数化，必须通过白名单映射处理。

---

## 5. 防御清单

在开发中，可按下面清单检查：

### 必做项

- 所有查询默认使用参数化语句。
- 禁止直接拼接用户输入构造 SQL。
- 数据库账号按最小权限配置。
- 对异常信息做统一处理，避免将数据库报错直接返回前端。
- 在日志中记录关键失败行为，便于审计。

### 强烈建议

- 使用成熟数据库驱动和 ORM。
- 对输入进行类型约束与长度约束。
- 对动态排序字段使用白名单。
- 将安全测试纳入开发与上线流程。

### 不推荐依赖

- 单纯关键字过滤
- 单纯转义字符
- 只依赖前端校验

---

## 6. 学习完成后的程序示例演示

下面给出一个 **仅用于本地教学演示** 的 Python + SQLite 示例，用来对比：

- 脆弱写法：字符串拼接 SQL
- 安全写法：参数化查询

请只在本地学习环境中运行，不要用于任何未授权系统。

### 6.1 演示目标

通过同一组输入，观察两种写法的行为差异：

1. 脆弱版本可能出现非预期结果。
2. 安全版本会把输入当作普通字符串处理。

### 6.2 示例代码

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

    print("[脆弱写法 SQL]")
    print(query)

    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as exc:
        return [f"SQL error: {exc}"]


def safe_login(conn, username, password):
    cursor = conn.cursor()
    query = "SELECT id, username FROM users WHERE username = ? AND password = ?"

    print("[安全写法 SQL]")
    print(query)
    print("[参数]", (username, password))

    cursor.execute(query, (username, password))
    return cursor.fetchall()


def main():
    conn = setup_database()

    print("=== 正常登录测试 ===")
    normal_username = "alice"
    normal_password = "alice123"
    print("脆弱写法结果:", vulnerable_login(conn, normal_username, normal_password))
    print("安全写法结果:", safe_login(conn, normal_username, normal_password))

    print("\n=== 非法输入测试（教学用途） ===")
    test_username = "alice"
    test_password = "' OR '1'='1"

    print("脆弱写法结果:", vulnerable_login(conn, test_username, test_password))
    print("安全写法结果:", safe_login(conn, test_username, test_password))

    conn.close()


if __name__ == "__main__":
    main()
```

### 6.3 运行方式

将代码保存为 `demo.py` 后执行：

```bash
python demo.py
```

### 6.4 你应该观察什么

- 脆弱写法会把输入直接拼接进 SQL 语句。
- 安全写法会显示固定 SQL 模板，并把参数单独传入。
- 两者的关键区别是：数据库如何理解用户输入。

### 6.5 这个示例想说明的核心结论

不是“某个特殊字符串很危险”，而是：

- 只要拼接 SQL，就可能产生注入风险。
- 只要改为参数化查询，风险会大幅降低。

---

## 7. 进阶学习建议

完成基础学习后，可以继续：

1. 学习 ORM 中参数绑定的真实行为。
2. 研究动态排序、动态列名的白名单处理。
3. 学习如何在代码审计中快速识别注入点。
4. 在合法的靶场或实验环境中练习修复漏洞，而不是练习攻击现实系统。

---

## 8. 自测题

你可以用下面问题检验是否掌握：

1. SQL 注入的根本原因是什么？
2. 为什么字符串拼接会带来风险？
3. 参数化查询为什么更安全？
4. 为什么黑名单过滤不是可靠方案？
5. 排序字段这类不能直接参数化的位置应该如何处理？
6. 除了登录框，还有哪些常见注入入口？

---

## 9. 一页结论

记住下面三句话即可抓住重点：

- SQL 注入的本质是“把用户输入当成 SQL 代码执行了”。
- 最有效的基础防御是“参数化查询”。
- 标识符位置用“白名单”，权限控制用“最小权限”。

如果你是开发者，真正应该培养的是：看到字符串拼接 SQL 时，立即提高警惕。
