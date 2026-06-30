# design-md 子命令 —— 创建、应用、验证、导出 DESIGN.md

> 本文件是 `design-md` 子命令的完整流程,由顶层 [`SKILL.md`](../SKILL.md) 路由进入。
> 产出物 = **DESIGN.md** 设计系统文件(Google Labs agent-first 格式):YAML 前置 token(机器可读)+ Markdown 正文(人类可读设计理由)。
> 想从 DESIGN.md 进一步产出页面级硬 token UI markdown,见下游子命令 [`ui-md.md`](./ui-md.md)。

[google/design.md](https://github.com/google-labs-code/design.md) 让 AI 编码代理对设计系统有持久、结构化的理解。一份 DESIGN.md 文件 = **YAML 前置 token**(颜色/字体/间距/组件,机器可读)+ **Markdown 正文**(设计理由与边界用法,人类可读)。

**CLI**: `npx @google/design.md`(Windows 用 `npx designmd`)。全局安装:`npm install -g @google/design.md`

---

## Workflow Overview

| User Intent                           | Phase                                              |
| ------------------------------------- | -------------------------------------------------- |
| "Create a DESIGN.md for my project"   | → **Phase 1A/1B**: Generate from code or interview |
| "Extract tokens from my CSS/Tailwind" | → **Phase 1A**: Analyze code                       |
| Provides a screenshot/mockup          | → **Phase 1C**: Extract from image                 |
| "Build UI using our design system"    | → **Phase 2**: Apply tokens                        |
| "Lint / validate my DESIGN.md"        | → **Phase 3**: CLI lint                            |
| "Export tokens to Tailwind/CSS"       | → **Phase 3**: CLI export                          |
| Starting any frontend project         | → Scaffold DESIGN.md **first**                     |

**输入冲突优先级**:若用户同时提供代码和截图,以代码(更精确)为主、截图为辅助校验;若同时表达"新建"和"已有 DESIGN.md",先执行 Edge Cases 中的「合并 vs 覆写」流程。

**⚑ 标记的检查点规则(贯穿全文)**:遇到 ⚑ 标记时必须真正暂停,等待用户文字回复后才能继续;不能假设默认同意直接往下走。

---

## Phase 1: Generate a DESIGN.md

**写 prose 前先读 [`philosophy.md`](./philosophy.md)**:DESIGN.md 的设计质量由 prose 意图的清晰度决定(三原则:prose 优先于 tokens、具体参考胜过形容词列表、负约束定义风格),而非值的精度。下面三个子流程产出的 prose 都应遵循它。

### 1A. From Existing Code

When the user provides CSS, Tailwind config, or component source:

1. **Extract token candidates**: scan for color values in any CSS format — hex (`#RGB`/`#RGBA`/`#RRGGBB`/`#RRGGBBAA`), named, `rgb()`/`rgba()`/`hsl()`/`hsla()`/`hwb()`, `oklch()`/`oklab()`/`lab()`/`lch()`, `color-mix()` — plus `font-family`/`font-size`/`font-weight`, spacing values (`px`, `rem`), border-radius values
2. **Assign semantic roles**: group colors by function (primary action, body text, surface, border, error); name typography levels by usage (headline, body, label, caption)
3. **Infer scale**: 统计所有 spacing 数值,若 ≥70% 是 8 的倍数 → base=8px;否则 base=4px。归一化时四舍五入到最近的 base 倍数
4. **Write prose rationale**: for each token group, write 2-4 sentences explaining the design intent, not just the values

**⚑ 提取确认检查点**:在填写模板之前,先展示 token 提取结果供用户核对:

```
🎨 提取到的 tokens:
  Colors:  primary=#..., secondary=#..., neutral=#...
  Fonts:   [family] [sizes]
  Spacing: base=8px → xs/sm/md/lg/xl
  Radius:  sm=4px, md=8px

这些归类准确吗?有没有遗漏的关键颜色或需要调整的角色划分?
```

用户确认后,填写 DESIGN.md 模板并写完所有 markdown 章节。

### 1B. From Description — Interview Mode

逐一提问(不要一次全抛给用户),每问等待回答后再问下一个:

1. **品牌性格** — 用 3-5 个形容词描述你的产品感觉?(如"专业/极简/温暖/科技感")
2. **色彩方向** — 有现有品牌色吗?偏暖/冷/中性?有禁用色吗?
3. **字体风格** — 衬线体(传统/高端)还是无衬线(现代/简洁)?标题与正文是否用不同字体?
4. **信息密度** — 内容密集的数据 dashboard,还是宽松的消费者应用?
5. **参考品牌** — 有视觉风格接近的产品或网站可以参考吗?

**⚑ 生成前确认检查点**:收集完所有回答后,先汇总设计方向让用户确认,再生成文件:

```
📋 设计方向确认:
  品牌性格:[summary]
  色调方向:[warm/cool/neutral + 主色参考]
  字体策略:[font approach]
  密度定位:[dashboard / consumer]
  参考风格:[reference brands]

方向确认无误?确认后生成完整 DESIGN.md。
```

### 1C. From Screenshot or Image

1. Extract dominant colors → assign to `primary`, `secondary`, `tertiary`, `neutral` roles
2. Identify type hierarchy (size ratios, weight contrast between heading and body)
3. Measure spacing patterns (card padding, vertical rhythm, section gaps)
4. Note corner radius character (sharp ≈ 0-2px, subtle ≈ 4-8px, rounded ≈ 12-16px+)
5. Document visible component patterns (button styles, card structure, input fields)

---

## DESIGN.md Template

```
---
version: alpha
name: <Product Name>
description: <one-line brand summary>
colors:
  primary: "#..."
  secondary: "#..."
  tertiary: "#..."        # accent / CTA
  neutral: "#..."         # backgrounds, surfaces
typography:
  headline-lg:
    fontFamily: ...
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-md:
    fontFamily: ...
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: ...
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-sm:
    fontFamily: ...
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.08em
rounded:
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  # 更多组件模式(hover/active/disabled、chip、input 等)见 examples/heritage.md
---

## Overview

<Brand personality, target audience, emotional tone. 2-4 sentences.>

## Colors

<Role of each palette. What each color is for, where it should and shouldn't appear.>

## Typography

<Font strategy. Role of each typeface. Hierarchy rationale.>

## Layout

<Grid model (fixed-width or fluid), spacing philosophy, containment patterns.>

## Elevation & Depth

<How hierarchy is conveyed: shadows, tonal layers, borders, or flat contrast.>

## Shapes

<Corner radius philosophy. Sharp = engineered, round = approachable.>

## Components

<Key component patterns and interaction states not captured by tokens alone.>

## Do's and Don'ts

- Do ...
- Don't ...
```

---

## Phase 2: Apply DESIGN.md

When building frontend code alongside an existing DESIGN.md:

### Step 1 — Parse and Internalize

Read the DESIGN.md completely. Extract all token values into a lookup table. Then read the prose — it contains usage guardrails that tokens alone cannot express (e.g., "use tertiary for at most one CTA per screen", "labels are always uppercase").

**⚑ 应用前确认检查点**:如果是首次在项目中应用 DESIGN.md,展示解析结果让用户确认范围:

```
📋 将应用以下 token 到代码中:
  --color-primary: #...     --color-secondary: #...
  --font-body-md: 16px      --spacing-md: 16px
  核心组件约束:[Do's and Don'ts 摘要]

准备生成代码。有需要排除或额外关注的部分吗?
```

### Step 2 — 选择实现策略

根据项目栈选择 token 注入方式:

| 栈          | 推荐方式                       | 命令                                                                         |
| ----------- | ------------------------------ | ---------------------------------------------------------------------------- |
| Tailwind v4 | CLI 导出 CSS `@theme` 块       | `npx @google/design.md export --format css-tailwind DESIGN.md > theme.css`   |
| Tailwind v3 | CLI 导出 JSON config           | `npx @google/design.md export --format json-tailwind DESIGN.md > theme.json` |
| 纯 CSS/SCSS | 手动生成 `:root { --color-* }` | 见下方 CSS 示例                                                              |
| 原生平台    | 手动转换(见 Edge Cases 节)     | —                                                                            |

**CSS custom properties** 手动写法:

```css
:root {
  --color-primary: #1a1c1e;
  --color-secondary: #6c7278;
  --color-tertiary: #b8422e;
  --color-neutral: #f7f5f2;
  --font-size-headline-lg: 48px;
  --font-weight-headline: 600;
  --spacing-md: 16px;
  --radius-md: 8px;
}
```

### Step 3 — Resolve Token References

In the `components` section, `{path.to.token}` references point into the YAML tree. Always resolve these before generating code:

```yaml
button-primary:
  backgroundColor: "{colors.primary}" # → #1A1C1E
  typography: "{typography.label-sm}" # → { fontFamily, fontSize, fontWeight, ... }
  rounded: "{rounded.md}" # → 8px
```

对于嵌套引用(复合 Typography 对象),逐字段展开:`font-family: var(--font-label); font-size: var(--font-size-label-sm); font-weight: var(--font-weight-label-sm);`(完整字段列表见 [`spec-schema.md`](./spec-schema.md) Typography Tokens 节)

### Step 4 — Enforce Prose Guardrails

Actively check generated code against the **Do's and Don'ts** section. Common examples:

- Single accent color per screen
- Consistent corner radius within a view (don't mix sharp and rounded)
- WCAG AA contrast ratios (4.5:1 for body text)
- Typography weight limit per screen

**生成代码时的自查规则**:每写完一个组件,对照 DESIGN.md 的 Do's and Don'ts 列表检查一遍。发现违规时,在代码注释中注明"// ⚠️ 需确认:此处 border-radius 与设计规范 sm=4px 是否一致"。

---

## Phase 3: Validate & Maintain

### Lint a DESIGN.md

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md lint --format json DESIGN.md   # machine-readable output
```

Nine rules, each at a fixed severity (`error` / `warning` / `info`). **The canonical rule names and severities live in [`spec-schema.md`](./spec-schema.md) → Linter Rules** (mirrored from `packages/cli/src/linter/linter/rules/*.ts`) — consult that table when interpreting findings; do not rely on rule names from memory.

**`contrast-ratio` is checked automatically**: the linter computes the WCAG contrast ratio for every component's `backgroundColor` / `textColor` pair and emits a `warning` (ratio in the message) for any pair below WCAG AA (4.5:1). No manual contrast checking needed — read the finding.

**JSON output contract** (`--format json`):

```json
{
  "findings": [
    {
      "severity": "warning",
      "path": "components.button.borderColor",
      "message": "..."
    }
  ],
  "summary": { "errors": 0, "warnings": 1, "info": 0 }
}
```

Exit code 1 when any `error` finding is present; `warning` / `info` are advisory. Fix all `error` first, then triage `warning` by intent.

### Diff Two Versions

```bash
npx @google/design.md diff DESIGN.old.md DESIGN.new.md
```

Reports token-level changes. Exit 1 if regressions found.

### Export Token Formats

```bash
# W3C DTCG (.json) — 用于 Figma / Style Dictionary 等 token pipeline
npx @google/design.md export --format dtcg DESIGN.md > tokens.json
```

Tailwind v3/v4 导出命令见 **Phase 2 Step 2** 的栈选择决策表。

### Inject Spec into Agent Context

```bash
npx @google/design.md spec              # full spec text
npx @google/design.md spec --rules      # rules only
npx @google/design.md spec --rules-only --format json
```

Primary purpose: **inject the spec (or just the rule table) into an agent's prompt** when generating or reviewing a DESIGN.md without prior context, so the agent follows the canonical sections and rules instead of guessing. This is not merely "print the spec" — it is the bridge that gives the agent the same rule table the linter enforces.

---

## Edge Cases & Fallbacks

### CLI 不可用(无 npm / node 环境)

`npx @google/design.md` 无法运行时手动处理:Tailwind v4 → 手写 `@theme{--color-primary:#...}`;Tailwind v3 → 手写 `theme.extend.colors/fontSize` 对象;Lint → 对照 [`spec-schema.md`](./spec-schema.md) 逐项人工检查。告知用户:"CLI 不可用,已手动处理,可能未覆盖全部 9 条 lint 规则。"

### 输入 CSS/Tailwind 不完整或不一致

提取代码时遇到以下情况:

| 情形                                   | 处理方式                                                                           |
| -------------------------------------- | ---------------------------------------------------------------------------------- |
| 颜色 ≥8 个,无明显主次                  | 按使用频率排序,取最高频的前4个作为 primary/secondary/tertiary/neutral;在注释里注明 |
| 字体缺少 `font-weight` 或 `lineHeight` | 使用规范默认值:body 400/1.6,heading 600/1.1,label 500/1                            |
| spacing 无规律(如 13px, 27px)          | 提示用户"检测到非标准间距,建议对齐到 8px 网格",四舍五入后生成,原值写入注释         |
| 存在同名 token 多次定义(冲突)          | 取最后一条,在 DESIGN.md 注释中注明冲突来源文件和行号                               |
| 输入代码不含任何 font/color            | 降级为 Phase 1B 访谈模式,告知用户无法从代码提取                                    |

### 项目已有 DESIGN.md —— 合并 vs 覆写

用户请求生成新的 DESIGN.md 时,若项目根目录已有旧版本:

1. 先展示旧版 token 摘要(name、颜色、字体系列)
2. 明确询问:**"是覆盖旧版本 / 合并新旧 token / 另存为新文件?"**
3. 合并模式:旧 token 保留,新 token 追加;有冲突的 key 以新值为准,旧值写入行注释

### Lint 返回错误

`npx @google/design.md lint` 报错时:列出全部 error 级问题(不静默忽略);可自动修复的直接修(`colour:`→`colors:`、补 `#`、`fontWeight:"700"`→`fontWeight:700`);需判断的(orphaned token、unknown property)先问用户意图;修复后重跑 lint 确认 exit 0。

### 图片质量不足(Phase 1C)

当截图/图片分辨率低、色彩失真、或关键区域被遮挡时:

- 可识别的部分照常提取(颜色、明显的字重差异)
- 无法确认的 token 用 `"#PLACEHOLDER"` 标记,并在文件注释中说明原因
- 告知用户:"以下 token 因图片质量限制无法精确提取,请手动确认:[列表]"
- 建议:提供更高清截图,或切换到 Phase 1B 访谈模式补充缺失信息

### 输入信息不足以覆盖全部章节

若源数据(代码/截图/访谈)没有提供 Elevation、Shapes 等某些章节所需信息:仍按规范完整生成该章节,用合理默认值替代(如默认 flat/tonal elevation),并在 prose 中注明"此处为推断默认值,建议人工确认"——不可省略章节。

### 同一对话中需求范围变更

用户在生成过程中改变范围(如先要"整站规范",中途改成"只要按钮组件"):

- 不要静默缩小或放大范围继续生成
- 明确确认:"范围从 [原范围] 调整为 [新范围],对吗?" 确认后才重新规划步骤

### 目标环境不是 Web(React Native / Flutter / SwiftUI)

DESIGN.md 的 CSS 导出格式不直接适用于原生平台:

- 仍按标准格式生成 DESIGN.md(作为设计规范的 single source of truth)
- 在 Phase 2 Step 2 中,将 CSS 变量手动转为平台对应格式:
  - React Native: `StyleSheet.create({ colors: { primary: '#...' } })`
  - Flutter: `ThemeData(colorScheme: ColorScheme(primary: Color(0xFF...)))`
  - SwiftUI: `Color("primary")` + Assets.xcassets 颜色集
- 明确告知用户 CLI export 命令不适用于此场景

---

## Output Quality Checklist

交付前核对:YAML 无语法错误 · colors 均以 `#` 开头 · typography 至少含 fontFamily/fontSize/fontWeight/lineHeight · spacing 遵循统一 base scale · components 用 `{path.to.token}` 引用而非重复字面值 · prose 解释"为什么"而非只列数值 · Do's and Don'ts ≥4条且具体可执行 · 章节顺序为 Overview→Colors→Typography→Layout→Elevation→Shapes→Components→Do's and Don'ts · CLI 可用时跑一遍 lint 修完所有 error

---

## Reference Files

- [`spec-schema.md`](./spec-schema.md) — 完整 token 类型定义(字段类型、Dimension vs number、`fontFeature`/`fontVariation`)+ 权威 Linter Rules 表(9 条规则名 + severity)
- [`philosophy.md`](./philosophy.md) — DESIGN.md 写作三原则(prose 优先 / 具体参考 / 负约束),Phase 1 写 prose 前必读
- [`../examples/heritage.md`](../examples/heritage.md) — 生产级 DESIGN.md 范例,含完整 component 变体(hover/active/disabled/chip/input)

> 已在 Phase 1/2/3 内联引用,此处为索引。
