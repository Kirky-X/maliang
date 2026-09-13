---
name: neumorphism
title: 新拟物（软 UI）
source: 社区范式（Dribbble 2019 Alexander Plyuto 作品引发；neumorphism.io 参数生成器）
era: 2019~2021（已退潮——标注为谨慎使用）
category: design-language
status: experimental        # production | style | experimental
variance: 2-4          # dials VARIANCE 适配区间
motion: 1-3          # dials MOTION 适配区间
density: 2-4          # dials DENSITY 适配区间
platforms: 概念 / 小部件
verified: 2026-09-07
---
# 新拟物（Neumorphism / Soft UI）

## 一句话定位
同色凸凹浮雕：元素与背景同色，靠"左上亮影 + 右下暗影"挤出软浮雕感；曾风靡 Dribbble，因对比度缺陷退潮——本模板供识别与"降级改造"用。

## 视觉特征（token 级参数）
- **底色**：经典蓝灰白 **#E0E5EC**（同族 #E8ECF3 / #EBEEF3）；元素与背景必须同色
- **凸起（默认态）**：`box-shadow: -9px -9px 16px #FFFFFF, 9px 9px 16px rgba(163,177,198,.6)`
- **凹陷（按下/输入框）**：`inset -9px -9px 16px #FFFFFF, inset 9px 9px 16px rgba(163,177,198,.6)`
- **阴影比例**：偏移 8~10px、模糊 16~24px（blur ≈ 2×offset）；双影必须 135° 对角（左上亮/右下暗）
- **圆角**：控件 12~16px、卡片 20~24px；无描边
- **颜色**：单色系；文字 #6D7A8C（灰蓝）或 #44476A；强调色少量（如 #4A90D9）
- **字阶**：标题 24~32px 600、正文 15~16px——字色对比是最大短板
- **动效**：按下凸→凹 150~200ms ease-out，阴影同步切换 inset

## 结构骨架
1. 全局同色底，无分区线
2. 工具组：凸起圆形按钮（直径 48~56px）成排
3. 显示区：凹陷面板（嵌入感）承载数值/文本
4. 主 CTA：凸起大按钮，按下凹陷
5. 层级完全依赖阴影方向，放弃颜色区分

## 适用场景 / 慎用场景
- 适用：智能音箱/家居小控制面板、桌面小部件、概念 UI、装饰性局部
- 慎用（生产环境大多数场景）：**可访问性风险**——同色底上灰字对比常 <3:1，无法满足 WCAG AA 4.5:1（SC 1.4.3）；控件边界靠低对比阴影，低视力/强光下不可辨；按下状态只有深度变化无颜色反馈，色弱用户难感知

## AI 常见翻车点（反模式）
1. 在彩色背景上做新拟物——必须同色系（背景=元素色）
2. 阴影偏移与模糊比例失调——保持 blur ≈ 2×offset、135° 对角
3. 主 CTA 与底面同对比不可辨——生产环境请加实色填充或描边降级
4. 暗色模式照搬白色亮影——需换暗色对（如 #2C2C34 亮 / #23232A 暗），风险同样存在

## CSS 关键实现（≤15 行核心代码）
```css
.neu { background:#E0E5EC; border-radius:16px; color:#6D7A8C;
  box-shadow: -9px -9px 16px #FFFFFF, 9px 9px 16px rgba(163,177,198,.6); }
.neu-in { box-shadow: inset -9px -9px 16px #FFFFFF,
                      inset 9px 9px 16px rgba(163,177,198,.6); }
.neu-btn { width:56px; height:56px; border-radius:50%; cursor:pointer;
  transition: box-shadow .18s ease-out; }
.neu-btn:active { box-shadow: inset -6px -6px 10px #FFFFFF,
                             inset 6px 6px 10px rgba(163,177,198,.6); }
.neu-btn:focus-visible { outline:2px solid #4A90D9; outline-offset:4px; }
.neu strong { color:#3E4A5E; } /* 关键文字提对比，补可访问性 */
```

## 来源链接
- 参数生成器（数值来源）：https://neumorphism.io/
- 风格起点（Dribbble 标签聚合）：https://dribbble.com/tags/neumorphism
- 对比度强制要求 WCAG 2.1 SC 1.4.3：https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
