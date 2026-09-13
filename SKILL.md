---
name: maliang
description: "前端设计生成 skill,覆盖 UIUX 全生命周期(研究→定义→设计→实现→验证→交付→迭代)。触发：DESIGN.md/design token/CSS 提取/页面 UI markdown/组件规格/导出 Tailwind·CSS·DTCG·lint/转 HarmonyOS·Flutter·Element Plus/redesign/重设计/refresh/restructure/rebuild/去 AI 味/deslop/可用性评审/critique/用户旅程/persona/可用性测试/五秒测试/埋点/设计语言模板/液态玻璃/模板墙。不适用：无 UI 的后端/脚本/数据任务、纯文案写作、非视觉类代码生成。触发（含并入口）：产品 UI 设计/界面 craft/dashboard 界面/设置页设计/interface-design、UI 合规审查/a11y 审查/check accessibility/审查我的 UI（critique 读 web-interface-guidelines 快照）。边界：一次性改版不沉淀 token 用 redesign-existing-projects；代码质量/架构审查用 diting；安全扫描用 tiangang"
allowed-tools: "Bash(python3 scripts/*)"
license: MIT
---

# maliang (马良) —— 设计系统技能

> **脚本调用约定**：`python3 scripts/…` 中的相对路径以**本 skill 的安装目录**为基准（CWD 假设）。
> 在用户项目中执行时，一律以 `{SKILL_DIR}` 绝对路径调用，如 `python3 {SKILL_DIR}/scripts/ui-graph.py …`；`--target`/`--framework-file` 等输入参数显式指向用户项目路径，禁止把 skill 自带的 `examples/` 当作分析目标。

十一个子命令覆盖 UIUX 全生命周期(研究→定义→设计→实现→验证→交付→迭代,总图见 [`references/meta/lifecycle.md`](references/meta/lifecycle.md)):design-md(创建 DESIGN.md,含领域探索与决策账本)→ redesign(改版现有 UI)→ draw-md(页面级 UI markdown)→ preview(预览验证)→ critique(可用性评审)→ draw-harmony/draw-flutter/draw-element(框架代码)→ ui-graph(UI 关系管理)· ip(IP 形象)/ip-handbook(IP 视觉手册)。

- **design-md**(上游)— 产出 prose-first 的 **DESIGN.md**(YAML token + Markdown 设计理由,Google Labs agent-first 格式)。支持"创建、应用、验证、导出"四个动作。解决"设计系统**是什么、为什么**"。
- **redesign**(上游旁路)— 改版现有 UI,9 维审计(含 SEO 与追踪) + 保留规则。支持 Refresh / Restructure / Rebuild / Deslop 四模式。解决"**现有设计如何变好**"。
- **draw-md**(中游)— 从 DESIGN.md 产出页面级硬 token **UI markdown**(布局章节 + 组件参数表,颜色/字体/间距全引用 token,RGBA + HEX)。解决"每个页面/组件**具体怎么实现**"。
- **preview**(验证)— 使用 Element Plus 框架对 draw-md 产出进行实时预览验证,支持 iOS/Android 设备外壳。解决"**效果对不对**"。
- **critique**(验证·深评)— Nielsen 10 启发式 0-4 评分 + persona 走查 + 认知负荷清单,产出评分快照/趋势/backlog。解决"**好不好用**"。UI 合规/a11y 清单读 [`references/meta/web-interface-guidelines.md`](references/meta/web-interface-guidelines.md)（Vercel Web Interface Guidelines 快照, sha e3d624b, 2026-09-12）; 产品 UI craft 纪律与严格评审/去 slop 深流程见 [`references/interface-design/`](references/interface-design/)（原独立 skill 并入）
- **draw-harmony**(下游)— 将 draw-md 逻辑 UI 转换为 HarmonyOS(ArkTS)框架实现。解决"HarmonyOS **代码怎么写**"。
- **draw-flutter**(下游)— 将 draw-md 逻辑 UI 转换为 Flutter 框架实现。解决"Flutter **代码怎么写**"。
- **draw-element**(下游)— 将 draw-md 逻辑 UI 转换为 Element Plus 框架实现。解决"Element Plus **代码怎么写**"。
- **ui-graph**(关系管理)— 从 ui-markdown/ 产出 ui-relationships.json(层级 + 跳转) + ui-hash-state.json(哈希基线) + ui-implementation-map.json(逻辑 UI ↔ 实现映射)。解决"页面关系怎么管、变更怎么追、实现缺口在哪"。
- **ip**(IP 形象)— 基于 DESIGN.md 调性构造 prompt,优先调用 text_to_image API 生成图片,fallback 输出结构化 prompt 文档。解决"项目 IP **形象怎么生**"。
- **ip-handbook**(IP 视觉手册)— 8 模块产出规格(三视图/动作延展/表情包/字体/色彩/版式/周边物料/通用要求),2K 高清 3:4。解决"IP 视觉系统**怎么落地**"。

## 子命令路由

> 🔴 **CHECKPOINT**:无 DESIGN.md 时,严禁直接进入 draw-md / draw-* 下游子命令 —— 必须先走 design-md 建立设计系统,否则产出的 UI markdown 与框架代码无 token 可引用。

| 用户意图                                    | 子命令        | 完整流程                                                          |
| ------------------------------------------- | ------------- | ----------------------------------------------------------------- |
| 创建 / 生成 DESIGN.md(从代码/截图/访谈)     | design-md     | [`references/commands/design-md.md`](references/commands/design-md.md) |
| 应用 DESIGN.md 到前端代码                   | design-md     | [`references/commands/design-md.md`](references/commands/design-md.md) |
| lint / diff / 导出 / 验证 DESIGN.md         | design-md     | [`references/commands/design-md.md`](references/commands/design-md.md) |
| 🔷 改版 / 重设计现有 UI(Refresh/Restructure/Rebuild/Deslop 去AI味) | redesign | [`references/commands/redesign.md`](references/commands/redesign.md) |
| 产出页面级 UI markdown(token 表 + 页面规格) | draw-md       | [`references/commands/draw-md.md`](references/commands/draw-md.md)     |
| 跨页面复用组件(导航栏 / dock)规格化         | draw-md       | [`references/commands/draw-md.md`](references/commands/draw-md.md)     |
| 🔴 预览 UI markdown 效果(设备外壳 + Element)| preview       | [`references/commands/preview.md`](references/commands/preview.md)     |
| 🔷 可用性评审 / 评分(Nielsen+persona 走查+认知负荷) | critique | [`references/commands/critique.md`](references/commands/critique.md)   |
| 🔴 将 UI markdown 转换为 HarmonyOS(ArkTS)代码  | draw-harmony  | [`references/commands/draw-harmony.md`](references/commands/draw-harmony.md) |
| 🔴 将 UI markdown 转换为 Flutter(Dart)代码    | draw-flutter  | [`references/commands/draw-flutter.md`](references/commands/draw-flutter.md) |
| 🔴 将 UI markdown 转换为 Element Plus(Vue 3)代码 | draw-element | [`references/commands/draw-element.md`](references/commands/draw-element.md) |
| 🔷 生成 / 查询 UI 关系图(层级 + 跳转 + 哈希 + 实现映射) | ui-graph | [`references/commands/ui-graph.md`](references/commands/ui-graph.md) |
| 🔷 查询跳转目标未生成 / 异常跳转 / 未实现页面 | ui-graph | [`references/commands/ui-graph.md`](references/commands/ui-graph.md) |
| 🔷 基于 DESIGN.md 生成 IP 形象(API 优先,fallback prompt) | ip | [`references/commands/ip.md`](references/commands/ip.md) |
| 🔷 生成 IP 视觉手册(三视图/动作/表情/字体/色彩/版式/周边) | ip-handbook | [`references/commands/ip-handbook.md`](references/commands/ip-handbook.md) |

> 🔴 标记的行需先确认 draw-md 产出存在;preview/draw-* 无 UI markdown 输入时应在子命令流程内 fallback 引导用户回退到 draw-md。🔷 标记的行属新增能力,critique 需先有 preview 产出或可访问页面,ui-graph 需先有 draw-md 产出,ip/ip-handbook 需先有 DESIGN.md。

进入子命令后,按其流程文档执行。检查点、边界情形、交付核对清单均在各子命令文档内 —— **本路由器不含流程主体**。

### meta 文档加载时序(阶段 × 必读)

规范层 references/meta/ 不要求一次全读——按所处阶段加载,规划类工作不加载执行期文档:

| 阶段(子命令) | 动手前必读 | 按需查阅 |
| --- | --- | --- |
| design-md(创建系统) | [`product-reasoning.md`](references/meta/product-reasoning.md)、[`principles.md`](references/meta/principles.md) | [`dials.md`](references/meta/dials.md)、[`spec-schema.md`](references/meta/spec-schema.md)、[`analytics-events.md`](references/meta/analytics-events.md)(埋点事件表)、[`content-guide.md`](references/meta/content-guide.md)、[templates/README.md](references/templates/README.md)(选型四步) |
| redesign(改版) | [`ai-tells.md`](references/meta/ai-tells.md)、[`rules-priority.md`](references/meta/rules-priority.md) | [`dials.md`](references/meta/dials.md)、[`accessibility.md`](references/meta/accessibility.md)、[`surface-modes.md`](references/meta/surface-modes.md)、[`ux-rules.md`](references/meta/ux-rules.md) |
| draw-md(产出页面规格) | [`token.md`](references/meta/token.md)、[`ai-tells.md`](references/meta/ai-tells.md) | [`surface-modes.md`](references/meta/surface-modes.md)、[`visual-assets.md`](references/meta/visual-assets.md)、[templates/INDEX.md](references/templates/INDEX.md)、[`ux-rules.md`](references/meta/ux-rules.md)、[`llm-behavior.md`](references/meta/llm-behavior.md)(长产物防截断)、[`performance.md`](references/meta/performance.md) |
| preview(验证交付) | [`ai-tells.md`](references/meta/ai-tells.md)(豁免总则)、[`performance.md`](references/meta/performance.md) | [`ux-rules.md`](references/meta/ux-rules.md)、[`accessibility.md`](references/meta/accessibility.md)、[`content-guide.md`](references/meta/content-guide.md) |
| critique(可用性深评) | [`surface-modes.md`](references/meta/surface-modes.md)、[`principles.md`](references/meta/principles.md) | [`accessibility.md`](references/meta/accessibility.md)、[`ux-rules.md`](references/meta/ux-rules.md) |
| draw-harmony/flutter/element | [`performance.md`](references/meta/performance.md)、[`accessibility.md`](references/meta/accessibility.md) | [`token.md`](references/meta/token.md)(命名回填)、[`ux-rules.md`](references/meta/ux-rules.md) |
| ip / ip-handbook | [`product-reasoning.md`](references/meta/product-reasoning.md) | [`content-guide.md`](references/meta/content-guide.md) |

> 元规则:[`rules-priority.md`](references/meta/rules-priority.md) 与 [`philosophy.md`](references/meta/philosophy.md) 是全阶段裁决层,冲突时优先于各阶段文档;[`lifecycle.md`](references/meta/lifecycle.md) 是全生命周期总图(七段×载体×检查点);[`llm-behavior.md`](references/meta/llm-behavior.md) 在产出 > 2 屏的长文档时必读。

## 通用

- **不确定用哪个?** 先 `design-md`。没有 DESIGN.md 就无法产出可靠的 `draw-md` 硬 token,更无法进行框架适配。
- **完整流程链路**(每步产出 = 下步输入): `design-md`(→DESIGN.md) → `draw-md`(→examples/ui-markdown/*.md) → `preview`(→preview_*.html) → [`critique`](references/commands/critique.md)(→评分快照) → `draw-harmony`/`draw-flutter`/`draw-element`(→框架代码);迭代经 `redesign`/`ui-graph` 回流 decisions 账本。
- 维度规范(色 / 字 / 图 / 距 / 角 / 线 / 布局 / 海拔)在 [`references/dimensions/`](references/dimensions/) 下(含 color-palettes 调色板库、design-systems 参考设计系统、glass-effect/glass-advanced 液态玻璃配方、elevation 表面海拔);设计原则在 [`references/meta/principles.md`](references/meta/principles.md),十一个子命令共享参考,不在本路由器重复。
- **模板墙**在 [`references/templates/`](references/templates/INDEX.md):12 种设计语言(液态玻璃/M3 Expressive/Fluent 2/Bento/瑞士编辑/OLED 暗色/数据仪表盘等) + 整页模式(编辑分栏/纵深长廊/Dashboard 风格集/移动端五式/滚动图带) + 落地页编排 + 性格方向卡;选型走 README 四步路由 + [variation-engine](references/templates/variation-engine.md) 七轴组合。
- **术语库**在 [`references/vocabulary/`](references/vocabulary/),共 18 篇模式命名词汇,draw-md 组件命名对齐:cards / galleries / hero / layout / micro-interactions / navigation / scroll / typography / **popups(弹窗) / buttons(按钮反馈) / charts(图表选型) / forms(表单) / auth(登录认证) / tables(数据表格) / search(搜索筛选) / onboarding(新手引导) / states(页面状态) / commerce(定价转化)**(后 7 篇源自对 GOV.UK、WAI-ARIA、Carbon、NN/g、Atlassian、Baymard 等专业站点的抓取研究,2026-09-08)。
- **结构化 UX 规则**在 [`references/meta/ux-rules.md`](references/meta/ux-rules.md)(slug + Do/Don't + 严重级,脚本检查是它的机械化子集);页面模式判定见 [`surface-modes.md`](references/meta/surface-modes.md),图片策略见 [`visual-assets.md`](references/meta/visual-assets.md)。
- 数据埋点规范(事件命名 / 漏斗三件套 / 改版基线比对)见 [`references/meta/analytics-events.md`](references/meta/analytics-events.md);用户研究三产出(persona / journey / JTBD)见 design-md Phase 0a([`references/commands/design-md.md`](references/commands/design-md.md))。
- 默认页面清单(App 15 页 + Web 15 页,含 P0/P1/P2 选用规则)在 [`references/default-pages/index.md`](references/default-pages/index.md) 下,供 `draw-md` 子命令在新项目触发"页面清单确认"步骤时引用。
- 框架组件文档(按钮/文本/列表 × 三框架)在 [`references/framework/`](references/framework/index.md) 下,三个 draw-* 子命令共享。
- UI 关系管理工具 [`scripts/ui-graph.py`](scripts/ui-graph.py) 提供 7 个子命令(generate/list-missing/check-nav/compute-hash/diff-hash/build-impl-map/list-unimplemented),纯 Python 标准库实现,产出 ui-relationships.json(层级 + 跳转)、ui-hash-state.json(哈希基线)、ui-implementation-map.json(逻辑 UI ↔ 实现映射),供 `ui-graph` 子命令调用;配套 [`scripts/validate-draw-md.py`](scripts/validate-draw-md.py) 含 13 项检查(aria/touch-target/dark-mode/motion/radius/z-index 等),供 `preview` 子命令校验。

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
| -------- | -------- | ---------- |
| 无 DESIGN.md 直接要 UI markdown | 引导用户先走 design-md | 若用户坚持,产出"无 token 锚点"的临时规格并显式标注"待 DESIGN.md 建立后回填" |
| DESIGN.md 缺失关键 token(如无 color.text) | 在子命令流程内列出缺失 token 清单,询问用户补全 | 用 `{color-text-primary}` 等标准命名占位,标注"假设值,需 DESIGN.md 确认" |
| draw-* 找不到组件文档(framework/ 无对应类型) | 在 index.md 索引表查最接近的组件类型 | 用基础组件(button/text/list/layout)组合实现,标注"无原生对应,本方案为组合" |
| 用户提供的 UI markdown 不符合 draw-md 规格(见禁止事项 #3) | 提示具体偏差(缺 token / 缺布局章节) | 引导用户重跑 draw-md,不要硬解析不规范输入;preview 设备尺寸不在 scripts/ 时用最接近尺寸替代 |
| ip 子命令 text_to_image API 不可用(网络/限流/未配置) | 输出结构化 prompt 文档(正向/负向提示词 + CFG/步数/种子参数建议 + 比例 3:4),标注"待 API 可用后调用" | 引导用户用外部工具(Stable Diffusion/MJ)按 prompt 生成,产物回填到 examples/ip-character/ |
| ui-graph 找不到 ui-relationships.json(未 generate) | 提示先跑 `python3 scripts/ui-graph.py generate --target examples/ui-markdown/` | 若 ui-markdown/ 为空,引导回退到 draw-md 先产出页面 markdown |

## 禁止事项(反例黑名单)
1. **禁止跳过 design-md** — 无 DESIGN.md 直接产出 UI markdown 或框架代码,会导致 token 引用悬空、视觉不一致。
2. **禁止硬编码颜色/字号/间距** — 所有视觉值必须用 `{token-name}` 占位符引用,严禁 `#FF0000`、`14px`、`16px` 等具体值出现在示例代码中(文档说明中的 token 映射对照除外)。
3. **禁止跨子命令直连 / 禁止混合 token 命名** — design-md 产出不经 draw-md 直接转 draw-* 会丢失上下文,必须按链路执行;token 命名遵循 references/meta/token.md,不得混用 `{color-primary}` 和 `{primary-color}` 两种风格。
4. **禁止忽略 N/A 占位 / 禁止在 router 内写流程主体** — 跨框架转换时 N/A 组件不得强行冒充(回退组合方案);本文件是路由器,流程细节必须放在 references/commands/*.md。
