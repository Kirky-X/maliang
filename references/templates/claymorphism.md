---
name: claymorphism
title: 黏土拟态
source: Hype4 Academy（Michał Malewicz 命名与规范文 + 官方 CSS 生成器）
era: 2022（2021 末出现，2022 规范化）
category: design-language
status: style        # production | style | experimental
variance: 5-8          # dials VARIANCE 适配区间
motion: 3-6          # dials MOTION 适配区间
density: 2-5          # dials DENSITY 适配区间
platforms: 移动 / Web 消费类
verified: 2026-09-07
---
# 黏土拟态（Claymorphism）

## 一句话定位
把 UI 元素做成软黏土：超大圆角 + "外投影 + 内暗 + 内亮"三件套阴影，挤出可捏压的柔软立体感，介于拟物与新拟物之间。

## 视觉特征（token 级参数）
- **颜色**：低饱和粉彩 + 白元素——#A0C3FF（蓝）/ #FFC8DD（粉）/ #B9FBC0（绿）/ 底 #EEF1F8；文字用深蓝灰 #39415E 而非纯黑
- **圆角**：签名级大——卡片 32~40px、按钮/输入框 16~24px、图标底座 24px
- **阴影三件套（官方生成器数值）**：外投影 `0 24px 48px rgba(145,155,177,.4)` + 内下暗 `inset -8px -8px 16px rgba(145,155,177,.4)` + 内上亮 `inset 0 11px 28px #FFFFFF`
- **描边**：无描边（黏土不画轮廓）
- **背景**：可垫 2~3 个彩色 blob（直径 300~500px，`blur(40~80px)`），本体不透明
- **字阶**：圆润字体（Nunito / Baloo 2 / Quicksand）；标题 32~48px 700、正文 16/26、按钮 16px 700
- **间距**：宽松——卡内边距 24~32px、网格 gap 24~32px
- **动效**：按压 scale(0.96~0.98) + 阴影收紧 200~300ms ease-out；悬停上浮 translateY(-4px)

## 结构骨架
1. 背景：浅灰底 + 2~3 个大 blur 彩斑
2. 主体：单列或 2~3 列卡片，统一三件套阴影 + 32px 圆角
3. 图标：彩底白图标（底座自带内阴影），直径 48~64px
4. CTA：胶囊大按钮，同款三件套阴影
5. 层级只靠阴影深浅与尺寸，不用描边/分隔线

## 适用场景 / 慎用场景
- 适用：儿童/教育产品、轻工具 landing、表单向导、收藏/趣味类产品
- 慎用：数据密集后台（阴影噪声大）；深色主题（黏土语言依赖浅底）；严肃企业品牌

## AI 常见翻车点（反模式）
1. 只做外投影丢了内阴影——没有 inset 亮/暗对就没有"黏土体"
2. 圆角停在 12~16px——黏土感需要 32px+ 大圆角
3. 用纯黑文字 + 硬描边——应换深蓝灰圆润字、无描边
4. 阴影用纯黑 rgba(0,0,0,x)——必须蓝灰 rgba(145,155,177,x) 才软

## CSS 关键实现（≤15 行核心代码）
```css
.clay {
  background:#A0C3FF; color:#39415E; border-radius:32px; padding:32px;
  box-shadow: 0 24px 48px rgba(145,155,177,.4),
              inset -8px -8px 16px rgba(145,155,177,.4),
              inset 0 11px 28px #FFFFFF;
  font: 700 16px/1.5 "Nunito", sans-serif;
  transition: transform .25s ease-out, box-shadow .25s ease-out;
}
.clay:hover  { transform: translateY(-4px); }
.clay:active { transform: scale(.97);
  box-shadow: 0 12px 24px rgba(145,155,177,.35),
              inset -6px -6px 12px rgba(145,155,177,.4),
              inset 0 8px 20px #FFFFFF; }
```

## 来源链接
- 命名与规范原文（Malewicz, 2022）：https://hype4.academy/articles/design/claymorphism-in-user-interfaces
- 官方参数生成器（三件套阴影来源）：https://hype4.academy/tools/claymorphism-generator
- CSS 实现教程（同站官方）：https://hype4.academy/articles/coding/how-to-create-claymorphism-using-css
