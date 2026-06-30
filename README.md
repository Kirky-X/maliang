# maliang —— 设计系统技能

maliang 是一个面向 AI agent 的设计系统 skill,采用 Google Labs agent-first 格式(YAML token + Markdown 设计理由)。它通过两个子命令构成一条流水线:`design-md` 产出 prose-first 的 `DESIGN.md`,`ui-md` 从 `DESIGN.md` 产出页面级硬 token UI markdown。

- **design-md**(上游)— 创建、应用、验证、导出 `DESIGN.md`(解决"设计系统**是什么、为什么**")
- **ui-md**(下游)— 从 `DESIGN.md` 产出页面级 UI markdown(解决"每个页面/组件**具体怎么实现**")

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
# 例如 Claude Code: ~/.claude/skills/maliang/
```

## 使用示例

maliang 作为 skill 被 agent 加载后,通过自然语言意图触发,无需显式命令。以下为典型用法:

### design-md:创建 DESIGN.md

> 帮我基于现有 CSS 代码创建 DESIGN.md 设计系统文件

agent 将读取 `references/design-md.md` 流程,按 prose-first 方法论产出 `DESIGN.md`(YAML token + Markdown 设计理由)。

其他触发场景:
- "从这张 UI 截图提取设计 token"
- "lint 我的 DESIGN.md 是否符合规范"
- "把 DESIGN.md 导出为 Tailwind / CSS 变量 / W3C DTCG 格式"

### ui-md:生成页面级 UI markdown

> 基于 DESIGN.md 产出首页的 UI markdown 规格

agent 将读取 `references/ui-md.md` 流程,产出页面级硬 token markdown(布局章节 + 组件参数表,颜色/字体/间距全引用 token,RGBA + HEX)。

其他触发场景:
- "规格化跨页面复用的导航栏 / dock"
- "产出设置页的 UI markdown"

## 能力概览

### `references/` —— 13 个维度规范文件

两个子命令共享的参考文档:

| 文件                                                         | 维度                                |
| ------------------------------------------------------------ | ----------------------------------- |
| [`design-md.md`](references/design-md.md)                    | design-md 子命令流程(上游)        |
| [`ui-md.md`](references/ui-md.md)                            | ui-md 子命令流程(下游)            |
| [`philosophy.md`](references/philosophy.md)                  | prose-first 方法论                  |
| [`principles.md`](references/principles.md)                  | 设计原则(Do's and Don'ts)         |
| [`token.md`](references/token.md)                            | token 总规范                       |
| [`spec-schema.md`](references/spec-schema.md)                | DESIGN.md schema 与 lint 规则表    |
| [`color.md`](references/color.md)                            | 色彩维度                            |
| [`color-palettes.md`](references/color-palettes.md)          | 色板维度                            |
| [`font.md`](references/font.md)                              | 字体维度                            |
| [`icon.md`](references/icon.md)                              | 图标维度                            |
| [`spacing.md`](references/spacing.md)                        | 间距维度                            |
| [`radius.md`](references/radius.md)                          | 圆角维度                            |
| [`border.md`](references/border.md)                          | 描边维度                            |

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
└── ui-markdown/                # ui-md 产出示例
    ├── token.md                # 页面 token 表
    ├── ui/
    │   ├── home.md             # 首页规格
    │   └── setting/about.md    # 关于页规格
    └── organisms/
        ├── nav-bar.md          # 导航栏(跨页面复用)
        └── dock.md             # Dock(跨页面复用)
```

### `scripts/` —— 辅助脚本

- [`design_md_to_token_md.py`](scripts/design_md_to_token_md.py) — 从 DESIGN.md 提取 token 表

## FAQ

### `skills` 包版本要求?

需 `skills` npm 包 **v1.5.12+**(本仓库实测 v1.5.14)。`skills` 是 [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) 生态的 CLI,支持 68+ agents。用 `npx skills@latest` 自动获取最新版。

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

确认 GitHub 仓库 `Kirky-X/maliang` 已 push 含 `SKILL.md`(根目录,YAML frontmatter 含 `name` + `description`)的最新代码。`skills` 包通过 `git clone` 获取仓库后扫描 `SKILL.md`,仓库为空或缺少 `SKILL.md` 会报此错。

### `skills add` 提示"Installation complete"但 `.claude/skills/maliang/` 不存在?

这是 `skills` 包 v1.5.14 的已知问题:命令报告成功但未实际复制文件。**Workaround**:手动复制 skill 文件到 agent skills 目录:

```bash
# Claude Code
mkdir -p ~/.claude/skills/maliang
cp -r SKILL.md skill.json references examples scripts ~/.claude/skills/maliang/

# Trae
mkdir -p ~/.trae-cn/skills/maliang
cp -r SKILL.md skill.json references examples scripts ~/.trae-cn/skills/maliang/
```

## 许可证

MIT
