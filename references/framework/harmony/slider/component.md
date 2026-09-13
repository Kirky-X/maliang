# Slider 组件 API 文档

> ArkTS 滑块组件 `Slider`,支持单滑块与区间外组合实现,用于数值/区间录入(音量、亮度、价格范围筛选)。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `Slider` | 滑块,拖动选定数值 |
| `Slider` + 双 `@State` | 区间筛选(双滑块经组合实现,见 usage.md 场景 2) |

## 构造函数

```arkts
Slider(value?: {
  value?: number
  min?: number
  max?: number
  step?: number
  style?: SliderStyle   // OutSet | InSet | NONE
  direction?: Axis      // Horizontal | Vertical
  reverse?: boolean
})
```

## 核心属性(链式)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| blockColor | ResourceColor | 滑块圆点颜色 |
| trackColor | ResourceColor | 轨道底色 |
| selectedColor | ResourceColor | 已选轨道色 |
| showSteps | boolean | 显示刻度点 |
| showTips | boolean | 拖动时气泡提示 |
| trackThickness | Length | 轨道粗细 |

## 事件

| 事件 | 说明 |
| --- | --- |
| onChange | (value: number, mode: SliderChangeMode) => void,mode 含 Begin/Moving/End |

## 最小示例

```arkts
@Entry
@Component
struct SliderDemo {
  @State volume: number = 40
  build() {
    Column({ space: {spacing-md} }) {
      Text(`音量:${this.volume}%`).fontSize({font-size-md})
      Slider({
        value: this.volume,
        min: 0,
        max: 100,
        step: 1,
        style: SliderStyle.OutSet
      })
        .selectedColor({color-primary})
        .trackColor({color-bg-secondary})
        .blockColor({color-primary})
        .showTips(true)
        .width('100%')
        .onChange((value: number, mode: SliderChangeMode) => {
          if (mode === SliderChangeMode.End) this.volume = Math.round(value)
        })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`progress`](../progress/component.md) — 只读进度展示
- [`checkbox`](../checkbox/component.md) — 多选录入

## 参考链接

- ArkTS API 参考 - Slider: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-basic-components-slider
