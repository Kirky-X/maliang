# template/ —— 交付物骨架模板(复制填充)

> 本目录是**交付物骨架**的唯一 canonical:每份文件复制到目标位置后直接填充。
> 填法、校验规则与流程门禁在对应子命令文档(见下表),本目录只管骨架长什么样——两处互补不重复。
> 与 [`references/templates/`](../references/templates/INDEX.md)(模板墙)**分工不同**:模板墙是设计语言与整页模式的**选型参考**(读,不复制);本目录是**落盘起点**(复制,再填)。

| 文件 | 用途 | 消费方式 | 填法与校验规则(canonical) |
| --- | --- | --- | --- |
| [DESIGN.md](./DESIGN.md) | 设计契约骨架(YAML token + prose 章节,含溯源注释位) | 复制为 `.maliang/DESIGN.md` 后填充 | [`references/commands/design-md.md`](../references/commands/design-md.md) |
| [ui-page.md](./ui-page.md) | ui-markdown 页面骨架(frontmatter + 方向契约块 + 意图头 + 参数表字面形态) | 复制为 `.maliang/ui-markdown/ui/<page>.md` 后填充 | [`references/commands/draw-md.md`](../references/commands/draw-md.md) |
| [ip-prompt.md](./ip-prompt.md) | IP 形象生成 prompt 契约(8 维度 + 填写形态) | 按 8 维度组 prompt 调 API;API 不可用时落 fallback 文档 | [`references/commands/ip.md`](../references/commands/ip.md) |
| [a11y-walkthrough.md](./a11y-walkthrough.md) | A11y 实测记录(人工实测用;skill 只做键盘推演与要点声明,不伪造"已实测"结论) | 复制为 `.maliang/critique/a11y-walkthrough.md` 后逐页复测追加 | [`references/commands/critique.md`](../references/commands/critique.md) |

- **溯源注释**(`# D-P<n>-<m>` / `# no-decision: <来源>`)规则唯一 canonical 见 [`references/meta/token-provenance.md`](../references/meta/token-provenance.md)。
- **安装**:本目录随 skill 顶层条目整体分发(install-skill.sh 复制顶层,不在排除表),运行时以 `{SKILL_DIR}/template/…` 引用。
- **来源**:四份骨架 2026-11-07 自各命令文档内嵌段迁出成单真源,原位置留指针;迁移决策见 git 历史。骨架内的 `references/…` 路径为明文(非链接)——模板复制进用户项目后仍可读,不产生死链。
