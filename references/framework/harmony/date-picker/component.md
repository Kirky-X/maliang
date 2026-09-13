# DatePicker 组件 API 文档

> ArkTS 日期时间选择组件:`DatePickerDialog` / `TimePickerDialog`(弹窗式录入)与 `DatePicker` / `TimePicker`(内嵌组件)。用于表单**日期/时间录入**,与展示型 [`calendar`](../calendar/component.md)(浏览用途)区分。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `DatePicker` | 内嵌日期滚轮/日历选择 |
| `DatePickerDialog` | 日期选择弹窗(`DatePickerDialog.show`) |
| `TimePicker` | 内嵌时间滚轮选择 |
| `TimePickerDialog` | 时间选择弹窗(`TimePickerDialog.show`) |

## 核心构造/调用

```arkts
DatePickerDialog.show({
  start: new Date('2020-01-01'),
  end: new Date('2030-12-31'),
  selected: new Date(),
  lunar: false,
  onDateAccept: (value: Date) => {}
})

TimePickerDialog.show({
  selected: new Date(),
  useMilitaryTime: true,
  onAccept: (value: TimePickerResult) => {}
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| start / end | Date | 可选范围 |
| selected | Date | 当前选中值 |
| lunar | boolean | 是否农历展示 |
| onDateAccept / onAccept | 回调 | 确认选择回调 |
| onDateChange | 回调 | 滚动过程中实时变化 |

## 最小示例

```arkts
@Entry
@Component
struct DatePickerDemo {
  @State date: string = '请选择日期'
  build() {
    Column({ space: {spacing-md} }) {
      Text('入住日期').fontSize({font-size-md})
      Text(this.date)
        .fontSize({font-size-md})
        .fontColor(this.date === '请选择日期' ? {color-text-secondary} : {color-text-primary})
        .padding({spacing-md})
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-md})
        .onClick(() => {
          DatePickerDialog.show({
            selected: new Date(),
            onDateAccept: (value: Date) => {
              this.date = `${value.getFullYear()}-${value.getMonth() + 1}-${value.getDate()}`
            }
          })
        })
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`calendar`](../calendar/component.md) — 展示型日历(浏览,非录入)
- [`input`](../input/component.md) — 文本输入

## 参考链接

- ArkTS API 参考 - DatePickerDialog: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/js-apis-datepickerdialog
- ArkTS API 参考 - TimePickerDialog: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/js-apis-timepickerdialog
