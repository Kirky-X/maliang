## ADDED Requirements

### Requirement: SKILL.md 作为子命令路由器

`SKILL.md` SHALL 作为路由表存在，根据用户意图路由到 `design-md` 与 `ui-md` 两个子命令。`SKILL.md` MUST NOT 包含流程主体（Phase 1/2/3、Edge Cases、Quality Checklist 等执行步骤）。每个子命令的完整流程 SHALL 位于 `references/<子命令>.md`（即 `references/design-md.md` 与 `references/ui-md.md`）。

#### Scenario: SKILL.md 不含流程主体

- **WHEN** 读取 `SKILL.md`
- **THEN** 仅见路由表与子命令入口，不含 Phase 1/2/3 执行步骤、Edge Cases 或 Quality Checklist

#### Scenario: 路由到 design-md 子命令

- **WHEN** 用户意图为生成、应用或验证 DESIGN.md
- **THEN** `SKILL.md` 路由到 `design-md` 子命令（`references/design-md.md`）

#### Scenario: 路由到 ui-md 子命令

- **WHEN** 用户意图为生成 UI 组件 markdown 规格
- **THEN** `SKILL.md` 路由到 `ui-md` 子命令（`references/ui-md.md`）

## MODIFIED Requirements

### Requirement: Lint 规则表与上游源码一致

`references/spec-schema.md` 的 Linter Rules 表 SHALL 列出全部 9 条规则，规则名 MUST 与 `temp/design.md/packages/cli/src/linter/linter/rules/*.ts` 中各规则的 `name:` 字面量逐条一致（`broken-ref`、`missing-primary`、`contrast-ratio`、`orphaned-tokens`、`token-summary`、`missing-sections`、`missing-typography`、`section-order`、`unknown-key`），且每条 MUST 标注其 severity（error/warning/info）。`references/design-md.md` 的 lint 能力描述 MUST 不再出现 `required-keys`、`color-format`、`circular-reference`、`font-weight-type` 等杜撰规则名。

#### Scenario: 规则名逐条核对

- **WHEN** 将 `spec-schema.md` 的规则表与 `rules/*.ts` 的 `name:` 字面量逐条比对
- **THEN** 9 条规则名完全一致，无杜撰、无遗漏、无拼写偏差

#### Scenario: severity 可用于 agent 决策

- **WHEN** agent 读取规则表判断是否阻断
- **THEN** 每条规则带有明确的 severity（broken-ref=error；missing-primary/contrast-ratio/orphaned-tokens/missing-typography/section-order/unknown-key=warning；token-summary/missing-sections=info）

#### Scenario: SKILL.md 描述同步

- **WHEN** 读取 `references/design-md.md` 的 lint 能力描述
- **THEN** 不含任何杜撰规则名，与规则表一致

### Requirement: Color 类型覆盖全部 CSS color

`references/spec-schema.md` 的 Color 类型说明 MUST 覆盖 spec.md 声明的全部合法格式：hex（`#RGB`/`#RGBA`/`#RRGGBB`/`#RRGGBBAA`）、named（`red`/`transparent`）、functional（`rgb()`/`rgba()`/`hsl()`/`hsla()`/`hwb()`）、wide-gamut（`oklch()`/`oklab()`/`lch()`/`lab()`）、mixing（`color-mix()`）。MUST NOT 把 Color 窄化为"必须 `#` 开头、仅 sRGB"。`references/design-md.md` 的 token 提取指令 MUST 不限于"scan for hex colors"。

#### Scenario: 广色域格式合法

- **WHEN** DESIGN.md 的 color token 使用 `oklch(62% 0.18 250)` 这类广色域值
- **THEN** skill 文档将其识别为合法 color，不报格式错误

#### Scenario: 提取阶段识别多格式

- **WHEN** 从代码提取 color token
- **THEN** skill 指令覆盖 hex、rgb()、oklch() 等多种格式，不仅扫 hex

### Requirement: Lint 输出契约文档化

`references/design-md.md` MUST 文档化 `lint` 命令的 JSON 输出结构：顶层为 `{findings, summary}`，`findings` 为数组（每项含 `severity`/`path`/`message`），`summary` 为 `{errors, warnings, info}`。MUST 说明 exit code 1 表示存在 error。

#### Scenario: agent 解析 lint 结果

- **WHEN** agent 运行 `npx @google/design.md lint --format json` 并读取输出
- **THEN** 能按 `{findings, summary}` 结构解析，区分 error/warning/info

### Requirement: WCAG 对比度自动检查

`references/design-md.md` MUST 说明 `contrast-ratio` 规则会自动计算组件 `backgroundColor`/`textColor` 对的对比度，并对低于 WCAG AA（4.5:1）的对产生 warning，比值会写入 finding message。

#### Scenario: 低对比度被检出

- **WHEN** 组件的 textColor/backgroundColor 对比度低于 4.5:1
- **THEN** skill 文档告知 agent lint 会发 warning，而非仅靠人工核对

### Requirement: spec 命令的 agent 注入用途

`references/design-md.md` MUST 说明 `spec` 命令（`spec` / `spec --rules` / `spec --rules-only --format json`）的核心用途是"把规范全文或规则表注入 agent prompt"，而非仅"输出 spec 文本"。

#### Scenario: agent 需要规范上下文

- **WHEN** agent 在无 DESIGN.md 上下文时需要按规范生成
- **THEN** skill 文档指引其用 `spec` 命令注入规范

### Requirement: 设计方法论覆盖 prose-first

skill MUST 通过 `references/philosophy.md` 落地上游 `PHILOSOPHY.md` 的三条核心方法论：(1) prose 优先于 tokens（设计质量由意图描述的清晰度决定）；(2) 具体 reference 胜过形容词列表；(3) 负约束（Do's and Don'ts 的"不做什么"）定义风格。`references/design-md.md` 的 design-md 子命令流程 MUST 引用该文件。

#### Scenario: prose 写作有方法论指引

- **WHEN** agent 在 design-md 子命令流程生成 DESIGN.md 的 prose 章节
- **THEN** 有 prose-first / 具体 reference / 负约束的方法论可循，而非仅"写 2-4 句 rationale"
