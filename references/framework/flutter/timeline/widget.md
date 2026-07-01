# Flutter Timeline Widget 定义

> **本框架无原生 Timeline Widget。**

## 占位说明

Flutter Material Design 3 **未提供名为 `Timeline` 的独立 Widget**。其他框架(Ant Design `Timeline`、Element `el-timeline`)中的时间线,在 Flutter 中通过以下方式实现:

| 其他框架的 Timeline 场景 | Flutter 对应实现 |
| --- | --- |
| 垂直时间线 | `Column` + `Row`(左侧圆点+线,右侧内容) |
| 横向时间线 | `Row` + `Column`(顶部圆点+线,底部内容) |
| 自定义样式时间线 | `CustomPaint` + 自定义绘制 |
| 第三方时间线 | `timeline_tile` 包(推荐) |
| 步骤式时间线 | `Stepper`(详见 `steps/widget.md`) |

## 推荐替代方案

### 1. 垂直时间线 → Column + Row

```dart
class TimelineItem {
  const TimelineItem({
    required this.title,
    required this.time,
    this.description,
    this.color,
  });
  final String title;
  final String time;
  final String? description;
  final Color? color;
}

class VerticalTimeline extends StatelessWidget {
  const VerticalTimeline({super.key, required this.items});

  final List<TimelineItem> items;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        for (int i = 0; i < items.length; i++)
          IntrinsicHeight(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // 左侧时间线轴(圆点 + 线)
                SizedBox(
                  width: {size-md},
                  child: Column(
                    children: [
                      Container(
                        width: {size-xs},
                        height: {size-xs},
                        decoration: BoxDecoration(
                          color: items[i].color ?? {color-primary},
                          shape: BoxShape.circle,
                        ),
                      ),
                      if (i < items.length - 1)
                        Expanded(
                          child: Container(
                            width: 1,
                            color: {color-outline-variant},
                          ),
                        ),
                    ],
                  ),
                ),
                SizedBox(width: {spacing-sm}),
                // 右侧内容
                Expanded(
                  child: Padding(
                    padding: EdgeInsets.only(bottom: {spacing-md}),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          items[i].time,
                          style: TextStyle(
                            fontSize: {font-size-xs},
                            color: {color-text-tertiary},
                          ),
                        ),
                        SizedBox(height: {spacing-xxs}),
                        Text(
                          items[i].title,
                          style: TextStyle(
                            fontSize: {font-size-md},
                            fontWeight: FontWeight.w600,
                            color: {color-text-primary},
                          ),
                        ),
                        if (items[i].description != null) ...[
                          SizedBox(height: {spacing-xxs}),
                          Text(
                            items[i].description!,
                            style: TextStyle(
                              fontSize: {font-size-sm},
                              color: {color-text-secondary},
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
      ],
    );
  }
}
```

### 2. 横向时间线 → Row + Column

```dart
class HorizontalTimeline extends StatelessWidget {
  const HorizontalTimeline({super.key, required this.items});

  final List<TimelineItem> items;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: {size-xl},
      child: Row(
        children: [
          for (int i = 0; i < items.length; i++) ...[
            // 圆点
            Container(
              width: {size-xs},
              height: {size-xs},
              decoration: BoxDecoration(
                color: items[i].color ?? {color-primary},
                shape: BoxShape.circle,
              ),
            ),
            // 连接线(非最后一项)
            if (i < items.length - 1)
              Expanded(
                child: Container(
                  height: 1,
                  color: {color-outline-variant},
                ),
              ),
          ],
        ],
      ),
    );
  }
}
```

### 3. 第三方包 timeline_tile(推荐)

`timeline_tile`(https://pub.flutter-io.cn/packages/timeline_tile)提供完整的时间线项能力:

```dart
import 'package:timeline_tile/timeline_tile.dart';

TimelineTile(
  alignment: TimelineAlign.manual,
  lineXY: 0.2,
  isFirst: true,
  indicatorStyle: IndicatorStyle(
    width: {size-sm},
    height: {size-sm},
    color: {color-primary},
    padding: EdgeInsets.all({spacing-xs}),
  ),
  beforeLineStyle: LineStyle(
    color: {color-outline-variant},
    thickness: 1,
  ),
  startChild: Text(
    '09:00',
    style: TextStyle(color: {color-text-tertiary}),
  ),
  endChild: Padding(
    padding: EdgeInsets.all({spacing-sm}),
    child: Text('事件内容', style: TextStyle(color: {color-text-primary})),
  ),
)
```

### 4. 步骤式时间线 → Stepper

若时间线表示流程步骤,使用 `Stepper`(详见 `steps/widget.md`):

```dart
Stepper(
  currentStep: _currentStep,
  onStepContinue: () => setState(() => _currentStep++),
  onStepCancel: () => setState(() => _currentStep--),
  steps: const [
    Step(title: Text('提交订单'), content: Text('订单已提交')),
    Step(title: Text('支付成功'), content: Text('支付完成')),
    Step(title: Text('已发货'), content: Text('商品已发货')),
  ],
)
```

> 注:示例中的 `{color-primary}`、`{color-outline-variant}`、`{color-text-primary}`、`{color-text-secondary}`、`{color-text-tertiary}`、`{spacing-xs}`、`{spacing-sm}`、`{spacing-md}`、`{size-xs}`、`{size-sm}`、`{size-md}`、`{size-xl}`、`{font-size-xs}`、`{font-size-sm}`、`{font-size-md}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Column: https://api.flutter.dev/flutter/widgets/Column-class.html
- API 参考 - Row: https://api.flutter.dev/flutter/widgets/Row-class.html
- API 参考 - CustomPaint: https://api.flutter.dev/flutter/widgets/CustomPaint-class.html
- API 参考 - Stepper: https://api.flutter.dev/flutter/material/Stepper-class.html
- pub.dev - timeline_tile: https://pub.flutter-io.cn/packages/timeline_tile
