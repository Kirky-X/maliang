# design-md 子命令 —— 创建、应用、验证、导出 DESIGN.md

> 本文件是 `design-md` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 产出物 = **DESIGN.md** 设计系统文件(Google Labs agent-first 格式):YAML 前置 token(机器可读)+ Markdown 正文(人类可读设计理由)。
> 想从 DESIGN.md 进一步产出页面级硬token UI markdown,见下游子命令 [`draw-md.md`](./draw-md.md)。

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
| "Generate theme variations"           | → **Phase 4**: Variation Engine(见 advanced)     |
| Starting any frontend project         | → Scaffold DESIGN.md **first**                     |

**输入冲突优先级**:若用户同时提供代码和截图,以代码(更精确)为主、截图为辅助校验;若同时表达"新建"和"已有 DESIGN.md",先执行 Edge Cases 中的「合并 vs 覆写」流程(见 advanced)。

**🔴 CHECKPOINT 规则(贯穿全文)**:遇到 🔴 CHECKPOINT 标记时必须真正暂停,等待用户文字回复后才能继续;不能假设默认同意直接往下走。

---

## Phase 0: Brief Inference(推理设计方向)

> 进入 design-md 流程的**第一件事**。从用户的简短 brief(产品描述 / 截图 / 关键词)推理出设计方向,作为 Phase 1 写 prose 的输入。完整推理规则见 [`meta/product-reasoning.md`](../meta/product-reasoning.md)。

### 步骤

1. **提取 brief 关键词**:从用户输入识别产品类型 / 用户群 / 业务目标 / 平台 / 情绪关键词
2. **匹配产品类型**:对照 [`product-reasoning.md`](../meta/product-reasoning.md) 第 2 节 12 个示例,命中则采用其推理结果;未命中查询 [`color-palettes.md`](../dimensions/color-palettes.md) 192 套桶
3. **推理 7 维输出**:`Recommended_Pattern`(布局,见 [`vocabulary/layout.md`](../vocabulary/layout.md))、`Style_Priority`、`Color_Mood`(→ color-palettes.md)、`Typography_Mood`、`Key_Effects`(≤3)、`Decision_Rules`、`Anti_Patterns`(与 [`ai-tells.md`](../meta/ai-tells.md) 联动)
4. **推断 Dials**:DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY 三档(见 [`dials.md`](../meta/dials.md))
5. **选 1-2 个参考设计系统**:从 [`design-systems.md`](../dimensions/design-systems.md) 11 个系统中选最接近的

**🔴 CHECKPOINT · Brief 推理确认**:展示推理结果让用户确认:

```
📋 设计方向推理:
  产品类型 / 推荐布局 / 风格优先级 / 色彩情绪→palettes
  字体策略 / 关键效果(≤3) / Anti-Patterns
  Dials: VARIANCE=x / MOTION=x / DENSITY=x
  参考系统:[1-2 个]

方向确认无误?确认后进入 Phase 1 生成 DESIGN.md。
```

### Brief 不充分时 / 与 Phase 1 衔接

若 brief 缺关键词(如只说"做个 App"),不要硬推理:进入 Phase 1B 访谈模式补全,必须人工确认。推理结果写入 DESIGN.md frontmatter 的 `product:` 块(见 [`product-reasoning.md`](../meta/product-reasoning.md) 第 3 节),Phase 1 写 prose 时引用作为"为什么"的依据。

---

## Phase 1: Generate a DESIGN.md

**写 prose 前先读 [`philosophy.md`](../meta/philosophy.md)**:设计质量由 prose 意图清晰度决定(三原则:prose 优先 / 具体参考 / 负约束),非值的精度。下面三个子流程产出的 prose 都应遵循它。

### 1A. From Existing Code

1. **Extract token candidates**: scan for color values(所有合法 CSS 颜色格式,见 [`spec-schema.md`](../meta/spec-schema.md) 颜色 token 节)、`font-family`/`font-size`/`font-weight`、spacing values (`px`, `rem`)、border-radius values
2. **Assign semantic roles**: group colors by function (primary action, body text, surface, border, error); name typography levels by usage (headline, body, label, caption)
3. **Infer scale**: 统计所有 spacing 数值,若 ≥70% 是 8 的倍数 → base=8px;否则 base=4px。归一化时四舍五入到最近的 base 倍数
4. **Write prose rationale**: for each token group, write 2-4 sentences explaining the design intent, not just the values

**🔴 CHECKPOINT · 提取确认**:在填写模板之前,先展示 token 提取结果供用户核对:

```
🎨 提取到的 tokens:
  Colors: primary/secondary/neutral
  Fonts:  [family] [sizes]
  Spacing: base=8px → xs/sm/md/lg/xl
  Radius:  sm=4px, md=8px

归类准确吗?有遗漏或需调整的角色划分?
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
  品牌性格 / 色调方向 / 字体策略 / 密度定位 / 参考风格

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
  body-md:
    fontFamily: ...
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  # 完整阶梯(headline-md/body-lg/label-sm 等)见 spec-schema.md 推荐命名
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
<Role of each palette. Where it should/shouldn't appear.>
## Typography
<Font strategy. Role of each typeface. Hierarchy.>
## Layout
<Grid model, spacing philosophy, containment. 参考 [`layout.md`](../dimensions/layout.md)>
## Elevation & Depth
<Shadows, tonal layers, borders, or flat contrast.>
## Shapes
<Corner radius philosophy. Sharp = engineered, round = approachable.>
## Components
<Key patterns and interaction states not captured by tokens.>
## Do's and Don'ts
- Do ...
- Don't ...
```

---

## Phase 2: Apply DESIGN.md

### Step 1 — Parse and Internalize

Read the DESIGN.md completely. Extract all token values into a lookup table. Then read the prose — it contains usage guardrails that tokens alone cannot express (e.g., "use tertiary for at most one CTA per screen", "labels are always uppercase").

**🔴 CHECKPOINT · 应用前确认**:如果是首次在项目中应用 DESIGN.md,展示解析结果让用户确认范围:

```
📋 将应用 token 到代码:
  --color-primary/--color-secondary/--font-body-md/--spacing-md
  核心组件约束:[Do's and Don'ts 摘要]

有需排除或额外关注的部分吗?
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
  --color-primary: #1a1c1e;  --color-secondary: #6c7278;
  --spacing-md: 16px;  --radius-md: 8px;
  /* 其余 token 按命名空间 --color-*/--font-*/--spacing-*/--radius-* 同理展开 */
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

对于嵌套引用(复合 Typography 对象),逐字段展开(`font-family`/`font-size`/`font-weight` 等),完整字段列表见 [`spec-schema.md`](../meta/spec-schema.md) Typography Tokens 节。

### Step 4 — Enforce Prose Guardrails

Actively check generated code against the **Do's and Don'ts** section. Common examples: Single accent color per screen / Consistent corner radius within a view / WCAG AA contrast ratios (4.5:1) / Typography weight limit per screen.

**生成代码时的自查规则**:每写完一个组件,对照 DESIGN.md 的 Do's and Don'ts 列表检查一遍。发现违规时,在代码注释中注明"// ⚠️ 需确认:此处 border-radius 与设计规范 sm=4px 是否一致"。

---

## Phase 3: Validate & Maintain

### Lint a DESIGN.md

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md lint --format json DESIGN.md   # machine-readable output
```

Nine rules, each at a fixed severity (`error` / `warning` / `info`). **完整 9 条规则名、severity、触发场景、JSON output contract 全部见 [`spec-schema.md`](../meta/spec-schema.md) → Linter Rules**(权威镜像,不在此重复)。`contrast-ratio` 自动检查 WCAG AA(4.5:1);exit code 1 当存在 `error` 级 finding;`warning`/`info` 为建议性。Fix all `error` first, then triage `warning` by intent.

### 其他 CLI 命令(Diff / Export / Spec Inject)

```bash
# Diff 两版本(token-level changes, regressions 时 exit 1)
npx @google/design.md diff DESIGN.old.md DESIGN.new.md
# Export W3C DTCG (.json) for Figma/Style Dictionary(Tailwind v3/v4 见 Phase 2 Step 2)
npx @google/design.md export --format dtcg DESIGN.md > tokens.json
# Inject spec/rule table into agent prompt(无 prior context 时用)
npx @google/design.md spec --rules-only --format json
```

`spec` 命令的核心用途:在 agent 无 prior context 时**把 spec/rule table 注入其 prompt**,使其遵循 canonical sections and rules 而非猜测;这不是简单的"打印 spec",是让 agent 拿到与 linter 同一份规则表的桥梁。

---

## 约束汇总(硬性)

- [ ] YAML frontmatter MUST 含 name/version/updated/tokens(colors/typography/spacing);token 命名 kebab-case,禁止字面量
- [ ] prose-first 格式:YAML token + Markdown 设计理由(解释"为什么"非"是什么"),禁止纯 JSON/CSS 变量文件
- [ ] 4 个动作(创建/应用/验证/导出)输入输出 MUST 明确,不得跳过验证直接导出
- [ ] 引用 heritage 范例 MUST 用相对路径;导出格式 MUST 支持 Tailwind/CSS/W3C DTCG/lint 至少 3 种

---

## Output Quality Checklist

交付前核对:YAML 无语法错误 · colors 均以 `#` 开头 · typography 至少含 fontFamily/fontSize/fontWeight/lineHeight · spacing 遵循统一 base scale · components 用 `{path.to.token}` 引用而非重复字面值 · prose 解释"为什么"而非只列数值 · Do's and Don'ts ≥4条且具体可执行 · 章节顺序为 Overview→Colors→Typography→Layout→Elevation→Shapes→Components→Do's and Don'ts · CLI 可用时跑一遍 lint 修完所有 error

---

## 高级特性

**Phase 4 变体引擎(明/暗 / 季节 / A/B / 品牌 / 无障碍)、Edge Cases & Fallbacks(CLI 不可用 / 输入不完整 / 合并覆写 / Lint 错误 / 图片质量不足 / 非 Web 平台等)、Design Read(一行检查点 + Visual Thesis / Content Plan / Interaction Thesis 三件事)、Working Model(最小成本验证设计方向的工作模型)全部见 [`design-md-advanced.md`](./design-md-advanced.md)。**

---

## Reference Files

- [`design-md-advanced.md`](./design-md-advanced.md) — Phase 4 变体引擎 + Edge Cases & Fallbacks
- [`spec-schema.md`](../meta/spec-schema.md) — 完整 token 类型定义 + 权威 Linter Rules 表(9 条规则名 + severity)
- [`philosophy.md`](../meta/philosophy.md) — DESIGN.md 写作三原则(prose 优先 / 具体参考 / 负约束),Phase 1 写 prose 前必读
- [`../../examples/design-system/heritage/DESIGN.md`](../../examples/design-system/heritage/DESIGN.md) — 生产级 DESIGN.md 范例,含完整 component 变体(hover/active/disabled/chip/input)
