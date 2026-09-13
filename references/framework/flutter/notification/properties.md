# Flutter Notification 属性列表与默认值

本文档汇总 `MaterialBanner` 的完整属性与常驻横幅/消息中心的组合规格。所有颜色默认值以 design token 形式给出。

## MaterialBanner 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `content` | `Widget` | 必填 | 正文(支持多行富文本) |
| `actions` | `List<Widget>` | 必填 | 操作按钮组(至少含"关闭") |
| `leading` | `Widget?` | `null` | 前置图标(状态图标) |
| `backgroundColor` | `Color?` | 取主题 surface | 背景色,建议 `{color-bg-secondary}` |
| `surfaceTintColor` | `Color?` | 取主题 | M3 表面着色 |
| `shadowColor` | `Color?` | 取主题 | 阴影色 |
| `dividerColor` | `Color?` | 取主题 | 与内容分隔线颜色 |
| `elevation` | `double?` | `null` | 海拔(横幅建议 0-1) |
| `forceActionsBelow` | `bool` | `false` | 操作按钮强制换行到下方 |
| `margin` / `padding` | `EdgeInsetsGeometry?` | 取主题 | 外/内边距 |
| `onVisible` | `VoidCallback?` | `null` | 横幅首次可见回调 |

## ScaffoldMessenger 方法

| 方法 | 说明 |
| --- | --- |
| `showMaterialBanner(banner)` | 显示常驻横幅(不自动消失) |
| `hideCurrentMaterialBanner()` | 关闭当前横幅 |
| `clearMaterialBanners()` | 清空队列 |
| `showSnackBar(snackBar)` | toast 语义(短暂,归 message 类) |

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
