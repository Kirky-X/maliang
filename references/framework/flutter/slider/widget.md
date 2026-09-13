# Flutter Slider Widget 定义

## Widget 定义

Flutter Material Design 3 提供滑块 `Slider`(连续/离散)与区间滑块 `RangeSlider`(原生双滑块),用于数值/区间录入。M3 版本滑块带 `inactiveColor`/`activeColor` 分轨与数值气泡(`label`)。

| Slider 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 单滑块 | `Slider` | `StatefulWidget` | 连续/离散数值选择(M3) |
| 区间滑块 | `RangeSlider` | `StatefulWidget` | 原生双滑块区间(价格/时间范围) |
| iOS 风格 | `CupertinoSlider` | `StatelessWidget` | iOS 视觉滑块 |

## 构造函数

### Slider

```dart
const Slider({
  Key? key,
  required double value,
  required ValueChanged<double>? onChanged,
  ValueChanged<double>? onChangeStart,
  ValueChanged<double>? onChangeEnd,
  double min = 0.0,
  double max = 1.0,
  int? divisions,
  String? label,
  Color? activeColor,
  Color? inactiveColor,
  Color? thumbColor,
  Color? overlayColor,
  MouseCursor? mouseCursor,
  SemanticFormatterCallback? semanticFormatterCallback,
  FocusNode? focusNode,
  bool autofocus = false,
})
```

### RangeSlider

```dart
const RangeSlider({
  Key? key,
  required RangeValues values,
  required ValueChanged<RangeValues>? onChanged,
  ValueChanged<RangeValues>? onChangeStart,
  ValueChanged<RangeValues>? onChangeEnd,
  double min = 0.0,
  double max = 1.0,
  int? divisions,
  RangeLabels? labels,
  Color? activeColor,
  Color? inactiveColor,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `value` / `values` | `double` / `RangeValues` | 当前值/区间(start-end) |
| `onChanged` | `ValueChanged<...>?` | 拖动实时回调;`null` 时禁用 |
| `onChangeEnd` | `ValueChanged<...>?` | 松手回调(业务触发点) |
| `min` / `max` | `double` | 范围(默认 0.0-1.0) |
| `divisions` | `int?` | 离散档数(连续滑块不设) |
| `label` / `labels` | `String?` / `RangeLabels?` | 拖动气泡文本 |
| `activeColor` / `inactiveColor` | `Color?` | 已选轨/底轨颜色 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Slider 最小示例:连续滑块 + 离散档位
class SliderSample extends StatefulWidget {
  const SliderSample({super.key});

  @override
  State<SliderSample> createState() => _SliderSampleState();
}

class _SliderSampleState extends State<SliderSample> {
  double _volume = 40;
  int _level = 2;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Slider 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          children: [
            Text('音量:${_volume.round()}%',
                style: Theme.of(context).textTheme.bodyMedium),
            Slider(
              value: _volume,
              min: 0,
              max: 100,
              label: '${_volume.round()}%',
              activeColor: {color-primary},
              onChanged: (v) => setState(() => _volume = v),
            ),
            const SizedBox(height: {spacing-md}),
            Text('档位:$_level'),
            Slider(
              value: _level.toDouble(),
              min: 0,
              max: 3,
              divisions: 3, // 离散 4 档
              label: '$_level',
              activeColor: {color-primary},
              onChanged: (v) => setState(() => _level = v.round()),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 参考链接

- API 参考 - Slider: https://api.flutter.dev/flutter/material/Slider-class.html
- API 参考 - RangeSlider: https://api.flutter.dev/flutter/material/RangeSlider-class.html
- Material 3 - Slider: https://m3.material.io/components/slider
