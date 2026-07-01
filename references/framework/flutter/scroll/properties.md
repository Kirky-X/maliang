# Flutter Scroll 属性列表与默认值

本文档汇总 Flutter 滚动体系的完整属性、默认值与回调。所有视觉属性以 design token 形式引用,不在文档中硬编码。

## ListView 完整属性

### ListView(直接子节点)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<Widget>` | `[]` | 子节点列表 |
| `itemExtent` | `double?` | `null` | 固定项高度(优化性能) |
| `prototypeItem` | `Widget?` | `null` | 原型项(用于测量项高度) |

### ListView.builder

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `itemBuilder` | `IndexedWidgetBuilder` | 必填 | 项构建器 |
| `itemCount` | `int?` | `null`(无限) | 项数 |
| `itemExtent` | `double?` | `null` | 固定项高度 |
| `findChildIndexCallback` | `ChildIndexFinder?` | `null` | Key 复用回溯 |

### ListView.separated

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `itemBuilder` | `IndexedWidgetBuilder` | 必填 | 项构建器 |
| `separatorBuilder` | `IndexedWidgetBuilder` | 必填 | 分隔符构建器 |
| `itemCount` | `int` | 必填 | 项数(不含分隔符) |

## ScrollView 通用属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `scrollDirection` | `Axis` | `Axis.vertical` | 滑动方向 |
| `reverse` | `bool` | `false` | 是否反向 |
| `controller` | `ScrollController?` | `null` | 控制器 |
| `primary` | `bool?` | `null`(取父级) | 是否使用 PrimaryScrollController |
| `physics` | `ScrollPhysics?` | `null` | 滑动物理效果 |
| `shrinkWrap` | `bool` | `false` | 按内容收缩 |
| `padding` | `EdgeInsetsGeometry?` | `null` | 内边距 |
| `cacheExtent` | `double?` | `null`(默认 250px) | 预渲染范围 |
| `dragStartBehavior` | `DragStartBehavior` | `DragStartBehavior.start` | 拖拽开始时机 |
| `keyboardDismissBehavior` | `ScrollViewKeyboardDismissBehavior` | `manual` | 键盘收起策略 |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 裁剪行为 |
| `restorationId` | `String?` | `null` | 状态恢复 ID |

## ScrollPhysics 子类

| 子类 | 平台 | 行为 |
| --- | --- | --- |
| `AlwaysScrollableScrollPhysics` | 通用 | 始终可滑动(配合 RefreshIndicator) |
| `NeverScrollableScrollPhysics` | 通用 | 禁用滑动(嵌套场景) |
| `BouncingScrollPhysics` | iOS 默认 | 边界回弹 |
| `ClampingScrollPhysics` | Android 默认 | 边界夹紧(无回弹) |
| `FixedExtentScrollPhysics` | 通用 | 整页吸附(PageView/固定高度) |
| `PageScrollPhysics` | PageView 默认 | 整页滑动 |
| `RangeMaintainingScrollPhysics` | 通用 | 维持范围(配合其他物理) |

## ScrollController 属性与方法

| 属性 / 方法 | 类型 | 说明 |
| --- | --- | --- |
| `initialScrollOffset` | `double` | 初始偏移(默认 `0.0`) |
| `keepScrollOffset` | `bool` | 是否保持位置(默认 `true`) |
| `debugLabel` | `String?` | 调试标签 |
| `offset` | `double` | 当前偏移(只读,未附加时抛异常) |
| `position` | `ScrollPosition` | 当前位置(可多个) |
| `positions` | `Iterable<ScrollPosition>` | 所有附加的位置 |
| `hasClients` | `bool` | 是否有附加客户端 |
| `jumpTo(double offset)` | `void` | 瞬间跳转 |
| `animateTo(offset, {duration, curve})` | `Future<void>` | 动画跳转 |
| `jumpToRelative(double offset)` | `void` | 相对跳转 |
| `animateToRelative(offset, {duration, curve})` | `Future<void>` | 相对动画跳转 |

## ScrollNotification 体系

监听 `NotificationListener<ScrollNotification>`:

| 子类 | 触发时机 |
| --- | --- |
| `ScrollStartNotification` | 滑动开始 |
| `ScrollUpdateNotification` | 滑动中(携带 `metrics`) |
| `ScrollEndNotification` | 滑动结束 |
| `UserScrollNotification` | 用户手动滑动(携带 `direction`) |
| `OverscrollNotification` | 越界滑动(回弹/夹紧) |
| `ScrollMetricsNotification` | metrics 变化(尺寸/范围) |

## ScrollMetrics 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `pixels` | `double` | 当前偏移(px) |
| `minScrollExtent` | `double` | 最小偏移(通常 `0`) |
| `maxScrollExtent` | `double` | 最大偏移(内容总长 - 视口) |
| `viewportDimension` | `double` | 视口尺寸 |
| `axisDirection` | `AxisDirection` | 滑动轴方向 |
| `extentBefore` | `double` | 视口前内容长度 |
| `extentInside` | `double` | 视口内可见长度 |
| `extentAfter` | `double` | 视口后内容长度 |
| `outOfRange` | `bool` | 是否越界 |
| `atEdge` | `bool` | 是否在边界 |
| `axis` | `Axis` | 滑动轴向 |

## Sliver 类型对比

| Sliver | 用途 | 等价 Widget |
| --- | --- | --- |
| `SliverList` | 动态列表 | ListView |
| `SliverFixedExtentList` | 固定高度列表 | ListView(itemExtent) |
| `SliverPrototypeExtentList` | 原型高度列表 | ListView(prototypeItem) |
| `SliverGrid` | 网格 | GridView |
| `SliverPadding` | 内边距 | Padding |
| `SliverPersistentHeader` | 吸顶/吸底头部 | - |
| `SliverAppBar` | 应用栏(可折叠) | AppBar |
| `SliverFillRemaining` | 填充剩余 | - |
| `SliverToBoxAdapter` | 单 Widget 包装 | - |
| `SliverAnimatedList` | 动画列表 | AnimatedList |

## SliverGridDelegate 子类

| 子类 | 关键参数 | 说明 |
| --- | --- | --- |
| `SliverGridDelegateWithFixedCrossAxisCount` | `crossAxisCount`, `childAspectRatio` | 固定列数 |
| `SliverGridDelegateWithMaxCrossAxisExtent` | `maxCrossAxisExtent`, `childAspectRatio` | 按最大列宽自适应 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class ScrollFullSample extends StatefulWidget {
  const ScrollFullSample({super.key});

  @override
  State<ScrollFullSample> createState() => _ScrollFullSampleState();
}

class _ScrollFullSampleState extends State<ScrollFullSample> {
  final ScrollController _controller = ScrollController();
  double _progress = 0.0;

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
    if (!_controller.hasClients) return;
    final metrics = _controller.position;
    final max = metrics.maxScrollExtent;
    setState(() {
      _progress = max > 0 ? metrics.pixels / max : 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scroll 完整示例'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(4),
          child: LinearProgressIndicator(
            value: _progress,
            color: {color-primary},
            backgroundColor: {color-bg-secondary},
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.vertical_align_top),
            onPressed: () {
              _controller.animateTo(
                0,
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeOut,
              );
            },
          ),
        ],
      ),
      body: NotificationListener<ScrollNotification>(
        onNotification: (notification) {
          if (notification is ScrollEndNotification &&
              notification.metrics.atEdge &&
              notification.metrics.pixels > 0) {
            // 到达底部,触发加载更多
            debugPrint('到达底部,加载更多');
          }
          return false;
        },
        child: CustomScrollView(
          controller: _controller,
          physics: const BouncingScrollPhysics(
            parent: AlwaysScrollableScrollPhysics(),
          ),
          slivers: [
            // 1. 可折叠头部
            SliverAppBar(
              expandedHeight: {size-xl},
              pinned: false,
              flexibleSpace: FlexibleSpaceBar(
                title: const Text('头部内容'),
                background: Container(color: {color-secondary-container}),
              ),
            ),
            // 2. 吸顶分类条
            SliverPersistentHeader(
              pinned: true,
              delegate: _CategoryHeaderDelegate(
                child: Container(
                  color: {color-surface},
                  padding: const EdgeInsets.all({spacing-sm}),
                  child: Text(
                    '分类: 全部',
                    style: TextStyle(
                      color: {color-text-primary},
                      fontSize: {font-size-md},
                    ),
                  ),
                ),
              ),
            ),
            // 3. 网格内容
            SliverPadding(
              padding: const EdgeInsets.all({spacing-sm}),
              sliver: SliverGrid(
                gridDelegate:
                    const SliverGridDelegateWithMaxCrossAxisExtent(
                  maxCrossAxisExtent: 150,
                  mainAxisSpacing: {spacing-sm},
                  crossAxisSpacing: {spacing-sm},
                  childAspectRatio: 0.8,
                ),
                delegate: SliverChildBuilderDelegate(
                  (context, index) => Container(
                    decoration: BoxDecoration(
                      color: {color-surface},
                      borderRadius: BorderRadius.circular({radius-md}),
                      border: Border.all(color: {color-border-default}),
                    ),
                    child: Center(child: Text('项 $index')),
                  ),
                  childCount: 100,
                ),
              ),
            ),
            // 4. 加载更多指示
            const SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.all({spacing-md}),
                child: Center(child: CircularProgressIndicator()),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CategoryHeaderDelegate extends SliverPersistentHeaderDelegate {
  _CategoryHeaderDelegate({required this.child});
  final Widget child;

  @override
  double get minExtent => 48;
  @override
  double get maxExtent => 48;
  @override
  Widget build(context, double shrinkOffset, bool overlaps) => child;
  @override
  bool shouldRebuild(_) => false;
}
```

## 注意事项

- `shrinkWrap: true` 会禁用视口懒加载,一次性构建所有子项;**仅用于内容确实很短的场景**,长列表务必保持 `false`。
- `primary: true` 会强制使用 `PrimaryScrollController`,在嵌套滚动(如 `Drawer`/`NestedScrollView`)中可能导致滑动错位。
- `physics` 未设置时取 `ScrollConfiguration` 默认值(iOS 回弹 / Android 夹紧);若要全平台统一,显式设置 `BouncingScrollPhysics` 或 `ClampingScrollPhysics`。
- `ScrollController` 不可多 `ListView` 共用,会抛 `Multiple scroll positions attached` 异常。
- `itemExtent` 与 `prototypeItem` 二选一,固定高度项必须设置以提升性能(避免测量开销)。
- `SliverPersistentHeader` 的 `minExtent` ≤ `maxExtent`,且 `pinned: true` 时 `minExtent` 决定吸顶高度。
- `ScrollNotification` 监听必须在 `NotificationListener` 包裹的滚动 Widget 上,且回调返回 `true` 会阻断事件冒泡。
- `BouncingScrollPhysics` 在 Android 上无"光晕"反馈,如需水波纹效果使用 `ClampingScrollPhysics` + Material 主题。
