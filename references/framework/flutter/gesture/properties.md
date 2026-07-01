# Flutter Gesture 属性列表与默认值

本文档汇总 `GestureDetector` / `InkWell` / `Dismissible` / `Draggable` / `DragTarget` 的属性、默认值与回调。

## GestureDetector 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget?` | `null` | 子节点 |
| `behavior` | `HitTestBehavior` | `deferToChild` | 命中测试(opaque/deferToChild/translucent) |
| `onTapDown` | `ValueChanged<TapDownDetails>?` | `null` | 按下 |
| `onTapUp` | `ValueChanged<TapUpDetails>?` | `null` | 抬起 |
| `onTap` | `VoidCallback?` | `null` | 点击(完成) |
| `onTapCancel` | `VoidCallback?` | `null` | 取消点击 |
| `onDoubleTapDown` | `ValueChanged<TapDownDetails>?` | `null` | 双击按下 |
| `onDoubleTap` | `VoidCallback?` | `null` | 双击 |
| `onLongPress` | `VoidCallback?` | `null` | 长按 |
| `onLongPressStart` | `ValueChanged<LongPressStartDetails>?` | `null` | 长按开始 |
| `onLongPressMoveUpdate` | `ValueChanged<LongPressMoveUpdateDetails>?` | `null` | 长按移动 |
| `onLongPressEnd` | `ValueChanged<LongPressEndDetails>?` | `null` | 长按结束 |
| `onLongPressUp` | `VoidCallback?` | `null` | 长按抬起 |
| `onVerticalDragStart` | `ValueChanged<DragStartDetails>?` | `null` | 垂直拖动开始 |
| `onVerticalDragUpdate` | `ValueChanged<DragUpdateDetails>?` | `null` | 垂直拖动更新 |
| `onVerticalDragEnd` | `ValueChanged<DragEndDetails>?` | `null` | 垂直拖动结束 |
| `onHorizontalDrag*` | 同上 | `null` | 水平拖动 |
| `onPanStart/Update/End` | 同上 | `null` | 平移(任意方向) |
| `onScaleStart/Update/End` | 同上 | `null` | 缩放(双指) |
| `dragStartBehavior` | `DragStartBehavior` | `start` | 拖动起始行为 |
| `excludeFromSemantics` | `bool` | `false` | 排除无障碍 |

## InkWell 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget?` | `null` | 子节点 |
| `onTap` | `VoidCallback?` | `null` | 点击 |
| `onDoubleTap` | `VoidCallback?` | `null` | 双击 |
| `onLongPress` | `VoidCallback?` | `null` | 长按 |
| `onTapDown` | `ValueChanged<TapDownDetails>?` | `null` | 按下 |
| `onTapUp` | `ValueChanged<TapUpDetails>?` | `null` | 抬起 |
| `onTapCancel` | `VoidCallback?` | `null` | 取消 |
| `onHover` | `ValueChanged<bool>?` | `null` | 鼠标悬停 |
| `onFocusChange` | `ValueChanged<bool>?` | `null` | 焦点变化 |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |
| `borderRadius` | `BorderRadius?` | `null` | 水波纹裁剪圆角 |
| `customBorder` | `ShapeBorder?` | `null` | 自定义裁剪形状 |
| `radius` | `double?` | `null` | 水波纹半径 |
| `splashColor` | `Color?` | `null` | 水波纹颜色 |
| `highlightColor` | `Color?` | `null` | 高亮颜色 |
| `hoverColor` | `Color?` | `null` | 悬停颜色 |
| `focusColor` | `Color?` | `null` | 焦点颜色 |
| `overlayColor` | `MaterialStateProperty<Color?>?` | `null` | 状态叠加色 |
| `enableFeedback` | `bool` | `true` | 触觉/声音反馈 |
| `excludeFromSemantics` | `bool` | `false` | 排除无障碍 |

## Dismissible 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Key` | 必填 | 项标识 |
| `child` | `Widget` | 必填 | 项内容 |
| `onDismissed` | `ValueChanged<DismissDirection>?` | `null` | 删除回调 |
| `direction` | `DismissDirection` | `horizontal` | 允许方向 |
| `background` | `Widget?` | `null` | 滑动背景 |
| `secondaryBackground` | `Widget?` | `null` | 反向滑动背景 |
| `confirmDismiss` | `ConfirmDismissCallback?` | `null` | 确认删除(返回 Future<bool?>) |
| `movementDuration` | `Duration` | `Duration(milliseconds: 200)` | 移动动画时长 |
| `resizeDuration` | `Duration?` | `Duration(milliseconds: 300)` | 缩小动画时长 |
| `dismissThresholds` | `Map<DismissDirection, double>` | `{}` | 触发删除阈值(默认 0.4) |
| `dragStartBehavior` | `DragStartBehavior` | `start` | 拖动起始 |

### DismissDirection 取值

| 取值 | 允许方向 |
| --- | --- |
| `horizontal` | 水平(左右) |
| `vertical` | 垂直(上下) |
| `endToStart` | 终→始(RTL 下右→左) |
| `startToEnd` | 始→终 |
| `up` | 上滑 |
| `down` | 下滑 |

## Draggable 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `data` | `T?` | 必填 | 拖拽数据 |
| `child` | `Widget` | 必填 | 静态显示 |
| `childWhenDragging` | `Widget?` | `null` | 拖拽时原位显示 |
| `feedback` | `Widget` | 必填 | 拖拽时跟随指针显示 |
| `feedbackOffset` | `Offset` | `Offset.zero` | feedback 偏移 |
| `axis` | `Axis?` | `null` | 限制拖动轴 |
| `affinity` | `Axis?` | `null` | 手势亲和性 |
| `onDragStarted` | `VoidCallback?` | `null` | 拖拽开始 |
| `onDragUpdate` | `DragUpdateCallback?` | `null` | 拖拽更新 |
| `onDragEnd` | `DragEndCallback?` | `null` | 拖拽结束 |
| `onDragCompleted` | `VoidCallback?` | `null` | 拖拽完成(被接受) |
| `maxSimultaneousDrags` | `int?` | `null` | 最大同时拖拽数 |

## DragTarget 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `builder` | `DragTargetBuilder<T>` | 必填 | `(context, candidateData, rejectedData) => Widget` |
| `onAccept` | `DragTargetAccept<T>?` | `null` | 接受(数据) |
| `onAcceptWithDetails` | `DragTargetAcceptWithDetails<T>?` | `null` | 接受(含详情) |
| `onWillAccept` | `DragTargetWillAccept<T>?` | `null` | 是否接受(返回 bool) |
| `onLeave` | `DragTargetLeave<T>?` | `null` | 离开目标 |
| `onMove` | `DragTargetMove<T>?` | `null` | 在目标上移动 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class GestureFullSample extends StatefulWidget {
  const GestureFullSample({super.key});
  @override
  State<GestureFullSample> createState() => _GestureFullSampleState();
}

class _GestureFullSampleState extends State<GestureFullSample> {
  final _items = List.generate(5, (i) => 'Item ${i + 1}');
  Offset _position = Offset.zero;
  Color _targetColor = {color-bg-secondary};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gesture 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. Dismissible 滑动删除
          ..._items.map((item) => Dismissible(
                key: Key(item),
                direction: DismissDirection.endToStart,
                background: Container(
                  color: {color-danger},
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.only(right: {spacing-md}),
                  child: const Icon(Icons.delete, color: Colors.white),
                ),
                confirmDismiss: (_) async {
                  return await showDialog<bool>(
                        context: context,
                        builder: (_) => AlertDialog(
                          title: const Text('确认删除'),
                          actions: [
                            TextButton(
                                child: const Text('取消'),
                                onPressed: () => Navigator.pop(context, false)),
                            TextButton(
                                child: const Text('删除'),
                                onPressed: () => Navigator.pop(context, true)),
                          ],
                        ),
                      ) ??
                      false;
                },
                onDismissed: (_) =>
                    setState(() => _items.remove(item)),
                child: ListTile(
                  title: Text(item),
                  tileColor: {color-bg-primary},
                ),
              )),
          const SizedBox(height: {spacing-md}),
          // 2. Draggable + DragTarget
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Draggable<String>(
                data: 'red',
                child: Container(
                  width: 60, height: 60,
                  color: {color-danger},
                ),
                childWhenDragging: Container(
                  width: 60, height: 60,
                  color: {color-danger}.withOpacity(0.3),
                ),
                feedback: Container(
                  width: 60, height: 60,
                  color: {color-danger},
                ),
              ),
              DragTarget<String>(
                builder: (_, candidate, __) => Container(
                  width: 80, height: 80,
                  color: _targetColor,
                  alignment: Alignment.center,
                  child: Text(candidate.isEmpty ? '拖到此处' : '释放'),
                ),
                onAccept: (data) => setState(() {
                  _targetColor = data == 'red'
                      ? {color-danger}
                      : {color-bg-secondary};
                }),
              ),
            ],
          ),
          const SizedBox(height: {spacing-md}),
          // 3. GestureDetector 平移
          GestureDetector(
            onPanUpdate: (d) => setState(() =>
                _position += d.delta),
            child: Transform.translate(
              offset: _position,
              child: Container(
                width: 60, height: 60,
                color: {color-primary},
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- `GestureDetector` 的 `onTap` 与 `onVerticalDragUpdate` 等可能竞争;设 `behavior: HitTestBehavior.opaque` 让透明区域可点击
- `InkWell` 需 `Material` 祖先(水波纹依赖 Material);在 `Container(color:)` 上无效,需用 `Material` 或 `Ink` 包裹
- `Dismissible` 的 `key` 必须稳定且唯一,否则删除动画错乱
- `confirmDismiss` 返回 `false` 取消删除(项回弹),返回 `true` 确认
- `Draggable` 的 `feedback` 是拖拽时跟随指针的 Widget,通常与 `child` 相同但有透明度/缩放
- `onVerticalDragUpdate` 与 `onHorizontalDragUpdate` 互斥(同一手势只触发一个方向)
- `onPanUpdate` 与 `onScaleUpdate` 不能与 `onVerticalDrag/HorizontalDrag` 同时使用
- 长按时长由 `kLongPressTimeout`(500ms)决定,可通过 `LongPressGestureRecognizer` 自定义
