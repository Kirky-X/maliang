# preview 子命令 —— 使用 Element Plus 实时预览验证

> 本文件是 `preview` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 输入 = `draw-md` 产出的页面级 UI markdown(`examples/ui-markdown/` 下),输出 = 自包含 HTML 预览文件。
> 预览使用 Element Plus 框架(CDN 引入),支持设备外壳展示(从 `scripts/device_models.py` 读取尺寸)。

---

## 流程概览

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  1. 设备选择      │ -> │  2. 输入解析      │ -> │  3. HTML 模板注入  │ -> │  4. 预览校验      │
│  从 device_models │    │  读取 draw-md 产出 │    │  Element Plus CDN │    │  浏览器打开验证    │
│  读取尺寸配置      │    │  + token.md       │    │  + 设备外壳 CSS   │    │                  │
└──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## 1. 设备选择

从 [`scripts/device_models.py`](../../scripts/device_models.py) 读取设备尺寸配置,让用户选择预览设备:

### 可选设备列表

(设备清单见 `scripts/device_models.py`,流程文档不重复列出,避免与脚本脱节)

**🔴 CHECKPOINT · 设备选择**:展示设备列表,让用户选择预览设备。默认选 iPhone 15(393×852)。

---

## 2. 输入解析

读取 `draw-md` 产出的页面 markdown:

1. **解析 frontmatter** — 提取 `name`、`description`、`background`、`updated`、`version`
2. **解析 token.md** — 读取 `examples/ui-markdown/token.md`,建立 token 名→硬值映射表
3. **解析布局章节** — 按"顶部导航 → 主体区块 → 底部 dock"顺序,逐章提取组件类型与参数表
4. **解析 organisms** — 若页面引用了 `organisms/` 下的组件,读取对应 markdown

**🔴 CHECKPOINT · 输入解析确认**:确认 UI markdown + token.md 已读取,设备尺寸已从 device_models.py 选定,展示预览配置摘要(页面名 + 设备名 + 尺寸)供用户确认,再进入 HTML 生成。

---

## 3. HTML 模板注入

将解析结果注入 HTML 模板,生成自包含预览文件:

### HTML 结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>预览 - <页面名称></title>
  <!-- Element Plus CDN -->
  <link rel="stylesheet" href="https://unpkg.com/element-plus/dist/index.css">
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
  <script src="https://unpkg.com/element-plus"></script>
  <style>
    /* CSS 变量注入(从 token.md 解析) */
    :root {
      --color-primary: #...;
      --color-surface: #...;
      --font-size-md: 16px;
      --spacing-md: 16px;
      --radius-md: 8px;
      /* ... */
    }
    /* 设备外壳样式(从 scripts/devices/ 模板注入) */
    .device-shell { width: <设备宽度>px; height: <设备高度>px; ... }
  </style>
</head>
<body>
  <div id="app">
    <div class="device-shell">
      <div class="device-screen">
        <!-- 页面内容(从 draw-md 章节映射为 Element Plus 组件) -->
        <el-container>
          <el-header><!-- 顶部导航 --></el-header>
          <el-main><!-- 主体区块 --></el-main>
          <el-footer><!-- 底部 dock --></el-footer>
        </el-container>
      </div>
    </div>
  </div>
  <script>
    const { createApp } = Vue;
    const app = createApp({ /* 页面数据与方法 */ });
    app.use(ElementPlus);
    app.mount('#app');
  </script>
</body>
</html>
```

### 设备外壳 CSS

根据设备类型(phone / tablet)选择不同的外壳模板:

- **手机**(phone):圆角 + 刘海 + 边框,参考 [`scripts/devices/phone.html`](../../scripts/devices/phone.html)
- **平板**(tablet):圆角 + 无刘海 + 边框,参考 [`scripts/devices/tablet.html`](../../scripts/devices/tablet.html)

### 组件映射规则

| draw-md 逻辑组件 | Element Plus 预览组件 |
| ------------------- | --------------------- |
| button | `<el-button>` |
| text | `<el-text>` / `<p>` / `<h1>`~`<h6>` |
| list | `<el-table>` 或 `<div v-for>` |
| navigation bar | `<el-menu>` / `<el-header>` |
| dock | `<el-footer>` + `<el-button-group>` |

**🔴 CHECKPOINT · HTML 生成确认**:确认 preview HTML 已生成且 token 引用正确(无硬编码颜色/字号/间距),设备外壳 CSS 已注入,提示用户在浏览器打开验证效果。

---

## 4. 预览校验

生成 HTML 文件后,执行校验:

- [ ] HTML 文件自包含(无本地依赖,CDN 资源可访问)
- [ ] CSS 变量已从 token.md 注入到 `:root`,无 `{token-name}` 占位符残留
- [ ] 设备外壳尺寸与所选设备一致(宽×高)
- [ ] 页面内容按 draw-md 章节顺序排列(顶部导航 → 主体 → 底部 dock)
- [ ] Element Plus 组件正确渲染(无 Vue 控制台错误)
- [ ] 在浏览器中打开文件,视觉与 draw-md 描述一致

---

## 5. Pre-Flight Check(80+ 项机械检查)

> 交付前**机械扫描**(可脚本化,非主观判断)。任一项失败即"硬性失败",不可交付,必须返工。来源:taste-skill + ui-ux-pro-max-skill。检查项按 9 个维度分组。

### 5.1 · AI Tells(15 项,见 [`ai-tells.md`](../meta/ai-tells.md))

- [ ] 无 Tailwind 渐变文字 + 中性灰背景组合
- [ ] 非全场 `rounded-2xl`(至少 2 档圆角差异化)
- [ ] 无紫蓝粉渐变大面积背景
- [ ] 非 Inter / Geist 单字族(标题与正文有字体差异)
- [ ] 标题字距非统一 `tracking-tight`
- [ ] 短标题未滥用 `text-balance`
- [ ] 无三列等高卡片网格(feature 区)
- [ ] 容器宽度非全 `max-w-7xl`(差异化)
- [ ] 间距非全 `py-20`(节奏有变化)
- [ ] 无 lorem ipsum 残留
- [ ] 数字非 100/1k/10k 整数凑数
- [ ] 非三档定价 + 中间"Most Popular"(若 Pricing 区存在)
- [ ] 非默认 Lucide `Rocket/Zap/Shield` 三件套
- [ ] 无 `source.unsplash.com/random` 占位
- [ ] 字体非走 Google Fonts CDN 阻塞首屏

### 5.2 · Performance(10 项,见 [`performance.md`](../meta/performance.md))

- [ ] 所有图片含 `width` + `height` 或 `aspect-ratio`
- [ ] 字体含 `font-display: swap`
- [ ] 动画化属性仅限 `transform` / `opacity`
- [ ] grain/noise 用 `::before` 伪元素 + `position: fixed` + `pointer-events: none`
- [ ] `z-index` 全部 token 化(无魔法值)
- [ ] 首屏 JS ≤ 100KB gzip
- [ ] 长列表(> 100 项)用虚拟滚动
- [ ] `box-shadow` 大模糊(≥ 40px)慎用
- [ ] `backdrop-filter` 元素 ≤ 3 个
- [ ] `will-change` 非常驻(动画完成后移除)

### 5.3 · Accessibility · WCAG 对比度(8 项,见 [`accessibility.md`](../meta/accessibility.md))

- [ ] 所有正文文字对比度 ≥ 4.5:1
- [ ] 所有大文本对比度 ≥ 3:1
- [ ] UI 组件(border / 图标)对比度 ≥ 3:1
- [ ] `placeholder` 文字对比度 ≥ 4.5:1
- [ ] 暗色模式下对比度仍达标
- [ ] 非用纯红/纯绿表达信息(色盲友好)
- [ ] `disabled` 文字对比度 ≥ 3:1
- [ ] `focused` focus ring 对比度 ≥ 3:1

### 5.4 · Accessibility · 用户偏好(6 项)

- [ ] 装饰性动画含 `prefers-reduced-motion` 降级
- [ ] 视差 / pin / 横向平移在 reduced-motion 下完全禁用
- [ ] 暗色模式 token 通过 `prefers-color-scheme` 切换
- [ ] `backdrop-filter` 含 `prefers-reduced-transparency` 降级
- [ ] 半透明遮罩含 reduced-transparency 降级
- [ ] 双跑预览:默认 + reduced-motion,无信息丢失

### 5.5 · Accessibility · 交互可达(8 项)

- [ ] 所有交互元素 Tab 可达
- [ ] focus ring 可见(无 `outline: none` 无替代)
- [ ] 触摸目标 ≥ 44pt × 44pt
- [ ] 图片含 `alt`(装饰性 `alt=""`)
- [ ] 按钮无文字时含 `aria-label`
- [ ] 表单含 `<label>` 或 `aria-label`
- [ ] 页首含 "Skip to main content" 跳转链接
- [ ] DOM 顺序 = 视觉顺序(无正整数 `tabindex`)

### 5.6 · Token 完整性(10 项,见 [`token.md`](../meta/token.md))

- [ ] CSS 变量全部从 `:root` 读取,无 `{token-name}` 残留
- [ ] 无硬编码颜色(`#RRGGBB` 字面量在样式内联中)
- [ ] 无硬编码字号(`14px` / `16px` 等具体值,文档说明除外)
- [ ] 无硬编码间距
- [ ] z-index 全 token 化
- [ ] 暗色 token 在 `@media (prefers-color-scheme: dark)` 中覆盖
- [ ] Primitive → Semantic → Component 三层引用单向
- [ ] 组件引用 `{path.to.token}` 而非重复字面值
- [ ] Typography 复合对象字段完整(fontFamily/size/weight/lineHeight)
- [ ] 命名全部 kebab-case,无 camelCase / snake_case 混用

### 5.7 · 完整交互状态(8 项,见 [`principles.md`](../meta/principles.md) 第 14 定律)

- [ ] 所有按钮含 default / hover / pressed / focused / disabled 五态
- [ ] 所有可点击卡片含 hover / pressed 反馈
- [ ] Loading 状态有骨架 / spinner(> 200ms 操作)
- [ ] Empty 状态有插画 + 文案 + CTA
- [ ] Error 状态有错误说明 + 重试 CTA
- [ ] Tactile Feedback(`micro-press-scale` 或 `micro-hover-lift`)
- [ ] 状态过渡 duration ≤ 150ms(状态过渡)
- [ ] 表单提交后有 toast 反馈(成功 / 失败)

### 5.8 · LLM 截断信号(8 项,见 [`llm-behavior.md`](../meta/llm-behavior.md))

- [ ] 最后一个章节字数 ≥ 前面章节均值的 50%
- [ ] 代码块无 `// ...` / `// 其余类似` / `// TODO` 结尾
- [ ] 组件区有 ≥ 1 个组件的完整四态(不只 default)
- [ ] Do's and Don'ts ≥ 6 条(若 DESIGN.md 引用)
- [ ] 章节内容是真正的 X,非"该章节应包含 X"
- [ ] placeholder 占比 < 10%
- [ ] 文案具体(无"现代设计"等空泛词)
- [ ] 数字真实风(有尾数,非整数凑数)

### 5.9 · 第 13 定律 · 动画动机(7 项,见 [`principles.md`](../meta/principles.md))

- [ ] 每段动画可回答"为什么动"(状态变化 / 空间引导 / 反馈)
- [ ] 无装饰性循环动画(MOTION_INTENSITY ≤ 5 时)
- [ ] 入场动画 duration ≤ 600ms
- [ ] stagger 间隔 ≤ 120ms
- [ ] translateY 偏移 ≤ 30px(防眩晕)
- [ ] 缓动函数非默认 `linear`(用 ease-out / cubic-bezier)
- [ ] `ScrollTrigger.once: true` 或等价(避免反复触发)

**统计**:5.1 (15) + 5.2 (10) + 5.3 (8) + 5.4 (6) + 5.5 (8) + 5.6 (10) + 5.7 (8) + 5.8 (8) + 5.9 (7) = **80 项**

### Pre-Flight Check 执行规则

- 80 项均为**机械检查**(可脚本化,非主观判断)
- 任一项失败 = 硬性失败,不可降级为 warning
- 失败项必须列出具体位置(HTML 行号 / CSS 选择器)
- 修复后重跑全部 80 项(不可只跑失败项)
- 通过后进入第 6 节 Pre-Delivery Checklist(主观维度)

---

## 6. Pre-Delivery Checklist(5 维交付前检查)

> Pre-Flight Check 通过后的人工主观检查。5 个维度,每维度 1-5 分,任一维度 < 3 分不交付。来源:taste-skill。

### 维度 1 · Completeness(完整性)

- 设计是否覆盖所有页面章节?
- 组件是否覆盖 default + 状态变体?
- DESIGN.md 引用的 token 是否全部出现在产物中?
- 是否有"待补全"占位?

### 维度 2 · Correctness(正确性)

- 颜色对比度是否真的达标(不仅 Pre-Flight 项通过,实际场景也合理)?
- 间距是否符合 8px 网格(或 DESIGN.md 声明的 base)?
- 字体是否正确加载(无 fallback 到 system-ui)?
- 交互逻辑是否无矛盾(如 disabled 按钮可点击)?

### 维度 3 · Consistency(一致性)

- 跨页面间距 / 圆角 / 字号档位是否一致?
- 同类组件(如多个卡片)样式是否统一?
- 暗色模式与亮色模式视觉是否对应?
- 文案语气是否一致(同一称呼 / 同一术语)?

### 维度 4 · Brand Fit(品牌契合)

- 是否避免了 AI Tells 的"通用感"?
- 是否符合 [`product-reasoning.md`](../meta/product-reasoning.md) 推理的产品类型?
- 是否参考了 [`design-systems.md`](../dimensions/design-systems.md) 中的 1-2 个锚点?
- 视觉是否与品牌色 / 品牌字体一致?

### 维度 5 · Polish(完成度)

- 微动效是否丝滑(无闪烁 / 无跳帧)?
- 边界场景(空数据 / 长文本 / 错误)是否处理?
- 移动端布局是否真的可用(非仅"响应式")?
- 视觉细节(对齐 / 字距 / 阴影)是否到位?

### 评分规则

| 分数 | 含义                                   |
| ---- | -------------------------------------- |
| 5    | 优秀,可作为参考案例                   |
| 4    | 良好,可交付,小优化空间                |
| 3    | 及格,可交付但有可见问题                |
| 2    | 不及格,需返工(任一维度不可低于 3)   |
| 1    | 严重不及格,需重新设计                  |

**交付阈值**:5 维度全部 ≥ 3 分,且总分 ≥ 15 分。低于阈值不可交付,需返回 draw-md 修改。

**🔴 CHECKPOINT · 交付确认**:展示 5 维评分 + 总分,与用户确认后交付。低于阈值时明确说明"不可交付,需修复以下维度:[列表]"。

---

## 产出物

- 一个页面 → 一个 HTML 预览文件
- 文件命名:`preview_<page-name>_<device>.html`(如 `preview_home_iphone15.html`)
- 产出位置:用户指定目录(默认 `examples/preview/`)

---

## 约束汇总(硬性)

- [ ] 产出 HTML MUST 为自包含文件(CDN 引入 Element Plus,无本地构建依赖)
- [ ] 设备尺寸 MUST 从 `scripts/device_models.py` 读取,MUST NOT 硬编码在流程文档中
- [ ] 设备外壳 MUST 用纯 CSS 绘制(圆角 + 刘海 + 边框),MUST NOT 依赖图片资源
- [ ] Token 引用 MUST 解析为 CSS 变量值,MUST NOT 在产出 HTML 中残留 `{token-name}` 占位符
- [ ] 预览文件 MUST 可直接用浏览器打开(file:// 协议),MUST NOT 需要本地服务器

---

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
| -------- | -------- | ---------- |
| 设备尺寸不在 scripts/device_models.py | 提示用户从已支持设备中选择最接近的 | 用最接近尺寸替代,在预览 HTML 顶部标注"近似尺寸:实际 X×Y,使用 X'×Y'" |
| Element Plus CDN 不可达(离线环境) | 提示用户检查网络连接 | 引导用户下载 Element Plus 本地引用,提供本地引用代码片段 |
| UI markdown 缺少 token 引用(裸值) | 提示具体偏差(哪些值未引用 token) | 用 DESIGN.md 中的 token 替换裸值,标注"自动补全,需确认" |
| preview HTML 在浏览器中渲染异常 | 提示用户检查浏览器控制台错误 | 引导用户简化 UI markdown(移除复杂组件)后重试 |

---

## 禁止事项(反例)

- **禁止硬编码设备尺寸在流程文档中**:在 markdown 表格/正文写死宽高会与 `scripts/device_models.py` 脱节,设备更新时多处漂移。MUST 从 `scripts/device_models.py` 读取尺寸。
- **禁止用浏览器开发者工具手动改样式代替预览验证**:手动改值无法复现、不入产物,验证结果不可追溯。MUST 用 Element Plus 框架实时渲染生成自包含 HTML 预览。
- **禁止跳过 iOS/Android 双端验证**(只测一端):单端通过不代表另一端布局/字体一致,会遗漏平台差异。MUST 双端都跑预览校验。
- **禁止预览发现的问题只口头记录不写入修复清单**:口头记录易丢失,无法驱动下一轮迭代。MUST 输出到下一轮 `draw-md` 的输入(显式问题清单 + 对应组件/章节)。
- **禁止用模拟器截图代替真机预览**:模拟器颜色/字体渲染与真机有差异,关键页面视觉结论不可靠。关键页面 MUST 真机验证,模拟器仅用于布局快速校验。
