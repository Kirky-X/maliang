# Steps Usage Scenarios and Examples

> ArkTS does not have a native Steps component. This file provides a combined implementation solution based on Row+Icon. All colors, spacing, and border-radius are referenced via design tokens.

## Scenario 1: Horizontal Steps (Order Process)

```arkts
@Entry
@Component
struct HorizontalStepsPage {
  private steps: string[] = ['下单', '付款', '发货', '收货']
  @State current: number = 2
  build() {
    Row() {
      ForEach(this.steps, (step: string, idx: number) => {
        Column({ space: {spacing-xs} }) {
          if (idx < this.current) {
            SymbolGlyph($r('sys.symbol.checkmark_circle_fill'))
              .fontSize({font-size-md}).fontColor([{color-success}])
          } else {
            Text(`${idx + 1}`)
              .fontSize({font-size-xs})
              .fontColor(idx === this.current ? {color-text-on-primary} : {color-text-primary})
              .textAlign(TextAlign.Center)
              .width(24).height(24)
              .borderRadius({radius-full})
              .backgroundColor(idx === this.current ? {color-button-primary-bg} : {color-bg-secondary})
          }
          Text(step)
            .fontSize({font-size-xs})
            .fontColor(idx <= this.current ? {color-text-primary} : {color-text-primary})
        }
        .alignItems(HorizontalAlign.Center)

        if (idx < this.steps.length - 1) {
          Column().width(40).height(2)
            .backgroundColor(idx < this.current ? {color-success} : {color-bg-secondary})
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## Scenario 2: Vertical Steps

```arkts
@Entry
@Component
struct VerticalStepsPage {
  private steps: string[] = ['步骤一', '步骤二', '步骤三']
  @State current: number = 1
  build() {
    Column() {
      ForEach(this.steps, (step: string, idx: number) => {
        Row({ space: {spacing-sm} }) {
          Column() {
            Circle({ width: 24, height: 24 })
              .fill(idx <= this.current ? {color-button-primary-bg} : {color-bg-secondary})
            if (idx < this.steps.length - 1) {
              Column().width(2).layoutWeight(1)
                .backgroundColor(idx < this.current ? {color-button-primary-bg} : {color-border-default})
            }
          }.width(24).alignItems(HorizontalAlign.Center)

          Column({ space: {spacing-xs} }) {
            Text(`${step}标题`).fontSize({font-size-md})
            Text(`${step}描述信息`).fontSize({font-size-xs}).fontColor({color-text-primary})
          }
          .layoutWeight(1).alignItems(HorizontalAlign.Start)
          .padding({ bottom: {spacing-lg} })
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## Scenario 3: Clickable Step Switching

```arkts
@Entry
@Component
struct ClickableStepsPage {
  private steps: string[] = ['第一步', '第二步', '第三步']
  @State current: number = 0
  build() {
    Column({ space: {spacing-md} }) {
      Row() {
        ForEach(this.steps, (step: string, idx: number) => {
          Column({ space: {spacing-xs} }) {
            Text(`${idx + 1}`)
              .fontSize({font-size-sm})
              .fontColor({color-text-on-primary})
              .textAlign(TextAlign.Center)
              .width(32).height(32)
              .borderRadius({radius-full})
              .backgroundColor(idx === this.current ? {color-button-primary-bg}
                : idx < this.current ? {color-success} : {color-bg-secondary})
            Text(step).fontSize({font-size-xs})
          }
          .alignItems(HorizontalAlign.Center)
          .onClick(() => this.current = idx)
          if (idx < this.steps.length - 1) {
            Column().width(40).height(2)
              .backgroundColor(idx < this.current ? {color-success} : {color-border-default})
          }
        })
      }
      Text(`当前: ${this.steps[this.current]}`).fontSize({font-size-md})
    }
    .padding({spacing-md})
  }
}
```

## Notes

1. **Connecting line layoutWeight** — horizontal steps use fixed width, vertical use `layoutWeight(1)` to fill between nodes.
2. **Three states** — finish (checkmark/green), process (number/primary color), wait (number/gray); unified color scheme.
3. **Node size** — circle 24-32vp; number centered using `textAlign(Center)` + fixed width/height.
4. **Last node no line** — `if (idx < length - 1)` controls connecting line rendering.
5. **Vertical steps** — use `Column` main axis + each item `Row` (axis + content), structure similar to timeline.
6. **Responsive** — many steps horizontally will compress; mobile recommends vertical, or horizontal when step count ≤ 4.