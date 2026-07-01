# Carousel 使用场景与示例

> 列举 ArkTS Swiper 轮播组件的典型使用场景(slug 统一 carousel,ArkTS 原生名 Swiper)。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:首页 Banner 轮播

```arkts
@Entry
@Component
struct BannerCarouselPage {
  private banners: Resource[] = [$r('app.media.b1'), $r('app.media.b2'), $r('app.media.b3')]
  build() {
    Swiper() {
      ForEach(this.banners, (img: Resource) => {
        Image(img).width('100%').height(160).borderRadius({radius-lg})
      })
    }
    .autoPlay(true)
    .interval(4000)
    .loop(true)
    .indicator({
      size: 6,
      color: {color-bg-secondary},
      selectedColor: {color-button-primary-bg}
    })
    .padding({spacing-md})
  }
}
```

## 场景 2:卡片轮播(一屏多卡)

```arkts
@Entry
@Component
struct MultiCardPage {
  private cards: number[] = [1, 2, 3, 4, 5]
  build() {
    Swiper() {
      ForEach(this.cards, (n: number) => {
        Column() {
          Text(`卡片 ${n}`).fontSize({font-size-md})
        }
        .width('80%').height(120)
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
      })
    }
    .displayCount(2)
    .indicator(false)
    .padding({spacing-md})
  }
}
```

## 场景 3:自定义切换动画(Fade 淡入)

```arkts
@Entry
@Component
struct FadeCarouselPage {
  build() {
    Swiper() {
      ForEach([1, 2, 3], (n: number) => {
        Text(`页 ${n}`).fontSize({font-size-lg}).textAlign(TextAlign.Center).width('100%')
      })
    }
    .effectMode(SwiperEffectMode.Fade)
    .duration(500)
    .padding({spacing-md})
  }
}
```

## 场景 4:编程式跳转(SwiperController)

```arkts
@Entry
@Component
struct ControllerCarouselPage {
  private controller: SwiperController = new SwiperController()
  @State current: number = 0
  build() {
    Column({ space: {spacing-md} }) {
      Swiper(this.controller) {
        ForEach([1, 2, 3], (n: number) => {
          Text(`页 ${n}`).fontSize({font-size-lg})
        })
      }
      .onChange((i: number) => this.current = i)

      Row({ space: {spacing-sm} }) {
        Button('上一页').onClick(() => this.controller.showPrevious())
        Button('下一页').onClick(() => this.controller.showNext())
      }
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **loop 默认 true** — 自动循环;首尾衔接;设 `loop(false)` 时到末页停止。
2. **displayCount** — 一屏多项时,需给子项设固定宽度比例,否则挤压变形。
3. **indicator 自定义** — 布尔 `true` 用默认圆点;对象形式自定义大小颜色。
4. **autoPlay 需 loop** — `autoPlay(true)` 通常配合 `loop(true)`,否则到末页停止后不再切换。
5. **vertical 纵向** — 设 `vertical(true)` 上下滑动;常见于竖屏海报轮播。
6. **effectMode Fade** — 淡入淡出无位移效果,适合强调氛围而非顺序的场景。
