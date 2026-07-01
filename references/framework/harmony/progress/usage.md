# Progress 使用场景与示例

> 列举 ArkTS 进度条组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:线性下载进度

```arkts
@Entry
@Component
struct DownloadPage {
  @State progress: number = 0
  timer: number = -1
  aboutToAppear() {
    this.timer = setInterval(() => {
      this.progress = Math.min(100, this.progress + 10)
      if (this.progress >= 100) clearInterval(this.timer)
    }, 500)
  }
  aboutToDisappear() { clearInterval(this.timer) }
  build() {
    Column({ space: {spacing-sm} }) {
      Text(`下载中 ${this.progress}%`).fontSize({font-size-sm})
      Progress({ value: this.progress, total: 100, type: ProgressType.Linear })
        .width('100%')
        .color({color-button-primary-bg})
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-full})
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:环形进度(百分比)

```arkts
@Entry
@Component
struct RingProgressPage {
  @State value: number = 65
  build() {
    Column({ space: {spacing-sm} }) {
      Progress({ value: this.value, total: 100, type: ProgressType.Ring })
        .width(80).height(80)
        .color({color-success})
        .backgroundColor({color-bg-secondary})
        .strokeWidth(8)
      Text(`${this.value}%`).fontSize({font-size-md})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:弹窗内进度

```arkts
@CustomDialog
struct ProgressDialog {
  controller: CustomDialogController
  @State value: number = 0
  build() {
    Column({ space: {spacing-md} }) {
      Text('处理中').fontSize({font-size-md})
      Progress({ value: this.value, type: ProgressType.Linear })
        .width('100%')
        .color({color-button-primary-bg})
    }
    .padding({spacing-lg})
  }
}
```

## 场景 4:加载转圈(LoadingProgress)

不定进度场景用 `LoadingProgress`,无 value 参数。

```arkts
@Entry
@Component
struct LoadingPage {
  build() {
    Column({ space: {spacing-md} }) {
      LoadingProgress()
        .width(48).height(48)
        .color({color-button-primary-bg})
      Text('加载中...').fontSize({font-size-sm}).fontColor({color-text-primary})
    }
    .padding({spacing-lg})
  }
}
```

## 注意事项

1. **Progress 需主动更新 value** — 通过 `@State` 绑定,定时器或回调驱动;不会自动递增。
2. **LoadingProgress 无进度值** — 仅作加载动画,值已知时用 `Progress(Ring/Linear)`。
3. **strokeWidth 仅 Ring 生效** — Linear 类型线宽由 height 决定,Ring 由 strokeWidth。
4. **定时器清理** — `setInterval` 必须在 `aboutToDisappear` 清理,避免内存泄漏。
5. **环形配色** — `color` 为进度色,`backgroundColor` 为轨道底色;对比度需足够。
6. **total 灵活** — 下载字节数场景可设 `total` 为文件大小,`value` 为已下载字节,无需手动换算百分比。
