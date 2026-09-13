---
name: glassmorphism
title: 玻璃拟态（经典磨砂）
source: Michał Malewicz 规范文（hype4.academy）；Apple macOS Big Sur / visionOS 系统示范
era: 2020~2023 主流期
category: design-language
status: style        # production | style | experimental
variance: 4-7          # dials VARIANCE 适配区间
motion: 2-5          # dials MOTION 适配区间
density: 2-5          # dials DENSITY 适配区间
platforms: 移动 / Web 消费类
verified: 2026-09-07
---
# 玻璃拟态（Glassmorphism）

## 一句话定位
半透明磨砂浮卡：白色半透明底 + 毛玻璃模糊 + 细亮描边，悬浮于高饱和彩色背景之上，靠背景透色表达层级。

## 与液态玻璃的区别（必读）
- glassmorphism 是**静态磨砂贴片**：白色 tint、常用在内容卡片、模糊即全部效果
- Apple Liquid Glass 是**光学材质**：近中性无色、折射透镜 + 镜面高光、只用于控件/导航层、随系统无障碍设置退化
- 一句话：玻璃拟态 = "透色的白色磨砂卡"；液态玻璃 = "会流动的透镜"

## 视觉特征（token 级参数）
- **底色**：`rgba(255,255,255,0.10~0.25)`（浅）/ `rgba(255,255,255,0.06~0.10)`（深）；彩色 tint 版用品牌色 10~15% 透明
- **模糊**：`backdrop-filter: blur(12~24px) saturate(120~160%)`——大卡 24px、chip 12~16px；低于 8px 背景文字会穿透干扰
- **描边**：1px `rgba(255,255,255,0.2~0.4)`；进阶用渐变描边（上 0.6 → 下 0.1）模拟受光
- **阴影**：大而软 `0 8px 32px rgba(0,0,0,0.10~0.20)`
- **圆角**：16~24px
- **背景（前提条件）**：必须垫 2~3 个高饱和 blob（如 #7C3AED / #EC4899 / #0EA5E9，直径 300~600px、blur 80px），否则玻璃不可见
- **字阶**：白字为主——标题 24~32px 600、正文 15~16px rgba(255,255,255,.75)
- **对比度硬指标**：正文对背景 ≥4.5:1（WCAG AA），不足则加深 tint 或加暗 scrim

## 结构骨架
1. 底层：全屏渐变/彩斑背景
2. 浮层 1：玻璃导航条（pill 形）
3. 浮层 2：中央玻璃主卡（登录卡/信息卡）
4. 卡内元素全部实色（按钮/文字），禁止卡中卡再磨砂
5. 全屏玻璃浮层 ≤2 层，避免叠影

## 适用场景 / 慎用场景
- 适用：音乐/天气/壁纸类消费 App、登录卡、hero 悬浮卡、macOS/visionOS 风 Web 概念页
- 慎用：正文阅读、数据表格；低端设备（backdrop-filter 性能贵）；背景不可控的 UGC 页

## AI 常见翻车点（反模式）
1. 白底白字对比不足 4.5:1——必须加深 tint 或加 scrim
2. 灰白页面上直接上玻璃（没有彩色 blob 就没有玻璃感）
3. 玻璃卡里嵌玻璃卡，磨砂叠磨砂
4. blur 太小（<8px）背景文字穿透

## CSS 关键实现（≤15 行核心代码）
```css
.frost {
  background: rgba(255,255,255,.15);
  backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(255,255,255,.3); border-radius: 20px;
  color:#FFF; padding:32px; box-shadow: 0 8px 32px rgba(0,0,0,.12);
}
.frost-bg { position: relative; }
.frost-bg::before { content:""; position:absolute; inset:-20%; z-index:-1;
  background: radial-gradient(400px 400px at 30% 20%, #7C3AED, transparent 70%),
              radial-gradient(500px 500px at 75% 70%, #EC4899, transparent 70%);
  filter: blur(80px); }
```

## 来源链接
- 风格规范原文（Malewicz）：https://hype4.academy/articles/design/glassmorphism-in-user-interfaces
- 对照 Apple 官方 Liquid Glass（区分用）：https://developer.apple.com/documentation/technologyoverviews/liquid-glass
- HIG Materials（系统材质示范）：https://developer.apple.com/design/human-interface-guidelines/materials
