# Flutter ListView 属性列表与默认值

本文档列出 `ListView`(及其构建变体)与 `ListTile` 的完整属性、默认值与滚动回调。涉及颜色/间距的默认值以 design token 形式给出,不在文档中硬编码。

## ListView 通用属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `scrollDirection` | `Axis` | `Axis.vertical` | 滚动方向 |
| `reverse` | `bool` | `false` | 是否反向排列 |
| `controller` | `ScrollController?` | `null`(使用 `PrimaryScrollController`) | 滚动控制器 |
| `primary` | `bool?` | `null`(当 `controller` 为空时默认 `true`) | 是否使用主控制器 |
| `physics` | `ScrollPhysics?` | 平台默认(iOS `BouncingScrollPhysics`,其他 `ClampingScrollPhysics`) | 滚动行为 |
| `shrinkWrap` | `bool` | `false` | 是否按内容收缩高度 |
| `padding` | `EdgeInsetsGeometry?` | `null` | 内边距 |
| `itemExtent` | `double?` | `null` | 固定项高度(性能优化) |
| `prototypeItem` | `Widget?` | `null` | 以该项为高度基准 |
| `cacheExtent` | `double?` | `250.0`(逻辑像素) | 视口外预渲染范围 |
| `addAutomaticKeepAlives` | `bool` | `true` | 自动 `KeepAlive` |
| `addRepaintBoundaries` | `bool` | `true` | 自动 `RepaintBoundary` |
| `addSemanticIndexes` | `bool` | `true` | 自动语义索引 |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 裁剪行为 |
| `keyboardDismissBehavior` | `ScrollViewKeyboardDismissBehavior` | `manual` | 拖动时收起键盘 |
| `dragStartBehavior` | `DragStartBehavior` | `DragStartBehavior.start` | 拖动开始时机 |
| `restorationId` | `String?` | `null` | 状态恢复标识 |

### 构造变体差异

| 构造 | 特有参数 | 适用场景 |
| --- | --- | --- |
| `ListView` | `children: List<Widget>` | 少量静态子节点 |
| `ListView.builder` | `itemBuilder`、`itemCount`、`findChildIndexCallback` | 大数据量懒构建 |
| `ListView.separated` | `itemBuilder`、`separatorBuilder`、`itemCount` | 带分隔项 |
| `ListView.custom` | `childrenDelegate: SliverChildDelegate` | 完全自定义委托 |

## ListTile 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `leading` | `Widget?` | `null` | 前置(图标/头像) |
| `title` | `Widget?` | `null` | 标题 |
| `subtitle` | `Widget?` | `null` | 副标题 |
| `trailing` | `Widget?` | `null` | 后置(箭头/开关) |
| `isThreeLine` | `bool` | `false` | 是否三行布局 |
| `dense` | `bool?` | `null`(取主题) | 紧凑模式 |
| `visualDensity` | `VisualDensity?` | `null`(取主题) | 视觉密度 |
| `shape` | `ShapeBorder?` | `null` | 形状(影响墨水涟漪) |
| `style` | `ListTileStyle?` | `null`(取主题) | 文本样式来源(list/drawer) |
| `selectedColor` | `Color?` | `null` | 选中态颜色 |
| `iconColor` | `Color?` | `null` | 图标颜色 |
| `textColor` | `Color?` | `null` | 文本颜色 |
| `titleTextStyle` | `TextStyle?` | `null` | 标题样式(覆盖) |
| `subtitleTextStyle` | `TextStyle?` | `null` | 副标题样式 |
| `leadingAndTrailingTextStyle` | `TextStyle?` | `null` | 前后置文本样式 |
| `contentPadding` | `EdgeInsetsGeometry?` | 左右 `{spacing-md}`,上下 `{spacing-xs}` | 内边距 |
| `enabled` | `bool` | `true` | 是否可交互 |
| `selected` | `bool` | `false` | 是否选中 |
| `tileColor` | `Color?` | `null` | 背景色 |
| `selectedTileColor` | `Color?` | `null` | 选中背景色 |
| `focusColor` | `Color?` | `null` | 焦点色 |
| `hoverColor` | `Color?` | `null` | 悬停色 |
| `splashColor` | `Color?` | `null` | 涟漪色 |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |
| `mouseCursor` | `MouseCursor?` | `null` | 鼠标光标 |
| `enableFeedback` | `bool` | `true` | 触觉反馈 |
| `horizontalTitleGap` | `double?` | `16` | 标题与前后置水平间距 |
| `minVerticalPadding` | `double?` | `4` | 上下最小内边距 |
| `minLeadingWidth` | `double?` | `40` | leading 最小宽度 |
| `titleAlignment` | `ListTileTitleAlignment?` | `null`(取主题) | 标题对齐 |

## ScrollPhysics 常用值

| 值 | 行为 |
| --- | --- |
| `AlwaysScrollableScrollPhysics` | 始终可滚动(用于下拉刷新) |
| `NeverScrollableScrollPhysics` | 禁止滚动(嵌套场景) |
| `BouncingScrollPhysics` | iOS 风格,边界回弹 |
| `ClampingScrollPhysics` | Android 风格,边界钳制 |
| `FixedExtentScrollPhysics` | 配合 `FixedExtentScrollController`,吸附式 |

## 事件回调与滚动监听

ListView 本身不暴露点击/滚动回调,需通过 `ScrollController` + `NotificationListener` 实现。

### ScrollController

| API | 说明 |
| --- | --- |
| `controller.addListener(callback)` | 位置变化通知 |
| `controller.position.pixels` | 当前滚动偏移 |
| `controller.position.maxScrollExtent` | 最大可滚动偏移 |
| `controller.jumpTo(double)` | 跳转(无动画) |
| `controller.animateTo(double, ...)` | 动画跳转 |
| `controller.dispose()` | 释放资源 |

### NotificationListener(无需 controller)

| 回调 | 签名 | 说明 |
| --- | --- | --- |
| `onScroll` | `bool Function(ScrollNotification)` | 任意滚动通知(start/update/end/overscroll) |
| `onScrollStartNotification` | `bool Function(ScrollStartNotification)` | 滚动开始 |
| `onScrollUpdateNotification` | `bool Function(ScrollUpdateNotification)` | 滚动中 |
| `onScrollEndNotification` | `bool Function(ScrollEndNotification)` | 滚动结束 |
| `onOverscrollNotification` | `bool Function(OverscrollNotification)` | 越界 |

### ListTile 交互回调

| 回调 | 签名 | 说明 |
| --- | --- | --- |
| `onTap` | `void Function()` | 点击项 |
| `onLongPress` | `void Function()` | 长按项 |
| `onFocusChange` | `void Function(bool)` | 焦点变化 |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// ListView 完整示例:
/// - ListView.builder + ListTile
/// - ScrollController 实现上拉加载更多
/// - NotificationListener 实现滚动监听
/// - 下拉刷新 RefreshIndicator
/// - 自定义样式(token 引用)
class ListViewFullSample extends StatefulWidget {
  const ListViewFullSample({super.key});

  @override
  State<ListViewFullSample> createState() => _ListViewFullSampleState();
}

class _ListViewFullSampleState extends State<ListViewFullSample> {
  final ScrollController _controller = ScrollController();
  final List<String> _items = List.generate(20, (i) => '项 ${i + 1}');
  bool _isLoadingMore = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(_onScroll);
  }

  @override
  void dispose() {
    _controller.removeListener(_onScroll);
    _controller.dispose();
    super.dispose();
  }

  void _onScroll() {
    // 滚动到底部 100px 内触发加载
    if (_controller.position.pixels >=
            _controller.position.maxScrollExtent - 100 &&
        !_isLoadingMore) {
      _loadMore();
    }
  }

  Future<void> _loadMore() async {
    setState(() => _isLoadingMore = true);
    // 模拟网络请求
    await Future.delayed(const Duration(seconds: 1));
    final next = _items.length;
    setState(() {
      _items.addAll(List.generate(10, (i) => '项 ${next + i + 1}'));
      _isLoadingMore = false;
    });
  }

  Future<void> _onRefresh() async {
    // 下拉刷新
    await Future.delayed(const Duration(seconds: 1));
    setState(() {
      _items
        ..clear()
        ..addAll(List.generate(20, (i) => '项 ${i + 1}'));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ListView 完整示例')),
      body: NotificationListener<ScrollNotification>(
        onNotification: (notification) {
          // 滚动事件统一监听
          if (notification is ScrollStartNotification) {
            debugPrint('滚动开始');
          } else if (notification is ScrollEndNotification) {
            debugPrint('滚动结束,偏移=${_controller.position.pixels}');
          }
          return false;
        },
        child: RefreshIndicator(
          onRefresh: _onRefresh,
          color: {color-primary},
          child: ListView.builder(
            controller: _controller,
            padding: const EdgeInsets.symmetric(
              vertical: {spacing-sm},
            ),
            itemExtent: 72,
            itemCount: _items.length + 1, // 末尾加载指示器
            itemBuilder: (context, index) {
              // 最后一项:加载指示器
              if (index == _items.length) {
                return Padding(
                  padding: const EdgeInsets.all({spacing-md}),
                  child: Center(
                    child: _isLoadingMore
                        ? const CircularProgressIndicator()
                        : const Text('没有更多了'),
                  ),
                );
              }

              final item = _items[index];
              return ListTile(
                leading: CircleAvatar(
                  backgroundColor: {color-secondary-container},
                  child: Text(
                    '${index + 1}',
                    style: TextStyle(color: {color-on-secondary-container}),
                  ),
                ),
                title: Text(
                  item,
                  style: TextStyle(
                    fontSize: {font-size-md},
                    color: {color-on-surface},
                  ),
                ),
                subtitle: const Text('副标题描述'),
                trailing: const Icon(Icons.chevron_right),
                tileColor: {color-surface},
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: {spacing-md},
                  vertical: {spacing-xs},
                ),
                onTap: () => debugPrint('点击 $item'),
                onLongPress: () => debugPrint('长按 $item'),
              );
            },
          ),
        ),
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

在 `ThemeData` 中通过 `listTileTheme` 集中注入 token:

```dart
ThemeData(
  listTileTheme: const ListTileThemeData(
    tileColor: {color-surface},
    selectedTileColor: {color-secondary-container},
    iconColor: {color-on-surface-variant},
    textColor: {color-on-surface},
    contentPadding: EdgeInsets.symmetric(
      horizontal: {spacing-md},
      vertical: {spacing-xs},
    ),
    style: ListTileStyle.list,
  ),
)
```
