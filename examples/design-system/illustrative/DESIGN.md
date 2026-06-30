---
version: alpha
name: Illustrative
description: A warm, story-driven system pairing hand-drawn illustration with vibrant, rounded geometry.
colors:
  primary: "#5C5CE7"
  secondary: "#FF8A56"
  accent-green: "#7ED56F"
  accent-cyan: "#4ECDC4"
  accent-yellow: "#FFD166"
  ink: "#2D3436"
  ink-muted: "#636E72"
  surface: "#FFFFFF"
  neutral: "#F7F9FA"
  surface-muted: "#DFE6E9"
typography:
  headline-display:
    fontFamily: Round Friendly
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Round Friendly
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Round Friendly
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.25
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.08em
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
  xl: 48px
  gutter: 20px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.md}"
    padding: 12px 28px
  button-primary-hover:
    backgroundColor: "{colors.ink}"
  button-secondary:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.ink}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.md}"
    padding: 11px 27px
  button-text:
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
  chip:
    backgroundColor: "{colors.accent-yellow}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  chip-success:
    backgroundColor: "{colors.accent-green}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  chip-info:
    backgroundColor: "{colors.accent-cyan}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  chip-secondary:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

Illustrative is a design language built on warmth, character, and story. Hand-drawn
illustrations, vibrant but disciplined color, and rounded geometry work together to make
products feel approachable and human. The UI does not just present information — it invites
the user in. MAKE DESIGN WARM, MAKE EXPERIENCE MEMORABLE.

Target audience: consumer-facing products that need emotional connection — apps for
learning, productivity, community, and lifestyle. The product should feel like a friendly
companion, not a tool.

**Illustration style:** flat-style character illustrations in diverse life scenes (work,
study, sport, leisure), rendered in vibrant color. The illustration palette mirrors the UI
palette — `primary` purple, `secondary` orange, `accent-green`, `accent-cyan`, and
`accent-yellow` — so drawings and interface read as one system. Illustrations appear in
empty states, onboarding, and hero moments; they never decorate around critical data.

## Colors

The palette pairs one decisive primary with a quartet of illustrative accents, grounded by
warm grays.

- **Primary (#5C5CE7):** A friendly purple. Drives primary CTAs, links, and focus rings.
  White-on-purple achieves 5.0:1 — safe for button text.
- **Secondary (#FF8A56):** Warm orange for illustration accents, secondary surfaces, and
  playful highlights. Not for body text on white (2.3:1 fails AA); use `ink` (#2D3436) text
  on orange fills (5.2:1 passes).
- **Accent-green (#7ED56F):** Success states and illustration foliage. Decorative only —
  never for text.
- **Accent-cyan (#4ECDC4):** Info states and illustration water/sky. Decorative; `ink` text
  on cyan passes (6.3:1).
- **Accent-yellow (#FFD166):** Chip and badge backgrounds, illustration warmth. `ink` text
  on yellow passes (8.5:1).
- **Ink (#2D3436):** Deep warm gray for all primary text (12.2:1 on white).
- **Ink-muted (#636E72):** Captions and metadata (5.2:1 on white, 5.0:1 on `neutral`).
- **Surface (#FFFFFF):** Pure white for cards and inputs.
- **Neutral (#F7F9FA):** Near-white page background — softer than pure white, gives the
  product a paper-like warmth.
- **Surface-muted (#DFE6E9):** Pale gray for secondary containers and `button-secondary`
  fills (9.6:1 with `ink` text).

## Typography

Two friendly typefaces: **Round Friendly** for display headlines (its rounded terminals
reinforce approachability), **Inter** for body and UI labels (its open counters preserve
readability).

- **Headlines:** Round Friendly Bold/Semibold at large sizes. Tight negative tracking at
  display sizes keeps headlines dense enough to feel intentional. Round Friendly is a
  display face only — never use it for body copy.
- **Body:** Inter Regular at 16px with a generous 1.6 line-height. The openness matches the
  friendly tone — never compress body line-height below 1.5, and never go below 16px for
  body copy.
- **Labels:** Inter Medium at 12px with 0.08em tracking. Used for tags, metadata, and
  button labels. ALL CAPS is optional — Illustrative is less rigid than editorial systems;
  sentence case is acceptable for warmth.

## Layout

The layout uses a **12-column Fluid Grid** (max-width 1200px) with an 8px base spacing
unit, but allows intentional asymmetry to feel less engineered.

Cards use 16px–24px internal padding (`md`–`lg`). Section separators use `xl` (48px) to
create breathing room. The `gutter` token (20px) governs the gap between columns.
Illustrations may break the grid at hero moments — they are the one sanctioned departure
from the column structure, used to inject personality without sacrificing readability.

Mobile breakpoint: collapse to a single column, illustrations scale to full width.
Maintain `md` (16px) as the minimum padding at all screen sizes.

## Elevation & Depth

Depth is conveyed through **Soft Tonal Layers and Gentle Shadows** — unlike flat systems,
Illustrative permits a single soft shadow on cards to lift them off the `neutral`
background.

1. Neutral background (`#F7F9FA`) — base layer
2. Surface (`#FFFFFF`) — cards and inputs, optionally with a soft shadow
3. Surface-muted (`#DFE6E9`) — inset or secondary containers

Shadow: `0 4px 12px rgba(45, 52, 54, 0.08)` — low-opacity, short-spread, warm. Never use
sharp or dark shadows; they break the friendly character. Only one shadow per component —
do not stack.

## Shapes

The shape language is defined by **Rounded Friendliness**. Default radius is `md` (12px)
for cards, inputs, and buttons. `sm` (8px) is used for small inline elements; `lg` (16px)
for prominent cards.

The `full` (9999px) radius is reserved for chips, badges, and avatar-shaped elements.
Rounded geometry is core to the identity — never use sharp 0px corners on primary
containers.

## Components

**Buttons:** Primary buttons use `primary` purple (#5C5CE7) with white text — the brand
voice. On hover, the fill shifts to `ink` (#2D3436) for a grounded press state. Secondary
buttons use `surface-muted` (#DFE6E9) with `ink` text. Text buttons use `primary` purple.
All buttons use `md` (12px) radius and `label-caps` typography.

**Chips:** Pill-shaped (`full` radius) tags for statuses and selection. The default chip
uses `accent-yellow` (#FFD166) with `ink` text. Variants map the palette to semantics:
`chip-success` (`accent-green`), `chip-info` (`accent-cyan`), and `chip-secondary`
(`neutral` bg with `ink-muted` text for muted tags). All use `label-caps` typography. The
pill shape and warm fills distinguish them from the rounded buttons.

**Input fields:** White `surface`, `md` (12px) radius, 1px `surface-muted` border by
default. On focus, the border promotes to `primary` (purple) — a warm signal of attention.
Placeholders use `ink-muted`.

## Do's and Don'ts

- **Do** use illustrations in empty states, onboarding, and hero moments — they are the
  heart of the system.
- **Don't** place `secondary` orange text on white — contrast fails (2.3:1); use `ink`
  instead.
- **Do** pair every accent color with `ink` (#2D3436) text or white text where contrast
  allows.
- **Don't** use sharp 0px corners on primary containers — rounded geometry is identity.
- **Do** keep illustrations aligned to the UI palette; off-palette art breaks the system.
- **Don't** apply heavy or dark shadows — only the single soft warm shadow is permitted.
- **Do** maintain WCAG AA contrast (≥ 4.5:1) for all body text on all backgrounds.
- **Don't** mix Round Friendly into body copy — it is a display face only.
