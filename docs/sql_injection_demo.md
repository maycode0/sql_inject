# SQL 注入教学演示代码

## 1. 说明

这是一份可直接复制运行的本地教学演示代码，用来帮助你理解：

- 脆弱写法为什么会有风险
- 安全写法为什么应使用参数化查询

本示例仅用于本地学习与授权环境中的安全教学，不用于任何未授权系统。

---

## 2. 演示目标

通过同一组输入，观察两类场景下的安全写法与脆弱写法区别：

1. `vulnerable_login`：直接拼接 SQL
2. `safe_login`：使用参数化查询
3. `vulnerable_list_users`：直接拼接排序字段
4. `safe_list_users`：使用白名单映射排序字段

你将看到：

- 脆弱写法会把输入混入 SQL 结构
- 安全写法会把输入作为普通数据处理
- 值位置和结构位置需要不同的防御思路

---

## 3. 可直接运行的 Python 示例

当前项目中已经提供了可直接运行的文件：`ai_coding/sql_injection_demo.py`

如果你只是学习，直接运行这个文件即可；下面同时附上完整代码，方便阅读。

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
    print("输入 username =", repr(username))
    print("输入 password =", repr(password))
    print("脆弱写法结果:", vulnerable_login(conn, username, password))
    print("安全写法结果:", safe_login(conn, username, password))


def run_sort_case(conn, title, order_by):
    print(f"\n=== {title} ===")
    print("输入 order_by =", repr(order_by))
    print("脆弱排序结果:", vulnerable_list_users(conn, order_by))
    print("安全排序结果:", safe_list_users(conn, order_by))


def main():
    conn = setup_database()

    run_case(conn, "正常登录测试", "alice", "alice123")
    run_case(conn, "异常输入测试（教学用途）", "alice", "' OR '1'='1")
    run_sort_case(conn, "正常排序测试", "username")
    run_sort_case(conn, "白名单回退测试", "username DESC, id")

    conn.close()


if __name__ == "__main__":
    main()
```

---

## 4. 运行方式

```bash
python ai_coding/sql_injection_demo.py
```

如果你的环境中 `python` 命令不可用，也可以尝试：

```bash
py ai_coding/sql_injection_demo.py
```

---

## 5. 你应重点观察的内容

### 5.1 看 SQL 语句本身

重点不是记住某种输入，而是观察：

- 脆弱写法中，输入被直接拼进 SQL 文本
- 安全写法中，SQL 模板固定不变，参数单独传入

在新增的排序示例中，再额外观察：

- 脆弱排序写法中，`order_by` 直接进入 `ORDER BY`
- 安全排序写法中，只允许白名单中的固定字段参与排序

### 5.2 看查询结果差异

你需要思考：

- 为什么同样的输入，在两种写法中的结果会不同？
- 到底是“输入危险”，还是“SQL 拼接方式危险”？

标准答案是：真正危险的是字符串拼接 SQL，而不是某个单独的字符本身。

### 5.3 看两类防御手段的分工

这个示例现在同时演示了两种常见防御思路：

- 登录查询属于“值位置”，核心防御是参数化查询
- 排序字段属于“结构位置”，核心防御是白名单映射

这两种方式不是互相替代，而是分别解决不同类型的问题。

---

## 6. 建议你自己改动后再观察

你可以把示例扩展为以下练习：

1. 把 `username` 改成其他用户值
2. 给 `password` 传入普通错误密码
3. 增加一个搜索功能函数，分别写脆弱版和安全版
4. 给排序白名单再增加一个字段，例如 `created_at`
5. 试着输入一个不在白名单中的排序值，观察回退结果

---

## 7. 这个演示要记住的结论

- SQL 注入的本质，是把输入混成了 SQL 结构的一部分。
- 参数化查询的本质，是把输入强制当作数据处理。
- 排序字段、列名、表名这类结构位置，通常更适合白名单控制。
- 看到字符串拼接 SQL，就要主动检查风险。
