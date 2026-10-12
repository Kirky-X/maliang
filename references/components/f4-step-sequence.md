# F4 · 步骤序列（Step Sequence）

> 编号阶段（`1.0 → 2.0 → 3.0`）纵向流动，每阶段一标题一段正文，有时配小视觉。产品是一条工作流而非一个瞬间时的讲法。

## 名称与形状

有序列表结构：每步 = 编号 + 标题 + 段落（+ 可选小图），纵向堆叠并以连接线/箭头暗示推进。编号制式是气质开关：`1.0/2.0` 工程感、`01/02` 编辑感、`一/二/三` 中文正统。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 编号制式 | `一/二/三` · `01/02/03` · `1.0/2.0/3.0` |
| 布局 | 纵向堆叠 · 横向流动 · 斜向 |
| 连接物 | 线 · 箭头 · 无 |

## 何时用与勿混淆

- **何时用**：产品是一次流程/方法论/工序；onboarding、教学、服务说明。
- **勿混淆**：[F2 粘性滚动栈](f2-sticky-scroll-stack.md)（滚动同步但不编号）；[S1 左栏编号](s1-left-margin-numbered.md)（区段头编号，非步骤叙事）。

## DOM+CSS 骨架

```html
<ol class="steps">
  <li><span class="stage">1.0</span><h3>接入。</h3><p>…</p></li>
  <li><span class="stage">2.0</span><h3>规划。</h3><p>…</p></li>
</ol>
```

```css
.steps { list-style: none; display: grid; gap: var(--space-2xl); }
.steps .stage { font-family: var(--font-mono); color: var(--color-accent); }
.steps li { display: grid; grid-template-columns: 4rem 1fr; gap: var(--space-md); }
```

折叠要点：<60rem 编号从边栏移到与步骤同行（行内化）；<40rem 步骤容器收紧、连接线撤除——编号本身已足够表达顺序。

## 反模式

- 步骤数凑整膨胀（明明三步非要五步对称）——步骤数由流程决定，不由对称感决定。
- 每步配一张等尺寸图标卡——退化为三等卡反射单元；小视觉应当不均质、按需出现。
- 跨产出照抄同组旋钮值（同制式 + 同连接物）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id F4 · Step Sequence）。
