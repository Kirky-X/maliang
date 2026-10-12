# T1 · 边注拉引言（Pull-quote with Marginalia）

> 引言占宽栏，署名与来源链接浮在窄边栏。页面上已有边注节奏时的证言讲法。

## 名称与形状

两栏证明区：宽栏放引言本体，窄边栏放署名、职务、来源链接——Tufte 式边注结构。引言是主角，署名是它的旁注，层次靠栏宽差建立。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 引言处理 | 斜体 display · 正体大号 · 衬线斜体（西文限定） |
| 署名形制 | 签名式 · 印章式 · 时间戳式 |
| 边注内容 | 无 · 时间线 · 单条脚注 |

## 何时用与勿混淆

- **何时用**：页面已经有边注/旁注的排印节奏（编辑型长文里插一段证言）。
- **勿混淆**：[T3 独占巨引](t3-single-huge-quote.md)（居中占据整节）；[H3 引言主导](h3-quote-led.md)（住在 hero 槽位）。

## DOM+CSS 骨架

```html
<aside class="proof-margin">
  <blockquote>"…"</blockquote>
  <p class="attribution muted">— 姓名<br />职务，公司</p>
</aside>
```

```css
.proof-margin { display: grid; grid-template-columns: 1fr 12rem;
  gap: var(--space-xl); }
.proof-margin blockquote { font-size: var(--text-lg); line-height: 1.5; }
```

折叠要点：<60rem 边注移到引言下方、分隔退化为发丝线；<40rem 边注合并为一行（姓名 · 公司 · 年份）。

## 反模式

- 没有边注节奏的页面强插边栏——栏宽差没有体系支撑就是「歪了一列」；无体系用 [T3](t3-single-huge-quote.md)。
- 引言逐字照抄营销话术——真证言是用户语言，营销腔署名念不出人味；证言真实性归 [data-floor.md](../meta/data-floor.md) 管。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id T1 · Pull-quote with Marginalia）。
