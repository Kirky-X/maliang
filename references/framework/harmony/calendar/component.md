# Calendar 组件 API 文档

> ArkTS 日历组件 `Calendar` / `CalendarPicker`,用于日期选择与日历展示。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `Calendar` | 日历展示(可能需配合日历服务) |
| `CalendarPicker` | 日期选择器(独立组件,弹窗或内嵌) |

## 核心属性(CalendarPicker 参考)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| selectedDate | Date | 当前选中日期 |
| startDate / endDate | Date | 可选范围 |
| onDateChange | (date: Date) => void | 日期变化回调 |
| onAccept | (date: Date) => void | 确认回调 |

## 通用日期选择替代方案

由于 `CalendarPicker` 在不同 API 版本可用性不一,常用替代:
- `DatePicker` — 滚轮式日期选择(年/月/日三列)
- `DatePickerDialog` — 日期选择弹窗

## DatePickerDialog 用法

```arkts
DatePickerDialog.show({
  start: new Date('2020-01-01'),
  end: new Date('2030-12-31'),
  selected: new Date(),
  onAccept: (value: DatePickerResult) => {
    console.info(`${value.year}-${value.month + 1}-${value.day}`)
  }
})
```

## 最小示例

```arkts
@Entry
@Component
struct CalendarDemo {
  build() {
    Column() {
      Button('选择日期')
        .onClick(() => {
          DatePickerDialog.show({
            selected: new Date(),
            onAccept: (v: DatePickerResult) => console.info(`${v.year}-${v.month + 1}-${v.day}`)
          })
        })
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`input`](../input/component.md) — 日期可输入到 TextInput
- [`dialog`](../dialog/component.md) — 日期选择弹窗

## 参考链接

- ArkTS 官方文档:无独立章节(Calendar/CalendarPicker 散见各 API 文档)
- 相关组件:[`input`](../input/component.md) / [`dialog`](../dialog/component.md)
- 弹窗概述: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-dialog-overview
