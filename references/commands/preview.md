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
