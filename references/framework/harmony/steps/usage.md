# Steps 使用场景与示例

> ArkTS 无原生 Steps,本文件给出基于 Row+Icon 的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:横向步骤条(订单流程)

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

## 场景 2:纵向步骤条

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

## 场景 3:可点击切换步骤

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

## 注意事项

1. **连接线 layoutWeight** — 横向步骤线用固定宽度,纵向用 `layoutWeight(1)` 撑满节点间。
2. **状态三态** — finish(勾选/绿)、process(数字/主色)、wait(数字/灰);配色统一。
3. **节点尺寸** — 圆点 24-32vp;数字居中用 `textAlign(Center)` + 固定宽高。
4. **最后节点无线** — `if (idx < length - 1)` 控制连接线渲染。
5. **纵向步骤** — 用 `Column` 主轴 + 每项 `Row`(轴线 + 内容),结构类似时间线。
6. **响应式** — 步骤多时横向会挤压;移动端建议纵向,或步骤数 ≤ 4 时横向。
