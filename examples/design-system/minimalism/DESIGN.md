---
version: alpha
name: Minimalism
description: A whitespace-driven interface where restraint is the brand signal and a single blue accent carries every interaction.
colors:
  primary: "#212121"
  secondary: "#9D9D9D"
  tertiary: "#2563EB"
  neutral: "#F5F5F5"
  surface: "#FFFFFF"
  on-surface: "#212121"
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
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
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.04em
rounded:
  sm: 4px
  md: 8px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
  4xl: 64px
  gutter: 24px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "{colors.tertiary}"
  button-secondary:
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 11px 23px
  button-text:
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    padding: 4px 8px
  chip:
    backgroundColor: "{colors.neutral}"
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
    textColor: "{colors.primary}"
---

## Overview

Minimalism is the art of subtraction — when every decoration is stripped away, what remains is the information itself. The visual language relies on whitespace, typography, and subtle details to deliver clear information hierarchy and a focused user experience. The result is elegant, pure, and efficient: less is more, because "more" dilutes focus.

Target audience: tool-oriented professionals — developers, operators, data analysts — who need to be respected, not entertained. Every screen carries at most one blue call-to-action, because restraint is the personality of this style, not a cost-saving measure. The emotional tone is calm, professional, and credible — like opening a well-typeset technical document rather than loading an app.

## Colors

The palette is high-contrast neutrals anchored by a single accent. Neutrals carry 99% of the visual load; blue appears only at points of interaction.

- **Primary (#212121):** Near-black ink for all headlines and body text, and the fill color of primary buttons. Provides maximum readability and a sense of permanence. Never used as a large-area background — dark backgrounds crush the whitespace that gives minimalism its breath.
- **Secondary (#9D9D9D):** Medium gray for all supporting roles — secondary text, placeholders, dividers, borders, metadata. Never used for body copy (contrast falls below 4.5:1); its entire purpose is to recede behind the content.
- **Tertiary (#2563EB):** The sole accent color, reserved exclusively for CTAs, text links, and focus rings. At most one per screen — scarcity is its power. Not used as a background fill (except on hover), and never used for error states to avoid confusion with interactive CTAs.
- **Neutral (#F5F5F5):** Page background. Softer than pure white, giving the product a subtle paper-like tactility. Not used for cards — cards must use surface white to maintain tonal separation from the background.
- **Surface (#FFFFFF):** Pure white for cards, modals, and inputs — elevated containers that need to stand apart from the neutral base.
- **On-surface (#212121):** Text color atop surfaces. Semantically distinct from primary (it describes "where text lands" rather than "the brand color"), allowing independent replacement in a future dark mode.

## Typography

The strategy is a **single typeface — Inter** — with SF Pro Display as the automatic fallback on macOS. Minimalism is subtraction; introducing a second family adds visual noise without earning its place. Inter's five weights (Light / Regular / Medium / Semibold / Bold) are sufficient to build a complete hierarchy. Weight selection follows "less is more": no more than two weights per screen.

- **headline-lg (48px / Semibold):** Negative tracking of `-0.02em` mimics the compact density of print headlines. Used for page-level titles. Below 768px screens, must scale down to `headline-md` — otherwise the visual pressure is overwhelming.
- **headline-md (32px / Semibold):** Sub-headings and section titles. Light negative tracking `-0.01em` keeps it compact without being tight.
- **body-md (16px / Regular):** Body copy with a 1.6 line-height for long-form readability. **Never go below 16px** — minimalism is not about making text smaller, but about giving every size a reason to exist.
- **body-sm (14px / Regular):** Supporting text, table cells, card subtext. Not for primary paragraphs.
- **label-sm (12px / Medium):** Buttons, tags, and metadata only. Must be paired with `text-transform: uppercase` and `0.04em` letter-spacing — this all-caps + wide-tracking treatment is the identity mark of minimalism, visually separating functional text from reading text.

## Layout

The layout is built on a **12-column grid** with an 8px base unit. The spacing scale — 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 — is entirely multiples of 4, ensuring any combination aligns to the same rhythm.

Containers max out at 1200px, centered, to prevent reading line-widths from spiraling on wide screens. Cards use 24px internal padding (`gutter`). Sections are separated by `4xl` (64px) whitespace to create breathing room — here, whitespace *is* hierarchy, not emptiness. Information density is communicated through the rhythm of spacing, not through stacked cards.

Do not nest more than two levels of containment. Minimalism relies on whitespace to establish hierarchy, not on boxes within boxes. On mobile, collapse to a single-column fluid grid and maintain a minimum padding of 16px (`lg`) — spacing should never drop below this floor at any screen size.

## Elevation & Depth

Depth is conveyed through **tonal layering**, never drop shadows. The three-layer structure is fixed:

1. Neutral background (`#F5F5F5`) — base layer
2. Surface white cards (`#FFFFFF`) — content panels
3. Primary ink (`#212121`) — text and interactive overlays

**Do not use `box-shadow` for elevation.** Shadows make flat surfaces feel ornamental, betraying the print-like restraint of minimalism. When separation is needed, use a 1px border in the secondary color (`#9D9D9D`) — this is a CSS-layer implementation detail, not defined in the token schema. This constraint keeps the entire visual language flat, restrained, and document-like.

## Shapes

The corner-radius philosophy is **restraint**. Interactive elements and containers default to `sm` (4px) — just enough to depart from sharpness while preserving an engineered, architectural character.

The `full` radius (9999px) is reserved exclusively for chips and tags — small, pill-shaped elements where rounding signals selectability. Never apply `full` to buttons or cards; oversized rounding softens the professional, tool-like character and pushes it toward "friendly consumer product" territory. The choice of radius is itself a declaration of identity: 4px says "I am a tool."

## Components

**Buttons:** Primary uses deep ink fill with white text (`surface`). On hover, the background shifts to `tertiary` blue — the only sanctioned hover color in the system. Secondary buttons are transparent with a 1px `secondary` border and no fill. Text buttons are transparent with `primary` text and no border — used for tertiary actions and inline links. All three use `label-sm` typography (all-caps + wide tracking) to reinforce the utilitarian character. Button width should not exceed 200px unless spanning a full column.

**Chips:** `neutral` background with `primary` text and `full` radius. Used for filter tags and selection states. The pill shape visually distinguishes them from buttons — buttons are actions, chips are states.

**Inputs:** Minimal — `surface` white background with `sm` radius. Default border is a 1px `secondary` stroke (CSS-layer detail, not in the token schema). On focus, the border promotes to `tertiary` blue while text color stays `primary`. Error states use a CSS red — never `tertiary`, to avoid conflating form errors with CTAs.

## Do's and Don'ts

- **Do** keep at most one `tertiary` CTA per screen view — its guiding power depends on scarcity.
- **Don't** use `box-shadow` for depth; use tonal separation (neutral → surface → primary) and 1px `secondary` borders.
- **Do** render all `label-sm` text in ALL CAPS via `text-transform: uppercase` — this is minimalism's identity mark.
- **Don't** use `headline-lg` (48px) on screens narrower than 768px; scale down to `headline-md` (32px).
- **Do** maintain WCAG AA contrast (minimum 4.5:1) for all body text — `primary` on `surface` is ~16:1, `primary` on `neutral` is ~14:1.
- **Don't** use `secondary` (#9D9D9D) for body text — at ~2.6:1 contrast it is restricted to supporting text and borders only.
- **Do** use `neutral` (#F5F5F5) as the page background, not pure white — pure white leaves cards without a tonal anchor.
- **Don't** mix more than two font weights on a single screen — weight is a hierarchy tool, not decoration.
