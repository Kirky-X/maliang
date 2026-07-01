# maliang (马良) —— 设计系统技能

maliang 是一个面向 AI agent 的设计系统 skill,采用 Google Labs agent-first 格式(YAML token + Markdown 设计理由)。它通过六个子命令构成一条完整流水线:`design-md` 产出 prose-first 的 `DESIGN.md`,`draw-md` 从 `DESIGN.md` 产出页面级硬 token UI markdown,`preview` 使用 Element Plus 框架实时预览验证,`draw-harmony` / `draw-flutter` / `draw-element` 将逻辑 UI markdown 转换为具体框架实现代码。

六个子命令构成完整流水线:`design-md`(上游)→ `draw-md`(中游)→ `preview`(验证)→ `draw-harmony` / `draw-flutter` / `draw-element`(下游)。各子命令的完整路由表与流程文档见 [SKILL.md](SKILL.md)。

## 安装

### 方式一:通过 `skills` 包安装(推荐)

需 [Node.js](https://nodejs.org/) 18+ 和 `skills` npm 包(v1.5.12+)。`skills` 是 open agent skills 生态的 CLI,支持 68+ agents(Claude Code / Trae / Cursor / Codex / OpenCode 等)。

```bash
# 安装到 Claude Code
npx skills add https://github.com/Kirky-X/maliang.git --agent claude-code -y

# 等价简写(owner/repo)
npx skills add Kirky-X/maliang --agent claude-code -y

# 安装到 Trae
npx skills add Kirky-X/maliang --agent trae -y

# 列出仓库中可被发现的所有 skills(不安装)
npx skills add https://github.com/Kirky-X/maliang.git --list
```

安装后 skill 文件位于对应 agent 的 skills 目录(如 `.claude/skills/maliang/`)。

### 方式二:传统 git clone

```bash
git clone https://github.com/Kirky-X/maliang.git
# 将 SKILL.md + references/ + examples/ + scripts/ 链接或复制到 agent skills 目录
# 各 runtime 的 skills 目录路径示例(任选其一):
#   Claude Code:  ~/.claude/skills/maliang/
#   Trae:         ~/.trae-cn/skills/maliang/
#   Cursor:       ~/.cursor/skills/maliang/
#   Codex:        ~/.codex/skills/maliang/
```

## 使用示例

maliang 作为 skill 被 agent 加载后,通过自然语言意图触发,无需显式命令。子命令详细描述与用户意图路由见 [SKILL.md 路由表](./SKILL.md)。

| 子命令 | 一句话功能 |
| ------ | ---------- |
| design-md | 产出 prose-first 的 DESIGN.md |
| draw-md | 产出页面级硬 token UI markdown |
| preview | 用 Element Plus 实时预览验证 |
| draw-harmony | 转换为 HarmonyOS(ArkTS) |
| draw-flutter | 转换为 Flutter |
| draw-element | 转换为 Element Plus(Vue 3) |

## 能力概览

### `references/` —— 子命令流程 + 维度规范 + 框架文档

六个子命令共享的参考文档:

| 文件                                                         | 维度                                |
| ------------------------------------------------------------ | ----------------------------------- |
| [`design-md.md`](references/commands/design-md.md)                    | design-md 子命令流程(上游)        |
| [`draw-md.md`](references/commands/draw-md.md)                        | draw-md 子命令流程(中游)          |
| [`preview.md`](references/commands/preview.md)                        | preview 子命令流程(验证)          |
| [`draw-harmony.md`](references/commands/draw-harmony.md)              | draw-harmony 子命令流程(HarmonyOS) |
| [`draw-flutter.md`](references/commands/draw-flutter.md)              | draw-flutter 子命令流程(Flutter)   |
| [`draw-element.md`](references/commands/draw-element.md)              | draw-element 子命令流程(Element)   |
| [`philosophy.md`](references/meta/philosophy.md)                  | prose-first 方法论                  |
| [`principles.md`](references/meta/principles.md)                  | 设计原则(Do's and Don'ts)         |
| [`token.md`](references/meta/token.md)                            | token 总规范                       |
| [`spec-schema.md`](references/meta/spec-schema.md)                | DESIGN.md schema 与 lint 规则表    |
| [`color.md`](references/dimensions/color.md)                            | 色彩维度                            |
| [`color-palettes.md`](references/dimensions/color-palettes.md)          | 色板维度                            |
| [`font.md`](references/dimensions/font.md)                              | 字体维度                            |
| [`icon.md`](references/dimensions/icon.md)                              | 图标维度                            |
| [`spacing.md`](references/dimensions/spacing.md)                        | 间距维度                            |
| [`radius.md`](references/dimensions/radius.md)                          | 圆角维度                            |
| [`border.md`](references/dimensions/border.md)                          | 描边维度                            |
| [`framework/index.md`](references/framework/index.md)        | 框架资源总览(组件类型索引)        |

### `references/framework/` —— 分层框架文档数据库

```
references/framework/
├── index.md                          # 框架资源总览,含组件类型索引
├── harmony/                          # HarmonyOS(ArkTS)
│   ├── button/{component,usage}.md
│   ├── text/{component,usage}.md
│   └── list/{component,usage}.md
├── flutter/                          # Flutter(Dart)
│   ├── button/{widget,properties}.md
│   ├── text/{widget,properties}.md
│   └── list/{widget,properties}.md
└── element/                          # Element Plus(Vue 3)
    ├── button/{component,api}.md
    ├── text/{component,api}.md
    └── list/{component,api}.md
```

### `examples/` —— 13 种 design system 风格 + UI markdown 示例

```
examples/
├── design-system/              # 13 种风格的 DESIGN.md 示例
│   ├── DESIGN.md               # 根示例
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
└── ui-markdown/                # draw-md 产出示例
    ├── token.md                # 页面 token 表
    ├── ui/
    │   ├── home.md             # 首页规格
    │   └── setting/about.md    # 关于页规格
    └── organisms/
        ├── nav-bar.md          # 导航栏(跨页面复用)
        └── dock.md             # Dock(跨页面复用)
```

### `scripts/` —— 辅助脚本 + 设备模型

- [`design_md_to_token_md.py`](scripts/design_md_to_token_md.py) — 从 DESIGN.md 提取 token 表
- [`device_models.py`](scripts/device_models.py) — iOS/Android 手机与平板设备尺寸配置(6 款设备)
- [`devices/phone.html`](scripts/devices/phone.html) — 手机设备外壳 HTML/CSS 模板(带刘海)
- [`devices/tablet.html`](scripts/devices/tablet.html) — 平板设备外壳 HTML/CSS 模板(无刘海)

#### 支持的设备尺寸

| 设备名 | 平台 | 类型 | 尺寸(宽×高) |
| ------ | ---- | ---- | ------------- |
| iPhone 15 Pro Max | iOS | phone | 430×932 |
| iPhone 15 | iOS | phone | 393×852 |
| iPhone SE 3rd | iOS | phone | 375×667 |
| iPad Pro 12.9" | iOS | tablet | 1024×1366 |
| iPad Air | iOS | tablet | 820×1180 |
| Samsung Galaxy Tab S8 | Android | tablet | 1600×2560 |

## 完整流程链路

```
design-md ──► draw-md ──► preview ──► draw-harmony / draw-flutter / draw-element
(设计系统)   (逻辑稿)    (预览验证)   (框架实现)
```

1. `design-md` 产出 DESIGN.md(设计系统规范)
2. `draw-md` 从 DESIGN.md 产出页面级 UI markdown(逻辑稿)
3. `preview` 用 Element Plus + 设备外壳预览验证逻辑稿效果
4. `draw-harmony` / `draw-flutter` / `draw-element` 将逻辑稿转换为具体框架代码

## FAQ

### `skills` 包版本要求?

需 `skills` npm 包 **v1.5.12+**(本仓库实测 v1.5.14)。`skills` 是 [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) 生态的 CLI,支持 68+ agents。用 `npx skills@latest` 自动获取最新版。

### ui-md 去哪了?

`ui-md` 子命令已重命名为 `draw-md`(v0.1.0),以与下游 `draw-harmony` / `draw-flutter` / `draw-element` 系列命名对齐。功能完全不变,只需将触发语中的 `ui-md` 改为 `draw-md` 即可。

### 哪些源格式被支持?

实跑验证(2026-06-30,`skills` v1.5.14)四种 `npx skills add` 源格式兼容性:

| 命令格式                                           | 兼容性 | 说明                                          |
| -------------------------------------------------- | :----: | --------------------------------------------- |
| `npx skills add https://github.com/Kirky-X/maliang.git` |   ✓    | Full GitHub URL + .git 后缀,推荐             |
| `npx skills add https://github.com/Kirky-X/maliang`     |   ✓    | Full GitHub URL(无 .git),自动补全后缀      |
| `npx skills add Kirky-X/maliang`                   |   ✓    | owner/repo 简写,自动展开为 Full URL,推荐   |
| `npx skills add Kirky-X/maliang.git`               |   ✗    | **不支持** — skills 包 bug:生成 `maliang.git.git` 双后缀,clone 失败。改用 `Kirky-X/maliang`(不带 .git)或 Full URL |

**结论**:推荐使用前三种格式。避免 `owner/repo.git` 简写(skills v1.5.14 有双后缀 bug)。

### 远程安装提示"No skills found"?

确认 GitHub 仓库 `Kirky-X/maliang` 已 push 含 `SKILL.md`(根目录,YAML frontmatter 含 `name` + `description`)的最新代码。`skills` 包通过 `git clone` 获取仓库后扫描 `SKILL.md`,仓库为空或缺少 `SKILL.md` 会报该错。

### `skills add` 提示"Installation complete"但 `.claude/skills/maliang/` 不存在?

这是 `skills` 包 v1.5.14 的已知问题:命令报告成功但未实际复制文件。**Workaround**:手动复制 skill 文件到 agent skills 目录(以下为各 runtime 路径示例,Claude Code / Trae / Cursor / Codex 任选其一):

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

## 许可证

MIT
