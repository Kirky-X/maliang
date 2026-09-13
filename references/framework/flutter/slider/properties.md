# Flutter Slider 属性列表与默认值

本文档汇总 `Slider` 与 `RangeSlider` 的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出。

## Slider 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `double` | 必填 | 当前值 |
| `onChanged` | `ValueChanged<double>?` | 必填 | 拖动实时回调;`null` 时禁用 |
| `onChangeStart` | `ValueChanged<double>?` | `null` | 开始拖动回调 |
| `onChangeEnd` | `ValueChanged<double>?` | `null` | 松手回调(业务触发点) |
| `min` / `max` | `double` | `0.0` / `1.0` | 数值范围 |
| `divisions` | `int?` | `null`(连续) | 离散档数(设置后按档吸附) |
| `label` | `String?` | `null` | 拖动时值气泡文本 |
| `activeColor` | `Color?` | 取主题 | 已选轨道 + 滑块色,建议 `{color-primary}` |
| `inactiveColor` | `Color?` | 取主题 | 底轨色,建议 `{color-bg-secondary}` |
| `thumbColor` | `Color?` | 取主题 | 滑块圆点色 |
| `overlayColor` | `Color?` | 取主题 | 按压涟漪色 |
| `semanticFormatterCallback` | `SemanticFormatterCallback?` | `null` | 自定义读屏播报 |
| `focusNode` / `autofocus` | — | `null` / `false` | 焦点控制 |

## RangeSlider 构造参数(增量)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `values` | `RangeValues` | 必填 | 区间(start, end) |
| `onChanged` / `onChangeEnd` | `ValueChanged<RangeValues>?` | 必填/`null` | 区间拖动/松手回调 |
| `labels` | `RangeLabels?` | `null` | 双滑块气泡文本 |
| `divisions` | `int?` | `null` | 离散档数 |

## 三阶段回调语义

| 回调 | 触发时机 | 典型用途 |
| --- | --- | --- |
| `onChangeStart` | 手指按下 | 记录起始值/暂停播放 |
| `onChanged` | 拖动中持续 | 实时预览(文本/透明度) |
| `onChangeEnd` | 松手 | 业务请求/落库 |

## 完整示例(价格区间筛选)

```dart
import 'package:flutter/material.dart';

class RangeSliderSample extends StatefulWidget {
  const RangeSliderSample({super.key});

  @override
  State<RangeSliderSample> createState() => _RangeSliderSampleState();
}

class _RangeSliderSampleState extends State<RangeSliderSample> {
  RangeValues _price = const RangeValues(100, 900);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('价格区间')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('¥${_price.start.round()} - ¥${_price.end.round()}',
                style: Theme.of(context).textTheme.titleMedium),
            RangeSlider(
              values: _price,
              min: 0,
              max: 1000,
              divisions: 100,
              labels: RangeLabels(
                '¥${_price.start.round()}',
                '¥${_price.end.round()}',
              ),
              activeColor: {color-primary},
              onChanged: (v) => setState(() => _price = v),
              onChangeEnd: (v) {
                // 松手后触发筛选请求
              },
            ),
          ],
        ),
      ),
    );
  }
}
```

## 注意事项

- `value` 越出 `min`/`max` 会断言崩溃;数据回显前先 clamp。
- 连续滑块(无 `divisions`)不要用 `onChanged` 直接触发网络请求;用 `onChangeEnd`。
- 禁用态传 `onChanged: null`;视觉自动转灰,无需另设样式。
- 读屏:`semanticFormatterCallback` 自定义播报(如"音量 40%"),默认播报百分比。
- 触控目标:M3 滑块热区默认 48dp 高(满足无障碍);自定义 thumb 时不得缩到 24dp 以下热区。
- 语义分工:输入用 Slider;只读进度展示归 progress 类。
