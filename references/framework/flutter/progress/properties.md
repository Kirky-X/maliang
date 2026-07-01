# Flutter Progress 属性列表与默认值

本文档汇总 `LinearProgressIndicator` / `CircularProgressIndicator` / `RefreshProgressIndicator` 的属性、默认值。颜色/尺寸默认值以 design token 形式给出。

## LinearProgressIndicator 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `double?` | `null`(不确定型) | 进度 0.0~1.0 |
| `color` | `Color?` | `null`(主题 primary) | 进度色 |
| `backgroundColor` | `Color?` | `null` | 轨道背景色 |
| `valueColor` | `Animation<double>?` | `null` | 颜色动画 |
| `minHeight` | `double?` | `4.0` | 最小高度(条厚度) |
| `borderRadius` | `BorderRadius?` | `null`(M3 默认圆角) | 圆角 |
| `semanticsLabel` | `String?` | `null` | 无障碍标签 |
| `semanticsValue` | `String?` | `null` | 无障碍值 |
| `year2023` | `int?` | `true` | M3 样式开关 |

## CircularProgressIndicator 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `double?` | `null`(不确定型) | 进度 0.0~1.0 |
| `color` | `Color?` | `null`(主题 primary) | 进度色 |
| `backgroundColor` | `Color?` | `null` | 轨道背景色 |
| `valueColor` | `Animation<double>?` | `null` | 颜色动画 |
| `strokeWidth` | `double` | `4.0` | 线条厚度 |
| `strokeAlign` | `double` | `1.0` | 线条对齐(0=center,-1=内,1=外) |
| `strokeCap` | `StrokeCap?` | `null` | 线条端点(round/butt/square) |
| `trackColor` | `Color?` | `null` | 轨道色(M3 别名) |
| `year2023` | `int?` | `true` | M3 样式开关 |
| `semanticsLabel` | `String?` | `null` | 无障碍标签 |
| `semanticsValue` | `String?` | `null` | 无障碍值 |

## RefreshProgressIndicator 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `color` | `Color?` | `null` | 颜色 |
| `backgroundColor` | `Color?` | `null` | 背景 |
| `valueColor` | `Animation<double>?` | `null` | 颜色动画 |
| `strokeWidth` | `double` | `2.5` | 线条厚度 |
| `semanticsLabel` | `String?` | `null` | 无障碍标签 |
| `semanticsValue` | `String?` | `null` | 无障碍值 |

## 确定型 vs 不确定型

| 模式 | `value` | 行为 |
| --- | --- | --- |
| 确定型 | `0.0~1.0` | 显示固定进度,无动画 |
| 不确定型 | `null` | 动画循环(无限滚动) |

## valueColor 用法

`valueColor` 接受 `Animation<double>`,常配合 `AlwaysStoppedAnimation<Color>` 固定颜色,或用 `ColorTween` 实现渐变:

```dart
// 固定颜色(等价于 color)
valueColor: const AlwaysStoppedAnimation<Color>({color-primary}),

// 随主题变化
valueColor: AlwaysStoppedAnimation<Color>(
    Theme.of(context).colorScheme.primary),

// 渐变(需 AnimationController)
valueColor: _controller.drive(
  ColorTween(begin: {color-info}, end: {color-success}),
)
```

## 完整示例

```dart
import 'package:flutter/material.dart';

class ProgressFullSample extends StatefulWidget {
  const ProgressFullSample({super.key});
  @override
  State<ProgressFullSample> createState() => _ProgressFullSampleState();
}

class _ProgressFullSampleState extends State<ProgressFullSample>
    with SingleTickerProviderStateMixin {
  double _value = 0.0;

  void _increase() => setState(() => _value = (_value + 0.1).clamp(0.0, 1.0));

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Progress 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 不确定型线性
          const Text('不确定型线性'),
          const LinearProgressIndicator(),
          const SizedBox(height: {spacing-md}),
          // 2. 确定型线性 + 圆角
          Text('进度: ${(_value * 100).toInt()}%'),
          LinearProgressIndicator(
            value: _value,
            minHeight: 12,
            borderRadius: BorderRadius.circular({radius-full}),
            color: {color-primary},
            backgroundColor: {color-bg-secondary},
            semanticsLabel: '加载进度',
            semanticsValue: '${(_value * 100).toInt()}%',
          ),
          const SizedBox(height: {spacing-md}),
          // 3. 不确定型环形
          const Center(child: CircularProgressIndicator()),
          const SizedBox(height: {spacing-md}),
          // 4. 确定型环形 + 自定义厚度/端点
          Center(
            child: CircularProgressIndicator(
              value: _value,
              strokeWidth: 8,
              strokeCap: StrokeCap.round,
              color: {color-success},
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 5. 颜色动画(渐变)
          Center(
            child: CircularProgressIndicator(
              value: _value,
              valueColor: AlwaysStoppedAnimation<Color>(
                _value < 0.5 ? {color-warning} : {color-success},
              ),
            ),
          ),
          const SizedBox(height: {spacing-lg}),
          FilledButton(
            onPressed: _increase,
            child: const Text('增加进度'),
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- `value` 必须在 [0.0, 1.0] 范围,超出会 clamp
- 不确定型(`value: null`)始终有动画,确定型无动画(除非用 AnimationController 驱动 value)
- `valueColor` 优先级高于 `color`;两者都为 null 时取主题 `colorScheme.primary`
- `CircularProgressIndicator` 默认尺寸 36×36,可用 `SizedBox` 包裹改变大小
- 下拉刷新用 `RefreshIndicator` 包裹 `ListView`,其内部用 `RefreshProgressIndicator`
- `strokeAlign: -1` 让线条向内(避免溢出),`1` 向外,`0` 居中
