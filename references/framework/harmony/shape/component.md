# Shape 组件 API 文档

> ArkTS 几何图形绘制组件,包含 `Shape`(画布容器)、`Line`(线)、`Circle`(圆)、`Polyline`(折线)、`Polygon`(多边形)、`Path`(路径)、`Rect`(矩形)。

## 组件定义

`Shape` 作为画布容器承载各类图形子组件;每个图形组件也可独立使用,自带默认 `Shape` 父级。

## 图形组件清单

| 组件 | 说明 | 关键参数 |
| --- | --- | --- |
| `Shape` | 画布容器 | width/height/viewport |
| `Line` | 直线 | start/end 点坐标 |
| `Circle` | 圆形 | cx/cy(圆心) + r(半径) |
| `Polyline` | 折线(不闭合) | points 点序列 |
| `Polygon` | 多边形(闭合) | points 点序列 |
| `Path` | 路径(SVG 路径命令) | commands |
| `Rect` | 矩形 | x/y + width/height + rx/ry(圆角) |

## 通用样式属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| fill | ResourceColor | 填充色,`Color.Transparent` 表示不填充 |
| stroke | ResourceColor | 描边色 |
| strokeWidth | Length | 描边宽度 |
| strokeDashArray | Length[] | 虚线段 |
| strokeDashOffset | Length | 虚线偏移 |
| strokeLinecap | LineCapStyle | 端点:Butt/Round/Square |
| strokeLinejoin | LineJoinStyle | 拐角:Miter/Round/Bevel |
| antiAlias | boolean | 抗锯齿 |

## 最小示例

```arkts
@Entry
@Component
struct ShapeDemo {
  build() {
    Column() {
      Shape() {
        Circle({ width: 60, height: 60 })
          .fill({color-button-primary-bg})
        Rect({ width: 80, height: 40 }).fill(Color.Transparent)
          .stroke({color-border-default}).strokeWidth(2)
      }
      .width(100).height(100)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`divider`](../divider/component.md) — 分割线可用 Line 实现
- [`layout`](../layout/component.md) — Shape 作装饰背景叠加于布局

## 参考链接

- ArkTS 官方文档 - 几何图形绘制: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-draw-graphics
- 绘制几何图形 (Shape): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-geometric-shape-drawing
- 形状裁剪 (clipShape): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-clip-shape
