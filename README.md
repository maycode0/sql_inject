# sql_inject

一个面向学习与教学的 SQL 注入专题资料库，内容覆盖基础概念、成因分析、常见风险、演示代码、练习题与阶段性学习路线。

## 项目简介

这个仓库的目标是用相对清晰、可循序渐进的方式帮助你理解 SQL 注入：

- 什么是 SQL 注入，为什么会发生
- SQL 注入会带来哪些实际风险
- 如何通过参数化查询、白名单和最小权限等方式进行防御
- 如何通过演示代码和练习题巩固理解

适合以下场景：

- 安全入门学习
- Web 安全教学演示
- 开发者进行防注入知识补齐
- 课程或分享前的快速复习

## 仓库结构

- `README.md`：项目入口与学习导航
- `docs/sql_injection_handbook.md`：完整学习手册，适合系统阅读
- `docs/sql_injection_learning.md`：基础知识与核心概念
- `docs/sql_injection_study_plan.md`：分阶段学习计划
- `docs/sql_injection_demo.md`：演示说明文档
- `ai_coding/sql_injection_demo.py`：可运行的 Python 示例
- `docs/sql_injection_exercises.md`：练习题与答案解析
- `docs/sql_injection_mindmap.md`：知识点速览与复习提纲
- `docs/sql_injection_teaching_outline.md`：教学使用提纲

## 推荐阅读方式

如果你是第一次接触这个主题，建议按下面顺序学习：

1. `docs/sql_injection_handbook.md`
2. `docs/sql_injection_learning.md`
3. `docs/sql_injection_demo.md`
4. `ai_coding/sql_injection_demo.py`
5. `docs/sql_injection_exercises.md`
6. `docs/sql_injection_mindmap.md`

如果你想快速上手，可以直接从这两个入口开始：

- 想系统看一遍：`docs/sql_injection_handbook.md`
- 想先看代码：`ai_coding/sql_injection_demo.py`

## 运行示例

运行演示代码：

```bash
python ai_coding/sql_injection_demo.py
```

如果本机使用的是 Windows Python Launcher：

```bash
py ai_coding/sql_injection_demo.py
```

## 资料覆盖内容

当前仓库资料主要覆盖：

- SQL 注入基础定义
- 常见成因与攻击思路
- 风险与危害说明
- 参数化查询防御
- 白名单校验思路
- 最小权限原则
- 登录查询示例
- 排序字段白名单示例
- 学习练习与答案解析

## 适合怎么使用

- `学习`：按学习路线完整阅读文档并运行示例
- `教学`：使用手册、演示文档和教学提纲组织课程内容
- `复习`：直接查看脑图文档和练习题

## 免责声明

本仓库内容仅用于合法的安全学习、教学与防御研究，不应用于任何未授权测试或攻击行为。
