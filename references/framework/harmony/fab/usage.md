# FloatingActionButton 使用场景与示例

> 列举 ArkTS FAB 组合方案的典型场景。规范:单 FAB 原则;滚动联动出现/收起;与底部 dock 避让。

## 场景 1:标准圆形 FAB(新建入口)

```arkts
@Entry
@Component
struct FabPage {
  build() {
    Stack({ alignContent: Alignment.BottomEnd }) {
      List({ space: {spacing-sm}, scroller: new Scroller() }) {
        ForEach(['内容一', '内容二', '内容三'], (item: string) => {
          ListItem() {
            Text(item).fontSize({font-size-md})
              .padding({spacing-md})
              .backgroundColor({color-bg-primary})
              .borderRadius({radius-md})
          }
        })
      }
      .padding({spacing-md})

      Button() {
        SymbolGlyph($r('sys.symbol.plus')).fontSize(24)
          .fontColor([({color-text-inverse})])
      }
      .type(ButtonType.Circle)
      .width(56).height(56)
      .backgroundColor({color-primary})
      .shadow({ radius: 8, color: 'rgba(0,0,0,0.15)', offsetY: 2 })
      .margin({ right: {spacing-lg}, bottom: {spacing-xxl} })
      .onClick(() => promptAction.showToast({ message: '新建内容' }))
    }
    .width('100%').height('100%')
  }
}
```

## 场景 2:滚动联动出现/收起

```arkts
@Entry
@Component
struct ScrollFabPage {
  @State fabVisible: boolean = true
  private scroller: Scroller = new Scroller()
  private lastOffset: number = 0

  build() {
    Stack({ alignContent: Alignment.BottomEnd }) {
      List({ space: {spacing-sm}, scroller: this.scroller }) {
        ForEach(['条目一', '条目二', '条目三', '条目四'], (item: string) => {
          ListItem() {
            Text(item).fontSize({font-size-md}).padding({spacing-md})
          }
        })
      }
      .onScrollIndex((start: number) => {})
      .onScroll((xOffset: number, yOffset: number) => {
        // 下滑显示、上滑收起
        this.fabVisible = yOffset < this.lastOffset
        this.lastOffset = yOffset
      })

      if (this.fabVisible) {
        Button() {
          SymbolGlyph($r('sys.symbol.plus')).fontSize(24)
        }
        .type(ButtonType.Circle)
        .width(56).height(56)
        .backgroundColor({color-primary})
        .margin({ right: {spacing-lg}, bottom: {spacing-xxl} })
        .transition(TransitionEffect.OPACITY.animation({ duration: 200 }))
      }
    }
    .width('100%').height('100%')
  }
}
```

## 场景 3:扩展 FAB(带文案胶囊)

```arkts
@Entry
@Component
struct ExtendedFabPage {
  build() {
    Stack({ alignContent: Alignment.BottomEnd }) {
      Text('邮件列表').fontSize({font-size-md})
      Button() {
        Row({ space: {spacing-sm} }) {
          SymbolGlyph($r('sys.symbol.pencil')).fontSize(18)
            .fontColor([({color-text-inverse})])
          Text('写邮件').fontSize({font-size-md})
            .fontColor({color-text-inverse})
        }
      }
      .type(ButtonType.Capsule)
      .height(48)
      .padding({ left: {spacing-md}, right: {spacing-md} })
      .backgroundColor({color-primary})
      .shadow({ radius: 8, color: 'rgba(0,0,0,0.15)', offsetY: 2 })
      .margin({ right: {spacing-lg}, bottom: {spacing-xxl} })
    }
    .width('100%').height('100%')
  }
}
```

## 注意事项

1. **单 FAB 原则** — 每页最多 1 个 FAB,承载唯一一级操作(新建/发布/写);多个动作降级为长按菜单或底部入口。
2. **滚动联动** — 下滑(前进)显示、上滑(回看)收起,动效 ≤300ms;列表顶部时必显示。
3. **dock 避让** — 有底部 dock 时 FAB 悬浮其上方,不遮 dock 操作区;右侧留 ≥16vp 边距。
4. **层级与阴影** — FAB 位于内容层之上({z-index-*} 语义),投影轻(8px/15%),不做过激 elevation。
5. **无障碍** — `accessibilityText` 描述动作("新建笔记");触控目标 56vp 圆形达标。
