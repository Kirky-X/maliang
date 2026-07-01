# Timeline 使用场景与示例

> ArkTS 无原生 Timeline,本文件给出基于 List+轴线的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础时间线(竖线 + 圆点)

```arkts
@Entry
@Component
struct BasicTimelinePage {
  private items: Array<{ title: string; time: string }> = [
    { title: '订单创建', time: '10:00' },
    { title: '已付款', time: '10:05' },
    { title: '已发货', time: '11:00' },
    { title: '已签收', time: '14:30' }
  ]
  build() {
    Column() {
      ForEach(this.items, (item, idx: number) => {
        Row({ space: {spacing-sm} }) {
          // 时间轴
          Column() {
            Circle({ width: 10, height: 10 })
              .fill(idx === this.items.length - 1 ? {color-success} : {color-button-primary-bg})
            if (idx < this.items.length - 1) {
              Column().width(1).layoutWeight(1).backgroundColor({color-border-default})
            }
          }
          .width(20).alignItems(HorizontalAlign.Center)

          // 内容
          Column({ space: {spacing-xs} }) {
            Text(item.title).fontSize({font-size-md})
            Text(item.time).fontSize({font-size-xs}).fontColor({color-text-primary})
          }
          .layoutWeight(1).alignItems(HorizontalAlign.Start)
          .padding({ bottom: {spacing-md} })
        }
        .height(idx === this.items.length - 1 ? 'auto' : 'auto')
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:带图标节点的时间线

```arkts
@Entry
@Component
struct IconTimelinePage {
  private items: Array<{ title: string; done: boolean }> = [
    { title: '步骤一', done: true },
    { title: '步骤二', done: true },
    { title: '步骤三', done: false }
  ]
  build() {
    Column() {
      ForEach(this.items, (item, idx: number) => {
        Row({ space: {spacing-sm} }) {
          Column() {
            SymbolGlyph(item.done ? $r('sys.symbol.checkmark_circle_fill') : $r('sys.symbol.circle'))
              .fontSize({font-size-md})
              .fontColor([item.done ? {color-success} : {color-bg-secondary}])
            if (idx < this.items.length - 1) {
              Column().width(2).layoutWeight(1)
                .backgroundColor(item.done ? {color-success} : {color-border-default})
            }
          }
          .width(24).alignItems(HorizontalAlign.Center)

          Text(item.title)
            .fontSize({font-size-md})
            .fontColor(item.done ? {color-text-primary} : {color-text-primary})
            .padding({ bottom: {spacing-lg} })
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:封装可复用 Timeline 组件

```arkts
interface TimelineItem { title: string; time: string; status?: 'done' | 'current' | 'todo' }

@Component
struct Timeline {
  private items: TimelineItem[] = []
  build() {
    Column() {
      ForEach(this.items, (item, idx: number) => {
        Row({ space: {spacing-sm} }) {
          Column() {
            Circle({ width: 10, height: 10 })
              .fill(item.status === 'done' ? {color-success}
                : item.status === 'current' ? {color-button-primary-bg} : {color-bg-secondary})
            if (idx < this.items.length - 1) {
              Column().width(1).layoutWeight(1).backgroundColor({color-border-default})
            }
          }.width(20).alignItems(HorizontalAlign.Center)
          Column({ space: {spacing-xs} }) {
            Text(item.title).fontSize({font-size-md})
            Text(item.time).fontSize({font-size-xs}).fontColor({color-text-primary})
          }
          .layoutWeight(1).alignItems(HorizontalAlign.Start)
          .padding({ bottom: {spacing-md} })
        }
      })
    }
  }
}
```

## 注意事项

1. **竖线用 layoutWeight 撑满** — 节点间竖线高度由 `layoutWeight(1)` 自动填充,无需算固定高度。
2. **末项无竖线** — 最后一个节点不画下方竖线,用 `if (idx < length - 1)` 控制。
3. **状态配色** — 已完成绿、进行中主色、未开始灰;圆点颜色随状态切换。
4. **节点对齐** — 时间轴 Column 宽度固定 + `alignItems(Center)`,保证圆点居中于轴线。
5. **横向时间线** — 改为 `Row` 横向排列 + 横向 `Divider`,适合步骤展示。
6. **动态加载** — 物流轨迹等异步数据,先渲染骨架再填充。
