# 框架适配器契约 —— 运行时 × 组件源

> 本文件定义框架组件参考层的两层结构与接入契约，是**组件源登记、实时文档查询、选型呈现**的唯一 canonical；`draw-harmony` / `draw-flutter` / `draw-element` 三个子命令与 `preview` 共享本契约。
> **事实源顺序**：官网实时抓取为唯一事实源（按各组件源的 ingest 通道）；bundled 快照仅为回退源——仅官网程序化抓取失败的框架（当前：HarmonyOS/ArkUI，见 [INDEX.md](./INDEX.md)「API 基线」节）以快照为主源；其余框架断网时允许回退快照，快照缺失则跳过本级并显式报告。
> **不建持久缓存**：查询结果只在任务会话内按查询键内存去重，任务结束即弃，不落盘、不过期——agent 持续联网，断网即无工作场景；持久缓存只引入过期维护负担。
> **选型权**：最终框架/组件源由用户强制指定（见「用户强制指定门」）；本契约与 [INDEX.md](./INDEX.md) 两级选型表只负责呈现候选与适用场景，不替用户选择。

---

## 两层结构

| 层 | 是什么 | 实例（2026-11 登记） |
| --- | --- | --- |
| 运行时适配器 | 语言与渲染范式层：决定代码形态、主题机制、preview 模板 | `react` / `vue` / `arkts` / `flutter` |
| 组件源 profile | 挂在一个运行时之下、提供组件的具体来源 | react：shadcn/ui（registry-json）、Motif（registry-json）、Astryx（docs-site）；vue：Element Plus（docs-site，bundled 快照回退）；arkts：ArkUI（bundled-snapshot）；flutter：Material/Cupertino（docs-site） |

同一运行时可挂多个组件源。Motif 是 `react` 运行时上 shadcn 通道的第二个 registry 源，不是独立运行时适配器。新运行时/新组件源一律按「新增框架接入流程」（[INDEX.md](./INDEX.md)）登记 profile 后方可进入 draw-* 查询。

## 组件源 profile 契约（8 字段，必填）

每个组件源 profile 按下表登记；字段值是唯一对齐口径，禁止在 draw-* 文档里出现第二套同义枚举。

| # | 字段 | 取值域与说明 |
| --- | ---- | ------------ |
| 1 | 身份与版本锚点 | 名称、语言、基线版本。复制粘贴型无版本号时如实标注「无版本锚点，以项目内源码为准」（如 Motif） |
| 2 | 组件源声明 | ingest 通道枚举：`registry-json`（组件元数据 JSON 端点）\| `docs-site`（官方文档站 + URL 模式）\| `bundled-snapshot`（仓内快照回退）。附官方 URL 模式 |
| 3 | 分发模式与探测信号 | 枚举：`npm-package` \| `copy-paste`。npm 型探测信号 = 用户项目 package.json 依赖存在；复制粘贴型探测信号 = `components.json` 存在或 `components/ui/` 目录存在 |
| 4 | 组件词典 | 统一 slug ↔ 框架原生名映射（推广 [INDEX.md](./INDEX.md)「命名 slug 统一约定」既有 9 类做法）；新增组件类时先登记词典再建文档 |
| 5 | token 注入点 | 该框架主题机制的唯一说明位：EP/shadcn = CSS 变量；Astryx = StyleX 变量 + 主题包；Flutter = ThemeData；ArkUI = 主题属性。效果退化衔接见 [glass-effect.md](../dimensions/glass-effect.md)「效果 → 组件参数退化」 |
| 6 | 组合原语清单 | 该源的最小原语集（容器/输入/图标等），复合配方按此组装（配方 schema 见 [component-routing.md](./component-routing.md)「复合组件配方」） |
| 7 | 复用阶梯实例化 | 指向 [INDEX.md](./INDEX.md)「复用阶梯」，标注本源在三级控件阶梯的落点（npm 型组件=级 1 原生；registry 复制粘贴型=级 1–2；手搓仍为最后手段） |
| 8 | preview 通道 | 指向 `preview.py` 模板注册表的模板名（当前：`ep` / `react`）；react 模板覆盖 shadcn/Motif/Astryx 三源 |

## 分发模式与版本一致性

- **npm-package 型**（Astryx、Element Plus、Flutter 内置库）：组件本体经 `npm install`/包管理器进入用户项目 node_modules，源码不进用户仓库。版本锚点 = 已装版本；官网文档对应版本 > 已装版本时按 [INDEX.md](./INDEX.md)「超基线 API 两级语义」处理（`safe to plan around` 附检测与降级写法；`unsafe to write today` 禁止写入产出代码）。
- **copy-paste 型**（shadcn/ui、Motif）：官方不发 npm 包，组件本体源码文件写入用户项目目录（如 `components/ui/`）。**已知限制**：用户改动过组件源码后，官网文档可能与项目内组件失配——此时一律**以项目内源码为准**，官网文档只作 API 语义参考；这是复制粘贴型固有限制，无法完全消除。
- 版本探测文件口径：npm 型读 `package.json`；Flutter 读 `pubspec.yaml`；ArkTS 读 `oh-package.json5`。探测为 draw-* 必做步骤，流程细节在各 draw-* 文档。

## 用户强制指定门

draw-* 遇「目标组件源未指定」时执行：

1. 探测用户项目栈与已装包（按字段 3 探测信号）；
2. 按 [INDEX.md](./INDEX.md)「运行时 × 组件源两级选型表」呈现候选：已装的排前，每项附适用场景 + 慎用场景 + 风险标记；
3. **由用户指定最终组件源**——skill 只提醒"哪个更优"，不得自动锁定；呈现不等于选择；
4. 指定结果作为一条决策回写 DESIGN.md 决策账本（见下节），后续 draw / redesign 直接复用，不再重复询问；
5. 主源缺某类组件时，提示补充源候选（如 shadcn 主源缺 agent 部件 → Motif 补），经用户确认后混用，产出标注混合来源；混用边界遵守选型表「混用规则」。

## 查询契约

| 项 | 契约 |
| --- | --- |
| 查询键 | `运行时 × 组件源 × 组件`（三元组，会话内去重的唯一键） |
| 输入 | 用户意图（大白话先译为组件原语名词，翻译纪律见 [vocabulary/INDEX.md](../vocabulary/INDEX.md) 头注）或 draw-md 组件参数表条目 |
| 返回 | 该框架该组件的：用法（最小示例）+ 参数（Props/属性表）+ **`{token-name}` 引用形式的视觉值**；禁止返回裸 px/hex（违反 G01–G46 门禁），token 到具体值的解析发生在 draw-* 生成时按框架 token 注入点进行 |
| 通道 | 三级顺序：官网实时抓 → bundled 快照回退 → 显式报错 + 组合兜底。步骤细节在各 draw-* 文档「组件映射」节，本契约只定语义 |
| 去重 | 会话内内存级去重，任务结束即弃；禁止落盘、禁止建持久缓存库 |

## 决策账本回写

组件源选择是设计决策，回写规则与 [token-provenance.md](../meta/token-provenance.md) 决策 id 体系一致：

- 回写条目 = `决策 id + D-<阶段>-<序号>` 形态记入 DESIGN.md decisions 账本，内容含：选定运行时、选定组件源、选择理由、探测到的已装依赖证据；
- 后续 draw-* / redesign 读取账本即得组件源，不再重复执行「用户强制指定门」；
- 用户中途换源 = 新决策条目，旧条目保留不覆盖（账本 append-only）。

## 相关文档

- [INDEX.md](./INDEX.md)：组件类型索引、两级选型表、复用阶梯、超基线语义、新增框架接入流程
- [component-routing.md](./component-routing.md)：区块功能 → 组件类路由、复合组件配方
- [glass-effect.md](../dimensions/glass-effect.md)：效果 → 组件参数退化
- [token.md](../meta/token.md)：token 命名（查询返回值纪律的上位规范）
- 各框架命令文档:[draw-element.md](../commands/draw-element.md) / [draw-harmony.md](../commands/draw-harmony.md) / [draw-flutter.md](../commands/draw-flutter.md)(查询通道步骤与版本探测)
