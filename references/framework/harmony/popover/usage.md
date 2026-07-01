# Popover 使用场景与示例

> 列举 ArkTS Popup 气泡提示的典型使用场景(slug 统一 popover,ArkTS 原生名 Popup)。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:图标说明气泡

```arkts
@Entry
@Component
struct IconTipPage {
  @State show: boolean = false
  build() {
    Row() {
      SymbolGlyph($r('sys.symbol.questionmark_circle'))
        .fontSize({font-size-md})
        .fontColor([{color-text-primary}])
        .onClick(() => this.show = !this.show)
        .bindPopup(this.show, {
          message: '点击此处查看帮助文档',
          placement: Placement.Bottom,
          textColor: {color-text-on-primary},
          color: {color-bg-secondary}
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:长按显示气泡

```arkts
@Entry
@Component
struct LongPressTipPage {
  @State show: boolean = false
  build() {
    Column() {
      Text('长按查看详情')
        .fontSize({font-size-md})
        .padding({spacing-md})
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-md})
        .gesture(LongPressGesture().onAction(() => this.show = true))
        .bindPopup(this.show, {
          message: '这是详细说明信息',
          placement: Placement.Top,
          duration: 3000
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:自定义内容气泡(builder)

```arkts
@Entry
@Component
struct CustomPopoverPage {
  @State show: boolean = false
  build() {
    Column() {
      Button('点击')
        .onClick(() => this.show = !this.show)
        .bindPopup(this.show, {
          builder: this.popupContent,
          placement: Placement.Bottom,
          onStateChange: (e) => this.show = e.isVisible
        })
    }
    .padding({spacing-md})
  }

  @Builder popupContent() {
    Column({ space: {spacing-xs} }) {
      Text('自定义标题').fontSize({font-size-sm}).fontWeight(FontWeight.Bold)
      Text('自定义说明内容').fontSize({font-size-xs}).fontColor({color-text-primary})
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-md})
  }
}
```

## 场景 4:位置自适应(Placement)

```arkts
@Entry
@Component
struct PlacementPage {
  @State show: boolean = false
  build() {
    Column() {
      Button('底部弹出')
        .onClick(() => this.show = !this.show)
        .bindPopup(this.show, {
          message: '弹窗在按钮下方',
          placement: Placement.Bottom,
          enableArrow: true
        })
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **bindPopup 需显式控制 show** — 通过 `@State show` 控制;不设 duration 时手动关闭。
2. **duration 默认长** — 默认 10000ms;短暂提示需显式设置(如 3000ms)。
3. **placement 自动避让** — 边界处框架会自动翻转位置,但仍可能溢出,关键场景测试。
4. **builder 自定义内容** — 复杂气泡用 `builder` 传入 `@Builder`;此时 `message` 失效。
5. **onStateChange 同步状态** — 点击外部自动关闭时需在 `onStateChange` 同步 `show`,否则状态不一致。
6. **与 Toast 区别** — Popup 锚定组件、可交互、可自定义;Toast 全局居中、定时消失、不可交互。
