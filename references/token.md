# Design Token 命名规范

> 规范层。定义 token 的**命名规则与层级体系**，不含具体颜色/数值。具体硬值（RGBA + HEX）在产物层 [`examples/ui-markdown/token.md`](../examples/ui-markdown/token.md)。两层职责见 `design.md` Decision 4。

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
