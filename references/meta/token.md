# Design Token 命名规范

> 规范层。定义 token 的**命名规则与层级体系**，不含具体颜色/数值。具体硬值（RGBA + HEX）在产物层 [`examples/ui-markdown/token.md`](../../examples/ui-markdown/token.md)。两层职责隔离:规范层仅定义命名规则与层级体系(不含色值),产物层承载具体硬值(RGBA + HEX),以避免下游 draw-* 解析失败。

## 命名结构

```
[namespace]-[category]-[property]-[tier]-[state]-[mode]
```

从左到右越靠右越可选:

| 段        | 必选         | 取值                                                                                             |
| --------- | ------------ | ------------------------------------------------------------------------------------------------ |
| namespace | 否           | `default` / 主题名（省略即 default）                                                             |
| category  | **是**       | `color` / `font` / `spacing` / `radius` / `shadow` / `border` / `opacity` / `z-index` / `motion` |
| property  | **是**       | `bg` / `text` / `border` / `size` / `weight` / `x` / `y` …                                       |
| tier      | 是（数值类） | `xs`/`sm`/`md`/`lg`/`xl` 或 `100..900` 数字阶                                                    |
| state     | 否           | `hover` / `pressed` / `focused` / `disabled` / `selected`                                        |
| mode      | 否           | `dark`（`light` 省略）                                                                           |

命名仅示意角色,非颜色值:

```
color-bg-primary           # 语义:背景主色
color-text-secondary       # 语义:次级文字
color-button-primary-bg    # 组件:主按钮背景
font-size-title-lg         # 字体:大标题字号
spacing-md                 # 间距:中档
radius-sm                  # 圆角:小
```

## 四大原则

1. **结构清晰** — 主干（`category-property-tier`）稳定,修饰（`namespace`/`state`/`mode`）按需叠加,不破坏主干。
2. **中性命名** — 描述角色而非具体用途。`color-bg-primary` ✓；`color-search-button-bg` ✗（用途绑死,复用受限）。业务场景通过语义 token 映射,而非把业务名写进 token。
3. **避免冗余** — 同义不重复。`color-red-500` ✓；`color-red-500-red` ✗。数值阶用缩写 `lg/sm/md/xs`,不写 `large/small`。
4. **统一性** — 全局 kebab-case。禁止与 `camelCase` / `snake_case` 混用。

## Token 类别

| category | 管什么                | 命名示例（角色,非值）                |
| -------- | --------------------- | ------------------------------------ |
| color    | 颜色                  | `color-bg-primary`                   |
| font     | 字体族/字号/字重/行高 | `font-size-body`、`font-weight-bold` |
| spacing  | 间距                  | `spacing-md`                         |
| radius   | 圆角                  | `radius-sm`                          |
| shadow   | 阴影                  | `shadow-card`                        |
| border   | 边框/分割线           | `border-color-default`               |
| opacity  | 透明度                | `opacity-disabled`                   |
| z-index  | 层级                  | `z-index-modal`                      |
| motion   | 动效时长/缓动         | `motion-duration-fast`               |

## 三层层级（W3C DTCG）

- **Primitive（基础值）** — `color-red-500`,纯原始值,不直接用于组件。
- **Semantic（语义）** — `color-bg-primary` → 映射某个 Primitive,表达"背景主色"意图。
- **Component（组件）** — `color-button-primary-bg` → 映射 Semantic,绑定具体组件角色。

引用方向单向收窄:**组件层只引用语义层,语义层只引用基础层;禁止跨层直连**(component → primitive)。

## 暗色模式

`light` 省略,`dark` 加 `-dark` 后缀。明暗切换通过**语义 token 的主题映射**实现,而非复制整套 primitive。

## 平台适配

同一 token 在不同平台仅命名风格转换,语义不变:

| 平台        | 风格               |
| ----------- | ------------------ |
| CSS / JS    | kebab-case（原样） |
| iOS Swift   | camelCase          |
| Android XML | snake_case         |

## 版本管理

- 新增 token → 小版本
- 改语义/改值 → 升小版本并标注迁移路径
- 移除 token → 标 `deprecated`,保留一个发布周期后再删

## 导出格式

> 本节定义 token 在不同目标平台的**格式规范**。CLI 命令(`npx @google/design.md export`)见 [`design-md.md`](../commands/design-md.md) Phase 3。本文只管"导出后的格式长什么样 + 命名如何转换"。

### 1. W3C DTCG(Design Tokens Community Group)

JSON 标准,用于 Figma / Style Dictionary / Token Studio 等 token pipeline 工具。三层结构完整保留。

```json
{
  "color": {
    "red": {
      "500": { "$type": "color", "$value": "#ef4444" }
    },
    "bg": {
      "primary": { "$type": "color", "$value": "{color.red.500}" }
    }
  },
  "font": {
    "size": {
      "body": { "$type": "dimension", "$value": "16px" }
    }
  }
}
```

**规则**:
- 每个节点用 `$type` + `$value`(DTCG v1.0 规范)
- 引用用 `{path.to.token}` 字符串,不用 `$ref`
- 文件名 `tokens.json`,编码 UTF-8

### 2. Tailwind v3(JSON config)

```json
{
  "theme": {
    "extend": {
      "colors": {
        "primary": "#ef4444",
        "bg-primary": "var(--color-bg-primary)",
        "text-secondary": "var(--color-text-secondary)"
      },
      "fontSize": {
        "body": ["16px", { "lineHeight": "1.6" }],
        "title-lg": ["32px", { "lineHeight": "1.2", "fontWeight": "600" }]
      },
      "spacing": {
        "md": "16px",
        "lg": "32px"
      },
      "borderRadius": {
        "sm": "4px",
        "md": "8px"
      }
    }
  }
}
```

**规则**:
- 命名转 kebab-case(`color-bg-primary` → `bg-primary`,前缀 `color-` 移除后 `bg-` / `text-` 作 Tailwind utility)
- 复合 typography(fontSize + lineHeight + fontWeight)用 Tailwind v3 的 tuple 写法
- 优先引用 CSS 变量(`var(--...)`),便于运行时切换主题

### 3. Tailwind v4(CSS `@theme` 块)

```css
@import "tailwindcss";

@theme {
  --color-primary: #ef4444;
  --color-bg-primary: #ffffff;
  --color-text-secondary: #6c7278;

  --font-size-body: 16px;
  --font-size-title-lg: 32px;

  --spacing-md: 16px;
  --spacing-lg: 32px;

  --radius-sm: 4px;
  --radius-md: 8px;
}
```

**规则**:
- Tailwind v4 用 CSS `@theme` 块声明,直接映射到 CSS 变量
- 命名直接用 CSS 变量规则(kebab-case + `--` 前缀),与 [`token.md`](./token.md) 命名结构一致
- v4 不需要 JSON config,所有 token 都是 CSS 变量
- 暗色模式用 `@media (prefers-color-scheme: dark) { @theme { --color-bg-primary: #1a1c1e; } }`

### 4. CSS 变量(`:root`)

```css
:root {
  /* Primitive */
  --color-red-500: #ef4444;

  /* Semantic */
  --color-bg-primary: #ffffff;
  --color-text-primary: #1a1c1e;
  --color-text-secondary: #6c7278;

  /* Component */
  --color-button-primary-bg: var(--color-bg-primary);
  --color-button-primary-text: var(--color-text-primary);

  /* Typography */
  --font-size-body: 16px;
  --font-weight-body: 400;
  --line-height-body: 1.6;

  /* Spacing / Radius / Shadow / Z-Index */
  --spacing-md: 16px;
  --radius-md: 8px;
  --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.1);
  --z-index-modal: 400;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: #1a1c1e;
    --color-text-primary: #f7f5f2;
    /* 其他暗色覆盖 */
  }
}
```

**规则**:
- 三层结构(Primitive / Semantic / Component)都在 `:root` 中,通过 `var()` 引用链表达
- 暗色模式用 `@media (prefers-color-scheme: dark)` 覆盖语义层,Primitive 不动
- 复合 typography(fontFamily + fontSize + fontWeight + lineHeight)拆为多个 CSS 变量,CSS 中用 shorthand 重组

### 5. 命名跨格式映射

| 来源(token.md)    | DTCG                  | Tailwind v3       | Tailwind v4 / CSS    |
| ------------------- | --------------------- | ----------------- | -------------------- |
| `color-bg-primary`  | `color.bg.primary`    | `bg-primary`      | `--color-bg-primary` |
| `color-red-500`     | `color.red.500`       | `red-500`         | `--color-red-500`    |
| `font-size-body`    | `font.size.body`      | `body`(in fontSize) | `--font-size-body`  |
| `spacing-md`        | `spacing.md`          | `md`(in spacing)  | `--spacing-md`       |
| `radius-sm`         | `radius.sm`           | `sm`(in borderRadius) | `--radius-sm`     |
| `z-index-modal`     | `z-index.modal`       | `modal`(in zIndex) | `--z-index-modal`   |

### 6. 导出强制项

- 同一份 DESIGN.md **必须**能导出全部 4 种格式,缺一种需说明原因
- 命名转换**必须**保持语义一致(不因格式改语义,只改命名风格)
- 复合对象(typography)**必须**在所有格式中可还原(fontFamily + size + weight + lineHeight 不可丢)
- 暗色模式 token **必须**在 CSS / Tailwind v4 中通过 `@media` 覆盖,不可在 DTCG JSON 中重复定义
