<!-- 供体候选池快照(中文译本,非蒸馏供体;原文见「原始出处」)。
     站点分组: 基础设施与云(infra) · 站点摘要: 基础设施自动化。企业级整洁,黑白
     站点色板: #000000, #15181e, #0d0e12, #f1f2f3, #d5d7db, #b2b6bd
     晋升正式供体须满足 ../README.md §5 三条件;蒸馏稿另立 ../<id>.md,与本快照并存。 -->

# 设计系统:HashiCorp

## 1. 视觉主题与氛围

HashiCorp 的网站让企业基础设施变得可触摸——这套设计系统必须传达云基础设施管理的复杂度,同时保持可接近。视觉语言分成两种模式:信息区块用干净的白底亮色模式,hero 区与产品展示用戏剧化的暗色模式(`#15181e`、`#0d0e12`),这种昼夜二元性呼应"亮处构建、暗处部署"的开发者工作流。

排版的锚点是一款自定义品牌字体(HashiCorp Sans,加载名 `__hashicorpSans_96f0ca`),它承载了相当的分量——字面意义上的。标题用 600–700 字重配紧行高(1.17–1.19),形成密集、权威的文本块,传达企业级的可信感。82px、字重 600、开启 OpenType `"kern"` 的 hero 大标题不是装饰——它是基础设施级的排版。

HashiCorp 的辨识点在多产品色彩系统。产品线里每个产品都有自己的品牌色——Terraform 紫(`#7b42bc`)、Vault 黄(`#ffcf25`)、Waypoint 青(`#14c6cb`)、Vagrant 蓝(`#1868f2`)——这些颜色通过 CSS 自定义属性系统(`--mds-color-*`)作为强调 token 贯穿全站。这就形成了设计系统里的设计系统:母品牌是黑白加蓝色强调,而每个子产品注入自己的彩色身份。

组件系统用 `mds`(Markdown Design System)前缀,表明这是一套系统性、token 驱动的做法,颜色、间距、状态全部通过 CSS 变量管理。阴影极其细微——用 `rgba(97, 104, 117, 0.05)` 的双层微阴影,几乎不可见,但刚好提供足够深度,把交互表面与背景分开。

**关键特征:**
- 双模式:干净白色区块 + 戏剧化暗色(`#15181e`)hero/产品区
- 自定义 HashiCorp Sans 字体,600–700 字重,开 `"kern"` 特性
- 通过 `--mds-color-*` CSS 自定义属性的多产品色彩系统
- 产品品牌色:Terraform 紫、Vault 黄、Waypoint 青、Vagrant 蓝
- 大写字母配字距的说明标签(13px、字重 600、1.3px 字距)
- 微阴影:0.05 不透明度的双层——靠耳语而非喊叫表达深度
- token 驱动的 `mds` 组件系统,变量名带语义
- 紧凑圆角:2px–8px,没有任何药丸形或圆形
- 次级文本用 system-ui 回退字体栈

## 2. 色板与角色

### 品牌主色
- **Black**(`#000000`):主品牌色、亮面文本、`--mds-color-hcp-brand`
- **Dark Charcoal**(`#15181e`):暗色模式背景、hero 区
- **Near Black**(`#0d0e12`):最深的暗色模式表面、暗面表单输入

### 中性色阶
- **Light Gray**(`#f1f2f3`):浅背景、细微表面
- **Mid Gray**(`#d5d7db`):边框、暗面按钮文字
- **Cool Gray**(`#b2b6bd`):边框强调(0.1–0.4 不透明度)
- **Dark Gray**(`#656a76`):辅助文字、次级标签、`--mds-form-helper-text-color`
- **Charcoal**(`#3b3d45`):亮面次级文本、按钮边框
- **Near White**(`#efeff1`):暗面主文本

### 产品品牌色
- **Terraform Purple**(`#7b42bc`):`--mds-color-terraform-button-background`
- **Vault Yellow**(`#ffcf25`):`--mds-color-vault-button-background`
- **Waypoint Teal**(`#14c6cb`):`--mds-color-waypoint-button-background-focus`
- **Waypoint Teal Hover**(`#12b6bb`):`--mds-color-waypoint-button-background-hover`
- **Vagrant Blue**(`#1868f2`):`--mds-color-vagrant-brand`
- **Purple Accent**(`#911ced`):`--mds-color-palette-purple-300`
- **Visited Purple**(`#a737ff`):`--mds-color-foreground-action-visited`

### 语义色
- **Action Blue**(`#1060ff`):暗面主操作链接
- **Link Blue**(`#2264d6`):亮面主链接
- **Bright Blue**(`#2b89ff`):激活链接、hover 强调
- **Amber**(`#bb5a00`):`--mds-color-palette-amber-200`,警告状态
- **Amber Light**(`#fbeabf`):`--mds-color-palette-amber-100`,警告背景
- **Vault Faint Yellow**(`#fff9cf`):`--mds-color-vault-radar-gradient-faint-stop`
- **Orange**(`#a9722e`):`--mds-color-unified-core-orange-6`
- **Red**(`#731e25`):`--mds-color-unified-core-red-7`,错误状态
- **Navy**(`#101a59`):`--mds-color-unified-core-blue-7`

### 阴影
- **Micro Shadow**(`rgba(97, 104, 117, 0.05) 0px 1px 1px, rgba(97, 104, 117, 0.05) 0px 2px 2px`):默认卡片/按钮海拔
- **Focus Outline**:`3px solid var(--mds-color-focus-action-external)`——系统性焦点环

## 3. 排版规则

### 字族
- **主品牌**:`__hashicorpSans_96f0ca`(HashiCorp Sans),回退:`__hashicorpSans_Fallback_96f0ca`
- **System UI**:`system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial`

### 层级

| 角色 | 字体 | 字号 | 字重 | 行高 | 字距 | 备注 |
|------|------|------|--------|-------------|----------------|-------|
| 显示级 hero | HashiCorp Sans | 82px (5.13rem) | 600 | 1.17(紧) | normal | 开 `"kern"` |
| 区块标题 | HashiCorp Sans | 52px (3.25rem) | 600 | 1.19(紧) | normal | 开 `"kern"` |
| 特性标题 | HashiCorp Sans | 42px (2.63rem) | 700 | 1.19(紧) | -0.42px | 负字距 |
| 子标题 | HashiCorp Sans | 34px (2.13rem) | 600–700 | 1.18(紧) | normal | 特性区块 |
| 卡片标题 | HashiCorp Sans | 26px (1.63rem) | 700 | 1.19(紧) | normal | 卡片与面板标题 |
| 小标题 | HashiCorp Sans | 19px (1.19rem) | 700 | 1.21(紧) | normal | 紧凑标题 |
| 正文强调 | HashiCorp Sans | 17px (1.06rem) | 600–700 | 1.18–1.35 | normal | 加粗正文 |
| 大号正文 | system-ui | 20px (1.25rem) | 400–600 | 1.50 | normal | hero 描述 |
| 正文 | system-ui | 16px (1.00rem) | 400–500 | 1.63–1.69(松) | normal | 标准正文 |
| 导航链接 | system-ui | 15px (0.94rem) | 500 | 1.60(松) | normal | 导航项 |
| 小号正文 | system-ui | 14px (0.88rem) | 400–500 | 1.29–1.71 | normal | 次级内容 |
| 说明文字 | system-ui | 13px (0.81rem) | 400–500 | 1.23–1.69 | normal | 元数据、footer 链接 |
| 大写标签 | HashiCorp Sans | 13px (0.81rem) | 600 | 1.69(松) | 1.3px | `text-transform: uppercase` |

### 原则
- **品牌/系统分工**:标题与品牌关键文本用 HashiCorp Sans,正文、导航、功能文本用 system-ui。品牌字体承载分量,system-ui 承载词句。
- **字距常开**:所有 HashiCorp Sans 文本都开 OpenType `"kern"`——字形间距不可协商。
- **紧凑标题**:每个标题都用 1.17–1.21 行高,形成密集堆叠的文本块,感觉像基础设施——坚实、承重。
- **舒展正文**:正文用 1.50–1.69 行高(明显宽松),在密集标题之下形成舒适的阅读节奏。
- **大写标签做路标**:13px 大写配 1.3px 字距,用作系统性的分类/区块标记——永远是 HashiCorp Sans 字重 600。

## 4. 组件样式

### 按钮

**深色主按钮**
- 背景:`#15181e`
- 文字:`#d5d7db`
- padding:9px 9px 9px 15px(非对称,左侧留更多)
- 圆角:5px
- 边框:`1px solid rgba(178, 182, 189, 0.4)`
- 阴影:`rgba(97, 104, 117, 0.05) 0px 1px 1px, rgba(97, 104, 117, 0.05) 0px 2px 2px`
- 焦点:`3px solid var(--mds-color-focus-action-external)`
- hover:使用 `--mds-color-surface-interactive` token

**白色次级按钮**
- 背景:`#ffffff`
- 文字:`#3b3d45`
- padding:8px 12px
- 圆角:4px
- hover:`--mds-color-surface-interactive` + 低阴影海拔
- 焦点:`3px solid transparent` outline
- 外观干净、极简

**产品色按钮**
- Terraform:背景 `#7b42bc`
- Vault:背景 `#ffcf25`(深色文字)
- Waypoint:背景 `#14c6cb`,hover `#12b6bb`
- 每个产品按钮遵循相同结构,但用自己的品牌色

### 徽章 / 药丸
- 背景:`#42225b`(深紫)
- 文字:`#efeff1`
- padding:3px 7px
- 圆角:5px
- 边框:`1px solid rgb(180, 87, 255)`
- 字体:16px

### 输入

**文本输入(暗色模式)**
- 背景:`#0d0e12`
- 文字:`#efeff1`
- 边框:`1px solid rgb(97, 104, 117)`
- padding:11px
- 圆角:5px
- 焦点:`3px solid var(--mds-color-focus-action-external)` outline

**复选框**
- 背景:`#0d0e12`
- 边框:`1px solid rgb(97, 104, 117)`
- 圆角:3px

### 链接
- **亮面 Action Blue**:`#2264d6`,hover → blue-600 变量,hover 时下划线
- **暗面 Action Blue**:`#1060ff` 或 `#2b89ff`,hover 时下划线
- **暗面白**:`#ffffff`,透明下划线 → hover 时显示下划线
- **亮面中性**:`#3b3d45`,透明下划线 → hover 时显示下划线
- **暗面浅色**:`#efeff1`,hover 模式相同
- 所有链接用 `var(--wpl-blue-600)` 作 hover 色

### 卡片与容器
- 亮色模式:白底,微阴影海拔
- 暗色模式:`#15181e` 或更深的表面
- 圆角:卡片与容器 8px
- 产品展示卡带渐变边框或强调光

### 导航
- 干净的水平导航,带 mega-menu 下拉
- HashiCorp logo 左对齐
- 链接用 system-ui 15px 字重 500
- 产品分类按生命周期管理组组织
- 头部有"Get started"与"Contact us" CTA
- hero 区用暗色模式变体

## 5. 布局原则

### 间距系统
- 基数:8px
- 刻度:2px, 3px, 4px, 6px, 7px, 8px, 9px, 11px, 12px, 16px, 20px, 24px, 32px, 40px, 48px

### 网格与容器
- 内容最大宽:约 1150px(xl 断点)
- 全宽暗色 hero 区,内容居中收束
- 卡片网格:2–3 列布局
- 桌面尺度下宽裕的水平内边距

### 断点
| 名称 | 宽度 | 关键变化 |
|------|-------|-------------|
| 小屏手机 | <375px | 紧凑单列 |
| 手机 | 375–480px | 标准移动端 |
| 小屏平板 | 480–600px | 小幅调整 |
| 平板 | 600–768px | 2 列网格开始 |
| 小屏桌面 | 768–992px | 完整导航可见 |
| 桌面 | 992–1120px | 标准布局 |
| 大屏桌面 | 1120–1440px | 最大宽度内容 |
| 超宽屏 | >1440px | 居中,宽裕外边距 |

### 留白哲学
- **企业级呼吸感**:区块间用宽裕纵向间距(48px–80px+),传达稳定与严肃。
- **密标题、宽正文**:紧行高标题坐在舒展正文之上,形成每个区块"顶部压重"的视觉。
- **暗色即画布**:暗色 hero 区用额外纵向内边距,让 3D 插画与渐变有空间呼吸。

### 圆角刻度
- 极小(2px):链接、小内联元素
- 细微(3px):复选框、小输入框
- 标准(4px):次级按钮
- 舒适(5px):主按钮、徽章、输入框
- 卡片(8px):卡片、容器、图片

## 6. 深度与海拔

| 层 | 处理 | 用途 |
|-------|-----------|-----|
| 平(第 0 层) | 无阴影 | 默认表面、文本块 |
| 耳语(第 1 层) | `rgba(97, 104, 117, 0.05) 0px 1px 1px, rgba(97, 104, 117, 0.05) 0px 2px 2px` | 卡片、按钮、交互表面 |
| 焦点(第 2 层) | `3px solid var(--mds-color-focus-action-external)` outline | 焦点环——配色随语境 |

**阴影哲学**:HashiCorp 用的或许是现代网页设计里最细微的阴影系统。5% 不透明度的双层阴影几乎不可见——它们不是为了制造视觉深度,而是为了提示可交互性。如果你能看见阴影,那就是太强了。这种克制传达了企业级的稳定价值——没有东西漂浮,没有东西不确定。

## 7. Do's and Don'ts

### Do
- 标题与品牌文本用 HashiCorp Sans,正文与 UI 文本用 system-ui
- 所有 HashiCorp Sans 文本都开 `"kern"`
- 产品品牌色只用于各自的产品(Terraform = 紫,Vault = 黄,以此类推)
- 区块标记用 13px、字重 600、1.3px 字距的大写标签
- 阴影保持在"耳语"级别(0.05 不透明度双层)
- 用 `--mds-color-*` token 系统保持配色一致
- 维持"紧标题 / 宽正文"的节奏(1.17–1.21 对 1.50–1.69 行高)
- 无障碍用 `3px solid` 焦点 outline

### Don't
- 不要把产品品牌色用到产品语境之外(不要在 Vault 内容上放 Terraform 紫)
- 不要把阴影不透明度提到 0.1 以上——耳语级别是有意的
- 不要用药丸形按钮(圆角 >8px)——锐利、克制的圆角是结构性的
- 不要在标题上跳过 `"kern"` 特性——这款字体需要它
- 不要把小号正文交给 HashiCorp Sans——它专为 17px+ 的标题用途设计
- 不要在同一组件里混用产品色——每个产品只有一种颜色
- 不要在暗色背景用纯黑(`#000000`)——用 `#15181e` 或 `#0d0e12`
- 不要忘掉非对称按钮内边距——9px 9px 9px 15px 是有意的

## 8. 响应式

### 断点
| 名称 | 宽度 | 关键变化 |
|------|-------|-------------|
| 手机 | <768px | 单列、汉堡导航、堆叠 CTA |
| 平板 | 768–992px | 2 列网格、导航开始展开 |
| 桌面 | 992–1150px | 完整布局、mega-menu 导航 |
| 大屏 | >1150px | 最大宽度居中、宽裕外边距 |

### 折叠策略
- Hero:标题 82px → 52px → 42px
- 导航:mega-menu → 汉堡
- 产品卡:3 列 → 2 列 → 堆叠
- 暗色区块保持全宽但压缩内边距
- 按钮:内联 → 移动端全宽堆叠

## 9. Agent Prompt Guide

### 快速取色参考
- 亮面背景:`#ffffff`、`#f1f2f3`
- 暗面背景:`#15181e`、`#0d0e12`
- 亮面文本:`#000000`、`#3b3d45`
- 暗面文本:`#efeff1`、`#d5d7db`
- 链接:`#2264d6`(亮面)、`#1060ff`(暗面)、`#2b89ff`(激活)
- 辅助文字:`#656a76`
- 边框:`rgba(178, 182, 189, 0.4)`、`rgb(97, 104, 117)`
- 焦点:`3px solid` + 与产品匹配的颜色

### 组件提示词示例
- "在暗色背景(#15181e)上做 hero。标题 82px HashiCorp Sans 字重 600,行高 1.17,开 kern,白色文字。副文本 20px system-ui 字重 400,行高 1.50,文字 #d5d7db。两个按钮:深色主按钮(#15181e,5px 圆角,9px 15px 内边距)与白色次级按钮(#ffffff,4px 圆角,8px 12px 内边距)。"
- "设计一张产品卡:白底,8px 圆角,rgba(97,104,117,0.05) 双层阴影。标题 26px HashiCorp Sans 字重 700,正文 16px system-ui 字重 400 行高 1.63。"
- "做一个大写区块标签:13px HashiCorp Sans 字重 600,行高 1.69,字距 1.3px,text-transform uppercase,颜色 #656a76。"
- "做产品专属 CTA 按钮:Terraform → #7b42bc 背景,Vault → #ffcf25 配深色文字,Waypoint → #14c6cb。全部:5px 圆角,文字 500 字重,16px system-ui。"
- "设计一个暗色表单:#0d0e12 输入背景,#efeff1 文字,1px solid rgb(97,104,117) 边框,5px 圆角,11px 内边距。焦点:3px solid 强调色 outline。"

### 迭代指南
1. 永远先定模式:信息区块用亮色(白),hero/产品用暗色(#15181e)
2. HashiCorp Sans 只用于标题(17px+),其余全用 system-ui
3. 阴影在耳语级别(0.05 不透明度)——如果看得见就调低
4. 产品色是神圣的——每个产品恰好拥有一种颜色
5. 焦点环永远是 3px solid,配色随产品语境
6. 大写标签是系统性的路标模式——13px、600、1.3px 字距
