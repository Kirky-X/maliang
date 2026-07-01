# Shape 使用场景与示例

> 列举 ArkTS 几何图形绘制组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:圆形指示点

```arkts
@Entry
@Component
struct CircleDotPage {
  build() {
    Row({ space: {spacing-sm} }) {
      Circle({ width: 8, height: 8 }).fill({color-button-primary-bg})
      Circle({ width: 8, height: 8 }).fill({color-bg-secondary})
      Circle({ width: 8, height: 8 }).fill({color-bg-secondary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:折线趋势图

```arkts
@Entry
@Component
struct PolylineChartPage {
  build() {
    Shape() {
      Polyline()
        .points([[0, 80], [20, 50], [40, 60], [60, 30], [80, 40], [100, 10]])
        .fill(Color.Transparent)
        .stroke({color-button-primary-bg})
        .strokeWidth(2)
        .strokeLinecap(LineCapStyle.Round)
    }
    .width(120).height(100)
    .padding({spacing-md})
  }
}
```

## 场景 3:虚线分割(Line + dashArray)

```arkts
@Entry
@Component
struct DashedLinePage {
  build() {
    Line()
      .start([0, 0]).end([300, 0])
      .stroke({color-border-default})
      .strokeWidth(1)
      .strokeDashArray([6, 4])
      .padding({spacing-md})
  }
}
```

## 场景 4:圆角矩形卡片描边

```arkts
@Entry
@Component
struct RectBorderPage {
  build() {
    Shape() {
      Rect({ width: 160, height: 80 })
        .radiusWidth(8).radiusHeight(8)
        .fill({color-bg-primary})
        .stroke({color-border-default})
        .strokeWidth(1)
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:自定义 Path(对勾)

```arkts
@Entry
@Component
struct PathCheckPage {
  build() {
    Path()
      .commands('M10 50 L40 80 L90 20')
      .fill(Color.Transparent)
      .stroke({color-success})
      .strokeWidth(4)
      .strokeLinecap(LineCapStyle.Round)
      .strokeLinejoin(LineJoinStyle.Round)
      .width(100).height(100)
      .padding({spacing-md})
  }
}
```

## 注意事项

1. **fill 必须显式设置** — 默认黑色填充;只想描边时设 `fill(Color.Transparent)`。
2. **坐标系** — Shape 内部坐标相对于自身 viewport,非屏幕绝对坐标。
3. **Path 命令** — 兼容 SVG path 语法(M/L/C/Q/Z 等);复杂图形建议用 SVG 设计后导出。
4. **性能** — Shape 适合静态简单图形;复杂动画用 `Canvas` 或 `RenderNode`。
5. **strokeLinecap** — 折线/路径端点圆角用 `Round`,默认 `Butt` 看起来生硬。
6. **抗锯齿** — 默认开启 `antiAlias(true)`;小尺寸图形关闭可提升性能但边缘锯齿。
