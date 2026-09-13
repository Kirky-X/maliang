# DatePicker 使用场景与示例

> 列举 ArkTS 日期时间选择的典型场景。录入交互(弹窗/滚轮)与 calendar 的浏览交互分工明确:选日期用本类,看日程用 calendar。

## 场景 1:预订场景(范围外禁选)

```arkts
@Entry
@Component
struct BookingDatePage {
  @State checkIn: string = '请选择'
  build() {
    Column({ space: {spacing-md} }) {
      Text('入住日期').fontSize({font-size-md})
      Row({ space: {spacing-sm} }) {
        Text(this.checkIn)
          .fontSize({font-size-md})
          .fontColor(this.checkIn === '请选择' ? {color-text-secondary} : {color-text-primary})
        Image($r('sys.media.ohos_ic_public_arrow_down')).width(16).height(16)
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-secondary})
      .borderRadius({radius-md})
      .onClick(() => {
        DatePickerDialog.show({
          start: new Date(), // 今天起可选
          end: new Date('2026-12-31'),
          onDateAccept: (value: Date) => {
            this.checkIn = `${value.getMonth() + 1} 月 ${value.getDate()} 日`
          }
        })
      })
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
  }
}
```

## 场景 2:时间选择(24 小时制)

```arkts
@Entry
@Component
struct TimeSelectPage {
  @State time: string = '请选择时间'
  build() {
    Column({ space: {spacing-md} }) {
      Text('提醒时间').fontSize({font-size-md})
      Text(this.time)
        .fontSize({font-size-md})
        .padding({spacing-md})
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-md})
        .onClick(() => {
          TimePickerDialog.show({
            useMilitaryTime: true,
            onAccept: (value: TimePickerResult) => {
              this.time = `${value.hour}:${value.minute < 10 ? '0' + value.minute : value.minute}`
            }
          })
        })
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
  }
}
```

## 场景 3:内嵌 DatePicker(表单页内直接选择)

```arkts
@Entry
@Component
struct InlineDatePickerPage {
  @State selected: Date = new Date()
  build() {
    Column({ space: {spacing-md} }) {
      Text('出生日期').fontSize({font-size-md})
      DatePicker({
        start: new Date('1920-01-01'),
        end: new Date(),
        selected: this.selected
      })
        .lunar(false)
        .onDateChange((value: Date) => this.selected = value)
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **录入 vs 浏览** — 表单选值一律 DatePickerDialog/TimePickerDialog;浏览型日程视图才用 calendar,二者不互相替代。
2. **范围约束前置** — `start`/`end` 限定可选范围,范围外日期置灰,配合防错原则。
3. **实时回调与确认回调** — `onDateChange` 滚动实时触发(勿做重活);`onDateAccept` 确认时触发(业务落库点)。
4. **无障碍** — 弹窗自带焦点管理;触发器 `accessibilityText` 描述当前值(如"当前入住日期 9 月 10 日")。
5. **触控目标** — 触发器整体可点,热区 ≥44vp。
