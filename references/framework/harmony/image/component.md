# Image 组件 API 文档

> ArkTS 图片组件,用于展示本地、网络、资源图片,支持裁剪、缩放、圆角等处理。

## 组件定义

`Image` 通过传入图片源(`string` / `Resource` / `PixelMap`)创建,支持本地资源 `$r('app.media.xxx')`、网络 URL 与内存图片。

## 构造函数

```arkts
Image(src: string | Resource | PixelMap, options?: ImageOptions)
```

## 核心属性表

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| src | string \| Resource \| PixelMap | - | 图片源 |
| width / height | Length | - | 宽高,缺省按原图尺寸 |
| objectFit | ImageFit | `ImageFit.Cover` | 缩放模式:Contain/Cover/Auto/Fill/ScaleDown |
| objectRepeat | ImageRepeat | `NoRepeat` | 平铺模式 |
| interpolation | ImageInterpolation | `None` | 插值(放大平滑) |
| border | Border | - | 边框 |
| borderRadius | Length | - | 圆角,用 `{radius-md}` |
| opacity | number | `1` | 透明度 |
| alt | string \| Resource | - | 加载失败时占位图 |
| syncLoad | boolean | `false` | 是否同步加载 |
| matchTextDirection | boolean | `false` | 是否跟随文字方向 |
| draggable | boolean | `false` | 是否可拖拽 |
| onComplete | (event) => void | - | 加载完成回调 |
| onError | (event) => void | - | 加载失败回调 |

## ImageFit 枚举

| 值 | 描述 |
| --- | --- |
| `Contain` | 保持比例,完整显示,可能留白 |
| `Cover` | 保持比例,填满容器,可能裁剪 |
| `Auto` | 保持原图尺寸 |
| `Fill` | 拉伸填满,不保持比例 |
| `ScaleDown` | 等比缩小,不放大 |

## 最小示例

```arkts
@Entry
@Component
struct ImageDemo {
  build() {
    Column() {
      Image($r('app.media.logo'))
        .width(120).height(120)
        .objectFit(ImageFit.Cover)
        .borderRadius({radius-md})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`icon`](../icon/component.md) — 图标用法(SymbolGlyph/Image)
- [`avatar`](../avatar/component.md) — 头像基于 Image 圆形裁剪

## 参考链接

- ArkTS 官方文档 - 显示图片 (Image): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-graphics-display
