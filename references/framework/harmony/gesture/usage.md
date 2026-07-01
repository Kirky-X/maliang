# Gesture 使用场景与示例

> 列举 ArkTS 手势组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:双击点赞(TapGesture count=2)

```arkts
@Entry
@Component
struct DoubleTapPage {
  @State liked: boolean = false
  build() {
    Column() {
      Image($r('app.media.cover'))
        .width(200).height(200)
        .borderRadius({radius-md})
        .gesture(
          TapGesture({ count: 2 }).onAction(() => this.liked = true)
        )
      Text(this.liked ? '已点赞' : '双击点赞')
        .fontSize({font-size-sm})
        .fontColor(this.liked ? {color-danger} : {color-text-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:拖拽移动卡片(PanGesture)

```arkts
@Entry
@Component
struct DragPage {
  @State x: number = 0
  @State y: number = 0
  build() {
    Column() {
      Row()
        .width(80).height(80)
        .backgroundColor({color-button-primary-bg})
        .borderRadius({radius-md})
        .translate({ x: this.x, y: this.y })
        .gesture(
          PanGesture()
            .onActionUpdate((e: GestureEvent) => {
              this.x = e.offsetX
              this.y = e.offsetY
            })
        )
    }
    .width('100%').height('100%')
    .padding({spacing-md})
  }
}
```

## 场景 3:图片缩放(PinchGesture)

```arkts
@Entry
@Component
struct PinchPage {
  @State scale: number = 1
  build() {
    Column() {
      Image($r('app.media.photo'))
        .width(200).height(200)
        .scale({ x: this.scale, y: this.scale })
        .gesture(
          PinchGesture()
            .onActionUpdate((e: GestureEvent) => {
              this.scale = Math.max(0.5, Math.min(3, this.scale * e.scale))
            })
        )
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:长按弹出菜单(LongPressGesture)

```arkts
@Entry
@Component
struct LongPressMenuPage {
  build() {
    Column() {
      Text('长按出菜单')
        .fontSize({font-size-md})
        .padding({spacing-md})
        .backgroundColor({color-bg-secondary})
        .bindContextMenu(this.menuBuilder, ResponseType.LongPress)
    }
    .padding({spacing-md})
  }
  @Builder menuBuilder() {
    Menu() {
      MenuItem({ content: '复制' })
      MenuItem({ content: '删除' })
    }
  }
}
```

## 场景 5:组合手势(串行:长按 + 拖拽)

```arkts
@Entry
@Component
struct CombinedGesturePage {
  @State x: number = 0
  build() {
    Column() {
      Row()
        .width(80).height(80)
        .backgroundColor({color-success})
        .translate({ x: this.x })
        .gesture(
          GestureGroup(GestureMode.Sequence,
            LongPressGesture({ duration: 500 }),
            PanGesture().onActionUpdate((e: GestureEvent) => this.x = e.offsetX)
          )
        )
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **offsetX/offsetY 是相对增量** — `PanGesture` 的 offset 是从手势开始累计位移,拖拽需直接赋值非累加。
2. **gesture vs priorityGesture** — 子组件自带手势(如 List 滚动)会与父组件 gesture 冲突;父级用 `priorityGesture` 强制优先。
3. **GestureGroup Sequence** — 串行需按顺序完成前置手势;Parallel 同时识别;Exclusive 先触发者胜出。
4. **bindContextMenu 更省事** — 长按菜单建议直接用 `bindContextMenu`,而非手动 LongPressGesture + Menu。
5. **fingers 默认 1** — 多指手势需显式设置 `fingers: 2`;单指手势多指触摸会被忽略。
6. **缩放边界** — PinchGesture 需 clamp 上下限(如 0.5-3),避免缩放到 0 或负值。
