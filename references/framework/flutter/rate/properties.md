# Flutter Rate 属性列表与默认值

本文档定义评分组合方案的规格参数与实现细节。所有颜色默认值以 design token 形式给出。

## 组合方案规格参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` / `rating` | `double` | `0` | 当前评分(支持 0.5 步进) |
| `max` / `stars` | `int` | `5` | 星星总数 |
| `stepSize` | `double` | `1.0` | 步长(0.5 = 半星) |
| `readOnly` | `bool` | `false` | 只读展示态(禁交互) |
| `allowHalf` | `bool` | `true` | 是否支持半星 |
| `starColor` | `Color` | `{color-warning}` | 已选星色(评分惯例黄/橙) |
| `emptyColor` | `Color` | `{color-bg-secondary}` | 空星色 |
| `size` | `double` | `24.0` | 星星尺寸(输入 28 / 展示 14-16) |
| `direction` | `Axis` | `horizontal` | 排列方向 |

## 三态图标映射

| 条件 | 图标 | 语义 |
| --- | --- | --- |
| `value >= i + 1` | `Icons.star` | 整星选中 |
| `value >= i + 0.5` | `Icons.star_half` | 半星 |
| 其余 | `Icons.star_border` | 空星 |

## flutter_rating_bar 关键参数(采用包时)

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `initialRating` | `double` | `0` | 初始评分 |
| `minRating` / `maxRating` | `double` | `0` / `5` | 范围 |
| `allowHalfRating` | `bool` | `true` | 半星 |
| `itemSize` | `double` | `40.0` | 单星尺寸 |
| `ratingWidget` | `RatingWidget` | 必填 | full/half/empty 三态图标 |
| `onRatingUpdate` | `ValueChanged<double>` | 必填 | 评分回调 |
| `ignoreGestures` | `bool` | `false` | 只读态 |

## 完整示例(输入 + 提交 + 只读)

```dart
import 'package:flutter/material.dart';

class RateFullSample extends StatefulWidget {
  const RateFullSample({super.key});

  @override
  State<RateFullSample> createState() => _RateFullSampleState();
}

class _RateFullSampleState extends State<RateFullSample> {
  double _input = 0;
  final double _display = 4.5;

  List<Widget> _stars(double value, {required bool interactive}) => [
        for (var i = 0; i < 5; i++)
          GestureDetector(
            onTap: interactive
                ? () => setState(() => _input = i + 1.0)
                : null,
            child: Icon(
              value >= i + 1
                  ? Icons.star
                  : value >= i + 0.5
                      ? Icons.star_half
                      : Icons.star_border,
              color: {color-warning},
              size: interactive ? 28 : 16,
            ),
          ),
      ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('评价')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          const Text('宝贝满足你的期待吗?'),
          Row(children: _stars(_input, interactive: true)),
          Text(_input == 0 ? '点击评分' : '评分:$_input',
              style: Theme.of(context).textTheme.bodySmall),
          const SizedBox(height: {spacing-md}),
          FilledButton(
            onPressed: _input > 0 ? () {} : null, // 零分不可提交
            child: const Text('提交评价'),
          ),
          const Divider(),
          // 商品详情只读展示(无分控评:0 分显示占位)
          if (_display > 0)
            Row(children: [
              ..._stars(_display, interactive: false),
              const SizedBox(width: {spacing-sm}),
              Text('$_display',
                  style: Theme.of(context).textTheme.bodySmall),
            ])
          else
            const Text('暂无评分',
                style: TextStyle(color: {color-text-secondary})),
        ],
      ),
    );
  }
}
```

## 注意事项

- **输入 vs 展示分开建模**:输入态可交互、星大(28);展示态 `GestureDetector.onTap: null` / `IgnorePointer`、星小(14-16)。
- 半星用 `Icons.star_half` 简化实现;需精确比例时用 `Stack` + `ClipRect` 按比例裁剪填充。
- 触控目标:输入态单星点击区 ≥44dp(星 28 + 外层 padding 补足)。
- 无障碍:`Semantics(label: '4.5 分,满分 5 分')` 包裹;输入态声明 `slider` 语义并支持键盘左右调节。
- 零分/无数据不渲染空星阵,用"暂无评分"占位(无分控评)。
- 采用 `flutter_rating_bar` 时注意其维护状态;新项目建议自组(仅 Row + Icon,无额外依赖)。
