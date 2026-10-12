# N8 · 终端命令导航（Terminal Command）

> 导航排成一行 CLI 提示：`> studio --catalog --voice --get▮`。「链接」即命令旗标。闪烁光标（▮）**只允许出现在这里**——它有语义（「下一个字符你来输入」），页面他处禁用。

## 名称与形状

mono 字体的一行伪终端：提示符 + 工具名 + 若干下划线旗标链接 + 块状光标。Vercel CLI 文档落地页、Charm、Mitchell Hashimoto 个人站的母语。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 提示符 | `>` · `$` · `~/$` |
| 光标 | 行尾 · 末旗标后 · 无 |
| 行宽 | 通栏 · 内容宽 · ~80ch |

## 何时用与勿混淆

- **何时用**：CLI 工具、开发工具文档，或整站 terminal 题材（[tactical-terminal.md](../templates/tactical-terminal.md) 的默认导航）。
- **勿混淆**：[N4 藏于 ⌘K](n4-hidden-behind-k.md)（命令面板，非可见栏）；[N7 粗野厚板](n7-brutal-slab.md)（重排版但非终端隐喻）。

## DOM+CSS 骨架

```html
<header class="nav-term">
  <pre class="line"><span class="prompt">&gt;</span> studio
    <a href="#catalog">--catalog</a> <a href="#voice">--voice</a>
    <a href="#get">--get</a><span class="caret" aria-hidden="true">▮</span></pre>
</header>
```

```css
.nav-term .line { font-family: var(--font-mono); font-size: var(--text-sm); }
.nav-term .prompt { color: var(--color-accent); padding-right: 0.4ch; }
.nav-term a { color: var(--color-ink); text-underline-offset: 2px; }
.caret { display: inline-block; width: 1ch; color: var(--color-accent);
  animation: blink 1.05s steps(2) infinite; }
@keyframes blink { 50% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .caret { animation: none; opacity: 1; } }
```

折叠要点：<60rem 旗标多时折到第二个 `>` 行、光标保持行尾；<40rem 收成单个标着 `> menu` 的汉堡、光标留在行尾。

## 反模式

- 非开发者站点用 `> view --gallery`——提示符词汇成了布景装饰（婚礼摄影站的终端导航 = 服装错穿）；N8 只属于真终端/CLI 品牌。
- 光标闪烁元素扩散到 hero 或标题——全站光标特权归本原型一处；`prefers-reduced-motion` 必须停闪（上述 CSS 已内建）。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N8 · Terminal Command）。
