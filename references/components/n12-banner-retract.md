# N12 · 公告条 + 收回导航（Announcement Banner + Retracting Nav）

> 彩色促销**公告条**叠在一条真导航上方：下滚时公告条滑出收回、导航齐顶；上滚时滑回；× 永久关掉（高度归零、不留缝）。Apple 式双条，但上层是**公告条不是第二条导航**——靠色彩对比与「一条内容」守住这一点。

## 名称与形状

`position: fixed` 头部含两层：`--banner-h` 高的公告条 + `--bar-h` 高的导航栏。下滚过约 48px → `.is-compact`（`translateY(calc(var(--banner-h) * -1))` 收起公告条）；上滚 → 滑回；贴顶 → 恒显。关闭 = 把 `--banner-h` 置 0（整体位移的 `calc()` 随之自愈，无残留缝）。正文 padding-top 按 `banner + bar` 合高预留。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 公告条填充 | 实色 · 渐变 · 淡底+墨字 |
| 可关闭 | 有 × · 无 |
| 导航滚动态 | 粘性 · 也磨砂 |
| 公告内容 | 促销 · 状态 · 倒计时 |

## 何时用与勿混淆

- **何时用**：确有**限时**公告（发布、促销、免邮）值得常驻一条，页面是产品/营销页。数据主导与电商页好搭档。
- **勿混淆**：永不移动的静态公告条（可用，但那不是本原型）；[N1b](n1b-saas-three-section.md)（单栏无公告条）。

## DOM+CSS 骨架

```html
<header class="nav" id="nav">
  <div class="nav__banner">
    <p>新品 — <b>共享习惯</b>。<a class="banner-link">试试 →</a></p>
    <button class="nav__banner-x" aria-label="关闭公告"><span></span></button>
  </div>
  <div class="nav__bar"><div class="nav__bar-inner">
    <a class="nav__brand">Tally</a>
    <nav class="nav__links">…</nav>
    <a class="btn">开始</a>
  </div></div>
</header>
```

```css
:root { --banner-h: 42px; --bar-h: 64px; }
.nav { position: fixed; inset: 0 0 auto; z-index: 500;
  transition: transform 320ms var(--ease-out); }
.nav.is-compact { transform: translateY(calc(var(--banner-h) * -1)); }
.nav__banner { height: var(--banner-h); display: flex; align-items: center;
  justify-content: center; background: var(--color-accent); color: var(--color-paper); }
.demo-hero { padding-top: calc(var(--banner-h) + var(--bar-h) + 4rem); }
```

折叠要点：窄屏公告文案截断/去首部图形，导航链接塌缩为主 CTA + 汉堡；公告条与 CTA 命中区 ≥44px（总则 5）。

## 反模式

- 上层塞第二组导航链接——正是本原型要消灭的「双导航」味；公告条 = 一句话 + 一条链接 + 一个 ×。
- 直接动画公告条高度（抖动）——位移整体 `.nav`，高度只在关闭时置零。
- 公告过期不撤——限时件的「限时」是承诺。写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N12 · Announcement Banner + Retracting Nav）。
