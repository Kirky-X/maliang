---
version: alpha
name: Swiss Style
description: A grid-driven, typographically rational system with a single signal red for interaction.
colors:
  primary: "#E30613"
  ink: "#000000"
  ink-muted: "#666666"
  surface: "#FFFFFF"
  neutral: "#F2F2F2"
typography:
  headline-display:
    fontFamily: Helvetica Neue
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Helvetica Neue
    fontSize: 40px
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Helvetica Neue
    fontSize: 28px
    fontWeight: 500
    lineHeight: 1.25
  body-md:
    fontFamily: Helvetica Neue
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: Helvetica Neue
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Helvetica Neue
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.08em
rounded:
  sm: 2px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
  gutter: 24px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 12px 28px
  button-primary-hover:
    backgroundColor: "{colors.ink}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 11px 27px
  button-text:
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
  chip:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

Swiss Style (the International Typographic Style) is a design language built on the grid
system, rational typography, and objective information hierarchy. The UI conveys clarity
and engineering precision: every element earns its place through function, not decoration.
A single signal red (`#E30613`) drives all interaction; everything else is grayscale logic.

Target audience: information products, data analytics platforms, professional tools, and
B2B services where trust comes from clarity, not ornament. The product should feel like a
well-engineered instrument, not a styled surface.

## Colors

The palette is high-contrast grayscale anchored by a single signal red.

- **Primary (#E30613):** The iconic Swiss red. Reserved for primary CTAs, active states,
  and critical data emphasis. Used sparingly — its power is scarcity. On white it achieves
  ~4.9:1 contrast; never place red text on the `neutral` (#F2F2F2) background (drops to
  ~4.4:1, below AA).
- **Ink (#000000):** Pure black for headlines, primary text, and secondary button text.
  Provides maximum contrast (21:1 on white) and a sense of permanence.
- **Ink-muted (#666666):** Slate gray for captions, metadata, and chip text. Achieves 5.7:1
  on white and 5.2:1 on `neutral` — passes AA for body text.
- **Surface (#FFFFFF):** Pure white for cards, inputs, and elevated containers. Maintains
  tonal separation from the neutral page background.
- **Neutral (#F2F2F2):** A light gray foundation for the page background. Softer than white;
  separates content zones tonally without decoration.
- **Divider (#CCCCCC):** For 1px borders and separating rules. Decorative only — never used
  for text (1.6:1 on white).

## Typography

Helvetica Neue carries the entire system — its neutrality is the point. Hierarchy comes
from size and weight, not typeface variation.

- **Headlines:** Tight negative tracking at large sizes mimics the density of Swiss print.
  Display uses Bold (700); section headers step down to Medium (500). Never scale
  `headline-display` below 768px without dropping to `headline-lg`.
- **Body:** Regular (400) at 16px with a 1.55 line-height for sustained reading. Do not go
  below 16px for body copy.
- **Labels:** Medium (500) at 12px, wide tracking (0.08em), rendered ALL CAPS — reserved
  for metadata, tags, and UI controls. The visual separation between prose and metadata is
  core to the Swiss identity; do not apply `label-caps` to paragraph text.

## Layout

The layout follows a strict **12-column Grid** (max-width 1280px, centered) with an 8px
base spacing unit.

Grid alignment is non-negotiable: every element snaps to column boundaries and the 8px
rhythm. Section separators use `xl` (64px) to create breathing room; intra-component
padding uses `md` (16px). The `gutter` token (24px) governs the gap between columns.

Mobile breakpoint: collapse to a 4-column grid. Maintain `md` (16px) as the minimum
padding at all screen sizes. The grid is the structure — never break alignment for
decorative effect.

## Elevation & Depth

Depth is conveyed through **Tonal Layers and 1px Rules**, never drop shadows.

1. Neutral background (`#F2F2F2`) — base layer
2. White surface (`#FFFFFF`) — content cards and inputs
3. Ink (`#000000`) — text and interactive overlays

If a component needs separation, use a 1px `#CCCCCC` border. `box-shadow` is
prohibited — the visual language must remain flat, print-like, and objective.

## Shapes

The shape language is defined by **Engineered Sharpness**. Corner radii are minimal: `sm`
(2px) for interactive elements and containers — just enough to avoid pixel-rendering
harshness, no more.

The `full` (9999px) radius is reserved exclusively for chips and tags — small, pill-shaped
elements where rounded edges signal selectability. Never apply `full` to buttons or cards;
roundness softens the engineered aesthetic and breaks the Swiss character.

## Components

**Buttons:** Primary buttons use signal red (`#E30613`) with white text — the only red
fill in the system. On hover, the fill shifts to `ink` (`#000000`). Secondary buttons use a
white `surface` fill with a 1px `#CCCCCC` border (via CSS) and `ink` text. Text links use
`primary` red. All buttons use `label-caps` typography to reinforce the utilitarian,
label-like character.

**Chips:** `neutral` (#F2F2F2) background with `ink-muted` (#666666) text and `full` radius.
Used for filters and metadata tags. The pill shape distinguishes them from the sharp-edged
buttons.

**Input fields:** White `surface`, 2px radius, 1px `#CCCCCC` border by default.
On focus, the border promotes to `primary` (red) — the single signal that an input is
active. Placeholders use `ink-muted`.

## Do's and Don'ts

- **Do** reserve red (`#E30613`) for one primary CTA per screen view — scarcity is its power.
- **Don't** use drop shadows; tonal layers and 1px `#CCCCCC` borders carry all depth.
- **Do** snap every element to the 8px grid and 12-column structure.
- **Don't** place red text on the `neutral` (#F2F2F2) background — contrast drops below 4.5:1.
- **Do** render `label-caps` in ALL CAPS via `text-transform: uppercase`.
- **Don't** apply `full` radius to buttons or cards — chips and tags only.
- **Do** maintain WCAG AA contrast (≥ 4.5:1) for all body text on all backgrounds.
- **Don't** introduce decorative typefaces — Helvetica Neue is the entire system.
