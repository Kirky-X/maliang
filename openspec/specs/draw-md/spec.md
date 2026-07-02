## ADDED Requirements

### Requirement: draw-md 产物层目录结构

`draw-md` 子命令 SHALL 在 `examples/ui-markdown/` 下维护产物层目录：根级 `token.md`（硬值表）、`organisms/`（跨页面复用的重复性组件）、`ui/`（页面 markdown，SHALL 用嵌套子目录表达页面层级）。`ui/` 下的一级页面（首页）SHALL 由 `ui/main.md` 或 `ui/home.md` 描述；下级页面 SHALL 用嵌套子目录表达（如 `ui/setting/about.md` 表示 setting 下的 about 页）。

#### Scenario: 一级首页页面文件存在

- **WHEN** 查看产物层 `ui/` 目录
- **THEN** 首页由 `main.md` 或 `home.md` 表达，位于 `ui/` 根级

#### Scenario: 二级页面用嵌套子目录表达层级

- **WHEN** setting 页存在下级 about 页
- **THEN** about 页由 `ui/setting/about.md` 表达，目录嵌套对应页面层级

#### Scenario: 重复组件抽离到 organisms

- **WHEN** 导航栏、dock 栏等跨页面重复出现的组件
- **THEN** 其规格放入 `organisms/`，页面通过引用而非复制

### Requirement: 产物层 token.md 硬值表

`docs/ui/markdown/token.md` SHALL 含 6 个章节：颜色、字体、图标、间距、圆角、分割线。每个 token SHALL 同时给出 RGBA 与 HEX 两种格式。该文件是所有页面 markdown 的 frontmatter 与组件参数表的**唯一**颜色/数值引用源。

#### Scenario: 6 维度章节齐全

- **WHEN** 读取产物层 `token.md`
- **THEN** 含颜色、字体、图标、间距、圆角、分割线 6 个章节，无遗漏

#### Scenario: 双格式硬值

- **WHEN** 读取任一颜色 token
- **THEN** 同时给出 RGBA 与 HEX 两种格式（如 `#007AFF` / `rgba(0, 122, 255, 1)`）

### Requirement: 页面 markdown 的 frontmatter 契约

`ui/` 与 `organisms/` 下每份 markdown SHALL 以 YAML frontmatter 开头，MUST 含字段：`name`（组件/页面名称）、`description`（描述）、`updated`（更新时间，ISO 8601 日期）、`version`（版本号）。frontmatter 中的背景色等视觉属性 MUST 引用 `token.md` 中的 token，MUST NOT 硬编码颜色字面量（如 `#007AFF`）。

#### Scenario: 必填字段齐全

- **WHEN** 读取任一页面 markdown 的 frontmatter
- **THEN** 含 `name`、`description`、`updated`、`version` 四个必填字段

#### Scenario: 背景色引用 token 而非硬编码

- **WHEN** frontmatter 声明背景色等视觉属性
- **THEN** 引用 `token.md` 中的 token 名（如 `background: $color-surface`），MUST NOT 出现硬编码颜色字面量

### Requirement: 页面正文按视觉顺序组织布局章节

页面 markdown 正文 SHALL 按从上到下、从左到右的视觉顺序组织布局章节：**首章 SHALL 为顶部导航，末章 SHALL 为底部 dock**。每个章节内的子组件 SHALL 按从左到右顺序描述；内部组件 SHALL 用嵌套子章节展开。

#### Scenario: 首章为顶部导航

- **WHEN** 读取页面 markdown 的章节顺序
- **THEN** 第一个布局章节描述顶部导航

#### Scenario: 末章为底部 dock

- **WHEN** 读取页面 markdown 的章节顺序
- **THEN** 最后一个布局章节描述底部 dock

#### Scenario: 子组件从左到右描述

- **WHEN** 某章节含多个并列子组件（如导航栏的左 logo、中标题、右操作）
- **THEN** 按从左到右视觉顺序依次描述

### Requirement: 布局章节含组件参数表

每个布局章节 SHALL 含组件参数表，列 MUST 至少覆盖：宽度、高度、字体大小、圆角、背景颜色、字体颜色、padding。参数表中的背景颜色与字体颜色 MUST 引用 `token.md` 的 token。涉及响应式时，参数表 SHALL 标注断点差异。

#### Scenario: 参数列齐全

- **WHEN** 读取任一布局章节的组件参数表
- **THEN** 表头含宽度、高度、字体大小、圆角、背景颜色、字体颜色、padding 列

#### Scenario: 颜色列引用 token

- **WHEN** 参数表填写背景颜色或字体颜色
- **THEN** 值为 `token.md` 中的 token 引用，MUST NOT 为硬编码颜色字面量

#### Scenario: 响应式断点标注

- **WHEN** 组件在不同断点（如移动端/桌面端）尺寸不同
- **THEN** 参数表标注各断点的对应值
