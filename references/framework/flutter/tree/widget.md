# Flutter Tree Widget 定义

> **本框架无原生 Tree Widget。**

## 占位说明

Flutter Material Design 3 **未提供原生 Tree(树形组件)Widget**。其他框架(Ant Design / Element Plus)中的树形控件,在 Flutter 中通过以下方式实现:

| 其他框架的 Tree 场景 | Flutter 对应实现 |
| --- | --- |
| 可折叠分组列表 | `ExpansionTile` + `ListView`(简单二级展开) |
| 嵌套展开列表 | `ExpansionPanelList`(多面板展开) |
| 复杂树形(无限层级) | 第三方 `treeview` 包 |
| 文件目录树 | 第三方 `flutter_simple_treeview` 或自定义 |
| 数据可视化树 | `CustomPaint` + 自定义绘制 |

## 推荐替代方案

### 1. 简单二级展开 → ExpansionTile

```dart
ListView(
  children: [
    ExpansionTile(
      title: const Text('分组 1'),
      children: const [
        ListTile(title: Text('子项 1')),
        ListTile(title: Text('子项 2')),
      ],
    ),
    ExpansionTile(
      title: const Text('分组 2'),
      children: const [
        ListTile(title: Text('子项 3')),
      ],
    ),
  ],
)
```

### 2. 多面板展开 → ExpansionPanelList

```dart
ExpansionPanelList.radio(
  children: [
    ExpansionPanelRadio(
      headerBuilder: (_, __) => const Text('面板 1'),
      body: const ListTile(title: Text('内容 1')),
      value: 'panel1',
    ),
  ],
)
```

### 3. 无限层级树 → 第三方包

- `flutter_simple_treeview`(https://pub.flutter-io.cn/packages/flutter_simple_treeview)
- `treeview`](https://pub.flutter-io.cn/packages/treeview)

```dart
import 'package:flutter_simple_treeview/flutter_simple_treeview.dart';

Tree(
  nodes: [
    TreeNode(
      content: const Text('根节点'),
      children: [
        TreeNode(content: const Text('子节点 1')),
        TreeNode(
          content: const Text('子节点 2'),
          children: [
            TreeNode(content: const Text('孙节点')),
          ],
        ),
      ],
    ),
  ],
)
```

### 4. 自定义递归树

```dart
class TreeNode extends StatelessWidget {
  const TreeNode({
    super.key,
    required this.title,
    this.children = const [],
    this.level = 0,
  });

  final String title;
  final List<TreeNode> children;
  final int level;

  @override
  Widget build(BuildContext context) {
    return ExpansionTile(
      tilePadding: EdgeInsets.only(left: {spacing-md} * level),
      title: Text(title),
      children: children
          .map((child) => TreeNode(
                title: child.title,
                children: child.children,
                level: level + 1,
              ))
          .toList(),
    );
  }
}
```

> 注:递归构建树时需注意深度,过深的层级会导致 widget 树过深影响性能。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - ExpansionTile: https://api.flutter.dev/flutter/material/ExpansionTile-class.html
- API 参考 - ExpansionPanelList: https://api.flutter.dev/flutter/material/ExpansionPanelList-class.html
- pub.dev - flutter_simple_treeview: https://pub.flutter-io.cn/packages/flutter_simple_treeview
- pub.dev - treeview: https://pub.flutter-io.cn/packages/treeview
