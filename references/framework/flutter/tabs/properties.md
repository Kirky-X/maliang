# Flutter Tabs 属性列表与默认值

本文档汇总 `TabBar` / `TabBarView` / `DefaultTabController` / `Tab` 的属性、默认值与回调。颜色/尺寸默认值以 design token 形式给出。

## TabBar 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `tabs` | `List<Widget>` | 必填 | 标签列表(通常为 `Tab`) |
| `controller` | `TabController?` | `null`(取 DefaultTabController) | 状态控制器 |
| `isScrollable` | `bool` | `false` | 标签可滚动(标签多时为 true) |
| `padding` | `EdgeInsetsGeometry` | `EdgeInsets.zero` | 整体内边距 |
| `indicatorColor` | `Color?` | `Theme.of(context).indicatorColor` | 指示器颜色 |
| `indicatorWeight` | `double` | `2.0` | 指示器厚度 |
| `indicatorPadding` | `EdgeInsetsGeometry` | `EdgeInsets.zero` | 指示器内边距 |
| `indicator` | `Decoration?` | `null` | 自定义指示器(覆盖 indicatorColor/Weight) |
| `indicatorSize` | `TabBarIndicatorSize?` | `null`(M3 为 label) | 指示器宽度(tab/label) |
| `dividerColor` | `Color?` | `Theme.of(context).dividerColor` | 分割线颜色(M3 新增) |
| `dividerHeight` | `double?` | `1.0` | 分割线高度 |
| `labelColor` | `Color?` | `Theme.of(context).primaryColor` | 选中标签颜色 |
| `labelStyle` | `TextStyle?` | `Theme.textTheme.labelLarge` | 选中标签文本样式 |
| `labelPadding` | `EdgeInsetsGeometry` | `EdgeInsets.zero` | 标签内边距 |
| `unselectedLabelColor` | `Color?` | `labelColor.withOpacity(0.6)` | 未选中标签颜色 |
| `unselectedLabelStyle` | `TextStyle?` | `labelStyle` | 未选中标签文本样式 |
| `dragStartBehavior` | `DragStartBehavior` | `DragStartBehavior.start` | 拖动起始行为 |
| `overlayColor` | `MaterialStateProperty<Color?>?` | `null` | 悬停/按压叠加色 |
| `mouseCursor` | `MaterialStateProperty<MouseCursor?>?` | `null` | 鼠标光标 |
| `onTap` | `ValueChanged<int>?` | `null` | 点击回调(参数为索引) |
| `enableFeedback` | `bool` | `true` | 触觉/声音反馈 |

## TabBarView 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<Widget>` | 必填 | 各选项卡页面 |
| `controller` | `TabController?` | `null` | 状态控制器 |
| `physics` | `ScrollPhysics?` | `null`(默认 Bouncing) | 滑动物理 |
| `dragStartBehavior` | `DragStartBehavior` | `DragStartBehavior.start` | 拖动起始行为 |
| `viewportFraction` | `double` | `1.0` | 每页占视口比例(<1 可露出相邻页) |

## DefaultTabController 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `length` | `int` | 必填 | 选项卡数量 |
| `initialIndex` | `int` | `0` | 初始选中索引 |
| `child` | `Widget` | 必填 | 子树(其内可用 `TabBar`/`TabBarView`) |
| `animationDuration` | `Duration?` | `null` | 动画时长 |

## Tab 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `text` | `String?` | `null` | 标签文本(与 child 互斥) |
| `icon` | `Widget?` | `null` | 标签图标 |
| `iconMargin` | `EdgeInsetsGeometry` | `EdgeInsets.only(bottom: 10)` | 图标与文本间距 |
| `child` | `Widget?` | `null` | 自定义标签内容 |

## TabController 属性

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `length` | `int` | 选项卡数量 |
| `index` | `int` | 当前选中索引(可读写) |
| `previousIndex` | `int` | 上一个选中索引 |
| `offset` | `double` | 滑动偏移(动画中非 0) |
| `animation` | `Animation<double>?` | 动画对象(可用于监听过渡) |
| `indexIsChanging` | `bool` | 索引是否正在变化 |

### TabController 事件

```dart
final controller = TabController(length: 3, vsync: this);
controller.addListener(() {
  if (!controller.indexIsChanging) {
    debugPrint('切换到 ${controller.index}');
  }
});
```

## TabBarIndicatorSize 取值

| 取值 | 行为 |
| --- | --- |
| `tab` | 指示器占满整个 Tab 宽度 |
| `label` | 指示器仅占标签文本宽度(M3 默认) |

## 完整示例

```dart
import 'package:flutter/material.dart';

class TabsFullSample extends StatefulWidget {
  const TabsFullSample({super.key});

  @override
  State<TabsFullSample> createState() => _TabsFullSampleState();
}

class _TabsFullSampleState extends State<TabsFullSample>
    with TickerProviderStateMixin {
  late TabController _controller;
  int _lastIndex = 0;

  @override
  void initState() {
    super.initState();
    _controller = TabController(length: 4, vsync: this);
    _controller.addListener(() {
      if (!_controller.indexIsChanging && _controller.index != _lastIndex) {
        setState(() => _lastIndex = _controller.index);
        debugPrint('切换到 $_lastIndex');
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tabs 完整示例'),
        bottom: TabBar(
          controller: _controller,
          isScrollable: true,
          labelColor: {color-primary},
          unselectedLabelColor: {color-text-primary},
          indicatorColor: {color-primary},
          indicatorSize: TabBarIndicatorSize.label,
          indicatorWeight: 3.0,
          labelStyle: const TextStyle(
            fontSize: {font-size-md},
            fontWeight: FontWeight.w600,
          ),
          onTap: (i) => debugPrint('点击 $i'),
          tabs: const [
            Tab(text: '推荐'),
            Tab(text: '关注'),
            Tab(text: '热门'),
            Tab(icon: Icon(Icons.star), text: '收藏'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _controller,
        children: const [
            Center(child: Text('推荐内容')),
            Center(child: Text('关注内容')),
            Center(child: Text('热门内容')),
            Center(child: Text('收藏内容')),
        ],
      ),
    );
  }
}
```

## 注意事项

- `TabController` 需 `TickerProviderStateMixin`(或 `SingleTickerProviderStateMixin`),`vsync: this`
- `TabBar` 与 `TabBarView` 的 `children`/`tabs` 数量必须一致,否则越界崩溃
- `DefaultTabController` 适用于简单场景;需监听切换或动态增删 Tab 时改用手动 `TabController`
- `isScrollable: true` 让标签水平滚动(标签多时必需),否则标签会被压缩
- `TabBarView` 的 `children` 应保持轻量,重页面建议用 `AutomaticKeepAliveClientMixin` 保活
