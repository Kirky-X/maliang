# N13 · 行内 ⌘K 搜索药丸导航（Inline ⌘K Search Pill）

> 栏内一枚**可见**搜索药丸：占位文案 + `⌘K` 键帽提示，与链接并存（不取代它们）。点击或按 ⌘K / Ctrl K 开聚光灯弹层：分组、可键盘导航的结果。[N4](n4-hidden-behind-k.md) 的可见反面——新手看得见入口，快捷键留给熟手。Tailwind / Linear / Raycast / 文档站的形态。

## 名称与形状

顶栏三段中插一枚 40px 高的药丸钮（图标 + 「搜索文档…」+ ⌘/K 键帽），点击开固定定位弹层：输入行 + 分组结果 + 底部键位提示行。可见 affordance 与快捷键双通道同指一个面板。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 药丸位置 | 居中 · 字标右侧 |
| 结果分组 | 平铺 · 分组（默认） |
| 底部键位提示 | 显示 · 隐藏 |
| 开启通道 | 药丸+⌘K（默认）· 仅 ⌘K（→ 那是 N4 不是 N13） |

## 何时用与勿混淆

- **何时用**：搜索是主要动作的产品——开发工具、音乐/资料库应用、大体量内容站、文档。
- **勿混淆**：[N4 藏于 ⌘K](n4-hidden-behind-k.md)（无可见导航）；一只点了只聚焦输入框的普通搜索图标（无聚光灯面板）。

## DOM+CSS 骨架

```html
<button class="searchpill" aria-label="搜索（⌘K）">
  <span class="ico"></span><span class="text">搜索文档…</span>
  <span class="kbd"><kbd>⌘</kbd><kbd>K</kbd></span>
</button>
<div class="cmdk" aria-hidden="true">
  <div class="cmdk__backdrop" data-close></div>
  <div class="cmdk__panel" role="dialog" aria-modal="true">
    <input id="cmdk-input" placeholder="搜索文档…"><kbd>esc</kbd>
    <div class="cmdk__foot"><span><kbd>↑</kbd><kbd>↓</kbd> 移动</span>
      <span><kbd>↵</kbd> 打开</span><span><kbd>esc</kbd> 关闭</span></div>
  </div>
</div>
```

```css
.searchpill { display: flex; align-items: center; gap: 0.6rem; height: 40px;
  padding: 0 0.55rem 0 0.85rem; background: var(--color-paper-2);
  border: 1px solid var(--color-rule); border-radius: 999px; }
.cmdk { position: fixed; inset: 0; z-index: 700; opacity: 0; visibility: hidden;
  transition: opacity 200ms, visibility 200ms; }
.cmdk.is-open { opacity: 1; visibility: visible; }
.cmdk__panel { position: absolute; top: 14vh; left: 50%; width: min(560px, calc(100vw - 2rem)); }
```

JS 行为：⌘K / Ctrl K 切换、Esc 关、点背景关、↑/↓ 移动活动项、Enter 选中、打开即聚焦输入框并锁 body 滚动。折叠要点：窄屏药丸塌缩为搜索图标（≥44px 命中区），弹层变全高 sheet。

## 反模式

- 用 `<div>` 假弹层——不圈焦点、不理 Esc。**发了药丸就发了整套键盘模型**，两者不可拆卖。药丸长得像普通按钮（无图标无占位）也不行——它必须「看起来像搜索」。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N13 · Inline ⌘K Search Pill）。
