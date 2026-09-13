---
name: gradient-on-dark
title: 暗底流光型
category: page-pattern
status: style
source: 视频研究 v05「5 种高级质感网页」（SONAR 案例转写）
era: 2026
verified: 2026-09-07
variance: "5-8"
motion: "2-5"
density: "1-4"
platforms: Web 桌面端
---
# 暗底流光型（Gradient on Dark）

## 一句话定位
近黑底上一条三色渐变只喂给标题一处，5% 噪点防止色带——与"AI 到处铺渐变"相反，渐变是稀缺资源。

## 视觉特征（token 级参数）
- 底色：近黑 **#060608**（禁纯黑 #000——纯黑显廉价且 OLED 上丢层次）
- 标题渐变：一条 **92deg** 三色 linear-gradient（示例：品红 #FF3D8A → 青 #3DE8FF → 绿 #7DFF5C），`background-clip: text`
- 渐变**只出现在标题这一处**；正文、按钮、边框一律单色
- 全屏覆盖 **5% 噪点**（SVG turbulence 或 PNG 叠加，`opacity: .05`）防渐变色带
- 点缀：1px 彩色细线波形（SVG path），其余界面元素全部退到灰阶
- 案例 SONAR："SOUND IN MOTION" 巨字 + 白色实心副词 + 描边虚词

## 结构骨架
1. 全屏近黑 Hero：巨字标题（渐变 clip）+ 描边/实心混排
2. 一条横向细线波形穿过标题腰部
3. 顶栏极简：品牌字标 + 右侧唯一彩色 CTA 胶囊
4. 底部一行元信息（城市 · 日期 · 场次），小号等宽字
5. 后续章节保持近黑，彩色只允许极少量点睛

## 适用场景 / 慎用场景
- 适用：音乐/夜生活活动、电竞、潮流品牌、发布会 hero
- 慎用：阅读型内容页（渐变标题干扰长文）；明亮品牌

## AI 常见翻车点（反模式）
1. 渐变到处都用（标题/按钮/背景全渐变）——正确：全页只喂标题一处
2. 用纯黑 #000 当底（正确：近黑 #060608）
3. 无噪点导致渐变 banding 条纹
4. 渐变色相相邻（红→橙→黄），失去"流光"张力（正确：跨色相环 120°+）

## CSS 关键实现（≤15 行）
```css
.page { background: #060608; color: #f5f5f5; }
.page::after { /* 5% 噪点层 */
  content: ""; position: fixed; inset: 0; pointer-events: none; opacity: .05;
  background-image: url("data:image/svg+xml,..."); /* feTurbulence */
}
.headline {
  background: linear-gradient(92deg, #ff3d8a, #3de8ff, #7dff5c);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.ghost { color: transparent; -webkit-text-stroke: 1px rgba(255,255,255,.4); }
```

## 来源链接
- temp/video-analysis/v05.md（帧转写）；案例：SONAR 声音活动
