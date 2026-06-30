---
version: alpha
name: Cyberpunk
description: A dark, neon-lit interface where data takes visual form through glowing cyan, purple, and magenta on deep blue-black surfaces.
colors:
  primary: "#00F0FF"
  secondary: "#1D7AFE"
  tertiary: "#7A5CFF"
  accent: "#E040FF"
  danger: "#FF2D55"
  warning: "#FF9500"
  neutral: "#01012A"
  surface: "#13132C"
  elevated: "#1A2A4A"
  border: "#20354B"
  on-surface: "#00F0FF"
typography:
  headline-lg:
    fontFamily: Orbitron
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: Orbitron
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: Exo 2
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Exo 2
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-sm:
    fontFamily: Orbitron
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
rounded:
  sm: 2px
  md: 4px
  lg: 8px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  gutter: 24px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 12px 24px
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.secondary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 11px 23px
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    padding: 4px 8px
  chip:
    backgroundColor: "{colors.elevated}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 12px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 10px 14px
  input-focus:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.accent}"
  switch:
    backgroundColor: "{colors.border}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 12px
  badge-danger:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.danger}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 4px 8px
  badge-warning:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.warning}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 4px 8px
---

## Overview

Cyberpunk is the aesthetic of future technology — mechanical structures, data visualization, and systematic order constructed from neon and darkness. In this interface, data takes visual form: glowing cyan, purple, and magenta trace the contours of information across deep blue-black surfaces. The result is a world where the boundary between data and the future dissolves — make future visible.

Target audience: technology products, data visualization platforms, enterprise system backends, and creative portfolios. The users are engineers, analysts, and creators who see beauty in systems — dashboards, data flows, system health metrics — and expect an interface that treats data as a visual medium, not a spreadsheet. The emotional tone is electric, precise, and forward-looking — like reading telemetry from a machine that hasn't been built yet.

## Colors

The palette is a dual system: a deep, near-black blue spectrum for surfaces, and a vivid neon spectrum for interaction and data. Every neon color glows; every dark color recedes.

- **Primary (#00F0FF):** Cyan — the signature signal color. Used for primary text on dark surfaces, primary button fills, data line traces, and all "live" indicators. Its electric brightness against the dark base is the defining visual gesture of the style. High contrast on all dark surfaces (12:1+).
- **Secondary (#1D7AFE):** Electric blue — the secondary interaction color. Used for secondary button text and links where cyan would be too prominent. Cooler and deeper than `primary`; provides a second tier of interactive emphasis.
- **Tertiary (#7A5CFF):** Purple — used for data visualization accents, tertiary highlights, and gradient endpoints. Often paired with `primary` in neon gradients (cyan → purple) that define the cyberpunk visual signature.
- **Accent (#E040FF):** Magenta-pink — the sharpest neon in the palette. Used sparingly for focus states, special highlights, and critical data nodes. Its chromatic intensity demands attention; overuse causes visual fatigue. On focus, input text shifts to `accent` to signal active engagement.
- **Danger (#FF2D55):** Red — alerts, errors, and critical system states. Used in badge components for system warnings. Never confused with `accent` (magenta) because it carries an explicitly semantic, non-interactive meaning.
- **Warning (#FF9500):** Orange — cautionary states and non-critical alerts. Used in badge components alongside `danger` for a complete system-status vocabulary. Warm against the cool palette, making warnings immediately legible.
- **Neutral (#01012A):** The deepest blue-black — the void. Serves as the page background and the base for badges. Not pure black; the slight blue tint gives it depth and prevents the "flat void" of `#000000`. All neon colors achieve maximum contrast against this surface.
- **Surface (#13132C):** Dark blue-black for panels, inputs, and cards. One step lighter than `neutral`, creating tonal layering within the dark spectrum. The primary container color for interactive elements.
- **Elevated (#1A2A4A):** A lighter dark blue for elevated cards and chips. Creates a third tier of depth — `neutral` → `surface` → `elevated` — allowing information hierarchy through tonal graduation within the dark base.
- **Border (#20354B):** A muted blue-gray for borders, dividers, and the "off" state of switches. Defines structural edges without competing with neon content. Its neutrality makes it the ideal resting state for toggles.
- **On-surface (#00F0FF):** Text color atop surfaces. Shares the value of `primary` but is semantically independent, describing "text resting on a dark panel" rather than "the brand neon."

## Typography

The strategy pairs **Orbitron** — a geometric, futuristic display face — for headlines and labels with **Exo 2** — a highly legible sans-serif with subtle technical character — for body text. This dual-family approach separates "system voice" (Orbitron, all-caps, wide-tracked) from "human-readable content" (Exo 2, natural case, comfortable line-height).

- **headline-lg (48px / Bold):** Orbitron Bold with `-0.02em` tracking delivers the geometric density of a HUD display or terminal header. The letterforms themselves look engineered — each character feels machined, not written. Used for page-level titles and dashboard headers. Below 768px, scale down to `headline-md`.
- **headline-md (32px / Semibold):** Orbitron Semibold for section titles and panel headers. The lighter weight maintains the engineered feel without overpowering surrounding content.
- **body-md (16px / Regular):** Exo 2 Regular at 16px with 1.6 line-height for body copy and data descriptions. Exo 2's subtle technical character (slightly squared letterforms) keeps it on-theme without sacrificing readability. Never below 16px — data must be legible.
- **body-sm (14px / Regular):** Exo 2 for supporting text, table cells, and metadata. Not for primary paragraphs.
- **label-sm (12px / Medium):** Orbitron Medium for buttons, tags, system labels, and all metadata. Paired with `0.1em` letter-spacing and `text-transform: uppercase` — this wide-tracked all-caps treatment is the voice of the machine, visually separating system labels from human-readable prose. The widest tracking in any style; it makes every label feel like it was stamped by a terminal.

## Layout

The layout follows a **12-column grid** with a 24px gutter (`gutter`), optimized for data-dense dashboards and multi-panel interfaces. The spacing scale — 4 / 8 / 16 / 24 / 32 / 48 — provides enough steps to separate data panels without wasting screen real estate.

Containers max out at 1440px, centered — wider than most styles because cyberpunk interfaces favor multi-column dashboards over single-column reading. Panels and cards use 16px internal padding (`md`) to maximize data density while maintaining separation. Sections are separated by `2xl` (48px) whitespace, but panels within a section can be as close as `lg` (24px) — the neon borders and glowing edges provide visual separation that reduces the need for whitespace.

On mobile, collapse to a single-column stack and maintain a minimum padding of 16px (`md`). Data visualizations should degrade gracefully — charts and graphs that cannot fit should collapse to summary stats, not scale down illegibly.

## Elevation & Depth

Depth in cyberpunk is conveyed through **neon glow and tonal graduation within the dark spectrum**, not traditional drop shadows. The hierarchy is:

1. Neutral background (`#01012A`) — the void, deepest layer
2. Surface panels (`#13132C`) — dark blue-black containers, one step lighter
3. Elevated cards (`#1A2A4A`) — raised panels, a third tier of depth

**Neon glow replaces shadow.** Where flat design uses borders and minimalism uses tonal separation, cyberpunk uses `box-shadow` with neon-colored, blurred glow to indicate active or interactive elements. A primary button glows cyan (`0 0 12px rgba(0, 240, 255, 0.4)`); a focused input glows magenta (`0 0 8px rgba(224, 64, 255, 0.3)`). This glow is the cyberpunk equivalent of elevation — it signals "this element is live."

Inactive elements rely on the tonal graduation (`neutral` → `surface` → `elevated`) and 1px `border` (`#20354B`) strokes for separation. Do not apply glow to inactive elements — glow is reserved for active, focused, or critical states. Overuse of glow flattens the hierarchy and causes visual fatigue.

## Shapes

The shape language is defined by **mechanical precision and sharp angles**. Cyberpunk interfaces evoke engineered, machined surfaces — not organic curves.

- `sm` (2px): The default for buttons, inputs, and interactive elements — barely rounded, preserving the sharp, engineered aesthetic. This near-square corner is the cyberpunk signature.
- `md` (4px): For larger panels and cards where a slightly softer corner prevents the interface from feeling hostile. Still far sharper than most design systems.
- `lg` (8px): Reserved for large containers and modals where more rounding improves approachability without abandoning the mechanical character.
- `full` (9999px): Used exclusively for chips, tags, and switches — pill-shaped elements that contrast sharply with the otherwise angular interface. The pill shape signals "status" or "toggle," distinct from the rectangular "action" elements.

Never use large radii on buttons or panels — the sharpness is load-bearing. A 16px radius on a cyberpunk button makes it look like a consumer app, not a system interface.

## Components

**Buttons:** Primary buttons use `primary` (cyan) fill with `neutral` (deep blue-black) text — a glowing cyan button with dark text, evoking a lit switch or active terminal command. The cyan fill should carry a subtle glow. Secondary buttons are transparent with `secondary` (blue) text and a 1px `border` stroke — the "standby" state. Ghost buttons are transparent with `primary` text and no border — for tertiary actions and inline commands. All use `label-sm` typography (Orbitron, all-caps, wide-tracked) — the voice of the system, not the user.

**Chips:** `elevated` background with `primary` text and `full` radius. Used for status tags, data labels, and filter states. The pill shape against the angular panels creates a clear visual distinction — chips are metadata, not actions.

**Inputs:** `surface` background with `primary` text and `sm` radius. Placeholder text uses a dimmed neon. On focus, the text color shifts to `accent` (magenta) and the input gains a magenta glow (`box-shadow: 0 0 8px rgba(224, 64, 255, 0.3)`) — the metaphor of a terminal accepting input. Error states use `danger` text with a red glow, never `accent`.

**Switches:** The toggle track uses `border` (muted blue-gray) in its resting state with `primary` text. When activated, the track could shift to `elevated` with a cyan glow on the knob. The `full` radius and the tonal shift between resting and active states make the toggle legible without relying on color alone.

**Badges:** `neutral` background with semantic text colors — `danger` (red) for errors and critical alerts, `warning` (orange) for cautions. Used for system-status indicators (e.g., "78% SYSTEM HEALTH"). The `sm` radius keeps them angular and technical. Never use `accent` (magenta) for badges — it is reserved for interactive focus states.

## Do's and Don'ts

- **Do** use neon glow (`box-shadow` with blurred neon color) to indicate active, focused, or interactive elements — glow is the cyberpunk equivalent of elevation.
- **Don't** apply glow to inactive or resting elements — overuse flattens the hierarchy and causes visual fatigue.
- **Do** maintain the dark spectrum (`neutral` → `surface` → `elevated`) as the foundation; neon colors are accents, not backgrounds.
- **Don't** use neon colors as large-area backgrounds — they cause eye strain and destroy the dark-base contrast that makes the style work.
- **Do** pair Orbitron (all-caps, wide-tracked) for labels with Exo 2 (natural case) for body — the system voice must be distinct from the human-readable voice.
- **Don't** use large radii on buttons or panels — sharpness is load-bearing; 2px says "engineered," 16px says "consumer."
- **Do** maintain WCAG AA contrast (minimum 4.5:1) — `primary` on `surface` is ~13:1, `primary` on `elevated` is ~10:1, `accent` on `surface` is ~5.5:1, `danger` on `neutral` is ~5.5:1.
- **Don't** confuse `accent` (magenta, interactive) with `danger` (red, semantic) — they serve different purposes and must not be interchanged.
- **Do** use data visualization as a first-class element — charts, graphs, and system metrics are not decoration; they are the content.
