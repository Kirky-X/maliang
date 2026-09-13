# Flutter Popconfirm 属性列表与默认值

本文档定义 Popconfirm 组合方案(轻量确认弹窗)的规格参数。所有颜色默认值以 design token 形式给出。

## 组合方案规格参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `title / content` | `String` | 必填 | 确认问题,必须含明确宾语(对象名/金额) |
| `confirmText` | `String` | `'确定'`(建议具体动词) | 确认按钮文案,建议写"删除""确认注销" |
| `cancelText` | `String` | `'取消'` | 取消按钮文案 |
| `dangerous` | `bool` | `false` | 破坏性操作(确认按钮用 `{color-error}`) |
| `barrierDismissible` | `bool` | `true` | 点外部关闭(轻量确认建议 true) |
| `placement` | 枚举 | 触发器就近 | 气泡方案(Overlay)方位 |

## AlertDialog 相关参数(轻量确认形态)

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `content` | `Widget` | — | 问题文本 |
| `contentPadding` | `EdgeInsetsGeometry` | 取主题 | 建议 `{spacing-md}`(紧凑感) |
| `actions` | `List<Widget>` | — | 取消(左)+ 确认(右) |
| `actionsPadding` | `EdgeInsetsGeometry` | 取主题 | 按钮区内边距 |
| `title` | `Widget?` | `null` | 重确认时的标题 |

## 确认分级规范

| 级别 | 场景 | 形态 |
| --- | --- | --- |
| 轻量 | 列表项删除、移除收藏 | 气泡/紧凑弹窗(barrierDismissible: true) |
| 中等 | 退款、取消订单 | 紧凑弹窗 + 明确宾语(金额) |
| 重量 | 注销账户、清空数据 | 完整 AlertDialog(标题 + 后果说明) |

## 完整示例(危险确认 + 普通确认两档)

```dart
import 'package:flutter/material.dart';

class PopconfirmFullSample extends StatelessWidget {
  const PopconfirmFullSample({super.key});

  Future<bool> _confirm(
    BuildContext context, {
    required String question,
    required String confirmText,
    bool dangerous = false,
  }) async {
    final result = await showDialog<bool>(
      context: context,
      barrierDismissible: true,
      builder: (context) => AlertDialog(
        contentPadding: const EdgeInsets.all({spacing-md}),
        content: Text(question),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('取消'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(
              foregroundColor:
                  dangerous ? {color-error} : {color-primary},
            ),
            child: Text(confirmText),
          ),
        ],
      ),
    );
    return result ?? false;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('订单详情')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          OutlinedButton(
            child: const Text('申请退款'),
            onPressed: () async {
              final ok = await _confirm(
                context,
                question: '确认申请退款 ¥128.00?',
                confirmText: '确认申请',
              );
              if (ok && context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('退款申请已提交')),
                );
              }
            },
          ),
          const SizedBox(height: {spacing-md}),
          OutlinedButton(
            style: OutlinedButton.styleFrom(
              foregroundColor: {color-error},
            ),
            child: const Text('删除订单'),
            onPressed: () async {
              final ok = await _confirm(
                context,
                question: '确认删除该订单记录?',
                confirmText: '删除',
                dangerous: true,
              );
              if (ok && context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('已删除')),
                );
              }
            },
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- **确认按钮写具体动词**(删除/确认注销),不写"确定";取消为非危险默认样式。
- **危险色只给破坏性动作**;普通确认用 `{color-primary}`。
- **Web 端 (Flutter web)**:气泡形态建议 `Overlay` + `CompositedTransformFollower` 原位跟随;移动端紧凑弹窗体验更稳。
- 轻量确认 `barrierDismissible: true` + Esc 可关;重量确认(不可逆)建议 `barrierDismissible: false` 强制选择。
- 确认后的结果反馈走 toast(message 类),不在确认弹窗内继续弹层。
- 无障碍:弹窗自动获得焦点与模态语义;按钮文字自明,读屏完整播报问题与两个选项。
