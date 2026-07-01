# Flutter Message Widget 定义

## Widget 定义

Flutter 通过 `SnackBar` 实现"消息提示条"(其他框架常称 Toast / Notification),通常从屏幕底部短暂弹出。`SnackBar` 不是独立 Widget,需通过 `ScaffoldMessenger.showSnackBar` 触发。轻量提示(无操作)也可使用第三方 `fluttertoast` 包。

| Message 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| SnackBar(M3) | `SnackBar` | `StatefulWidget` | 底部消息条(可含操作按钮) |
| SnackBar 操作 | `SnackBarAction` | `StatelessWidget` | SnackBar 内嵌操作按钮 |
| 控制器 | `ScaffoldMessenger` | `StatefulWidget` | 管理 SnackBar 队列与显示 |
| 第三方 Toast | `Fluttertoast` | - | 跨平台原生 Toast(无操作) |
| Material Banner | `MaterialBanner` | `StatefulWidget` | 顶部持久消息条 |

> `SnackBar` 一次只显示一个,新 SnackBar 会关闭当前并显示自己;`MaterialBanner` 持续显示直到用户主动关闭。

## 构造函数

### SnackBar

```dart
const SnackBar({
  Key? key,
  required Widget content,
  SnackBarAction? action,
  double? width,
  double? elevation,
  Color? backgroundColor,
  Color? shadowColor,
  Color? surfaceTintColor,
  EdgeInsetsGeometry? margin,
  EdgeInsetsGeometry? padding,
  ShapeBorder? shape,
  SnackBarBehavior? behavior,
  Duration duration = _snackBarDisplayDuration,
  Animation<double>? animation,
  VoidCallback? onVisible,
  double? insetAnimationDuration,
  bool? showCloseIcon,
  Color? closeIconColor,
  DismissDirection? dismissDirection,
})
```

### SnackBarAction

```dart
const SnackBarAction({
  Key? key,
  required String label,
  required VoidCallback onPressed,
  Color? textColor,
  Color? disabledTextColor,
})
```

### ScaffoldMessenger.showSnackBar

```dart
ScaffoldMessenger.of(context).showSnackBar(SnackBar snackBar)
ScaffoldMessenger.of(context).hideCurrentSnackBar({SnackBarClosedReason reason})
ScaffoldMessenger.of(context).removeCurrentSnackBar({SnackBarClosedReason reason})
ScaffoldMessenger.of(context).clearSnackBars()
```

### MaterialBanner

```dart
const MaterialBanner({
  Key? key,
  required Widget content,
  required List<Widget> actions,
  Color? backgroundColor,
  double? elevation,
  EdgeInsetsGeometry? padding,
  EdgeInsetsGeometry? leadingPadding,
  Widget? leading,
  Color? shadowColor,
  Color? surfaceTintColor,
  TextStyle? contentTextStyle,
  double? forceActionsBelow,
  OverflowBarAlignment overflowAlignment = OverflowBarAlignment.end,
  bool forceOverflowBelow = false,
})
```

## 核心属性

### SnackBar

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `content` | `Widget` | 消息内容(通常为 `Text`) |
| `action` | `SnackBarAction?` | 操作按钮(如"撤销") |
| `duration` | `Duration` | 显示时长(默认 4 秒) |
| `behavior` | `SnackBarBehavior?` | 显示方式(fixed/floating) |
| `backgroundColor` | `Color?` | 背景色 |
| `elevation` | `double?` | 阴影高度(floating 时生效) |
| `margin` | `EdgeInsetsGeometry?` | 外边距(floating 时生效) |
| `padding` | `EdgeInsetsGeometry?` | 内边距 |
| `shape` | `ShapeBorder?` | 形状 |
| `width` | `double?` | 宽度(固定后 behavior 自动 floating) |
| `showCloseIcon` | `bool?` | 是否显示关闭图标 |
| `closeIconColor` | `Color?` | 关闭图标颜色 |
| `dismissDirection` | `DismissDirection?` | 滑动关闭方向 |
| `onVisible` | `VoidCallback?` | 显示时回调 |
| `animation` | `Animation<double>?` | 自定义动画 |

### SnackBarBehavior 取值

| 取值 | 说明 |
| --- | --- |
| `SnackBarBehavior.fixed` | 固定在底部(默认 M2 风格) |
| `SnackBarBehavior.floating` | 浮动(M3 推荐,带阴影) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Message 最小示例:SnackBar + SnackBarAction
class MessageSample extends StatelessWidget {
  const MessageSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Message 示例')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 1. 基础 SnackBar
            ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('这是一条消息'),
                    duration: Duration(seconds: 2),
                  ),
                );
              },
              child: const Text('显示基础消息'),
            ),
            // 2. 带操作的 SnackBar
            ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: const Text('已删除'),
                    action: SnackBarAction(
                      label: '撤销',
                      onPressed: () {
                        // 撤销删除逻辑
                      },
                    ),
                  ),
                );
              },
              child: const Text('显示带操作的消息'),
            ),
            // 3. M3 floating 风格
            ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: const Text('M3 浮动消息'),
                    behavior: SnackBarBehavior.floating,
                    backgroundColor: {color-primary},
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular({radius-md}),
                    ),
                    margin: const EdgeInsets.all({spacing-md}),
                  ),
                );
              },
              child: const Text('显示浮动消息'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: Row(
      children: [
        Icon(Icons.check_circle, color: {color-on-primary}),
        const SizedBox(width: {spacing-sm}),
        Expanded(
          child: Text(
            '操作成功',
            style: TextStyle(color: {color-on-primary}),
          ),
        ),
      ],
    ),
    behavior: SnackBarBehavior.floating,
    backgroundColor: {color-primary},
    elevation: {elevation-md},
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-md}),
    ),
    margin: const EdgeInsets.all({spacing-md}),
    padding: const EdgeInsets.symmetric(
      horizontal: {spacing-md},
      vertical: {spacing-sm},
    ),
    duration: const Duration(seconds: 3),
    action: SnackBarAction(
      label: '查看',
      textColor: {color-on-primary},
      onPressed: () {},
    ),
  ),
)
```

> 注:示例中的 `{color-primary}`、`{spacing-md}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - 展示 SnackBar: https://docs.flutter.cn/cookbook/design/snackbars
- API 参考 - SnackBar: https://api.flutter.dev/flutter/material/SnackBar-class.html
- API 参考 - SnackBarAction: https://api.flutter.dev/flutter/material/SnackBarAction-class.html
- API 参考 - ScaffoldMessenger: https://api.flutter.dev/flutter/material/ScaffoldMessenger-class.html
- API 参考 - MaterialBanner: https://api.flutter.dev/flutter/material/MaterialBanner-class.html
- pub.dev - fluttertoast: https://pub.flutter-io.cn/packages/fluttertoast
