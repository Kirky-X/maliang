# 组件路由 —— 区块功能 → 组件类判据

> 本文件是 framework/ 的**选型判据层**:回答「这个区块要做什么 → 该用哪(组)组件类」。由 [`draw-md`](../commands/draw-md.md) 步骤 2.6「③ 组件路由」在布局章节定稿后、写参数表前逐区块过表;组件 slug 一律取自 [`INDEX.md`](./INDEX.md) 的 56 类。
>
> **分工**(各层各管什么,不重复建层):[`../default-pages/INDEX.md`](../default-pages/INDEX.md) 管「整页有哪些页面 + 每页资产映射」(仅 30 默认页);[`../components/INDEX.md`](../components/INDEX.md) 管「每个区段长成什么形态」(51 原型,营销页向);[`../vocabulary/`](../vocabulary/) 管「模式级命名词汇」;[`INDEX.md`](./INDEX.md) 管「选中的组件类有哪些文档」。**本表只回答一层**:任意页面里每个区块的组件类组合怎么选。

---

## 使用规则

1. **逐区块判功能**:一个布局章节 = 一个主功能,查表取推荐组合;组合顺序 = 视觉/结构主次。
2. **判据优先于组合**:区块同时命中多行时,按「首屏承诺 > 操作主次 > 信息密度」排序取主行,其余行的组件降级为辅助。
3. **「不推荐」列是反模式**:跨过它(即用被不推荐的组合)MUST 在组件意图头或 `intent` 字段写明理由——与每页 ≤3 核心组件的 intent 纪律同源。
4. **落空处理**:找不到匹配行时按判据最近的行组合,并在组件意图头说明假设;**连续 2 个区块落空** → 按 [`INDEX.md`](./INDEX.md)「新增组件流程」补类,不硬凑。

---

## 路由表(按功能域分组)

### 数据展示

| 区块功能 | 判据 | 推荐组合 | 不推荐 |
| --- | --- | --- | --- |
| 结构化明细 | 字段 ≥3 且需行级操作/排序/筛选 | `table + pagination + tag` | `grid + card`——行数大时密度失衡、列不对齐 |
| KPI / 指标概览 | 少量数值是主角(2-6 个) | `statistic + card` | `table`——读不出主次,数值被列结构稀释 |
| 趋势 / 占比 / 分布图 | 数据含时序或构成关系 | 图表走 `pattern: chart-*`(vocabulary),`card` 承载 | 纯 `text` 罗列数值——丢失形状信息 |
| 单对象只读详情 | 一字段名配一值,无录入 | `text + divider`(+ `image` / `tag`) | `form`——只读场景误用录入容器 |
| 多媒体展示 | 视觉内容是区块主体 | `image` / `video` / `carousel` | `list` 塞大图——行结构压扁视觉 |

### 列表与集合

| 区块功能 | 判据 | 推荐组合 | 不推荐 |
| --- | --- | --- | --- |
| 内容流列表 | 条目结构一致、纵向滚动 | `list + avatar`(+ `badge` 未读) | `table`——移动端行过宽 |
| 网格内容墙 | 卡片视觉权重高、每项字段少 | `grid + card + image` | 明细字段多时改 `table` 行 |
| 树形层级浏览 | 层级 ≥2 且需展开收起 | `tree` | `menu`——导航语义,不是数据结构 |
| 可勾选集合 | 多选后统一提交 | `checkbox + list` | `switch`——即时生效语义,误触发 |
| 即时开关集合 | 改了立即生效、无提交动作 | `switch`(+ `list` 行) | `checkbox`——留下「要提交」的错误预期 |
| 时间序列事件 | 按时间轴演进的状态节点 | `timeline` | `list`——丢时序感 |
| 标签 / 筛选集合 | 元数据标注或 chip 筛选 | `tag` | `button` 排排坐——动作语义误导 |

### 表单录入

| 区块功能 | 判据 | 推荐组合 | 不推荐 |
| --- | --- | --- | --- |
| 结构化提交 | 字段 ≥3 或需统一校验/提交 | `form + input/select/radio/checkbox/date-picker/upload + button` | 逐字段散放无 `form` 容器——校验与提交失锚 |
| 单值快捷输入 | 1-2 字段 | `input + button` | 整套 `form`——容器过重 |
| 分步长流程 | 步骤 ≥3 或有前后依赖 | `steps + form + button` | `tabs`——平级语义,非流程 |
| 连续值 / 评分录入 | 连续区间或星级语义 | `slider` / `rate` | `input` 手敲数值——交互成本高且易越界 |

### 操作与反馈

| 区块功能 | 判据 | 推荐组合 | 不推荐 |
| --- | --- | --- | --- |
| 轻量结果反馈 | 不打断、自动消失 | `message` | `dialog`——为一句提示打断操作流 |
| 重要结果 / 需选择 | 需用户知晓或决策 | `dialog` / `notification` | `message`——易漏读 |
| 危险操作确认 | 不可逆或影响面大 | `popconfirm` / `dialog` | 无确认直接执行 |
| 上下文补充说明 | hover/点击触发的辅助信息 | `popover`(icon 承载) | 挤进主文案——密度失衡 |
| 不离开当前上下文的子任务 | 浮层内完成小任务或看详情 | `drawer` / `dialog` | 新开整页——上下文丢失 |
| 等待反馈 | 首屏结构已知用骨架,局部用指示器 | `skeleton` / `loading` | 白屏干等 |
| 耗时进度 | 耗时可估、有百分比语义 | `progress` | `loading` 无限转——不可估时长 |

### 导航与结构

| 区块功能 | 判据 | 推荐组合 | 不推荐 |
| --- | --- | --- | --- |
| 层级回溯 | 多级路径需表明当前位置 | `breadcrumb`(+ `navigation`) | 返回按钮堆叠——位置感丢失 |
| 平级内容分组切换 | 同层互斥视图切换 | `tabs` / `segmented` | `steps`——流程语义误用 |
| 页面级主导航 | 顶部/底部全局导航 | `navigation` / `menu` | 页内自造返回——与 organisms 导航漂移 |
| 次要操作收纳 | 次要操作 ≥3 个 | `dropdown` | 全部平铺——操作主次失衡 |
| 单页唯一高频创建动作 | 移动端主操作沉底悬浮 | `fab` | 多 `fab` 并存——主操作失焦 |

### 状态与空态

| 区块功能 | 判据 | 推荐组合 | 不推荐 |
| --- | --- | --- | --- |
| 空态 / 错误出口 | 无数据或失败且需出路 | `image + button + text` | `alert` 占整屏——没有出口动作 |

---

## 组合纪律

- **单区块组合 ≤3 类**:超出说明区块粒度太大,该拆章(布局章节粒度见 [`../commands/draw-md.md`](../commands/draw-md.md) 布局章节规则),不是组合更长。
- **组合连接符**:组件类之间用 ` + ` 连接(如 `input + icon`),与 draw-md「组件类型标注规范」一致;frontmatter `components` 数组按页面出现顺序去重登记。
- **图表特殊路径**:图表不是组件类,一律经 frontmatter `pattern: chart-*` 声明(见 draw-md「模式引用(`pattern:` 字段)」),`table`/`statistic` 等只做数值承载。
- **vocabulary 词汇不进 slug 列**:区块级模式(如 `search-bar`、`table-sortable`)走 `pattern:` 字段,本表推荐列只收组件类。
- **icon 资产选型不在本表**:组件类 `icon` 只声明「有图标位」;用哪个图标库、哪个具体图标资产,按 [`../dimensions/icon.md`](../dimensions/icon.md) 走 xizhi skill 路由,本表不复述其 API(防双处维护)。

---

## 复合组件配方

> **分工**:vocabulary 的 `pattern: search-bar` 等 `pattern:` 字段管**命名**(区块叫什么);本节管**零件**(该区块由哪些组件类/原语拼成、逐框架映射到什么组件)。复合组件配方指**有原生组件可用**的组合;「框架无原生对应」的组合方案在 [INDEX.md](./INDEX.md)「N/A 占位说明」体系内,两者不混。
> 组件源 profile 与查询契约见 [adapter-contract.md](./adapter-contract.md);实时型源的逐框架映射以查询结果为准,本表只登记组件类角色与已知落点。

### 配方 schema

| 要素 | 说明 |
| ---- | ---- |
| 名称 | 配方 slug(kebab-case,与 vocabulary 命名对齐) |
| 角色分解 | 组成零件清单:每个角色 = 一个组件类(取自 [INDEX.md](./INDEX.md) 56 类)或框架原语 |
| 逐框架组件映射 | 每个运行时/组件源下,各角色落到的具体组件(bundled 源指向 framework/ 对应文档;实时型源指向组件源 profile 词典,以查询结果为准) |
| token 锚点 | 视觉值(尺寸/间距/圆角/颜色)一律 `{token-name}` 引用,命名按 [`../meta/token.md`](../meta/token.md),以项目 DESIGN.md 为准;禁止裸值 |
| 反模式 | 已知的错误拼法及原因 |

角色可被单组件吸收(如框架 input 组件自带容器与图标槽);吸收时该角色不单独落组件,映射表标注「吸收」。新增配方 = 本节追加一条(schema 五要素齐全),不另建文件。

### 首例:`search-box`(搜索框)

需求形态:矩形容器 + 单行输入 + 前置搜索图标,可带清除与提交动作。

| 角色 | 组件类 | react(shadcn 通道) | vue(Element Plus) | flutter | arkts |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 容器 | `layout` | 带定位的容器(div/Card,承载 icon 绝对定位) | 吸收(el-input 内建容器) | 吸收(TextField 自带容器) | 吸收(Row + TextInput 容器) |
| 输入框 | `input` | Input | el-input | TextField | TextInput |
| 图标 | `icon` | lucide Search 图标(资产路由走 xizhi) | el-icon(prefix 槽) | prefixIcon | SymbolGlyph/内置搜索图标 |

token 锚点:容器内边距、图标尺寸、边框与圆角、占位文案色一律 `{token-name}` 引用(具体语义 token 名以项目 DESIGN.md 为准,不在本表固化,防双处维护)。

反模式:

| 禁止 | 原因 | 正确做法 |
| ---- | ---- | -------- |
| 用 `button` 冒充整条搜索框 | 丢输入语义,无法聚焦/受控 | 容器 + input + icon 组合 |
| 图标裸 SVG 内联、绕开 `icon` 组件类 | 绕过 xizhi 资产路由与图标语义 | `icon` 角色落组件类,资产走 xizhi |
| 在 input 上手搓边框阴影再造容器 | 越权到样式四级阶梯(见 [INDEX.md](./INDEX.md)「复用阶梯」) | 容器角色交给框架组件或语义 token |
