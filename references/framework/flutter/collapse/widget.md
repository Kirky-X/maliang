# Flutter Collapse Widget 定义

## Widget 定义

Flutter Material Design 3 提供"折叠面板"系列 Widget,涵盖单级展开(`ExpansionTile`)、多面板手风琴(`ExpansionPanelList`)、卡片折叠(`ExpansionPanel`)等场景。

| Collapse 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| ExpansionTile | `ExpansionTile` | `StatefulWidget` | ListView 内单级展开(常用) |
| ExpansionPanelList | `ExpansionPanelList` | `StatefulWidget` | 多面板手风琴(配合 `ExpansionPanel`) |
| ExpansionPanel | `ExpansionPanel` | - | 单个折叠面板(用于 ExpansionPanelList) |
| ExpansionPanelList.radio | `ExpansionPanelList.radio` 工厂 | - | 单选式手风琴(同时只能展开一个) |

> `ExpansionTile` 用于 ListView,`ExpansionPanelList` 用于独立区域。两者内部都通过 `AnimationController` + `SizeTransition` / `CrossFade` 实现展开动画。

## 构造函数

### ExpansionTile

```dart
const ExpansionTile({
  super.key,
  this.leading,                        // 头部 Widget
  required this.title,                 // 标题
  this.subtitle,                       // 副标题
  this.onExpansionChanged,             // 展开/折叠回调
  this.children = const [],            // 子节点(展开时显示)
  this.initiallyExpanded = false,      // 初始是否展开
  this.maintainState = false,          // 折叠时是否保持子项状态
  this.tilePadding,                    // 标题内边距
  this.expandedCrossAxisAlignment,     // 展开后子项交叉轴对齐
  this.expandedAlignment,              // 展开后子项主轴对齐
  this.childrenPadding,                // 子项区域内边距
  this.backgroundColor,                // 展开时背景色
  this.collapsedBackgroundColor,       // 折叠时背景色
  this.textColor,                      // 展开时文字色
  this.collapsedTextColor,             // 折叠时文字色
  this.iconColor,                      // 展开时图标色
  this.collapsedIconColor,             // 折叠时图标色
  this.shape,                          // 展开时形状
  this.collapsedShape,                 // 折叠时形状
  this.clipBehavior,                   // 裁剪行为
  this.controlAffinity = ListTileControlAffinity.platform,  // 展开图标位置
  this.dense,                          // 紧凑模式
})
```

### ExpansionPanelList

```dart
const ExpansionPanelList({
  super.key,
  this.children = const [],            // 面板列表
  this.expansionCallback,              // 展开/折叠回调
  this.animationDuration = kThemeExpandDuration,  // 动画时长
  this.elevation,                      // 面板高度
  this.expandHeaderPadding,            // 头部内边距
  this.dividerColor,                   // 分隔线颜色
  this.materialGapSize,                // 面板间距(M3 新增)
})
```

### ExpansionPanelList.radio(单选式)

```dart
const ExpansionPanelList.radio({
  super.key,
  this.children = const [],            // List<ExpansionPanelRadio>
  this.expansionCallback,
  this.animationDuration = kThemeExpandDuration,
  this.elevation,
  this.expandHeaderPadding,
  this.dividerColor,
  this.materialGapSize,
})
```

## 核心属性(ExpansionTile)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `title` | `Widget` | 标题 |
| `subtitle` | `Widget?` | 副标题 |
| `leading` | `Widget?` | 头部 Widget |
| `children` | `List<Widget>` | 子节点 |
| `initiallyExpanded` | `bool` | 初始是否展开 |
| `onExpansionChanged` | `ValueChanged<bool>?` | 展开/折叠回调 |
| `backgroundColor` | `Color?` | 展开时背景 |
| `collapsedBackgroundColor` | `Color?` | 折叠时背景 |
| `textColor` | `Color?` | 展开时文字色 |
| `collapsedTextColor` | `Color?` | 折叠时文字色 |
| `iconColor` | `Color?` | 展开时图标色 |
| `collapsedIconColor` | `Color?` | 折叠时图标色 |
| `shape` | `ShapeBorder?` | 展开时形状 |
| `collapsedShape` | `ShapeBorder?` | 折叠时形状 |
| `controlAffinity` | `ListTileControlAffinity` | 展开图标位置 |
| `maintainState` | `bool` | 折叠时是否保持子项状态 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Collapse 最小示例:展示 ExpansionTile 与 ExpansionPanelList
class CollapseSample extends StatelessWidget {
  const CollapseSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Collapse 示例')),
      body: ListView(
        children: [
          // 1. ExpansionTile(单级展开)
          ExpansionTile(
            title: const Text('分组 1'),
            leading: const Icon(Icons.folder),
            children: const [
              ListTile(title: Text('子项 1')),
              ListTile(title: Text('子项 2')),
            ],
          ),
          // 2. 带副标题与初始展开
          ExpansionTile(
            title: const Text('分组 2'),
            subtitle: const Text('2 项'),
            initiallyExpanded: true,
            children: const [
              ListTile(title: Text('子项 3')),
            ],
          ),
        ],
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
ExpansionTile(
  title: Text(
    '自定义面板',
    style: TextStyle(
      fontSize: {font-size-md},
      fontWeight: FontWeight.w600,
      color: {color-text-primary},
    ),
  ),
  subtitle: Text(
    '3 项',
    style: TextStyle(fontSize: {font-size-sm}, color: {color-text-secondary}),
  ),
  leading: Icon(Icons.expand_more, size: {icon-size-sm}, color: {color-primary}),
  backgroundColor: {color-surface-variant},
  collapsedBackgroundColor: {color-surface},
  textColor: {color-primary},
  collapsedTextColor: {color-text-primary},
  iconColor: {color-primary},
  collapsedIconColor: {color-text-tertiary},
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular({radius-md}),
    side: BorderSide(color: {color-outline-variant}),
  ),
  collapsedShape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular({radius-md}),
  ),
  tilePadding: EdgeInsets.symmetric(horizontal: {spacing-md}),
  childrenPadding: EdgeInsets.symmetric(horizontal: {spacing-md}),
  children: const [
    ListTile(title: Text('子项 1')),
    ListTile(title: Text('子项 2')),
  ],
)
```

> 注:示例中的 `{color-surface}`、`{color-surface-variant}`、`{color-primary}`、`{color-text-primary}`、`{color-text-secondary}`、`{color-text-tertiary}`、`{color-outline-variant}`、`{spacing-md}`、`{font-size-md}`、`{font-size-sm}`、`{icon-size-sm}`、`{radius-md}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - ExpansionTile: https://api.flutter.dev/flutter/material/ExpansionTile-class.html
- API 参考 - ExpansionPanelList: https://api.flutter.dev/flutter/material/ExpansionPanelList-class.html
- API 参考 - ExpansionPanel: https://api.flutter.dev/flutter/material/ExpansionPanel-class.html
- API 参考 - ExpansionPanelRadio: https://api.flutter.dev/flutter/material/ExpansionPanelRadio-class.html
