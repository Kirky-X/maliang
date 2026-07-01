# Layout 组件 API 文档

> ArkTS 声明式 UI 的布局体系,提供线性、层叠、弹性、相对、栅格等布局容器。所有可视组件均需置于布局容器中编排。

## 组件定义

ArkTS 布局通过容器组件(`Row`/`Column`/`Flex`/`RelativeContainer`/`Grid`/`GridItem`/`Stack`/`GridRow`/`GridCol`)组织子节点。容器决定子节点的尺寸分配与对齐方式。

## 核心布局容器

| 容器 | 说明 | 主轴方向 |
| --- | --- | --- |
| `Row` | 线性布局 | 水平 |
| `Column` | 线性布局 | 垂直 |
| `Flex` | 弹性布局(支持换行/收缩) | 可配置 |
| `Stack` | 层叠布局 | Z 轴堆叠 |
| `RelativeContainer` | 相对布局 | 锚点对齐 |
| `Grid` / `GridItem` | 网格布局 | 行列 |
| `GridRow` / `GridCol` | 栅格布局(响应式断点) | 12 列 |

## 通用布局属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| width / height | Length | 宽高 |
| padding | Padding | 内边距,用 `{spacing-md}` |
| margin | Margin | 外边距 |
| justifyContent | FlexAlign | 主轴对齐 |
| alignItems | ItemAlign | 交叉轴对齐 |
| layoutWeight | number | 剩余空间权重分配 |
| constraintSize | ConstraintSize | 最小/最大尺寸约束 |
| border / borderRadius | - | 边框,圆角用 `{radius-md}` |

## 最小示例

```arkts
@Entry
@Component
struct LayoutDemo {
  build() {
    Column() {
      // 水平线性布局,两端对齐
      Row() {
        Text('左').fontSize({font-size-md})
        Text('右').fontSize({font-size-md})
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceBetween)
      .padding({spacing-md})

      // 弹性布局自动换行
      Flex({ wrap: FlexWrap.Wrap }) {
        ForEach([1, 2, 3], (item: number) => {
          Text(`项${item}`)
            .padding({spacing-sm})
            .backgroundColor({color-bg-secondary})
        })
      }
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`List`](../list/component.md) — 列表本质是垂直线性布局的滚动容器
- [`tabs`](../tabs/component.md) — 选项卡内部使用线性布局编排标签栏
- [`grid`](../grid/component.md) — Grid 是网格布局容器

## 参考链接

- ArkTS 官方文档 - 组件布局: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development
- 线性布局 (Row/Column): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-linear
- 弹性布局 (Flex): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-flex-layout
- 相对布局 (RelativeContainer): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-relative-layout
- 栅格布局 (GridRow/GridCol): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-grid-layout
