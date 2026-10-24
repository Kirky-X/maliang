# Flutter Dialog Widget 定义

## Widget 定义

Flutter 对话框通过 `showDialog` 函数(返回 `Future<T?>`)在 `Overlay` 上展示模态对话框。`Dialog` 为基类,`AlertDialog`(Material 警告框)、`SimpleDialog`(简单选择列表)为常用子类。底部弹窗用 `showModalBottomSheet`。

| Widget/函数 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `showDialog` | 函数 | - | 显示模态对话框(返回 Future) |
| `AlertDialog` | `AlertDialog` | `Dialog` | Material 警告框(标题/内容/按钮) |
| `SimpleDialog` | `SimpleDialog` | `Dialog` | 简单选项列表对话框 |
| `Dialog` | `Dialog` | `StatelessWidget` | 通用对话框容器 |
| `showModalBottomSheet` | 函数 | - | 底部模态弹窗 |

## 构造函数

### showDialog

```dart
Future<T?> showDialog<T>({
  required BuildContext context,
  required WidgetBuilder builder,        // 对话框构建函数
  bool barrierDismissible = true,         // 点击遮罩是否关闭
  Color? barrierColor,                    // 遮罩颜色
  String? barrierLabel,
  bool useSafeArea = true,                // 是否避开系统 UI
  bool useRootNavigator = true,           // 是否用根 Navigator
  RouteSettings? routeSettings,
  Offset? anchorPoint,
  TraversalEdgeBehavior? traversalEdgeBehavior,
})
```

### AlertDialog

```dart
const AlertDialog({
  super.key,
  Widget? icon,                          // 顶部图标
  EdgeInsetsGeometry? iconPadding,
  Color? iconColor,
  Widget? title,                         // 标题
  EdgeInsetsGeometry? titlePadding,
  TextStyle? titleTextStyle,
  Widget? content,                       // 内容
  EdgeInsetsGeometry? contentPadding = const EdgeInsets.fromLTRB(24, 20, 24, 24),
  TextStyle? contentTextStyle,
  List<Widget>? actions,                 // 底部按钮(通常 TextButton)
  EdgeInsetsGeometry? actionsPadding,
  MainAxisAlignment? actionsAlignment,
  VerticalDirection? actionsOverflowDirection,
  double? actionsOverflowButtonSpacing,
  EdgeInsetsGeometry? buttonPadding,
  Color? backgroundColor,
  double? elevation,
  Color? shadowColor,
  Color? surfaceTintColor,
  ShapeBorder? shape,                    // 形状(圆角)
  String? semanticLabel,
  Clip clipBehavior = Clip.none,
  AlignmentGeometry? alignment,
})
```

### SimpleDialog

```dart
const SimpleDialog({
  super.key,
  Widget? title,
  EdgeInsetsGeometry? titlePadding,
  TextStyle? titleTextStyle,
  List<Widget>? children,               // 选项(SimpleDialogOption)
  EdgeInsetsGeometry? contentPadding,
  Color? backgroundColor,
  double? elevation,
  ShapeBorder? shape,
})
```

### SimpleDialogOption

```dart
const SimpleDialogOption({
  super.key,
  VoidCallback? onPressed,              // 选中回调
  Widget? child,
  EdgeInsets padding = const EdgeInsets.symmetric(vertical: 8, horizontal: 24),
})
```

> 属性与方法明细以 [properties.md](properties.md) 为唯一维护处；本文件只讲定义、构造与示例。

## 最小示例

```dart
import 'package:flutter/material.dart';

class DialogSample extends StatelessWidget {
  const DialogSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Dialog 示例')),
      body: Center(
        child: ElevatedButton(
          child: const Text('显示对话框'),
          onPressed: () async {
            final result = await showDialog<String>(
              context: context,
              builder: (_) => AlertDialog(
                title: const Text('确认删除'),
                content: const Text('此操作不可撤销,是否继续?'),
                actions: [
                  TextButton(
                    child: const Text('取消'),
                    onPressed: () => Navigator.pop(context, 'cancel'),
                  ),
                  FilledButton(
                    style: FilledButton.styleFrom(backgroundColor: {color-danger}),
                    child: const Text('删除'),
                    onPressed: () => Navigator.pop(context, 'delete'),
                  ),
                ],
              ),
            );
            debugPrint('结果: $result');
          },
        ),
      ),
    );
  }
}
```

## 参考链接

- Flutter 官方文档:无独立教程页(本 widget 在聚合页中介绍)
- Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - AlertDialog: https://api.flutter.dev/flutter/material/AlertDialog-class.html
- API 参考 - SimpleDialog: https://api.flutter.dev/flutter/material/SimpleDialog-class.html
- API 参考 - showDialog: https://api.flutter.dev/flutter/material/showDialog.html
- API 参考 - Dialog: https://api.flutter.dev/flutter/material/Dialog-class.html
