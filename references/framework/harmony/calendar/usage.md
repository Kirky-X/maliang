# Calendar 使用场景与示例

> 展示型日历(浏览,非录入)的典型场景。**选日期/选时间的录入场景全部收敛到 [date-picker](../date-picker/usage.md)**(DatePickerDialog / TimePickerDialog / 范围选择都在那边),本文件不再重复;「选日期用 date-picker,看日程用 calendar」,二者不互相替代。所有颜色、间距、圆角一律经设计 token 引用。

## 场景 1:月历浏览日程(展示型主场景)

```arkts
@Entry
@Component
struct CalendarBrowsePage {
  @State selectedDate: string = ''
  @State monthLabel: string = '2026 年 10 月'
  private events: Map<string, number> = new Map([
    ['2026-10-24', 2], ['2026-10-26', 1], ['2026-10-28', 3]
  ])
  private days: number[] = Array.from({ length: 31 }, (_, i) => i + 1)

  build() {
    Column({ space: {spacing-md} }) {
      Text(this.monthLabel).fontSize({font-size-md}).fontColor({color-text-primary})

      Grid() {
        ForEach(this.days, (d: number) => {
          GridItem() {
            Column({ space: 2 }) {
              Text(`${d}`)
                .fontSize({font-size-sm})
                .fontColor({color-text-primary})
                .width(32).height(32).textAlign(TextAlign.Center)
                .borderRadius({radius-full})
                .border(this.selectedDate === `2026-10-${d.toString().padStart(2, '0')}`
                  ? { width: {border-thin}, color: {color-brand-primary} } : { width: 0 })
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

      List({ space: {spacing-sm} }) {
        ForEach(this.selectedDate ? ['上午:设计评审', '下午:版本发布'] : [], (item: string) => {
          ListItem() {
            Text(item).fontSize({font-size-sm}).fontColor({color-text-primary})
              .padding({spacing-sm})
              .backgroundColor({color-bg-secondary}).borderRadius({radius-md})
          }
        })
      }
      .width('100%')
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:月切换(配合 Swiper)

```arkts
@Entry
@Component
struct CalendarSwipePage {
  private months: string[] = ['2026 年 09 月', '2026 年 10 月', '2026 年 11 月']
  @State current: number = 1

  build() {
    Column({ space: {spacing-sm} }) {
      Swiper() {
        ForEach(this.months, (m: string) => {
          Column({ space: {spacing-sm} }) {
            Text(m).fontSize({font-size-md}).fontColor({color-text-primary})
            // 此处复用场景 1 的月历网格组件(抽成 @Builder 或子组件)
            Text('月历网格').fontSize({font-size-sm}).fontColor({color-text-secondary})
          }
          .justifyContent(FlexAlign.Center)
        })
      }
      .index(this.current)
      .loop(false)
      .indicator(false)
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **浏览不弹选择器** —— 点日期联动下方列表;要选值直接引导用户去 date-picker,不在月历上做录入。
2. **事件圆点** —— 有日程的日期加 `{color-brand-primary}` 圆点;当日加描边或填充强调;选中日期用实心反色。
3. **补位灰显** —— 上月/下月补位日期用 `{color-text-secondary}` 弱化,不可点或点了切月。
4. **月切换** —— 左右滑动切月用 `Swiper`(场景 2),不要用左右箭头按钮塞满头。
5. **数据源** —— 事件集合按 `YYYY-MM-DD` 建 Map,月切换时按月请求;缺省月份不预取。
6. **无障碍** —— 日期格补充 `accessibilityText`(如"10 月 24 日,2 个日程"),圆点信息不能只靠颜色传达。
