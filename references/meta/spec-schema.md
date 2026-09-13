# DESIGN.md Token Schema 参考

DESIGN.md 文件 YAML front matter 的完整 schema。
已对照 `docs/spec.md`(格式规范)与 `packages/cli/src/linter/linter/rules/*.ts`(规则 `name:` + severity)核验。

---

## 顶层键

```yaml
version: alpha # string, optional. Current spec version: "alpha"
name: string # required. Product/design system name
description: string # optional. One-line brand summary
colors: map # see Colors section
typography: map # see Typography section
rounded: map # see Rounded section
spacing: map # see Spacing section
components: map # see Components section
```

---

## Schema 版本戳

DESIGN.md 头部(front matter 之前)须带 schema 版本戳注释:

```html
<!-- maliang:design-schema 1 -->
```

- 戳标识的是 **schema 结构版本**(顶层键与章节约定),不是产物 release 版本
- schema 结构变化(增删顶层键 / 字段语义调整)时递增 N;仅改 token 值不递增
- 下游工具(validate / ui-graph)读戳识别 schema 漂移,避免用旧解析约定读新文件
- 来源:impeccable(`<!-- impeccable:product-schema 1 -->`)与 ui-ux-pro-max 数据治理

---

## 决策账本(decisions)

顶层可选键。跨会话的设计决策记忆:已记录的取值是"决定而非缺陷",后续会话先读账本再动 UI,漂移即违规。该键为 maliang 扩展键,不属 Google linter 已知键,lint 保持静默(见 `unknown-key` 规则)。

```yaml
decisions:
  - decision: 深度策略用 borders-only,不用投影
    rationale: 后台工具,用户要密度;阴影显"浮"
    date: 2026-01-15
    scope: 全站
```

| 字段        | 类型   | 必选 | 说明                                       |
| ----------- | ------ | ---- | ------------------------------------------ |
| `decision`  | string | 是   | 决策内容(一句话,可被引用)               |
| `rationale` | string | 是   | 为什么(含被拒绝的替代项更佳)             |
| `date`      | string | 是   | 决策日期 `YYYY-MM-DD`                      |
| `scope`     | string | 否   | 生效范围(页面 / 组件 / 全站,默认全站)   |

- 迭代 / redesign 交付后,把本轮新出现的设计决策追加进账本,防止跨轮次漂移
- 来源:interface-design `system.md` Decisions 表(Decision | Rationale | Date)

---

## 用户研究块(users)

顶层可选键。承接 design-md Phase 0a 的"用户三产出"(画像 / 旅程 / JTBD),供 `critique` 任务脚本与 analytics 漏斗引用。该键为 maliang 扩展键,不属 Google linter 已知键,lint 保持静默(同 `decisions`)。

```yaml
users:
  personas:
    - name: 首次置业的租房客
      goal: 3 分钟内判断这套房值不值得约看
      pain: 图片与实景不符,怕白跑一趟
      ability: 移动端熟练,只在通勤时浏览
  journey:
    - task: 约看一套房
      steps:
        - step: 刷列表
          touchpoint: 筛选器
          emotion-break: 房源太多无从下手
        - step: 看详情
          touchpoint: 房源详情页
  jtbd: 当我加班到晚上九点刷到一套房时,我要 30 秒内确认它靠谱,以便明天一早就能约看。
```

| 字段              | 类型 | 必选 | 说明                                                          |
| ----------------- | ---- | ---- | ------------------------------------------------------------- |
| `users.personas`  | list | 否   | 1-3 个画像:`name` / `goal` / `pain` / `ability`,各 ≤ 5 行 |
| `users.journey`   | list | 否   | 主任务旅程:`task` + `steps[]`(step / touchpoint / emotion-break) |
| `users.jtbd`      | string | 否 | 1-2 句"当…时,我要…,以便…"                                |

- 无真实用户研究时整块省略,或写一行 `research: none` 声明"未做用户研究,按 surface-modes 模式假设"(低置信)
- **分工**:本块是**设计态研究产物**,回答"这个产品的用户是谁";[`../commands/critique.md`](../commands/critique.md) 评审 A-3 的 persona 表是**评审态固定走查人格**(急性老手等 5 类),回答"任何界面都会栽在哪"——后者可从前者的 journey 取任务素材,但两者不互相替代

---

## 颜色 token

**类型**: `map<string, Color>`

**颜色格式**: 任意合法 CSS 颜色字符串。支持的格式:

- **Hex**: `#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`
- **命名色**: `red`, `cornflowerblue`, `transparent`
- **函数式**: `rgb()`, `rgba()`, `hsl()`, `hsla()`, `hwb()`
- **广色域**: `oklch()`, `oklab()`, `lch()`, `lab()`
- **混合**: `color-mix(in srgb, ...)`

所有值在内部转换为 sRGB 以进行 WCAG 对比度检查;原始格式在显示/导出时保留。出于简洁与工具支持,推荐默认使用 Hex(`#RRGGBB`)。

```yaml
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FFFFFF"
  on-surface: "#1A1C1E"
  error: "#BA1A1A"
```

**推荐命名**(非规范性):
`primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`

Material Design 3 (MD3) 配对 token(`on-primary`、`primary-container` 等)被识别为同级,不会被标记为孤立。

**文字四级色阶**(推荐,非规范性):

| token                  | 用途       |
| ---------------------- | ---------- |
| `color-text-primary`   | 默认正文   |
| `color-text-secondary` | 辅助说明   |
| `color-text-tertiary`  | 元数据     |
| `color-text-muted`     | 禁用       |

只用两级说明层级太扁。来源:interface-design(Text hierarchy)。

---

## 字体排版 token

**类型**: `map<string, Typography>`

每个 `Typography` 对象接受:

| 字段            | 类型                | 必选     | 说明                                                                        |
| --------------- | ------------------- | -------- | --------------------------------------------------------------------------- |
| `fontFamily`    | string              | 是       | 精确字体族名(如 `Public Sans`)                                             |
| `fontSize`      | Dimension           | 是       | 如 `48px`、`3rem`、`1.5em`                                                  |
| `fontWeight`    | number              | 是       | 数值:`100`–`900`。YAML 裸数字或带引号字符串                                 |
| `lineHeight`    | Dimension or number | 是       | 无单位数字 = fontSize 的倍数(如 `1.6`)。或带单位:`24px`                   |
| `letterSpacing` | Dimension           | 否       | 如 `-0.02em`、`0.1em`                                                      |
| `fontFeature`   | string              | 否       | CSS `font-feature-settings` 值(如 `"liga" 1, "calt" 0`)                    |
| `fontVariation` | string              | 否       | CSS `font-variation-settings` 值                                            |

**Dimension 格式**: 数字后跟 `px`、`em` 或 `rem`。

```yaml
typography:
  headline-lg:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Public Sans
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  headline-sm:
    fontFamily: Public Sans
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.3
  body-lg:
    fontFamily: Public Sans
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.7
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-lg:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.06em
  label-md:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.08em
  label-sm:
    fontFamily: Space Grotesk
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
```

**推荐命名**(非规范性):
`headline-display`, `headline-lg`, `headline-md`, `headline-sm`,
`body-lg`, `body-md`, `body-sm`,
`label-lg`, `label-md`, `label-sm`,
`caption`

---

## 圆角 token

**类型**: `map<string, Dimension>`

**Dimension 格式**: 数字后跟 `px`、`em` 或 `rem`。
`9999px` 是惯用的 "pill" / 完全圆角值。

```yaml
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px
```

**推荐阶梯命名**: `none`, `sm`, `md`, `lg`, `xl`, `full`

---

## 间距 token

**类型**: `map<string, Dimension | number>`

`Dimension` 带单位后缀(`px`、`em`、`rem`)。裸 `number` 表示无单位比例或列数。

```yaml
spacing:
  base: 8px # base unit (4px or 8px grids are most common)
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
  gutter: 24px
  margin: 32px
  grid-columns: 12 # unitless column count
```

---

## 组件 token

**类型**: `map<string, map<string, string | token-reference>>`

把组件标识符映射到一组属性 token。
值可以是字面值,也可以是 `{path.to.token}` 形式、指向 YAML 树内部的引用。

### Token 引用语法

```yaml
backgroundColor: "{colors.primary}" # resolves to a Color
typography: "{typography.label-md}" # resolves to a Typography object (composite allowed)
rounded: "{rounded.md}" # resolves to a Dimension
padding: 12px # literal Dimension (no reference needed)
```

对复合值(如 `{typography.label-md}`)的引用仅允许在 `components` 章节内使用。

### 组件属性 token

| 属性             | 类型             | 说明                                |
| ---------------- | ---------------- | ----------------------------------- |
| `backgroundColor` | Color            | 背景填充                            |
| `textColor`       | Color            | 前景文字颜色                        |
| `typography`      | Typography (ref) | 完整字体规格                        |
| `rounded`         | Dimension        | 圆角半径                            |
| `padding`         | Dimension        | 内边距(简写或逐项)                |
| `size`            | Dimension        | 通用尺寸                            |
| `height`          | Dimension        | 固定高度                            |
| `width`           | Dimension        | 固定宽度                            |

未知属性(上述八项之外的任何属性)会被 `broken-ref` 规则以 warning 严重级别标记,并指出合法的子 token。边框及其他未由这八项 token 覆盖的视觉细节,应放在章节叙述中,而非组件 YAML 里。

### 变体模式

组件变体(hover、active、pressed、disabled)使用带后缀的键:

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "{colors.secondary}"
  button-primary-active:
    backgroundColor: "{colors.tertiary}"
  button-primary-disabled:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.neutral}"

  chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.full}"
    padding: 6px 12px
    typography: "{typography.label-sm}"

  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 10px 14px
    typography: "{typography.body-md}"
  input-focus:
    backgroundColor: "{colors.secondary}"
  input-error:
    textColor: "{colors.error}"
```

---

## Linter 规则(9 条)

`npx @google/design.md@0.4.0 lint` 命令运行九条规则。每条以固定严重级别触发——权威来源是 `packages/cli/src/linter/linter/rules/*.ts`(规则 `name:` + `severity`),下表为其镜像。

| #   | 规则                | 严重级别 | 检查内容                                                                                                                                                  |
| --- | ------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `broken-ref`         | error    | 无法解析到任何已定义 token 的 token 引用(`{colors.primary}`)。同时以降级的 warning 标记未知组件子 token(如 `borderColor`)。                              |
| 2   | `missing-primary`    | warning  | 定义了颜色但没有 `primary` 色——agent 会自动生成一个。                                                                                                    |
| 3   | `contrast-ratio`     | warning  | 组件 `backgroundColor`/`textColor` 配对低于 WCAG AA(4.5:1);比值包含在消息中。                                                                          |
| 4   | `orphaned-tokens`    | warning  | 定义了颜色 token 但未被任何组件引用。                                                                                                                    |
| 5   | `token-summary`      | info     | 各章节定义了多少 token 的汇总。                                                                                                                          |
| 6   | `missing-sections`   | info     | 当存在其他 token 时,可选章节(spacing、rounded)缺失。                                                                                                  |
| 7   | `missing-typography` | warning  | 定义了颜色但没有字体排版 token——agent 会使用默认字体。                                                                                                   |
| 8   | `section-order`      | warning  | 章节以非规范顺序出现。                                                                                                                                    |
| 9   | `unknown-key`        | warning  | 某个顶层 YAML 键看上去是已知键的拼写错误(如 `colours` → `colors`);自定义扩展键保持静默。                                                              |

**严重级别驱动 agent 决策**: `error` 阻断(退出码 1);`warning` 与 `info` 为建议性。

**JSON 输出契约**(`--format json`):

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

当存在任何 `error` 发现时,退出码为 1。

---

## 导出格式

| 格式标志        | 输出                                       | 用例                                     |
| --------------- | ------------------------------------------ | ---------------------------------------- |
| `json-tailwind` | Tailwind v3 `theme.extend` JSON            | `tailwind.config.js`                     |
| `css-tailwind`  | Tailwind v4 `@theme { }` CSS 块            | Tailwind v4 CSS-first 配置               |
| `dtcg`          | W3C Design Token Community Group `.json`   | Figma、Style Dictionary、Token Pipeline  |
| `tailwind`      | `json-tailwind` 的别名(向后兼容)          | —                                        |

`css-tailwind` 产出的 Tailwind v4 CSS 变量命名空间:

- `--color-*` 来自 `colors`
- `--font-*` 与 `--text-*` 来自 `typography`
- `--leading-*`、`--tracking-*`、`--font-weight-*`
- `--radius-*` 来自 `rounded`
- `--spacing-*` 来自 `spacing`
