# Grid 组件 API 文档

> ArkTS 网格列表组件,本文件聚焦数据网格场景。`Grid` 为容器,`GridItem` 为单元格。与 [`layout`](../layout/component.md) 中的布局 Grid 互补。

## 组件定义

`Grid` 通过 `columnsTemplate` / `rowsTemplate` 定义网格骨架,内部用 `GridItem` 承载内容,支持横向/纵向滚动、瀑布流变体 `WaterFlow`。

## 构造函数

```arkts
Grid(value?: { scroller?: Scroller; layoutOptions?: GridLayoutOptions })
GridItem(value?: { rowStart?: number; rowEnd?: number; columnStart?: number; columnEnd?: number })
```

## 核心属性表

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| columnsTemplate | string | 列模板,如 `'1fr 1fr 1fr'`(3 列) |
| rowsTemplate | string | 行模板 |
| columnsGap / rowsGap | Length | 列/行间距,用 `{spacing-sm}` |
| scrollBar | BarState | 滚动条显示 |
| cachedCount | number | 缓存项数 |
| enableScrollInteraction | boolean | 是否允许手势滚动 |
| onReachStart / onReachEnd | () => void | 到顶/到底回调 |
| onScrollIndex | (first, last) => void | 可视区索引变化 |

## GridItem 跨列属性

| 属性 | 说明 |
| --- | --- |
| columnStart / columnEnd | 跨多列(类似 colspan) |
| rowStart / rowEnd | 跨多行(类似 rowspan) |

## 最小示例

```arkts
@Entry
@Component
struct GridDemo {
  private data: number[] = [1, 2, 3, 4, 5, 6]
  build() {
    Grid() {
      ForEach(this.data, (n: number) => {
        GridItem() {
          Text(`项${n}`).fontSize({font-size-md})
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

## 关联组件

- [`layout`](../layout/component.md) — 布局 Grid 与本数据网格互补
- [`list`](../list/component.md) — 一维列表,Grid 是二维扩展

## 参考链接

- ArkTS 官方文档 - 创建网格 (Grid/GridItem): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-grid
- 创建瀑布流 (WaterFlow): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-waterflow
