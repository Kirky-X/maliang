# Flutter Timeline 属性列表与默认值

> **本框架无原生 Timeline Widget,以下为替代方案的属性汇总。**

## 占位说明

Flutter 不存在 `Timeline` 类。本文档汇总替代实现(`Column` + `Row` + `CustomPaint` + 第三方 `timeline_tile`)的关键属性,供设计 token 映射参考。

## 替代方案 1:Column + Row(垂直时间线)

### Column 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<Widget>` | 必填 | 子节点(每项为时间线条目) |
| `mainAxisAlignment` | `MainAxisAlignment` | `MainAxisAlignment.start` | 主轴对齐 |
| `mainAxisSize` | `MainAxisSize` | `MainAxisSize.max` | 主轴尺寸 |
| `crossAxisAlignment` | `CrossAxisAlignment` | `CrossAxisAlignment.center` | 交叉轴对齐 |
| `verticalDirection` | `VerticalDirection` | `VerticalDirection.down` | 垂直方向 |
| `textDirection` | `TextDirection?` | `null` | 文本方向 |
| `textBaseline` | `TextBaseline?` | `null` | 文本基线 |

### Row 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<Widget>` | 必填 | 子节点 |
| `mainAxisAlignment` | `MainAxisAlignment` | `MainAxisAlignment.start` | 主轴对齐 |
| `mainAxisSize` | `MainAxisSize` | `MainAxisSize.max` | 主轴尺寸 |
| `crossAxisAlignment` | `CrossAxisAlignment` | `CrossAxisAlignment.center` | 交叉轴对齐 |
| `verticalDirection` | `VerticalDirection` | `VerticalDirection.down` | 垂直方向 |
| `textDirection` | `TextDirection?` | `null` | 文本方向 |
| `textBaseline` | `TextBaseline?` | `null` | 文本基线 |

## 替代方案 2:CustomPaint(自定义绘制)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `painter` | `CustomPainter?` | `null` | 自定义绘制器 |
| `foregroundPainter` | `CustomPainter?` | `null` | 前景绘制器 |
| `size` | `Size` | `Size.zero` | 尺寸(默认 0,需父约束) |
| `isComplex` | `bool` | `false` | 是否复杂(缓存提示) |
| `willChange` | `bool` | `false` | 是否会变化 |
| `child` | `Widget?` | `null` | 子节点 |

### CustomPainter 抽象方法

| 方法 | 说明 |
| --- | --- |
| `void paint(Canvas canvas, Size size)` | 绘制 |
| `bool shouldRepaint(covariant CustomPainter oldDelegate)` | 是否需要重绘 |

## 替代方案 3:Stepper(步骤式时间线)

详见 `steps/properties.md`。核心属性:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `steps` | `List<Step>` | 必填 | 步骤列表 |
| `currentStep` | `int` | `0` | 当前步骤 |
| `onStepContinue` | `VoidCallback?` | `null` | 继续回调 |
| `onStepCancel` | `VoidCallback?` | `null` | 取消回调 |
| `onStepTapped` | `ValueChanged<int>?` | `null` | 点击步骤回调 |
| `type` | `StepperType` | `StepperType.vertical` | 类型(`vertical` / `horizontal`) |
| `physics` | `ScrollPhysics?` | `null` | 滚动物理 |

## 替代方案 4:timeline_tile 包

`timeline_tile`(https://pub.flutter-io.cn/packages/timeline_tile)提供 `TimelineTile`:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `alignment` | `TimelineAlign` | `TimelineAlign.center` | 轴位置(`start` / `center` / `manual`) |
| `lineXY` | `double` | `0.5`(center) | 轴横向位置(配合 `manual`) |
| `isFirst` | `bool` | `false` | 是否首项(隐藏上连线) |
| `isLast` | `bool` | `false` | 是否末项(隐藏下连线) |
| `indicatorStyle` | `IndicatorStyle` | `IndicatorStyle()` | 圆点样式 |
| `beforeLineStyle` | `LineStyle` | `LineStyle()` | 上连线样式 |
| `afterLineStyle` | `LineStyle` | `LineStyle()` | 下连线样式 |
| `startChild` | `Widget?` | `null` | 左/上子节点 |
| `endChild` | `Widget?` | `null` | 右/下子节点 |

### IndicatorStyle 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `width` | `double` | `12.0` | 圆点宽 |
| `height` | `double` | `12.0` | 圆点高 |
| `color` | `Color` | `Colors.blue` | 圆点颜色 |
| `padding` | `EdgeInsets` | `EdgeInsets.all(0)` | 内边距 |
| `indicator` | `Widget?` | `null` | 自定义圆点 Widget |
| `iconStyle` | `IconStyle?` | `null` | 图标样式 |
| `drawGap` | `bool` | `false` | 是否在圆点处断开连线 |

### LineStyle 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `color` | `Color` | `Colors.gray` | 线颜色 |
| `thickness` | `double` | `2.0` | 线宽 |

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 已完成节点圆点 | `{color-primary}` |
| 当前节点圆点 | `{color-primary}` |
| 未完成节点圆点 | `{color-surface-variant}` |
| 连接线 | `{color-outline-variant}` |
| 节点标题 | `{font-size-md}` / `{color-text-primary}` |
| 节点时间 | `{font-size-xs}` / `{color-text-tertiary}` |
| 节点描述 | `{font-size-sm}` / `{color-text-secondary}` |
| 节点间距 | `{spacing-md}` |
| 圆点尺寸 | `{size-xs}` |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Column: https://api.flutter.dev/flutter/widgets/Column-class.html
- API 参考 - Row: https://api.flutter.dev/flutter/widgets/Row-class.html
- API 参考 - CustomPaint: https://api.flutter.dev/flutter/widgets/CustomPaint-class.html
- API 参考 - Stepper: https://api.flutter.dev/flutter/material/Stepper-class.html
- pub.dev - timeline_tile: https://pub.flutter-io.cn/packages/timeline_tile
