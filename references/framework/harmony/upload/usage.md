# Upload 使用场景与示例

> 列举 ArkTS 上传组合方案的典型场景。完整模式为"触发器 + 文件列表 + 进度 + 失败重试",所有颜色、间距通过 design token 引用。

## 场景 1:头像上传(单图 + 裁剪入口)

```arkts
@Entry
@Component
struct AvatarUploadPage {
  @State avatar: ResourceStr | string = $r('app.media.avatar_default')
  private picker = new photoAccessHelper.PhotoViewPicker()

  async pickAvatar() {
    let result = await this.picker.select({
      MIMEType: photoAccessHelper.PhotoViewMIMETypes.IMAGE_TYPE,
      maxSelectNumber: 1
    })
    if (result.photoUris.length > 0) {
      this.avatar = result.photoUris[0]
      // 进入上传队列,成功后 toast(promptAction.showToast)
    }
  }

  build() {
    Column({ space: {spacing-md} }) {
      Image(this.avatar).width(72).height(72).borderRadius({radius-full})
      Button('更换头像', { buttonStyle: ButtonStyleMode.NORMAL }).onClick(() => this.pickAvatar())
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:多图上传队列(进度 + 失败重试)

```arkts
@Entry
@Component
struct UploadQueuePage {
  @State items: Array<{ name: string, progress: number, failed: boolean }> = [
    { name: 'a.jpg', progress: 100, failed: false },
    { name: 'b.jpg', progress: 46, failed: false },
    { name: 'c.jpg', progress: 0, failed: true }
  ]
  build() {
    Column({ space: {spacing-sm} }) {
      ForEach(this.items, (f: { name: string, progress: number, failed: boolean }) => {
        Row({ space: {spacing-sm} }) {
          Text(f.name).fontSize({font-size-md}).layoutWeight(1)
          if (f.failed) {
            Text('上传失败').fontSize({font-size-sm}).fontColor({color-error})
            Button('重试', { buttonStyle: ButtonStyleMode.NORMAL, type: ButtonType.Capsule })
              .fontSize({font-size-sm})
          } else if (f.progress < 100) {
            Progress({ value: f.progress, total: 100, type: ProgressType.Linear }).width(96)
          } else {
            Text('已完成').fontSize({font-size-sm}).fontColor({color-success})
          }
        }
        .padding({spacing-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:附件文档上传(校验 + 限制提示)

```arkts
@Entry
@Component
struct DocUploadPage {
  @State docs: string[] = []
  private maxCount: number = 5
  private maxSizeMB: number = 10

  build() {
    Column({ space: {spacing-md} }) {
      Text(`已选 ${this.docs.length}/${this.maxCount},单个 ≤ ${this.maxSizeMB}MB`)
        .fontSize({font-size-sm}).fontColor({color-text-secondary})
      Button('选择文件', { buttonStyle: ButtonStyleMode.NORMAL })
        .enabled(this.docs.length < this.maxCount)
        .onClick(async () => {
          let picker = new documentAccess.DocumentViewPicker()
          let result = await picker.select()
          // 逐项校验大小与类型,超限 toast 提示
        })
      ForEach(this.docs, (d: string) => {
        Text(d).fontSize({font-size-md})
      })
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **必须走系统 Picker** — 媒体/文件选取只能经 PhotoViewPicker/DocumentViewPicker,应用无法绕过沙箱直读。
2. **数量与大小前置校验** — `maxSelectNumber` + 应用层大小校验,超限给明确提示(对齐防错原则)。
3. **状态四态** — 等待/上传中(Progress)/成功/失败(可重试),失败项保留文件与重试入口。
4. **无障碍** — 触发器 Button 自带语义;列表项 `accessibilityText` 描述文件名与进度。
5. **触控目标** — 触发器与重试按钮热区 ≥44vp。
