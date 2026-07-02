# design-md 高级特性 —— 变体生成与边缘场景

> 本文件是 [`design-md.md`](./design-md.md) 的延伸,承载 **Phase 4 变体引擎**与 **Edge Cases & Fallbacks**。主流程(Phase 0-3 + Template + Lint)见主文件。
> 由顶层 [`SKILL.md`](../../SKILL.md) 路由进入;主文件末尾会引用本文件。

---

## Phase 4: Variation Engine(变体生成)

> 从一份主 DESIGN.md 派生多个主题变体(明/暗 / 季节 / A/B / 品牌)。来源:taste-skill + ui-ux-pro-max-skill。**输入**:主 DESIGN.md + 变体规格。**输出**:N 个 `DESIGN.<variant>.md` 文件 + diff 报告。

### 触发场景

| 用户意图                              | 变体类型           | 输出文件                       |
| ------------------------------------- | ------------------ | ------------------------------ |
| "做个暗色版本"                        | mode               | `DESIGN.dark.md`               |
| "做圣诞节主题"                        | seasonal           | `DESIGN.holiday-christmas.md`  |
| "A/B 测试两个 hero 配色"             | ab-test            | `DESIGN.ab-a.md` / `.ab-b.md`  |
| "为子品牌 X 派生一份"                 | brand              | `DESIGN.brand-x.md`            |
| "做高对比度无障碍版"                  | accessibility      | `DESIGN.a11y-aaa.md`           |

### 变体生成流程

1. **解析主 DESIGN.md**:提取全部 token + prose,建立基础结构
2. **应用变体规格**:对每个 token 应用变体规则(见下方规则类型)
3. **保持 prose 一致**:prose 章节不变,除非变体明确改语义(如"高对比度版"需在 Overview 加说明)
4. **生成 diff 报告**:列出相对主版本的 token 改动(增 / 删 / 改值)
5. **lint 每个变体**:每个 `DESIGN.<variant>.md` 单独跑 Phase 3 lint,确保仍合规

### 变体规则类型

#### Type 1 · Mode(明暗模式)

```yaml
# 主 DESIGN.md
colors:
  bg-primary: "#ffffff"
  text-primary: "#1a1c1e"

# DESIGN.dark.md(自动反演 + 暗色独立设计,见 color.md 第 5 节)
colors:
  bg-primary: "#1a1c1e"        # 不纯黑
  text-primary: "#f7f5f2"      # 不纯白
  # 强调色饱和度下调
```

**规则**:暗色不是简单反色,需独立设计;对比度仍需满足 WCAG AA(见 [`accessibility.md`](../meta/accessibility.md))。

#### Type 2 · Seasonal(季节主题)

```yaml
# DESIGN.holiday-christmas.md
colors:
  primary: "#dc2626"  # 红
  tertiary: "#16a34a"  # 绿(辅助强调)
  # prose 加说明:本主题为圣诞限定,12 月生效
```

**规则**:季节变体只改 Primitive 层(色相),Semantic 层映射不变;功能色(success/danger)不可改色相(语义固定)。

#### Type 3 · AB Test(A/B 测试)

```yaml
# DESIGN.ab-a.md
colors:
  primary: "#3b82f6"  # 原色
  # hero CTA 文案:"立即开始"

# DESIGN.ab-b.md
colors:
  primary: "#dc2626"  # 红色(假设 B 测试红色 CTA 转化更高)
  # hero CTA 文案:"免费试用"
```

**规则**:A/B 变体只改被测变量(单变量原则),其余 token 完全一致;diff 报告需明确标出"测试变量"。

#### Type 4 · Brand(子品牌)

```yaml
# DESIGN.brand-x.md(sub-brand)
colors:
  primary: "#8b5cf6"  # 子品牌色(避开 ai-tells.md Lila Rule 柔紫)
  # font-family: Söhne  # 子品牌字体
  # prose 加说明:子品牌定位 / 受众差异
```

**规则**:子品牌变体可改色相 + 字体,但保留主品牌的 Layout / Component 模式;在 prose 中说明子品牌定位差异。

#### Type 5 · Accessibility(无障碍增强)

```yaml
# DESIGN.a11y-aaa.md
colors:
  text-primary: "#0a0a0a"  # 比主版本更深,达 AAA 7:1
  text-secondary: "#404040"  # 也达 AAA
  border-default: "#525252"  # 提对比
dials:
  motion_intensity: 1  # 强制最低动效
  design_variance: 2   # 减少视觉变化
```

**规则**:无障碍变体不可"减功能",只增强可达性;Motion Intensity 强制 ≤ 3;所有对比度达 AAA(7:1)。

### 变体约束(硬性)

- [ ] 每个变体 MUST 单独通过 Phase 3 lint,不可豁免
- [ ] 变体 MUST 显式声明 `variant_of: DESIGN.md`(在 frontmatter)
- [ ] diff 报告 MUST 列出全部 token 改动(增 / 删 / 改值)
- [ ] prose 章节 MUST 保持一致,除非变体类型明确改语义
- [ ] Accessibility 变体 MUST 不引入新的反模式(如降低对比度换美观)
- [ ] AB Test 变体 MUST 单变量,其余 token 完全一致

### 失败模式

| 触发条件                          | 处理                                                     |
| --------------------------------- | -------------------------------------------------------- |
| 变体改了 Semantic 命名            | 报错,变体只改 Primitive 值,不改 Semantic 命名          |
| 变体 lint 失败                    | 修复后重生成,不可"豁免变体 lint"                       |
| 变体引入 AI Tells(如柔紫)       | 拒绝生成,提示按 [`ai-tells.md`](../meta/ai-tells.md) 修改 |
| AB 变体改了多个变量               | 拆为多组 AB,保持单变量原则                               |
| 变体 prose 与主版本冲突           | 变体 prose 必须说明差异,不可静默改                      |

---

## Edge Cases & Fallbacks

### CLI 不可用(无 npm / node 环境)

`npx @google/design.md` 无法运行时手动处理:Tailwind v4 → 手写 `@theme{--color-primary:#...}`;Tailwind v3 → 手写 `theme.extend.colors/fontSize` 对象;Lint → 对照 [`spec-schema.md`](../meta/spec-schema.md) 逐项人工检查。告知用户:"CLI 不可用,已手动处理,可能未覆盖全部 9 条 lint 规则。"

### 输入 CSS/Tailwind 不完整或不一致

| 情形                                   | 处理方式                                                                           |
| -------------------------------------- | ---------------------------------------------------------------------------------- |
| 颜色 ≥8 个,无明显主次                  | 按使用频率排序,取最高频的前4个作为 primary/secondary/tertiary/neutral;在注释里注明 |
| 字体缺少 `font-weight` 或 `lineHeight` | 使用规范默认值:body 400/1.6,heading 600/1.1,label 500/1                            |
| spacing 无规律(如 13px, 27px)          | 提示用户"检测到非标准间距,对齐到 8px 网格",四舍五入后生成,原值写入注释         |
| 存在同名 token 多次定义(冲突)          | 取最后一条,在 DESIGN.md 注释中注明冲突来源文件和行号                               |
| 输入代码不含任何 font/color            | 降级为 Phase 1B 访谈模式,告知用户无法从代码提取                                    |

### 项目已有 DESIGN.md —— 合并 vs 覆写

用户请求生成新的 DESIGN.md 时,若项目根目录已有旧版本:

1. 先展示旧版 token 摘要(name、颜色、字体系列)
2. 明确询问:**"是覆盖旧版本 / 合并新旧 token / 另存为新文件?"**
3. 合并模式:旧 token 保留,新 token 追加;有冲突的 key 以新值为准,旧值写入行注释

### Lint 返回错误

`npx @google/design.md lint` 报错时:列出全部 error 级问题(不静默忽略);可自动修复的直接修(`colour:`→`colors:`、补 `#`、`fontWeight:"700"`→`fontWeight:700`);需判断的(orphaned token、unknown property)先问用户意图;修复后重跑 lint 确认 exit 0。

### 图片质量不足(Phase 1C)

当截图/图片分辨率低、色彩失真、或关键区域被遮挡时:

- 可识别的部分照常提取(颜色、明显的字重差异)
- 无法确认的 token 用 `"#PLACEHOLDER"` 标记,并在文件注释中说明原因
- 告知用户:"以下 token 因图片质量限制无法精确提取,请手动确认:[列表]"
- 请用户提供更高清截图,或切换 Phase 1B 访谈模式补充缺失信息

### 输入信息不足以覆盖全部章节

若源数据(代码/截图/访谈)没有提供 Elevation、Shapes 等某些章节所需信息:仍按规范完整生成该章节,用 flat elevation + tonal layer 默认值替代,并在 prose 中注明"此处为推断默认值,标注'需人工确认'"——不可省略章节。

### 同一对话中需求范围变更

用户在生成过程中改变范围(如先要"整站规范",中途改成"只要按钮组件"):

- 不要静默缩小或放大范围继续生成
- 明确确认:"范围从 [原范围] 调整为 [新范围],对吗?" 确认后才重新规划步骤

### 目标环境不是 Web(React Native / Flutter / SwiftUI)

DESIGN.md 的 CSS 导出格式不直接适用于原生平台:

- 仍按标准格式生成 DESIGN.md(作为设计规范的 single source of truth)
- 在 Phase 2 Step 2 中,将 CSS 变量手动转为平台对应格式:
  - React Native: `StyleSheet.create({ colors: { primary: '#...' } })`
  - Flutter: `ThemeData(colorScheme: ColorScheme(primary: Color(0xFF...)))`
  - SwiftUI: `Color("primary")` + Assets.xcassets 颜色集
- 明确告知用户 CLI export 命令不适用于此场景

---

## Reference Files

- [`design-md.md`](./design-md.md) — 主流程(Phase 0-3 + Template + Lint)
- [`spec-schema.md`](../meta/spec-schema.md) — 完整 token 类型定义 + 权威 Linter Rules 表
- [`philosophy.md`](../meta/philosophy.md) — DESIGN.md 写作三原则
- [`../../examples/design-system/heritage/DESIGN.md`](../../examples/design-system/heritage/DESIGN.md) — 生产级 DESIGN.md 范例

---

## Design Read(设计读取三件事)

> Phase 0 Brief Inference 之后的**设计读取**环节。在写 prose 前,先用"一行检查点"锁定设计意图,再产出三件论点性产物。来源:taste-skill。

### 一行检查点

进入 Phase 1 写 prose 前,用一句话回答:"本设计的**单一视觉论点**是什么?"——这句话必须能用 15 字以内表达,不可含"和/且/同时"(多论点 = 无焦点)。

**示例**:
- ✅ "克制的暗色专业感"(Linear 风)
- ✅ "温暖手绘的文档感"(Notion 风)
- ❌ "现代且简洁同时高端"(三论点,无焦点)

**🔴 CHECKPOINT · Design Read 确认**:展示一行检查点 + 三件事(下),用户确认后进入 Phase 1。

### 三件事(论点性产物)

| 产物                | 回答的问题                          | 形式                          | 长度        |
| ------------------- | ----------------------------------- | ----------------------------- | ----------- |
| **Visual Thesis**(视觉论点) | "用户第一眼应感受到什么?"          | 一句话 + 1-2 个参考锚点       | ≤ 30 字     |
| **Content Plan**(内容计划) | "信息层级与阅读路径是什么?"        | 章节列表 + 每章节的密度档位   | ≤ 10 章节   |
| **Interaction Thesis**(交互论点) | "核心交互动作的反馈语言是什么?"    | 主交互 + 反馈模式 + 缓动曲线  | ≤ 3 个主交互 |

#### Visual Thesis 示例

```
Visual Thesis: "深色优先的键盘驱动效率感"
参考锚点: Linear (dark-first) + GitHub (密度)
→ 驱动 token: bg-primary 深灰(非黑)、font mono 强化、accent 单点紫蓝
```

#### Content Plan 示例

```
Content Plan:
  1. Hero (density=2, 单 CTA)
  2. Features (density=5, bento 4 单元)
  3. Testimonial (density=3, 单列)
  4. Pricing (density=6, 三档)
  5. FAQ (density=7, 折叠列表)
阅读路径: F 型 → Z 型 → 单列聚焦
```

#### Interaction Thesis 示例

```
Interaction Thesis:
  主交互: command palette ⌘K
  反馈模式: 即时出现(无延迟) + 键盘高亮
  缓动: ease-snappy (cubic-bezier(0.16, 1, 0.3, 1))
  → 驱动: MOTION_INTENSITY=4, micro-focus-ring 强化
```

### 三件事与 Phase 1 prose 的关系

三件事是 **prose 的骨架**——Phase 1 写 Overview / Layout / Components 章节时,必须引用三件事作为"为什么"的依据。Visual Thesis → Overview 章节;Content Plan → Layout 章节;Interaction Thesis → Components 章节。prose 不可与三件事矛盾。

---

## Working Model(工作模型)

> 用**最小成本验证设计方向**的概念。在投入完整 DESIGN.md 生成前,先用 Working Model 快速证伪/证实设计假设,避免方向错误后大规模返工。来源:taste-skill。

### 什么是 Working Model

Working Model = **1 个可交互的最小原型**,只验证 Visual Thesis 的核心假设,不含完整 token / 完整组件。它是"设计假设的实验装置",非最终产物。

### 与 Phase 0/1 的关系

```
Phase 0 Brief Inference → 推理设计方向
  ↓
Design Read(三件事)→ 锁定论点
  ↓
Working Model(可选)→ 最小验证论点  ← 在这里
  ↓ 证实
Phase 1 Generate DESIGN.md → 完整 token + prose
```

### Working Model 的最小要素

- ✅ 必须:1 个 Hero 区块(验证 Visual Thesis 第一眼感受)、1 个核心组件(验证 Interaction Thesis 反馈语言)、配色 token ≤5(primary/neutral/text/bg/border)、1 字族(验证字体气质)
- ❌ 不需:完整 token 表(用裸值)、完整组件库(只验证核心交互)、多页面(单页足够)

### Working Model 产出形式

- **HTML 单文件**(≤ 100 行):含 1 个 Hero + 1 个组件,裸 CSS,无框架
- **截图**:浏览器渲染后截图,与参考锚点对比
- **判断**:Visual Thesis 成立 → 进入 Phase 1;不成立 → 回 Phase 0 调整 Thesis

### 何时用 / 何时不用

- ✅ 用:全新项目(方向未定)、brief 模糊(如"做个现代 App")、大品牌改造(高风险,证伪成本远低于返工)
- ❌ 不用:已有 DESIGN.md 仅做变体(方向已定)、brief 含明确参考截图(方向已锁定)、小工具页(低风险,直接 Phase 1)

### 失败模式

- **Working Model 沦为完整原型(> 100 行)**:提示"Working Model 是验证装置,非产物",精简到核心假设
- **用户要求多页面**:拒绝,明确"多页面属于 Phase 1 产物,Working Model 单页"
- **验证失败**:回 Phase 0 调整 Visual Thesis,不强行进入 Phase 1
