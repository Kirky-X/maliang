# Flutter Popconfirm Widget 定义

> **本组件为 maliang 组合方案,Flutter 无原生 Popconfirm 气泡确认 Widget。** 通过 `showDialog`(轻量确认弹窗)或 `Overlay` 自定义气泡组合实现破坏性操作二次确认。

## 缺失原因

Flutter Material 未提供"气泡内确认/取消双按钮"的 Popconfirm 形态(M3 无对应组件);二次确认由 AlertDialog 或 Overlay 组合承担。

## 替代方案(组合结构)

| 角色 | Flutter 实现 |
| --- | --- |
| 轻量确认 | `showDialog` + 自定义 `AlertDialog`(紧凑,小窗) |
| 原位气泡 | `Overlay` + `CompositedTransformFollower`(跟随触发器) |
| 确认/取消按钮 | `Row` + `TextButton`(确认用 `{color-error}`) |
| 重确认升级 | `showDialog` + `AlertDialog`(完整弹窗,见 dialog 类) |

## 核心 API(组合方案)

```dart
Future<bool?> showConfirmDelete(BuildContext context) {
  return showDialog<bool>(
    context: context,
    builder: (context) => AlertDialog(
      content: const Text('确认删除"地址一"?'),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context, false),
          child: const Text('取消'),
        ),
        TextButton(
          onPressed: () => Navigator.pop(context, true),
          style: TextButton.styleFrom(foregroundColor: {color-error}),
          child: const Text('删除'),
        ),
      ],
    ),
  );
}
```

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Popconfirm 最小示例:列表项删除二次确认
class PopconfirmSample extends StatelessWidget {
  const PopconfirmSample({super.key});

  Future<void> _confirmDelete(BuildContext context, String item) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        contentPadding: const EdgeInsets.all({spacing-md}),
        content: Text('确认删除"$item"?'),
        actionsPadding: const EdgeInsets.symmetric(horizontal: {spacing-md}),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('取消'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: {color-error}),
            child: const Text('删除'),
          ),
        ],
      ),
    );
    if (confirmed == true && context.mounted) {
      // 执行删除后用 toast(message 类)反馈
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('已删除')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('地址管理')),
      body: ListView(
        children: ['地址一', '地址二'].map((item) {
          return ListTile(
            title: Text(item),
            trailing: IconButton(
              tooltip: '删除$item',
              icon: const Icon(Icons.delete_outline),
              onPressed: () => _confirmDelete(context, item),
            ),
          );
        }).toList(),
      ),
    );
  }
}
```

## 参考链接

- API 参考 - AlertDialog: https://api.flutter.dev/flutter/material/AlertDialog-class.html
- API 参考 - Overlay: https://api.flutter.dev/flutter/widgets/Overlay-class.html
