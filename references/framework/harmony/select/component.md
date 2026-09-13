# Select 组件 API 文档

> ArkTS 下拉选择器组件 `Select`(API 10+ 原生)。用于表单内**数据录入**——从选项集中选定一个值(区别于 `Menu`/`Dropdown` 的动作菜单语义)。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `Select` | 下拉选择器,点击展开选项列表,选定值回填 |
| `TextPicker` | 滚轮选择器(备选,滑轮档位交互) |

> 与 [`dropdown`](../dropdown/component.md)(动作菜单)区分:Select 提交值到表单状态,Dropdown 触发命令。

## Select 构造函数

```arkts
Select(options: SelectOption[] | Array<SelectOption>)
// SelectOption { value: ResourceStr; icon?: ResourceStr }
```

## 核心属性(链式)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| selected | number \| undefined | 当前选中项索引 |
| value | ResourceStr | 当前选中项文本 |
| font / fontColor / backgroundColor | — | 触发器文本与背景样式 |
| optionWidth / optionHeight | Dimension | 下拉面板尺寸 |
| space | Dimension | 触发器与面板间距 |

## 事件

| 事件 | 说明 |
| --- | --- |
| onSelected | (index: number, value: string) => void 选中某项 |
| onSelectChange | (index: number, value?: string) => void 展开/收起时选中项变化 |

## 最小示例

```arkts
@Entry
@Component
struct SelectDemo {
  @State city: string = '请选择'
  private cities: SelectOption[] = [
    { value: '上海' },
    { value: '北京' },
    { value: '广州' }
  ]
  build() {
    Column({ space: {spacing-md} }) {
      Text('城市').fontSize({font-size-md})
      Select(this.cities)
        .selected(0)
        .value(this.city)
        .font({ size: {font-size-md} })
        .fontColor({color-text-primary})
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-md})
        .onSelected((index: number, value: string) => this.city = value)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`dropdown`](../dropdown/component.md) — 动作菜单(命令触发,非数据录入)
- [`input`](../input/component.md) — 文本输入
- [`checkbox`](../checkbox/component.md) — 多选

## 参考链接

- ArkTS 官方文档 - Select: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-basic-components-select
- ArkTS API 参考 - TextPicker: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-basic-components-textpicker
