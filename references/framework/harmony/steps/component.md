# Steps 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Steps 步骤条组件。** 通过 `Row` + `Icon`/`Circle` + 连接线组合实现横向/纵向步骤条。

## 缺失原因

ArkTS 没有原生步骤条(类似 Element `<el-steps>`)。步骤条本质是节点(圆点/图标)+ 连接线 + 文字,用 `Row`(横向)/ `Column`(纵向)+ `ForEach` 渲染。

## 替代方案

- **方案 1:Row + Icon + 连接线(横向)** — 节点用 `Circle` 或 `SymbolGlyph`,节点间用 `Divider`/`Column` 连接。
- **方案 2:Column + 连接线(纵向)** — 纵向步骤,类似时间线结构。

## 步骤状态语义

| 状态 | 节点样式 | 配色 |
| --- | --- | --- |
| finish(已完成) | 勾选图标 | `{color-success}` |
| process(进行中) | 数字/高亮 | `{color-button-primary-bg}` |
| wait(未开始) | 数字/灰 | `{color-bg-secondary}` |

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:Row+Icon) |
| Flutter | 第三方步骤条包 |
| Element Plus | `<el-steps>` |

## 最小示例

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

## 关联组件

- [`timeline`](../timeline/component.md) — 时间线与步骤条结构相似
- [`icon`](../icon/component.md) — 步骤节点图标

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`timeline`](../timeline/component.md) / [`icon`](../icon/component.md)
- 创建列表 (List): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list
