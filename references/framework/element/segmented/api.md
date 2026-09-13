# Segmented API

> `<el-segmented>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-segmented 属性(Props)

| 属性名           | 类型                                              | 默认值   | 说明                                     |
| ---------------- | ------------------------------------------------- | -------- | ---------------------------------------- |
| `model-value` / `v-model` | `string \| number \| boolean`            | —        | 绑定值(对应 option 的 value)          |
| `options`        | `Array<string \| number \| boolean \| Option>`    | 必填     | 选项(Option:`{ label, value, disabled }`)|
| `size`           | `'large' \| 'default' \| 'small'`                 | —        | 尺寸                                     |
| `block`          | `boolean`                                         | `false`  | 撑满容器宽度                             |
| `disabled`       | `boolean`                                         | `false`  | 是否禁用                                 |
| `validate-event` | `boolean`                                         | `true`   | 是否触发表单校验                         |
| `name`           | `string`                                          | —       | 原生 name 属性                           |
| `id`             | `string`                                          | —       | 原生 id 属性                             |
| `aria-label`     | `string`                                          | —       | 无障碍标签                               |

## 事件(Events)

| 事件名   | 回调签名                              | 说明                       |
| -------- | ------------------------------------- | -------------------------- |
| `change` | `(val: string \| number \| boolean) => void` | 选中段变化时触发 |

## 方法 / 插槽

- 无对外方法。
- 插槽:`default`(作用域插槽,`{ item }` 自定义选项内容)。

## 与相邻组件的分工

| 维度 | `el-segmented`(本类) | `el-tabs`(tabs 类) | `el-radio-group`(radio 类) |
| ---- | ---------------------- | --------------------- | --------------------------- |
| 语义 | 视图/筛选状态切换      | 页面级内容区切换      | 表单互斥录入                |
| 项数 | 2-5                    | 不限(含内容区)      | 不限                        |
| 外观 | 胶囊分段,选中滑移     | 下划线/卡片页签       | 圆点单选                    |
| 典型 | 日/周/月、地图图层     | 商品详情多页签        | 支付方式                    |

## 关键规格要点

- **尺寸**:默认高 32px,`large` 40px,`small` 24px;`block` 时撑满容器均分。
- **项数**:2-5 项;超 5 项转 tabs;需要多选时本组件不适用(用 checkbox)。
- **无障碍**:渲染为 `role="radiogroup"` 互斥组,方向键切换;`aria-label` 必须声明;图标段须保证文字可读或补语义。
- **CSS 变量**:`--el-segmented-item-selected-bg-color` / `--el-segmented-item-selected-color` 用 token 注入,勿硬编码。
