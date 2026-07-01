# Card 使用场景与示例

> ArkTS 无原生 Card,本文件给出基于 Column 的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础信息卡片

```arkts
@Entry
@Component
struct BasicCardPage {
  build() {
    Column({ space: {spacing-sm} }) {
      Text('产品名称').fontSize({font-size-md}).fontWeight(FontWeight.Bold)
      Text('这是产品的简短描述,用于介绍产品特性。')
        .fontSize({font-size-sm}).fontColor({color-text-primary})
      Row() {
        Text('¥99').fontSize({font-size-lg}).fontColor({color-danger})
        Blank()
        Button('购买')
          .backgroundColor({color-button-primary-bg})
          .fontColor({color-text-on-primary})
      }
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-md})
    .shadow(ShadowStyle.OUTER_DEFAULT_MD)
    .margin({spacing-md})
  }
}
```

## 场景 2:图文卡片(列表项)

```arkts
@Entry
@Component
struct ImageCardPage {
  build() {
    Column() {
      Image($r('app.media.cover'))
        .width('100%').height(120)
        .objectFit(ImageFit.Cover)
        .borderRadius({ radius: {radius-md}, topLeft: 0, topRight: 0 })
      Column({ space: {spacing-xs} }) {
        Text('卡片标题').fontSize({font-size-md}).fontWeight(FontWeight.Bold)
        Text('描述内容').fontSize({font-size-sm}).fontColor({color-text-primary})
      }
      .padding({spacing-md})
      .alignItems(HorizontalAlign.Start)
    }
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-md})
    .clip(true)
    .shadow(ShadowStyle.OUTER_DEFAULT_MD)
    .margin({spacing-md})
  }
}
```

## 场景 3:可点击卡片(onClick)

```arkts
@Entry
@Component
struct ClickableCardPage {
  build() {
    Column() {
      Column({ space: {spacing-sm} }) {
        Text('点击进入详情').fontSize({font-size-md})
        Text('查看更多 >').fontSize({font-size-sm}).fontColor({color-button-primary-bg})
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
      .borderRadius({radius-md})
      .onClick(() => console.info('卡片点击'))
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:封装可复用卡片组件

```arkts
@Component
struct MyCard {
  @BuilderParam content: () => void
  build() {
    Column() {
      this.content()
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-md})
    .shadow(ShadowStyle.OUTER_DEFAULT_MD)
  }
}

@Entry
@Component
struct ReusableCardPage {
  build() {
    Column() {
      MyCard() {
        Text('通过 @BuilderParam 传入内容').fontSize({font-size-md})
      }
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **clip(true)** — 图片超出圆角区域需设 `clip(true)` 裁剪,否则圆角失效。
2. **shadow 枚举** — `ShadowStyle.OUTER_DEFAULT_SM/MD/LG` 预设阴影;自定义用 `ShadowOptions`。
3. **@BuilderParam 透传** — 封装卡片用 `@BuilderParam` 接收子内容,类似 Vue slot。
4. **点击态** — 可点击卡片建议设 `.stateStyles` 或 `hoverEffect(HoverEffect.Highlight)` 提供反馈。
5. **嵌套阴影** — 卡片内嵌卡片避免多层阴影,视觉混乱;内层用边框区分。
6. **性能** — 大量卡片列表用 `LazyForEach` + 卡片组件复用,避免重复创建阴影开销。
