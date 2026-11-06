# 排版模式命名词汇

> 模式词汇库。文字排版的高级模式,补充 [`font.md`](../dimensions/font.md) 的"用什么值",本文管"怎么排"。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `type-display`        | 大字号 display 字体,极致对比                    | Hero 标题、品牌站                     |
| `type-editorial`      | 衬线 body + 无衬线 UI,杂志感                     | 长文 / 博客 / 出版物                  |
| `type-technical`      | Mono + Sans 分工,工程感                          | DevTool、文档、代码                   |
| `type-numeric-display`| 数字特殊字体(tabular-nums)                      | 价格、金融数据、统计                  |
| `type-kinetic`        | 文字切割 / 重组 / 滚动驱动变形;变体:编辑式超大标题+不对称网格下逐字母响应鼠标 | 品牌叙事、IP 落地页、互动作品集                   |
| `type-mask-reveal`    | 文字遮罩揭示动画                                  | Hero 标题入场                          |
| `type-marquee`        | 滚动文字带                                        | 公告、新闻 ticker、品牌 slogan        |
| `type-quote`          | 大引号 + 引文 + 署名                              | 评价、推荐语、媒体引用                |
| `type-sticky`         | 标题 sticky,正文滚动                             | 长文 / 章节导航                       |
| `type-drop-cap`       | 首字母下沉                                        | 杂志风长文、editorial                 |
| `type-knockout-photo` | 镂空透图:照片从大标题字形镂空处透出,上滑文字放大至照片铺满全屏,回滑收回(滚动 scrub) | 品牌叙事、专题首屏(配合 [scroll.md](scroll.md) `scroll-scrub-bind`) |
| `type-inline-image-expand` | 标题嵌图展开:标题行内嵌等高圆角小图,点击原地展开成整宽大图,上下文字两侧让位,再点缩回 | 图文标题、编辑式列表(与 [hero.md](hero.md) `hero-inline-image-type` 互见:彼条 hero 静态嵌图,本条正文嵌图可展开) |
| `type-line-stagger-swap` | 逐行换题:旧标题逐行错开下沉退场,新标题逐行升起进场,关联插画弹性回位 | 首页标题轮换、主题切换 |
| `type-expand-fulltext` | 展开全文:长文"展开全文"平滑顶开铺展,再点平滑收回,页面不猛跳 | 摘要长文、评论折叠(与 [cards.md](cards.md) `card-collapsible` 互见:彼条卡片折叠容器,本条纯文本流) |
| `type-typewriter-loop` | 打字机循环:文案逐字打出+块光标闪烁,打完停一拍→删除倒放→换下一句循环;等宽字重排版防宽度抖动,逐字间隔 40-70ms(与 [chat.md](chat.md) `chat-stream-typewriter` 互见:彼条 AI 回复一次性流式,本条营销位循环轮播) | hero 副标题轮播、终端风营销站 |
| `type-text-scramble` | 乱码解码:目标文字先以随机字符扰动,再从左到右逐位锁定为真实字符(每字符独立定时器,总时长随文本长度收敛在 0.6-1s);用等宽数字/字体防锁定时抖动;装饰档可跳过,reduced-motion 直出终稿 | 数据解密氛围、terminal 风、数字大盘标题 |

## 使用规则

- 单页排版模式 ≤ 2 种组合(如 `type-display` hero + `type-editorial` body)
- 数字必须用 `font-variant-numeric: tabular-nums`(对齐位数),见 [`principles.md`](../meta/principles.md) UI 技巧
- 触发 [`ai-tells.md`](../meta/ai-tells.md) "Inter 单字族" 时,改 `type-editorial` 或 `type-display`
- `type-marquee` 必须实现 `prefers-reduced-motion` 降级(静态显示完整文字)
- `type-marquee` 跑马灯细节:渐隐区域从文本消失处起向前扩展约 16px(透明度渐变),只计文本区域不含容器 padding;限制滚动次数(如每次激活只滚一遍)控功耗与骚扰感
- `type-kinetic` 仅 MOTION_INTENSITY ≥ 8 使用(见 [`dials.md`](../meta/dials.md))
- 文字展开/换字动效(`type-expand-fulltext` / `type-line-stagger-swap`)必须逐帧过渡高度,禁整块闪换致页面跳动
- 中文行高 ≥ 1.6,英文 ≥ 1.4

## 文字层级色

> 文字颜色按视觉重要度分层,直接映射 DESIGN.md 的 text token 层级;层级差靠色阶+字重联合表达(与 principles 第 15 定律 weight beats size 同源)。

| 层级 | 角色 | 适用场景 |
| --- | --- | --- |
| `text-primary` | 主文字色,最高对比 | 标题、正文主句、关键数值 |
| `text-secondary` | 补充说明色 | 副标题、说明文字、表单帮助文本 |
| `text-tertiary` | 弱化色 | 占位符、禁用项、时间戳/元信息 |
| `text-quaternary` | 极弱色 | 水印字、装饰性页脚、背景标签 |

- 每级与背景的实际对比仍须过 WCAG(口径见 [`../dimensions/color.md`](../dimensions/color.md));tertiary/quaternary 只承载可弃信息,禁放必读内容
- 层级数固定 4 级封顶——再多一档,相邻档差异就小到读不出层级

## 在 draw-md 中的写法

```markdown
## Typography
- pattern: type-editorial
- display: { family: "Fraunces", weight: 700, size: 48px, tracking: -0.03em }
- body: { family: "Inter", weight: 400, size: 16px, line_height: 1.7 }
- numeric: { family: "Inter", variant_numeric: tabular-nums }
```
