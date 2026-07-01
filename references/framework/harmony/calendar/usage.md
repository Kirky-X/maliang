# Calendar 使用场景与示例

> 列举 ArkTS 日历/日期选择的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:日期选择弹窗(DatePickerDialog)

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

## 场景 2:时间选择(TimePickerDialog)

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

## 场景 3:日期范围选择(两个 DatePicker)

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

## 场景 4:内嵌日历(自定义网格实现)

无 CalendarPicker 时,用 Grid 自行实现月历。

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

## 注意事项

1. **月份从 0 开始** — `DatePickerResult.month` 是 0-11,显示需 +1;容易出错。
2. **DatePickerDialog 推荐** — 系统自带滚轮日期选择,体验一致;优先于自绘日历。
3. **范围校验** — 自定义日期范围需校验 start ≤ end,避免逻辑错误。
4. **自绘日历复杂** — 含跨月、闰年、星期对齐;非必要用系统 DatePicker。
5. **padStart 补零** — 月份/日期不足两位补零,保证格式统一(如 `2026-07-01`)。
6. **i18n 日期格式** — 不同地区日期格式不同,用 `intl.DateTimeFormat` 格式化。
