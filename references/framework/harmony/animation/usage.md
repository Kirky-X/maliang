# Animation 使用场景与示例

> 列举 ArkTS 动画能力的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:点击缩放反馈(animateTo)

```arkts
@Entry
@Component
struct ScaleAnimPage {
  @State scale: number = 1
  build() {
    Column() {
      Button('点我')
        .scale({ x: this.scale, y: this.scale })
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
        .onClick(() => {
          animateTo({ duration: 200, curve: Curve.EaseOut }, () => {
            this.scale = this.scale === 1 ? 0.9 : 1
          })
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:渐显渐隐(属性动画 animation)

```arkts
@Entry
@Component
struct FadeAnimPage {
  @State opacity: number = 1
  build() {
    Column() {
      Text('淡入淡出')
        .fontSize({font-size-lg})
        .opacity(this.opacity)
        .animation({ duration: 400, curve: Curve.EaseInOut })
      Button('切换')
        .onClick(() => this.opacity = this.opacity === 1 ? 0.2 : 1)
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:列表项出现转场(transition)

```arkts
@Entry
@Component
struct TransitionPage {
  @State show: boolean = false
  build() {
    Column() {
      Button('切换显示').onClick(() => this.show = !this.show)
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
      if (this.show) {
        Text('新内容')
          .fontSize({font-size-md})
          .padding({spacing-md})
          .backgroundColor({color-bg-secondary})
          .borderRadius({radius-md})
          .transition({ type: TransitionType.Insert, translate: { y: 50 }, opacity: 0 })
          .transition({ type: TransitionType.Delete, opacity: 0 })
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:弹簧动画(springMotion)

```arkts
@Entry
@Component
struct SpringPage {
  @State x: number = 0
  build() {
    Column() {
      Row()
        .width(80).height(80)
        .backgroundColor({color-button-primary-bg})
        .borderRadius({radius-full})
        .translate({ x: this.x })
        .onClick(() => {
          animateTo({ curve: curves.springMotion() }, () => {
            this.x = this.x === 0 ? 200 : 0
          })
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:无限旋转(loading 图标)

```arkts
@Entry
@Component
struct RotatePage {
  @State angle: number = 0
  aboutToAppear() {
    animateTo({ duration: 1000, iterations: -1, curve: Curve.Linear }, () => {
      this.angle = 360
    })
  }
  build() {
    SymbolGlyph($r('sys.symbol.arrow_clockwise'))
      .fontSize({font-size-lg})
      .fontColor([{color-button-primary-bg}])
      .rotate({ angle: this.angle })
  }
}
```

## 注意事项

1. **animateTo vs animation** — `animateTo` 在闭包改值触发,适合交互驱动;`animation` 链式附加,适合声明式。
2. **状态变量必须 @State** — 动画依赖状态变更触发;非状态变量改动不产生动画。
3. **transition 需 if 控制** — `transition` 仅在组件 `if/else` 插入/移除时触发,常驻不触发。
4. **iterations=-1 无限循环** — loading 类动画用 -1;记得在 `aboutToDisappear` 停止。
5. **springMotion 需引入 curves** — `import { curves } from '@kit.ArkUI'`,弹簧效果更自然。
6. **性能** — 优先改 `transform`(scale/translate/rotate/opacity),避免改 width/height 触发布局重排。
