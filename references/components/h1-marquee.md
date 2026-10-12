# H1 · 跑马灯宣言（Marquee）

> 一句宣言撑满首屏：无副标题、无 CTA 入镜。品牌或人物本身即是信息，字号与留白完成全部层级。

## 名称与形状

单节 hero：整屏只放一句 display 级大字（`min-height: 80dvh`），内容贴底或贴边。没有图、没有按钮组，页面由这一句话压场。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 字号档 | `xxl`（clamp 4-12rem）· `xl`（clamp 3-8rem） |
| 对齐 | 偏左 · 居中 · 偏右 |
| 底衬 | 无 · 上方单线 · 下方单线 |

## 何时用与勿混淆

- **何时用**：品牌或人物本身就是信息；宣言式品牌页、个人作品集、发布预告。
- **勿混淆**：[H4 数字主导](h4-stat-led.md)（主角是一个数字，不是一句话）；[H5 书信开场](h5-letter-hero.md)（第一人称、有称呼）。

## DOM+CSS 骨架

```html
<section class="hero-marquee">
  <h1 class="display-xxl">一句宣言。</h1>
</section>
```

```css
.hero-marquee { min-height: 80dvh; display: grid; align-content: end;
  padding: 0 var(--page-gutter) var(--space-2xl); }
.display-xxl { font-size: clamp(4rem, 12vw, 12rem); line-height: 0.92; }
```

折叠要点：<40rem 字号降一档（`xl`→`lg` 档）、收窄两侧 padding；对齐随排版自然收敛，无需单独处理。

## 反模式

- 塞副标题或 CTA 进首屏——不是本原型的工作；行动交给 [C1 描边 chip](c1-outlined-chip.md) 等在下方区段承担。hero 硬约束（栈 ≤4 层、标题 ≤12 中文字）见 [hero.md](../vocabulary/hero.md)，叠加生效。
- 大字底下再压渐变或装饰条——触发 [ai-tells.md](../meta/ai-tells.md) hero 禁令。
- 跨产出照抄上一次旋钮值（同字号档 + 同对齐 + 同底衬 = 同款）：复用本原型必须至少换一个旋钮并在盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H1 · Marquee）。
