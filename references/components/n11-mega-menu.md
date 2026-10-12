# N11 · 巨型菜单导航（Mega-menu Panel）

> 顶栏触发器展开**全宽多列面板**：每项图标 · 标题 · 一句描述，按列头分组，常配一枚推广卡；面板展开时页面压暗纱。Vercel「Products」、Figma「Products」、Notion「Resources」的形态。

## 名称与形状

常规顶栏 + 全宽下拉面板两层结构：触发器（`aria-expanded`）开 `position: absolute; top: 100%` 的面板，面板内 2-4 列分组链接 + 侧栏特性卡；页面其余部分盖一层暗纱。**载荷（分组与解释）才是设计题**，栏本身不是。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 列数 | 2 · 3 · 4 |
| 特性位 | 无 · 推广卡 · 代码样例 |
| 暗纱 | 压暗+模糊 · 仅压暗 · 无 |
| 开启方式 | hover+click（默认）· 仅 click |

## 何时用与勿混淆

- **何时用**：目的地多到需要分组 + 解释——6+ 产品线的平台、文档/资源枢纽。
- **勿混淆**：[N1b](n1b-saas-three-section.md)（小单列下拉，非全宽面板）；[N1](n1-wordmark-2-links.md)（无任何下拉）。

## DOM+CSS 骨架

```html
<header class="nav">
  <button class="nav__link" aria-controls="mega-p" aria-expanded="false">产品</button>
  <div class="mega-panel" id="mega-p">
    <div class="mega-panel__inner">
      <div class="mega-col"><p class="head">收款</p>
        <a class="mega-link"><b>支付</b><i>卡片、ACH、电汇</i></a></div>
      <a class="mega-feature"><p>Vault</p><p>稳定币结算</p></a>
    </div>
  </div>
</header>
```

```css
.mega-panel { position: absolute; top: 100%; left: 0; right: 0;
  opacity: 0; visibility: hidden; transform: translateY(-10px);
  backdrop-filter: blur(20px) saturate(160%);
  border-bottom: 1px solid var(--color-rule);
  transition: opacity 240ms, transform 280ms var(--ease-out); }
.mega-panel.is-open { opacity: 1; visibility: visible; transform: none; }
.mega-panel__inner { display: grid; grid-template-columns: repeat(3, 1fr) 1.1fr;
  gap: 2rem; max-width: var(--page-max); margin: 0 auto; padding: 2rem var(--page-gutter); }
```

JS 行为：hover 开（约 140ms 关闭宽限，防指针跨缝闪烁）、click 切换、Esc 关、同时只开一面板、暗纱与 `aria-expanded` 随状态走。

折叠要点：窄屏整包塌缩为抽屉，面板列堆成手风琴分组；触发器与面板项命中区 ≥44px（总则 5）。

## 反模式

- 超过 4 列或面板高过 60vh——载荷爆炸即失控；装不下说明信息架构要先修。hover 开但无关闭宽限——指针跨缝面板闪烁。
- 条目裸链无一句描述——「图标网格」只是化了妆的 [N1b](n1b-saas-three-section.md)。写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N11 · Mega-menu Panel）。
