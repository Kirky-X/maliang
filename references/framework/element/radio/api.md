# Radio API

> `<el-radio>` / `<el-radio-group>` / `<el-radio-button>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-radio-group 属性(Props)

| 属性名           | 类型                              | 默认值     | 说明                          |
| ---------------- | --------------------------------- | ---------- | ----------------------------- |
| `model-value` / `v-model` | `string \| number \| boolean` | —  | 绑定值                        |
| `size`           | `'large' \| 'default' \| 'small'` | —          | 尺寸                          |
| `disabled`       | `boolean`                         | `false`    | 是否禁用                      |
| `text-color`     | `string`                          | `'#ffffff'`| 按钮激活时文字色              |
| `fill`           | `string`                          | `'#409eff'`| 按钮激活时填充色              |

## el-radio 属性(Props)

| 属性名     | 类型                              | 默认值 | 说明                          |
| ---------- | --------------------------------- | ------ | ----------------------------- |
| `model-value` / `v-model` | `string \| number \| boolean` | — | 单个 radio 的绑定值(独立使用) |
| `label`    | `string \| number \| boolean`     | —      | Radio 的值                    |
| `disabled` | `boolean`                         | `false`| 是否禁用                      |
| `border`   | `boolean`                         | `false`| 是否显示边框                  |
| `size`     | `'large' \| 'default' \| 'small'` | —      | 尺寸(边框模式下)           |
| `name`     | `string`                          | —      | 原生 name 属性                |

## el-radio-button 属性(Props)

| 属性名     | 类型                              | 默认值 | 说明            |
| ---------- | --------------------------------- | ------ | --------------- |
| `label`    | `string \| number \| boolean`     | —      | Radio 的值      |
| `disabled` | `boolean`                         | `false`| 是否禁用        |
| `size`     | `'large' \| 'default' \| 'small'` | —      | 尺寸            |
| `name`     | `string`                          | —      | 原生 name 属性  |

## el-radio / el-radio-group 事件(Events)

| 事件名    | 回调签名                             | 说明                       |
| --------- | ------------------------------------ | -------------------------- |
| `change`  | `(value: string \| number \| boolean) => void` | 绑定值变化时触发 |

## 方法 / 插槽

- 无对外方法。
- 插槽:`default`(标签文字)。

```vue
<el-radio label="1">
  <el-icon><User /></el-icon>
  <span>用户</span>
</el-radio>
```
