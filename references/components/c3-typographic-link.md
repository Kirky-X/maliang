# C3 · 排版链接（Typographic Link）

> 一个词、一个箭头、一条 1px 下划线。没有盒子，没有填充。编辑型页面的 CTA 该闭嘴时就用它。

## 名称与形状

纯文字行动：下划线（或 hover 才出现的下划线）+ 可选箭头。重量最轻的 CTA 层级，靠措辞与箭头承担召唤力。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 下划线 | 实线 · 虚线 · 双线 · 无（hover 现线） |
| hover 行为 | 加粗 · 滑动 · 换色 |
| 箭头 | → · ↗ · 无 |

## 何时用与勿混淆

- **何时用**：编辑/长文档页面，CTA 不应大声；次级行动、延伸阅读。
- **勿混淆**：[C1 描边 chip](c1-outlined-chip.md)（有边框、重量更高）；[C4 粘性底栏](c4-sticky-bottom-bar.md)（常驻容器）。

## DOM+CSS 骨架

```html
<a class="link">读完整案例 →</a>
```

```css
.link { text-underline-offset: 0.2em; text-decoration-thickness: 1px; }
.link:hover { text-decoration-thickness: 2px; }
.link .arrow { display: inline-block;
  transition: translate var(--dur-short) var(--ease-out); }
.link:hover .arrow { translate: 0.2em 0; }
```

折叠要点：<60rem 与 <40rem 均不变——文字链接天然换行适配；命中区不足 44px 时用 padding 扩热区而非放大字号。

## 反模式

- 给文字链接套盒子加底色——那是 [C1](c1-outlined-chip.md) 的工作；两种重量混在一处 = 层级混乱。
- 一页 CTA 全是文字链接、无任何主行动——最轻的层级承担不了主召唤；主 CTA 缺位时升 [C1](c1-outlined-chip.md) 或实心。
- 跨产出照抄同组旋钮值（同下划线 + 同 hover）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id C3 · Typographic Link）。
