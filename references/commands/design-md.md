# design-md 子命令 —— 创建、应用、验证、导出 DESIGN.md

> 本文件是 `design-md` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 产出物 = **DESIGN.md** 设计系统文件(Google Labs agent-first 格式):YAML 前置 token(机器可读)+ Markdown 正文(人类可读设计理由)。
> 想从 DESIGN.md 进一步产出页面级硬 token UI markdown,见下游子命令 [`draw-md.md`](./draw-md.md)。

[google/design.md](https://github.com/google-labs-code/design.md) 让 AI 编码代理对设计系统有持久、结构化的理解。一份 DESIGN.md 文件 = **YAML 前置 token**(颜色/字体/间距/组件,机器可读)+ **Markdown 正文**(设计理由与边界用法,人类可读)。

**CLI**: `npx @google/design.md`(Windows 用 `npx designmd`)。全局安装:`npm install -g @google/design.md`

---

## Workflow Overview

| User Intent                           | Phase                                              |
| ------------------------------------- | -------------------------------------------------- |
| 任意 design-md 触发                   | → **Phase 0**: Brief Inference(推理设计方向)     |
| "Create a DESIGN.md for my project"   | → **Phase 1A/1B**: Generate from code or interview |
| "Extract tokens from my CSS/Tailwind" | → **Phase 1A**: Analyze code                       |
| Provides a screenshot/mockup          | → **Phase 1C**: Extract from image                 |
| "Build UI using our design system"    | → **Phase 2**: Apply tokens                        |
| "Lint / validate my DESIGN.md"        | → **Phase 3**: CLI lint(9 项规则)               |
| "Export tokens to Tailwind/CSS"       | → **Phase 3**: CLI export                          |
| "Generate theme variations"           | → **Phase 4**: Variation Engine                    |
| Starting any frontend project         | → Scaffold DESIGN.md **first**                     |

**输入冲突优先级**:若用户同时提供代码和截图,以代码(更精确)为主、截图为辅助校验;若同时表达"新建"和"已有 DESIGN.md",先执行 Edge Cases 中的「合并 vs 覆写」流程。

**🔴 CHECKPOINT 规则(贯穿全文)**:遇到 🔴 CHECKPOINT 标记时必须真正暂停,等待用户文字回复后才能继续;不能假设默认同意直接往下走。

---

## Phase 0: Brief Inference(推理设计方向)

> 进入 design-md 流程的**第一件事**。从用户的简短 brief(产品描述 / 截图 / 关键词)推理出设计方向,作为 Phase 1 写 prose 的输入。来源:taste-skill + ui-ux-pro-max-skill。完整推理规则见 [`meta/product-reasoning.md`](../meta/product-reasoning.md)。

### 步骤

1. **提取 brief 关键词**:从用户输入识别产品类型 / 用户群 / 业务目标 / 平台 / 情绪关键词
2. **匹配产品类型**:对照 [`product-reasoning.md`](../meta/product-reasoning.md) 第 2 节 12 个示例,命中则采用其推理结果;未命中查询 [`color-palettes.md`](../dimensions/color-palettes.md) 192 套桶
3. **推理 7 维输出**:
   - `Recommended_Pattern`(布局模式,见 [`vocabulary/layout.md`](../vocabulary/layout.md))
   - `Style_Priority`(设计风格优先级)
   - `Color_Mood`(色彩情绪 → 查 color-palettes.md)
   - `Typography_Mood`(字体情绪)
   - `Key_Effects`(关键效果,≤ 3 个)
   - `Decision_Rules`(决策规则)
   - `Anti_Patterns`(反模式,与 [`ai-tells.md`](../meta/ai-tells.md) 联动)
4. **推断 Dials**:DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY 三档(见 [`dials.md`](../meta/dials.md))
5. **选 1-2 个参考设计系统**:从 [`design-systems.md`](../dimensions/design-systems.md) 11 个系统中选最接近的

**🔴 CHECKPOINT · Brief 推理确认**:展示推理结果让用户确认:

```
📋 设计方向推理:
  产品类型:[matched type or "未命中,需手动确认"]
  推荐布局:[pattern names]
  风格优先级:[high > medium > low]
  色彩情绪:[mood] → 查 palettes:[桶名]
  字体策略:[display + ui]
  关键效果:[≤3 items]
  Anti-Patterns:[禁止模式]
  Dials: VARIANCE=x / MOTION=x / DENSITY=x
  参考系统:[1-2 个 design system names]

方向确认无误?确认后进入 Phase 1 生成 DESIGN.md。
```

### Brief 不充分时

若用户 brief 缺关键词(如只说"做个 App"),不要硬推理:

- 进入 Phase 1B 访谈模式补全信息
- 提示用户:"brief 信息不足以推理设计方向,需补充以下问题"
- 不接受默认推理结果,必须人工确认

### 与 Phase 1 的衔接

Phase 0 的推理结果写入 DESIGN.md frontmatter 的 `product:` 块(见 [`product-reasoning.md`](../meta/product-reasoning.md) 第 3 节),Phase 1 写 prose 时引用这些推理结果作为"为什么"的依据。

---

## Phase 1: Generate a DESIGN.md

**写 prose 前先读 [`philosophy.md`](../meta/philosophy.md)**:DESIGN.md 的设计质量由 prose 意图的清晰度决定(三原则:prose 优先于 tokens、具体参考胜过形容词列表、负约束定义风格),而非值的精度。下面三个子流程产出的 prose 都应遵循它。

### 1A. From Existing Code

When the user provides CSS, Tailwind config, or component source:

1. **Extract token candidates**: scan for color values in any CSS format — hex (`#RGB`/`#RGBA`/`#RRGGBB`/`#RRGGBBAA`), named, `rgb()`/`rgba()`/`hsl()`/`hsla()`/`hwb()`, `oklch()`/`oklab()`/`lab()`/`lch()`, `color-mix()` — plus `font-family`/`font-size`/`font-weight`, spacing values (`px`, `rem`), border-radius values
2. **Assign semantic roles**: group colors by function (primary action, body text, surface, border, error); name typography levels by usage (headline, body, label, caption)
3. **Infer scale**: 统计所有 spacing 数值,若 ≥70% 是 8 的倍数 → base=8px;否则 base=4px。归一化时四舍五入到最近的 base 倍数
4. **Write prose rationale**: for each token group, write 2-4 sentences explaining the design intent, not just the values

**🔴 CHECKPOINT · 提取确认**:在填写模板之前,先展示 token 提取结果供用户核对:

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

**🔴 CHECKPOINT · 生成前确认**:收集完所有回答后,先汇总设计方向让用户确认,再生成文件:

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
  # 更多组件模式(hover/active/disabled、chip、input 等)见 examples/design-system/heritage/DESIGN.md
---

## Overview

<Brand personality, target audience, emotional tone. 2-4 sentences.>

## Colors

<Role of each palette. What each color is for, where it should and shouldn't appear.>

## Typography

<Font strategy. Role of each typeface. Hierarchy rationale.>

## Layout

<Grid model (fixed-width or fluid), spacing philosophy, containment patterns.>

布局类型选用参考 [`layout.md`](../dimensions/layout.md)。

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

**🔴 CHECKPOINT · 应用前确认**:如果是首次在项目中应用 DESIGN.md,展示解析结果让用户确认范围:

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

对于嵌套引用(复合 Typography 对象),逐字段展开:`font-family: var(--font-label); font-size: var(--font-size-label-sm); font-weight: var(--font-weight-label-sm);`(完整字段列表见 [`spec-schema.md`](../meta/spec-schema.md) Typography Tokens 节)

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

Nine rules, each at a fixed severity (`error` / `warning` / `info`). **The canonical rule names and severities live in [`spec-schema.md`](../meta/spec-schema.md) → Linter Rules** (mirrored from `packages/cli/src/linter/linter/rules/*.ts`) — consult that table when interpreting findings; do not rely on rule names from memory.

#### 9 项 Lint 规则速查

> 完整字段定义与触发条件见 [`spec-schema.md`](../meta/spec-schema.md) → Linter Rules。本表仅作快速识别,不替代规范。

| # | 规则名(典型)              | Severity | 触发场景                                          | 修复方向                                |
| - | --------------------------- | -------- | ------------------------------------------------- | --------------------------------------- |
| 1 | `missing-required-field`    | error    | YAML 缺 name/version/colors/typography/spacing    | 补全必需字段                            |
| 2 | `invalid-color-format`      | error    | 颜色非 `#` 开头 / 非 valid hex / rgb              | 规范化为 `#RRGGBB` 或 `rgba()`          |
| 3 | `invalid-numeric`           | error    | 数字字段含单位错误(如 `fontWeight: "700"` 字符串)| 改为裸数字 `700`                        |
| 4 | `orphaned-token`            | warning  | token 定义了但未被任何组件引用                    | 评估是否删除,或在组件中引用             |
| 5 | `unknown-property`          | warning  | 组件属性不在 spec-schema 已知列表                 | 改用规范属性名,或扩展 spec-schema      |
| 6 | `contrast-ratio`            | warning  | 组件 `backgroundColor` / `textColor` 对比度 < 4.5:1 | 改深文字色或改浅背景色(见 [`color.md`](../dimensions/color.md) 第 8 节) |
| 7 | `invalid-token-reference`   | error    | `{path.to.token}` 引用指向不存在的 token          | 修正引用路径,或创建被引用 token         |
| 8 | `redundant-token`           | info     | 两个 token 名不同但值相同                         | 评估是否合并(谨慎,可能是有意为之)    |
| 9 | `deprecated-field`          | warning  | 使用了 spec 中标 deprecated 的字段                | 迁移到替代字段                          |

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

## Phase 4: Variation Engine(变体生成)

> 从一份主 DESIGN.md 派生多个主题变体(明/暗 / 季节 / A/B / 品牌)。来源:taste-skill + ui-ux-pro-max-skill。**输入**:主 DESIGN.md + 变体规格。**输出**:N 个 `DESIGN.<variant>.md` 文件 + diff 报告。

### 触发场景

| 用户意图                              | 变体类型           | 输出文件                       |
| ------------------------------------- | ------------------ | ------------------------------ |
| "做个暗色版本"                        | mode               | `DESIGN.dark.md`               |
| "做圣诞节主题"                        | seasonal           | `DESIGN.holiday-christmas.md`  |
| "A/B 测试两个 hero 配色"             | ab-test            | `DESIGN.ab-a.md` / `.ab-b.md`  |
| "为子品牌 X 派生一份"                 | brand              | `DESIGN.brand-x.md`            |
| "做高对比度无障碍版"                  | accessibility      | `DESIGN.a11y-aaa.md`           |

### 变体生成流程

1. **解析主 DESIGN.md**:提取全部 token + prose,建立基础结构
2. **应用变体规格**:对每个 token 应用变体规则(见下方规则类型)
3. **保持 prose 一致**:prose 章节不变,除非变体明确改语义(如"高对比度版"需在 Overview 加说明)
4. **生成 diff 报告**:列出相对主版本的 token 改动(增 / 删 / 改值)
5. **lint 每个变体**:每个 `DESIGN.<variant>.md` 单独跑 Phase 3 lint,确保仍合规

### 变体规则类型

#### Type 1 · Mode(明暗模式)

```yaml
# 主 DESIGN.md
colors:
  bg-primary: "#ffffff"
  text-primary: "#1a1c1e"

# DESIGN.dark.md(自动反演 + 暗色独立设计,见 color.md 第 5 节)
colors:
  bg-primary: "#1a1c1e"        # 不纯黑
  text-primary: "#f7f5f2"      # 不纯白
  # 强调色饱和度下调
```

**规则**:暗色不是简单反色,需独立设计;对比度仍需满足 WCAG AA(见 [`accessibility.md`](../meta/accessibility.md))。

#### Type 2 · Seasonal(季节主题)

```yaml
# 主 DESIGN.md
colors:
  primary: "#3b82f6"  # 蓝

# DESIGN.holiday-christmas.md
colors:
  primary: "#dc2626"  # 红
  tertiary: "#16a34a"  # 绿(辅助强调)
  # prose 加说明:本主题为圣诞限定,12 月生效
```

**规则**:季节变体只改 Primitive 层(色相),Semantic 层映射不变;功能色(success/danger)不可改色相(语义固定)。

#### Type 3 · AB Test(A/B 测试)

```yaml
# 主 DESIGN.md
colors:
  primary: "#3b82f6"

# DESIGN.ab-a.md
colors:
  primary: "#3b82f6"  # 原色
  # hero CTA 文案:"立即开始"

# DESIGN.ab-b.md
colors:
  primary: "#dc2626"  # 红色(假设 B 测试红色 CTA 转化更高)
  # hero CTA 文案:"免费试用"
```

**规则**:A/B 变体只改被测变量(单变量原则),其余 token 完全一致;diff 报告需明确标出"测试变量"。

#### Type 4 · Brand(子品牌)

```yaml
# 主 DESIGN.md(parent brand)
colors:
  primary: "#3b82f6"
  # font-family: Inter

# DESIGN.brand-x.md(sub-brand)
colors:
  primary: "#8b5cf6"  # 子品牌色(避开 ai-tells.md Lila Rule 柔紫)
  # font-family: Söhne  # 子品牌字体
  # prose 加说明:子品牌定位 / 受众差异
```

**规则**:子品牌变体可改色相 + 字体,但保留主品牌的 Layout / Component 模式;在 prose 中说明子品牌定位差异。

#### Type 5 · Accessibility(无障碍增强)

```yaml
# DESIGN.a11y-aaa.md
colors:
  text-primary: "#0a0a0a"  # 比主版本更深,达 AAA 7:1
  text-secondary: "#404040"  # 也达 AAA
  border-default: "#525252"  # 提对比
dials:
  motion_intensity: 1  # 强制最低动效
  design_variance: 2   # 减少视觉变化
```

**规则**:无障碍变体不可"减功能",只增强可达性;Motion Intensity 强制 ≤ 3;所有对比度达 AAA(7:1)。

### 变体约束(硬性)

- [ ] 每个变体 MUST 单独通过 Phase 3 lint,不可豁免
- [ ] 变体 MUST 显式声明 `variant_of: DESIGN.md`(在 frontmatter)
- [ ] diff 报告 MUST 列出全部 token 改动(增 / 删 / 改值)
- [ ] prose 章节 MUST 保持一致,除非变体类型明确改语义
- [ ] Accessibility 变体 MUST 不引入新的反模式(如降低对比度换美观)
- [ ] AB Test 变体 MUST 单变量,其余 token 完全一致

### 失败模式

| 触发条件                          | 处理                                                     |
| --------------------------------- | -------------------------------------------------------- |
| 变体改了 Semantic 命名            | 报错,变体只改 Primitive 值,不改 Semantic 命名          |
| 变体 lint 失败                    | 修复后重生成,不可"豁免变体 lint"                       |
| 变体引入 AI Tells(如柔紫)       | 拒绝生成,提示按 [`ai-tells.md`](../meta/ai-tells.md) 修改 |
| AB 变体改了多个变量               | 拆为多组 AB,保持单变量原则                               |
| 变体 prose 与主版本冲突           | 变体 prose 必须说明差异,不可静默改                      |

---

## 约束汇总(硬性)

- [ ] DESIGN.md 的 YAML frontmatter MUST 含 name/version/updated/tokens(至少 colors/typography/spacing)
- [ ] 每个 token MUST 有语义化命名(kebab-case,如 `color-brand-primary`),禁止字面量
- [ ] prose-first 格式:YAML token + Markdown 设计理由,禁止纯 JSON / 纯 CSS 变量文件
- [ ] 设计理由 MUST 解释"为什么"(呼应 philosophy.md),不只是"是什么"
- [ ] 4 个动作(创建/应用/验证/导出)的输入输出 MUST 明确,不得跳过验证直接导出
- [ ] 引用 heritage 范例 MUST 用相对路径(`examples/design-system/heritage/DESIGN.md`),禁止绝对路径
- [ ] 导出格式 MUST 支持 Tailwind / CSS / W3C DTCG / lint 至少 3 种,缺一种需说明原因

---

## Edge Cases & Fallbacks

### CLI 不可用(无 npm / node 环境)

`npx @google/design.md` 无法运行时手动处理:Tailwind v4 → 手写 `@theme{--color-primary:#...}`;Tailwind v3 → 手写 `theme.extend.colors/fontSize` 对象;Lint → 对照 [`spec-schema.md`](../meta/spec-schema.md) 逐项人工检查。告知用户:"CLI 不可用,已手动处理,可能未覆盖全部 9 条 lint 规则。"

### 输入 CSS/Tailwind 不完整或不一致

提取代码时遇到以下情况:

| 情形                                   | 处理方式                                                                           |
| -------------------------------------- | ---------------------------------------------------------------------------------- |
| 颜色 ≥8 个,无明显主次                  | 按使用频率排序,取最高频的前4个作为 primary/secondary/tertiary/neutral;在注释里注明 |
| 字体缺少 `font-weight` 或 `lineHeight` | 使用规范默认值:body 400/1.6,heading 600/1.1,label 500/1                            |
| spacing 无规律(如 13px, 27px)          | 提示用户"检测到非标准间距,对齐到 8px 网格",四舍五入后生成,原值写入注释         |
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
- 请用户提供更高清截图,或切换 Phase 1B 访谈模式补充缺失信息

### 输入信息不足以覆盖全部章节

若源数据(代码/截图/访谈)没有提供 Elevation、Shapes 等某些章节所需信息:仍按规范完整生成该章节,用 flat elevation + tonal layer 默认值替代(如默认 flat/tonal elevation),并在 prose 中注明"此处为推断默认值,标注'需人工确认'"——不可省略章节。

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

- [`spec-schema.md`](../meta/spec-schema.md) — 完整 token 类型定义(字段类型、Dimension vs number、`fontFeature`/`fontVariation`)+ 权威 Linter Rules 表(9 条规则名 + severity)
- [`philosophy.md`](../meta/philosophy.md) — DESIGN.md 写作三原则(prose 优先 / 具体参考 / 负约束),Phase 1 写 prose 前必读
- [`../../examples/design-system/heritage/DESIGN.md`](../../examples/design-system/heritage/DESIGN.md) — 生产级 DESIGN.md 范例,含完整 component 变体(hover/active/disabled/chip/input)

> 已在 Phase 1/2/3 内联引用,此处为索引。
