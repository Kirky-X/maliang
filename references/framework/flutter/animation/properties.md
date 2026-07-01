# Flutter Animation 属性列表与默认值

本文档汇总 `AnimationController` / `AnimatedBuilder` / 隐式动画 / `Hero` 的属性、默认值。颜色/尺寸默认值以 design token 形式给出。

## AnimationController 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `double` | `0.0`(可指定) | 当前值 |
| `duration` | `Duration?` | `null` | 正向时长 |
| `reverseDuration` | `Duration?` | `null` | 反向时长 |
| `lowerBound` | `double` | `0.0` | 下界 |
| `upperBound` | `double` | `1.0` | 上界 |
| `vsync` | `TickerProvider` | 必填 | Ticker 提供者 |
| `debugLabel` | `String?` | `null` | 调试标签 |
| `animationBehavior` | `AnimationBehavior` | `normal` | disable 时是否播放 |

## AnimationController 方法

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `forward` | `TickerFuture forward({double? from})` | 0→1 |
| `reverse` | `TickerFuture reverse({double? from})` | 1→0 |
| `stop` | `void stop({bool cancelCanceled = true})` | 停止 |
| `reset` | `void reset()` | 重置到 lowerBound |
| `repeat` | `TickerFuture repeat({bool reverse, double? min, double? max, Duration? period})` | 重复 |
| `fling` | `TickerFuture fling({Duration? duration, double? initialVelocity, SpringDescription? spring})` | 弹性 |
| `animateTo` | `TickerFuture animateTo(double target, {Duration? duration, Curve curve = Curves.linear})` | 动画到 |
| `animateBack` | 同上 | 反向动画到 |
| `dispose` | `void dispose()` | 释放 |

## AnimationStatus 取值

| 取值 | 说明 |
| --- | --- |
| `dismissed` | 停在 lowerBound(未播放) |
| `forward` | 正向播放中 |
| `reverse` | 反向播放中 |
| `completed` | 停在 upperBound(完成) |

## AnimatedBuilder 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `animation` | `Listenable` | 必填 | 监听对象(Animation/ChangeNotifier) |
| `builder` | `TransitionBuilder` | 必填 | 构建函数 `(context, child)` |
| `child` | `Widget?` | `null` | 不重建的子节点(性能优化) |

## ImplicitlyAnimatedWidget 共有属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `duration` | `Duration` | 必填 | 动画时长 |
| `curve` | `Curve` | `Curves.linear` | 动画曲线 |
| `onEnd` | `VoidCallback?` | `null` | 结束回调 |

## 隐式动画 Widget 列表

| Widget | 动画属性 |
| --- | --- |
| `AnimatedContainer` | 颜色/尺寸/padding/margin/边框/对齐/变换 |
| `AnimatedOpacity` | opacity |
| `AnimatedAlign` | alignment |
| `AnimatedPositioned` | left/top/right/bottom(Stack 中) |
| `AnimatedPadding` | padding |
| `AnimatedDefaultTextStyle` | 文本样式 |
| `AnimatedPhysicalModel` | elevation/color/shadow |
| `AnimatedTheme` | ThemeData |
| `AnimatedCrossFade` | 两子节点交叉淡入淡出 |
| `AnimatedSwitcher` | 子节点切换动画 |
| `TweenAnimationBuilder<T>` | 任意 Tween(通用) |

## Hero 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `tag` | `Object` | 必填 | 唯一标识(跨页面匹配) |
| `child` | `Widget` | 必填 | 共享内容 |
| `createRectTween` | `CreateRectTween?` | `null` | 自定义 Rect 过渡 |
| `flightShuttleBuilder` | `FlightShuttleBuilder?` | `null` | 飞行中替换内容 |
| `placeholderBuilder` | `HeroPlaceholderBuilder?` | `null` | 占位 |
| `transitionOnUserGestures` | `bool` | `false` | 用户手势(如 iOS 左滑)时是否过渡 |

## 常用 Curve

| Curve | 行为 |
| --- | --- |
| `Curves.linear` | 线性(默认) |
| `Curves.ease` / `Curves.easeIn` / `Curves.easeOut` / `Curves.easeInOut` | 缓动 |
| `Curves.bounceIn` / `Curves.bounceOut` | 弹跳 |
| `Curves.elasticIn` / `Curves.elasticOut` | 弹性 |
| `Curves.fastOutSlowIn` | M3 推荐标准 |
| `Curves.easeInOutCubicEmphasized` | M3 强调 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class AnimationFullSample extends StatefulWidget {
  const AnimationFullSample({super.key});
  @override
  State<AnimationFullSample> createState() => _AnimationFullSampleState();
}

class _AnimationFullSampleState extends State<AnimationFullSample>
    with TickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _animation;
  late Animation<Color?> _colorAnim;
  bool _expanded = false;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    // Tween 链式:值动画 + 颜色动画
    _animation = CurvedAnimation(parent: _ctrl, curve: Curves.easeInOut)
      ..addStatusListener((status) {
        if (status == AnimationStatus.completed) _ctrl.reverse();
        if (status == AnimationStatus.dismissed) _ctrl.forward();
      });
    _colorAnim = ColorTween(
      begin: {color-primary},
      end: {color-danger},
    ).animate(_animation);
    _ctrl.forward();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Animation 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. AnimatedBuilder(显式)
          AnimatedBuilder(
            animation: _animation,
            builder: (_, child) => Opacity(
              opacity: _animation.value,
              child: child,
            ),
            child: Container(
              width: 80, height: 80,
              color: _colorAnim.value,
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 2. AnimatedContainer(隐式)
          AnimatedContainer(
            duration: const Duration(milliseconds: 400),
            curve: Curves.fastOutSlowIn,
            width: _expanded ? 200 : 100,
            height: 60,
            decoration: BoxDecoration(
              color: _expanded ? {color-primary} : {color-bg-secondary},
              borderRadius: BorderRadius.circular({radius-md}),
            ),
          ),
          ElevatedButton(
            child: const Text('切换隐式动画'),
            onPressed: () => setState(() => _expanded = !_expanded),
          ),
          const SizedBox(height: {spacing-md}),
          // 3. AnimatedSwitcher(子节点切换)
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 300),
            transitionBuilder: (child, anim) =>
                ScaleTransition(scale: anim, child: child),
            child: Text(
              _expanded ? '展开' : '收起',
              key: ValueKey(_expanded), // 必须有 key 才触发切换
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 4. TweenAnimationBuilder(通用隐式)
          TweenAnimationBuilder<double>(
            tween: Tween(begin: 0.0, end: _expanded ? 1.0 : 0.0),
            duration: const Duration(milliseconds: 400),
            builder: (_, v, __) => LinearProgressIndicator(value: v),
          ),
          const SizedBox(height: {spacing-md}),
          // 5. Hero(需配合 Navigator,此处示意)
          const Hero(
            tag: 'avatar',
            child: CircleAvatar(
              radius: 30,
              child: Icon(Icons.person),
            ),
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- `AnimationController` 必须有 `vsync`(用 `SingleTickerProviderStateMixin`/`TickerProviderStateMixin`),必须在 `dispose()` 释放
- `AnimatedBuilder` 的 `child` 参数用于不参与重建的静态子节点,显著提升性能
- 隐式动画(`AnimatedXxx`)每次属性变化触发动画,无需手动控制 controller
- 显式动画适合循环/复杂时序,隐式动画适合简单属性过渡
- `Hero` 的 `tag` 必须全局唯一(跨页面),否则抛异常
- `addStatusListener` 监听状态变化,`addListener` 监听值变化(需手动 setState)
- `CurvedAnimation` 包装 controller 应用曲线;`Tween.animate(controller)` 链式映射值域
- 避免在 `build` 中创建 `AnimationController`(应放 `State` 字段,initState 初始化)
