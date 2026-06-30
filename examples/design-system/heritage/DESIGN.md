---
version: alpha
name: Heritage
description: An editorial product with architectural minimalism and journalistic gravitas.
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FFFFFF"
  on-surface: "#1A1C1E"
typography:
  headline-display:
    fontFamily: Public Sans
    fontSize: 64px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Public Sans
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
rounded:
  sm: 4px
  md: 8px
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
    textColor: "{colors.neutral}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 12px 28px
  button-primary-hover:
    backgroundColor: "{colors.tertiary}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 11px 27px
  chip:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.secondary}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

Architectural Minimalism meets Journalistic Gravitas. The UI evokes a premium matte finish —
a high-end broadsheet or contemporary gallery catalog. Every layout decision prioritizes
reading clarity over decoration. Interactive elements are restrained: a single earthy red
accent does all the heavy lifting for calls to action.

Target audience: sophisticated readers and professionals who associate visual restraint with
credibility. The product should feel like opening a well-designed magazine, not loading an
app.

## Colors

The palette is rooted in high-contrast neutrals anchored by a single, evocative accent.

- **Primary (#1A1C1E):** A deep ink for headlines and core text. Provides maximum readability
  and a sense of permanence. Use for all primary text, primary buttons, and outlines.
- **Secondary (#6C7278):** A sophisticated slate for utilitarian elements — borders, captions,
  placeholder text, and metadata. Never use as a background fill; it exists purely in
  supporting roles.
- **Tertiary (#B8422E):** An earthy brick red as the sole driver of interaction. Used
  exclusively for primary CTAs, hover states, and critical highlights. Do not use tertiary
  for more than one element per screen — its power comes from scarcity.
- **Neutral (#F7F5F2):** A warm limestone that serves as the foundation for all pages.
  Softer than pure white; gives the product a tactile, paper-like feel.
- **Surface (#FFFFFF):** Pure white for cards, modals, and elevated containers to maintain
  the tonal separation from the neutral background.

## Typography

The strategy leverages two typefaces with distinct characters: **Public Sans** carries the
editorial voice; **Space Grotesk** handles all technical and metadata roles.

- **Display & Headlines:** Public Sans at varying weights establishes visual hierarchy.
  Large sizes use tight negative tracking (`-0.03em`) to achieve the density of a print
  headline. Never use `headline-display` at small screen widths without scaling down.
- **Body:** Public Sans Regular at 16px with a generous line-height (1.6) ensures
  long-form readability. Do not go below 16px for body copy.
- **Labels:** Space Grotesk is reserved exclusively for timestamps, tags, metadata, and
  UI labels. It is always rendered in ALL CAPS with wide letter-spacing (`0.1em`). This
  visual separation between prose and metadata is a core identity element — do not
  apply `label-caps` to paragraph text.

## Layout

The layout follows a **Fixed-Max-Width Grid** (max-width: 1200px, centered) with a
strict 8px spacing scale.

Cards use 24px internal padding (`gutter`). Section separators use `xl` spacing (64px)
to create breathing room between content blocks. Avoid nesting more than two levels of
containment — the design language relies on white space to establish hierarchy, not
layering.

Mobile breakpoint: collapse to a single-column fluid grid. Maintain the 16px base spacing
unit (`md`) as the minimum padding at all screen sizes.

## Elevation & Depth

Depth is conveyed through **Tonal Layers**, not drop shadows. The hierarchy is:

1. Neutral background (`#F7F5F2`) — base layer
2. White surface (`#FFFFFF`) — content cards and panels
3. Primary ink (`#1A1C1E`) — text and interactive overlays

Do not use `box-shadow` for elevation. If depth must be communicated in a component,
use a 1px `border` in the secondary color (`#6C7278`) rather than a shadow. This keeps
the visual language flat and print-like.

## Shapes

The shape language is defined by **Architectural Sharpness**. All interactive elements
and containers use the `sm` radius (4px) by default. This provides just enough softness
to feel modern while maintaining a rigid, engineered aesthetic.

The `full` radius (9999px) is reserved exclusively for chips and tags — small,
pill-shaped elements where rounded edges signal selectability. Never apply `full` to
buttons or cards.

## Components

**Buttons:** Primary buttons use deep ink background with neutral text. On hover, the
background shifts to tertiary (earthy red) — the only sanctioned hover color. Secondary
buttons are outlined with no fill. Both use `label-caps` typography to reinforce the
utilitarian character. Buttons should never exceed 200px width unless spanning a full
column.

**Chips:** Neutral background with secondary text and border. Used for filter tags and
selection states. The pill shape (full radius) distinguishes them visually from buttons.

**Input fields:** Minimal — white background, subtle `sm` radius. Borders are a CSS-layer
detail (the token schema defines no border property), implemented as a 1px secondary stroke
by default. On focus, the border promotes to primary color. Error state uses a CSS-red; no
`tertiary` in form errors to avoid confusion with interactive CTAs.

## Do's and Don'ts

- **Do** use `tertiary` for exactly one CTA per screen view — its impact depends on scarcity.
- **Don't** add drop shadows; use tonal separation and 1px borders instead.
- **Do** render all `label-caps` text in ALL CAPS via `text-transform: uppercase`.
- **Don't** use `headline-display` (64px) on screens narrower than 768px — scale to `headline-lg`.
- **Do** maintain WCAG AA contrast (minimum 4.5:1) for all body text on all backgrounds.
- **Don't** mix `sm` and `full` corner radii within a single component group.
- **Do** use `neutral` (#F7F5F2) as the page background, not pure white.
- **Don't** use more than two font weights on a single screen.
