# Flutter Grid 属性列表与默认值

本文档汇总 `GridView` / `SliverGrid` / `SliverGridDelegate` 的属性、默认值与回调。

## GridView 属性(继承 ScrollView)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `scrollDirection` | `Axis` | `Axis.vertical` | 滚动方向 |
| `reverse` | `bool` | `false` | 是否反向滚动 |
| `controller` | `ScrollController?` | `null` | 滚动控制器 |
| `primary` | `bool?` | `null` | 是否主滚动 |
| `physics` | `ScrollPhysics?` | `null` | 滚动物理 |
| `shrinkWrap` | `bool` | `false` | 是否收缩到内容尺寸 |
| `padding` | `EdgeInsetsGeometry?` | `null` | 内边距 |
| `gridDelegate` | `SliverGridDelegate` | 必填 | 网格布局委托 |
| `addAutomaticKeepAlives` | `bool` | `true` | 自动保活 |
| `addRepaintBoundaries` | `bool` | `true` | 自动重绘边界 |
| `addSemanticIndexes` | `bool` | `true` | 语义索引 |
| `cacheExtent` | `double?` | `null` | 缓存区高度 |

### builder 模式额外

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `itemBuilder` | `IndexedWidgetBuilder` | 子项构建函数 |
| `itemCount` | `int?` | 子项数量(null 为无限) |
| `findChildIndexCallback` | `ChildIndexGetter?` | key→index 回调(重排优化) |

## SliverGridDelegateWithFixedCrossAxisCount 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `crossAxisCount` | `int` | 必填 | 列数 |
| `mainAxisSpacing` | `double` | `0.0` | 主轴间距(垂直网格为行间距) |
| `crossAxisSpacing` | `double` | `0.0` | 交叉轴间距(列间距) |
| `childAspectRatio` | `double` | `1.0` | 子节点宽/高比 |

## SliverGridDelegateWithMaxCrossAxisExtent 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `maxCrossAxisExtent` | `double` | 必填 | 单元最大宽度(自动算列数) |
| `mainAxisSpacing` | `double` | `0.0` | 行间距 |
| `crossAxisSpacing` | `double` | `0.0` | 列间距 |
| `childAspectRatio` | `double` | `1.0` | 子节点宽/高比 |

## SliverGrid 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `gridDelegate` | `SliverGridDelegate` | 必填 | 网格布局委托 |
| `delegate` | `SliverChildDelegate` | 必填 | 子节点委托(builder/list) |

## 列数计算规则

### FixedCrossAxisCount

列数固定为 `crossAxisCount`,单元宽度 = (视口宽 - (列数-1)×列间距) / 列数。

### MaxCrossAxisExtent

列数 = `(视口宽 / maxCrossAxisExtent).ceil()`,单元宽度自适应。例如视口 360、`maxCrossAxisExtent: 120` → 列数 3,每列约 120。

## 完整示例

```dart
import 'package:flutter/material.dart';

class GridFullSample extends StatelessWidget {
  const GridFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Grid 完整示例'),
          bottom: const TabBar(tabs: [
            Tab(text: '固定列'),
            Tab(text: '自适应'),
            Tab(text: 'Sliver'),
          ]),
        ),
        body: TabBarView(
          children: [
            // 1. 固定 2 列
            GridView.builder(
              padding: const EdgeInsets.all({spacing-sm}),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                mainAxisSpacing: {spacing-sm},
                crossAxisSpacing: {spacing-sm},
                childAspectRatio: 0.75, // 卡片偏窄高
              ),
              itemCount: 20,
              itemBuilder: (_, i) => _card(i),
            ),
            // 2. 自适应列数(每列约 160)
            GridView.builder(
              padding: const EdgeInsets.all({spacing-sm}),
              gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                maxCrossAxisExtent: 160,
                mainAxisSpacing: {spacing-sm},
                crossAxisSpacing: {spacing-sm},
                childAspectRatio: 1.0,
              ),
              itemCount: 30,
              itemBuilder: (_, i) => _card(i),
            ),
            // 3. SliverGrid 嵌入 CustomScrollView
            CustomScrollView(
              slivers: [
                const SliverAppBar(title: Text('Sliver 网格')),
                SliverGrid(
                  gridDelegate:
                      const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 3,
                    crossAxisSpacing: {spacing-sm},
                    mainAxisSpacing: {spacing-sm},
                  ),
                  delegate: SliverChildBuilderDelegate(
                    (_, i) => _card(i),
                    childCount: 50,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _card(int i) => Container(
        decoration: BoxDecoration(
          color: {color-bg-secondary},
          borderRadius: BorderRadius.circular({radius-md}),
        ),
        alignment: Alignment.center,
        child: Text('Item $i',
            style: TextStyle(fontSize: {font-size-md})),
      );
}
```

## 注意事项

- `GridView.count` / `GridView.extent` 适合小数据量(直接传 children);大数据量用 `GridView.builder`(懒加载)
- `childAspectRatio` 是"宽/高",>1 为扁,<1 为窄高
- `SliverGridDelegateWithMaxCrossAxisExtent` 更适合响应式(不同屏宽自动调整列数)
- `GridView` 嵌入 `Column` 时需设 `shrinkWrap: true` 或用 `Expanded` 包裹,否则无界高度崩溃
- Sliver 模式(`SliverGrid` + `CustomScrollView`)可混合多种滚动布局(如顶部 Appbar + 网格 + 列表)
- 大量子项推荐用 `GridView.builder` + `itemExtent`(若固定尺寸)以提升性能
