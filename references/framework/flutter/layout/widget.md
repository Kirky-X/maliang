# Flutter Layout Widget 定义

## Widget 定义

Flutter 布局 Widget 用于在二维空间中排列子节点。核心分为线性布局(Flex 系列)、层叠布局(Stack)、单子节点容器(Container/Padding/Align/Center/SizedBox)和撑开/占据空间(Expanded/Flexible/Spacer)。所有布局 Widget 均为 `RenderObjectWidget` 子类,通过 `RenderBox` 协议测量与布局。

| 分类 | 代表 Widget | 基类 | 用途 |
| --- | --- | --- | --- |
| 线性布局 | `Row` / `Column` / `Flex` | `Flex` | 水平/垂直排列子节点 |
| 弹性空间 | `Expanded` / `Flexible` / `Spacer` | `ParentDataWidget<FlexParentData>` | 在 Flex 中分配剩余空间 |
| 层叠布局 | `Stack` / `IndexedStack` | `MultiChildRenderObjectWidget` | 子节点沿 Z 轴堆叠 |
| 对齐定位 | `Align` / `Center` | `SingleChildRenderObjectWidget` | 单子节点对齐 |
| 间距 | `Padding` / `SizedBox` | `SingleChildRenderObjectWidget` | 内边距/固定尺寸占位 |
| 容器 | `Container` | `StatelessWidget` | 组合装饰/变换/尺寸的便利容器 |
| 约束 | `ConstrainedBox` / `AspectRatio` / `FractionallySizedBox` | `SingleChildRenderObjectWidget` | 约束子节点尺寸 |

## 构造函数

### Row / Column

```dart
const Row({
  super.key,
  MainAxisAlignment mainAxisAlignment = MainAxisAlignment.start,
  MainAxisSize mainAxisSize = MainAxisSize.max,
  CrossAxisAlignment crossAxisAlignment = CrossAxisAlignment.center,
  TextDirection? textDirection,
  VerticalDirection verticalDirection = VerticalDirection.down,
  TextBaseline? textBaseline,
  List<Widget> children = const <Widget>[],
})
// Column 构造参数与 Row 一致,仅主轴方向不同
```

### Stack

```dart
const Stack({
  super.key,
  AlignmentGeometry alignment = AlignmentDirectional.topStart,
  TextDirection? textDirection,
  StackFit fit = StackFit.loose,
  Clip clipBehavior = Clip.hardEdge,
  List<Widget> children = const <Widget>[],
})
```

### Container

```dart
Container({
  super.key,
  AlignmentGeometry? alignment,
  EdgeInsetsGeometry? padding,
  Color? color,
  Decoration? decoration,
  Decoration? foregroundDecoration,
  double? width, double? height,
  BoxConstraints? constraints,
  EdgeInsetsGeometry? margin,
  Matrix4? transform,
  AlignmentGeometry? transformAlignment,
  Widget? child,
  Clip clipBehavior = Clip.none,
})
```

### Padding / SizedBox / Align

```dart
const Padding({super.key, required EdgeInsetsGeometry padding, Widget? child})
const SizedBox({super.key, double? width, double? height, Widget? child})
const Align({super.key, AlignmentGeometry alignment = Alignment.center,
  double? widthFactor, double? heightFactor, Widget? child})
```

### Expanded / Flexible

```dart
const Expanded({super.key, required int flex, Widget? child})
const Flexible({super.key, required int flex, FlexFit fit = FlexFit.loose, Widget? child})
```

## 核心属性

### Flex(Row/Column)属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `mainAxisAlignment` | `MainAxisAlignment` | 主轴对齐(start/center/end/spaceBetween/spaceAround/spaceEvenly) |
| `crossAxisAlignment` | `CrossAxisAlignment` | 交叉轴对齐 |
| `mainAxisSize` | `MainAxisSize` | 主轴尺寸(max/min) |
| `textDirection` | `TextDirection?` | 文本方向(LTR/RTL) |
| `verticalDirection` | `VerticalDirection` | 垂直方向(up/down) |
| `children` | `List<Widget>` | 子节点列表 |

### Stack 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `alignment` | `AlignmentGeometry` | 默认对齐(子节点未用 Positioned 时) |
| `fit` | `StackFit` | 子节点约束(loose/expand/passthrough) |
| `clipBehavior` | `Clip` | 超出边界裁剪,默认 `Clip.hardEdge` |

## 最小示例

```dart
import 'package:flutter/material.dart';

class LayoutSample extends StatelessWidget {
  const LayoutSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Layout 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Row + Expanded 弹性分配
            Row(
              children: [
                Expanded(flex: 2, child: _box('2')),
                const SizedBox(width: {spacing-sm}),
                Expanded(flex: 1, child: _box('1')),
              ],
            ),
            const SizedBox(height: {spacing-md}),
            // Stack 层叠
            SizedBox(
              height: 80,
              child: Stack(
                children: [
                  Container(color: {color-bg-secondary}),
                  const Positioned(
                    right: {spacing-sm},
                    top: {spacing-sm},
                    child: Text('右上角'),
                  ),
                ],
              ),
            ),
            const SizedBox(height: {spacing-md}),
            // Center + SizedBox 居中固定尺寸
            Center(
              child: SizedBox(
                width: 120, height: 40,
                child: Container(
                  color: {color-primary},
                  alignment: Alignment.center,
                  child: Text('居中',
                    style: TextStyle(color: {color-text-on-primary})),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _box(String label) => Container(
        height: 40,
        color: {color-primary},
        alignment: Alignment.center,
        child: Text(label,
            style: TextStyle(color: {color-text-on-primary})),
      );
}
```

## 参考链接

- Flutter 官方文档 - 布局: https://docs.flutter.cn/ui/layout
- Flutter 官方文档 - 构建布局教程: https://docs.flutter.cn/ui/layout/tutorial
- Widget 目录 - Layout: https://docs.flutter.cn/ui/widgets/layout
- API 参考 - Row: https://api.flutter.dev/flutter/widgets/Row-class.html
- API 参考 - Column: https://api.flutter.dev/flutter/widgets/Column-class.html
- API 参考 - Stack: https://api.flutter.dev/flutter/widgets/Stack-class.html
- API 参考 - Container: https://api.flutter.dev/flutter/widgets/Container-class.html
