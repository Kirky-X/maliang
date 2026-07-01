# Grid 使用场景与示例

> 列举 ArkTS 数据网格组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:商品网格(3 列)

```arkts
@Entry
@Component
struct ProductGridPage {
  private products: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  build() {
    Grid() {
      ForEach(this.products, (id: number) => {
        GridItem() {
          Column({ space: {spacing-xs} }) {
            Image($r('app.media.cover')).width('100%').height(100).borderRadius({radius-md})
            Text(`商品${id}`).fontSize({font-size-sm})
            Text('¥99').fontSize({font-size-sm}).fontColor({color-danger})
          }
          .padding({spacing-sm})
          .backgroundColor({color-bg-primary})
          .borderRadius({radius-md})
        }
      })
    }
    .columnsTemplate('1fr 1fr 1fr')
    .columnsGap({spacing-sm})
    .rowsGap({spacing-sm})
    .padding({spacing-md})
  }
}
```

## 场景 2:跨列网格(Header 跨满)

```arkts
@Entry
@Component
struct SpanGridPage {
  build() {
    Grid() {
      GridItem() {
        Text('分组标题').fontSize({font-size-md}).fontWeight(FontWeight.Bold)
      }
      .columnStart(0).columnEnd(1)  // 跨 2 列

      ForEach([1, 2, 3, 4], (n: number) => {
        GridItem() { Text(`项${n}`).padding({spacing-md}) }
      })
    }
    .columnsTemplate('1fr 1fr')
    .rowsGap({spacing-sm})
    .padding({spacing-md})
  }
}
```

## 场景 3:无限滚动(下拉加载)

```arkts
@Entry
@Component
struct InfiniteGridPage {
  @State data: number[] = Array.from({ length: 12 }, (_, i) => i + 1)
  build() {
    Grid() {
      ForEach(this.data, (n: number) => {
        GridItem() {
          Text(`${n}`).padding({spacing-md}).backgroundColor({color-bg-secondary})
        }
      })
    }
    .columnsTemplate('1fr 1fr 1fr')
    .columnsGap({spacing-sm})
    .rowsGap({spacing-sm})
    .cachedCount(3)
    .padding({spacing-md})
    .onReachEnd(() => this.loadMore())
  }
  loadMore() {
    const start = this.data.length
    this.data.push(...Array.from({ length: 6 }, (_, i) => start + i + 1))
  }
}
```

## 场景 4:瀑布流(WaterFlow)

```arkts
@Entry
@Component
struct WaterFlowPage {
  build() {
    WaterFlow() {
      ForEach([1, 2, 3, 4, 5], (n: number) => {
        FlowItem() {
          Column() {
            Image($r('app.media.img')).width('100%').height(80 + n * 30)
            Text(`卡片${n}`).fontSize({font-size-sm})
          }
          .backgroundColor({color-bg-primary}).borderRadius({radius-md})
        }
      })
    }
    .columnsTemplate('1fr 1fr')
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **columnsTemplate 与 rowsTemplate 不可同时为固定值** — 同时固定会导致尺寸冲突;通常只设一个,另一个由内容撑开滚动。
2. **跨列需指定起点终点** — `columnStart`/`columnEnd` 是索引(从 0 开始),不设则占 1 格。
3. **大数据用 LazyForEach** — 千级数据用 `LazyForEach` 替代 `ForEach`,避免一次性渲染卡顿。
4. **cachedCount** — 预渲染屏外项,值过大占内存,建议 3-5。
5. **WaterFlow 是 Grid 变体** — 高度不等的瀑布流用 `WaterFlow` + `FlowItem`,非 `Grid`。
6. **滚动监听** — `onScrollIndex` 返回可视区首尾索引,适合做吸顶/加载更多。
