# Flutter FAB 属性列表与默认值

本文档汇总 `FloatingActionButton` 系列的完整属性、默认值与滚动联动实现。所有颜色默认值以 design token 形式给出。

## FloatingActionButton 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `onPressed` | `VoidCallback?` | 必填 | 点击回调;`null` 时禁用 |
| `child` | `Widget` | — | 内容(图标) |
| `tooltip` | `String?` | `null` | 长按提示 + 读屏语义(必须声明) |
| `foregroundColor` | `Color?` | 取主题 onPrimaryContainer | 图标色,建议 `{color-text-inverse}` |
| `backgroundColor` | `Color?` | 取主题 primaryContainer | 底色,建议 `{color-primary}` |
| `focusColor` / `hoverColor` / `splashColor` | `Color?` | 取主题 | 交互态颜色 |
| `elevation` | `double?` | `6`(M3 默认 3) | 海拔 |
| `highlightElevation` | `double?` | `12`(M3 默认 3) | 按压海拔 |
| `disabledElevation` | `double?` | 取主题 | 禁用海拔 |
| `shape` | `ShapeBorder?` | 取主题(CircularNotched) | 形状 |
| `mini` | `bool` | `false` | 小尺寸(40dp) |
| `isExtended` | `bool` | `false` | 扩展胶囊形态 |
| `materialTapTargetSize` | `MaterialTapTargetSize?` | 取主题 | 触控目标尺寸 |

## 工厂构造差异

| 构造 | 尺寸 | 典型用途 |
| --- | --- | --- |
| `FloatingActionButton()` | 56dp 圆形 | 标准"新建"入口 |
| `FloatingActionButton.small()` | 40dp 圆形 | 次级悬浮(桌面端) |
| `FloatingActionButton.large()` | 96dp 圆形 | 特殊强调 |
| `FloatingActionButton.extended()` | 56dp 高胶囊 | 图标 + 文案(写邮件/发布) |

## Scaffold 相关属性

| 属性 | 说明 |
| --- | --- |
| `floatingActionButton` | 挂载 FAB |
| `floatingActionButtonLocation` | 位置(`endFloat` 默认 / `endDocked` 与 dock 融合 / `centerDocked`) |
| `floatingActionButtonAnimator` | 位置/显隐动画 |

## 完整示例(滚动联动出现/收起)

```dart
import 'package:flutter/material.dart';

class ScrollFabSample extends StatefulWidget {
  const ScrollFabSample({super.key});

  @override
  State<ScrollFabSample> createState() => _ScrollFabSampleState();
}

class _ScrollFabSampleState extends State<ScrollFabSample> {
  bool _visible = true;
  double _lastOffset = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('内容流')),
      body: NotificationListener<ScrollNotification>(
        onNotification: (n) {
          if (n.metrics.axis != Axis.vertical) return false;
          final offset = n.metrics.pixels;
          if (offset < _lastOffset) {
            if (!_visible) setState(() => _visible = true); // 下滑显示
          } else if (offset > _lastOffset) {
            if (_visible) setState(() => _visible = false); // 上滑收起
          }
          _lastOffset = offset;
          return false;
        },
        child: ListView.builder(
          itemCount: 40,
          itemBuilder: (_, i) => ListTile(title: Text('条目 $i')),
        ),
      ),
      floatingActionButton: AnimatedScale(
        scale: _visible ? 1.0 : 0.0,
        duration: const Duration(milliseconds: 200),
        child: FloatingActionButton.extended(
          onPressed: () {},
          tooltip: '发布内容',
          backgroundColor: {color-primary},
          foregroundColor: {color-text-inverse},
          icon: const Icon(Icons.publish),
          label: const Text('发布'),
        ),
      ),
    );
  }
}
```

## 注意事项

- **单 FAB 原则**:每页最多 1 个;多动作收进长按/底部 sheet。
- `tooltip` 必须声明(读屏 + 长按提示),否则无障碍语义缺失。
- 滚动联动用 `NotificationListener<ScrollNotification>`;动效 200ms(`AnimatedScale`/`AnimatedSlide`),列表在顶部时必须显示。
- `bottomNavigationBar` 共存时用 `floatingActionButtonLocation: endDocked` 或留出避让边距。
- 颜色经 `ThemeData.floatingActionButtonTheme` 统一注入 token,不要逐实例硬编码。
- 禁用态传 `onPressed: null`;自动转灰并保留占位。
