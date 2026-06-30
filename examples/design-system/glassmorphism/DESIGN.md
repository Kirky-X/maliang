---
version: alpha
name: Glassmorphism
description: A frosted-glass UI style using translucency, backdrop blur, and subtle highlights to float content above vibrant backgrounds.
colors:
  primary: "#7EA8FF"
  secondary: "#A78BFA"
  accent-pink: "#F9A8D4"
  accent-yellow: "#FCD34D"
  accent-green: "#6EE7B7"
  glass-bg: "#FFFFFF26"
  glass-border: "#FFFFFF40"
  glass-shadow: "#1F2687"
  on-glass: "#0F172A"
  on-color: "#0F172A"
  text-muted: "#64748B"
  white: "#FFFFFF"
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.25
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.33
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
  label:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0.05em
rounded:
  sm: 8px
  md: 12px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
components:
  button-primary:
    backgroundColor: "{colors.glass-bg}"
    textColor: "{colors.on-glass}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-secondary:
    backgroundColor: "{colors.white}"
    textColor: "{colors.on-glass}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 11px 23px
  input:
    backgroundColor: "{colors.glass-bg}"
    textColor: "{colors.on-glass}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
  chip:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-color}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 4px 12px
---

## Overview

Glassmorphism floats content on translucent, frosted-glass surfaces that blur and tint
whatever sits behind them. By combining `backdrop-filter: blur`, semi-transparent fills,
and subtle white borders and highlights, the style creates depth through atmospheric
layering rather than opaque cards. The result feels light, modern, and immersive — UI that
belongs to its environment rather than sitting on top of it.

Target audience: high-end product and brand sites, system and tool applications,
data-visualisation dashboards, mobile interfaces, and creative or art projects where
atmosphere and a sense of future-forward polish matter more than information density. Best
used over vibrant or gradient backgrounds where the blur effect is visible.

## Colors

The palette splits into **vibrant glass tints** (for backgrounds and accents) and
**translucent whites** (for the glass surfaces themselves).

- **primary (#7EA8FF):** Soft blue — the brand accent and default chip/active tint. Paired
  with `on-color` (#0F172A, near-black) for labels at 7.6:1.
- **secondary (#A78BFA):** Soft purple — secondary accent and gradient endpoint.
- **accent-pink (#F9A8D4) / accent-yellow (#FCD34D) / accent-green (#6EE7B7):** Vibrant
  tints for data visualisation, tags, and decorative gradients. Used as backgrounds with
  `on-color` dark text.
- **glass-bg (#FFFFFF26):** The core glass fill — white at 15% opacity. Every glass surface
  (cards, inputs, buttons) uses this. Combined with `backdrop-filter: blur(20px)` it
  produces the frosted effect.
- **glass-border (#FFFFFF40):** A 1px white border at 25% opacity. Defines the glass edge
  and catches light.
- **glass-shadow (#1F2687):** The coloured drop-shadow tint behind the canonical
  `0 8px 32px rgba(31,38,135,0.37)`. Gives glass a sense of floating above the canvas.
- **on-glass (#0F172A):** Dark slate text on glass surfaces. Clears AA against the light
  frosted fill (≈18:1 over white).
- **on-color (#0F172A):** Same dark slate, used on vibrant tints where white text would
  fail (e.g. `primary` + white = 2.4:1 ✗; `primary` + `on-color` = 7.6:1 ✓).
- **text-muted (#64748B):** Secondary text and captions. Use only on glass over light
  backgrounds.
- **white (#FFFFFF):** Highlights and the inset top-edge light
  (`inset 0 1px 0 rgba(255,255,255,0.4)`).

## Typography

**Inter** (or SF Pro Display) across five weights (Light 300, Regular 400, Medium 500,
Semibold 600, Bold 700).

- **headline-lg (32px / 600):** Hero and page titles on glass. Rendered in `on-glass`.
- **headline-md (24px / 500):** Card titles and section headers.
- **body-md (16px / 400):** Primary body copy at 1.5 line-height. Keep at or above 16px.
- **body-sm (14px / 400):** Captions and helper text, in `text-muted`.
- **label (12px / 500, 0.05em tracking):** Buttons, chips, and tab labels.

The type should feel light — favour Regular and Medium over Bold. Heavy weights crowd the
airy aesthetic.

## Layout

A fluid grid with a 4px base. The spacing scale — `xs` (4), `sm` (8), `md` (16), `lg` (24),
`xl` (32) — stays generous so glass panels have room to float.

- Glass card padding: `lg` (24px) on desktop, `md` (16px) on mobile.
- Gap between glass panels: `md` (16px) minimum — panels must not touch, or the blur
  overlaps unattractively.
- Section rhythm: `xl` (32px).
- Breakpoint: single column below 768px; reduce the blur radius on mobile for performance.

## Elevation & Depth

Depth comes from **layered translucency**, not opaque shadows. A glass surface floats
because it blurs and tints the vibrant background behind it, framed by a hairline
`glass-border` and a soft coloured shadow using the `glass-shadow` tint.

The canonical glass recipe (per source):

- Background: `rgba(255,255,255,0.15)` → `glass-bg` (#FFFFFF26)
- Blur: `backdrop-filter: blur(20px)`
- Border: `1px solid rgba(255,255,255,0.25)` → `glass-border` (#FFFFFF40)
- Shadow: `0 8px 32px rgba(31,38,135,0.37)` → tinted by `glass-shadow`
- Highlight: `inset 0 1px 0 rgba(255,255,255,0.4)` → uses `white`

Layer order: vibrant/gradient page background → glass panel → text/controls. Never stack
more than two glass layers — nested blur destroys legibility and performance.

## Shapes

Glass surfaces favour **soft, generous radii** to complement the frosted aesthetic.

- **sm (8px):** Inputs and small controls.
- **md (12px):** Buttons and medium cards — the default.
- **lg (16px):** Large glass panels, modals, and hero cards.
- **full (9999px):** Chips, avatars, and pill toggles.

Sharp corners (0px) clash with the soft, liquid feel — avoid them.

## Components

- **button-primary:** `glass-bg` fill with an `on-glass` dark label, `md` radius, `label`
  typography. Carries a `glass-border` and the canonical shadow. The default CTA — it
  floats above the canvas.
- **button-secondary:** Opaque `white` fill with `on-glass` text — used when a glass button
  would be lost against a busy background.
- **input:** `glass-bg` fill, `on-glass` text, `sm` radius, inset highlight. Placeholder
  uses `text-muted`. On focus the `glass-border` brightens.
- **chip:** `primary` tinted fill with `on-color` dark text, `full` radius. Selected state
  shifts to `secondary`.

Icons follow the Outline style — thin strokes that match the airy, light aesthetic.

## Do's and Don'ts

- **Do** place glass over vibrant or gradient backgrounds — the blur needs something to
  blur.
- **Don't** stack more than two glass layers — nested blur kills legibility and performance.
- **Do** use `on-glass` (#0F172A) dark text on glass; white text fails AA on light frosted
  fills.
- **Don't** use white text on `primary`/`secondary` tints — it fails AA (2.4:1). Use
  `on-color` instead.
- **Do** include the `backdrop-filter: blur(20px)` — without it, the surface is just a
  translucent box, not glass.
- **Don't** use blur in performance-critical lists or on low-end mobile — fall back to
  opaque `white` surfaces.
- **Do** add the inset top highlight (`white` at 0.4) — it gives the glass its "lit from
  above" feel.
- **Don't** use 0px radii — sharp corners fight the soft aesthetic.
