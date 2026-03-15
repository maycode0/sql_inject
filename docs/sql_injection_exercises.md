# SQL 注入练习题与答案解析

## 1. 使用说明

这份文档用于配合以下资料一起学习：

- `docs/sql_injection_learning.md`
- `docs/sql_injection_study_plan.md`
- `docs/sql_injection_demo.md`

建议先自己作答，再看答案解析。

---

## 2. 基础题

### 题目 1

什么是 SQL 注入？请用一句话说明其本质。

### 题目 2

下面哪种写法风险更高？为什么？

```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
```

```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

### 题目 3

SQL 注入的根本问题是下面哪一个？

1. 数据库执行速度太慢
2. 用户输入长度太长
3. 程序把用户输入当成 SQL 代码的一部分处理
4. 前端页面没有做美化

### 题目 4

为什么说“只过滤几个特殊字符”通常不是可靠的防御手段？

### 题目 5

参数化查询的核心作用是什么？

---

## 3. 理解题

### 题目 6

除了登录表单，还有哪些常见位置可能成为 SQL 注入入口？至少写出 4 个。

### 题目 7

为什么排序字段、列名、表名这类动态结构，不能简单地完全依赖普通参数化查询解决？

### 题目 8

请解释“值位置”和“结构位置”的区别。

### 题目 9

最小权限原则在 SQL 注入防御中有什么价值？

### 题目 10

为什么不应把数据库原始报错直接返回给前端用户？

---

## 4. 判断题

请判断对错，并说明原因。

### 题目 11

只要使用了 ORM，就绝对不会有 SQL 注入风险。

### 题目 12

前端做了输入校验，后端就可以不再做防御。

### 题目 13

参数化查询是防 SQL 注入最重要的基础手段之一。

### 题目 14

如果某个参数用于动态排序，推荐使用白名单映射。

### 题目 15

SQL 注入只会影响数据读取，不会影响数据修改。

---

## 5. 代码分析题

### 题目 16

阅读下面代码，指出风险点：

```python
def get_user(conn, user_id):
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()
```

需要回答：

1. 风险点在哪？
2. 应如何改写？

### 题目 17

阅读下面代码，指出问题：

```python
def search_user(conn, keyword):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username LIKE '%" + keyword + "%'"
    cursor.execute(query)
    return cursor.fetchall()
```

需要回答：

1. 为什么这段代码也有风险？
2. 更安全的思路是什么？

### 题目 18

阅读下面代码：

```python
def list_users(conn, order_by):
    cursor = conn.cursor()
    query = f"SELECT id, username FROM users ORDER BY {order_by}"
    cursor.execute(query)
    return cursor.fetchall()
```

需要回答：

1. 这和普通登录拼接风险有什么相同点？
2. 这里更推荐哪种防御方式？

---

## 6. 场景题

### 题目 19

你在审计一个项目时，发现很多地方都写着：

```python
sql = f"SELECT * FROM orders WHERE status = '{status}'"
```

你会如何分步骤整改？请写出一个简要方案。

### 题目 20

如果业务必须支持用户按 `name`、`created_at`、`id` 排序，你会如何安全设计？

---

## 7. 参考答案与解析

### 第 1 题答案

SQL 注入是指应用程序把用户输入当成 SQL 语句的一部分执行，导致查询语义被篡改。

解析：

关键不是“输入里有特殊字符”，而是“程序没有把输入当成纯数据处理”。

### 第 2 题答案

第一种风险更高，第二种更安全。

解析：

- 第一种是字符串拼接，输入直接进入 SQL 文本。
- 第二种是参数化查询，输入和 SQL 模板分离。

### 第 3 题答案

正确答案：3

解析：

SQL 注入的根本问题，是程序把输入混入了 SQL 结构中。

### 第 4 题答案

因为黑名单很难覆盖全部情况，数据库语法复杂，绕过方式也很多。

解析：

可靠的核心方法不是猜哪些字符危险，而是从机制上阻止输入参与 SQL 结构解释。

### 第 5 题答案

参数化查询的核心作用，是让数据库把输入当作数据而不是 SQL 代码处理。

### 第 6 题答案

常见入口包括：

- 搜索框
- URL 参数
- 分页参数
- 排序字段
- API 查询条件
- 报表筛选条件

### 第 7 题答案

因为排序字段、列名、表名通常属于 SQL 结构的一部分，而不是普通值。

解析：

这类位置更适合先做白名单校验，再映射成固定安全片段。

### 第 8 题答案

- 值位置：例如 `WHERE username = ?` 中的用户名参数，适合参数化。
- 结构位置：例如 `ORDER BY name` 中的字段名、排序方向、表名等，通常要靠白名单。

### 第 9 题答案

最小权限原则可以在漏洞出现时降低破坏范围。

解析：

如果数据库账号没有高危权限，即使出现问题，攻击面和影响面也会更小。

### 第 10 题答案

因为原始报错可能泄露数据库结构、表名、字段名或查询细节。

解析：

这类信息会帮助攻击者理解系统实现，增加进一步利用的风险。

### 第 11 题答案

错误。

解析：

ORM 只是降低风险，不代表绝对安全。如果开发者拼接原生 SQL，依然可能出问题。

### 第 12 题答案

错误。

解析：

前端校验可以被绕过，真正可信的防护必须在后端完成。

### 第 13 题答案

正确。

解析：

参数化查询是最重要的基础防御措施之一。

### 第 14 题答案

正确。

解析：

排序字段属于结构位置，最合适的策略通常是白名单映射。

### 第 15 题答案

错误。

解析：

SQL 注入可能影响读取、修改、删除，甚至破坏业务可用性。

### 第 16 题答案

风险点：

- `user_id` 被直接拼接进 SQL。

更安全的改法：

```python
def get_user(conn, user_id):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()
```

### 第 17 题答案

风险原因：

- 即使是 `LIKE` 查询，只要用户输入被直接拼接，依然可能带来风险。

更安全的思路：

```python
def search_user(conn, keyword):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username LIKE ?"
    cursor.execute(query, (f"%{keyword}%",))
    return cursor.fetchall()
```

### 第 18 题答案

相同点：

- 都让用户输入直接影响 SQL 结构。

更推荐的防御方式：

- 使用白名单映射。

示例：

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

### 第 19 题答案

可以按下面步骤整改：

1. 搜索所有拼接 SQL 的位置。
2. 按“值位置”和“结构位置”分类。
3. 值位置统一改成参数化查询。
4. 结构位置统一改成白名单映射。
5. 检查数据库账号权限是否过大。
6. 补充异常处理和日志记录。
7. 在测试环境中验证修复后的行为。

### 第 20 题答案

可以设计一个字段白名单：

```python
allowed_sort_fields = {
    "name": "name",
    "created_at": "created_at",
    "id": "id",
}
```

然后：

1. 先校验用户输入是否在白名单中。
2. 如果不在，则使用默认字段，如 `id`。
3. 最终只拼接白名单中预定义的固定字段。

解析：

这里的关键不在于“过滤危险字符”，而在于“只允许有限、明确、可控的结构片段进入 SQL”。

---

## 8. 建议使用方式

你可以把这份练习分三次完成：

1. 第一次只做基础题和判断题
2. 第二次做代码分析题
3. 第三次做场景题，并尝试自己写整改方案

如果你能独立答出大部分问题，说明你已经不只是记住概念，而是开始具备实际分析能力。
