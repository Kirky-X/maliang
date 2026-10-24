# Flutter Grid Widget 定义

## Widget 定义

Flutter 网格由 `GridView`(继承自 `BoxScrollView`)承载,通过 `SliverGridDelegate` 控制列数/宽高比/间距。Sliver 体系下可用 `SliverGrid` 嵌入 `CustomScrollView`。`CarouselView` 为 M3 新增的可滚动卡片轮播(见 carousel)。

| Widget | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `GridView` | `GridView` | `BoxScrollView` | 可滚动网格 |
| `SliverGrid` | `SliverGrid` | `SliverMultiBoxAdaptorWidget` | Sliver 网格(嵌入 CustomScrollView) |
| `SliverGridDelegate` | `SliverGridDelegate` | - | 抽象网格布局委托 |
| `SliverGridDelegateWithFixedCrossAxisCount` | - | `SliverGridDelegate` | 固定列数 |
| `SliverGridDelegateWithMaxCrossAxisExtent` | - | `SliverGridDelegate` | 按最大列宽自适应列数 |
| `CarouselView` | `CarouselView` | `BoxScrollView` | M3 卡片轮播(见 carousel) |

## 构造函数

### GridView(常用工厂构造)

```dart
// 固定列数
GridView.count({
  required int crossAxisCount,
  double mainAxisSpacing = 0.0,        // 主轴(行)间距
  double crossAxisSpacing = 0.0,       // 交叉轴(列)间距
  double childAspectRatio = 1.0,       // 子节点宽高比
  ...ScrollView 参数,
  required List<Widget> children,
})

// 按最大列宽自适应
GridView.extent({
  required double maxCrossAxisExtent, // 单元最大宽度
  double mainAxisSpacing = 0.0,
  double crossAxisSpacing = 0.0,
  double childAspectRatio = 1.0,
  required List<Widget> children,
})

// 通用构造(配合 gridDelegate)
GridView({
  required SliverGridDelegate gridDelegate,
  required List<Widget> children,
})

// builder 构造(大数据量,懒加载)
GridView.builder({
  required SliverGridDelegate gridDelegate,
  required IndexedWidgetBuilder itemBuilder,
  int? itemCount,
})
```

### SliverGridDelegate

```dart
// 固定列数
const SliverGridDelegateWithFixedCrossAxisCount({
  required int crossAxisCount,
  double mainAxisSpacing = 0.0,
  double crossAxisSpacing = 0.0,
  double childAspectRatio = 1.0,
})

// 按最大列宽
const SliverGridDelegateWithMaxCrossAxisExtent({
  required double maxCrossAxisExtent,
  double mainAxisSpacing = 0.0,
  double crossAxisSpacing = 0.0,
  double childAspectRatio = 1.0,
})
```

### SliverGrid

```dart
SliverGrid({
  required SliverGridDelegate gridDelegate,
  required SliverChildDelegate delegate,   // SliverChildBuilderAdapter 或 SliverChildListDelegate
})
```

> 属性与方法明细以 [properties.md](properties.md) 为唯一维护处；本文件只讲定义、构造与示例。

## 最小示例

```dart
import 'package:flutter/material.dart';

class GridSample extends StatelessWidget {
  const GridSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Grid 示例')),
      body: GridView.builder(
        padding: const EdgeInsets.all({spacing-sm}),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          mainAxisSpacing: {spacing-sm},
          crossAxisSpacing: {spacing-sm},
          childAspectRatio: 1.0,
        ),
        itemCount: 30,
        itemBuilder: (_, i) => Container(
          decoration: BoxDecoration(
            color: {color-primary},
            borderRadius: BorderRadius.circular({radius-md}),
          ),
          alignment: Alignment.center,
          child: Text('$i',
              style: TextStyle(color: {color-text-on-primary})),
        ),
      ),
    );
  }
}
```

## 参考链接

- Flutter 官方文档 - 列表 & 网格: https://docs.flutter.cn/ui/layout/lists
- Cookbook - 构建一个网格视图: https://docs.flutter.cn/cookbook/lists/grid-lists
- Flutter 官方文档 - 使用 Sliver 实现各种酷炫滚动效果: https://docs.flutter.cn/ui/layout/scrolling/slivers
- API 参考 - GridView: https://api.flutter.dev/flutter/widgets/GridView-class.html
- API 参考 - SliverGrid: https://api.flutter.dev/flutter/widgets/SliverGrid-class.html
