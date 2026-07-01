# Animation 组件 API 文档

> ArkTS 动画能力,包含 `animateTo`(显式动画)、`transition`(转场动画)、`animation`(属性动画)、`attributeModifier`(属性修改器)。

## 核心 API

| API | 用途 | 触发方式 |
| --- | --- | --- |
| `animateTo` | 显式动画(改变属性产生过渡) | 闭包内修改 @State |
| `animation` | 属性动画(声明式附加) | 链式调用 |
| `transition` | 组件出现/消失转场 | if/else 控制显隐 |
| `attributeModifier` | 动态属性修改 | Modifier 实例 |

## animateTo 签名

```arkts
animateTo(
  options: AnimateParam,   // duration/easing/curve/delay/iterations/playMode
  event: () => void        // 在闭包内修改状态触发动画
)
```

## AnimateParam 参数

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| duration | number | 时长(ms) |
| tempo | number | 速率(1=原速) |
| curve | Curve \| ICurve | 曲线:Linear/Ease/EaseIn/EaseOut/EaseInOut/springMotion |
| delay | number | 延迟(ms) |
| iterations | number | 迭代次数,-1 无限 |
| playMode | PlayMode | Normal/Reverse/Alternate |
| onFinish | () => void | 完成回调 |

## transition 用法

```arkts
// 出现/消失转场
.transition({ type: TransitionType.Insert, translate: { y: 100 } })
.transition({ type: TransitionType.Delete, opacity: 0 })
```

## 最小示例

```arkts
@Entry
@Component
struct AnimationDemo {
  @State scale: number = 1
  build() {
    Column() {
      Button('放大')
        .scale({ x: this.scale, y: this.scale })
        .onClick(() => {
          animateTo({ duration: 300, curve: Curve.EaseOut }, () => {
            this.scale = this.scale === 1 ? 1.5 : 1
          })
        })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`dialog`](../dialog/component.md) — 弹窗模态转场
- [`carousel`](../carousel/component.md) — Swiper 切换动画

## 参考链接

- ArkTS 官方文档 - 使用动画: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-use-animation
- 动画概述: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-animation
- 属性动画: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-attribute-animation-apis
- 转场动画: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-animation-transition
- 弹簧曲线: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-spring-curve
- 属性修改器 (AttributeModifier): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-user-defined-extension-attributemodifier
