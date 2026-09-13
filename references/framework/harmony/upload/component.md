# Upload 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Upload 组件。** 通过系统 Picker(`photoAccessHelper.PhotoViewPicker` / `DocumentViewPicker`)+ `Button` 触发器 + `List` 文件列表 + `Progress` 进度组合实现上传。

## 缺失原因

ArkUI 无统一 `<Upload>` 表单控件;文件/媒体选取由系统安全沙箱的 Picker Kit 承担(应用无法直接访问媒体库),上传流程需应用层组合。

## 替代方案(组合结构)

| 角色 | ArkTS 实现 |
| --- | --- |
| 触发器 | `Button`(选图片/选文件两个入口) |
| 媒体选取 | `photoAccessHelper.PhotoViewPicker`(PhotoViewPicker.select) |
| 文件选取 | `DocumentViewPicker`(DocumentSelectOptions) |
| 文件列表 | `List` + `ListItem`(缩略图 + 文件名 + 状态) |
| 进度/状态 | `Progress`(线性)+ 状态文本(上传中/成功/失败重试) |

## 核心组合 API

```arkts
import { photoAccessHelper } from '@kit.MediaLibraryKit'
import { documentAccess } from '@kit.CoreFileKit'

// 图片选取
let picker = new photoAccessHelper.PhotoViewPicker()
let result = await picker.select({
  MIMEType: photoAccessHelper.PhotoViewMIMETypes.IMAGE_TYPE,
  maxSelectNumber: 9
})
// result.photoUris: string[]

// 文件选取
let docPicker = new documentAccess.DocumentViewPicker()
let docResult = await docPicker.select() // 返回文件 URI 列表
```

## 最小示例

```arkts
@Entry
@Component
struct UploadDemo {
  @State files: Array<{ name: string, uri: string, progress: number }> = []
  private picker = new photoAccessHelper.PhotoViewPicker()

  async pick() {
    let result = await this.picker.select({
      MIMEType: photoAccessHelper.PhotoViewMIMETypes.IMAGE_TYPE,
      maxSelectNumber: 9
    })
    this.files = result.photoUris.map((uri: string, i: number) => ({
      name: `图片 ${i + 1}`, uri, progress: 0
    }))
    // 逐个上传,更新 progress
  }

  build() {
    Column({ space: {spacing-md} }) {
      Button('选择图片').onClick(() => this.pick())
      List({ space: {spacing-sm} }) {
        ForEach(this.files, (f: { name: string, uri: string, progress: number }) => {
          ListItem() {
            Row({ space: {spacing-sm} }) {
              Image(f.uri).width(48).height(48).borderRadius({radius-sm})
              Text(f.name).fontSize({font-size-md}).layoutWeight(1)
              Progress({ value: f.progress, total: 100, type: ProgressType.Linear })
                .width(96)
            }
          }
        })
      }
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`progress`](../progress/component.md) — 上传进度
- [`button`](../button/component.md) — 触发器
- [`message`](../message/component.md) — 上传结果 toast

## 参考链接

- HarmonyOS 官方文档 - 选择并获取媒体资源: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/selecting-media-assets
- HarmonyOS 官方文档 - DocumentViewPicker: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/js-apis-file-picker
