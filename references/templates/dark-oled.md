---
name: dark-oled
title: OLED 暗色模式
source: Google Material 暗色主题规范 / Apple HIG Dark Mode / Android 官方文档（均为官方一手）
era: Material 2 暗色规范 2018；M3 2021；Android 10+ 系统级暗色
category: design-language
status: production        # production | style | experimental
variance: 2-6          # dials VARIANCE 适配区间
motion: 2-6          # dials MOTION 适配区间
density: 3-8          # dials DENSITY 适配区间
platforms: 全平台（可与任意模板叠加）
verified: 2026-09-07
---
# OLED 暗色模式（Dark OLED）

## 一句话定位
以"像素发光成本"为第一性原理的暗色规范：纯黑与近黑分层、白色透明度做文字三档层级、彩色统一降饱和，兼顾省电、对比度与夜间舒适度。

## 视觉特征（token 级参数）
- **底色两档**：OLED 省电/影院场景用纯黑 **#000000**（像素不发光）；通用暗色用近黑 **#121212**（Material 官方推荐底，避免 OLED 拖影与黑块感）；M3 基线 surface 为 #1C1B1F（微暖中性）
- **层级提升（不用投影）**：M2 elevation overlay 白色叠加——1dp=5%、4dp=9%、8dp=12%、16dp=15%、24dp=16%；iOS 近似三档 #000000 → #1C1C1E → #2C2C2E
- **文字三档（官方数值）**：主文字 white 87% = rgba(255,255,255,.87)；次级 60%；禁用 38%
- **彩色降饱和**：功能色统一用 200 色阶——blue #90CAF9 / green #A5D6A7 / red #EF9A9A / yellow #FFF59D；禁用 500~700 高饱和原色直出
- **描边/分隔**：分隔线 1px rgba(255,255,255,.08~.12)；卡片可加 1px rgba(255,255,255,.06) 细边替代投影
- **圆角**：与亮色一致（卡片 12~16px）
- **阴影**：暗色禁用黑色投影（不可见），层级一律靠表面提亮
- **动效**：明暗切换 300~400ms fade；Android 13+ 提供 350ms 圆形扩散转场

## 结构骨架
1. 背景层：#000 或 #121212 全局
2. 卡片层：提亮一档（#1C1C1E 或白 overlay 9~12%）
3. 悬浮层（菜单/浮窗）：再提亮一档（#2C2C2E 或 overlay 16%）+ 1px 细边
4. 文字三档 87/60/38 + 200 色阶功能色
5. 媒体保持原亮度，UI 亮度不得反超媒体

## 适用场景 / 慎用场景
- 适用：AMOLED 设备、媒体/阅读类、开发者工具、夜间高频生产力应用
- 慎用：户外强光为主的场景（暗色降低可读性）；打印/导出物；纯黑底上放大段白文（halation 眩光，正文用 .87 白而非纯白）

## AI 常见翻车点（反模式）
1. 亮色直接反色：文字仍用黑色系——必须换 87/60/38 白三档
2. 暗色下保留黑色投影分层——改用表面提亮
3. 状态色照搬亮色高饱和（如 #2196F3）——必须换 200 色阶
4. 深灰/纯黑随机混用无层级——应形成 #000/#121212/#1C1C1E/#2C2C2E 的固定梯子

## CSS 关键实现（≤15 行核心代码）
```css
@media (prefers-color-scheme: dark) {
  :root { --bg:#000; /* 近黑方案改 #121212 */
    --surface:#1C1C1E; --surface-hi:#2C2C2E;
    --on:#FFFFFFDE; --on-med:#FFFFFF99; --on-low:#FFFFFF61;
    --stroke:#FFFFFF14; --accent:#90CAF9; --danger:#EF9A9A; }
}
.oled-card { background:var(--surface); border:1px solid var(--stroke);
  color:var(--on); border-radius:12px; box-shadow:none; }
.oled-sub { color:var(--on-med); }
.oled-float { background:var(--surface-hi); border:1px solid var(--stroke); }
```

## 来源链接
- Material 暗色主题（#121212 / 87-60-38 / elevation overlay 数值）：https://m2.material.io/design/color/dark-theme.html
- Apple HIG Dark Mode：https://developer.apple.com/design/human-interface-guidelines/dark-mode
- Android 官方暗色实现：https://developer.android.com/develop/ui/views/theming/darktheme
