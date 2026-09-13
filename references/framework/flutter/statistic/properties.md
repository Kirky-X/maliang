# Flutter Statistic 属性列表与默认值

本文档定义统计/描述组合方案的规格参数与实现细节。所有颜色默认值以 design token 形式给出。

## 组合方案规格参数(statistic)

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `title` | `String` | — | 标签文字(small,次要色) |
| `value` | `String` | 必填 | 数值(含千分位/货币前缀) |
| `precision` | `int` | `0` | 小数位(金额 2) |
| `delta` | `double?` | `null` | 环比变化(正负驱动箭头与色) |
| `deltaPrecision` | `String` | `'%'` | delta 单位后缀 |
| `valueStyle` | `TextStyle` | `headlineMedium + bold` | 数值样式(28-32 粗体) |
| `tabularFigures` | `bool` | `true` | 数字等宽(`FontFeature.tabularFigures()`) |
| `deltaColorUp` / `deltaColorDown` | `Color` | `{color-success}` / `{color-error}` | 涨跌色(按业务可调换) |

## 组合方案规格参数(descriptions)

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `items` | `List<(String, String)>` | 必填 | 键值对列表 |
| `labelWidth` | `double` | `0.32 * 宽` | 键列宽占比(32%-40%) |
| `bordered` | `bool` | `false` | 键列底色分块(表格式) |
| `column` | `int` | `1` | 列数(宽表 2) |
| `valueStyle` | `TextStyle` | `bodyMedium` | 值样式(可换行) |

## delta 方向语义

| delta 值 | 箭头 | 默认色 | 业务调换示例 |
| --- | --- | --- | --- |
| `> 0` | `↑`(Icons.arrow_upward) | `{color-success}` | GMV 涨=好;退款涨=改 `{color-error}` |
| `< 0` | `↓`(Icons.arrow_downward) | `{color-error}` | 同上反向 |
| `== 0` | `—` | 次要色 | 持平 |

## 完整示例(KPI 卡 + 订单键值对)

```dart
import 'package:flutter/material.dart';
import 'dart:ui' show FontFeature;

class StatisticFullSample extends StatelessWidget {
  const StatisticFullSample({super.key});

  Widget _kpi(BuildContext context, String title, String value, double? delta) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title,
            style: const TextStyle(
                fontSize: 13, color: {color-text-secondary})),
        Row(
          crossAxisAlignment: CrossAxisAlignment.baseline,
          textBaseline: TextBaseline.alphabetic,
          children: [
            Text(value,
                style: Theme.of(context).textTheme.headlineMedium!.copyWith(
                      fontWeight: FontWeight.bold,
                      fontFeatures: const [FontFeature.tabularFigures()],
                    )),
            if (delta != null) ...[
              const SizedBox(width: {spacing-sm}),
              Text(
                '${delta >= 0 ? '↑' : '↓'} ${delta.abs().toStringAsFixed(1)}%',
                style: TextStyle(
                  fontSize: 12,
                  color: delta >= 0 ? {color-success} : {color-error},
                ),
              ),
            ],
          ],
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final order = const [
      ('订单编号', 'SO-20260908-001'),
      ('下单时间', '2026-09-08 14:32'),
      ('支付方式', '微信支付'),
      ('配送地址', '上海市浦东新区xx路 88 号'),
    ];
    return Scaffold(
      appBar: AppBar(title: const Text('订单详情')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          Row(
            children: [
              Expanded(child: _kpi(context, '订单金额', '¥2,180', 3.1)),
              Expanded(child: _kpi(context, '退款金额', '¥0.00', null)),
            ],
          ),
          const Divider(height: {spacing-lg} * 2),
          const Text('订单信息',
              style: TextStyle(fontWeight: FontWeight.w600)),
          for (final (k, v) in order)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(
                    width: 96,
                    child: Text(k,
                        style: const TextStyle(
                            fontSize: 13, color: {color-text-secondary})),
                  ),
                  Expanded(
                    child: Text(v,
                        style: Theme.of(context).textTheme.bodyMedium),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
```

## 注意事项

- **数字等宽必须开**:`FontFeature.tabularFigures()`,实时刷新数值不跳动(对齐 data-dense-dashboard 模板)。
- **delta 带词不裸箭头**:读屏播报"涨 12.4%",箭头仅视觉增强。
- 键值对长值自动换行:`crossAxisAlignment: start`,键列定宽不破列。
- 数值字号 28-32 + Bold 为 KPI 档;行内统计 18-20 即可,不层层放大。
- 无障碍:读屏顺序"标签 → 值 → delta";`Semantics` 合并整卡避免碎片化播报。
- 语义分工:KPI 卡容器用 card 类;目标完成度用 progress 类;本类只管数值与键值排版。
