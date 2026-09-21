# component 子命令 —— 单组件路由

> 当 brief 是**一个元素**而非一个页面时（"做个按钮" / "这个输入框很廉价" / "单独一个 toast"），走本流程替代 `draw-md` 的页面机制：保留 craft floor 与现有 token，跳过骨架 / 引擎 / 轮换，强制交付**全部八状态 + 预览文件**。页面级的状态检查见 [`preview-checklist.md`](preview-checklist.md) §5.7（那是页面完成度的子集）；本文件是**组件粒度**的完整清单与几何纪律。
>
> 来源：Adapted from finesse-ui component-scope（github.com/mouse-lin/finesse-skill，MIT License），2026-09 吸收并本地化。

## §0 范围检测 —— 两个信号路由

在进入任何模式判定之前运行。**≥2 条命中 → 走组件流程**：

- brief 点名**单个 UI 元素**：button · input · textarea · select · checkbox · radio · switch · slider · card · modal · drawer · dropdown · menu · tooltip · popover · tab strip · chip · badge · tag · avatar · breadcrumb · pagination · toast · snackbar · banner · accordion row · date picker · file upload
- brief **≤ 30 词且只指一件事**
- 目标是**单个组件文件**（`Button.tsx` / `components/input.css` / `Card.vue` / `ui/toast.svelte`）
- 用户说"就这个 X" / "单独一个 Y" / "只改这个"

**反向信号——命中任一仍走页面流程**：点名多个 section、要布局、说"页面 / 落地页 / dashboard / 设置页"。

**含糊时问恰好一个问题然后执行**："一张定价卡，还是整个定价页？" 用户不回应时**默认组件**——改向一个组件远比改向一整页便宜。

## §1 组件路线保留什么

- **所属表面继承模式**：仪表盘里的按钮是 Operate register（[`../meta/surface-modes.md`](../meta/surface-modes.md)），发布页里的按钮是 Persuade/Experience。无上下文可读时问用户，默认 Operate。
- **craft floor 全保留**：tinted neutrals（禁纯 `#fff`/`#000`）、半透明/发丝描边、带色相阴影、对比度地板——任何范围都不可谈判。
- **现有 token 优先**。先读项目：存在 `DESIGN.md` / `tokens.css` / `:root` 块时，组件**按名消费 token**（`var(--accent)`），不发明任何字面量。往锁定了 accent 的项目里自带一个 `#4F46E5` 是缺陷，不是设计。
- **廉价黑名单**照常适用：渐变文字、侧条纹边框、装饰性玻璃拟态、未调色中性色、对比度失败、混用圆角刻度（见 [`../meta/ai-tells.md`](../meta/ai-tells.md)）。
- 有动效就必须 `prefers-reduced-motion` 降级；路线选型见 [`../motion-skeletons/ROUTING.md`](../motion-skeletons/ROUTING.md)（组件级动效几乎总是 R1）。

## §2 组件路线跳过什么（明确说出来）

Design Read、骨架选型、hero 引擎、整页 dials、跨次轮换日志——组件没有 hero 也没有 section，跳过这些**并且告知用户跳过了**。交互模式选型仍可用 [`../vocabulary/`](../vocabulary/) 各表（如 toast 用 `toast-queue-handoff`，见 [`sheet-drawer.md`](../vocabulary/sheet-drawer.md)）。

## §3 八状态 —— 唯一硬门槛

**每个可交互组件交付全部八态的代码**，不是建议：

| 状态 | 要求 |
| --- | --- |
| **default** | 静息态 |
| **hover** | 指针反馈。锁在 `@media (hover: hover)` 内，触屏上永不粘住 |
| **focus-visible** | 可见 ring，与相邻表面对比 **≥3:1**；**绝不动画它的出现**——键盘用户需要它即时落位。用 `outline` + `outline-offset`，不用 `border` |
| **active** | 按压态：1px 位移或填充加深。**最常被漏掉的一个** |
| **disabled** | 三通道而非一通道：`opacity: .5` **且** `cursor: not-allowed` **且** 原生 `disabled` 属性（或 `aria-disabled="true"`）。只有 opacity 是"变淡的可用态"，不是禁用态 |
| **loading** | 锁定终宽避免文字换 loading 时回流；>300ms 的操作必须给 |
| **error** | 状态给出原因**和**修法（"密码需 8 位以上"），禁止只写"无效" |
| **success** | 静默成功通常是对的——效果已在屏上就别庆祝；对用户看得见的事再弹 toast 是噪声 |

**改布局即破坏的几何纪律：**

- **状态间禁止改 `border-width`**。default/hover/focus/error 全部同宽；状态走 `background-color` / `border-color` / `outline` / `box-shadow`——宽度一变邻居全移一像素。
- **focus ring 用 `outline` 不用 `border`**，静息时预置 `outline: 2px solid transparent`，激活零几何位移。
- **表单行统一基高**：38px 输入框配 44px 按钮是最常见的调参痕迹。定一个高度（触控 44px 地板）全行共享。
- **预留辅助/错误槽位**：`min-height: 1lh` 即使为空，错误出现时页面不下沉。

与既有规范的关系：[`../vocabulary/states.md`](../vocabulary/states.md) 管页面级 Loading/Empty/Error；本表把同样的纪律收到**单个控件**粒度并补齐 `active`、锐化 `focus` 为 `:focus-visible`。

## §4 交付两文件

1. **组件本体**：匹配项目既有约定（`Button.tsx` / `Button.vue` / `button.css` + markup），token 按名消费，禁止内联字面量色值。
2. **`<Name>.preview.html`**：独立页面，八个状态**堆叠排列并加标签**。让真实伪类与强制类**双写**（`:hover` 与 `.is-hover` 同规则），预览才能钉住需要真实指针的状态。用户打开一次确认后即删——交付时明确说明它不是生产代码。

## §5 与 draw-md / preview 的关系

- 组件构建**不写** `build-log.json`、**不盖** variation-engine 印章（跨次轮换是页面级概念）；但若项目已有 DESIGN.md，产出的 token 用法须与其一致。
- 组件并入页面后，由 [`preview-checklist.md`](preview-checklist.md) §5.7 在页面级复检。
- 模式词汇（微交互命名 / 进度确认 / 抽屉链路）照常从 [`../vocabulary/`](../vocabulary/) 取用。
