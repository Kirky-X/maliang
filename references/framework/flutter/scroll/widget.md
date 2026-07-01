# Flutter Scroll Widget 定义

## Widget 定义

Flutter 滚动体系由"视口(Viewport)+ 滑动配置(ScrollPhysics)+ 控制器(ScrollController)+ 偏移(ScrollOffset)"四层组成。核心 Widget 分为可滚动容器(GridView/ListView/CustomScrollView 等)与 Sliver 系列(在 CustomScrollView 中组合使用)。

| Scroll 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 纵向列表 | `ListView` | `BoxScrollView` | 线性列表(同向滑动) |
| 网格 | `GridView` | `BoxScrollView` | 二维网格 |
| 自定义滚动 | `CustomScrollView` | `ScrollView` | 组合多个 Sliver |
| 横向翻页 | `PageView` | `ScrollView` | 整页滑动(轮播/引导页) |
| 单子节点滚动 | `SingleChildScrollView` | `StatelessWidget` | 单 Widget 滚动(超出视口) |
| 列表固定头部 | `SliverPersistentHeader` | `Sliver` | 吸顶/吸底头部 |
| 列表项分隔 | `SliverList` / `SliverFixedExtentList` | `Sliver` | 滚动主体(按需创建) |
| 网格 Sliver | `SliverGrid` | `Sliver` | Sliver 网格 |
| 滚动监听 | `ScrollNotification` / `ScrollController` | - | 滑动事件监听 |

> `ListView.builder` / `GridView.builder` 默认懒加载,长列表首选;`ListView()` 一次性渲染所有项,仅适用于短列表。

## 构造函数

### ListView

```dart
ListView({
  Key? key,
  Axis scrollDirection = Axis.vertical,
  bool reverse = false,
  ScrollController? controller,
  bool? primary,
  ScrollPhysics? physics,
  bool shrinkWrap = false,
  EdgeInsetsGeometry? padding,
  double? itemExtent,
  Widget? prototypeItem,
  bool addAutomaticKeepAlives = true,
  bool addRepaintBoundaries = true,
  bool addSemanticIndexes = true,
  double? cacheExtent,
  List<Widget> children = const <Widget>[],
  DragStartBehavior dragStartBehavior = DragStartBehavior.start,
  ScrollViewKeyboardDismissBehavior keyboardDismissBehavior = ScrollViewKeyboardDismissBehavior.manual,
  String? restorationId,
  Clip clipBehavior = Clip.hardEdge,
})

ListView.builder({ ... required IndexedWidgetBuilder itemBuilder, required int itemCount, ... })
ListView.separated({ ... required IndexedWidgetBuilder separatorBuilder, ... })
ListView.custom({ ... required SliverChildDelegate childrenDelegate, ... })
```

### CustomScrollView

```dart
const CustomScrollView({
  Key? key,
  Axis scrollDirection = Axis.vertical,
  bool reverse = false,
  ScrollController? controller,
  bool? primary,
  ScrollPhysics? physics,
  bool shrinkWrap = false,
  Key? center,
  double anchor = 0.0,
  double? cacheExtent,
  List<Widget> slivers = const <Widget>[],
  DragStartBehavior dragStartBehavior = DragStartBehavior.start,
  ScrollViewKeyboardDismissBehavior keyboardDismissBehavior = ScrollViewKeyboardDismissBehavior.manual,
  Clip clipBehavior = Clip.hardEdge,
  String? restorationId,
})
```

### PageView

```dart
PageView({
  Key? key,
  Axis scrollDirection = Axis.horizontal,
  bool reverse = false,
  PageController? controller,
  ScrollPhysics? physics,
  bool pageSnapping = true,
  ValueChanged<int>? onPageChanged,
  List<Widget> children = const <Widget>[],
  DragStartBehavior dragStartBehavior = DragStartBehavior.start,
  bool allowImplicitScrolling = false,
  String? restorationId,
  Clip clipBehavior = Clip.hardEdge,
  ScrollBehavior? scrollBehavior,
})

PageView.builder({ ... required IndexedWidgetBuilder itemBuilder, required int itemCount, ... })
```

## 核心属性(通用)

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `scrollDirection` | `Axis` | `Axis.vertical` | 滑动方向(vertical/horizontal) |
| `reverse` | `bool` | `false` | 是否反向(如聊天列表) |
| `controller` | `ScrollController?` | `null` | 控制器(跳转、监听偏移) |
| `primary` | `bool?` | `null` | 是否使用 PrimaryScrollController |
| `physics` | `ScrollPhysics?` | `null`(取 ScrollBehavior) | 滑动物理效果 |
| `shrinkWrap` | `bool` | `false` | 是否按内容大小收缩(禁用视口优化) |
| `padding` | `EdgeInsetsGeometry?` | `null` | 内边距 |
| `itemExtent` | `double?` | `null` | 固定项高度(性能优化) |
| `cacheExtent` | `double?` | `null`(默认 250px) | 视口外预渲染范围 |
| `addAutomaticKeepAlives` | `bool` | `true` | 是否自动保活(防止滚动销毁) |
| `addRepaintBoundaries` | `bool` | `true` | 是否添加 RepaintBoundary |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 裁剪行为 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Scroll 最小示例:ListView / CustomScrollView / PageView
class ScrollSample extends StatelessWidget {
  const ScrollSample({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Scroll 示例'),
          bottom: const TabBar(
            tabs: [Tab(text: 'ListView'), Tab(text: 'Sliver'), Tab(text: 'PageView')],
          ),
        ),
        body: TabBarView(
          children: [
            // 1. ListView.builder
            ListView.builder(
              itemCount: 50,
              itemExtent: {size-md},
              padding: const EdgeInsets.all({spacing-sm}),
              itemBuilder: (context, index) => ListTile(
                leading: CircleAvatar(child: Text('${index + 1}')),
                title: Text('列表项 ${index + 1}'),
                tileColor: {color-surface},
              ),
            ),
            // 2. CustomScrollView + Sliver
            CustomScrollView(
              slivers: [
                SliverAppBar(
                  pinned: true,
                  expandedHeight: {size-xl},
                  flexibleSpace: const FlexibleSpaceBar(title: Text('Sliver 演示')),
                ),
                SliverGrid(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 3,
                    mainAxisSpacing: {spacing-sm},
                    crossAxisSpacing: {spacing-sm},
                    childAspectRatio: 1.0,
                  ),
                  delegate: SliverChildBuilderDelegate(
                    (context, index) => Container(
                      color: {color-primary},
                      alignment: Alignment.center,
                      child: Text('$index'),
                    ),
                    childCount: 30,
                  ),
                ),
              ],
            ),
            // 3. PageView
            PageView.builder(
              itemCount: 5,
              itemBuilder: (context, index) => Container(
                color: index.isEven ? {color-primary} : {color-secondary},
                alignment: Alignment.center,
                child: Text(
                  '第 ${index + 1} 页',
                  style: const TextStyle(fontSize: {font-size-xl}),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 自定义 Sliver(MD3 主题映射)

```dart
SliverPersistentHeader(
  pinned: true,
  delegate: _StickyHeaderDelegate(
    child: Container(
      padding: const EdgeInsets.all({spacing-sm}),
      color: {color-surface},
      child: Text(
        '吸顶头部',
        style: TextStyle(
          color: {color-text-primary},
          fontSize: {font-size-md},
        ),
      ),
    ),
  ),
)
```

> 注:示例中的 `{color-primary}`、`{spacing-sm}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - 滚动: https://docs.flutter.cn/ui/layout/scrolling
- 使用 Sliver 实现各种酷炫滚动效果: https://docs.flutter.cn/ui/layout/scrolling/slivers
- 在列表开头添加一个浮动的顶栏: https://docs.flutter.cn/cookbook/lists/floating-app-bar
- 构建一个平行错位滚动的效果: https://docs.flutter.cn/cookbook/effects/parallax-scrolling
- Widget 目录 - Scrolling: https://docs.flutter.cn/ui/widgets/scrolling
- API 参考 - CustomScrollView: https://api.flutter.dev/flutter/widgets/CustomScrollView-class.html
- API 参考 - ScrollPhysics: https://api.flutter.dev/flutter/widgets/ScrollPhysics-class.html
