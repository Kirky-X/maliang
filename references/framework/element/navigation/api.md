# Navigation API(分组速览)

> 本文件为导航分组的属性速览。各组件完整 API 见对应单独目录的 api.md。

## el-affix

| 属性名      | 类型      | 默认值   | 说明                         |
| ----------- | --------- | -------- | ---------------------------- |
| `offset`    | `number`  | `0`      | 偏移距离(px)               |
| `position`  | `'top' \| 'bottom'` | `'top'` | 固定位置              |
| `z-index`   | `number`  | `100`    | 层级                         |
| `target`    | `string`  | —        | 触发固定的容器选择器         |

事件:`fixed` `(value: boolean) => void`、`change` `(value: boolean) => void`。

## el-backtop

| 属性名        | 类型             | 默认值  | 说明                          |
| ------------- | ---------------- | ------- | ----------------------------- |
| `target`      | `string`         | —       | 触发滚动的容器选择器          |
| `visibility-height` | `number`   | `200`   | 滚动高度达到此值才显示        |
| `right`       | `number`         | `40`    | 距右距离(px)                |
| `bottom`      | `number`         | `40`    | 距底距离(px)                |

事件:`click` `(evt: MouseEvent) => void`。插槽:`default` 自定义内容。

## el-breadcrumb / el-breadcrumb-item

| 属性名        | 类型     | 默认值   | 说明                       |
| ------------- | -------- | -------- | -------------------------- |
| `separator`   | `string` | `'/'`    | el-breadcrumb 分隔符       |
| `separator-icon` | `Component` | —   | 图标分隔符                 |
| `to`          | `object` | —        | el-breadcrumb-item 路由跳转 |
| `replace`     | `boolean`| `false`  | 是否 replace 路由          |

## el-menu 速览

| 属性名            | 类型                                    | 默认值     | 说明                |
| ----------------- | --------------------------------------- | ---------- | ------------------- |
| `mode`            | `'horizontal' \| 'vertical'`            | `'vertical'` | 模式               |
| `default-active`  | `string`                                | —          | 默认激活项          |
| `collapse`        | `boolean`                               | `false`    | 是否折叠            |
| `background-color`| `string`                                | —          | 菜单背景色          |
| `text-color`      | `string`                                | —          | 菜单文字色          |
| `active-text-color`| `string`                               | —          | 激活项文字色        |
| `unique-opened`   | `boolean`                               | `false`    | 是否只保持一个展开  |

## el-steps / el-step 速览

| 属性名        | 类型                                       | 默认值  | 说明                       |
| ------------- | ------------------------------------------ | ------- | -------------------------- |
| `space`       | `number \| string`                         | —       | el-steps 间距              |
| `direction`   | `'vertical' \| 'horizontal'`               | `'horizontal'` | 方向               |
| `active`      | `number`                                   | `0`     | 当前步骤                   |
| `process-status` | `'wait' \| 'process' \| 'finish' \| 'error' \| 'success'` | `'process'` | 当前步骤状态 |
| `align-center`| `boolean`                                  | `false` | 居中对齐                   |

el-step 属性:`title` / `description` / `icon` / `status`。
