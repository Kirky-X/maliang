# List 组件 API 文档

> ArkTS 声明式 UI 框架内置的列表容器组件,用于展示纵向或横向滚动的同质数据集合。声明于 `build()` 方法内。

## 组件定义

`List` 是 ArkTS 容器组件之一,通过 `List(...)` 构造函数创建。其直接子组件必须为 `ListItem` 或 `ListItemGroup`,常配合 `LazyForEach` 实现大数据量懒加载。

## 构造函数

```arkts
List(value?: { initialIndex?: number; space?: number | string; scroller?: Scroller })
```

## 核心属性表

| 属性              | 类型                          | 默认值                  | 说明                                                |
| ----------------- | ----------------------------- | ----------------------- | --------------------------------------------------- |
| listDirection     | Axis                          | `Axis.Vertical`         | 滚动方向:`Vertical`(纵向)/`Horizontal`(横向)      |
| scroller          | Scroller                      | -                       | 滚动控制器,支持 scrollTo / scrollToIndex 等编程滚动 |
| space             | number \| string              | -                       | ListItem 之间的间距(仅同层 ListItem 生效)          |
| initialIndex      | number                        | `0`                      | 初始展示项索引                                      |
| divider           | DividerStyle                  | -                       | 分割线样式:{ strokeWidth, color, startMargin, endMargin } |
| scrollBar         | BarState                      | `BarState.Auto`         | 滚动条显示:`Auto` / `On` / `Off`                    |
| edgeEffect        | EdgeEffect                    | `EdgeEffect.Spring`     | 边缘拖拽效果:`Spring`(回弹)/`Fade`(渐隐)/`None`    |
| cachedCount       | number                        | `1`                      | 预渲染项数,配合 LazyForEach 提升滚动流畅度         |
| lanes             | number \| Length              | `1`                      | 列数;>1 时为多列瀑布流(纵向列表)                  |
| sticky            | StickyStyle                   | -                       | 粘性头部:`Header` / `Footer`                       |
| onScrollIndex     | (start, end) => void          | -                       | 滚动时回调首尾可见项索引                            |
| onReachStart      | () => void                    | -                       | 滚动到顶部回调(配合下拉刷新)                      |
| onReachEnd        | () => void                    | -                       | 滚动到底部回调(配合上拉加载)                      |

## ListItem 子组件

```arkts
List() {
  ListItem() {
    // 单个列表项内容,通常为 Row/Column 容器
    Row() {
      Text('列表项')
    }
  }
}
```

| 属性        | 类型    | 说明                          |
| ----------- | ------- | ----------------------------- |
| selectable  | boolean | 是否可选中(配合菜单/长按)   |
| swipeAction | object  | 侧滑操作按钮配置              |

## ListItemGroup 子组件

```arkts
List() {
  ListItemGroup({ header: this.groupHeader, footer: this.groupFooter }) {
    ListItem() { /* ... */ }
    ListItem() { /* ... */ }
  }
}
```

## 最小示例

```arkts
@Entry
@Component
struct ListDemo {
  private data: string[] = ['项目 A', '项目 B', '项目 C']

  build() {
    List({ space: {spacing-sm} }) {
      ForEach(this.data, (item: string) => {
        ListItem() {
          Text(item)
            .fontSize({font-size-md})
            .fontColor({color-text-primary})
            .padding({spacing-md})
            .width('100%')
        }
      }, (item: string) => item)
    }
    .divider({
      strokeWidth: 1,
      color: {color-border-default},
      startMargin: {spacing-md},
      endMargin: {spacing-md}
    })
    .width('100%')
    .height('100%')
  }
}
```

## 关联组件

- [`Text`](../text/component.md) — ListItem 内常用 Text 展示标题与描述
- [`Button`](../button/component.md) — ListItem 末尾常放置 Button 作为操作入口
