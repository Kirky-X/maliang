---
version: alpha
name: Neomorphism
description: A soft, extruded UI style using dual-direction light and shadow on a monochromatic canvas for a tactile, futuristic feel.
colors:
  primary: "#6B7280"
  accent: "#7A87BA"
  accent-cyan: "#7DC9FC"
  accent-purple: "#AC84E4"
  background: "#E0E5EC"
  surface: "#E0E5EC"
  on-surface: "#4B5563"
  on-primary: "#FFFFFF"
  muted: "#9CA3AF"
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
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-raised:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
  chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 4px 12px
---

## Overview

Neomorphism (Soft UI) creates interfaces that feel extruded from a single monochromatic
surface. By applying soft, dual-direction shadows to elements that share the background
colour, it produces a tactile, futuristic aesthetic — as if controls were pressed into or
raised out of a soft material. The result is calm, low-contrast, quietly modern, and
comfortable for long sessions.

Target audience: system and tool applications, data and information dashboards,
collaboration and productivity platforms, and lightweight consumer apps where a restful,
low-fatigue interface is valued over high-contrast urgency.

**A note on contrast (surfaced, not hidden):** the source palette is intentionally
low-saturation and light. Its deepest neutral `primary` (#6B7280) reaches only 3.8:1 on the
signature `background` (#E0E5EC) canvas — below WCAG AA. To honour the style while keeping
text legible, body copy uses `on-surface` (#4B5563), a deeper companion grey from the same
neutral family, which clears AA at 6:1. `primary` (#6B7280) is reserved for button fills,
where it pairs with `on-primary` white text at 4.8:1. This trade-off follows the source's
own caution: in low-contrast contexts, ensure legibility and obvious interaction feedback.

## Colors

The palette is built on one foundational canvas colour with a small set of muted accents.

- **background (#E0E5EC):** The signature light grey-blue canvas. Every surface shares this
  colour so that shadows — not fills — define edges.
- **surface (#E0E5EC):** Identical to `background` by design. Neomorphic elements are never
  distinguished by fill; only by light and shadow.
- **primary (#6B7280):** The deepest neutral from the source palette. Used as a fill for
  primary buttons and as borders/dividers. Paired with `on-primary` (#FFFFFF) for button
  labels at 4.8:1.
- **on-surface (#4B5563):** Body and heading text. A deeper companion to #6B7280, chosen so
  that text clears WCAG AA (6:1) on the light canvas. All text — headlines, body, labels —
  uses this token.
- **accent (#7A87BA):** Muted blue-purple for active states, selected chips, and focus
  rings. Decorative/interactive only — not for body text (2.8:1 on canvas).
- **accent-cyan (#7DC9FC) / accent-purple (#AC84E4):** Gradient endpoints and icon tints.
  Used sparingly for delight (gradients Blue→Cyan, Cyan→Purple, Purple→Pink per the source).
- **muted (#9CA3AF):** Placeholder text and disabled states. Large-text or non-critical use
  only.
- **on-primary (#FFFFFF):** White label text on `primary` fills.

## Typography

**Inter** (or SF Pro Display) carries the entire system across five weights (Light 300,
Regular 400, Medium 500, Semibold 600, Bold 700).

- **headline-lg (32px / 600):** Page titles. Rendered in `on-surface`.
- **headline-md (24px / 500):** Section headings and card titles.
- **body-md (16px / 400):** Primary body copy at 1.5 line-height. Never below 16px.
- **body-sm (14px / 400):** Captions, helper text, and metadata.
- **label (12px / 500, 0.05em tracking):** Buttons, chips, and toggles. Slightly wider
  tracking than body to separate control labels from prose.

Keep weights restrained — two weights per screen is ideal. The calm aesthetic is undermined
by heavy bold usage.

## Layout

A simple fluid grid with a 4px base unit. The spacing scale — `xs` (4), `sm` (8), `md` (16),
`lg` (24), `xl` (32) — is deliberately tight because Neomorphism relies on generous canvas
breathing room rather than dense packing.

- Card padding: `md` (16px) standard, `lg` (24px) for primary panels.
- Section gaps: `xl` (32px). Avoid larger gaps — the soft aesthetic benefits from proximity.
- Touch targets: minimum 44×44px (use `md` spacing to maintain clearance).
- Breakpoint: single column below 768px; maintain `md` (16px) as minimum padding at all sizes.

## Elevation & Depth

Depth is the defining feature of Neomorphism. Instead of drop shadows, elements use
**dual shadows** — a light shadow top-left and a dark shadow bottom-right — to appear
extruded from (or pressed into) the shared `surface`/`background` canvas.

- **Raised (default):** `box-shadow: 6px 6px 12px #BEBEC1, -6px -6px 12px #FFFFFF;` — the
  element appears to rise from the surface.
- **Pressed/inset:** `box-shadow: inset 6px 6px 12px #BEBEC1, inset -6px -6px 12px #FFFFFF;`
  — the element appears pressed in. Used for active toggles, pressed buttons, and selected
  inputs.
- **Flat:** No shadow — for disabled or informational surfaces.

The light source is assumed top-left, consistently. Never reverse it within the same screen.
Shadows must stay soft — sharp shadows break the material illusion. Avoid stacking more than
two elevation levels; the aesthetic depends on a single, calm plane.

## Shapes

Neomorphism favours **soft, generous radii** — sharp corners fight the soft shadow
aesthetic.

- **sm (8px):** Inputs and small controls — the minimum softness.
- **md (12px):** Buttons and medium cards — the default radius for most components.
- **lg (16px):** Large panels and containers — softer, more prominent.
- **full (9999px):** Chips, avatars, and circular toggles.

Never use a 0px radius — it breaks the soft aesthetic. Keep radii consistent within a
component group.

## Components

- **button-primary:** Filled `primary` (#6B7280) with an `on-primary` white label. The main
  CTA. `md` radius, `label` typography. On press, transition to an inset shadow.
- **button-raised:** `surface` background (same as canvas) with `on-surface` text, raised
  via the dual shadow. The quintessential neomorphic button — for secondary actions.
- **input:** `surface` background, `on-surface` text, `sm` radius, inset shadow to appear
  recessed. Placeholder uses `muted`. On focus the inset shadow deepens slightly and an
  `accent` ring appears.
- **chip:** `surface` background, `on-surface` label, `full` radius. Selected state uses
  the `accent` fill.

Icons are simple and soft — outline weight, rounded line caps, no sharp detail.

## Do's and Don'ts

- **Do** use dual shadows (light top-left, dark bottom-right) for every raised element.
- **Don't** use fills to distinguish elements — only shadows and insets.
- **Do** use `on-surface` (#4B5563) for all text to clear WCAG AA on the light canvas.
- **Don't** use `accent` (#7A87BA) for body text — it fails AA (2.8:1).
- **Do** keep the light source consistent (top-left) across the whole screen.
- **Don't** stack more than two elevation levels — the aesthetic needs a single calm plane.
- **Do** use inset shadows for pressed and active states.
- **Don't** use 0px radii — they break the soft aesthetic.
- **Do** fall back to a subtle `primary` border when shadows alone are insufficient for
  legibility in low-vision contexts.
