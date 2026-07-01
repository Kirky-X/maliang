# Flutter ListView Widget 定义

## Widget 定义

`ListView` 是 Flutter 提供的可滚动列表 Widget,继承自 `BoxScrollView`(→ `ScrollView` → `StatelessWidget`)。它通过 `build()` 方法将一组子节点沿主轴(默认垂直)线性排列,超出视口部分按需懒加载。

Material Design 3 中,列表项推荐使用 `ListTile`,其颜色 / 内边距 / 排版由主题 token 驱动。

### 相关类与构造变体

| 类 / 构造 | 基类 | 用途 |
| --- | --- | --- |
| `ListView` | `BoxScrollView` | 静态/少量子节点列表 |
| `ListView.builder` | `ListView` | 大量子节点,按索引懒构建(推荐) |
| `ListView.separated` | `ListView` | 带分隔器的构建式列表 |
| `ListView.custom` | `ListView` | 自定义 `SliverChildDelegate` |
| `ListTile` | `StatelessWidget` | 标准列表项(leading/title/trailing) |
| `ScrollController` | `ChangeNotifier` | 控制并监听滚动位置 |

## 构造函数

### ListView(默认)

```dart
ListView({
  super.key,
  super.scrollDirection = Axis.vertical,  // 滚动方向
  super.reverse = false,                  // 是否反向
  super.controller,                       // ScrollController?
  super.primary,                          // 是否与父级 PrimaryScrollController 关联
  super.physics,                          // ScrollPhysics?(滚动行为)
  super.shrinkWrap = false,               // 是否按内容收缩高度
  super.padding,                          // EdgeInsetsGeometry?
  this.itemExtent,                        // double?(固定项高度,优化性能)
  this.prototypeItem,                     // Widget?(以该项高度为基准优化)
  bool addAutomaticKeepAlives = true,     // 自动 KeepAlive
  bool addRepaintBoundaries = true,       // 自动 RepaintBoundary
  bool addSemanticIndexes = true,         // 自动语义索引
  super.cacheExtent,                      // double?(预渲染范围)
  super.children,                         // List<Widget> 静态子节点
  super.dragStartBehavior,
  super.keyboardDismissBehavior,
  super.restorationId,
  super.clipBehavior = Clip.hardEdge,
})
```

### ListView.builder(懒加载,推荐)

```dart
ListView.builder({
  super.key,
  super.scrollDirection,
  super.reverse,
  super.controller,
  super.primary,
  super.physics,
  super.shrinkWrap,
  super.padding,
  this.itemExtent,            // 固定高度,性能最佳
  this.prototypeItem,
  required IndexedWidgetBuilder itemBuilder,  // 必填:按索引构建
  ChildIndexGetter? findChildIndexCallback,
  int? itemCount,             // 子项数量
  bool addAutomaticKeepAlives = true,
  bool addRepaintBoundaries = true,
  bool addSemanticIndexes = true,
  super.cacheExtent,
  super.dragStartBehavior,
  super.keyboardDismissBehavior,
  super.restorationId,
  super.clipBehavior,
})
```

### ListView.separated(带分隔器)

```dart
ListView.separated({
  super.key,
  super.scrollDirection,
  super.reverse,
  super.controller,
  super.primary,
  super.physics,
  super.shrinkWrap,
  super.padding,
  required IndexedWidgetBuilder itemBuilder,   // 必填
  required IndexedWidgetBuilder separatorBuilder, // 必填:分隔项构建
  int? itemCount,
  bool addAutomaticKeepAlives = true,
  bool addRepaintBoundaries = true,
  bool addSemanticIndexes = true,
  super.cacheExtent,
  super.dragStartBehavior,
  super.keyboardDismissBehavior,
  super.restorationId,
  super.clipBehavior,
})
```

### ListTile

```dart
const ListTile({
  super.key,
  this.leading,            // Widget? 前置(图标/头像)
  this.title,              // Widget? 标题
  this.subtitle,           // Widget? 副标题
  this.trailing,           // Widget? 后置(箭头/开关)
  this.isThreeLine = false,// 是否三行布局
  this.dense,              // bool? 紧凑
  this.visualDensity,      // VisualDensity?
  this.shape,              // ShapeBorder?
  this.style,              // ListTileStyle?
  this.selectedColor,      // Color?
  this.iconColor,          // Color?
  this.textColor,          // Color?
  this.titleTextStyle,     // TextStyle?
  this.subtitleTextStyle,  // TextStyle?
  this.leadingAndTrailingTextStyle,
  this.contentPadding,     // EdgeInsetsGeometry?
  this.enabled = true,     // 是否可交互
  this.onTap,              // VoidCallback?
  this.onLongPress,        // VoidCallback?
  this.onFocusChange,      // ValueChanged<bool>?
  this.mouseCursor,        // MouseCursor?
  this.selected = false,   // 是否选中
  this.focusColor,         // Color?
  this.hoverColor,         // Color?
  this.splashColor,        // Color?
  this.focusNode,          // FocusNode?
  this.autofocus = false,
  this.tileColor,          // Color? 背景
  this.selectedTileColor,  // Color? 选中背景
  this.enableFeedback = true,
  this.horizontalTitleGap, // double?
  this.minVerticalPadding, // double?
  this.minLeadingWidth,    // double?
  this.titleAlignment,     // ListTileTitleAlignment?
})
```

## 核心属性(ListView)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `scrollDirection` | `Axis` | 滚动方向,默认 `Axis.vertical` |
| `reverse` | `bool` | 是否反向排列,默认 `false` |
| `controller` | `ScrollController?` | 滚动控制器,监听/跳转位置 |
| `primary` | `bool?` | 是否关联 `PrimaryScrollController` |
| `physics` | `ScrollPhysics?` | 滚动行为(`Bouncing`/`Clamping`/`AlwaysScrollable`) |
| `shrinkWrap` | `bool` | 是否按内容收缩,默认 `false` |
| `padding` | `EdgeInsetsGeometry?` | 内边距 |
| `itemExtent` | `double?` | 固定项高度(性能优化) |
| `cacheExtent` | `double?` | 视口外预渲染高度 |
| `itemBuilder` | `IndexedWidgetBuilder` | 按索引构建项(`.builder`/`.separated`) |
| `itemCount` | `int?` | 项总数 |
| `children` | `List<Widget>` | 静态子节点(默认构造) |
| `addAutomaticKeepAlives` | `bool` | 自动保持状态,默认 `true` |
| `addRepaintBoundaries` | `bool` | 自动隔离重绘,默认 `true` |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// ListView 最小示例:静态列表、builder、separated 三种用法
class ListViewSample extends StatelessWidget {
  const ListViewSample({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('ListView 示例'),
          bottom: const TabBar(tabs: [
            Tab(text: '静态'),
            Tab(text: 'builder'),
            Tab(text: 'separated'),
          ]),
        ),
        body: TabBarView(
          children: [
            // 1. 静态 ListView + ListTile
            ListView(
              padding: const EdgeInsets.all({spacing-sm}),
              children: const [
                ListTile(leading: Icon(Icons.inbox), title: Text('收件箱')),
                ListTile(leading: Icon(Icons.send), title: Text('已发送')),
                ListTile(leading: Icon(Icons.drafts), title: Text('草稿')),
              ],
            ),

            // 2. ListView.builder:按需构建
            ListView.builder(
              itemCount: 50,
              itemExtent: 56,   // 固定高度,优化性能
              itemBuilder: (context, index) => ListTile(
                leading: const Icon(Icons.label),
                title: Text('项 $index'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => debugPrint('点击项 $index'),
              ),
            ),

            // 3. ListView.separated:带分隔线
            ListView.separated(
              itemCount: 20,
              separatorBuilder: (context, index) => Divider(
                height: 1,
                color: {color-outline-variant},
              ),
              itemBuilder: (context, index) => ListTile(
                title: Text('分隔列表项 $index'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 性能要点

- 大数据量优先用 `ListView.builder` + `itemExtent`(固定高度),避免一次性构建全部子节点。
- `shrinkWrap: true` 会破坏懒加载,仅在列表嵌套且需按内容计算高度时使用,并搭配 `physics: NeverScrollableScrollPhysics()`。
- 通过 `ScrollController` 监听位置实现下拉刷新 / 上拉加载。

详见 `properties.md`。
