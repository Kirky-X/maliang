# Flutter Alert 属性列表与默认值

> 分工:AlertDialog 参数唯一真源在本文件(默认值更全);showDialog / SimpleDialog / SimpleDialogOption / Dialog.fullscreen 的对话框体系参数真源见 [dialog](../dialog/properties.md),本文件不复述(防双份漂移)。

本文档汇总 Material Design 3 警示框(`AlertDialog` / `SimpleDialog` / `showDialog`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## AlertDialog 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `icon` | `Widget?` | `null` | 顶部图标 |
| `iconColor` | `Color?` | `{color-secondary}` | 图标颜色 |
| `iconPadding` | `EdgeInsetsGeometry` | `EdgeInsets.fromLTRB(24, 24, 24, 0)` | 图标内边距 |
| `title` | `Widget?` | `null` | 标题 |
| `titlePadding` | `EdgeInsetsGeometry` | `EdgeInsets.fromLTRB(24, 16, 24, 0)` | 标题内边距 |
| `titleTextStyle` | `TextStyle?` | `{font-size-lg}` / `{color-on-surface}` | 标题样式 |
| `content` | `Widget?` | `null` | 内容 |
| `contentPadding` | `EdgeInsetsGeometry` | `EdgeInsets.fromLTRB(24, 16, 24, 0)` | 内容内边距 |
| `contentTextStyle` | `TextStyle?` | `{font-size-md}` / `{color-on-surface-variant}` | 内容样式 |
| `actions` | `List<Widget>?` | `null` | 操作按钮列表 |
| `actionsPadding` | `EdgeInsetsGeometry` | `EdgeInsets.fromLTRB(24, 24, 24, 24)` | 操作区内边距 |
| `actionsAlignment` | `MainAxisAlignment?` | `MainAxisAlignment.end` | 操作按钮对齐 |
| `actionsOverflowDirection` | `VerticalDirection` | `VerticalDirection.up` | 操作溢出方向 |
| `actionsOverflowButtonSpacing` | `double?` | `null` | 操作溢出按钮间距(官方参数名核对) |
| `buttonPadding` | `EdgeInsetsGeometry` | `EdgeInsets.all(8)` | 按钮内边距 |
| `backgroundColor` | `Color?` | `{color-surface}` | 背景色 |
| `elevation` | `double?` | `6.0` | 高度 |
| `shadowColor` | `Color?` | `{color-shadow}` | 阴影色 |
| `surfaceTintColor` | `Color?` | `{color-surface-variant}` | M3 表面染色 |
| `insetPadding` | `EdgeInsets` | `EdgeInsets.symmetric(horizontal: 40, vertical: 24)` | 外边距 |
| `clipBehavior` | `Clip` | `Clip.none` | 裁剪行为 |
| `shape` | `ShapeBorder?` | `RoundedRectangleBorder(borderRadius: 28)` | 形状 |
| `alignment` | `AlignmentGeometry?` | `Alignment.center` | 对齐位置 |
| `scrollable` | `bool` | `false` | 是否可滚动 |

## Dialog.fullscreen 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget` | 必填 | 内容 |
| `backgroundColor` | `Color?` | `{color-surface}` | 背景色 |
| `elevation` | `double?` | `0` | 高度(全屏无阴影) |
| `insetAnimationDuration` | `Duration` | `Duration(milliseconds: 100)` | 入场动画时长 |
| `insetAnimationCurve` | `Curve` | `Curves.decelerate` | 入场动画曲线 |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Alert 完整示例:展示标准警示框、错误警示、确认对话框
class AlertFullSample extends StatelessWidget {
  const AlertFullSample({super.key});

  Future<void> _showConfirm(BuildContext context) async {
    final result = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        icon: Icon(Icons.help_outline, color: {color-primary}, size: {icon-size-md}),
        title: const Text('确认删除'),
        content: const Text('删除后将无法恢复,确定继续吗?'),
        actionsAlignment: MainAxisAlignment.end,
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('取消'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(
              backgroundColor: {color-error},
              foregroundColor: {color-on-error},
            ),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('删除'),
          ),
        ],
      ),
    );
    if (result == true) {
      debugPrint('用户确认删除');
    }
  }

  Future<void> _showError(BuildContext context) async {
    await showDialog<void>(
      context: context,
      builder: (context) => AlertDialog(
        icon: Icon(Icons.error, color: {color-error}, size: {icon-size-md}),
        title: Text(
          '操作失败',
          style: TextStyle(
            fontSize: {font-size-lg},
            color: {color-text-primary},
          ),
        ),
        content: Text(
          '网络异常,请稍后重试',
          style: TextStyle(
            fontSize: {font-size-md},
            color: {color-text-secondary},
          ),
        ),
        backgroundColor: {color-surface},
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular({radius-lg}),
        ),
        actions: [
          FilledButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('知道了'),
          ),
        ],
      ),
    );
  }

  Future<void> _showOptions(BuildContext context) async {
    final result = await showDialog<String>(
      context: context,
      builder: (context) => SimpleDialog(
        title: const Text('选择操作'),
        children: [
          SimpleDialogOption(
            onPressed: () => Navigator.pop(context, 'edit'),
            child: const Text('编辑'),
          ),
          SimpleDialogOption(
            onPressed: () => Navigator.pop(context, 'share'),
            child: const Text('分享'),
          ),
          SimpleDialogOption(
            onPressed: () => Navigator.pop(context, 'delete'),
            child: const Text('删除'),
          ),
        ],
      ),
    );
    debugPrint('用户选择: $result');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Alert 完整示例')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            FilledButton(
              onPressed: () => _showConfirm(context),
              child: const Text('确认对话框'),
            ),
            const SizedBox(height: {spacing-sm}),
            FilledButton(
              onPressed: () => _showError(context),
              child: const Text('错误警示'),
            ),
            const SizedBox(height: {spacing-sm}),
            FilledButton(
              onPressed: () => _showOptions(context),
              child: const Text('选项对话框'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

在 `ThemeData` 中通过 `dialogTheme` 注入主题级样式:

```dart
ThemeData(
  dialogTheme: DialogTheme(
    backgroundColor: {color-surface},
    surfaceTintColor: {color-surface-variant},
    elevation: {elevation-md},
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-lg}),
    ),
    titleTextStyle: TextStyle(
      fontSize: {font-size-lg},
      color: {color-text-primary},
    ),
    contentTextStyle: TextStyle(
      fontSize: {font-size-md},
      color: {color-text-secondary},
    ),
  ),
)
```

