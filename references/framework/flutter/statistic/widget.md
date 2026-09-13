# Flutter Statistic Widget 定义

> **本组件为 maliang 组合方案,Flutter 无原生 Statistic(统计数值)/ Descriptions(键值对详情)Widget。** 通过 `Text` + `Column`/`Table` 组合实现轻量数据展示。

## 缺失原因

Flutter Material 未提供统计值/描述列表组件;数值强调与键值对详情属于排版组合,由基础 Widget 表达。

## 替代方案(组合结构)

| 角色 | Flutter 实现 |
| --- | --- |
| 统计值(statistic) | `Column`:`Text` 标题(small)+ `Text` 数值(28-32 粗体)+ `Text` delta |
| delta 胶囊 | `Container` + `Row`(箭头图标 + 百分比) |
| 键值对(descriptions) | `Column` + `Row`(键 32-40% 宽 + 值 Expanded)或 `Table` |
| 数字等宽 | `FontFeature.tabularFigures()`(`TextStyle.fontFeatures`) |

## 核心 API(组合方案)

```dart
Text('¥128,460',
  style: Theme.of(context).textTheme.headlineMedium!.copyWith(
    fontWeight: FontWeight.bold,
    fontFeatures: const [FontFeature.tabularFigures()], // 数字等宽
  ),
)
```

## 最小示例

```dart
import 'package:flutter/material.dart';
import 'dart:ui' show FontFeature;

/// Statistic 最小示例:KPI 统计 + delta
class StatisticSample extends StatelessWidget {
  const StatisticSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('经营概况')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('今日 GMV',
                style: TextStyle(color: {color-text-secondary}, fontSize: 13)),
            Row(
              crossAxisAlignment: CrossAxisAlignment.baseline,
              textBaseline: TextBaseline.alphabetic,
              children: [
                Text('¥128,460',
                    style: Theme.of(context).textTheme.headlineMedium!.copyWith(
                          fontWeight: FontWeight.bold,
                          fontFeatures: const [FontFeature.tabularFigures()],
                        )),
                const SizedBox(width: {spacing-sm}),
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: {color-bg-secondary},
                    borderRadius: BorderRadius.circular({radius-sm}),
                  ),
                  child: const Text('↑ 12.4%',
                      style: TextStyle(
                          fontSize: 12, color: {color-success})),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

## 参考链接

- API 参考 - FontFeature: https://api.flutter.dev/flutter/dart-ui/FontFeature-class.html
- API 参考 - Table: https://api.flutter.dev/flutter/widgets/Table-class.html
- Element Plus Statistic(对照系): https://element-plus.org/zh-CN/component/statistic
