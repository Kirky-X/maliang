# Image 使用场景与示例

> 列举 ArkTS Image 组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:网络图片加载(含占位与错误)

```arkts
@Entry
@Component
struct NetworkImagePage {
  build() {
    Column() {
      Image('https://example.com/cover.jpg')
        .width('100%').height(200)
        .objectFit(ImageFit.Cover)
        .borderRadius({radius-lg})
        .alt($r('app.media.placeholder'))
        .onError(() => console.info('图片加载失败'))
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:圆形头像(Cover + borderRadius)

```arkts
@Entry
@Component
struct AvatarImagePage {
  build() {
    Image($r('app.media.avatar'))
      .width(64).height(64)
      .objectFit(ImageFit.Cover)
      .borderRadius({radius-full})
      .border({ width: 1, color: {color-border-default} })
  }
}
```

## 场景 3:封面图(固定比例填充)

```arkts
@Entry
@Component
struct CoverImagePage {
  build() {
    Stack() {
      Image($r('app.media.banner'))
        .width('100%').height(180)
        .objectFit(ImageFit.Cover)
      Text('精选')
        .fontSize({font-size-sm})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-danger})
        .padding({spacing-xs})
        .borderRadius({radius-sm})
        .position({ x: {spacing-md}, y: {spacing-md} })
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:图标按钮中的图片

```arkts
@Entry
@Component
struct IconButtonImagePage {
  build() {
    Row() {
      Image($r('app.media.icon_back'))
        .width(24).height(24)
        .fillColor({color-text-primary})
      Text('返回')
        .fontSize({font-size-md})
        .fontColor({color-text-primary})
        .margin({ left: {spacing-sm} })
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:画廊网格(Image + Grid)

```arkts
@Entry
@Component
struct GalleryPage {
  private imgs: string[] = ['a', 'b', 'c', 'd', 'e', 'f']
  build() {
    Grid() {
      ForEach(this.imgs, (name: string) => {
        GridItem() {
          Image($r(`app.media.${name}`))
            .aspectRatio(1)
            .objectFit(ImageFit.Cover)
            .borderRadius({radius-md})
        }
      })
    }
    .columnsTemplate('1fr 1fr 1fr')
    .columnsGap({spacing-sm})
    .rowsGap({spacing-sm})
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **网络图片需声明权限** — `ohos.permission.INTERNET` 在 module.json5 配置;否则加载失败无报错。
2. **objectFit 默认 Cover** — 与 Web `<img>` 默认 `Fill` 不同,会裁剪以填满,需显式确认预期。
3. **alt 占位** — 网络图片建议设置 `alt`,加载失败时显示占位图,避免空白。
4. **fillColor 仅矢量图生效** — 对 SVG/PNG 着色需注意资源格式,位图无法着色。
5. **大图性能** — 列表内大量图片建议用 `syncLoad(false)` 异步加载,避免阻塞渲染。
6. **aspectRatio** — 用 `aspectRatio(ratio)` 锁定比例,比固定宽高更适配不同屏幕。
