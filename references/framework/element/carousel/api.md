# Carousel API

> `<el-carousel>` 与 `<el-carousel-item>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-carousel 属性(Props)

| 属性名               | 类型                                      | 默认值    | 说明                              |
| -------------------- | ----------------------------------------- | --------- | --------------------------------- |
| `height`             | `string`                                  | —         | 高度(必填,如 `'200px'`)        |
| `initial-index`      | `number`                                  | `0`       | 初始幻灯片索引                    |
| `initial-index`      | `number`                                  | `0`       | 初始索引                          |
| `trigger`            | `'hover' \| 'click'`                      | `'hover'` | 指示器触发方式                    |
| `autoplay`           | `boolean`                                 | `true`    | 是否自动切换                      |
| `interval`           | `number`                                  | `3000`    | 自动切换间隔(ms)                |
| `indicator-position` | `'outside' \| 'none'`                     | —         | 指示器位置                        |
| `arrow`              | `'always' \| 'hover' \| 'never'`          | `'hover'` | 切换箭头显示时机                  |
| `type`               | `'card'`                                  | —         | 模式,card 为卡片化               |
| `loop`               | `boolean`                                 | `true`    | 是否循环                          |
| `direction`          | `'horizontal' \| 'vertical'`              | `'horizontal'` | 方向                       |
| `pause-on-hover`     | `boolean`                                 | `true`    | 鼠标悬停是否暂停                  |

## el-carousel-item 属性(Props)

| 属性名  | 类型      | 默认值 | 说明                          |
| ------- | --------- | ------ | ----------------------------- |
| `name`  | `string`  | —      | 幻灯片名称(用于 setActiveItem) |
| `label`| `string`  | —      | 指示器文字                    |

## el-carousel 事件(Events)

| 事件名    | 回调签名                                  | 说明                       |
| --------- | ----------------------------------------- | -------------------------- |
| `change`  | `(current: number, prev: number) => void` | 切换时触发                 |

## el-carousel 方法(Methods)

| 方法名            | 签名                                    | 说明                            |
| ----------------- | --------------------------------------- | ------------------------------- |
| `setActiveItem`   | `(index: number \| name: string) => void` | 切换到指定幻灯片              |
| `prev`            | `() => void`                            | 上一张                          |
| `next`            | `() => void`                            | 下一张                          |

## 插槽(Slots)

| 组件               | 插槽名    | 说明           |
| ------------------ | --------- | -------------- |
| `el-carousel`      | `default` | 幻灯片容器     |
| `el-carousel-item` | `default` | 单页内容       |
