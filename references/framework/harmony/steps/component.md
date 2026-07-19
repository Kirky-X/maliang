# Steps Component API Documentation

> **This component is a maliang combined solution; ArkTS has no native Steps component.** Implemented via `Row` + `Icon`/`Circle` + connecting lines for horizontal/vertical steps.

## Reason for Absence

ArkTS has no native steps component (similar to Element `<el-steps>`). Steps are essentially nodes (circles/icons) + connecting lines + text, rendered with `Row` (horizontal) / `Column` (vertical) + `ForEach`.

## Alternative Solutions

- **Solution 1: Row + Icon + connecting lines (horizontal)** — nodes use `Circle` or `SymbolGlyph`, nodes connected via `Divider`/`Column`.
- **Solution 2: Column + connecting lines (vertical)** — vertical steps, similar timeline structure.

## Step State Semantics

| State | Node Style | Color |
| --- | --- | --- |
| finish (completed) | Checkmark icon | `{color-success}` |
| process (in progress) | Number/highlight | `{color-button-primary-bg}` |
| wait (not started) | Number/gray | `{color-bg-secondary}` |

## Cross-Framework Comparison

| Framework | Implementation |
| --- | --- |
| ArkTS | No native (this combined solution: Row+Icon) |
| Flutter | Third-party steps packages |
| Element Plus | `<el-steps>` |

## Minimal Example

```arkts
@Entry
@Component
struct StepsDemo {
  private steps: string[] = ['下单', '付款', '发货', '收货']
  @State current: number = 1
  build() {
    Row() {
      ForEach(this.steps, (step: string, idx: number) => {
        Column({ space: {spacing-xs} }) {
          Circle({ width: 24, height: 24 })
            .fill(idx <= this.current ? {color-button-primary-bg} : {color-bg-secondary})
          Text(step).fontSize({font-size-xs})
            .fontColor(idx <= this.current ? {color-text-primary} : {color-text-primary})
        }.alignItems(HorizontalAlign.Center)
        if (idx < this.steps.length - 1) {
          Column().width(40).height(2)
            .backgroundColor(idx < this.current ? {color-button-primary-bg} : {color-bg-secondary})
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## Related Components

- [`timeline`](../timeline/component.md) — Timeline has similar structure to steps
- [`icon`](../icon/component.md) — Step node icons

## Reference Links

- ArkTS Official Documentation: No independent chapter (this component is a maliang combined solution)
- Related components: [`timeline`](../timeline/component.md) / [`icon`](../icon/component.md)
- Creating Lists (List): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list