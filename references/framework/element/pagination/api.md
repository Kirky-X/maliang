# Pagination API

> `<el-pagination>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名                  | 类型                  | 默认值                                | 说明                              |
| ----------------------- | --------------------- | ------------------------------------- | --------------------------------- |
| `total`                 | `number`              | —                                     | 总条数                            |
| `current-page` / `v-model` | `number`           | `1`                                   | 当前页                            |
| `page-size` / `v-model:page-size` | `number`     | `10`                                  | 每页条数                          |
| `default-current-page`  | `number`              | —                                     | 默认当前页(非受控)            |
| `default-page-size`     | `number`              | —                                     | 默认每页条数(非受控)          |
| `page-count`            | `number`              | —                                     | 总页数(替代 total)            |
| `pager-count`           | `number`              | `7`                                   | 页码按钮数                        |
| `page-sizes`            | `number[]`            | `[10, 20, 30, 40, 50, 100]`           | 可选每页条数                      |
| `layout`                | `string`              | `'prev, pager, next, jumper, ->, total'` | 布局组合                       |
| `small`                 | `boolean`             | `false`                               | 是否小型                          |
| `background`            | `boolean`             | `false`                               | 是否带背景                        |
| `hide-on-single-page`   | `boolean`             | `false`                               | 只有一页时是否隐藏                |
| `prev-text`             | `string`              | —                                     | 上一页文字                        |
| `next-text`             | `string`              | —                                     | 下一页文字                        |
| `disabled`              | `boolean`             | `false`                               | 是否禁用                          |

## 事件(Events)

| 事件名            | 回调签名                | 说明                       |
| ----------------- | ----------------------- | -------------------------- |
| `size-change`     | `(size: number) => void`| 每页条数变化               |
| `current-change`  | `(page: number) => void`| 当前页变化                 |
| `prev-click`      | `(page: number) => void`| 点击上一页                 |
| `next-click`      | `(page: number) => void`| 点击下一页                 |

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

`<el-pagination>` 不提供专用插槽,布局通过 `layout` 字符串控制。
