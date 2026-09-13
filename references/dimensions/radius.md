# 圆角规范

> 规范层。圆角的**语义阶梯、用法边界、一致性**。具体硬值在产物层 [`examples/ui-markdown/token.md`](../../examples/ui-markdown/token.md)。

## 语义阶梯

| token          | 值(px) | 用途                       |
| -------------- | ------ | -------------------------- |
| radius-sharp   | 0      | 直角(图片/分隔/严谨数据表) |
| radius-subtle  | 4      | 小控件(标签/chip/输入框)   |
| radius-rounded | 8~12   | 卡片/容器(主流)            |
| radius-xl      | 16~24  | 大卡片/弹窗/模态           |
| radius-full    | 9999   | 胶囊(按钮/头像/开关)       |

卡片主流 8~12px,即规范记法 `radius-md` 档(见下"记法对照")。

## 记法对照(规范记法 = radius-sm/md/lg)

全库规范记法统一为 tier 三档 `radius-sm` / `radius-md` / `radius-lg`,与 [`token.md`](../meta/token.md) 命名结构(tier: sm/md/lg/xs/xl)一致;语义阶梯的档名描述**用途**,与规范记法一一映射:

| 规范记法 | 值(px) | 对应语义档 | 典型用途 |
| -------- | ------ | ---------- | -------- |
| radius-sm | 4-6   | radius-subtle | chip/tag/输入框等小控件 |
| radius-md | 8-12  | radius-rounded | 卡片/容器(主流) |
| radius-lg | 16+   | radius-xl     | 大卡片/弹窗/模态 |

- `radius-sharp`(0)与 `radius-full`(胶囊)不占 tier 档,直通保留。
- `rounded.lg` / `rounded.md` 等 Tailwind 风格写法是**框架映射写法**,不是规范记法;token → 各框架的映射见 [`../commands/draw-md.md`](../commands/draw-md.md) 与 draw-flutter / draw-harmony / draw-element 的映射表,跨格式命名转换见 [token.md](../meta/token.md) 的命名跨格式映射节。
- 产物契约硬约束:draw-md 中卡片类组件 MUST 用 `{radius-lg}`(16px,脚本检查 12,见 draw-md.md);本文语义阶梯的 rounded(8~12)是"容器主流"的选型语义档。选型语义与产物契约各归其文件,禁止再造第三套档名。

## 用法边界

- **容器/卡片** — rounded(8~12),柔和但不失结构
- **小元素**(chip/tag/badge) — subtle(4),与尺寸匹配
- **可点击行动按钮** — rounded 或 full(胶囊),CTA 常胶囊形
- **头像/状态点** — full(圆)
- **图片/媒体** — sharp(0)或与容器一致,不强制圆角

圆角大小与元素尺寸**正相关**:小元素小圆角,大元素大圆角。

## 一致性

同一层级/同一组件族的圆角 MUST 一致。同一视图混用 4/8/12/16 会显凌乱。例外:圆形元素(头像)不受矩形圆角体系约束。

## 双倍圆角技巧

较大形状用**两倍大**的圆角半径(与双倍间距配套),视觉更平衡(见 [spacing.md](./spacing.md))。图标内边距小处用 subtle,大容器用 rounded/xl。

## 超椭圆(squircle)(可选进阶)

圆角矩形在高阶表达可用**超椭圆**(介于圆与矩形之间,既有圆形柔和又有矩形稳定),更和谐——仅用于品牌强表达场景,不作为默认。
