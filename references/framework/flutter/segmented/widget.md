# Flutter SegmentedButton Widget 定义

## Widget 定义

Flutter Material Design 3 提供分段控件 `SegmentedButton<T>`(StatefulWidget),用于 2-5 项互斥(或多选)视图切换/筛选,介于 tabs 与 radio 之间。M3 原生组件,支持图标 + 文本与 `selectedIcon` 定制。

| Segmented 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 分段控件 | `SegmentedButton<T>` | `StatefulWidget` | M3 互斥/多选分段(`multiSelectionEnabled` 可多选) |
| iOS 风格 | `CupertinoSlidingSegmentedControl<T>` | `StatefulWidget` | iOS 滑动分段(Cupertino) |

## 构造函数

```dart
const SegmentedButton<T>({
  Key? key,
  required Set<T> segments,
  required Set<T> selected,
  ValueChanged<Set<T>>? onSelectionChanged,
  bool multiSelectionEnabled = false,
  bool emptySelectionAllowed = false,
  ButtonSegment<T>? Function(Set<T> selected)? showSelectedIcon,
  Widget? selectedIcon,
  Widget? unselectedIcon,
  TextStyle? style,
  BorderSide? side,
  BorderRadiusGeometry? borderRadius,
})
```

## ButtonSegment 定义

```dart
const ButtonSegment<T>({
  required T value,
  required Widget label,
  Widget? icon,
  Widget? avatar,
  bool enabled = true,
  ButtonSegment? tooltip,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `segments` | `Set<ButtonSegment<T>>` | 分段定义(value + label + icon) |
| `selected` | `Set<T>` | 当前选中值集合(互斥时长度 1) |
| `onSelectionChanged` | `ValueChanged<Set<T>>?` | 选中变化回调 |
| `multiSelectionEnabled` | `bool` | 多选模式(默认互斥) |
| `selectedIcon` | `Widget?` | 选中段前缀图标(默认 check) |
| `style` | `ButtonStyle?` | 覆盖主题样式 |

## 最小示例

```dart
import 'package:flutter/material.dart';

enum TrendRange { day, week, month }

/// SegmentedButton 最小示例:日/周/月互斥切换
class SegmentedSample extends StatefulWidget {
  const SegmentedSample({super.key});

  @override
  State<SegmentedSample> createState() => _SegmentedSampleState();
}

class _SegmentedSampleState extends State<SegmentedSample> {
  final Set<TrendRange> _selected = {TrendRange.week};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('数据趋势')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SegmentedButton<TrendRange>(
              segments: const [
                ButtonSegment(value: TrendRange.day, label: Text('日')),
                ButtonSegment(value: TrendRange.week, label: Text('周')),
                ButtonSegment(value: TrendRange.month, label: Text('月')),
              ],
              selected: _selected,
              onSelectionChanged: (s) => setState(() => _selected = s),
              style: SegmentedButton.styleFrom(
                selectedBackgroundColor: {color-primary},
                selectedForegroundColor: {color-text-inverse},
                backgroundColor: {color-bg-secondary},
                foregroundColor: {color-text-primary},
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 参考链接

- API 参考 - SegmentedButton: https://api.flutter.dev/flutter/material/SegmentedButton-class.html
- Material 3 - Segmented buttons: https://m3.material.io/components/segmented-buttons
