# Flutter Notification Widget 定义

> **本组件为 maliang 组合方案,Flutter 无原生应用内 Notification(消息中心/横幅)Widget。** 通过 `ScaffoldMessenger.showMaterialBanner`(常驻横幅)+ 自定义 Inbox 列表组合实现。

## 缺失原因

Flutter 的 `SnackBar`(message 类)是短暂轻反馈;应用内"常驻、可关闭、带操作按钮"的通知横幅与消息中心无独立 Material Widget,仅提供 `MaterialBanner` 近似形态与 `NotificationListener`(滚动事件,非本语义)。

## 替代方案(组合结构)

| 角色 | Flutter 实现 |
| --- | --- |
| 常驻横幅 | `ScaffoldMessenger.of(context).showMaterialBanner(MaterialBanner(...))`(不自消失,需手动关闭) |
| 顶部覆盖横幅 | `Overlay` + 自定义 Entry(全局多层) |
| 多行富文本 | `MaterialBannerContent`(leading + content 多行 + actions) |
| 消息中心 | 页面入口 + `ListView` 未读列表(应用层状态) |

## 核心 API

```dart
ScaffoldMessenger.of(context)
  ..hideCurrentMaterialBanner()
  ..showMaterialBanner(MaterialBanner(
    content: const Text('同步失败,3 条变更未同步'),
    leading: const Icon(Icons.cloud_off),
    actions: [
      TextButton(onPressed: _retry, child: const Text('重试')),
      TextButton(
        onPressed: ScaffoldMessenger.of(context).hideCurrentMaterialBanner,
        child: const Text('关闭'),
      ),
    ],
    backgroundColor: {color-bg-secondary},
  ));
```

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Notification 最小示例:常驻失败横幅(重试 + 关闭)
class NotificationSample extends StatelessWidget {
  const NotificationSample({super.key});

  void _showBanner(BuildContext context) {
    ScaffoldMessenger.of(context).showMaterialBanner(
      MaterialBanner(
        content: const Text('上传失败,3 个附件未完成'),
        leading: const Icon(Icons.error_outline),
        actions: [
          TextButton(onPressed: () {}, child: const Text('重试')),
          TextButton(
            onPressed: () => ScaffoldMessenger.of(context).hideCurrentMaterialBanner(),
            child: const Text('关闭'),
          ),
        ],
        backgroundColor: {color-bg-secondary},
        elevation: 0,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Notification 示例')),
      body: Center(
        child: FilledButton(
          onPressed: () => _showBanner(context),
          child: const Text('触发失败横幅'),
        ),
      ),
    );
  }
}
```

## 参考链接

- API 参考 - MaterialBanner: https://api.flutter.dev/flutter/material/MaterialBanner-class.html
- API 参考 - ScaffoldMessenger: https://api.flutter.dev/flutter/material/ScaffoldMessenger-class.html
