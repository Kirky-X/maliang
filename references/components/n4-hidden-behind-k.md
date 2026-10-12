# N4 · 藏于 ⌘K 导航（Hidden Behind ⌘K）

> 无可见导航：用户经 `⌘K` 打开命令面板去任何地方。为键盘优先的受众设计。

## 名称与形状

页面上只有一枚极小的 ⌘K 提示（或干脆全靠快捷键），面板承载全部目的地。把导航整个收进一个搜索框——极简的极限形态，也是风险最大的形态。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 触发 | 按钮 · 纯键盘 · 两者 |
| 面板 | modal · sheet · spotlight |
| 最近记录 | 显示 · 隐藏 |

## 何时用与勿混淆

- **何时用**：受众是技术用户、默认预期这个交互（开发者工具、内部工具）。
- **勿混淆**：[N13 行内搜索药丸](n13-inline-cmdk-pill.md)（可见的对面形态——新手看得见入口，⌘K 是进阶级）；[N2 浮动角标](n2-floating-chip.md)（永远可见的小块）。

## DOM+CSS 骨架

```html
<button class="kbd-hint" aria-label="打开命令面板">⌘ K</button>
<dialog class="palette">
  <input type="text" placeholder="跳转到…" />
  <ul><li><a href="#pricing">定价</a></li></ul>
</dialog>
```

```css
.palette { border: 1px solid var(--color-rule); border-radius: 8px;
  padding: var(--space-md); }
.palette::backdrop { background: oklch(0% 0 0 / 0.3); }
```

折叠要点：<60rem 为不识 ⌘K 的用户出现汉堡；<40rem ⌘K 等价物是屏幕上的可点按钮（原生 `<dialog>` 保证焦点圈与 Esc 关闭）。

## 反模式

- 受众不是键盘优先用户也藏导航——隐藏式导航要求受众懂暗号，否则等于没有导航；一般受众用 [N13](n13-inline-cmdk-pill.md)。
- 面板用 `<div>` 假弹层——焦点不圈、Esc 不关；必须原生 `<dialog>` 或等效焦点管理。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N4 · Hidden Behind ⌘K）。
