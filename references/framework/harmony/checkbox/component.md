# Checkbox 组件 API 文档

> ArkTS 复选框组件 `Checkbox`(单选项)+ `CheckboxGroup`(多选组)。同名 `Checkbox` 通过 `group` 归组,支持全选联动。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `Checkbox` | 单个复选项 |
| `CheckboxGroup` | 多选组容器,管理组内全选/反选 |

## Checkbox 构造函数

```arkts
Checkbox(value: { name?: string; group?: string })
// name: 该项标识;group: 组名(同组受 CheckboxGroup 管理)
```

## CheckboxGroup 构造函数

```arkts
CheckboxGroup(value?: { group?: string })
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| selected | boolean | 是否选中 |
| selectAll | boolean | 组内是否全选(仅 CheckboxGroup) |
| selectedColor | ResourceColor | 选中态颜色 |
| onChange | (isChecked: boolean) => void | 选中状态变化回调 |

## CheckboxGroup 事件

| 事件 | 说明 |
| --- | --- |
| onChange | (itemName: CheckboxGroupResult) => void,含 name/status 列表 |

## 最小示例

```arkts
@Entry
@Component
struct CheckboxDemo {
  @State checked: boolean = false
  build() {
    Row({ space: {spacing-sm} }) {
      Checkbox({ name: 'agree', group: 'terms' })
        .select(this.checked)
        .selectedColor({color-primary})
        .onChange((isChecked: boolean) => this.checked = isChecked)
      Text('我已阅读并同意服务条款').fontSize({font-size-md})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`radio`](../radio/component.md) — 互斥单选
- [`switch`](../switch/component.md) — 二态开关
- [`select`](../select/component.md) — 下拉选择器

## 参考链接

- ArkTS 官方文档 - 复选框 (Checkbox): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-checkbox
- ArkTS API 参考 - CheckboxGroup: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-basic-components-checkboxgroup
