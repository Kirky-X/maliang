# Gesture 组件 API 文档

> ArkTS 手势组件,包含单一手势与组合手势。通过 `.gesture()` / `.parallelGesture()` / `.priorityGesture()` 绑定到组件。

## 单一手势组件

| 组件 | 说明 | 关键回调 |
| --- | --- | --- |
| `TapGesture` | 点击(支持多击/多指) | onAction |
| `LongPressGesture` | 长按 | onAction / onActionEnd |
| `PanGesture` | 拖拽 | onActionStart / onActionUpdate / onActionEnd |
| `PinchGesture` | 捏合缩放 | onActionStart / onActionUpdate |
| `RotationGesture` | 旋转 | onActionStart / onActionUpdate |
| `SwipeGesture` | 滑动 | onAction |

## 绑定方法

| 方法 | 并存策略 |
| --- | --- |
| `.gesture(g)` | 默认,与子组件手势竞争 |
| `.parallelGesture(g)` | 并行,不与子组件冲突 |
| `.priorityGesture(g)` | 优先级最高,覆盖子组件 |

## 组合手势

```arkts
GestureGroup(mode: GestureMode, ...gestures)
// GestureMode: Sequence(串行) / Parallel(并行) / Exclusive(互斥)
```

## 单一手势参数

| 手势 | 关键参数 |
| --- | --- |
| TapGesture | count(点击次数) / fingers(手指数) |
| LongPressGesture | repeat / duration / fingers |
| PanGesture | distance / fingers |
| PinchGesture | distance / fingers |
| RotationGesture | angle / fingers |
| SwipeGesture | speed / fingers |

## 最小示例

```arkts
@Entry
@Component
struct GestureDemo {
  build() {
    Column() {
      Text('长按我')
        .fontSize({font-size-md})
        .gesture(
          LongPressGesture().onAction(() => console.info('长按触发'))
        )
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`carousel`](../carousel/component.md) — Swiper 滑动手势
- [`dialog`](../dialog/component.md) — 弹窗拖拽关闭

## 参考链接

- ArkTS 官方文档 - 添加手势响应: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-interaction-development-guide-support-gesture
- 绑定手势方法: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-gesture-events-binding
- 单一手势: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-gesture-events-single-gesture
- 组合手势: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-gesture-events-combined-gestures
- 手势冲突处理: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-gesture-events-gesture-judge
