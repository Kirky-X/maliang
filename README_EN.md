# Maliang (马良) — Design System Skill

[![GitHub Release](https://img.shields.io/github/v/release/Kirky-X/maliang?style=flat-square)](https://github.com/Kirky-X/maliang/releases)
[![GitHub License](https://img.shields.io/github/license/Kirky-X/maliang?style=flat-square)](LICENSE)

maliang is a design system skill for AI agents, using Google Labs agent-first format (YAML tokens + Markdown design rationale). It provides six subcommands forming a complete pipeline: `design-md` produces prose-first `DESIGN.md`, `draw-md` generates page-level hard-token UI markdown from `DESIGN.md`, `preview` renders real-time previews using Element Plus, and `draw-harmony` / `draw-flutter` / `draw-element` convert the logical UI markdown into framework-specific implementation code.

Pipeline flow: `design-md` (upstream) → `draw-md` (midstream) → `preview` (validation) → `draw-harmony` / `draw-flutter` / `draw-element` (downstream). See [SKILL.md](SKILL.md) for the full route table and process documentation.

## Installation

### Method 1: Via `skills` package (recommended)

Requires [Node.js](https://nodejs.org/) 18+ and the `skills` npm package (v1.5.12+). `skills` is the CLI for the open agent skills ecosystem, supporting 68+ agents (Claude Code / Trae / Cursor / Codex / OpenCode, etc.).

```bash
# Install to Claude Code
npx skills add https://github.com/Kirky-X/maliang.git --agent claude-code -y

# Equivalent shorthand (owner/repo)
npx skills add Kirky-X/maliang --agent claude-code -y

# Install to Trae
npx skills add Kirky-X/maliang --agent trae -y

# List all discoverable skills in this repo (no install)
npx skills add https://github.com/Kirky-X/maliang.git --list
```

After installation, skill files are located in the corresponding agent's skills directory (e.g. `.claude/skills/maliang/`).

### Method 2: Traditional git clone

```bash
git clone https://github.com/Kirky-X/maliang.git
# Link or copy SKILL.md + references/ + examples/ + scripts/ to the agent skills directory
# Skills directory paths for each runtime (choose one):
#   Claude Code:  ~/.claude/skills/maliang/
#   Trae:         ~/.trae-cn/skills/maliang/
#   Cursor:       ~/.cursor/skills/maliang/
#   Codex:        ~/.codex/skills/maliang/
```

## Usage

Once loaded as a skill by an agent, maliang is triggered by natural language intent — no explicit commands needed. See [SKILL.md route table](./SKILL.md) for detailed subcommand descriptions and intent routing.

| Subcommand | One-liner |
| ---------- | --------- |
| design-md | Produces prose-first DESIGN.md |
| draw-md | Generates page-level hard-token UI markdown |
| preview | Real-time preview with Element Plus |
| draw-harmony | Converts to HarmonyOS (ArkTS) |
| draw-flutter | Converts to Flutter |
| draw-element | Converts to Element Plus (Vue 3) |

## Capabilities

### `references/` — Subcommand flows + dimension specs + framework docs

Shared reference documents for all six subcommands:

| File | Dimension |
| ---- | --------- |
| [`design-md.md`](references/commands/design-md.md) | design-md subcommand flow (upstream) |
| [`draw-md.md`](references/commands/draw-md.md) | draw-md subcommand flow (midstream) |
| [`preview.md`](references/commands/preview.md) | preview subcommand flow (validation) |
| [`draw-harmony.md`](references/commands/draw-harmony.md) | draw-harmony subcommand flow (HarmonyOS) |
| [`draw-flutter.md`](references/commands/draw-flutter.md) | draw-flutter subcommand flow (Flutter) |
| [`draw-element.md`](references/commands/draw-element.md) | draw-element subcommand flow (Element) |
| [`philosophy.md`](references/meta/philosophy.md) | prose-first methodology |
| [`principles.md`](references/meta/principles.md) | Design principles (Do's and Don'ts) |
| [`token.md`](references/meta/token.md) | Token specification |
| [`spec-schema.md`](references/meta/spec-schema.md) | DESIGN.md schema and lint rules |
| [`color.md`](references/dimensions/color.md) | Color dimension |
| [`color-palettes.md`](references/dimensions/color-palettes.md) | Color palette dimension |
| [`font.md`](references/dimensions/font.md) | Typography dimension |
| [`icon.md`](references/dimensions/icon.md) | Icon dimension |
| [`spacing.md`](references/dimensions/spacing.md) | Spacing dimension |
| [`radius.md`](references/dimensions/radius.md) | Border radius dimension |
| [`border.md`](references/dimensions/border.md) | Border dimension |
| [`framework/index.md`](references/framework/index.md) | Framework resource index (component type index) |

### `references/framework/` — Layered framework document database

```
references/framework/
├── index.md                          # Framework resource index with component type index
├── harmony/                          # HarmonyOS (ArkTS)
│   ├── button/{component,usage}.md
│   ├── text/{component,usage}.md
│   └── list/{component,usage}.md
├── flutter/                          # Flutter (Dart)
│   ├── button/{widget,properties}.md
│   ├── text/{widget,properties}.md
│   └── list/{widget,properties}.md
└── element/                          # Element Plus (Vue 3)
    ├── button/{component,api}.md
    ├── text/{component,api}.md
    └── list/{component,api}.md
```

### `examples/` — 13 design system styles + UI markdown examples

```
examples/
├── design-system/              # DESIGN.md examples for 13 styles
│   ├── DESIGN.md               # Root example
│   ├── material-design/
│   ├── skeuomorphism/
│   ├── minimalism/
│   ├── cyberpunk/
│   ├── illustrative/
│   ├── swiss-style/
│   ├── glassmorphism/
│   ├── neomorphism/
│   ├── y2k/
│   ├── editorial/
│   ├── brutalism/
│   └── heritage/
└── ui-markdown/                # draw-md output examples
    ├── token.md                # Page token table
    ├── ui/
    │   ├── home.md             # Home page spec
    │   └── setting/about.md    # About page spec
    └── organisms/
        ├── nav-bar.md          # Navigation bar (cross-page reuse)
        └── dock.md             # Dock (cross-page reuse)
```

### `scripts/` — Helper scripts + device models

- [`design_md_to_token_md.py`](scripts/design_md_to_token_md.py) — Extract token table from DESIGN.md
- [`device_models.py`](scripts/device_models.py) — iOS/Android phone and tablet device size configuration (6 devices)
- [`devices/phone.html`](scripts/devices/phone.html) — Phone device shell HTML/CSS template (with notch)
- [`devices/tablet.html`](scripts/devices/tablet.html) — Tablet device shell HTML/CSS template (no notch)

#### Supported device sizes

| Device | Platform | Type | Size (W×H) |
| ------ | -------- | ---- | ----------- |
| iPhone 15 Pro Max | iOS | phone | 430×932 |
| iPhone 15 | iOS | phone | 393×852 |
| iPhone SE 3rd | iOS | phone | 375×667 |
| iPad Pro 12.9" | iOS | tablet | 1024×1366 |
| iPad Air | iOS | tablet | 820×1180 |
| Samsung Galaxy Tab S8 | Android | tablet | 1600×2560 |

## Full Pipeline

```
design-md ──► draw-md ──► preview ──► draw-harmony / draw-flutter / draw-element
(Design Sys) (Logic UI)  (Preview)    (Framework impl)
```

1. `design-md` outputs DESIGN.md (design system specification)
2. `draw-md` generates page-level UI markdown from DESIGN.md (logical UI)
3. `preview` validates the logical UI with Element Plus + device shells
4. `draw-harmony` / `draw-flutter` / `draw-element` convert logical UI to framework-specific code

## FAQ

### What version of the `skills` package is required?

Requires `skills` npm package **v1.5.12+** (tested with v1.5.14 on this repo). `skills` is the CLI for the [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) ecosystem, supporting 68+ agents. Use `npx skills@latest` to get the latest version automatically.

### Where did ui-md go?

The `ui-md` subcommand has been renamed to `draw-md` (v0.1.0) to align with the downstream `draw-harmony` / `draw-flutter` / `draw-element` naming convention. Functionality is identical — just replace `ui-md` with `draw-md` in your trigger phrases.

### Which URL formats are supported?

Tested (2026-06-30, `skills` v1.5.14) compatibility for four `npx skills add` URL formats:

| Command format | Compatible | Notes |
| -------------- | :--------: | ----- |
| `npx skills add https://github.com/Kirky-X/maliang.git` | ✓ | Full GitHub URL + .git suffix, recommended |
| `npx skills add https://github.com/Kirky-X/maliang` | ✓ | Full GitHub URL (no .git), auto-appends suffix |
| `npx skills add Kirky-X/maliang` | ✓ | owner/repo shorthand, auto-expands to full URL, recommended |
| `npx skills add Kirky-X/maliang.git` | ✗ | **Not supported** — skills package bug: generates `maliang.git.git` double suffix, clone fails. Use `Kirky-X/maliang` (no .git) or full URL |

**Conclusion**: Use the first three formats. Avoid the `owner/repo.git` shorthand (skills v1.5.14 has a double-suffix bug).

### Remote install says "No skills found"?

Make sure the GitHub repo `Kirky-X/maliang` has been pushed with the latest code containing `SKILL.md` (in the root directory with YAML frontmatter including `name` + `description`). The `skills` package clones the repo and scans for `SKILL.md` — an empty repo or missing `SKILL.md` will trigger this error.

### `skills add` says "Installation complete" but `.claude/skills/maliang/` doesn't exist?

This is a known issue with the `skills` package v1.5.14: the command reports success but doesn't actually copy the files. **Workaround**: manually copy the skill files to the agent skills directory (choose one for your runtime):

```bash
# Claude Code
mkdir -p ~/.claude/skills/maliang
cp -r SKILL.md skill.json references examples scripts ~/.claude/skills/maliang/

# Trae
mkdir -p ~/.trae-cn/skills/maliang
cp -r SKILL.md skill.json references examples scripts ~/.trae-cn/skills/maliang/

# Cursor
mkdir -p ~/.cursor/skills/maliang
cp -r SKILL.md skill.json references examples scripts ~/.cursor/skills/maliang/

# Codex
mkdir -p ~/.codex/skills/maliang
cp -r SKILL.md skill.json references examples scripts ~/.codex/skills/maliang/
```

## License

MIT
