---
name: data-dense-dashboard
title: 数据密集型仪表盘
source: 综合范式（Apple HIG 布局 + Material 数据表格 + GitHub/Grafana 实践体系）
era: 持续演进（2020s 主流形态）
category: design-language
status: production        # production | style | experimental
variance: 2-4          # dials VARIANCE 适配区间
motion: 1-3          # dials MOTION 适配区间
density: 7-10          # dials DENSITY 适配区间
platforms: Web 后台
verified: 2026-09-07
---
# 数据密集型仪表盘（Data-Dense Dashboard）

## 一句话定位
以"扫一眼读数"为目标的高密度面板：严格 4/8px 网格、KPI 卡片区、明细表格区、等宽数字字体，层级靠字号与灰阶而非装饰。

## 视觉特征（token 级参数）
- **栅格**：12 列、gap 16px（紧凑 8px）；KPI 卡最小 240×120px；页边距 24px；内容最大宽 1600px
- **底色**：亮 #F7F8FA 页底 + #FFFFFF 卡；暗 #0D1117 页底 + #161B22 卡（GitHub 暗系）；描边 1px #E5E7EB（亮）/ #30363D（暗）
- **圆角**：8~12px（克制，≤16px）
- **信息层级（数字优先）**：KPI 数值 28~32px/1.1 semibold + `font-variant-numeric: tabular-nums`；环比 delta 13px（▲ #16A34A / ▼ #DC2626）；卡标题 13px 500 #374151；辅助标签 11~12px 大写 +0.04em #6B7280
- **表格**：行高 40px（紧凑 32px）；表头 12px #6B7280 大写；行分隔 1px #F3F4F6；悬停行 #F9FAFB；数字列右对齐等宽
- **数字字体**：Inter（tnum）/ SF Pro / Roboto Mono——等宽防刷新跳动
- **图表**：折线 2px、柱宽 8~12px、网格线 1px rgba(107,114,128,.15)；每图 ≤5 系列；色板 #2563EB / #16A34A / #D97706 / #DC2626 / #7C3AED（色盲安全顺序）
- **动效**：数值滚动 500ms ease-out；卡片入场 stagger 40ms；悬停仅描边变色 100ms

## 结构骨架
1. 顶部：页标题 20px + 右对齐时间范围/筛选器（控件高 32px）
2. 第一行：4~6 张等宽 KPI 卡（数值 + delta + 迷你 sparkline）
3. 第二行：主趋势图（8 列）+ 分布/漏斗（4 列）
4. 第三行起：明细表格（12 列或 8+4 主从），列排序 + 固定表头
5. 全局：面包屑 + 上次刷新时间戳 + 舒适/紧凑密度切换

## 适用场景 / 慎用场景
- 适用：运营后台、监控/可观测平台、金融看板、CRM/ERP 数据页
- 慎用：营销首页（密度即压迫感）；移动端直接等比缩放（应重排为单列卡片流）；内容型网站

## AI 常见翻车点（反模式）
1. 数字用比例字体导致刷新跳动——必须 tabular-nums
2. 装饰过重（24px 大圆角、渐变卡、玻璃混入）——密度场景装饰是负资产
3. KPI 只有大数字没有基准（缺环比 delta/目标线）
4. 图表 10+ 系列不分级——用色盲安全色板 + 直接标注替代纯图例

## CSS 关键实现（≤15 行核心代码）
```css
.dash { display:grid; grid-template-columns:repeat(12,1fr); gap:16px;
  padding:24px; background:#F7F8FA;
  font:400 13px/1.5 Inter,"SF Pro Text",sans-serif; }
.kpi { grid-column:span 3; background:#FFF; border:1px solid #E5E7EB;
  border-radius:10px; padding:16px; }
.kpi-value { font-size:30px; font-weight:600; line-height:1.1;
  font-variant-numeric:tabular-nums; color:#111827; }
.kpi-delta.up { color:#16A34A; } .kpi-delta.down { color:#DC2626; }
.kpi-label { font-size:11px; letter-spacing:.04em; text-transform:uppercase; color:#6B7280; }
@media (max-width:1024px) { .kpi { grid-column:span 6; } }
```

## 来源链接
- Apple HIG Layout（信息层级原则）：https://developer.apple.com/design/human-interface-guidelines/layout
- Material Data Tables（密度与行高范式）：https://m2.material.io/components/data-tables
- 等宽数字 CSS 规范：https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
