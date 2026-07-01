# Loading API

> `v-loading` 指令参数、`ElLoadingService` 选项与实例方法。用法见 [component.md](./component.md)。

## v-loading 指令修饰符

| 修饰符       | 说明                            |
| ------------ | ------------------------------- |
| `fullscreen` | 全屏遮罩                        |
| `lock`       | 全屏时锁定 body 滚动            |
| `body`       | 遮罩插入到 body 而非当前元素    |

## v-loading 自定义属性(通过 element-loading-* 传递)

| 属性名                          | 类型                | 说明                |
| ------------------------------- | ------------------- | ------------------- |
| `element-loading-text`          | `string`            | 加载文字            |
| `element-loading-background`    | `string`            | 遮罩背景色          |
| `element-loading-spinner`       | `string`            | 自定义图标类        |
| `element-loading-svg`           | `string`            | 自定义 SVG          |
| `element-loading-svg-view-box`  | `string`            | SVG viewBox         |

## ElLoadingService 选项

| 属性名        | 类型                                   | 默认值   | 说明                          |
| ------------- | -------------------------------------- | -------- | ----------------------------- |
| `target`      | `string \| HTMLElement`                | `body`   | 挂载目标                      |
| `fullscreen`  | `boolean`                              | `false`  | 是否全屏                      |
| `lock`        | `boolean`                              | `false`  | 是否锁定滚动                  |
| `text`        | `string`                               | —        | 加载文字                      |
| `background`  | `string`                               | —        | 遮罩背景                      |
| `customClass` | `string`                               | —        | 自定义类名                    |
| `body`        | `boolean`                              | `false`  | 是否插入 body                 |
| `spinner`     | `string`                               | —        | 图标类                        |
| `svg`         | `string`                               | —        | 自定义 SVG                    |
| `svgViewBox`  | `string`                               | —        | SVG viewBox                   |

## 实例方法

| 方法名  | 签名         | 说明            |
| ------- | ------------ | --------------- |
| `close` | `() => void` | 关闭加载        |

## 事件 / 插槽

`v-loading` 指令与 `ElLoadingService` 均无事件与插槽(图标与文字通过选项配置)。
