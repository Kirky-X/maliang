# Timeline 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Timeline 时间线组件。** 通过 `List` + `Divider`/`Shape`(竖线)+ 节点圆点组合实现。

## 缺失原因

ArkTS 没有原生时间线组件。时间线本质是垂直列表 + 左侧时间轴(竖线 + 节点),用 `List` 承载条目,左侧用 `Column` + `Divider` 画轴线,圆点用 `Circle` 或 `borderRadius-full`。

## 替代方案

- **方案 1:List + 左侧轴线** — 每个 `ListItem` 是 `Row`:左侧时间轴(竖线+圆点),右侧内容。
- **方案 2:Column + Divider** — 简单时间线用 `Column` 垂直排列,节点间用 `Divider` 连接。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:List+轴线) |
| Flutter | `TimelineTile`(第三方) |
| Element Plus | `<el-timeline>` |

## 最小示例

```arkts
@Entry
@Component
struct TimelineDemo {
  private items: string[] = ['事件一', '事件二', '事件三']
  build() {
    Column() {
      ForEach(this.items, (item: string, idx: number) => {
        Row({ space: {spacing-sm} }) {
          // 左侧时间轴
          Column() {
            Circle({ width: 10, height: 10 }).fill({color-button-primary-bg})
            if (idx < this.items.length - 1) {
              Column().width(1).layoutWeight(1).backgroundColor({color-border-default})
            }
          }.width(20).alignItems(HorizontalAlign.Center)
          // 右侧内容
          Column() {
            Text(item).fontSize({font-size-md})
            Text('2026-01-01').fontSize({font-size-xs}).fontColor({color-text-primary})
          }.layoutWeight(1).alignItems(HorizontalAlign.Start)
        }
        .height(idx === this.items.length - 1 ? 40 : 80)
      })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`list`](../list/component.md) — 时间线基于 List
- [`shape`](../shape/component.md) — 轴线圆点用 Circle/Line
- [`divider`](../divider/component.md) — 节点间分隔

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`list`](../list/component.md) / [`shape`](../shape/component.md)
- 创建列表 (List): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list
