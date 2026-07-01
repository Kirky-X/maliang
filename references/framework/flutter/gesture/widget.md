# Flutter Gesture Widget 定义

## Widget 定义

Flutter 手势通过 `GestureDetector`(透明,无视觉)监听子节点手势事件。高级交互:`Dismissible`(滑动删除)、`LongPressDraggable`(长按拖拽)、`Draggable`/`DragTarget`(拖放)、`InkWell`/`InkResponse`(水波纹点击)。底层用 `Listener`(指针事件)与 `GestureRecognizer`(手势识别)。

| Widget | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `GestureDetector` | `GestureDetector` | `StatelessWidget` | 通用手势监听 |
| `InkWell` | `InkWell` | `InkResponse` | Material 水波纹点击 |
| `InkResponse` | `InkResponse` | `StatefulWidget` | 自定义水波纹响应 |
| `Dismissible` | `Dismissible` | `StatefulWidget` | 滑动删除/取消 |
| `Draggable<T>` | `Draggable<T>` | `StatefulWidget` | 可拖拽源 |
| `DragTarget<T>` | `DragTarget<T>` | `StatefulWidget` | 拖放目标 |
| `LongPressDraggable<T>` | `LongPressDraggable<T>` | `Draggable<T>` | 长按拖拽 |
| `Listener` | `Listener` | `StatelessWidget` | 底层指针事件 |
| `InteractiveViewer` | `InteractiveViewer` | `StatefulWidget` | 缩放/平移子节点 |

## 构造函数

### GestureDetector

```dart
const GestureDetector({
  super.key,
  Widget? child,
  void Function(TapDownDetails)? onTapDown,
  void Function(TapUpDetails)? onTapUp,
  VoidCallback? onTap,                  // 点击
  VoidCallback? onTapCancel,
  void Function(TapDownDetails)? onDoubleTapDown,
  VoidCallback? onDoubleTap,            // 双击
  VoidCallback? onLongPress,            // 长按
  void Function(LongPressStartDetails)? onLongPressStart,
  void Function(LongPressMoveUpdateDetails)? onLongPressMoveUpdate,
  VoidCallback? onLongPressEnd,
  VoidCallback? onLongPressUp,
  void Function(DragDownDetails)? onVerticalDragDown,
  void Function(DragStartDetails)? onVerticalDragStart,
  void Function(DragUpdateDetails)? onVerticalDragUpdate,
  VoidCallback? onVerticalDragEnd,
  ...onHorizontalDrag*,
  void Function(DragStartDetails)? onPanStart,    // 平移
  void Function(DragUpdateDetails)? onPanUpdate,
  void Function(DragEndDetails)? onPanEnd,
  void Function(ScaleStartDetails)? onScaleStart, // 缩放
  void Function(ScaleUpdateDetails)? onScaleUpdate,
  void Function(ScaleEndDetails)? onScaleEnd,
  HitTestBehavior behavior = HitTestBehavior.deferToChild,
})
```

### Dismissible

```dart
const Dismissible({
  super.key,
  required Widget child,
  required Key key,                     // 必填(区分项)
  void Function(DismissDirection)? onDismissed, // 删除回调
  DismissDirection direction = DismissDirection.horizontal,
  double? background,                   // 滑动背景(左)
  Widget? secondaryBackground,          // 滑动背景(右)
  bool confirmDismiss,                  // 确认删除
  ...
})
```

### Draggable / DragTarget

```dart
const Draggable<T>({
  super.key,
  required Widget child,                // 静态显示
  required Widget childWhenDragging,    // 拖拽时显示
  required T data,                      // 拖拽数据
  VoidCallback? onDragStarted,
  DragEndCallback? onDragEnd,
  ...
})

const DragTarget<T>({
  super.key,
  required DragTargetBuilder<T> builder,  // (context, candidate, rejected) => Widget
  void Function(T?)? onAccept,
  ...
})
```

## 核心属性

### GestureDetector 常用回调

| 回调 | 说明 |
| --- | --- |
| `onTap` | 点击 |
| `onDoubleTap` | 双击 |
| `onLongPress` | 长按(500ms) |
| `onVerticalDragUpdate` | 垂直拖动更新 |
| `onHorizontalDragUpdate` | 水平拖动更新 |
| `onPanUpdate` | 平移(任意方向) |
| `onScaleUpdate` | 缩放(双指) |

### Dismissible 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `key` | `Key` | 必填(项标识) |
| `child` | `Widget` | 必填 |
| `onDismissed` | `ValueChanged<DismissDirection>` | 删除回调 |
| `direction` | `DismissDirection` | 滑动方向(horizontal/vertical/up/down/endToStart/startToEnd) |
| `background` | `Widget?` | 滑动露出的背景 |
| `confirmDismiss` | `ConfirmDismissCallback?` | 确认删除(可异步) |

## 最小示例

```dart
import 'package:flutter/material.dart';

class GestureSample extends StatelessWidget {
  const GestureSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gesture 示例')),
      body: ListView(
        children: [
          // 1. GestureDetector 点击/长按
          GestureDetector(
            onTap: () => debugPrint('点击'),
            onLongPress: () => debugPrint('长按'),
            child: Container(
              padding: const EdgeInsets.all({spacing-md}),
              color: {color-primary},
              child: Text('点击或长按',
                  style: TextStyle(color: {color-text-on-primary})),
            ),
          ),
          // 2. InkWell 水波纹
          InkWell(
            onTap: () {},
            child: const ListTile(title: Text('水波纹点击')),
          ),
          // 3. Dismissible 滑动删除
          Dismissible(
            key: const ValueKey('item1'),
            background: Container(color: {color-danger}),
            onDismissed: (_) => debugPrint('删除'),
            child: const ListTile(title: Text('滑动删除')),
          ),
        ],
      ),
    );
  }
}
```

## 参考链接

- Flutter 官方文档 - 手势: https://docs.flutter.cn/ui/interactivity/gestures
- Cookbook - 处理点击: https://docs.flutter.cn/cookbook/gestures/handling-taps
- Cookbook - 添加 Material 水波纹: https://docs.flutter.cn/cookbook/gestures/ripples
- Cookbook - 实现滑动取消: https://docs.flutter.cn/cookbook/gestures/dismissible
- Cookbook - 拖动界面元素: https://docs.flutter.cn/cookbook/effects/drag-a-widget
- Cookbook - 跨应用拖放: https://docs.flutter.cn/ui/interactivity/gestures/drag-outside
- API 参考 - GestureDetector: https://api.flutter.dev/flutter/widgets/GestureDetector-class.html
- API 参考 - Dismissible: https://api.flutter.dev/flutter/widgets/Dismissible-class.html
- API 参考 - InkWell: https://api.flutter.dev/flutter/material/InkWell-class.html
- API 参考 - Draggable: https://api.flutter.dev/flutter/widgets/Draggable-class.html
