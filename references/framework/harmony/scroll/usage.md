# Scroll 使用场景与示例

> ArkTS 无独立 Scroll 指南页,本文件给出基于 `Scroll` 容器组件的实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础滚动容器(Scroll)

```arkts
@Entry
@Component
struct ScrollPage {
  build() {
    Scroll() {
      Column() {
        ForEach([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], (n: number) => {
          Text(`第 ${n} 行`)
            .width('100%')
            .padding({spacing-md})
            .fontSize({font-size-md})
            .backgroundColor({color-bg-primary})
            .margin({ bottom: {spacing-sm} })
        })
      }
      .padding({spacing-md})
    }
    .scrollBar(BarState.Auto)
    .width('100%').height('100%')
  }
}
```

## 场景 2:横向滚动(scrollHorizontal)

```arkts
@Entry
@Component
struct HorizontalScrollPage {
  build() {
    Scroll() {
      Row({ space: {spacing-sm} }) {
        ForEach([1, 2, 3, 4, 5, 6], (n: number) => {
          Text(`标签${n}`)
            .padding({spacing-sm})
            .backgroundColor({color-bg-secondary})
            .borderRadius({radius-full})
        })
      }
      .padding({spacing-md})
    }
    .scrollable(ScrollDirection.Horizontal)
    .scrollBar(BarState.Off)
  }
}
```

## 场景 3:回顶部(Scroller 控制)

```arkts
@Entry
@Component
struct ScrollToTopPage {
  private scroller: Scroller = new Scroller()
  build() {
    Stack({ alignContent: Alignment.BottomEnd }) {
      Scroll(this.scroller) {
        Column() {
          ForEach([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], (n: number) => {
            Text(`行 ${n}`).padding({spacing-md}).fontSize({font-size-md})
          })
        }
        .padding({spacing-md})
      }
      .width('100%').height('100%')

      Button({ type: ButtonType.Circle }) {
        SymbolGlyph($r('sys.symbol.arrow_up')).fontColor([{color-text-on-primary}])
      }
      .width(48).height(48)
      .backgroundColor({color-button-primary-bg})
      .margin({spacing-md})
      .onClick(() => this.scroller.scrollEdge(Edge.Top))
    }
  }
}
```

## 场景 4:列表场景(用 List 而非 Scroll)

列表数据用 `List` 而非 `Scroll`,享性能优化与懒加载。

```arkts
@Entry
@Component
struct ListScrollPage {
  private data: number[] = Array.from({ length: 50 }, (_, i) => i)
  build() {
    List({ space: {spacing-sm} }) {
      ForEach(this.data, (n: number) => {
        ListItem() {
          Text(`项 ${n}`).padding({spacing-md}).backgroundColor({color-bg-primary})
        }
      })
    }
    .padding({spacing-md})
    .cachedCount(5)
  }
}
```

## 注意事项

1. **Scroll 适合非列表** — 列表数据优先用 `List`(懒加载);Scroll 适合详情页/表单等内容结构化但非长列表。
2. **scrollable 方向** — `ScrollDirection.Vertical`(默认)/ `Horizontal` / `None`;双向滚动需嵌套。
3. **scrollEdge** — `Edge.Top`/`Edge.Bottom` 快速回顶/回底;精确位置用 `scrollTo({ xOffset, yOffset })`。
4. **scrollBar** — `BarState.Auto`(默认)/ `On` / `Off`;移动端建议 Auto 或 Off。
5. **Scroll 嵌套滚动冲突** — 外层纵向 + 内层纵向会冲突;内层用 `nestedScroll` 选项配置滚动联动。
6. **性能** — Scroll 内大量子项不会懒加载,一次性渲染;千级数据务必用 List + LazyForEach。
