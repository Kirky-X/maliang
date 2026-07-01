# Flutter Tabs Widget 定义

## Widget 定义

Flutter Material 选项卡由三个 Widget 协同:`TabBar`(选项卡条)、`TabBarView`(选项卡内容页)、`DefaultTabController`(状态控制器)。`TabBar` 显示可点击的 `Tab` 标签,`TabBarView` 根据选中索引切换页面,二者通过 `TabController` 同步状态。继承关系:`TabBar` / `TabBarView` 均为 `StatefulWidget`,`DefaultTabController` 为 `StatelessWidget`。

| Widget | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `TabBar` | `TabBar` | `StatefulWidget` | 顶部选项卡条 |
| `TabBarView` | `TabBarView` | `StatefulWidget` | 可横向滑动的页面容器 |
| `DefaultTabController` | `DefaultTabController` | `StatelessWidget` | 自动管理 TabController |
| `TabController` | `TabController` | `ChangeNotifier` | 状态控制器(手动管理) |
| `Tab` | `Tab` | `StatelessWidget` | 单个标签(文本/图标) |
| `TabBarIndicator` | `TabBarIndicator` | - | 选中指示器样式 |

## 构造函数

### TabBar

```dart
const TabBar({
  super.key,
  required List<Widget> tabs,
  TabController? controller,
  bool isScrollable = false,
  EdgeInsetsGeometry padding = EdgeInsets.zero,
  Color? indicatorColor,
  double indicatorWeight = 2.0,
  EdgeInsetsGeometry indicatorPadding = EdgeInsets.zero,
  Decoration? indicator,                  // 自定义指示器
  TabBarIndicatorSize? indicatorSize,
  Color? labelColor,
  TextStyle? labelStyle,
  EdgeInsetsGeometry labelPadding = EdgeInsets.zero,
  Color? unselectedLabelColor,
  TextStyle? unselectedLabelStyle,
  DragStartBehavior dragStartBehavior = DragStartBehavior.start,
  MaterialStateProperty<MouseCursor?>? mouseCursor,
  ValueChanged<int>? onTap,
  ...
})
```

### TabBarView

```dart
const TabBarView({
  super.key,
  required List<Widget> children,
  TabController? controller,
  ScrollPhysics? physics,
  DragStartBehavior dragStartBehavior = DragStartBehavior.start,
  double viewportFraction = 1.0,
})
```

### DefaultTabController

```dart
const DefaultTabController({
  super.key,
  required int length,          // 选项卡数量
  int initialIndex = 0,
  required Widget child,
  Duration? animationDuration,
})
```

### Tab

```dart
const Tab({
  super.key,
  String? text,
  Widget? icon,
  EdgeInsetsGeometry iconMargin = const EdgeInsets.only(bottom: 10),
  Widget? child,
})
```

## 核心属性

### TabBar 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `tabs` | `List<Widget>` | 标签列表(通常为 `Tab`) |
| `controller` | `TabController?` | 状态控制器(省略时取 `DefaultTabController`) |
| `isScrollable` | `bool` | 标签多时可滚动 |
| `indicatorColor` | `Color?` | 指示器颜色 |
| `indicatorWeight` | `double` | 指示器厚度,默认 2.0 |
| `indicatorSize` | `TabBarIndicatorSize?` | 指示器宽度(tab/label) |
| `labelColor` | `Color?` | 选中标签颜色 |
| `labelStyle` | `TextStyle?` | 选中标签样式 |
| `unselectedLabelColor` | `Color?` | 未选中标签颜色 |
| `onTap` | `ValueChanged<int>?` | 点击回调 |

### TabBarView 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `children` | `List<Widget>` | 各选项卡页面 |
| `controller` | `TabController?` | 状态控制器 |
| `physics` | `ScrollPhysics?` | 滑动物理 |

## 最小示例

```dart
import 'package:flutter/material.dart';

class TabsSample extends StatelessWidget {
  const TabsSample({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Tabs 示例'),
          bottom: const TabBar(
            tabs: [
              Tab(text: '首页'),
              Tab(text: '发现'),
              Tab(text: '我的'),
            ],
            labelColor: {color-primary},
            unselectedLabelColor: {color-text-primary},
            indicatorColor: {color-primary},
          ),
        ),
        body: const TabBarView(
          children: [
            Center(child: Text('首页内容')),
            Center(child: Text('发现内容')),
            Center(child: Text('我的内容')),
          ],
        ),
      ),
    );
  }
}
```

## 自定义指示器

通过 `indicator` 传入 `UnderlineTabIndicator` 或自定义 `Decoration`:

```dart
TabBar(
  indicator: UnderlineTabIndicator(
    borderSide: BorderSide(width: 3.0, color: {color-primary}),
    insets: const EdgeInsets.symmetric(horizontal: {spacing-sm}),
  ),
  indicatorSize: TabBarIndicatorSize.label,
  tabs: const [Tab(text: 'A'), Tab(text: 'B')],
)
```

## 参考链接

- Cookbook - 在应用中添加 Tab 导航: https://docs.flutter.cn/cookbook/design/tabs
- Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - TabBar: https://api.flutter.dev/flutter/material/TabBar-class.html
- API 参考 - TabBarView: https://api.flutter.dev/flutter/material/TabBarView-class.html
- API 参考 - DefaultTabController: https://api.flutter.dev/flutter/material/DefaultTabController-class.html
