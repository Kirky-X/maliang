# Flutter Shape Widget 定义

## Widget 定义

Flutter 自定义图形通过 `CustomPaint`(在 `Canvas` 上绘制)+ `CustomPainter`(绘制逻辑)实现。裁剪用 `CustomClipper`(配合 `ClipPath`)。形状边框用 `ShapeBorder`(如 `RoundedRectangleBorder`、`CircleBorder`)。

| Widget/类 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `CustomPaint` | `CustomPaint` | `SingleChildRenderObjectWidget` | 自定义绘制容器 |
| `CustomPainter` | `CustomPainter` | `Listenable` | 绘制逻辑(paint/shouldRepaint) |
| `CustomClipper` | `CustomClipper<T>` | `Listenable` | 裁剪路径 |
| `ClipPath` | `ClipPath` | `SingleChildRenderObjectWidget` | 按路径裁剪子节点 |
| `ClipRRect` | `ClipRRect` | `SingleChildRenderObjectWidget` | 圆角矩形裁剪 |
| `ClipOval` | `ClipOval` | `SingleChildRenderObjectWidget` | 椭圆裁剪 |
| `ShapeBorder` | `ShapeBorder` | - | 抽象形状边框 |
| `Canvas` | `Canvas` | - | 绘制画布 |

## 构造函数

### CustomPaint

```dart
const CustomPaint({
  super.key,
  CustomPainter? painter,        // 前景 painter(子节点之下绘制)
  CustomPainter? foregroundPainter, // 背景 painter(子节点之上绘制)
  Size size = Size.zero,          // 子节点为 null 时的尺寸
  bool isComplex = false,         // 提示复杂(启用缓存)
  bool willChange = false,        // 提示会变化
  Widget? child,                  // 子节点(可选)
})
```

### CustomPainter(抽象类,需继承)

```dart
abstract class CustomPainter extends Listenable {
  void paint(Canvas canvas, Size size);          // 绘制实现
  bool shouldRepaint(covariant CustomPainter oldDelegate); // 是否重绘
  SemanticsBuilderCallback? get semanticsBuilder;
  bool? hitTest(Offset position);
}
```

### CustomClipper(抽象类,需继承)

```dart
abstract class CustomClipper<T extends Path> extends Listenable {
  T getClip(Size size);            // 返回裁剪路径
  bool shouldReclip(covariant CustomClipper oldClipper);
  Rect getApproximateClipRect(Size size) => ...;
}
```

### ClipPath / ClipRRect / ClipOval

```dart
const ClipPath({
  super.key,
  required CustomClipper<Path> clipper,   // 或 Clip
  Clip clipBehavior = Clip.antiAlias,
  Widget? child,
})

const ClipRRect({
  super.key,
  required BorderRadius borderRadius,
  Clip clipBehavior = Clip.antiAlias,
  Widget? child,
})

const ClipOval({super.key, Clip clipBehavior = Clip.antiAlias, Widget? child})
```

### ShapeBorder 常用子类

```dart
RoundedRectangleBorder({BorderRadius borderRadius, BorderSide side})
CircleBorder({BorderSide side})
StadiumBorder({BorderSide side})            // 胶囊形
ContinuousRectangleBorder({BorderRadius, BorderSide}) // M3 连续圆角
BeveledRectangleBorder({BorderRadius, BorderSide})    // 斜角
```

## 核心属性

### CustomPaint 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `painter` | `CustomPainter?` | 前景 painter(子节点下方) |
| `foregroundPainter` | `CustomPainter?` | 背景 painter(子节点上方) |
| `size` | `Size` | 无 child 时的尺寸 |
| `isComplex` | `bool` | 提示复杂(启用层缓存) |
| `willChange` | `bool` | 提示会变化 |
| `child` | `Widget?` | 子节点 |

### ClipRRect 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `borderRadius` | `BorderRadius` | 圆角半径 |
| `clipBehavior` | `Clip` | 裁剪方式(none/hardEdge/antiAlias/antiAliasWithSaveLayer) |

## 最小示例

```dart
import 'package:flutter/material.dart';

class ShapeSample extends StatelessWidget {
  const ShapeSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Shape 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          children: [
            // 1. CustomPaint 绘制圆
            CustomPaint(
              size: const Size(100, 100),
              painter: CirclePainter(color: {color-primary}),
            ),
            const SizedBox(height: {spacing-md}),
            // 2. ClipRRect 圆角裁剪
            ClipRRect(
              borderRadius: BorderRadius.circular({radius-lg}),
              child: Container(
                width: 120, height: 80,
                color: {color-bg-secondary},
              ),
            ),
            const SizedBox(height: {spacing-md}),
            // 3. ClipOval 椭圆裁剪
            ClipOval(
              child: Container(
                width: 80, height: 80,
                color: {color-success},
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class CirclePainter extends CustomPainter {
  final Color color;
  const CirclePainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;
    canvas.drawCircle(size.center(Offset.zero), size.width / 2, paint);
  }

  @override
  bool shouldRepaint(covariant CirclePainter old) => old.color != color;
}
```

## 参考链接

- Flutter 官方文档 - 自定义图形: https://docs.flutter.cn/ui/design/graphics
- Flutter 官方文档 - 使用自定义的着色器: https://docs.flutter.cn/ui/design/graphics/fragment-shaders
- Widget 目录 - Painting: https://docs.flutter.cn/ui/widgets/painting
- API 参考 - CustomPaint: https://api.flutter.dev/flutter/widgets/CustomPaint-class.html
- API 参考 - CustomPainter: https://api.flutter.dev/flutter/rendering/CustomPainter-class.html
- API 参考 - Canvas: https://api.flutter.dev/flutter/dart-ui/Canvas-class.html
- API 参考 - ShapeBorder: https://api.flutter.dev/flutter/painting/ShapeBorder-class.html
