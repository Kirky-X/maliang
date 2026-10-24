# 变更管理指南

> 本项目使用 **specmark** 规格驱动变更工作流管理所有非平凡修改。统一入口，不再维护 openspec/ 约定。

## 统一入口

| 目录 | 用途 | 状态 |
| ---- | ---- | ---- |
| `specmark/changes/` | **主变更目录** — specmark skill 的运行时产物，所有 spec-driven 变更在此创建 | 活跃 |
| `openspec/` | 前身约定，从未启用 | 弃用（仅 .gitignore 保留条目） |

**规则**：变更由 specmark skill 创建与管理，产物目录为 `specmark/changes/<change-name>/`，具体文件构成以 specmark skill 的阶段定义为准（proposal / design / tasks / specs）。

## 工作流

specmark 共八阶段：explore → clarify → propose → analyze → apply → converge → archive，status 为随时可用的状态查询。各阶段产物与审查门禁以 specmark skill 文档为准；其中 converge 阶段的通过标准是 0 CRITICAL 且无 HIGH。

## 与 .gitignore 的关系

`specmark/` 与 `openspec/` 均在 `.gitignore` 中 — 变更产物为**开发期工作文档**，不入版本库。
归档后的变更如需长期追溯，由开发者手动提取到独立文档或 wiki。

## 触发方式

- 手动：`请使用 specmark 工作流` 或 `/specmark`
- 自动：当任务涉及 proposal/design/tasks 生成时，规则 23 路由到 specmark skill
- 轻量修改（不超过 3 步且不超过 3 个文件）：不走 specmark，直接修改 + commit
