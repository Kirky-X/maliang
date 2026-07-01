# Shape API(汇总)

> 本文件汇总 Border/Divider/Watermark 三个组件的属性速览。Divider 完整 API 见 [../divider/api.md](../divider/api.md)。

## Border 边框(工具类)

Border 为纯 CSS 工具类,无组件属性。常用类名:

| 类名                | 说明                          |
| ------------------- | ----------------------------- |
| `el-border`         | 基础边框(1px 实线)          |
| `el-border-top`     | 仅上边框                      |
| `el-border-bottom`  | 仅下边框                      |
| `el-rounded`        | 圆角,映射 {radius-sm}        |
| `el-rounded-full`   | 全圆角,映射 {radius-full}    |
| `el-shadow`         | 基础阴影                      |
| `el-shadow-hover`   | 悬浮阴影                      |

> 自定义项目应使用 design token(`{radius-sm}` / `{color-border-default}`)而非直接套类,以保持主题一致。

## el-divider 属性

| 属性名               | 类型                          | 默认值      | 说明                       |
| -------------------- | ----------------------------- | ----------- | -------------------------- |
| `direction`          | `'horizontal' \| 'vertical'`  | `'horizontal'` | 方向                    |
| `content-position`   | `'left' \| 'center' \| 'right'` | `'center'` | 文字位置                 |
| `border-style`       | `'none' \| 'solid' \| 'dashed' \| 'dotted' \| 'double'` | `'solid'` | 边框样式 |
| `icon`               | `string \| Component`         | —           | 自定义图标                 |

插槽:`default` 分割线文字、`icon`(被 `icon` 属性替代)。完整定义见 [../divider/api.md](../divider/api.md)。

## el-watermark 属性

| 属性名        | 类型                | 默认值 | 说明                                |
| ------------- | ------------------- | ------ | ----------------------------------- |
| `width`       | `number`            | `120`  | 水印宽度                            |
| `height`      | `number`            | `64`   | 水印高度                            |
| `content`     | `string \| string[]`| —      | 水印内容,数组为多行                |
| `gap`         | `[number, number]`  | `[0,0]`| 水印间距 [x, y]                     |
| `offset`      | `[number, number]`  | `['50%','50%']` | 水印偏移                  |
| `rotate`      | `number`            | `-22`  | 旋转角度                            |
| `z-index`     | `number`            | `9`    | 层级                                |
| `font`        | `object`            | —      | 字体配置 { color, fontSize, ... }  |
| `image`       | `string`            | —      | 图片水印地址(优先于 content)     |
| `monospace`   | `boolean`           | `false`| 是否等宽字体                        |
| `inherit`     | `boolean`           | `true` | 子节点是否继承水印                  |

## 事件 / 方法 / 插槽

el-divider 与 el-watermark 均无对外事件与方法。el-divider 有 `default` 插槽(文字);el-watermark 有 `default` 插槽(被保护内容)。
