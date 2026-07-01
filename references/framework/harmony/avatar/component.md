# Avatar 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Avatar 头像组件。** 通过 `Image`(图片头像)+ `borderRadius(radius-full)` 圆形裁剪 + `border` 装饰实现。

## 缺失原因

ArkTS 没有专门头像组件。头像本质是圆形图片,用 `Image` + `objectFit(Cover)` + `borderRadius(radius-full)` 即可;无图片时用 `Text` 取首字母作占位。

## 替代方案

- **方案 1:Image 圆形裁剪** — 有图片资源时,`Image().borderRadius({radius-full})` 最直接。
- **方案 2:Text 首字母占位** — 无图片时,用文字首字母 + 背景色圆形容器。
- **方案 3:Badge 包裹角标** — 头像带在线状态/消息角标,用 `Badge` 包裹 Image。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:Image 圆形) |
| Flutter | `CircleAvatar` |
| Element Plus | `<el-avatar>` |

## 最小示例

```arkts
@Entry
@Component
struct AvatarDemo {
  build() {
    Row({ space: {spacing-md} }) {
      Image($r('app.media.user1'))
        .width(48).height(48)
        .objectFit(ImageFit.Cover)
        .borderRadius({radius-full})
      Column() {
        Text('圆形头像').fontSize({font-size-sm})
      }
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`image`](../image/component.md) — 头像基于 Image
- [`badge`](../badge/component.md) — 头像角标

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`image`](../image/component.md)
- 显示图片 (Image): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-graphics-display
