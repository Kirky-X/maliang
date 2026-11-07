---
version: alpha
name: <产品名>
description: <一句话品牌摘要>
decisions:                          # 0d 决策表;id 供 token 行尾溯源,字段见 references/meta/spec-schema.md
  - id: D-P1-1                      # 原则 P1 下的第 1 条决策
    decision: <一句话决策,可被 token 引用>
    rationale: <为什么,含被拒绝的默认>
    date: 2026-01-15
    scope: 全站
  # 原则 P1/P2/P3 对应 ## Overview 里的 2-3 条立场
  # 溯源注释规则(# D-P<n>-<m> / # no-decision: <来源>)唯一 canonical 见 references/meta/token-provenance.md
colors:
  primary: "#..." # D-P1-1
  secondary: "#..." # D-P1-2
  tertiary: "#..." # D-P1-1        # 强调色 / CTA
  neutral: "#..." # D-P1-2         # 背景、表面
typography:
  headline-lg: # D-P2-1
    fontFamily: ...
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  body-md: # D-P2-1
    fontFamily: ...
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  # 完整阶梯(headline-md/body-lg/label-sm 等)见 references/meta/spec-schema.md 推荐命名
rounded:
  sm: 4px # D-P3-1
  md: 8px # D-P3-1
  lg: 16px # D-P3-1
  full: 9999px # D-P3-2
spacing:
  xs: 4px # D-P3-1
  sm: 8px # D-P3-1
  md: 16px # D-P3-1
  lg: 32px # no-decision: 继承品牌规范
  xl: 64px # D-P3-1
components:
  button-primary: # D-P1-3
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  # 更多组件模式(hover/active/disabled、chip、input 等)见本仓 examples/design-system/heritage/DESIGN.md
effects:                            # 可选特效段(maliang 扩展键,lint 静默;1C 第 6 步识别结果落这里,无特效或静帧无证据时整段省略或弃权)
  primary_technology: CSS only # D-P3-3
  performance_tier: lightweight # lightweight(CSS+简单 JS)/medium(Canvas 2D、SVG 动画)/heavy(WebGL、Three.js、shader)
  fallback_strategy: reduced-motion 与低端设备降级为静态 poster 帧 # D-P3-3
---

## Overview
<品牌性格、目标受众、情感调性。2-4 句。>
<P1/P2/P3 三条原则,每条须落得到下方至少一个 token 值——只写在散文里不改值的原则不算立场,见 references/meta/token-provenance.md(V3 空原则)。>
## Colors
<每个色板的角色。该出现在哪、不该出现在哪。>
## Typography
<字体策略。每个字族的角色。层级。>
## Layout
<栅格模型、间距哲学、容器约束。参考 references/dimensions/layout.md>
## Elevation & Depth
<阴影、色调分层、边框,或纯对比。>
## Shapes
<圆角哲学。锐利 = 工程感,圆润 = 亲和。>
## Components
<token 无法表达的关键模式与交互状态。区段形态先从 references/components/INDEX.md 挑名——从索引挑名、只加载选中的那几个(典型 5-7 个),不整库加载;区段原型管「这段长成什么」,元素级外观(按钮/卡片/表单)与模式级命名词汇(含 nav-* 导航等结构条目)都在 references/vocabulary/。>
## Do's and Don'ts
- Do ...
- Don't ...
## Provenance
<仅提取型 DESIGN.md(1A/1C 且来源为 URL)需要,置于文末。记:来源模式(截图/URL)+ 来源归属三选 attestation(自有 / 本品牌公开参照)+ 提取日期 + 一行置信注记。三选处置与写法见 references/meta/source-hygiene.md §4。>
