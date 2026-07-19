# Calendar Component API Documentation

> ArkTS calendar components `Calendar` / `CalendarPicker`, used for date selection and calendar display.

## Component Definition

| Component | Purpose |
| --- | --- |
| `Calendar` | Calendar display (may require calendar service integration) |
| `CalendarPicker` | Date picker (standalone component, dialog or embedded) |

## Core Properties (CalendarPicker Reference)

| Property | Type | Description |
| --- | --- | --- |
| selectedDate | Date | Currently selected date |
| startDate / endDate | Date | Selectable range |
| onDateChange | (date: Date) => void | Date change callback |
| onAccept | (date: Date) => void | Confirmation callback |

## Common Date Selection Alternatives

Due to `CalendarPicker` availability varying across API versions, common alternatives include:
- `DatePicker` — wheel-style date selection (year/month/day three columns)
- `DatePickerDialog` — date selection dialog

## DatePickerDialog Usage

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

## Minimal Example

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

## Related Components

- [`input`](../input/component.md) — Date can be input into TextInput
- [`dialog`](../dialog/component.md) — Date selection dialog

## Reference Links

- ArkTS Official Documentation: No independent chapter (Calendar/CalendarPicker scattered across API documentation)
- Related components: [`input`](../input/component.md) / [`dialog`](../dialog/component.md)
- Dialog Overview: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-dialog-overview