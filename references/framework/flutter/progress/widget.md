# Flutter Progress Widget 定义

## Widget 定义

Flutter 进度指示器均为 `StatelessWidget`,分两类:**确定型**(已知进度,`value: 0.0~1.0`)与**不确定型**(无限循环动画,`value: null`)。`LinearProgressIndicator`(线性条)、`CircularProgressIndicator`(环形)、`RefreshProgressIndicator`(下拉刷新环)为 Material 实现。

| Widget | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `LinearProgressIndicator` | `LinearProgressIndicator` | `StatelessWidget` | 线性进度条 |
| `CircularProgressIndicator` | `CircularProgressIndicator` | `StatelessWidget` | 环形进度条 |
| `RefreshProgressIndicator` | `RefreshProgressIndicator` | `StatelessWidget` | 下拉刷新指示器 |

> 确定型与不确定型由 `value` 决定:`value == null` 为不确定型(动画循环),`value` 为 0.0~1.0 为确定型。

## 构造函数

### LinearProgressIndicator

```dart
const LinearProgressIndicator({
  super.key,
  double? value,                  // null=不确定型;0.0~1.0=确定型
  Color? backgroundColor,
  Color? color,
  Animation<double>? valueColor,  // 颜色动画(可随主题变化)
  double? minHeight,
  String? semanticsLabel,
  String? semanticsValue,
  int? year2023 = true,           // M3 样式开关
  BorderRadius? borderRadius,     // M3 圆角
})
```

### CircularProgressIndicator

```dart
const CircularProgressIndicator({
  super.key,
  double? value,
  Color? backgroundColor,
  Color? color,
  Animation<double>? valueColor,
  double strokeWidth = 4.0,        // 线条厚度
  String? semanticsLabel,
  String? semanticsValue,
  int? year2023 = true,
  double? trackColor,
})
```

### RefreshProgressIndicator

```dart
const RefreshProgressIndicator({
  super.key,
  Color? backgroundColor,
  Color? color,
  Animation<double>? valueColor,
  double strokeWidth = 2.5,
  String? semanticsLabel,
  String? semanticsValue,
})
```

## 核心属性

### 通用属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `value` | `double?` | 进度(0.0~1.0);null 为不确定型 |
| `color` | `Color?` | 进度颜色 |
| `backgroundColor` | `Color?` | 轨道背景色 |
| `valueColor` | `Animation<double>?` | 颜色动画(配合 `AlwaysStoppedAnimation` 或 `Tween`) |
| `semanticsLabel` | `String?` | 无障碍标签 |
| `semanticsValue` | `String?` | 无障碍进度值 |

### LinearProgressIndicator 专属

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `minHeight` | `double?` | `4.0` | 最小高度(条厚度) |
| `borderRadius` | `BorderRadius?` | `null` | 圆角(M3) |

### CircularProgressIndicator 专属

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `strokeWidth` | `double` | `4.0` | 线条厚度 |

## 最小示例

```dart
import 'package:flutter/material.dart';

class ProgressSample extends StatelessWidget {
  const ProgressSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Progress 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          children: [
            // 不确定型线性
            const LinearProgressIndicator(),
            const SizedBox(height: {spacing-md}),
            // 确定型线性(60%)
            LinearProgressIndicator(
              value: 0.6,
              minHeight: 8,
              borderRadius: BorderRadius.circular({radius-full}),
              color: {color-primary},
              backgroundColor: {color-bg-secondary},
            ),
            const SizedBox(height: {spacing-lg}),
            // 不确定型环形
            const CircularProgressIndicator(),
            const SizedBox(height: {spacing-md}),
            // 确定型环形(45%)
            CircularProgressIndicator(
              value: 0.45,
              strokeWidth: 6,
              color: {color-success},
            ),
          ],
        ),
      ),
    );
  }
}
```

## 动态进度(配合 AnimationController)

```dart
class DynamicProgress extends StatefulWidget {
  const DynamicProgress({super.key});
  @override
  State<DynamicProgress> createState() => _DynamicProgressState();
}

class _DynamicProgressState extends State<DynamicProgress>
    with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this, duration: const Duration(seconds: 3),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) =>
      CircularProgressIndicator(value: _ctrl.value);
}
```

## 参考链接

- Flutter 官方文档:无独立教程页(本 widget 在聚合页中介绍)
- Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- Widget 目录 - Async(加载态): https://docs.flutter.cn/ui/widgets/async
- API 参考 - LinearProgressIndicator: https://api.flutter.dev/flutter/material/LinearProgressIndicator-class.html
- API 参考 - CircularProgressIndicator: https://api.flutter.dev/flutter/material/CircularProgressIndicator-class.html
- API 参考 - RefreshProgressIndicator: https://api.flutter.dev/flutter/material/RefreshProgressIndicator-class.html
