<!-- 供体候选池快照(原文存档,非蒸馏供体)。
     站点分组: 分析仪表板模板(styleAnalytics) · 站点摘要: Heat Map & Heatmap Style is a UI style reference for analytics and BI dashboards, focused on Color-coded grid/matrix, data intensity visualization, geographical heat maps, correlation matrices, cell-based representation.
     站点色板: #1e293b, #1e3a5f, #0369a1, #0284c7, #38bdf8, #7dd3fc
     晋升正式供体须满足 references/donors/README.md §5 三条件;蒸馏稿另立 references/donors/<id>.md,与本快照并存。 -->

# Heat Map & Heatmap Style

## 1. Visual Theme & Atmosphere

Heat Map & Heatmap Style is a UI style reference for analytics and BI dashboards, combining Color-coded grid/matrix, data intensity visualization, geographical heat maps, correlation matrices, cell-based representation, gradient coloring. The visual direction is shaped by Color gradient transitions on data change, cell highlighting on hover, tooltip reveal on click, smooth color animation.

Use it for Geographical analysis, performance matrices (效能), correlation analysis, user behavior heatmaps, temperature/intensity data. Avoid it for Linear data representation, categorical comparisons (use bar charts), small datasets.

**Key Characteristics:**
- Primary palette: Gradient scale: Cool (blue #0080FF) to hot (red #FF0000), neutral middle (white/yellow)
- Secondary palette: Support gradients: Light (cool blue) to dark (warm red), divergent for positive/negative data, monochromatic options
- Effects: Color gradient transitions on data change, cell highlighting on hover, tooltip reveal on click, smooth color animation
- Accessibility: ⚠ Colorblind considerations; performance: ⚡ Excellent; dark mode: ✓ Full (with adjustments).
- Best for: Geographical analysis, performance matrices (效能), correlation analysis, user behavior heatmaps, temperature/intensity data
- Avoid for: Linear data representation, categorical comparisons (use bar charts), small datasets

## 2. Implementation Notes

- Framework fit: D3.js 10/10, Recharts 8/10, Chart.js 8/10
- Era reference: 2020s Modern
- Local preview: [Open HTML preview](../../refstyles/29-heatmap-density.html)
- Library index: [Open UI/UX Pro Max home](../../index.html)
