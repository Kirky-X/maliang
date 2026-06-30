---
version: alpha
name: Material Design
description: A cross-platform design language by Google built on material metaphors, meaningful motion, and shadow-based elevation.
colors:
  primary: "#6200EE"
  primary-light: "#7C4DFF"
  tertiary: "#BB86FC"
  secondary: "#03DAC6"
  background: "#FFFFFF"
  surface: "#FFFFFF"
  on-primary: "#FFFFFF"
  on-secondary: "#000000"
  on-surface: "#212121"
  outline: "#BDBDBD"
  error: "#B00020"
typography:
  headline-lg:
    fontFamily: Roboto
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.25
  headline-md:
    fontFamily: Roboto
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.33
  body-md:
    fontFamily: Roboto
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Roboto
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
  label:
    fontFamily: Roboto
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0.1em
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  xxxl: 48px
  huge: 64px
components:
  button-filled:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-filled-hover:
    backgroundColor: "{colors.primary-light}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-outlined:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 11px 23px
  button-text:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: 8px 12px
  fab:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 16px
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

Material Design is Google's design language built on material metaphors — surfaces, edges,
and shadows inspired by the physical world — combined with meaningful motion to deliver
consistent, intuitive, and predictable experiences across platforms. The UI is treated as
layered sheets of digital paper that can split, merge, and elevate in response to user
input, with light and shadow doing the work of indicating hierarchy.

Target audience: teams building cross-platform products (Android, Web, iOS), enterprise
back-office and management systems, and complex data applications where clear hierarchy,
predictable components, and accessibility are non-negotiable. Material Design is especially
suited to Android apps and multi-platform products that must feel native everywhere, and to
teams that prioritise accessibility standards.

## Colors

The palette pairs a deep purple `primary` with a vivid teal `secondary`, grounded by a
neutral grey scale.

- **primary (#6200EE):** Deep purple — the brand anchor. Used for filled buttons, active
  states, and key affordances. Paired with `on-primary` (#FFFFFF) for labels at 7.6:1
  contrast.
- **primary-light (#7C4DFF):** The lighter purple tonal companion, used for hover states
  on `primary` fills (see `button-filled-hover`).
- **tertiary (#BB86FC):** A pale purple accent from the source palette. Used for decorative
  highlights and selection states where `primary` would be too heavy.
- **secondary (#03DAC6):** Vivid teal used as a secondary accent — FAB fills and toggle
  highlights. Uses `on-secondary` (#000000) because the teal is light enough that black
  text passes AA at 11.9:1, while white text would fail.
- **background / surface (#FFFFFF):** Both default to pure white. `background` is the page
  canvas; `surface` is the card/sheet layer. Foreground text uses `on-surface` (#212121,
  near-black) at 16:1 contrast.
- **outline (#BDBDBD):** Hairline divider and outlined-button stroke. Decorative only —
  never used for body text.
- **error (#B00020):** Reserved exclusively for error states and form validation messaging.

## Typography

A single typeface — **Roboto** — carries the entire hierarchy through four weights (Light
300, Regular 400, Medium 500, Bold 700).

- **headline-lg (32px / 700):** Screen titles and hero text. Tight and confident.
- **headline-md (24px / 500):** Section headers and dialog titles.
- **body-md (16px / 400):** Primary body copy at 1.5 line-height for long-form readability.
  Never go below 16px for body.
- **body-sm (14px / 400):** Secondary copy, captions, and helper text.
- **label (12px / 500, 0.1em tracking):** Buttons, chips, tabs, and navigation. The wide
  tracking is a Material signature — apply it wherever text labels sit inside a control.

## Layout

A **12-column grid** structures every screen, with a base spacing unit of 4px. The spacing
scale — `xs` (4), `sm` (8), `md` (12), `lg` (16), `xl` (24), `xxl` (32), `xxxl` (48),
`huge` (64) — covers touch targets, gutters, and section rhythm.

- Minimum touch target: 48×48px (use `xxxl` spacing to guarantee clearance).
- Card padding: `lg` (16px) on mobile, `xl` (24px) on desktop.
- Section separation: `huge` (64px) between top-level sections; `xxl` (32px) within a section.
- Breakpoints: collapse the 12-column grid to a single column below 600px; expand gutters
  using `xl` at the lg breakpoint.

## Elevation & Depth

Depth is expressed through **shadow elevation**, not colour. Material surfaces occupy one
of five elevation levels (0dp → 24dp shadow). Higher elevation means higher priority and a
softer, more diffuse shadow.

Motion reinforces elevation: surfaces lift on press (an elevation transition), FABs expand
into sheets, and modals scale-in on a decelerating curve. All motion should feel natural
and meaningful — never decorative. A pressed card rises with a `lg` shadow; a dialog
arrives at `xxxl` elevation.

## Shapes

Material shape language uses four radii plus `none` to signal component type:

- **none (0):** Full-bleed images and dividers.
- **sm (4px):** Text fields, outlined buttons, and small cards — restrained and functional.
- **md (8px):** Filled buttons, dialogs, and medium cards — the default for most surfaces.
- **lg (16px):** Bottom sheets, large cards, and FAB-expanded sheets — softer, more prominent.
- **full (9999px):** FABs, chips, and avatars — pill/circle shapes that signal touchability.

Never mix `sm` and `full` within the same component group.

## Components

- **button-filled:** Solid `primary` background with an `on-primary` label. The default CTA.
  Uses `md` radius and `label` typography. On hover the background lifts to `primary-light`
  (`button-filled-hover`).
- **button-outlined:** White `background` fill, `primary` text, 1px `outline` stroke. For
  secondary actions that need less visual weight.
- **button-text:** White `background`, `primary` text, no stroke. Tertiary and in-flow
  actions (e.g. "Cancel" in a dialog).
- **fab:** Circular (`full` radius) `secondary`-filled button carrying `on-secondary`
  text/icon. Promotes the single primary screen action — only one FAB per screen.
- **input:** White `surface` with `on-surface` text, `sm` radius, outlined by default with
  `outline`. On focus the border promotes to `primary`. Helper text appears below in
  `body-sm`.
- **chip:** `surface` background, `on-surface` label, `full` radius. Used for filters and
  selection.

Icons follow the Outlined style at 24dp for consistency across the system.

## Do's and Don'ts

- **Do** keep one FAB per screen — its prominence depends on singularity.
- **Don't** use `secondary` teal for body text — it fails AA on white.
- **Do** apply `label` typography (0.1em tracking) to every in-control label.
- **Don't** mix radii within a component group — buttons stay `md`, chips stay `full`.
- **Do** maintain WCAG AA (≥4.5:1) — every `on-*` token is paired to pass.
- **Don't** use drop shadows for decoration — elevation is meaningful and tied to state.
- **Do** use `error` (#B00020) only for errors; never as a brand colour.
- **Don't** scale body copy below 16px (`body-md`).
