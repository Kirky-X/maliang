# Video 使用场景与示例

> 列举 ArkTS 视频播放组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础视频播放(默认控件)

```arkts
@Entry
@Component
struct BasicVideoPage {
  private controller: VideoController = new VideoController()
  build() {
    Column() {
      Video({
        src: 'https://example.com/demo.mp4',
        controller: this.controller,
        previewUri: $r('app.media.cover')
      })
        .width('100%').height(220)
        .controls(true)
        .autoPlay(false)
        .objectFit(ImageFit.Contain)
        .borderRadius({radius-md})
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:自定义控件(隐藏默认 controls)

```arkts
@Entry
@Component
struct CustomVideoPage {
  private controller: VideoController = new VideoController()
  @State playing: boolean = false
  build() {
    Stack({ alignContent: Alignment.Center }) {
      Video({
        src: $r('app.media.intro'),
        controller: this.controller
      })
        .width('100%').height(220)
        .controls(false)
        .borderRadius({radius-md})

      if (!this.playing) {
        Button({ type: ButtonType.Circle }) {
          SymbolGlyph($r('sys.symbol.play_fill'))
            .fontSize({font-size-xl})
            .fontColor([{color-text-on-primary}])
        }
        .width(56).height(56)
        .backgroundColor({color-button-primary-bg})
        .onClick(() => { this.controller.start(); this.playing = true })
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:循环背景视频(静音自动播放)

```arkts
@Entry
@Component
struct LoopVideoPage {
  private controller: VideoController = new VideoController()
  build() {
    Video({
      src: $r('app.media.bg'),
      controller: this.controller
    })
      .width('100%').height(300)
      .controls(false)
      .autoPlay(true)
      .muted(true)
      .loop(true)
      .objectFit(ImageFit.Cover)
  }
}
```

## 场景 4:倍速播放

```arkts
@Entry
@Component
struct SpeedVideoPage {
  private controller: VideoController = new VideoController()
  build() {
    Column({ space: {spacing-md} }) {
      Video({
        src: $r('app.media.demo'),
        controller: this.controller,
        currentProgressRate: 2  // 2 倍速
      })
        .width('100%').height(200)
        .controls(true)
        .borderRadius({radius-md})
      Row({ space: {spacing-sm} }) {
        Button('1x').onClick(() => this.controller.pause())
        Button('2x').onClick(() => this.controller.start())
      }
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **网络视频需 INTERNET 权限** — module.json5 配置 `ohos.permission.INTERNET`。
2. **autoPlay 受限** — 部分设备为省电禁止自动播放,需用户交互触发 `controller.start()`。
3. **静音循环作背景** — 背景视频设 `muted(true) + loop(true)`,但耗电较高,慎用。
4. **currentProgressRate 倍速** — 1.0/2.0/0.5 等;非标准倍速可能不被支持。
5. **controller 必须复用** — 每次渲染 new 新 controller 会丢失状态,声明为成员变量。
6. **objectFit Cover 会裁剪** — 视频比例与容器不符时 Cover 裁剪;Contain 留黑边。
