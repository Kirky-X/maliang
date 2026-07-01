# Icon 组件 API 文档

> ArkTS 图标组件,主要用 `SymbolGlyph`(矢量符号图标)与 `Image`(位图图标)。`SymbolSpan` 用于文本内联图标。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `SymbolGlyph` | 系统符号图标(矢量,可着色/动画) |
| `SymbolSpan` | 文本内联符号 |
| `Image` | 位图图标(PNG/SVG) |

## SymbolGlyph 构造函数

```arkts
SymbolGlyph(value?: Resource)
```

## 核心属性表

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| fontSize | Length | 图标大小,用 `{font-size-lg}` |
| fontColor | ResourceColor[] | 颜色(支持多色数组) |
| fontWeight | FontWeight \| number | 线宽 |
| renderingStrategy | SymbolRenderingStrategy | 单色/多色渲染 |
| effectStrategy | SymbolEffectStrategy | 动效:None/Scale/Replace/Hierarchical |
| symbolEffect | SymbolEffect | 弹性/脉冲效果 |

## Image 作图标

```arkts
Image($r('app.media.icon_home')).width(24).height(24).fillColor({color-text-primary})
```

## 最小示例

```arkts
@Entry
@Component
struct IconDemo {
  build() {
    Row({ space: {spacing-md} }) {
      SymbolGlyph($r('sys.symbol.chevron-right'))
        .fontSize({font-size-lg})
        .fontColor([{color-text-primary}])
      Image($r('app.media.icon_home')).width(24).height(24)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`image`](../image/component.md) — 位图图标基于 Image
- [`divider`](../divider/component.md) — 列表项图标 + 文字 + 箭头组合

## 参考链接

- ArkTS 官方文档 - 图标小符号 (SymbolGlyph/SymbolSpan): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-symbol
