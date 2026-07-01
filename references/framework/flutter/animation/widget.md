# Flutter Animation Widget 定义

## Widget 定义

Flutter 动画分三类:**显式动画**(用 `AnimationController` 驱动,精确控制)、**隐式动画**(`AnimatedXxx` 系列,自动过渡属性变化)、**转场动画**(`Hero` 共享元素、`PageTransition` 等)。核心类 `Animation<T>` 是值随时间变化的可监听对象。

| Widget/类 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `AnimationController` | `AnimationController` | `Animation<double>` | 显式动画控制器 |
| `Animation<T>` | `Animation<T>` | `Listenable` | 抽象动画值 |
| `Tween<T>` | `Tween<T>` | - | 值映射(开始→结束) |
| `AnimatedBuilder` | `AnimatedBuilder` | `StatelessWidget` | 监听 Animation 重建 |
| `AnimatedWidget` | `AnimatedWidget` | `StatefulWidget` | 动画 Widget 基类 |
| `AnimatedContainer` | `AnimatedContainer` | `ImplicitlyAnimatedWidget` | 隐式动画容器 |
| `AnimatedOpacity` | `AnimatedOpacity` | `ImplicitlyAnimatedWidget` | 隐式透明度动画 |
| `AnimatedAlign` | `AnimatedAlign` | `ImplicitlyAnimatedWidget` | 隐式对齐动画 |
| `ImplicitlyAnimatedWidget` | `ImplicitlyAnimatedWidget` | `StatefulWidget` | 隐式动画基类 |
| `Hero` | `Hero` | `StatefulWidget` | 跨页面共享元素动画 |
| `TweenAnimationBuilder` | `TweenAnimationBuilder` | `ImplicitlyAnimatedWidget` | 通用隐式动画 |

## 构造函数

### AnimationController

```dart
AnimationController({
  double? value,                       // 初始值
  Duration? duration,                  // 正向时长
  Duration? reverseDuration,           // 反向时长
  String? debugLabel,
  double lowerBound = 0.0,
  double upperBound = 1.0,
  TickerProvider vsync,                // 必填,提供 Ticker
  AnimationBehavior animationBehavior = AnimationBehavior.normal,
})
```

### AnimatedBuilder

```dart
const AnimatedBuilder({
  super.key,
  required Listenable animation,
  required TransitionBuilder builder,    // (context, child) => Widget
  Widget? child,
})
```

### AnimatedContainer

```dart
AnimatedContainer({
  super.key,
  AlignmentGeometry? alignment,
  EdgeInsetsGeometry? padding,
  Color? color,
  Decoration? decoration,
  double? width, double? height,
  BoxConstraints? constraints,
  EdgeInsetsGeometry? margin,
  Matrix4? transform,
  Widget? child,
  Curve curve = Curves.linear,          // 动画曲线
  Duration duration,                    // 必填
  VoidCallback? onEnd,
})
```

### Hero

```dart
const Hero({
  super.key,
  required Object tag,                  // 唯一标识(跨页面匹配)
  required Widget child,
  CreateRectTween? createRectTween,
  FlightShuttleBuilder? flightShuttleBuilder,
  HeroFlightShuttleBuilder? placeholderBuilder,
  bool transitionOnUserGestures = false,
})
```

## 核心属性

### AnimationController 方法

| 方法 | 说明 |
| --- | --- |
| `forward({from})` | 正向播放(0→1),返回 TickerFuture |
| `reverse({from})` | 反向播放(1→0) |
| `stop({cancelCanceled})` | 停止 |
| `reset()` | 重置到 lowerBound |
| `repeat({reverse, min, max, period})` | 重复播放 |
| `fling({...})` | 弹性动画 |
| `animateTo(target, {duration, curve})` | 动画到指定值 |
| `animateBack(target, {...})` | 反向动画到指定值 |
| `dispose()` | 释放(必调) |

### AnimationController 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `value` | `double` | 当前值(可读写) |
| `duration` | `Duration?` | 正向时长 |
| `view` | `Animation<double>` | 自身视图 |
| `status` | `AnimationStatus` | 当前状态(dismissed/forward/reverse/completed) |
| `isAnimating` | `bool` | 是否播放中 |

### ImplicitlyAnimatedWidget 共有属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `duration` | `Duration` | 动画时长 |
| `curve` | `Curve` | 动画曲线 |
| `onEnd` | `VoidCallback?` | 动画结束回调 |

## 最小示例

```dart
import 'package:flutter/material.dart';

class AnimationSample extends StatefulWidget {
  const AnimationSample({super.key});
  @override
  State<AnimationSample> createState() => _AnimationSampleState();
}

class _AnimationSampleState extends State<AnimationSample>
    with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  bool _expanded = false;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Animation 示例')),
      body: Column(children: [
        // 1. AnimatedBuilder + AnimationController
        AnimatedBuilder(
          animation: _ctrl,
          builder: (_, child) => Opacity(opacity: _ctrl.value, child: child),
          child: Container(
            width: 80, height: 80,
            color: {color-primary},
          ),
        ),
        ElevatedButton(
          child: const Text('显式动画'),
          onPressed: () => _ctrl.forward(from: 0),
        ),
        // 2. 隐式动画 AnimatedContainer
        AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeInOut,
          width: _expanded ? 200 : 100,
          height: 100,
          color: _expanded ? {color-primary} : {color-bg-secondary},
        ),
        ElevatedButton(
          child: const Text('隐式动画'),
          onPressed: () => setState(() => _expanded = !_expanded),
        ),
      ]),
    );
  }
}
```

## 参考链接

- Flutter 官方文档 - 动画 & 过渡: https://docs.flutter.cn/ui/animations
- Flutter 官方文档 - 动画教程: https://docs.flutter.cn/ui/animations/tutorial
- Flutter 官方文档 - 隐式动画: https://docs.flutter.cn/ui/animations/implicit-animations
- Flutter 官方文档 - Hero 动画: https://docs.flutter.cn/ui/animations/hero-animations
- Flutter 官方文档 - 交错动画: https://docs.flutter.cn/ui/animations/staggered-animations
- Cookbook - 过渡 Container 属性: https://docs.flutter.cn/cookbook/animation/animated-container
- Cookbook - 渐入渐出 widget: https://docs.flutter.cn/cookbook/animation/opacity-animation
- Cookbook - 页面转场动画: https://docs.flutter.cn/cookbook/animation/page-route-animation
- Widget 目录 - Animation: https://docs.flutter.cn/ui/widgets/animation
- API 参考 - AnimationController: https://api.flutter.dev/flutter/animation/AnimationController-class.html
- API 参考 - AnimatedBuilder: https://api.flutter.dev/flutter/widgets/AnimatedBuilder-class.html
- API 参考 - Hero: https://api.flutter.dev/flutter/widgets/Hero-class.html
