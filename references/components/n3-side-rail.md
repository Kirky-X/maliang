# N3 · 侧栏轨导航（Side Rail）

> 左缘细竖条：旋转 90° 的字标 + 2-3 枚区段圆点指示。编辑/作品集的能量。

## 名称与形状

`writing-mode: vertical-rl` 的窄竖条贴左缘：字标竖排，区段指示点纵列。为长而分节的页面服务——圆点即进度。侧栏占位是它的代价：主内容必须为它让出列。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 侧 | 左 · 右 |
| 宽 | 12ch · 16ch · 20ch |
| 指示器 | 实心条 · 纯文字 · 编号 |

## 何时用与勿混淆

- **何时用**：长页、区段编号明确（与 [S1 左栏编号](s1-left-margin-numbered.md) 同族搭配）；文档/参考站默认导航。
- **勿混淆**：[N1 字标双链](n1-wordmark-2-links.md)（横向顶栏）；[N4 藏于 ⌘K](n4-hidden-behind-k.md)（完全不可见）。

## DOM+CSS 骨架

```html
<nav class="nav-rail">
  <p class="wordmark vertical">工作室</p>
  <ul class="dots"><li></li><li></li><li></li></ul>
</nav>
```

```css
.nav-rail { position: fixed; left: 0; top: 0; bottom: 0; width: 3rem;
  padding: var(--space-md); writing-mode: vertical-rl;
  display: flex; justify-content: space-between; align-items: center; }
```

折叠要点：<60rem 竖条解除粘性、升到内容上方变成汉堡触发钮；<40rem 汉堡成为唯一导航（竖排在窄屏无条件退场）。

## 反模式

- 竖条与横顶栏并存双导航——导航轴唯一；选了侧轨就撤顶栏。
- 圆点不指示真实区段（装饰点）——指示器必须可点且对应真实锚点，假指示器触发 [ai-tells.md](../meta/ai-tells.md) 伪交互条目。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N3 · Side Rail）。
