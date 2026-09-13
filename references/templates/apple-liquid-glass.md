---
name: apple-liquid-glass
title: 液态玻璃
source: Apple HIG「Materials」/ WWDC 2025「Meet Liquid Glass」（官方一手）
era: 2025 / iOS 26、iPadOS 26、macOS Tahoe 26
category: design-language
status: production        # production | style | experimental
variance: 4-7          # dials VARIANCE 适配区间
motion: 3-7          # dials MOTION 适配区间
density: 2-5          # dials DENSITY 适配区间
platforms: Apple 全平台 / Web 近似
verified: 2026-09-07
---
# 液态玻璃（Apple Liquid Glass）

## 一句话定位
Apple 2025 年发布的动态材质：把控件与导航做成悬浮于内容之上的"光学玻璃"，折射、模糊底层内容，并随环境与系统设置自适应明暗。

## 视觉特征（token 级参数）
- **分层铁律**：只用于功能层（Tab Bar / Sidebar / Toolbar 等控件与导航）；官方明确禁止铺在内容层卡片上；内容层用标准材质四档 ultraThin / thin / regular / thick
- **双变体**：regular（模糊 + 亮度自适应，系统组件默认，文字多时必用）；clear（高透明，仅用于照片/视频等富媒体之上）
- **调光层（官方数值）**：clear 变体下背景偏亮时，叠 **35% 不透明度黑色 dimming layer**；背景够暗或播放器自带则免加
- **模糊/饱和（Web 近似）**：`backdrop-filter: blur(20px) saturate(180%)`；官方本体是折射透镜（lensing）而非纯高斯模糊
- **高光描边**：上缘 1px 高光 white 30%~35%、下缘 1px 暗边 black 10%~15%；镜面高光随滚动/倾角流动
- **形状**：Capsule 胶囊 + 同心圆角（控件圆角与容器圆角同心）；本体近中性透明（亮 rgba(255,255,255,.14~.2) / 暗 rgba(40,40,40,.35)），彩色仅点睛
- **字阶**：SF Pro；iOS 基准 body 17/22，导航标题 17/22 semibold，大标题 34/41 bold
- **动效**：弹性 morph（按压收缩、展开归位）约 0.3~0.5s，spring 阻尼 0.8~0.9；滚动到边缘自动触发 scroll edge effect（玻璃下模糊+降不透明度）
- **无障碍自适应**：系统"降低透明度"→ 退化为近实色；"增强对比"→ 提高底色不透明度与描边；必须实现降级

## 结构骨架
1. 底层：全出血内容层（媒体、滚动列表）
2. 浮层：底部 Tab Bar / 顶部 Toolbar 用 Liquid Glass 胶囊，内容从其下穿透滚动
3. 边缘：scroll edge effect 在玻璃边缘做渐隐模糊
4. 内容层内一律普通材质/实色卡片；仅瞬态控件（slider/toggle）激活时短暂呈现玻璃感
5. 弹出层：alert / popover / sheet 用 regular 玻璃（信息多时提高不透明度）

## 适用场景 / 慎用场景
- 适用：媒体消费、地图/相机、沉浸式浏览等内容为王的界面；系统级导航与控件
- 慎用：高密度生产力表格；玻璃铺满内容层（官方反模式）；深浅背景反复切换区域

## AI 常见翻车点（反模式）
1. 给所有卡片套玻璃——官方明确玻璃只属于控件/导航层
2. 做成彩色磨砂贴片——那是 [glassmorphism](glassmorphism.md)；Liquid Glass 是近中性光学材质。两者在模板墙中互斥，同一界面二选一、不得混用
3. 缺少 reduce-transparency 下的实色降级，可访问性翻车
4. 描边一圈均匀白色——真实高光应是上亮下暗梯度 + 镜面流动

## CSS 关键实现（≤15 行核心代码）
```css
.glass {
  border-radius: 9999px;                 /* capsule 或与容器同心圆角 */
  background: rgba(255,255,255,.14);     /* 暗色环境 rgba(40,40,40,.35) */
  backdrop-filter: blur(20px) saturate(180%);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.35),
              inset 0 -1px 0 rgba(0,0,0,.12),
              0 8px 24px rgba(0,0,0,.12);
  transition: transform .35s cubic-bezier(.2,0,0,1);
}
.glass:active { transform: scale(.96); }
@media (prefers-reduced-transparency: reduce) {
  .glass { background: rgba(249,249,249,.94); backdrop-filter: none; }
}
```

## 来源链接
- HIG Materials（2025-09-09 官方更新，含 35% 调光层数值）：https://developer.apple.com/design/human-interface-guidelines/materials
- Liquid Glass 技术总览：https://developer.apple.com/documentation/technologyoverviews/liquid-glass
- WWDC25「Meet Liquid Glass」Session 219：https://developer.apple.com/videos/play/wwdc2025/219/
