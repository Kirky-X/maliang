# Flutter FAB Widget 定义

## Widget 定义

Flutter Material Design 3 原生提供悬浮操作按钮 `FloatingActionButton`(FAB),配合 `Scaffold.floatingActionButton` 使用,是移动端"新建/发布/写"一级操作入口的标准实现。

| FAB 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 标准 FAB | `FloatingActionButton` | `StatelessWidget` | 圆形 56dp,单图标 |
| 小型 FAB | `FloatingActionButton.small` | 工厂构造 | 圆形 40dp |
| 大型 FAB | `FloatingActionButton.large` | 工厂构造 | 圆形 96dp |
| 扩展 FAB | `FloatingActionButton.extended` | 工厂构造 | 圆角胶囊(图标 + 文案) |

## 构造函数

```dart
const FloatingActionButton({
  Key? key,
  required VoidCallback? onPressed,
  VoidCallback? onLongPress,
  Widget? child,
  Color? foregroundColor,
  Color? backgroundColor,
  Color? focusColor,
  Color? hoverColor,
  Color? splashColor,
  double? elevation,
  double? focusElevation,
  double? hoverElevation,
  double? highlightElevation,
  double? disabledElevation,
  String? tooltip,
  ShapeBorder? shape,
  bool mini = false,
  MaterialTapTargetSize? materialTapTargetSize,
  bool? enableFeedback,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `onPressed` | `VoidCallback?` | 点击回调;`null` 时禁用 |
| `child` | `Widget` | 内容(图标) |
| `tooltip` | `String?` | 长按提示 + 读屏语义 |
| `backgroundColor` / `foregroundColor` | `Color?` | 底色 / 图标色 |
| `elevation` | `double?` | 海拔(M3 默认 3) |
| `mini` | `bool` | 小尺寸(40dp) |
| `shape` | `ShapeBorder?` | 形状 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// FAB 最小示例:标准圆形 FAB + 扩展 FAB
class FabSample extends StatelessWidget {
  const FabSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('笔记')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: const [Text('列表主体')],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        tooltip: '新建笔记',
        backgroundColor: {color-primary},
        foregroundColor: {color-text-inverse},
        child: const Icon(Icons.add),
      ),
      // 扩展 FAB(写邮件场景):
      // floatingActionButton: FloatingActionButton.extended(
      //   onPressed: () {},
      //   icon: const Icon(Icons.edit),
      //   label: const Text('写邮件'),
      // ),
    );
  }
}
```

## 参考链接

- API 参考 - FloatingActionButton: https://api.flutter.dev/flutter/material/FloatingActionButton-class.html
- Material 3 - FAB: https://m3.material.io/components/floating-action-button
