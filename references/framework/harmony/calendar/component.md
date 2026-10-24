# Calendar 日历展示组件 API 文档

> **定位:展示型日历(浏览,非录入)**——查看某月哪几天有日程/预订,点进当日列表。**选日期请直接用 [date-picker](../date-picker/component.md)**(DatePickerDialog / CalendarPicker / DatePicker 都收敛在那边,本文件不再重复);「选日期用 date-picker,看日程用 calendar」,二者不互相替代。ArkUI 没有只读月历组件,展示型日历用 `Grid` + 日期计算组合实现,即本文件的最小示例。

## 与 date-picker 的分工

| 需求 | 去处 |
| --- | --- |
| 选一个日期/一段日期(录入) | [date-picker](../date-picker/component.md)(DatePickerDialog / CalendarPicker / DatePicker) |
| 浏览某月日程、看哪些天有事、点开当日列表 | 本文件(Grid 自绘月历 + 日程列表) |

## 展示型月历的组合要点

- **网格**:7 列 `Grid`,列头一至日;上月/下月补位日期灰显,当月正常。
- **事件标记**:有日程的日期下加圆点(`{color-brand-primary}`);今日用描边或填充强调。
- **数据源**:日程集合按 `YYYY-MM-DD` 建 `Map<string, number>`(或事件数组),渲染每格时查当日事件数决定圆点。
- **交互**:点日期 → `@State selectedDate` 更新 → 下方日程列表联动;浏览型**不弹选择器**——要选值就跳 date-picker。

## 最小示例

```arkts
@Entry
@Component
struct CalendarViewPage {
  @State selectedDate: string = ''
  // 日程占用表:YYYY-MM-DD → 当日事件数(实际项目来自服务端)
  private events: Map<string, number> = new Map([
    ['2026-10-24', 2], ['2026-10-26', 1]
  ])
  private days: number[] = Array.from({ length: 31 }, (_, i) => i + 1)

  build() {
    Column({ space: {spacing-md} }) {
      Text('2026 年 10 月').fontSize({font-size-md}).fontColor({color-text-primary})
      Grid() {
        ForEach(this.days, (d: number) => {
          GridItem() {
            Column({ space: 2 }) {
              Text(`${d}`)
                .fontSize({font-size-sm})
                .fontColor({color-text-primary})
                .width(32).height(32).textAlign(TextAlign.Center)
                .borderRadius({radius-full})
                .border(d === 24 ? { width: {border-thin}, color: {color-brand-primary} } : { width: 0 })
              if (this.events.get(`2026-10-${d.toString().padStart(2, '0')}`)) {
                Circle({ width: 4, height: 4 }).fill({color-brand-primary})
              }
            }
          }
          .onClick(() => this.selectedDate = `2026-10-${d.toString().padStart(2, '0')}`)
        })
      }
      .columnsTemplate('1fr 1fr 1fr 1fr 1fr 1fr 1fr')
      .height({spacing-3xl})

      if (this.selectedDate) {
        Text(`${this.selectedDate} 的日程`).fontSize({font-size-sm}).fontColor({color-text-secondary})
      }
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`date-picker`](../date-picker/component.md) — 选日期(录入)走那边
- [`list`](../list/component.md) — 当日日程列表

## 参考链接

- Grid 网格容器:https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-container-grid
- Swiper 组件:https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-container-swiper
