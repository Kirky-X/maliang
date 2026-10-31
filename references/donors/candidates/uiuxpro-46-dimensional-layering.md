<!-- 供体候选池快照(原文存档,非蒸馏供体)。
     站点分组: 通用风格模板(styleGeneral) · 站点摘要: Dimensional Layering is a UI style reference for general interfaces, focused on Depth, overlapping, z-index, layers, 3D.
     站点色板: #ffffff, #f5f5f5, #e0e0e0
     晋升正式供体须满足 references/donors/README.md §5 三条件;蒸馏稿另立 references/donors/<id>.md,与本快照并存。 -->

# Dimensional Layering

## 1. Visual Theme & Atmosphere

Dimensional Layering is a UI style reference for general interfaces, combining Depth, overlapping, z-index, layers, 3D, shadows, elevation, floating, cards, spatial hierarchy. The visual direction is shaped by z-index stacking, box-shadow elevation (4 levels), transform: translateZ(), backdrop-filter, parallax.

Use it for Dashboards (儀表板), card layouts, modals, navigation, product showcases, SaaS interfaces (SaaS). Avoid it for Print-style layouts, simple blogs, low-end devices, flat design requirements.

**Key Characteristics:**
- Primary palette: Neutral base (#FFFFFF, #F5F5F5, #E0E0E0) + brand accent for elevated elements
- Secondary palette: Shadow variations (sm/md/lg/xl), elevation colors, highlight colors for top layers
- Effects: z-index stacking, box-shadow elevation (4 levels), transform: translateZ(), backdrop-filter, parallax
- Accessibility: ⚠ Moderate (SR issues); performance: ⚠ Good; dark mode: ✓ Full.
- Best for: Dashboards (儀表板), card layouts, modals, navigation, product showcases, SaaS interfaces (SaaS)
- Avoid for: Print-style layouts, simple blogs, low-end devices, flat design requirements

## 2. Implementation Notes

- Framework fit: Tailwind 10/10, MUI 10/10, Chakra 10/10
- Era reference: 2020s Modern
- Local preview: [Open HTML preview](../../refstyles/46-dimensional-layering.html)
- Library index: [Open UI/UX Pro Max home](../../index.html)
