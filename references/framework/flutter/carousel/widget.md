# Flutter Carousel Widget 定义

## Widget 定义

Flutter 未提供独立的 `Carousel` Widget,轮播图通过 `PageView` + `PageController` 组合实现。配合 `carousel_slider` 第三方包(基于 `PageView`)可获取开箱即用的轮播能力(自动播放、循环、指示器)。本页同时给出原生 `PageView` 实现与第三方 `carousel_slider` 用法。

| Carousel 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 原生轮播 | `PageView` | `ScrollView` | 整页滑动,业务层实现自动播放/循环 |
| 控制器 | `PageController` | `ScrollController` | 控制页跳转、初始页、视口比例 |
| 指示器 | 自定义 Widget | - | 自绘圆点指示器(`flutter/material` 未内置) |
| 第三方封装 | `CarouselSlider` | `StatefulWidget` | 自动播放、循环、无限滚动、多页同屏 |

> 推荐优先使用 `PageView`,可完全控制行为;`carousel_slider` 适合快速集成。

## 构造函数

### PageView(用于轮播)

```dart
PageView({
  Key? key,
  Axis scrollDirection = Axis.horizontal,
  bool reverse = false,
  PageController? controller,
  ScrollPhysics? physics,
  bool pageSnapping = true,
  ValueChanged<int>? onPageChanged,
  List<Widget> children = const <Widget>[],
  DragStartBehavior dragStartBehavior = DragStartBehavior.start,
  bool allowImplicitScrolling = false,
  String? restorationId,
  Clip clipBehavior = Clip.hardEdge,
  ScrollBehavior? scrollBehavior,
})

PageView.builder({ ... required IndexedWidgetBuilder itemBuilder, required int itemCount, ... })
```

### PageController

```dart
PageController({
  int initialPage = 0,
  bool keepPage = true,
  double viewportFraction = 1.0,
})
```

### CarouselSlider(第三方)

```dart
CarouselSlider({
  Key? key,
  required List<Widget> items,
  required CarouselOptions options,
})
```

## 核心属性

### PageView 轮播相关属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `controller` | `PageController?` | 控制器,设置 `viewportFraction` 实现多页同屏 |
| `onPageChanged` | `ValueChanged<int>?` | 页面切换回调 |
| `pageSnapping` | `bool` | 是否吸附整页(默认 `true`,关闭则可滑动到中间位置) |
| `physics` | `ScrollPhysics?` | 滑动物理(常设 `PageScrollPhysics` 或 `BouncingScrollPhysics`) |
| `allowImplicitScrolling` | `bool` | 是否允许 TalkBack 隐式滚动(默认 `false`) |

### PageController 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `initialPage` | `int` | 初始页索引(默认 `0`) |
| `keepPage` | `bool` | 是否记忆当前位置(默认 `true`) |
| `viewportFraction` | `double` | 视口比例(`< 1.0` 时同屏显示多页,默认 `1.0`) |
| `page` | `double?` | 当前页(带小数,滑动中变化) |
| `hasClients` | `bool` | 是否有附加客户端 |

### CarouselOptions(第三方包)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `height` | `double?` | 轮播高度 |
| `aspectRatio` | `double?` | 宽高比(与 `height` 二选一) |
| `viewportFraction` | `double` | 视口比例(默认 `0.8`) |
| `initialPage` | `int` | 初始页 |
| `enableInfiniteScroll` | `bool` | 无限循环(默认 `true`) |
| `reverse` | `bool` | 反向 |
| `autoPlay` | `bool` | 自动播放(默认 `false`) |
| `autoPlayInterval` | `Duration` | 自动播放间隔(默认 4s) |
| `autoPlayAnimationDuration` | `Duration` | 切换动画时长(默认 800ms) |
| `autoPlayCurve` | `Curve` | 切换曲线(默认 `Curves.fastOutSlowIn`) |
| ` enlargeCenterPage` | `bool` | 中间页放大(默认 `false`) |
| `onPageChanged` | `CarouselPageChangedCallback` | 页面变化回调 |
| `scrollDirection` | `Axis` | 滑动方向(默认 `Axis.horizontal`) |

## 最小示例

```dart
import 'dart:async';
import 'package:flutter/material.dart';

/// Carousel 最小示例:PageView 自动轮播 + 圆点指示器
class CarouselSample extends StatefulWidget {
  const CarouselSample({super.key});

  @override
  State<CarouselSample> createState() => _CarouselSampleState();
}

class _CarouselSampleState extends State<CarouselSample> {
  final PageController _controller = PageController(viewportFraction: 0.85);
  int _current = 0;
  Timer? _timer;
  final List<Color> _colors = [];

  @override
  void initState() {
    super.initState();
    _startAutoPlay();
  }

  void _startAutoPlay() {
    _timer = Timer.periodic(const Duration(seconds: 3), (_) {
      final next = (_current + 1) % 5;
      _controller.animateToPage(
        next,
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
      );
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Carousel 示例')),
      body: Column(
        children: [
          SizedBox(
            height: {size-xl},
            child: PageView.builder(
              controller: _controller,
              itemCount: 5,
              onPageChanged: (i) => setState(() => _current = i),
              itemBuilder: (context, index) {
                return AnimatedBuilder(
                  animation: _controller,
                  builder: (context, child) {
                    double scale = 0.9;
                    if (_controller.position.haveDimensions) {
                      final page = _controller.page ?? 0;
                      scale = (1 - (index - page).abs() * 0.1).clamp(0.8, 1.0);
                    }
                    return Transform.scale(scale: scale, child: child);
                  },
                  child: Container(
                    margin: const EdgeInsets.symmetric(horizontal: {spacing-xs}),
                    decoration: BoxDecoration(
                      color: index.isEven ? {color-primary} : {color-secondary},
                      borderRadius: BorderRadius.circular({radius-md}),
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      '第 ${index + 1} 页',
                      style: const TextStyle(
                        color: {color-on-primary},
                        fontSize: {font-size-lg},
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: {spacing-sm}),
          // 圆点指示器
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: List.generate(5, (i) {
              return Container(
                width: {size-xs},
                height: {size-xs},
                margin: const EdgeInsets.symmetric(horizontal: {spacing-xs}),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: i == _current ? {color-primary} : {color-bg-secondary},
                ),
              );
            }),
          ),
        ],
      ),
    );
  }
}
```

## 自定义指示器(MD3 主题映射)

```dart
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  width: _current == index ? {size-sm} : {size-xs},
  height: {size-xs},
  margin: const EdgeInsets.symmetric(horizontal: {spacing-xs}),
  decoration: BoxDecoration(
    borderRadius: BorderRadius.circular({radius-sm}),
    color: _current == index ? {color-primary} : {color-bg-tertiary},
  ),
)
```

> 注:示例中的 `{color-primary}`、`{spacing-xs}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- pub.dev - carousel_slider: https://pub.flutter-io.cn/packages/carousel_slider
- API 参考 - PageView: https://api.flutter.dev/flutter/widgets/PageView-class.html
- API 参考 - PageController: https://api.flutter.dev/flutter/widgets/PageController-class.html
