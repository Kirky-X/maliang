# F5 · 标注截图（Annotated Screenshot）

> 产品截图居中占主位，箭头或短标签指向 UI 细节。产品界面自己会说话时的讲法。

## 名称与形状

一张真实产品截图做区段主角，标注（编号钉、边栏标签或行内箭头）锚定到具体 UI 位置——每条标注一句话，解释「这里发生了什么」。截图必须真实（[visual-assets.md](../meta/visual-assets.md)），标注位置用 `--x/--y` 自定义属性定位。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 标注形制 | 编号钉 · 边栏标签 · 行内箭头 |
| 框 | 设备壳 · 素框 · 无框浮起 |
| 主从 | 图主导 · 文主导 |

## 何时用与勿混淆

- **何时用**：产品 UI 本身就是解释力来源；功能深讲、发布说明、教程。
- **勿混淆**：[F2 粘性滚动栈](f2-sticky-scroll-stack.md)（多张截图按序滚动）；[H8 模型分栏](h8-mockup-split-browser-framed.md)（hero 槽位的无标注模型）。

## DOM+CSS 骨架

```html
<figure class="annotated">
  <img src="" alt="" />
  <span class="callout" style="--x:60%; --y:30%;">→ 自动指派。</span>
</figure>
```

```css
.annotated { position: relative; }
.annotated .callout { position: absolute; left: var(--x); top: var(--y);
  font-size: var(--text-sm); white-space: nowrap; }
```

折叠要点：<60rem 截图全宽、标注退化为图下方的编号列表（序号对应位置）；<40rem 截图 16/9、标注合并为单一图例块。

## 反模式

- 标注钉漂移错位（百分比定位在响应式下对不上 UI 元素）——关键标注必须在多视口实测对位，错位读作 broken。
- 给截图里的假界面做标注——假 UI + 假标注双重违禁（[ai-tells.md](../meta/ai-tells.md) §10）。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id F5 · Annotated Screenshot）。
