# Flutter Message 属性列表与默认值

本文档汇总 `SnackBar` / `SnackBarAction` / `MaterialBanner` 的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## SnackBar 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `content` | `Widget` | 必填 | 消息内容 |
| `action` | `SnackBarAction?` | `null` | 操作按钮 |
| `duration` | `Duration` | `Duration(milliseconds: 4000)` | 显示时长 |
| `behavior` | `SnackBarBehavior?` | `null`(取主题,M3 默认 floating) | 显示方式 |
| `backgroundColor` | `Color?` | `null`(取主题 `{color-inverse-surface}`) | 背景色 |
| `elevation` | `double?` | `null`(M3 默认 6.0) | 阴影高度 |
| `shadowColor` | `Color?` | `null`(取主题) | 阴影色 |
| `surfaceTintColor` | `Color?` | `null`(取主题) | 表面染色(M3) |
| `margin` | `EdgeInsetsGeometry?` | `null`(floating 时 `EdgeInsets.all(8)`) | 外边距 |
| `padding` | `EdgeInsetsGeometry?` | `null`(默认 `EdgeInsets.symmetric(horizontal: 16, vertical: 8)`) | 内边距 |
| `shape` | `ShapeBorder?` | `null`(M3 默认圆角矩形 4dp) | 形状 |
| `width` | `double?` | `null` | 宽度(设置后强制 floating) |
| `showCloseIcon` | `bool?` | `false` | 是否显示关闭图标 |
| `closeIconColor` | `Color?` | `null`(取主题) | 关闭图标颜色 |
| `dismissDirection` | `DismissDirection?` | `DismissDirection.horizontal` | 滑动关闭方向 |
| `animation` | `Animation<double>?` | `null` | 自定义动画 |
| `onVisible` | `VoidCallback?` | `null` | 显示完成回调 |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 裁剪行为 |

## SnackBarAction 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `label` | `String` | 必填 | 按钮文本 |
| `onPressed` | `VoidCallback` | 必填 | 点击回调 |
| `textColor` | `Color?` | `null`(取主题 `{color-inverse-primary}`) | 文本颜色 |
| `disabledTextColor` | `Color?` | `null` | 禁用态文本颜色 |

## SnackBarBehavior 取值

| 取值 | 说明 | M3 推荐 |
| --- | --- | --- |
| `SnackBarBehavior.fixed` | 固定底部(占满宽度,无 margin) | 否 |
| `SnackBarBehavior.floating` | 浮动(带 margin 和 elevation) | 是 |

## ScaffoldMessenger 方法

| 方法 | 说明 |
| --- | --- |
| `showSnackBar(SnackBar)` | 显示 SnackBar(会关闭当前) |
| `hideCurrentSnackBar({reason})` | 隐藏当前(带动画) |
| `removeCurrentSnackBar({reason})` | 移除当前(无动画) |
| `clearSnackBars()` | 清空队列 |
| `currentSnackBar` | `ScaffoldFeatureController<SnackBar, SnackBarClosedReason>?` 当前 SnackBar |

## SnackBarClosedReason 取值

| 取值 | 说明 |
| --- | --- |
| `SnackBarClosedReason.action` | 用户点击 action |
| `SnackBarClosedReason.dismiss` | 用户滑动关闭 |
| `SnackBarClosedReason.hide` | 调用 `hideCurrentSnackBar` |
| `SnackBarClosedReason.remove` | 调用 `removeCurrentSnackBar` / `clearSnackBars` |
| `SnackBarClosedReason.timeout` | `duration` 到期 |
| `SnackBarClosedReason.swipe` | 滑动关闭(等价 dismiss) |

## MaterialBanner 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `content` | `Widget` | 必填 | 内容 |
| `actions` | `List<Widget>` | 必填 | 操作按钮列表 |
| `leading` | `Widget?` | `null` | 前置图标 |
| `backgroundColor` | `Color?` | `null`(取主题 `{color-surface}`) | 背景色 |
| `elevation` | `double?` | `null`(M3 默认 0) | 阴影高度 |
| `shadowColor` | `Color?` | `null` | 阴影色 |
| `surfaceTintColor` | `Color?` | `null` | 表面染色 |
| `padding` | `EdgeInsetsGeometry?` | `null`(默认 `EdgeInsets.all(16)`) | 内边距 |
| `leadingPadding` | `EdgeInsetsGeometry?` | `null`(默认 `EdgeInsets.symmetric(horizontal: 8)`) | 前置图标内边距 |
| `contentTextStyle` | `TextStyle?` | `null`(取主题) | 内容文本样式 |
| `forceActionsBelow` | `bool?` | `null` | 强制操作按钮在内容下方 |
| `overflowAlignment` | `OverflowBarAlignment` | `OverflowBarAlignment.end` | 操作按钮对齐 |
| `forceOverflowBelow` | `bool` | `false` | 强制溢出在下方 |
| `dividerColor` | `Color?` | `null` | 分隔线颜色 |

## ScaffoldMessengerState 关键方法

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `showMaterialBanner` | `void showMaterialBanner(MaterialBanner banner)` | 显示 MaterialBanner |
| `hideCurrentMaterialBanner` | `void hideCurrentMaterialBanner()` | 隐藏当前 |
| `removeCurrentMaterialBanner` | `void removeCurrentMaterialBanner()` | 移除当前 |
| `clearMaterialBanners` | `void clearMaterialBanners()` | 清空队列 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class MessageFullSample extends StatelessWidget {
  const MessageFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Message 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 基础 SnackBar
          ElevatedButton(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('基础消息提示')),
              );
            },
            child: const Text('基础 SnackBar'),
          ),
          // 2. 带操作 + 撤销逻辑
          ElevatedButton(
            onPressed: () => _showUndoSnackBar(context),
            child: const Text('带撤销操作'),
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
                  elevation: {elevation-md},
                  showCloseIcon: true,
                  closeIconColor: {color-on-primary},
                ),
              );
            },
            child: const Text('M3 浮动消息'),
          ),
          // 4. 自定义内容(带图标)
          ElevatedButton(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Row(
                    children: [
                      Icon(Icons.check_circle, color: {color-on-primary}),
                      const SizedBox(width: {spacing-sm}),
                      const Expanded(child: Text('操作成功')),
                    ],
                  ),
                  backgroundColor: {color-success},
                  behavior: SnackBarBehavior.floating,
                ),
              );
            },
            child: const Text('成功消息(带图标)'),
          ),
          // 5. 错误消息
          ElevatedButton(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: const Text('操作失败,请重试'),
                  backgroundColor: {color-error},
                  behavior: SnackBarBehavior.floating,
                  action: SnackBarAction(
                    label: '重试',
                    textColor: {color-on-error},
                    onPressed: () {},
                  ),
                ),
              );
            },
            child: const Text('错误消息(带重试)'),
          ),
          const Divider(),
          // 6. MaterialBanner(顶部持久)
          ElevatedButton(
            onPressed: () {
              ScaffoldMessenger.of(context).showMaterialBanner(
                MaterialBanner(
                  content: const Text('网络连接异常'),
                  leading: const Icon(Icons.wifi_off),
                  backgroundColor: {color-warning-bg},
                  contentTextStyle: TextStyle(color: {color-warning-text}),
                  actions: [
                    TextButton(
                      onPressed: () =>
                          ScaffoldMessenger.of(context).hideCurrentMaterialBanner(),
                      child: const Text('关闭'),
                    ),
                    TextButton(
                      onPressed: () {},
                      child: const Text('重试'),
                    ),
                  ],
                ),
              );
            },
            child: const Text('显示 MaterialBanner'),
          ),
        ],
      ),
    );
  }

  void _showUndoSnackBar(BuildContext context) {
    final messenger = ScaffoldMessenger.of(context);
    messenger.showSnackBar(
      SnackBar(
        content: const Text('已删除 1 项'),
        duration: const Duration(seconds: 5),
        action: SnackBarAction(
          label: '撤销',
          onPressed: () {
            messenger.showSnackBar(
              const SnackBar(
                content: Text('已恢复'),
                duration: Duration(seconds: 1),
              ),
            );
          },
        ),
      ),
    );
  }
}
```

## 注意事项

- `SnackBar` 必须通过 `ScaffoldMessenger.of(context).showSnackBar` 显示;**不要直接 `showDialog` 包装**,会破坏队列管理。
- `ScaffoldMessenger` 是 Flutter 2.0+ 引入的,替代旧的 `Scaffold.of(context).showSnackBar`;旧 API 已废弃。
- `SnackBar` 队列:新 SnackBar 会立即关闭当前并显示自己;若需排队显示,需自行管理 `Future.delayed`。
- `duration: Duration(seconds: 0)` 不会立即关闭,需用 `Duration(milliseconds: 1)` 或 `removeCurrentSnackBar`。
- `behavior: SnackBarBehavior.floating` 与 `width` 互斥;设置 `width` 会强制 floating 且忽略 `margin`。
- `MaterialBanner` 持续显示直到用户关闭,**不要用于临时提示**,会遮挡内容。
- `ScaffoldMessengerState` 在 `Scaffold` 上层,跨页面时 SnackBar 不会消失;若需页面级隔离,使用 `ScaffoldMessenger`(独立实例)包裹。
- iOS 上 `SnackBar` 行为与 Android 一致(非原生风格);若需 iOS 原生 Toast,使用 `Cupertino` 风格自定义或 `fluttertoast` 包。
