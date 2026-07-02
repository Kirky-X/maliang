# 排版模式命名词汇

> 模式词汇库。文字排版的高级模式,补充 [`font.md`](../dimensions/font.md) 的"用什么值",本文管"怎么排"。来源:taste-skill。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `type-display`        | 大字号 display 字体,极致对比                    | Hero 标题、品牌站                     |
| `type-editorial`      | 衬线 body + 无衬线 UI,杂志感                     | 长文 / 博客 / 出版物                  |
| `type-technical`      | Mono + Sans 分工,工程感                          | DevTool、文档、代码                   |
| `type-numeric-display`| 数字特殊字体(tabular-nums)                      | 价格、金融数据、统计                  |
| `type-kinetic`        | 文字切割 / 重组 / 滚动驱动变形                    | 品牌叙事、IP 落地页                   |
| `type-mask-reveal`    | 文字遮罩揭示动画                                  | Hero 标题入场                          |
| `type-marquee`        | 滚动文字带                                        | 公告、新闻 ticker、品牌 slogan        |
| `type-quote`          | 大引号 + 引文 + 署名                              | 评价、推荐语、媒体引用                |
| `type-sticky`         | 标题 sticky,正文滚动                             | 长文 / 章节导航                       |
| `type-drop-cap`       | 首字母下沉                                        | 杂志风长文、editorial                 |

## 使用规则

- 单页排版模式 ≤ 2 种组合(如 `type-display` hero + `type-editorial` body)
- 数字必须用 `font-variant-numeric: tabular-nums`(对齐位数),见 [`principles.md`](../meta/principles.md) UI 技巧
- 触发 [`ai-tells.md`](../meta/ai-tells.md) "Inter 单字族" 时,改 `type-editorial` 或 `type-display`
- `type-marquee` 必须实现 `prefers-reduced-motion` 降级(静态显示完整文字)
- `type-kinetic` 仅 MOTION_INTENSITY ≥ 8 使用(见 [`dials.md`](../meta/dials.md))
- 中文行高 ≥ 1.6,英文 ≥ 1.4

## 在 draw-md 中的写法

```markdown
## Typography
- pattern: type-editorial
- display: { family: "Fraunces", weight: 700, size: 48px, tracking: -0.03em }
- body: { family: "Inter", weight: 400, size: 16px, line_height: 1.7 }
- numeric: { family: "Inter", variant_numeric: tabular-nums }
```
