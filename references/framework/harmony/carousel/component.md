# Carousel 组件 API 文档

> ArkTS 轮播组件。**注意:目录 slug 统一用 `carousel`,ArkTS 原生组件名为 `Swiper`。** 支持自动播放、循环、指示器、自定义动画。

## 组件定义

`Swiper` 容器承载多个子组件(通常为 `Image` 或卡片),横向/纵向滑动切换。

## 构造函数

```arkts
Swiper(value?: { controller?: SwiperController; index?: number; ... })
```

## 核心属性表

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| index | number | 当前页索引 |
| autoPlay | boolean | 是否自动播放 |
| interval | number | 自动切换间隔(ms),默认 3000 |
| loop | boolean | 是否循环,默认 true |
| vertical | boolean | 是否纵向滑动,默认 false |
| indicator | boolean \| IndicatorStyle | 指示器(布尔或自定义样式) |
| duration | number | 切换动画时长(ms) |
| displayCount | number \| SwiperAutoFill | 同屏显示项数 |
| effectMode | SwiperEffectMode | 切换动画:None/Cover/Fade |
| onChange | (index: number) => void | 切换回调 |

## IndicatorStyle(自定义指示器)

```arkts
indicator: {
  size: 8,
  color: {color-bg-secondary},
  selectedColor: {color-button-primary-bg},
  mask: false
}
```

## 最小示例

```arkts
@Entry
@Component
struct CarouselDemo {
  private imgs: Resource[] = [$r('app.media.a'), $r('app.media.b'), $r('app.media.c')]
  build() {
    Swiper() {
      ForEach(this.imgs, (img: Resource) => {
        Image(img).width('100%').height(160).borderRadius({radius-md})
      })
    }
    .autoPlay(true)
    .interval(3000)
    .indicator(true)
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`tabs`](../tabs/component.md) — Tabs 也是页签切换,Swiper 更偏内容轮播
- [`image`](../image/component.md) — 轮播内容常用 Image

## 参考链接

- ArkTS 官方文档 - 创建轮播 (Swiper): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-looping
- 创建弧形轮播 (ArcSwiper): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-arcswiper
