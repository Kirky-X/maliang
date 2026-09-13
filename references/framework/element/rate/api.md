# Rate API

> `<el-rate>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-rate 属性(Props)

| 属性名            | 类型                                     | 默认值                 | 说明                                       |
| ----------------- | ---------------------------------------- | ---------------------- | ------------------------------------------ |
| `model-value` / `v-model` | `number`                          | `0`                    | 绑定分数                                   |
| `max`             | `number`                                 | `5`                    | 星星总数                                   |
| `disabled`        | `boolean`                                | `false`                | 只读展示(输入禁用)                     |
| `allow-half`      | `boolean`                                | `false`                | 支持半星                                   |
| `low-threshold`   | `number`                                 | `2`                    | 低分/中分档界                              |
| `high-threshold`  | `number`                                 | `4`                    | 中分/高分档界                              |
| `colors`          | `string[] \| Record<number, string>`     | 亮色蓝梯度             | 分数档颜色(可用 token)                  |
| `void-color`      | `string`                                 | 灰色                   | 未选星色,建议 `{color-bg-secondary}`     |
| `disabled-void-color` | `string`                             | 灰色                   | 只读态未选星色                             |
| `icon-classes`    | `string[] \| Record<number, string>`     | `StarFilled` 等        | 各档图标                                   |
| `void-icon-class` | `string`                                 | —                      | 未选图标                                   |
| `show-text`       | `boolean`                                | `false`                | 显示档位文案                               |
| `show-score`      | `boolean`                                | `false`                | 显示当前分数                               |
| `text-color`      | `string`                                 | —                      | 文案颜色                                   |
| `texts`           | `string[]`                               | 极差/失望/一般/满意/惊喜 | 五档文案(配 show-text)                 |
| `score-template`  | `string`                                 | `'{value}'`            | 分数模板                                   |
| `clearable`       | `boolean`                                | `false`                | 再次点击同星可清零                         |
| `size`            | `'large' \| 'default' \| 'small'`        | —                      | 尺寸                                       |
| `aria-label`      | `string`                                 | `'Rating'`             | 无障碍标签                                 |

## 事件(Events)

| 事件名   | 回调签名                  | 说明                       |
| -------- | ------------------------- | -------------------------- |
| `change` | `(value: number) => void` | 分数变化时触发             |

## 方法 / 插槽

- 无对外方法。
- 插槽:`default` / `text`(自定义档位文案区域)。

## 关键规格要点

- **输入 vs 展示**:录入用默认态(可 `clearable`);列表/详情展示一律 `disabled`,分数经 `score-template` 保留一位小数。
- **半星**:`allow-half` 后步长 0.5;展示侧同支持半星渲染。
- **尺寸**:默认星 18px,`large` 24px,`small` 14px。
- **无障碍**:渲染为滑杆语义(`aria-valuenow` 自动维护);`aria-label` 按业务覆盖(如"商品评分");只读态对读屏播报"4.5 分,满分 5 分"。
- **无分控评**:0 分/无数据不渲染星阵,用"暂无评分"文案兜底。
