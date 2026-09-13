---
name: aurora-gradient
title: 极光渐变
source: Stripe 官网渐变范式 + 社区 mesh gradient 工具（实现依 CSS 官方规范）
era: 2017~至今（2023~2025 SaaS 官网复兴）
category: design-language
status: style        # production | style | experimental
variance: 4-8          # dials VARIANCE 适配区间
motion: 3-7          # dials MOTION 适配区间
density: 1-4          # dials DENSITY 适配区间
platforms: Web hero 区
verified: 2026-09-07
---
# 极光渐变（Aurora / Mesh Gradient）

## 一句话定位
多个模糊彩色光斑在背景上缓慢流动，模拟极光/晨雾的氛围渐变——Stripe 范式以来 SaaS 官网 hero 区最主流的背景语言。

## 视觉特征（token 级参数）
- **颜色组合（示例 4 色）**：#7C3AED（紫）/ #06B6D4（青）/ #EC4899（粉）/ #22D3EE（蓝绿）；高级感替代组 #6366F1 + #A78BFA + #F0ABFC；底色深 #0B0B14 或浅 #F8FAFC
- **光斑**：每斑 300~600px、单屏 3~5 个、覆盖 30~50% 画面
- **模糊**：光斑 `blur(60~100px)`（必须 ≥60px 才无边界）；或用 `radial-gradient(color, transparent 70%)` 免 blur
- **透明度**：光斑 0.5~0.8；文字区加 scrim `linear-gradient(rgba(0,0,0,.4), transparent)` 保对比
- **噪点**：叠加 SVG feTurbulence 颗粒 opacity 0.03~0.06 消 banding（色带）
- **前景元素**：不参与渐变（一屏只有一个渐变源）；卡片可用 rgba(255,255,255,.08) 玻璃或实色
- **字阶**：深底白字 display 56~80px 600；浅底深字 #0F172A
- **动效**：光斑位移循环 15~25s alternate、linear 或 ease-in-out；可选 hue-rotate ±15°；仅光斑层加 `will-change: transform`

## 结构骨架
1. 底层：纯色底（深或浅）
2. 斑层：3~5 个 radial-gradient 光斑 + blur + 缓慢 keyframes 位移
3. 噪点层：SVG 噪点铺满消色带
4. 内容层：居中 hero 大字 + CTA，对比度靠 scrim
5. 可选前景：细描边玻璃卡，不再叠渐变

## 适用场景 / 慎用场景
- 适用：SaaS/开发者产品官网 hero、发布页背景、登录页、404 页
- 慎用：长文正文页、后台界面、严格无障碍场景（文字对比必须达标）；整站连续多屏使用（视觉疲劳）

## AI 常见翻车点（反模式）
1. blur 不足露出圆形边界——必须 ≥60px 或 transparent 70% 渐变
2. 渐变色带 banding——缺噪点层
3. 默认紫+蓝像 Tailwind 模板——至少替换 1 个非常规色（青/粉/暖橙）
4. 文字直接压亮斑对比 <4.5:1

## CSS 关键实现（≤15 行核心代码）
```css
.aurora { position:relative; overflow:hidden; background:#0B0B14; }
.aurora::before { content:""; position:absolute; inset:-30%;
  background:
    radial-gradient(40% 40% at 25% 30%, #7C3AEDcc, transparent 70%),
    radial-gradient(35% 35% at 70% 25%, #06B6D4aa, transparent 70%),
    radial-gradient(45% 45% at 60% 75%, #EC489999, transparent 70%);
  filter: blur(80px);
  animation: drift 20s ease-in-out infinite alternate; }
@keyframes drift { to { transform: translate(6%,-4%) rotate(8deg); } }
.aurora::after { content:""; position:absolute; inset:0; opacity:.05;  /* 噪点 */
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'/%3E"); }
@media (prefers-reduced-motion: reduce) { .aurora::before { animation:none; } }
```

## 来源链接
- Stripe 官网（渐变范式源头）：https://stripe.com
- CSS radial-gradient 官方文档：https://developer.mozilla.org/en-US/docs/Web/CSS/gradient/radial-gradient
- Mesh 生成工具：https://meshgradient.in/ / https://csshero.org/mesher/
