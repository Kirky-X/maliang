# Flutter Dialog 属性列表与默认值

本文档汇总 `AlertDialog` / `SimpleDialog` / `showDialog` 的属性、默认值与回调。颜色/尺寸默认值以 design token 形式给出。

## showDialog 参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `context` | `BuildContext` | 必填 | 上下文 |
| `builder` | `WidgetBuilder` | 必填 | 对话框构建函数 |
| `barrierDismissible` | `bool` | `true` | 点击遮罩关闭 |
| `barrierColor` | `Color?` | `Colors.black54` | 遮罩色 |
| `barrierLabel` | `String?` | `null` | 无障碍标签 |
| `useSafeArea` | `bool` | `true` | 避开系统 UI |
| `useRootNavigator` | `bool` | `true` | 用根 Navigator |
| `routeSettings` | `RouteSettings?` | `null` | 路由设置 |
| `anchorPoint` | `Offset?` | `null` | 锚点(显示位置) |

## AlertDialog 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `icon` | `Widget?` | `null` | 顶部图标(M3) |
| `iconPadding` | `EdgeInsetsGeometry?` | `null` | 图标内边距 |
| `iconColor` | `Color?` | `null` | 图标颜色 |
| `title` | `Widget?` | `null` | 标题 |
| `titlePadding` | `EdgeInsetsGeometry?` | `null` | 标题内边距 |
| `titleTextStyle` | `TextStyle?` | `null` | 标题样式 |
| `content` | `Widget?` | `null` | 内容 |
| `contentPadding` | `EdgeInsetsGeometry` | `EdgeInsets.fromLTRB(24, 20, 24, 24)` | 内容内边距 |
| `contentTextStyle` | `TextStyle?` | `null` | 内容样式 |
| `actions` | `List<Widget>?` | `null` | 底部按钮 |
| `actionsPadding` | `EdgeInsetsGeometry?` | `null` | 按钮区内边距 |
| `actionsAlignment` | `MainAxisAlignment?` | `null` | 按钮对齐 |
| `actionsOverflowDirection` | `VerticalDirection?` | `null` | 按钮溢出方向 |
| `actionsOverflowButtonSpacing` | `double?` | `null` | 溢出按钮间距 |
| `buttonPadding` | `EdgeInsetsGeometry?` | `null` | 单按钮内边距 |
| `backgroundColor` | `Color?` | `null`(主题 surface) | 背景色 |
| `elevation` | `double?` | `null` | 高度 |
| `shadowColor` | `Color?` | `null` | 阴影色 |
| `surfaceTintColor` | `Color?` | `null` | 表面染色 |
| `shape` | `ShapeBorder?` | `null`(默认圆角 28) | 形状 |
| `clipBehavior` | `Clip` | `Clip.none` | 裁剪 |
| `alignment` | `AlignmentGeometry?` | `null`(居中) | 对齐 |
| `semanticLabel` | `String?` | `null` | 无障碍标签 |

## SimpleDialog 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `title` | `Widget?` | `null` | 标题 |
| `titlePadding` | `EdgeInsetsGeometry?` | `null` | 标题内边距 |
| `titleTextStyle` | `TextStyle?` | `null` | 标题样式 |
| `children` | `List<Widget>?` | `null` | 选项(通常 SimpleDialogOption) |
| `contentPadding` | `EdgeInsetsGeometry` | `EdgeInsets.fromLTRB(0, 12, 0, 16)` | 内容内边距 |
| `backgroundColor` | `Color?` | `null` | 背景色 |
| `elevation` | `double?` | `null` | 高度 |
| `shape` | `ShapeBorder?` | `null` | 形状 |

## SimpleDialogOption 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `onPressed` | `VoidCallback?` | `null` | 选中回调 |
| `child` | `Widget?` | `null` | 选项内容 |
| `padding` | `EdgeInsetsGeometry` | `EdgeInsets.symmetric(vertical: 8, horizontal: 24)` | 内边距 |

## 事件/返回值

`showDialog<T>` 返回 `Future<T?>`:
- `Navigator.pop(context, value)` 关闭并返回 `value`
- `Navigator.pop(context)` 关闭返回 `null`
- 点击遮罩(若 `barrierDismissible: true`)关闭返回 `null`

## 完整示例

```dart
import 'package:flutter/material.dart';

class DialogFullSample extends StatelessWidget {
  const DialogFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Dialog 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. AlertDialog(确认)
          ElevatedButton(
            child: const Text('AlertDialog'),
            onPressed: () async {
              final r = await showDialog<bool>(
                context: context,
                builder: (_) => AlertDialog(
                  icon: const Icon(Icons.warning),
                  iconColor: {color-warning},
                  title: const Text('确认操作'),
                  content: const Text('即将执行不可逆操作,是否继续?'),
                  backgroundColor: {color-bg-primary},
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular({radius-lg}),
                  ),
                  actionsAlignment: MainAxisAlignment.end,
                  actions: [
                    TextButton(
                      child: const Text('取消'),
                      onPressed: () => Navigator.pop(context, false),
                    ),
                    FilledButton(
                      child: const Text('确认'),
                      onPressed: () => Navigator.pop(context, true),
                    ),
                  ],
                ),
              );
              debugPrint('确认结果: $r');
            },
          ),
          // 2. SimpleDialog(选择)
          ElevatedButton(
            child: const Text('SimpleDialog'),
            onPressed: () async {
              final r = await showDialog<String>(
                context: context,
                builder: (_) => SimpleDialog(
                  title: const Text('选择语言'),
                  children: [
                    SimpleDialogOption(
                      onPressed: () => Navigator.pop(context, 'zh'),
                      child: const Text('简体中文'),
                    ),
                    SimpleDialogOption(
                      onPressed: () => Navigator.pop(context, 'en'),
                      child: const Text('English'),
                    ),
                  ],
                ),
              );
              debugPrint('选择: $r');
            },
          ),
          // 3. 底部弹窗
          ElevatedButton(
            child: const Text('ModalBottomSheet'),
            onPressed: () async {
              await showModalBottomSheet(
                context: context,
                builder: (_) => Container(
                  padding: const EdgeInsets.all({spacing-md}),
                  child: const Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text('底部弹窗'),
                      ListTile(title: Text('选项一')),
                      ListTile(title: Text('选项二')),
                    ],
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- `showDialog` 内 `Navigator.pop(context, value)` 的 `context` 必须是对话框构建函数的 context,否则可能弹错栈
- `useRootNavigator: true`(默认)对嵌套 Navigator 至关重要,避免对话框被内层 Navigator 覆盖
- `barrierDismissible: false` 用于强制用户做出选择(如必须确认删除)
- 对话框内容过长时,用 `SingleChildScrollView` 包裹 `content`
- `actions` 按钮顺序:Android 习惯"取消在左、确认在右",iOS 反之;`actionsOverflowDirection` 控制溢出排列
- 全屏对话框用 `showDialog` + `Dialog(fullscreen)` 或 `showGeneralDialog` 自定义转场
