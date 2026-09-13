---
name: neo-brutalism
title: 新粗野主义
source: 社区范式（neobrutalism.dev 组件库；Gumroad、Figma 等品牌推动流行）
era: 2016 起源 / 2022~2024 主流化
category: design-language
status: style        # production | style | experimental
variance: 7-10          # dials VARIANCE 适配区间
motion: 3-7          # dials MOTION 适配区间
density: 3-6          # dials DENSITY 适配区间
platforms: Web（官网/活动页）
verified: 2026-09-07
---
# 新粗野主义（Neo-Brutalism）

## 一句话定位
对精致 SaaS 风的反叛：粗黑描边、零模糊硬投影、高饱和色块、超粗大字，故意"糙"出态度——识别度优先于优雅。

## 视觉特征（token 级参数）
- **颜色**：高饱和平涂——#FF6B6B（红）/ #FFD93D（黄）/ #6BCB77（绿）/ #4D96FF（蓝），底色 #FFFDF5 或 #F5F0E8；文字与描边一律纯黑 #000000
- **描边**：2~3px solid #000 作用于所有元素（按钮、输入框、卡片、头像）
- **阴影**：零模糊硬投影——小件 `4px 4px 0 #000`、大卡 `8px 8px 0 #000`；禁止 blur>0、禁止灰色/彩色阴影
- **圆角**：两极 0 或 8px；禁用 12px+ 柔圆角
- **字阶**：超粗无衬线（Archivo Black / Space Grotesk / Inter 800~900）；标题 48~96px 大写、行高 0.95~1.1、letter-spacing -0.02em；正文 16/24 纯黑不玩灰阶
- **间距**：紧凑 16~24px；分区用黑线分割而非留白
- **贴纸元素**：标签/图章 rotate(-3deg~3deg) 斜放
- **动效**：悬停 translate(4px,4px) + 阴影归零模拟"按进纸面"；时长 100~150ms，linear 或 steps

## 结构骨架
1. 顶栏：3px 黑下边线，logo + 高饱和 CTA（硬投影）
2. Hero：超大黑字标题 + 纯色 div 拼色块（不依赖图片）
3. 主体：直角卡片网格，每卡 2px 黑边 + 4px 硬投影
4. CTA 区：整块反色（黑底白字或高亮黄）
5. 页脚：黑底白字单行

## 适用场景 / 慎用场景
- 适用：独立开发者产品、创意工作室、活动页、潮牌电商、开发者工具官网
- 慎用：金融/医疗等严肃场景；高密度后台；深色模式（黑底上黑描边黑投影失效）

## AI 常见翻车点（反模式）
1. 投影加了 blur 或用灰色——必须是零模糊纯黑
2. 配色掺渐变或低饱和粉彩——粗野主义要高饱和平涂
3. 混入玻璃拟态/柔和大圆角——风格立即杂交失真
4. 标题不够粗不够大——没有 48px+ 的 800~900 字重就没有粗野味

## CSS 关键实现（≤15 行核心代码）
```css
.nb-card {
  background:#FFFDF5; border:2px solid #000; border-radius:8px;
  box-shadow: 4px 4px 0 #000; padding:24px;
  transition: transform .12s linear, box-shadow .12s linear;
}
.nb-card:hover { transform: translate(4px,4px); box-shadow: 0 0 0 #000; }
.nb-btn {
  background:#FFD93D; border:2px solid #000; border-radius:8px; color:#000;
  box-shadow: 4px 4px 0 #000; padding:12px 24px;
  font: 800 16px "Space Grotesk", sans-serif;
}
.nb-title { font: 900 clamp(48px,8vw,96px)/0.98 "Archivo Black", sans-serif;
  text-transform: uppercase; letter-spacing:-.02em; color:#000; }
```

## 来源链接
- 组件库与 token 参考：https://www.neobrutalism.dev/
- 风格词条（Web 设计语境）：https://en.wikipedia.org/wiki/Neubrutalism
- 风格综述与历史：https://99designs.com/blog/design-other/neo-brutalism-web-design/
