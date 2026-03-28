# sql_inject

这是一个以 SQL 注入教学为核心的资料型仓库，内容包括：

- 一份可直接运行的 Python 演示脚本
- 多份中文讲义、学习手册、练习题与授课大纲
- 与 PPT / 讲义生成相关的方法说明和提示词素材

本仓库的重点是帮助学习者理解 SQL 注入的成因、防御思路与课堂演示方式，而不是提供面向未授权环境的攻击利用指南。

## 仓库内容

### 可运行代码

- `ai_coding/sql_injection_demo.py`：使用 `sqlite3` 内存数据库演示两类常见场景
  - 登录查询中的字符串拼接 vs 参数化查询
  - 排序字段中的直接拼接 vs 白名单映射

### 教学文档

- `docs/sql_injection_demo.md`：演示代码说明与观察重点
- `docs/sql_injection_handbook.md`：系统化学习手册
- `docs/sql_injection_exercises.md`：练习题
- `docs/sql_injection_teaching_outline.md`：教师授课版大纲
- `docs/sql_injection_mindmap.md`：知识结构整理
- `docs/sql_injection_study_plan.md`：学习计划

### 参考资料

- `references/prompts.md`：可复用提示词
- `references/method.md`：PPT 生成工作方法
- `references/agent-integration.md`：面向代理的集成原则

### 代理规范

- `AGENTS.md`：提供给 agentic coding agents 的仓库规则、命令约定与代码风格说明
- `.trae/skills/ppt-agent-workflow/SKILL.md`：PPT 类任务的阶段化工作规则

## 快速开始

在仓库根目录执行：

```bash
python ai_coding/sql_injection_demo.py
```

如果本机使用 Windows Python Launcher，也可以执行：

```bash
py ai_coding/sql_injection_demo.py
```

运行后可观察到：

- 脆弱写法如何把输入直接混入 SQL 结构
- 安全写法如何通过参数化查询隔离输入
- 排序等结构位置为什么更适合用白名单控制

## 推荐阅读顺序

如果你第一次接触本仓库，建议按下面顺序阅读：

1. `docs/sql_injection_demo.md`
2. `ai_coding/sql_injection_demo.py`
3. `docs/sql_injection_handbook.md`
4. `docs/sql_injection_exercises.md`
5. `docs/sql_injection_teaching_outline.md`

这样可以先看演示目标，再看代码，再进入系统化理解与教学设计。

## 构建、Lint、测试现状

当前仓库不是一个完整应用项目，而是“文档 + 单文件演示脚本”的组合，因此请注意：

- 没有正式的 build 流水线
- 没有正式的 lint 配置
- 没有正式的自动化测试套件

当前可确认的最小验证方式是：

```bash
python ai_coding/sql_injection_demo.py
```

### 关于“单个测试”

当前仓库没有 `pytest`、`unittest` 测试目录或测试配置，因此不存在标准化的“单个测试命令”。

如果只是验证某段行为，可以：

- 直接运行整个示例脚本并观察对应输出
- 在本地 Python 交互环境中手工导入函数做临时验证

但后者只是开发期手段，不属于仓库正式约定。

## 适合本仓库的修改方式

- 修改教学代码时，优先保持示例简洁、可讲解、可运行
- 修改文档时，优先使用中文，强调教学语境与安全边界
- 新增安全示例时，必须明确区分“脆弱写法”和“安全写法”
- 新增工具链时，请同步更新 `AGENTS.md` 与相关 README / 文档

## 安全与使用边界

- 本仓库内容仅用于教学、防御、审计和授权测试场景
- 不应把示例扩写成针对真实未授权系统的利用手册
- 文档中的风险示例应服务于理解漏洞成因与修复方法，而不是炫技展示 payload

## 给协作代理的说明

如果你是自动化代理或编码助手，开始工作前建议先阅读：

1. `AGENTS.md`
2. `.trae/skills/ppt-agent-workflow/SKILL.md`（当任务与 PPT、讲义或结构化内容生成有关时）

其中 `AGENTS.md` 已记录本仓库当前真实存在的命令、风格和限制，尤其说明了：

- 当前没有正式 build / lint / test 流水线
- 当前标准验证方式是运行 `ai_coding/sql_injection_demo.py`
- 不应虚构不存在的工具配置

## 后续可扩展方向

如果后续你希望把本仓库逐步工程化，可以考虑：

1. 增加 `tests/` 目录与 `pytest` 测试
2. 为演示脚本补充更细粒度的函数级验证
3. 增加最小 lint / format 配置
4. 将文档入口整理成更清晰的学习路径页

在做这些扩展时，请同步更新 `AGENTS.md`，避免仓库说明与实际状态不一致。
声明：AI率/100%
