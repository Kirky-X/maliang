# N9 · 贴边极简导航（Edge-aligned Minimal）

> 字标贴死左缘，单枚 CTA 贴死右缘，中间是大片空——没有链接行。「缺席」就是设计：Apple 产品页、Carl Hauser、奢侈品站的导航。

## 名称与形状

`justify-content: space-between` 的两端布局：两个元素、一整条负空间。留白即宣言——品牌得配得上这份沉默。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| CTA 形 | 描边 · 实心药丸 · 文字+箭头 |
| 字标字体 | 衬线斜体（西文限定）· 无衬线 · mono |
| 上下 padding | 紧 · 标准 · 宽松 |

## 何时用与勿混淆

- **何时用**：奢侈/安静/工坊/园艺题材，品牌配得上沉默；目的地极少且主行动唯一。
- **勿混淆**：[N1 字标双链](n1-wordmark-2-links.md)（中间填了两条链接）；[N2 浮动角标](n2-floating-chip.md)（脱离文档流的角落块）。

## DOM+CSS 骨架

```html
<header class="nav-edge">
  <a class="wordmark">工作室</a>
  <a class="cta-outline">获取 →</a>
</header>
```

```css
.nav-edge { display: flex; justify-content: space-between; align-items: center;
  padding: var(--space-md) var(--page-gutter); }
.nav-edge .wordmark { font-size: var(--text-md); }
```

折叠要点：<60rem 不变（本就为呼吸空间设计）；<40rem 字标与 CTA 保持贴边、CTA padding 补足 44px 命中区（总则 5）。

## 反模式

- 为「填空间」加 4 条行内链接——空间就是本原型的内容；填上即成「多绕一步的 N1」，直接换 [N1](n1-wordmark-2-links.md) 或 [N1b](n1b-saas-three-section.md)。
- 奢侈站配 2px 粗边或重阴影——重量词汇与沉默气质互斥。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N9 · Edge-aligned Minimal）。
