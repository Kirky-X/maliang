# Flutter Alert Widget 定义

## Widget 定义

Flutter Material Design 3 通过对话框体系提供"警示框"能力,核心由 `showDialog` + `AlertDialog` / `SimpleDialog` 组合实现。与其他框架(Ant Design `Modal.warning`、Element `MessageBox`)的"警示弹窗"对应。

| Alert 类型 | 实现方式 | 基类 | 用途 |
| --- | --- | --- | --- |
| AlertDialog | `AlertDialog` | `StatelessWidget` | 标题+内容+操作按钮的标准警示框 |
| SimpleDialog | `SimpleDialog` | `StatelessWidget` | 选项列表式警示框 |
| SimpleDialogOption | `SimpleDialogOption` | `StatelessWidget` | SimpleDialog 选项条目 |
| Dialog(全屏) | `Dialog.fullscreen` | `StatelessWidget` | 全屏对话框(M3 新增) |

> 弹出由 `showDialog` / `showAdaptiveDialog`(M3 跨平台)驱动,返回 `Future<T?>` 用于接收用户选择。

## 构造函数

### AlertDialog

```dart
const AlertDialog({
  super.key,
  this.icon,                       // 顶部图标(M3 推荐)
  this.iconColor,                  // 图标颜色
  this.iconPadding,                // 图标内边距
  this.title,                      // 标题
  this.titlePadding,               // 标题内边距
  this.titleTextStyle,             // 标题文字样式
  this.content,                    // 内容区(通常为 Text 或 Column)
  this.contentPadding,             // 内容区内边距
  this.contentTextStyle,           // 内容文字样式
  this.actions,                    // 操作按钮列表(List<Widget>)
  this.actionsPadding,             // 操作区内边距
  this.actionsAlignment,           // 操作区对齐
  this.actionsOverflowDirection,   // 操作区溢出方向
  this.actionsOverflowSpacing,     // 操作区溢出间距
  this.buttonPadding,              // 按钮内边距
  this.backgroundColor,            // 背景色
  this.elevation,                  // z 轴高度
  this.shadowColor,                // 阴影色
  this.surfaceTintColor,           // M3 表面染色
  this.insetPadding,               // 外边距(默认屏幕两侧 40)
  this.clipBehavior,               // 裁剪行为
  this.shape,                      // 形状(圆角等)
  this.alignment,                  // 对齐位置
  this.scrollable = false,         // 是否可滚动
})
```

### SimpleDialog

```dart
const SimpleDialog({
  super.key,
  this.title,                  // 标题
  this.titlePadding,           // 标题内边距
  this.titleTextStyle,         // 标题文字样式
  this.children,               // 选项列表(List<Widget>,通常为 SimpleDialogOption)
  this.contentPadding,         // 内容区内边距
  this.backgroundColor,        // 背景色
  this.elevation,              // 高度
  this.shadowColor,
  this.surfaceTintColor,
  this.insetPadding,
  this.clipBehavior,
  this.shape,
  this.alignment,
})
```

## 核心属性(AlertDialog)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `icon` | `Widget?` | 顶部图标(M3 推荐使用,如 `Icon(Icons.warning)`) |
| `title` | `Widget?` | 警示标题 |
| `content` | `Widget?` | 警示内容 |
| `actions` | `List<Widget>?` | 操作按钮,通常为 `TextButton` 或 `FilledButton` |
| `backgroundColor` | `Color?` | 背景色 |
| `elevation` | `double?` | 高度(M3 默认 6) |
| `shape` | `ShapeBorder?` | 形状(M3 默认圆角 28) |
| `alignment` | `AlignmentGeometry?` | 屏幕对齐(默认居中) |
| `scrollable` | `bool` | 内容超出时是否滚动 |
| `actionsAlignment` | `MainAxisAlignment?` | 操作按钮对齐(M3 默认 `end`) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// 警示框最小示例:展示标准 AlertDialog
class AlertSample extends StatelessWidget {
  const AlertSample({super.key});

  Future<void> _showAlert(BuildContext context) async {
    final result = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        icon: const Icon(Icons.warning),
        title: const Text('确认操作'),
        content: const Text('此操作不可撤销,是否继续?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, 'cancel'),
            child: const Text('取消'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, 'ok'),
            child: const Text('确认'),
          ),
        ],
      ),
    );
    debugPrint('用户选择: $result');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Alert 示例')),
      body: Center(
        child: FilledButton(
          onPressed: () => _showAlert(context),
          child: const Text('显示警示框'),
        ),
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    icon: Icon(Icons.error, color: {color-error}, size: {icon-size-md}),
    title: Text(
      '错误',
      style: TextStyle(
        fontSize: {font-size-lg},
        fontWeight: FontWeight.w600,
        color: {color-text-primary},
      ),
    ),
    content: Text(
      '操作失败,请稍后重试',
      style: TextStyle(
        fontSize: {font-size-md},
        color: {color-text-secondary},
      ),
    ),
    backgroundColor: {color-surface},
    surfaceTintColor: {color-surface-variant},
    elevation: {elevation-md},
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-lg}),
    ),
    actionsPadding: EdgeInsets.all({spacing-md}),
    actions: [
      FilledButton(
        style: FilledButton.styleFrom(
          backgroundColor: {color-error},
          foregroundColor: {color-on-error},
        ),
        onPressed: () => Navigator.pop(context),
        child: const Text('知道了'),
      ),
    ],
  ),
)
```

> 注:示例中的 `{color-error}`、`{spacing-md}`、`{radius-lg}`、`{icon-size-md}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - AlertDialog: https://api.flutter.dev/flutter/material/AlertDialog-class.html
- API 参考 - SimpleDialog: https://api.flutter.dev/flutter/material/SimpleDialog-class.html
- API 参考 - showDialog: https://api.flutter.dev/flutter/material/showDialog.html
