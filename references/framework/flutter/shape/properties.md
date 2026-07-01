# Flutter Shape 属性列表与默认值

本文档汇总 `CustomPaint` / `CustomPainter` / `CustomClipper` / `ShapeBorder` 的属性、默认值与回调。

## CustomPaint 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `painter` | `CustomPainter?` | `null` | 前景 painter(子节点下方) |
| `foregroundPainter` | `CustomPainter?` | `null` | 背景 painter(子节点上方) |
| `size` | `Size` | `Size.zero` | 无 child 时尺寸 |
| `isComplex` | `bool` | `false` | 提示复杂(启用层缓存) |
| `willChange` | `bool` | `false` | 提示会变化 |
| `child` | `Widget?` | `null` | 子节点 |

## CustomPainter 抽象方法

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `paint` | `void paint(Canvas canvas, Size size)` | 绘制实现 |
| `shouldRepaint` | `bool shouldRepaint(covariant CustomPainter oldDelegate)` | 是否需要重绘 |
| `semanticsBuilder` | `SemanticsBuilderCallback? get` | 语义构建(可访问性) |
| `hitTest` | `bool? hitTest(Offset position)` | 点击测试 |

## Canvas 常用绘制方法

| 方法 | 说明 |
| --- | --- |
| `drawLine(Offset, Offset, Paint)` | 画线 |
| `drawRect(Rect, Paint)` | 画矩形 |
| `drawCircle(Offset, double, Paint)` | 画圆 |
| `drawOval(Rect, Paint)` | 画椭圆 |
| `drawPath(Path, Paint)` | 画路径 |
| `drawArc(Rect, double, double, bool, Paint)` | 画弧 |
| `drawText(TextSpan, Offset)` | 画文本(需 TextPainter) |
| `drawImage(Image, Offset, Paint)` | 画图片 |
| `clipPath(Path)` | 裁剪路径 |
| `save()` / `restore()` | 保存/恢复状态 |
| `translate(double, double)` | 平移 |
| `rotate(double)` | 旋转 |
| `scale(double)` | 缩放 |

## Paint 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `color` | `Color` | `Color(0xFF000000)` | 颜色 |
| `style` | `PaintingStyle` | `PaintingStyle.fill` | fill/stroke |
| `strokeWidth` | `double` | `0.0` | 线宽 |
| `strokeCap` | `StrokeCap` | `StrokeCap.butt` | 线端点 |
| `strokeJoin` | `StrokeJoin` | `StrokeJoin.miter` | 线连接 |
| `blendMode` | `BlendMode` | `BlendMode.srcOver` | 混合模式 |
| `shader` | `Shader?` | `null` | 着色器(渐变/图片) |
| `maskFilter` | `MaskFilter?` | `null` | 滤镜(模糊) |
| `isAntiAlias` | `bool` | `true` | 抗锯齿 |

## Clip 取值

| 取值 | 行为 |
| --- | --- |
| `Clip.none` | 不裁剪 |
| `Clip.hardEdge` | 硬边裁剪(最快,无抗锯齿) |
| `Clip.antiAlias` | 抗锯齿裁剪(默认,推荐) |
| `Clip.antiAliasWithSaveLayer` | 抗锯齿 + 独立层(最慢,精确保真) |

## ShapeBorder 子类属性

### RoundedRectangleBorder

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `borderRadius` | `BorderRadius` | `BorderRadius.zero` | 圆角 |
| `side` | `BorderSide` | `BorderSide.none` | 边框 |

### CircleBorder

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `side` | `BorderSide` | `BorderSide.none` | 边框 |
| `eccentricity` | `double` | `0.0` | 偏心率(0=圆,1=椭圆) |

### StadiumBorder

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `side` | `BorderSide` | `BorderSide.none` | 边框 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class ShapeFullSample extends StatelessWidget {
  const ShapeFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Shape 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. CustomPaint 绘制饼图
          CustomPaint(
            size: const Size(120, 120),
            painter: PieChartPainter(progress: 0.65),
          ),
          const SizedBox(height: {spacing-md}),
          // 2. CustomPaint 绘制虚线
          CustomPaint(
            size: const Size(double.infinity, 20),
            painter: DashedLinePainter(color: {color-border-default}),
          ),
          const SizedBox(height: {spacing-md}),
          // 3. ClipPath 自定义形状裁剪
          ClipPath(
            clipper: const TicketClipper(),
            child: Container(
              height: 80,
              color: {color-primary},
              alignment: Alignment.center,
              child: Text('票根',
                  style: TextStyle(color: {color-text-on-primary})),
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 4. ShapeBorder(用于 Material/Card)
          Container(
            width: 100, height: 100,
            decoration: ShapeDecoration(
              color: {color-bg-secondary},
              shape: const CircleBorder(),
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 5. StadiumBorder 胶囊形
          Container(
            padding: const EdgeInsets.symmetric(
                horizontal: {spacing-md}, vertical: {spacing-sm}),
            decoration: ShapeDecoration(
              color: {color-primary},
              shape: const StadiumBorder(),
            ),
            child: Text('胶囊',
                style: TextStyle(color: {color-text-on-primary})),
          ),
        ],
      ),
    );
  }
}

class PieChartPainter extends CustomPainter {
  final double progress;
  const PieChartPainter({required this.progress});

  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    final radius = size.width / 2;
    // 背景圆
    canvas.drawCircle(center, radius, Paint()..color = {color-bg-secondary});
    // 进度弧
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -pi / 2, // 从顶部开始
      2 * pi * progress,
      true,
      Paint()..color = {color-primary}..style = PaintingStyle.fill,
    );
  }

  @override
  bool shouldRepaint(covariant PieChartPainter old) =>
      old.progress != progress;
}

class DashedLinePainter extends CustomPainter {
  final Color color;
  const DashedLinePainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    const dashWidth = 5.0, dashSpace = 5.0;
    final paint = Paint()
      ..color = color
      ..strokeWidth = 2;
    double startX = 0;
    while (startX < size.width) {
      canvas.drawLine(
          Offset(startX, size.height / 2),
          Offset(startX + dashWidth, size.height / 2),
          paint);
      startX += dashWidth + dashSpace;
    }
  }

  @override
  bool shouldRepaint(covariant DashedLinePainter old) => old.color != color;
}

class TicketClipper extends CustomClipper<Path> {
  const TicketClipper();

  @override
  Path getClip(Size size) {
    final path = Path();
    final r = 10.0;
    path.lineTo(size.width, 0);
    path.lineTo(size.width, size.height / 2 - r);
    path.arcToPoint(Offset(size.width, size.height / 2 + r),
        radius: Radius.circular(r), clockwise: false);
    path.lineTo(size.width, size.height);
    path.lineTo(0, size.height);
    path.lineTo(0, size.height / 2 + r);
    path.arcToPoint(Offset(0, size.height / 2 - r),
        radius: Radius.circular(r), clockwise: false);
    path.close();
    return path;
  }

  @override
  bool shouldReclip(covariant TicketClipper old) => false;
}
```

## 注意事项

- `shouldRepaint` 返回 `false` 可避免不必要重绘,性能优化关键
- `isComplex: true` + `willChange: false` 启用光栅层缓存,复杂图形大幅提升性能
- `Clip.antiAliasWithSaveLayer` 性能开销大,仅在需要透明度保真时使用
- `CustomPainter` 中颜色随主题变化时,应在 `shouldRepaint` 比较颜色,或用 `repaint` 监听 `Animation`
- `Path` 是绘制复杂图形的核心,支持 `moveTo`/`lineTo`/`arcTo`/`cubicTo`/`quadraticBezierTo`
- `ShapeDecoration` 比 `BoxDecoration` 更通用(支持任意 `ShapeBorder`)
- 自定义着色器(Fragment Shaders)需 `.frag` 文件 + pubspec 配置,见官方文档
