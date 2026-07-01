# Radio 组件 API 文档

> ArkTS 单选框组件,`Radio`(单选项)+ `RadioGroup`(单选组)。同名 `Radio` 自动归组,也可用 `RadioGroup` 容器显式分组。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `Radio` | 单个单选项 |
| `RadioGroup` | 单选组容器,管理组内 Radio 互斥 |

## Radio 构造函数

```arkts
Radio(value: { group: string; value: string })
// group: 组名;value: 该项的值
```

## RadioGroup 构造函数

```arkts
RadioGroup(value?: { group?: string })
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| checked | boolean | 是否选中 |
| group | string | 组名(同组互斥) |
| value | string | 选项值 |
| onChange | (isChecked: boolean) => void | 选中状态变化回调 |

## RadioGroup 事件

| 事件 | 说明 |
| --- | --- |
| onChange | (value: string) => void 选中项的 value |

## 最小示例

```arkts
@Entry
@Component
struct RadioDemo {
  @State gender: string = 'male'
  build() {
    Column({ space: {spacing-sm} }) {
      RadioGroup({ group: 'gender' }) {
        Radio({ group: 'gender', value: 'male' }).checked(true)
        Text('男').fontSize({font-size-md})
        Radio({ group: 'gender', value: 'female' })
        Text('女').fontSize({font-size-md})
      }
      .onChange((v: string) => this.gender = v)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`switch`](../switch/component.md) — 开关(Toggle)单选二态
- [`input`](../input/component.md) — 表单输入

## 参考链接

- ArkTS 官方文档 - 单选框 (Radio): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-radio-button
