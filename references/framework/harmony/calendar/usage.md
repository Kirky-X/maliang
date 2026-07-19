# Calendar Usage Scenarios and Examples

> Lists typical usage scenarios for ArkTS calendar/date selection. All colors, spacing, and border-radius are referenced via design tokens.

## Scenario 1: Date Selection Dialog (DatePickerDialog)

```arkts
@Entry
@Component
struct DatePickPage {
  @State dateStr: string = '请选择日期'
  build() {
    Column() {
      Text(this.dateStr).fontSize({font-size-md}).padding({spacing-md})
      Button('选择日期')
        .onClick(() => {
          DatePickerDialog.show({
            start: new Date('2020-01-01'),
            end: new Date('2030-12-31'),
            selected: new Date(),
            onAccept: (v: DatePickerResult) => {
              this.dateStr = `${v.year}-${(v.month + 1).toString().padStart(2, '0')}-${v.day.toString().padStart(2, '0')}`
            }
          })
        })
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## Scenario 2: Time Selection (TimePickerDialog)

```arkts
@Entry
@Component
struct TimePickPage {
  @State timeStr: string = '请选择时间'
  build() {
    Column() {
      Text(this.timeStr).fontSize({font-size-md})
      Button('选择时间')
        .onClick(() => {
          TimePickerDialog.show({
            selected: new Date(),
            onAccept: (v: TimePickerResult) => {
              this.timeStr = `${v.hour.toString().padStart(2, '0')}:${v.minute.toString().padStart(2, '0')}`
            }
          })
        })
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## Scenario 3: Date Range Selection (Two DatePickers)

```arkts
@Entry
@Component
struct DateRangePage {
  @State start: string = ''
  @State end: string = ''
  build() {
    Row({ space: {spacing-sm} }) {
      Text(this.start || '开始日期')
        .fontSize({font-size-sm}).padding({spacing-sm})
        .backgroundColor({color-bg-secondary}).borderRadius({radius-md})
        .onClick(() => DatePickerDialog.show({
          selected: new Date(),
          onAccept: (v) => this.start = `${v.year}-${v.month + 1}-${v.day}`
        }))
      Text('至').fontSize({font-size-sm})
      Text(this.end || '结束日期')
        .fontSize({font-size-sm}).padding({spacing-sm})
        .backgroundColor({color-bg-secondary}).borderRadius({radius-md})
        .onClick(() => DatePickerDialog.show({
          selected: new Date(),
          onAccept: (v) => this.end = `${v.year}-${v.month + 1}-${v.day}`
        }))
    }
    .padding({spacing-md})
  }
}
```

## Scenario 4: Embedded Calendar (Custom Grid Implementation)

When CalendarPicker is not available, use Grid to implement a monthly calendar.

```arkts
@Entry
@Component
struct CustomCalendarPage {
  private days: number[] = Array.from({ length: 30 }, (_, i) => i + 1)
  @State picked: number = 1
  build() {
    Column({ space: {spacing-md} }) {
      Text('2026年7月').fontSize({font-size-md}).fontWeight(FontWeight.Bold)
      Grid() {
        ForEach(this.days, (d: number) => {
          GridItem() {
            Text(`${d}`)
              .fontSize({font-size-sm})
              .textAlign(TextAlign.Center)
              .width(32).height(32)
              .borderRadius({radius-full})
              .backgroundColor(this.picked === d ? {color-button-primary-bg} : {color-bg-primary})
              .fontColor(this.picked === d ? {color-text-on-primary} : {color-text-primary})
              .onClick(() => this.picked = d)
          }
        })
      }
      .columnsTemplate('1fr 1fr 1fr 1fr 1fr 1fr 1fr')
      .rowsGap({spacing-xs})
    }
    .padding({spacing-md})
  }
}
```

## Notes

1. **Months start from 0** — `DatePickerResult.month` is 0-11, display needs +1; easy to make mistakes.
2. **DatePickerDialog recommended** — system built-in wheel date picker, consistent UX; prefer over custom-drawn calendar.
3. **Range validation** — custom date ranges need to validate start ≤ end, avoid logical errors.
4. **Custom calendar is complex** — includes cross-month, leap year, weekday alignment; use system DatePicker unless necessary.
5. **padStart zero-padding** — months/days less than two digits pad with zeros, ensure format consistency (e.g., `2026-07-01`).
6. **i18n date format** — different regions have different date formats, use `intl.DateTimeFormat` for formatting.