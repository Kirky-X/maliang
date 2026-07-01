# Icon 使用场景与示例

> 列举 ArkTS 图标组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:列表项箭头图标

```arkts
@Entry
@Component
struct ListIconPage {
  build() {
    Column() {
      Row() {
        Text('设置').fontSize({font-size-md})
        Blank()
        SymbolGlyph($r('sys.symbol.chevron-right'))
          .fontSize({font-size-md})
          .fontColor([{color-text-primary}])
      }
      .width('100%')
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
    }
  }
}
```

## 场景 2:多色符号图标

```arkts
@Entry
@Component
struct MultiColorIconPage {
  build() {
    Row({ space: {spacing-md} }) {
      SymbolGlyph($r('sys.symbol.star_fill'))
        .fontSize({font-size-xl})
        .fontColor([{color-warning}])
      SymbolGlyph($r('sys.symbol.heart_fill'))
        .fontSize({font-size-xl})
        .fontColor([{color-danger}])
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:图标按钮(Button + Image)

```arkts
@Entry
@Component
struct IconButtonPage {
  build() {
    Row({ space: {spacing-lg} }) {
      Button({ type: ButtonType.Circle }) {
        Image($r('app.media.icon_share')).width(20).height(20)
      }
      .width(44).height(44)
      .backgroundColor({color-bg-secondary})

      Button({ type: ButtonType.Circle }) {
        Image($r('app.media.icon_back')).width(20).height(20)
      }
      .width(44).height(44)
      .backgroundColor({color-bg-secondary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:动效图标(SymbolGlyph effectStrategy)

```arkts
@Entry
@Component
struct AnimatedIconPage {
  @State playing: boolean = false
  build() {
    Column({ space: {spacing-sm} }) {
      SymbolGlyph($r('sys.symbol.play_fill'))
        .fontSize({font-size-xl})
        .fontColor([{color-button-primary-bg}])
        .effectStrategy(this.playing ? SymbolEffectStrategy.Scale : SymbolEffectStrategy.None)
      Button('切换').onClick(() => this.playing = !this.playing)
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:内联图标(SymbolSpan)

```arkts
@Entry
@Component
struct InlineIconPage {
  build() {
    Text() {
      SymbolSpan($r('sys.symbol.info')).fontColor([{color-info}])
      Span(' 提示信息').fontSize({font-size-sm})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **SymbolGlyph 资源前缀** — 系统符号用 `$r('sys.symbol.xxx')`,自定义需放入 resources 并用 `$r('app.symbol.xxx')`。
2. **fontColor 是数组** — 支持多色符号;单色传单元素数组 `[{color-xxx}]`。
3. **fillColor 仅位图生效** — 矢量符号着色用 `fontColor`,Image 着色用 `fillColor`,不可混用。
4. **图标尺寸用 fontSize** — SymbolGlyph 无 width/height,通过 `fontSize` 控制大小。
5. **effectStrategy** — 需配合 `@State` 变化触发动效;静态图标用 `None`。
6. **无障碍** — 纯图标需设 `accessibilityText`,避免读屏无内容。
