# Slider 使用场景与示例

> 列举 ArkTS 滑块的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:设置页数值调节(音量/亮度)

```arkts
@Entry
@Component
struct SettingSliderPage {
  @State brightness: number = 60
  build() {
    Column({ space: {spacing-md} }) {
      Row() {
        Text('亮度').fontSize({font-size-md}).layoutWeight(1)
        Text(`${this.brightness}%`).fontSize({font-size-md}).fontColor({color-text-secondary})
      }
      .width('100%')
      Slider({
        value: this.brightness,
        min: 0,
        max: 100,
        step: 5,
        style: SliderStyle.InSet
      })
        .selectedColor({color-primary})
        .showSteps(false)
        .onChange((value: number, mode: SliderChangeMode) => {
          if (mode === SliderChangeMode.End) this.brightness = Math.round(value)
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:价格区间筛选(双滑块组合)

ArkTS 无原生 RangeSlider,用两个 Slider 上下排布 + 交叉钳制组合:

```arkts
@Entry
@Component
struct RangeSliderPage {
  @State minPrice: number = 100
  @State maxPrice: number = 900
  build() {
    Column({ space: {spacing-sm} }) {
      Text(`¥${this.minPrice} - ¥${this.maxPrice}`).fontSize({font-size-md})
      Slider({ value: this.minPrice, min: 0, max: 1000, step: 10, style: SliderStyle.NONE })
        .selectedColor({color-primary})
        .onChange((v: number, mode: SliderChangeMode) => {
          if (mode === SliderChangeMode.End) this.minPrice = Math.min(Math.round(v), this.maxPrice - 10)
        })
      Slider({ value: this.maxPrice, min: 0, max: 1000, step: 10, style: SliderStyle.NONE })
        .selectedColor({color-primary})
        .onChange((v: number, mode: SliderChangeMode) => {
          if (mode === SliderChangeMode.End) this.maxPrice = Math.max(Math.round(v), this.minPrice + 10)
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:档位刻度(离散档选择)

```arkts
@Entry
@Component
struct StepSliderPage {
  @State level: number = 2
  private labels: string[] = ['低', '中', '高', '很高']
  build() {
    Column({ space: {spacing-sm} }) {
      Slider({ value: this.level, min: 0, max: 3, step: 1, style: SliderStyle.OutSet })
        .showSteps(true) // 显示刻度点
        .showTips(true)
        .selectedColor({color-primary})
        .onChange((v: number, mode: SliderChangeMode) => {
          if (mode === SliderChangeMode.End) this.level = Math.round(v)
        })
      Text(`当前档位:${this.labels[this.level]}`).fontSize({font-size-md})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **onChange 分阶段处理** — Moving 阶段做轻量预览(如数值文本),End 阶段才触发业务(请求/落库),避免高频重建。
2. **双滑块钳制** — 区间组合必须做 min ≤ max 的交叉钳制(留最小间隔),否则出现反区间。
3. **步进粒度** — step 与业务粒度一致(价格 10、音量 1、档位 1);连续拖动时 round 处理。
4. **无障碍** — Slider 自带方向键调节语义;`accessibilityText` 播报当前值(如"音量 40%")。
5. **触控目标** — 滑块圆点视觉 20-28vp,热区 SHOULD ≥44vp(加宽 padding 或外层手势区)。
