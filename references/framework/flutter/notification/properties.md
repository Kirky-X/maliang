# Flutter Notification 属性列表与默认值

> MaterialBanner 与 ScaffoldMessenger 方法的参数唯一真源见 [message](../message/properties.md);本文件保留 notification 场景的选型对照与完整示例,不复述参数表(防双份漂移)。

本文档汇总 `MaterialBanner` 的完整属性与常驻横幅/消息中心的组合规格。所有颜色默认值以 design token 形式给出。

## notification 与 message(toast)选型对照

| 维度 | notification(本类) | message(SnackBar) |
| --- | --- | --- |
| 驻留 | 常驻,必须手动关闭 | 1.5-5s 自动消失 |
| 操作 | actions 多按钮(重试/查看) | 至多 1 个 action |
| 排版 | 多行 + leading 图标 | 单行截断 |
| 典型 | 同步失败、离线横幅、版本公告 | "已删除"类轻反馈 |

## 完整示例(常驻横幅 + 未读消息中心)

```dart
import 'package:flutter/material.dart';

class NotificationFullSample extends StatefulWidget {
  const NotificationFullSample({super.key});

  @override
  State<NotificationFullSample> createState() => _NotificationFullSampleState();
}

class _Message {
  _Message(this.title, this.unread);
  final String title;
  final bool unread;
}

class _NotificationFullSampleState extends State<NotificationFullSample> {
  final List<_Message> _items = [
    _Message('订单已发货', true),
    _Message('优惠券到账', true),
    _Message('登录提醒', false),
  ];

  void _showSyncBanner() {
    ScaffoldMessenger.of(context)
      ..hideCurrentMaterialBanner()
      ..showMaterialBanner(MaterialBanner(
        content: const Text('同步失败,3 条变更未同步'),
        leading: const Icon(Icons.cloud_off),
        actions: [
          TextButton(
            onPressed: () => ScaffoldMessenger.of(context).hideCurrentMaterialBanner(),
            child: const Text('重试'),
          ),
          TextButton(
            onPressed: () => ScaffoldMessenger.of(context).hideCurrentMaterialBanner(),
            child: const Text('关闭'),
          ),
        ],
        backgroundColor: {color-bg-secondary},
        elevation: 0,
      ));
  }

  @override
  Widget build(BuildContext context) {
    final unread = _items.where((m) => m.unread).length;
    return Scaffold(
      appBar: AppBar(
        title: const Text('消息中心'),
        actions: [
          Badge(
            label: Text('$unread'),
            isLabelVisible: unread > 0,
            child: IconButton(
              tooltip: '未读消息',
              icon: const Icon(Icons.notifications),
              onPressed: _showSyncBanner,
            ),
          ),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all({spacing-md}),
        itemCount: _items.length,
        itemBuilder: (_, i) => ListTile(
          title: Text(
            _items[i].title,
            style: TextStyle(
              fontWeight: _items[i].unread ? FontWeight.bold : FontWeight.normal,
            ),
          ),
          trailing: _items[i].unread
              ? const Icon(Icons.circle, size: 8, color: {color-primary})
              : null,
        ),
      ),
    );
  }
}
```

## 注意事项

- `showMaterialBanner` **不会自动消失**,`actions` 必须提供关闭入口,否则遮蔽内容。
- 横幅显示在 Scaffold 顶部、正文之下的 `Material` 层;多横幅排队展示。
- 需要"叠在 AppBar 之上"或全局多层时改用 `Overlay` + 自定义 Entry,注意 `rootOverlay` 与层级 `{z-index-*}`。
- 与 SnackBar 分工:能 5s 内忘掉的信息不进横幅(避免打断)。
- 无障碍:横幅出现时经 `Semantics(liveRegion: true)` 播报;关闭/重试按钮必须有 tooltip/语义标签。
