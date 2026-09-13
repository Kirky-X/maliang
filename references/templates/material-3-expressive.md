---
name: material-3-expressive
title: M3 富表现力
source: Google Material Design 官网（m3.material.io 官方博客与动效规范）
era: 2025 / Android 16、Wear OS（Pixel 优先推送）
category: design-language
status: production        # production | style | experimental
variance: 5-8          # dials VARIANCE 适配区间
motion: 5-9          # dials MOTION 适配区间
density: 3-7          # dials DENSITY 适配区间
platforms: Android / 跨端 Web
verified: 2026-09-07
---
# M3 富表现力（Material 3 Expressive）

## 一句话定位
Google 2025 年对 Material 3 的"情绪升级"：大胆的形状对比、弹簧物理动效、鲜艳色彩角色，把"有生命感"做成 Android 默认设计语言。

## 视觉特征（token 级参数）
- **色彩**：角色制（基线 27 角色：primary / onPrimary / primaryContainer / surface / surfaceContainer…），Expressive 鼓励 secondary/tertiary 大面积对撞；基线值 primary **#6750A4** / onPrimary #FFFFFF / primaryContainer #EADDFF / surface #FEF7FF / surfaceContainer #F3EDF7；实际项目应从品牌 seed 生成 tonal palette（T0~T100）
- **形状**（M3 shape scale）：extra-small 4dp / small 8dp / medium 12dp / large 16dp / extra-large 28dp / full 胶囊；签名手法是同屏"形状对比"（28dp 大圆角卡 × 胶囊按钮 × 尖角 badge）
- **字阶**：Roboto Flex 变量字体（可调 optical size / weight / emphasis）；body-large 16/24、headline-medium 28/36、display-large 57/64；Expressive 用 700+ 字重做 emphasis 提权
- **动效-时长**：short4 200ms（选择件）、medium 250~400ms、long 450~600ms、extra-long 700~1000ms；官方标配 **进场 500ms / 退场 200ms**
- **动效-曲线**：standard `cubic-bezier(0.2,0,0,1)`；emphasized-decelerate `cubic-bezier(0.05,0.7,0.1,1)`；emphasized-accelerate `cubic-bezier(0.3,0,0.8,0.15)`
- **动效-弹簧物理（核心）**：以 damping/stiffness 替代固定时长；官方博客示例 spring(dampingRatio=0.6, stiffness=1600) 量级；空间位移用低阻尼 0.6~0.9（带微弹），颜色/透明度用无弹 1.0
- **形状 morph**：FAB ↔ Extended FAB、chip ↔ 全宽按钮、导航指示点 ↔ 胶囊 pill 的变形是标志动效
- **间距**：4dp 基数栅格；组件内边距 16dp，卡片间 8~16dp

## 结构骨架
1. 大标题顶栏或去顶栏 hero 大字，字重 700+
2. 主体：28dp 大圆角分组卡片，用 surfaceContainer 底色而非白底+阴影
3. 主操作：胶囊/大圆角 filled button（高 56~64dp），按压触发形状 morph
4. 底部导航：active 图标配 pill 形状指示器，切换时 shape morph
5. 反馈：涟漪弱化，改用弹簧位移 + 容器色填充

## 适用场景 / 慎用场景
- 适用：Android/跨端 C 端产品、健康、音乐、相机等情绪化场景、Wear OS
- 慎用：企业后台密集表单（弹簧降低录入效率）；官方建议克制——不要一屏用尽全部表现力

## AI 常见翻车点（反模式）
1. 只放大圆角不加动效——M3E 的灵魂是 spring + shape morph
2. 全屏套用基线紫 #6750A4——官方把它当默认值，品牌产品应换 seed 色
3. 用 ease/linear 硬套——必须换 emphasized/standard 曲线或 spring
4. 进场退场同长——退场必须短（200ms）

## CSS 关键实现（≤15 行核心代码）
```css
.m3-card { border-radius: 28px; background: #F3EDF7; padding: 16px; }
.m3-btn {
  height: 56px; padding: 0 24px; border-radius: 9999px;
  background: #6750A4; color: #FFF;
  font: 600 16px/1 "Roboto Flex", Roboto, sans-serif;
  transition: border-radius .45s cubic-bezier(.05,.7,.1,1),
              transform .35s cubic-bezier(.2,0,0,1);
}
.m3-btn:active { border-radius: 16px; transform: scale(.97); } /* 形状 morph */
@media (prefers-reduced-motion: reduce) { .m3-btn { transition: none; } }
```

## 来源链接
- 官方博客 Start building with M3 Expressive：https://m3.material.io/blog/building-with-m3-expressive
- 动效物理官方博客：https://m3.material.io/blog/m3-expressive-motion-theming
- Easing & duration token 表：https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
- Spring composite token：https://m3.material.io/styles/motion/overview/specs
