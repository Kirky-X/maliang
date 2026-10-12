# N1 · 字标双链导航（Wordmark + 2 Links）

> 顶栏：左字标，右两条文字链（「定价」/「登录」）。无 logo 图，无菜单图标。极简变体。

## 名称与形状

最少的顶栏结构：一行 flex，字标贴左、两条链接贴右。**警告：这是最被滥用的 AI 指纹导航**——只有页面真只有 2 个目的地时才轮到它；真实产品导航默认看 [N1b SaaS 三段栏](n1b-saas-three-section.md) 或 N5/N11/N13。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 位置 | 左右分布 · 居中 · 右齐 |
| 链接形态 | 纯文字 · 文字+图标 · 药丸 |
| 粘性 | 是 · 否 |

## 何时用与勿混淆

- **何时用**：页面确实只有 2 个目的地（落地页 → 定价、登录）。
- **勿混淆**：[N1b](n1b-saas-three-section.md)（中簇多链接的密集标准栏）；[N3 侧栏轨](n3-side-rail.md)（竖向）；[N9 贴边极简](n9-edge-aligned-minimal.md)（中间是空的，无链接行）。

## DOM+CSS 骨架

```html
<nav class="nav-min">
  <a class="wordmark">工作室</a>
  <ul><li><a>定价</a></li><li><a>登录</a></li></ul>
</nav>
```

```css
.nav-min { display: flex; justify-content: space-between; align-items: center;
  padding: var(--space-md) var(--page-gutter); }
.nav-min ul { display: flex; gap: var(--space-md); list-style: none; }
```

折叠要点：<60rem 不变；<40rem 链接过长时折到第二行、字标不动；链接命中区按总则 5 补足 44px。

## 反模式

- 反射性默认 N1 而页面实际有 5 个目的地——先数目的地再选型；选型时声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N1 · Wordmark + 2 Links）。
