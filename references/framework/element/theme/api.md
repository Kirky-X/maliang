# Theme API(主题变量)

> 本文件列出常用 Element Plus CSS 变量与 SCSS 变量,便于与 design token 建立映射。无组件属性/事件/方法/插槽。

## 核心 CSS 变量(运行时覆盖)

### 颜色

| CSS 变量                       | 默认值     | 说明                | 建议 token 映射          |
| ------------------------------ | ---------- | ------------------- | ------------------------ |
| `--el-color-primary`           | `#409eff`  | 主色                | `{color-primary}`        |
| `--el-color-success`           | `#67c23a`  | 成功色              | `{color-success}`        |
| `--el-color-warning`           | `#e6a23c`  | 警告色              | `{color-warning}`        |
| `--el-color-danger`            | `#f56c6c`  | 危险色              | `{color-danger}`         |
| `--el-color-info`              | `#909399`  | 信息色              | `{color-info}`           |
| `--el-text-color-primary`      | `#303133`  | 主要文字            | `{color-text-primary}`   |
| `--el-text-color-regular`      | `#606266`  | 常规文字            | `{color-text-secondary}` |
| `--el-bg-color`                | `#ffffff`  | 容器背景            | `{color-bg-primary}`     |
| `--el-bg-color-page`           | `#f2f3f5`  | 页面背景            | `{color-bg-secondary}`   |
| `--el-border-color`            | `#dcdfe6`  | 边框                | `{color-border-default}` |

### 圆角 / 间距

| CSS 变量                  | 默认值 | 说明       | 建议 token 映射 |
| ------------------------- | ------ | ---------- | --------------- |
| `--el-border-radius-base` | `4px`  | 基础圆角   | `{radius-sm}`   |
| `--el-border-radius-small`| `2px`  | 小圆角     | `{radius-sm}`   |
| `--el-border-radius-round`| `20px` | 圆角       | `{radius-lg}`   |
| `--el-border-radius-circle`| `100%`| 正圆       | `{radius-full}` |

### 字号

| CSS 变量                  | 默认值  | 说明       | 建议 token 映射 |
| ------------------------- | ------- | ---------- | --------------- |
| `--el-font-size-base`     | `14px`  | 基础字号   | `{font-size-md}`|
| `--el-font-size-small`    | `13px`  | 小字号     | `{font-size-sm}`|
| `--el-font-size-large`    | `18px`  | 大字号     | `{font-size-lg}`|

## SCSS 变量(构建时覆盖)

在 `@forward 'element-plus/theme-chalk/src/common/var.scss' with (...)` 中覆盖,主要分组:

| SCSS 变量组       | 说明                          |
| ----------------- | ----------------------------- |
| `$colors`         | 各功能色基础值及明暗派生      |
| `$border-radius`  | 圆角预设                      |
| `$font-size`      | 字号预设                      |
| `$spacing`        | 间距预设                      |
| `$box-shadow`     | 阴影预设                      |

## 暗色模式

通过为根元素添加 `.dark` 类,并用 `html.dark { ... }` 覆盖上述变量实现。Element Plus 内置 `element-plus/theme-chalk/dark/css-vars.css` 提供默认暗色变量。
