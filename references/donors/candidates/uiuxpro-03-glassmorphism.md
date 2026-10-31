<!-- 供体候选池快照(原文存档,非蒸馏供体)。
     站点分组: 通用风格模板(styleGeneral) · 站点摘要: Glassmorphism is a UI style reference for general interfaces, focused on Frosted glass, transparent, blurred background, layered, vibrant background.
     站点色板: #667eea, #764ba2, #f093fb, #0080ff, #8b00ff, #ff1493
     晋升正式供体须满足 references/donors/README.md §5 三条件;蒸馏稿另立 references/donors/<id>.md,与本快照并存。 -->

# Glassmorphism

## 1. Visual Theme & Atmosphere

Glassmorphism is a UI style reference for general interfaces, combining Frosted glass, transparent, blurred background, layered, vibrant background, light source, depth, multi-layer. The visual direction is shaped by Backdrop blur (10-20px), subtle border (1px solid rgba white 0.2), light reflection, Z-depth.

Use it for Modern SaaS (SaaS), financial dashboards (儀表板), high-end corporate (企業), lifestyle apps (應用程式), modal overlays, navigation. Avoid it for Low-contrast backgrounds, critical accessibility (無障礙性), performance-limited (效能), dark text on dark.

**Key Characteristics:**
- Primary palette: Translucent white: rgba(255,255,255,0.1-0.3)
- Secondary palette: Vibrant: Electric Blue #0080FF, Neon Purple #8B00FF, Vivid Pink #FF1493, Teal #20B2AA
- Effects: Backdrop blur (10-20px), subtle border (1px solid rgba white 0.2), light reflection, Z-depth
- Accessibility: ⚠ Ensure 4.5:1; performance: ⚠ Good; dark mode: ✓ Full.
- Best for: Modern SaaS (SaaS), financial dashboards (儀表板), high-end corporate (企業), lifestyle apps (應用程式), modal overlays, navigation
- Avoid for: Low-contrast backgrounds, critical accessibility (無障礙性), performance-limited (效能), dark text on dark

## 2. Implementation Notes

- Framework fit: Tailwind 9/10, MUI 8/10, Chakra 8/10
- Era reference: 2020s Modern
- Local preview: [Open HTML preview](../../refstyles/03-glassmorphism.html)
- Library index: [Open UI/UX Pro Max home](../../index.html)
