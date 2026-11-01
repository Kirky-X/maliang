---
description: 按 Web 界面规则快照审查 UI 代码的合规性
argument-hint: <file-or-pattern>
---

# Web Interface Guidelines


审查以下文件的合规性:$ARGUMENTS

读文件,对照下方规则检查。输出简洁但完整 —— 为简短可以牺牲语法。高信噪比。

## 规则

### 无障碍

- 纯图标按钮需要 `aria-label`
- 表单控件需要 `<label>` 或 `aria-label`
- 交互元素需要键盘处理器(`onKeyDown`/`onKeyUp`)
- 动作用 `<button>`,导航用 `<a>`/`<Link>`(不用 `<div onClick>`)
- 图片需要 `alt`(装饰性图片用 `alt=""`)
- 装饰性图标需要 `aria-hidden="true"`
- 异步更新(吐司、校验)需要 `aria-live="polite"`
- 先用语义 HTML(`<button>`、`<a>`、`<label>`、`<table>`),再用 ARIA
- 标题层级 `<h1>`–`<h6>`;为主内容加跳过链接
- 标题锚点加 `scroll-margin-top`
- 有意义的媒体需要按情况提供字幕、文字稿或描述
- 媒体控件需要键盘支持;装饰性媒体需要对辅助技术隐藏

### 焦点态

- 交互元素需要可见焦点:`focus-visible:ring-*` 或等价方案
- 绝不在没有焦点替代方案时用 `outline-none` / `outline: none`
- 用 `:focus-visible` 而非 `:focus`(避免点击时出现焦点环)
- 复合控件用 `:focus-within` 做组焦点
- 粘性页头/页脚/浮层不得遮住获得焦点的元素

### 表单

- 输入框需要 `autocomplete` 与有意义的 `name`
- 用正确的 `type`(`email`、`tel`、`url`、`number`)与 `inputmode`
- 键盘调度:验证码用 `inputmode="numeric"`,金额用 `"decimal"`;用户名/验证码上 `autocapitalize="none"` + `autocorrect="off"`;`enterkeyhint` 与动作匹配(`go`/`search`/`send`/`next`/`done`)
- 绝不阻止粘贴(`onPaste` + `preventDefault`)
- 标签可点击(`htmlFor` 或包裹控件)
- 邮箱、验证码、用户名关闭拼写检查(`spellCheck={false}`)
- 复选框/单选框:标签与控件共用单一热区(无死区)
- 提交按钮在请求开始前保持可用;请求期间显示 spinner
- 错误内联显示在字段旁;提交时聚焦第一个错误
- 占位符以 `…` 结尾并展示示例格式
- 非认证字段用 `autocomplete="off"`,避免触发密码管理器
- 有未保存改动时离开前警告(`beforeunload` 或路由守卫)

### 动画

- 尊重 `prefers-reduced-motion`(提供降级变体或直接禁用)
- 只动 `transform`/`opacity`(对合成器友好)
- 绝不用 `transition: all` —— 显式列出属性
- 设置正确的 `transform-origin`
- SVG:变换放在 `<g>` 包裹层上,配 `transform-box: fill-box; transform-origin: center`
- 动画可中断 —— 动画中响应用户输入
- 自动播放的动效超过 5 秒且与其他内容并存时,需要暂停、停止或隐藏控件
- 静音装饰性循环在 `prefers-reduced-motion` 下必须停止

### 排版

- 用 `…` 不用 `...`
- 用弯引号 `“` `”` 不用直引号 `"`
- 不换行空格:`10&nbsp;MB`、`⌘&nbsp;K`、品牌名
- 加载态以 `…` 结尾:`"Loading…"`、`"Saving…"`
- 数字列/对比加 `font-variant-numeric: tabular-nums`
- 标题用 `text-wrap: balance` 或 `text-pretty`(防孤行)

### 内容处理

- 文本容器处理长内容:`truncate`、`line-clamp-*` 或 `break-words`
- flex 子项需要 `min-w-0` 才能截断文本
- 处理空态 —— 空字符串/空数组不要渲染出坏掉的 UI
- 用户生成内容:预想短、中等与超长输入

### 图片

- `<img>` 需要显式 `width` 与 `height`(防 CLS)
- 首屏以下图片:`loading="lazy"`
- 首屏关键图片:`priority` 或 `fetchpriority="high"`

### 性能

- 大列表(>50 项):虚拟化(`virtua`、`content-visibility: auto`)
- 渲染中不做布局读取(`getBoundingClientRect`、`offsetHeight`、`offsetWidth`、`scrollTop`)
- 批量读/写 DOM;避免交错
- 优先非受控输入;受控输入必须每次击键都廉价
- 为 CDN/资源域加 `<link rel="preconnect">`
- 关键字体:`<link rel="preload" as="font">` 配 `font-display: swap`
- 优先 `<video autoplay muted loop playsinline>` 而非动图 GIF;提供静态替代
- 短的非必要循环:Safari H.264 MP4 `<picture>` 源、`prefers-reduced-motion` 媒体条件、静态回退

### 导航与状态

- URL 反映状态 —— 筛选、标签页、分页、展开面板写进查询参数
- 链接用 `<a>`/`<Link>`(支持 Cmd/Ctrl+click、中键点击)
- 所有有状态 UI 都可深链(若用了 `useState`,考虑通过 nuqs 或类似方案同步 URL)
- 破坏性动作需要确认模态或撤销窗口 —— 绝不立即执行

### 触控与交互

- `touch-action: manipulation`(消除双击缩放的延迟)
- `-webkit-tap-highlight-color` 要刻意设置 —— 关掉它就等于强制每个交互元素都要有显式 `:active` 按压反馈(见下文「手势手感」),否则触控将失去全部反馈
- `overscroll-behavior` 分两层:根滚动容器只在类 app 外壳里设 `none`,以杀掉下拉刷新劫持(内容页/文档页保持默认);内部滚动容器设 `contain` —— 模态/抽屉/底部面板也算
- 绝不用 `touchmove` + `preventDefault` 假造:它挡住原生滚动、强制非被动监听、卡帧
- 拖拽期间:禁用文本选择,被拖元素加 `inert`
- `user-select: none` 只用于控件外壳(按钮、标签页、滑块)并配 `-webkit-touch-callout: none`;内容文本(段落、代码、说明)必须保持可选;绝不加在 `body` 上
- 拖拽/滑动/捏合/路径手势需要轻点/点击与键盘替代方案,除非确实必要
- `autoFocus` 慎用 —— 仅桌面、仅单个主输入框;移动端避免

### 手势手感


- 触摸按下时高亮(`:active`),松开时提交 —— 按压反馈不等于提交
- 拖过取消阈值必须可见地取消(状态 + 位置回退),而不是默默吞掉手势
- 并行运行所有可能的手势识别器,消歧后取消败者 —— 绝不用只报最终状态的识别器
- 双击检测给每一次单击都加上歧义延迟;要么有意识地接受这个代价,要么放弃双击(轴锁定 / 迟滞阈值在 [`../motion-skeletons/gesture-arbitration.md`](../motion-skeletons/gesture-arbitration.md),此处不复述)

### 安全区与布局

- 满幅布局需要 `env(safe-area-inset-*)` 处理刘海
- 避免多余滚动条:容器加 `overflow-x-hidden`,修掉内容溢出
- 布局用 flex/grid,不用 JS 测量

### 暗色模式与主题

- 暗色主题在 `<html>` 上设 `color-scheme: dark`(修正滚动条、输入框)
- `<meta name="theme-color">` 与页面背景一致
- 原生 `<select>`:显式 `background-color` 与 `color`(Windows 暗色模式)

### 语言与 i18n

- 日期/时间:用 `Intl.DateTimeFormat`,不用硬编码格式
- 数字/货币:用 `Intl.NumberFormat`,不用硬编码格式
- 通过 `Accept-Language` / `navigator.languages` 判断语言,不用 IP
- 品牌名、代码 token、标识符:用 `translate="no"` 包裹,防自动翻译弄乱

### 水合安全

- 带 `value` 的输入框需要 `onChange`(或改用 `defaultValue` 走非受控)
- 日期/时间渲染:防住服务端与客户端的水合不匹配
- `suppressHydrationWarning` 只在真正需要处使用

### 悬浮与交互态

- 按钮/链接需要 `hover:` 态(视觉反馈)
- 交互态提升对比:悬浮/按下/焦点比其余更突出
- 仅悬浮样式包在 `@media (hover: hover) and (pointer: fine)` 里 —— 两个条件都要:触控设备会伪造精细指针,或在轻点时锁定悬浮,留下一个卡住的悬浮态直到下次点到别处

### 内容与文案

- 主动语态:"Install the CLI" 而非 "The CLI will be installed"
- 标题/按钮用 Title Case(Chicago 风格)
- 计数用阿拉伯数字:"8 deployments" 而非 "eight"
- 按钮标签具体:"Save API Key" 而非 "Continue"
- 错误信息包含修法/下一步,不只是问题
- 用第二人称;避免第一人称
- 空间受限时用 `&` 而非 "and"

### 反模式(见到就报)

- `user-scalable=no` 或 `maximum-scale=1` 禁用缩放
- `onPaste` 配 `preventDefault`
- `transition: all`
- `outline-none` 没有 focus-visible 替代
- 内联 `onClick` 导航而没有 `<a>`
- `<div>` 或 `<span>` 挂点击处理器(应为 `<button>`)
- 图片没有尺寸
- 大数组 `.map()` 没有虚拟化
- 表单输入没有标签
- 图标按钮没有 `aria-label`
- 硬编码日期/数字格式(应用 `Intl.*`)
- `autoFocus` 没有明确理由
- 压缩视频适用时用动图 GIF
- 仅有手势的动作,没有轻点/点击与键盘替代

## 输出格式

按文件分组。用 `file:line` 格式(VS Code 可点击)。发现要简短。

```text
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - input lacks label
src/Button.tsx:55 - animation missing prefers-reduced-motion
src/Button.tsx:67 - transition: all → list properties

## src/Modal.tsx

src/Modal.tsx:12 - missing overscroll-behavior: contain
src/Modal.tsx:34 - "..." → "…"

## src/Card.tsx

✓ pass
```

给出问题 + 位置。修法不明显时才解释。不要开场白。
