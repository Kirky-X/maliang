---
version: alpha
name: Skeuomorphism
description: A tactile interface that borrows real-world materials — leather, paper, wood, glass — to make digital affordances feel familiar and trustworthy.
colors:
  primary: "#2E1E15"
  secondary: "#8B6B4D"
  tertiary: "#D4A574"
  neutral: "#F5F0E6"
  surface: "#E8D5B7"
  on-surface: "#2E1E15"
  leather: "#5A3E2B"
  wood: "#C9B99C"
  glass: "#A7C7E7"
typography:
  headline-lg:
    fontFamily: Georgia
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: Georgia
    fontSize: 32px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body-md:
    fontFamily: Helvetica
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Helvetica
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-sm:
    fontFamily: Helvetica
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.04em
rounded:
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  gutter: 20px
components:
  button-primary:
    backgroundColor: "{colors.leather}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
  button-secondary:
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 11px 23px
  chip:
    backgroundColor: "{colors.wood}"
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
    textColor: "{colors.tertiary}"
  switch:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 12px
---

## Overview

Skeuomorphism is the design philosophy of borrowing from the physical world. By simulating real materials — leather, wood, paper, glass — and their textures, lighting, and physical interactions, the interface lets users understand functionality through familiar visual metaphors. This lowers the learning curve, builds trust through tactile authenticity, and creates an immersive experience that resonates emotionally.

Target audience: broad user groups who benefit from real-world metaphors, including automotive and industrial contexts where physical affordances make complex operations intuitive, gaming and entertainment applications where immersion is paramount, and cultural or luxury brands where craftsmanship and heritage must be conveyed through material quality. The emotional tone is warm, substantial, and crafted — like holding a well-made physical object.

## Colors

The palette is a warm, earthy spectrum drawn from natural materials. Every color maps to a physical substance, giving the interface a tangible, crafted quality.

- **Primary (#2E1E15):** The darkest brown — near-black with warmth. Used for all body text and headlines, providing readability with a softer edge than pure black. Also the hover state for primary buttons, deepening the leather to its richest tone.
- **Secondary (#8B6B4D):** A medium saddle brown for supporting roles — borders, captions, metadata, and placeholder text. Its warmth keeps utilitarian elements from feeling cold or clinical. Never used for body copy; contrast is insufficient for extended reading.
- **Tertiary (#D4A574):** A warm gold accent — the patina of aged brass. Used sparingly for highlights, focus states, and interactive emphasis. Its material warmth distinguishes it from the flat blues of digital UIs; it signals "this is crafted, not computed."
- **Neutral (#F5F0E6):** The lightest warm tone — aged paper. Serves as the page background, giving the product a parchment-like foundation. Softer and warmer than white; never used for cards, which need the surface tone to separate from the base.
- **Surface (#E8D5B7):** A light warm tone — aged parchment or light wood. Used for cards, inputs, and elevated containers. Its tonal difference from `neutral` creates depth without shadows, evoking layers of stacked paper.
- **On-surface (#2E1E15):** Text color atop surfaces. Shares the value of `primary` but is semantically independent, describing "text resting on a material surface" rather than "the brand ink."
- **Leather (#5A3E2B):** A deep, rich brown — the color of oiled leather. Used exclusively as the fill for primary buttons, where the material metaphor is strongest. On hover, deepens to `primary` for a "pressed leather" effect.
- **Wood (#C9B99C):** A mid-tone warm gray-brown — light wood or aged brass. Used for chips and tags, where its material warmth distinguishes them from flat digital pills. Also suitable for dividers and secondary borders.
- **Glass (#A7C7E7):** A cool, translucent blue — frosted glass. Used for switch toggles in their "on" state, evoking a glass knob sliding into position. The cool tone provides the only chromatic contrast in an otherwise warm palette, drawing the eye to active toggle states.

## Typography

The strategy pairs **Georgia** (a serif) for headlines with **Helvetica** (a sans-serif) for body and UI text. This dual-family approach mirrors the editorial tradition where serif typefaces carry gravitas and sans-serifs handle utility — a convention that reinforces the material, crafted character of skeuomorphism.

- **headline-lg (48px / Bold):** Georgia at bold weight with `-0.02em` tracking delivers the density and authority of a leather-bound book title. Used for page-level headlines. The serif letterforms add the texture that sans-serifs cannot — each terminal and bracket contributes to the crafted feel.
- **headline-md (32px / Medium):** Georgia at medium weight for section titles. Lighter tracking `-0.01em` maintains compactness while allowing the serifs to breathe.
- **body-md (16px / Regular):** Helvetica Regular at 16px with 1.6 line-height for body copy. The neutrality of Helvetica lets the content speak while the surrounding materials carry the personality. Never below 16px — readability is non-negotiable.
- **body-sm (14px / Regular):** Helvetica for supporting text, table cells, and card subtext. Not for primary paragraphs.
- **label-sm (12px / Medium):** Helvetica Medium for buttons, tags, and metadata. Paired with `0.04em` letter-spacing and `text-transform: uppercase` to create a "engraved label" effect — reminiscent of embossed text on leather goods.

## Layout

The layout follows a **12-column grid** with a 20px gutter (`gutter`), evoking the proportions of a printed catalogue. The spacing scale — 4 / 8 / 16 / 24 / 32 / 48 — provides enough steps to layer materials without crowding.

Containers max out at 1200px, centered. Cards use 24px internal padding (`lg`) to give content room to breathe within its material frame. Sections are separated by `2xl` (48px) whitespace — more generous than flat designs, because skeuomorphic elements carry visual weight that requires surrounding space to avoid feeling cluttered.

Avoid nesting more than two levels of containment. Each layer of material should be visually distinct (leather → paper → wood), not stacked arbitrarily. On mobile, collapse to a single column and maintain a minimum padding of 16px (`md`).

## Elevation & Depth

Depth in skeuomorphism is conveyed through **material layering and subtle inner shadows**, not flat tonal shifts. The hierarchy evokes physical objects resting on surfaces:

1. Neutral background (`#F5F0E6`) — the desk or table surface
2. Surface cards (`#E8D5B7`) — paper or parchment laid atop the desk
3. Leather and wood elements — physical objects resting on the paper

Unlike flat design, skeuomorphism *does* use `box-shadow`, but sparingly and with intention: a soft, low-offset shadow beneath cards suggests they are physically resting on the surface; an inner highlight along the top edge of buttons suggests a raised, tactile surface. These shadows should be subtle (low opacity, small blur) — the goal is suggestion, not realism. Heavy drop shadows are a sign of amateur skeuomorphism and should be avoided.

For switches and toggles, the "on" state uses the `glass` color with a subtle inset shadow to suggest a recessed track, while the knob itself appears raised. This physical metaphor makes the toggle state immediately legible.

## Shapes

The shape language is defined by **material-appropriate rounding**. Unlike minimalism's architectural sharpness, skeuomorphic elements have the softer edges of physical objects.

- `sm` (4px): Used for inputs and text fields — the slight rounding of a stamped or cut paper edge.
- `md` (8px): Used for buttons — the rounded corner of a leather button or wooden tile, substantial enough to feel tactile without losing structure.
- `lg` (16px): Reserved for larger containers and cards where more pronounced rounding evokes the curvature of a physical object.
- `full` (9999px): Used exclusively for chips, tags, and switches — pill-shaped elements that mimic physical components like toggles and label badges.

Never mix `sm` and `lg` within the same component group — the inconsistency breaks the material illusion.

## Components

**Buttons:** Primary buttons use `leather` fill with `neutral` text — the metaphor of a dark leather button with light embossed text. On hover, the fill deepens to `primary` (the richest leather tone). Secondary buttons are transparent with a `primary` text and a 1px `secondary` border, evoking an engraved outline. Both use `label-sm` typography in all-caps to simulate embossed or engraved labels. The `md` radius gives buttons a tactile, slightly rounded edge.

**Chips:** `wood` background with `primary` text and `full` radius. The warm wood tone distinguishes them from buttons, and the pill shape signals selectability. Used for filter tags and selection states.

**Inputs:** `surface` background (parchment) with `primary` text and `sm` radius. The default border is a 1px `secondary` stroke, suggesting the recessed edge of an inset panel. On focus, the text color shifts to `tertiary` (warm gold), and the border may gain a subtle inner glow — the metaphor of light catching a brass frame. Error states use a muted red, never `tertiary`.

**Switches:** The toggle track uses `glass` (frosted blue) in the "on" state, with `primary` text. The `full` radius and the cool blue tone against the warm palette create a clear "active" signal — like a glass indicator light turning on. In the "off" state, the track reverts to `neutral` or `wood`, and the knob rests in a recessed position.

## Do's and Don'ts

- **Do** map every color to a physical material — if a color doesn't evoke leather, wood, paper, or glass, it doesn't belong in this palette.
- **Don't** over-skeuomorph — excessive texture and ornamentation creates visual noise and cognitive load. The goal is suggestion, not photorealism.
- **Do** use subtle shadows (low opacity, small blur) to suggest physical layering — cards resting on surfaces, raised buttons.
- **Don't** use heavy drop shadows or excessive gradients — amateur skeuomorphism relies on them; crafted skeuomorphism implies depth through material and tone.
- **Do** pair Georgia (serif) for headlines with Helvetica (sans) for body — the editorial pairing reinforces the crafted, material character.
- **Don't** mix `sm` and `lg` radii within the same component group — inconsistent rounding breaks the material illusion.
- **Do** maintain WCAG AA contrast (minimum 4.5:1) — `primary` on `neutral` is ~12:1, `primary` on `surface` is ~11:1, `neutral` on `leather` is ~8.5:1.
- **Don't** use skeuomorphism for data-dense dashboards or performance-sensitive contexts — the material richness competes with information clarity and can impact rendering performance on low-end devices.
- **Do** ensure consistent availability across devices — skeuomorphic textures and shadows must degrade gracefully on screens where they cannot render faithfully.
