# Flutter Rate Widget 定义

> **本组件为 maliang 组合方案,Flutter 无原生 Rate/评分 Widget。** 通过 `Row` + `Icon`(星星)+ `GestureDetector` 组合实现,或采用生态验证包(`flutter_rating_bar` / `flutter_rating`)。

## 缺失原因

Flutter Material 未提供星级评分 Widget(M3 无 Rating 组件);评分输入/展示由组合方案承担。

## 替代方案(组合结构)

| 角色 | Flutter 实现 |
| --- | --- |
| 星星阵 | `Row` + `Icon(Icons.star / star_half / star_border)` |
| 输入交互 | `GestureDetector`(整星点击)+ `MouseRegion`(悬停预览) |
| 半星 | `Icon(Icons.star_half)` 或 `Stack` 裁剪(`ClipRect` + `Align`) |
| 展示态(只读) | 纯 `Row` + `IgnorePointer` |
| 成熟包 | `flutter_rating_bar`(pub.dev 验证,支持半星/任意图标) |

## 核心 API(组合方案)

```dart
// 单颗星的三态映射
Icon(
  value >= i + 1
      ? Icons.star                 // 整星
      : value >= i + 0.5
          ? Icons.star_half        // 半星
          : Icons.star_border,     // 空星
  color: {color-warning},
  size: 24,
)
```

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Rate 最小示例:评分输入 + 只读展示
class RatingSample extends StatefulWidget {
  const RatingSample({super.key});

  @override
  State<RatingSample> createState() => _RatingSampleState();
}

class _RatingSampleState extends State<RatingSample> {
  double _score = 0;

  Widget _star(int index, {required bool interactive, VoidCallback? onTap}) {
    final v = _score;
    final icon = v >= index + 1
        ? Icons.star
        : v >= index + 0.5
            ? Icons.star_half
            : Icons.star_border;
    final star = Icon(icon, color: {color-warning}, size: 28);
    return interactive
        ? GestureDetector(onTap: onTap, child: star)
        : star;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('评分示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 输入态:整星点击
            Row(
              children: [
                for (var i = 0; i < 5; i++)
                  _star(i, interactive: true,
                      onTap: () => setState(() => _score = i + 1.0)),
              ],
            ),
            const SizedBox(height: {spacing-sm}),
            Text('评分:$_score',
                style: Theme.of(context).textTheme.bodySmall),
            const Divider(),
            // 展示态:只读
            Row(
              children: [
                for (var i = 0; i < 5; i++)
                  _star(4 - 4 + i, interactive: false),
                const SizedBox(width: {spacing-sm}),
                Text('4.5 (2.3 万条)',
                    style: Theme.of(context).textTheme.bodySmall),
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

- pub.dev - flutter_rating_bar: https://pub.dev/packages/flutter_rating_bar
- API 参考 - Icon: https://api.flutter.dev/flutter/widgets/Icon-class.html
- API 参考 - GestureDetector: https://api.flutter.dev/flutter/widgets/GestureDetector-class.html
