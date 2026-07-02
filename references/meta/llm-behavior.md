# LLM 行为研究 —— 输出截断与缓解

> 规范层。LLM 在生成长 UI 产物时存在系统性"截断 / 偷懒"行为:省略章节、压缩代码、用 placeholder 凑数。本文识别根本原因并提供四种缓解方式。来源:taste-skill/research/laziness。

理解这些行为的目的是**在 design-md / draw-md / preview 流程中主动规避**,而非事后补救。

## 1. 截断的根本原因

LLM 输出截断并非随机失败,而是训练与推理层面的系统性偏差。四个根因:

### 1.1 RLHF(人类反馈强化学习)偏差

- RLHF 倾向奖励"简短、礼貌、点到为止"的回答,长输出在训练中被惩罚
- 模型学会"主动结束"以获取奖励,即使任务未完成
- **症状**:DESIGN.md 章节写到第 5 节开始变短,Do's and Don'ts 只写 2-3 条凑数

### 1.2 Training Data 偏差

- 训练语料中"完整规范文档"远少于"代码片段 + 简短说明"
- 模型见过的"完整 DESIGN.md"样本不足,倾向于生成它见过的多数模式(片段化)
- **症状**:token 表只列 3-4 个颜色就跳到 prose,组件区只写 button-primary 不写变体

### 1.3 Cognitive Shortcuts(认知捷径)

- LLM 在长上下文中倾向用"模式匹配"代替"逐步推理"
- 见到"颜色"就直接列 5 个色相,见到"按钮"就给 1 个 default 态,不推理 hover/pressed/disabled
- **症状**:输出看起来"对",但每个章节都是模板,缺业务特异性

### 1.4 Output Limits(硬性输出上限)

- 模型最大输出 token(如 4K / 8K / 32K)是物理约束
- 接近上限时模型会"主动收尾"——不是被截断,而是预判空间不足而压缩
- **症状**:最后一个章节明显比前面短,代码块用 `// ... rest omitted` 收尾

## 2. 四种缓解方式

### 2.1 Parameter Tuning(参数调优)

| 参数              | 调整方向                | 效果                                  |
| ----------------- | ----------------------- | ------------------------------------- |
| `temperature`     | 降到 0.3-0.5            | 减少随机性,聚焦任务                  |
| `max_tokens`      | 显式设为 8K+            | 防止模型自我审查,但物理上限不可突破  |
| `top_p`           | 0.9(略低于默认)       | 减少长尾,聚焦强概率路径              |
| `frequency_penalty` | 0.3-0.5                | 抑制重复模式(避免反复"在现代设计中")|
| `presence_penalty` | 0.2-0.4                | 鼓励覆盖更多主题(减少跳章)         |

**适用**:LLM 推理层可调时(API 直调、本地模型)。封装好的 IDE 插件通常不可调。

### 2.2 Prompt Engineering(提示工程)

#### 显式章节清单 + 最小项数

```
必须输出以下章节,每节标注 [done] 标记:
[ ] Overview(≥ 3 句)
[ ] Colors(≥ 5 个 token:primary/secondary/tertiary/neutral/surface)
[ ] Typography(≥ 4 个层级:headline-lg / headline-md / body-md / label-sm)
[ ] Layout(说明 grid + spacing + containment)
[ ] Elevation & Depth(说明阴影策略)
[ ] Shapes(说明 radius 档位)
[ ] Components(≥ 3 个组件:button-primary 含 hover/active/disabled + 1 个 input + 1 个 chip)
[ ] Do's and Don'ts(≥ 6 条,3 Do + 3 Don't)
```

#### 反捷径指令

```
禁止行为:
- 禁止用 `// ...` 或 `// 其余类似` 省略代码
- 禁止 placeholder 凑数(如 `color-primary: "#TODO"`)
- 禁止跳过组件状态(hover / pressed / focused / disabled 必须全部覆盖)
- 禁止 Do's and Don'ts 少于 6 条
- 禁止最后一个章节明显短于前面(若内容确实少,说明原因)
```

#### 显式分阶段(本技能已采用)

design-md / draw-md / preview 拆分,每个子命令产出聚焦单一职责,降低单次输出压力。这是 SKILL.md 路由器的核心设计动机之一。

### 2.3 Architectural Patterns(架构模式)

#### Chunked Generation(分块生成)

长文档分多次生成,每次产出 1-2 章节,下次带前文摘要继续。本技能 design-md 的 Phase 1A/1B/1C + Phase 2 + Phase 3 即此模式。

#### Schema-First(结构先行)

先输出 YAML frontmatter(机器可读、结构强制),再补 prose。即使 prose 被截断,token 表仍完整,draw-* 可继续。

#### Self-Check Loop(自检循环)

生成完后让模型自检:"对照章节清单,逐项检查是否完整 + 每项是否达到最小项数"。本技能在 [`design-md.md`](../commands/design-md.md) 的 Output Quality Checklist 与 [`preview.md`](../commands/preview.md) 的 Pre-Flight Check 中实现。

### 2.4 Reference Prompts(参考提示)

为常见场景提供"已验证完整的示例产物",让模型模仿而非从头推理。

- [`examples/design-system/heritage/DESIGN.md`](../../examples/design-system/heritage/DESIGN.md) — 生产级 DESIGN.md 范例,含完整 component 变体
- [`examples/ui-markdown/`](../../examples/ui-markdown/) — draw-md 产出范例
- 这些范例本身就是"反截断"的种子:模型见到完整产物后,会倾向于复制其完整度

## 3. 本技能的集成策略

| 阶段       | 缓解措施                                                                |
| ---------- | ----------------------------------------------------------------------- |
| design-md  | Schema-First(YAML 强制)+ 章节清单 CHECKPOINT + heritage 范例引用      |
| draw-md    | 分页面产出(单文件 ≤ 1 页)+ 组件参数表 schema 强制字段                |
| preview    | Pre-Flight Check 80+ 项机械检查(见 [`preview.md`](../commands/preview.md)) |
| draw-*     | 单组件单文件,避免单次输出跨多组件                                      |
| redesign   | 8 维度审计清单(见 [`redesign.md`](../commands/redesign.md))逐项扫描   |

## 4. 识别截断的信号

交付前若出现以下信号,视为截断,**不可交付**:

- 最后一个章节字数 < 前面章节均值的 50%
- 代码块以 `// ...` / `// 其余类似` / `// TODO` 结尾
- 组件区只有 default 态,无 hover/pressed/disabled
- Do's and Don'ts < 6 条
- 任何章节内容是"该章节应包含 X"而非真正的 X
- placeholder 占比 > 10%(`#TODO` / `#PLACEHOLDER` / ` TBD`)

## 与其他文档的关系

- 本文档是 meta 层,被所有 commands 子命令文档引用
- 截断检查项集成到 [`preview.md`](../commands/preview.md) Pre-Flight Check
- 重设计场景的截断识别在 [`redesign.md`](../commands/redesign.md) 第 2 步 Audit
- 不涉及具体设计规则,仅管"输出完整性"
