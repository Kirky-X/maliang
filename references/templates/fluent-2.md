---
name: fluent-2
title: Fluent 2 设计系统
source: Microsoft Fluent 2 官网 / Microsoft Learn（Windows App SDK 官方文档）
era: 2023 / Windows 11、Microsoft 365、@fluentui v9
category: design-language
status: production        # production | style | experimental
variance: 2-5          # dials VARIANCE 适配区间
motion: 2-5          # dials MOTION 适配区间
density: 4-8          # dials DENSITY 适配区间
platforms: Windows / Web / 跨平台
verified: 2026-09-07
---
# Fluent 2（Microsoft Fluent 2）

## 一句话定位
微软跨 Web/Windows/iOS/Android 的统一设计系统：token 驱动、克制中性，以 1px 细描边 + 双层软阴影 + 亚克力浮层构成"安静的专业感"。

## 视觉特征（token 级参数）
- **色彩**：品牌主色 brandWeb.80 **#0F6CBD**（Fluent 2 回归蓝）；正文 text1 #242424、次级 #424242、占位 #616161；边框 neutralStroke1 #D1D1D1；页面底 #FAF9F8（浅灰白）
- **圆角**：2 / 4 / 6 / 8 / 12px 档位——≤32px 小组件 2px、medium 4px、large 6px、extra-large 8~12px；Fluent 2 预设把控件圆角从 2px 提到 4px
- **阴影**：双层阴影梯子 shadow2~shadow64（数字≈模糊 px，low ramp 2/4/8/16 + high ramp 28/64）；shadow2 = `0 1px 2px rgba(0,0,0,.14), 0 0 2px rgba(0,0,0,.12)`，offset 随档位翻倍
- **描边**：1px 实线是组件默认语言（按钮/输入框/卡片均有 hairline），阴影只表达层级不做造型
- **材质**：Acrylic 亚克力官方五层配方 = 背景 + 模糊 + **exclusion 混合层** + tint 色层 + 噪点；仅用于 transient surface（flyout/菜单/浮窗）
- **字阶**（Windows type ramp，Segoe UI Variable）：Display 68/92、Title Large 40/52、Title 28/36、Subtitle 20/28、Body 14/20、Caption 12/16；字重 400/600/700
- **间距**：4px 基数（s=4, m=8, l=12, xl=16…）；控件标准高度 32px
- **动效**：微交互 100~150ms、浮层出入 200~300ms，近似 fluent ease `cubic-bezier(0.33,0,0.67,1)`，出入对称

## 结构骨架
1. 左侧 48px 图标栏 + 240~320px 导航面板（NavigationView 模式），1px 分隔线而非阴影
2. 顶部命令栏 48px，图标按钮 32×32
3. 内容区白底卡片：4~8px 圆角、1px 描边、悬停阴影升级 shadow4→shadow8
4. 弹层：菜单/浮窗用 Acrylic + 8px 圆角 + shadow8
5. 表单高密度：控件 32px 高，垂直节奏 4px 网格

## 适用场景 / 慎用场景
- 适用：企业软件、生产力套件、B 端管理后台、跨平台一致性要求高的产品
- 慎用：强情绪消费级营销页（会过素）；Acrylic 铺大面积背景（官方 don'ts）

## AI 常见翻车点（反模式）
1. 圆角放大到 12~16px——Fluent 控件就是 4~8px，大圆角破坏识别度
2. 无描边纯阴影卡片——Fluent 是 1px 描边 + 阴影并存
3. 多块 Acrylic 相邻拼接产生接缝（官方明确禁止）；accent 色文字压 Acrylic（14px 下对比不达标）
4. 重投影大悬浮——Fluent 阴影梯子全程低调

## CSS 关键实现（≤15 行核心代码）
```css
:root { --brand:#0F6CBD; --stroke:#D1D1D1; --text:#242424;
        --shadow4: 0 2px 4px rgba(0,0,0,.14), 0 0 2px rgba(0,0,0,.12); }
.fluent-card {
  background:#FFF; border:1px solid var(--stroke); border-radius:6px;
  box-shadow: var(--shadow4); color: var(--text); padding:16px;
  font: 400 14px/20px "Segoe UI Variable Text","Segoe UI",sans-serif;
}
.fluent-card:hover { box-shadow: 0 4px 8px rgba(0,0,0,.14), 0 0 2px rgba(0,0,0,.12); }
.fluent-btn { background:var(--brand); color:#FFF; border-radius:4px;
  height:32px; padding:0 12px; font:600 14px "Segoe UI Variable"; border:1px solid transparent; }
```

## 来源链接
- Fluent 2 官网（principles / shapes / elevation / typography / design-tokens）：https://fluent2.microsoft.design/
- Acrylic 官方五层配方与 do/don't：https://learn.microsoft.com/en-us/windows/apps/design/style/acrylic
- Windows 字体 ramp：https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/typography
