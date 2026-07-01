# Flutter Skeleton Widget 定义

> **本框架无原生 Skeleton Widget。**

## 占位说明

Flutter Material Design 3 **未提供名为 `Skeleton` / `SkeletonItem` 的独立 Widget**。其他框架(Ant Design `Skeleton`、Element `el-skeleton`)中的骨架屏,在 Flutter 中通过以下方式实现:

| 其他框架的 Skeleton 场景 | Flutter 对应实现 |
| --- | --- |
| 文本块占位 | `Container` + 灰色背景 + `Shimmer` 动画 |
| 头像占位 | `CircleAvatar` + 灰色背景 + `Shimmer` |
| 卡片占位 | `Card` + 灰色 `Container` 子项 + `Shimmer` |
| 图片占位 | `Container` + 灰色背景 + `Shimmer`(可配合 `FadeInImage`) |
| 列表项占位 | `ListView` + 上述组合 |

## 推荐替代方案

### 1. shimmer 第三方包(官方推荐)

`shimmer` 包(https://pub.flutter-io.cn/packages/shimmer)是 Flutter 团队维护的骨架屏动画包。

```dart
import 'package:shimmer/shimmer.dart';

SizedBox(
  width: {size-md},
  height: {size-sm},
  child: Shimmer.fromColors(
    baseColor: {color-surface-variant},
    highlightColor: {color-surface},
    child: Container(
      decoration: BoxDecoration(
        color: {color-surface-variant},
        borderRadius: BorderRadius.circular({radius-sm}),
      ),
    ),
  ),
)
```

### 2. 自定义 Skeleton Widget(基于 AnimatedBuilder)

```dart
class SkeletonBox extends StatefulWidget {
  const SkeletonBox({
    super.key,
    this.width = double.infinity,
    this.height = {size-sm},
    this.borderRadius = const Radius.circular({radius-sm}),
  });

  final double width;
  final double height;
  final Radius borderRadius;

  @override
  State<SkeletonBox> createState() => _SkeletonBoxState();
}

class _SkeletonBoxState extends State<SkeletonBox>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 1000),
  )..repeat(reverse: true);

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (_, __) => Container(
        width: widget.width,
        height: widget.height,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.all(widget.borderRadius),
          color: Color.lerp(
            {color-surface-variant},
            {color-surface},
            _controller.value,
          ),
        ),
      ),
    );
  }
}
```

### 3. 完整骨架屏列表

```dart
ListView.builder(
  itemCount: 5,
  itemBuilder: (_, __) => Card(
    child: Padding(
      padding: const EdgeInsets.all({spacing-md}),
      child: Row(
        children: [
          SkeletonBox(
            width: {size-lg},
            height: {size-lg},
            borderRadius: Radius.circular({radius-full}),
          ),
          const SizedBox(width: {spacing-md}),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SkeletonBox(height: {size-sm}),
                const SizedBox(height: {spacing-sm}),
                SkeletonBox(height: {size-sm}, width: 200),
              ],
            ),
          ),
        ],
      ),
    ),
  ),
)
```

> 注:示例中的 `{color-surface}`、`{color-surface-variant}`、`{spacing-md}`、`{size-sm}`、`{radius-sm}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- pub.dev - shimmer: https://pub.flutter-io.cn/packages/shimmer
- API 参考 - AnimatedBuilder: https://api.flutter.dev/flutter/widgets/AnimatedBuilder-class.html
- API 参考 - AnimationController: https://api.flutter.dev/flutter/animation/AnimationController-class.html
