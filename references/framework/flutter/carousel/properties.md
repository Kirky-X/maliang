# Flutter Carousel 属性列表与默认值

本文档汇总 Flutter 轮播实现(`PageView` + `PageController` + 第三方 `CarouselSlider`)的完整属性、方法与默认值。所有视觉属性以 design token 形式引用,不在文档中硬编码。

## PageView 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `scrollDirection` | `Axis` | `Axis.horizontal` | 滑动方向(轮播固定为 horizontal) |
| `reverse` | `bool` | `false` | 是否反向 |
| `controller` | `PageController?` | `null` | 控制器 |
| `physics` | `ScrollPhysics?` | `null`(取 PageScrollPhysics) | 滑动物理 |
| `pageSnapping` | `bool` | `true` | 整页吸附 |
| `onPageChanged` | `ValueChanged<int>?` | `null` | 页面切换回调 |
| `allowImplicitScrolling` | `bool` | `false` | TalkBack 隐式滚动 |
| `dragStartBehavior` | `DragStartBehavior` | `DragStartBehavior.start` | 拖拽开始时机 |
| `restorationId` | `String?` | `null` | 状态恢复 ID |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 裁剪行为 |
| `scrollBehavior` | `ScrollBehavior?` | `null` | 滚动行为覆盖 |

## PageController 属性与方法

| 属性 / 方法 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `initialPage` | `int` | `0` | 初始页 |
| `keepPage` | `bool` | `true` | 是否记忆位置 |
| `viewportFraction` | `double` | `1.0` | 视口比例(`< 1.0` 时多页同屏) |
| `page` | `double?` | - | 当前页(含小数,滑动中变化) |
| `hasClients` | `bool` | - | 是否有附加客户端 |
| `initialPage` | `int` | `0` | 初始页 |
| `jumpToPage(int page)` | `void` | - | 瞬间跳转 |
| `animateToPage(page, {duration, curve})` | `Future<void>` | - | 动画跳转 |
| `jumpTo(double offset)` | `void` | - | 跳转到偏移(继承自 ScrollController) |
| `animateTo(...)` | `Future<void>` | - | 动画跳转(继承) |

> `viewportFraction: 0.8` 实现"前后页露边"效果(常见轮播样式);此时 `page` 的值仍为整数索引。

## CarouselOptions(carousel_slider 包)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `height` | `double?` | `null` | 高度(与 `aspectRatio` 二选一) |
| `aspectRatio` | `double?` | `16/9` | 宽高比 |
| `viewportFraction` | `double` | `0.8` | 视口比例 |
| `initialPage` | `int` | `0` | 初始页 |
| `enableInfiniteScroll` | `bool` | `true` | 无限循环 |
| `reverse` | `bool` | `false` | 反向 |
| `autoPlay` | `bool` | `false` | 自动播放 |
| `autoPlayInterval` | `Duration` | `Duration(seconds: 4)` | 自动播放间隔 |
| `autoPlayAnimationDuration` | `Duration` | `Duration(milliseconds: 800)` | 切换动画时长 |
| `autoPlayCurve` | `Curve` | `Curves.fastOutSlowIn` | 切换曲线 |
| `enlargeCenterPage` | `bool` | `false` | 中间页放大 |
| `enlargeFactor` | `double` | `0.3` | 放大系数(配合 `enlargeCenterPage`) |
| `pageSnapping` | `bool` | `true` | 整页吸附 |
| `onPageChanged` | `CarouselPageChangedCallback?` | `null` | 页面变化回调(index/reason) |
| `onScrolled` | `ValueChanged<double>?` | `null` | 滑动偏移回调 |
| `scrollDirection` | `Axis` | `Axis.horizontal` | 滑动方向 |
| `pauseAutoPlayOnTouch` | `bool` | `true` | 触摸时暂停自动播放 |
| `pauseAutoPlayOnManualNavigate` | `bool` | `true` | 手动跳转后暂停 |
| `pauseAutoPlayInFiniteScroll` | `bool` | `false` | 有限滚动时暂停 |
| `pageViewKey` | `Key?` | `null` | PageView Key |

## CarouselPageChangedReason

`onPageChanged` 第二参数取值:

| 取值 | 触发场景 |
| --- | --- |
| `CarouselPageChangedReason.manual` | 用户手动滑动 |
| `CarouselPageChangedReason.autoPlay` | 自动播放触发 |
| `CarouselPageChangedReason.controller` | 程序化调用 `nextPage`/`previousPage` |
| `CarouselPageChangedReason.pageJump` | `jumpToPage` 调用 |

## CarouselController 方法

| 方法 | 说明 |
| --- | --- |
| `nextPage({duration, curve, reason})` | 下一页 |
| `previousPage({duration, curve, reason})` | 上一页 |
| `jumpToPage(int page)` | 跳转到指定页 |
| `animateToPage(page, {duration, curve})` | 动画跳转 |
| `startAutoPlay()` | 启动自动播放 |
| `stopAutoPlay()` | 停止自动播放 |

## 完整示例

```dart
import 'dart:async';
import 'package:flutter/material.dart';

class CarouselFullSample extends StatefulWidget {
  const CarouselFullSample({super.key});

  @override
  State<CarouselFullSample> createState() => _CarouselFullSampleState();
}

class _CarouselFullSampleState extends State<CarouselFullSample> {
  final PageController _controller = PageController(
    initialPage: 0,
    viewportFraction: 0.8,
  );
  int _current = 0;
  Timer? _timer;
  bool _autoPlay = true;
  final int _itemCount = 5;

  @override
  void initState() {
    super.initState();
    _startAutoPlay();
  }

  void _startAutoPlay() {
    _timer?.cancel();
    if (!_autoPlay) return;
    _timer = Timer.periodic(const Duration(seconds: 3), (_) {
      if (!_controller.hasClients) return;
      final next = (_current + 1) % _itemCount;
      _controller.animateToPage(
        next,
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
      );
    });
  }

  void _stopAutoPlay() {
    _timer?.cancel();
    _timer = null;
  }

  @override
  void dispose() {
    _stopAutoPlay();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Carousel 完整示例'),
        actions: [
          IconButton(
            icon: Icon(_autoPlay ? Icons.pause : Icons.play_arrow),
            onPressed: () {
              setState(() => _autoPlay = !_autoPlay);
              _autoPlay ? _startAutoPlay() : _stopAutoPlay();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          SizedBox(
            height: {size-xl},
            child: PageView.builder(
              controller: _controller,
              itemCount: _itemCount,
              onPageChanged: (i) => setState(() => _current = i),
              physics: const BouncingScrollPhysics(),
              itemBuilder: (context, index) {
                return AnimatedBuilder(
                  animation: _controller,
                  builder: (context, child) {
                    double scale = 0.85;
                    if (_controller.position.haveDimensions) {
                      final page = _controller.page ?? 0;
                      scale = (1 - (index - page).abs() * 0.15).clamp(0.75, 1.0);
                    }
                    return Transform.scale(scale: scale, child: child);
                  },
                  child: GestureDetector(
                    onTap: () => debugPrint('点击了第 ${index + 1} 页'),
                    child: Container(
                      margin: const EdgeInsets.symmetric(horizontal: {spacing-xs}),
                      decoration: BoxDecoration(
                        color: index.isEven ? {color-primary} : {color-secondary},
                        borderRadius: BorderRadius.circular({radius-md}),
                        boxShadow: [
                          BoxShadow(
                            color: {color-shadow},
                            blurRadius: 8,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      alignment: Alignment.center,
                      child: Text(
                        '${index + 1} / $_itemCount',
                        style: const TextStyle(
                          color: {color-on-primary},
                          fontSize: {font-size-xl},
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 圆点指示器(动态宽度)
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: List.generate(_itemCount, (i) {
              final active = i == _current;
              return GestureDetector(
                onTap: () {
                  _controller.animateToPage(
                    i,
                    duration: const Duration(milliseconds: 300),
                    curve: Curves.easeInOut,
                  );
                },
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  width: active ? {size-sm} : {size-xs},
                  height: {size-xs},
                  margin: const EdgeInsets.symmetric(horizontal: {spacing-xs}),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular({radius-sm}),
                    color: active ? {color-primary} : {color-bg-tertiary},
                  ),
                ),
              );
            }),
          ),
          const SizedBox(height: {spacing-md}),
          // 控制按钮
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(
                onPressed: () {
                  _controller.previousPage(
                    duration: const Duration(milliseconds: 300),
                    curve: Curves.easeInOut,
                  );
                },
                icon: const Icon(Icons.chevron_left),
              ),
              Text('${_current + 1} / $_itemCount'),
              IconButton(
                onPressed: () {
                  _controller.nextPage(
                    duration: const Duration(milliseconds: 300),
                    curve: Curves.easeInOut,
                  );
                },
                icon: const Icon(Icons.chevron_right),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- 自动播放 `Timer` 必须在 `dispose()` 中 `cancel()`,否则组件销毁后仍触发 `setState` 抛异常。
- `PageController.viewportFraction < 1.0` 时,`page` 仍为整数索引;但 `itemBuilder` 中需用 `_controller.page` 计算缩放比例。
- 无限循环:原生 `PageView` 不支持真正无限滚动,需用大数(如 `itemCount: 100000`)模拟;`carousel_slider` 内置 `enableInfiniteScroll` 通过复制首尾项实现。
- `pageSnapping: false` 允许停在中间位置,但破坏轮播体验;仅在交互式浏览(非轮播)时使用。
- `BouncingScrollPhysics` 在 iOS 上更自然,Android 上需要主动设置以获得回弹效果。
- 自动播放与用户手势冲突:触摸时应暂停(`pauseAutoPlayOnTouch`),松开后恢复;手写实现需监听 `GestureDetector.onPanDown`/`onPanEnd`。
- Web 平台下 `PageView` 默认不支持鼠标拖拽,需配置 `ScrollBehavior` 启用拖拽。
