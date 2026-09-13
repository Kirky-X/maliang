# Statistic 使用场景与示例

> 列举 ArkTS 统计/描述组合方案的典型场景:KPI 概览、详情页键值对、订单信息。

## 场景 1:KPI 卡(统计 + delta + 目标)

```arkts
@Entry
@Component
struct KpiCardPage {
  build() {
    Column({ space: {spacing-md} }) {
      Text('GMV').fontSize({font-size-sm}).fontColor({color-text-secondary})
      Row({ space: {spacing-sm} }) {
        Text('¥128,460').fontSize(32).fontWeight(FontWeight.Bold).fontFeature('tnum on')
        Text('↑ 12.4%')
          .fontSize({font-size-sm})
          .fontColor({color-error})
          .padding({ left: {spacing-xs}, right: {spacing-xs}, top: 2, bottom: 2 })
          .backgroundColor({color-bg-secondary})
          .borderRadius({radius-sm})
      }
      Row({ space: {spacing-sm} }) {
        Progress({ value: 78, total: 100, type: ProgressType.Linear }).width('70%')
        Text('目标 78%').fontSize({font-size-sm}).fontColor({color-text-secondary})
      }
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-lg})
  }
}
```

## 场景 2:详情页键值对(descriptions)

```arkts
@Entry
@Component
struct DescriptionsPage {
  @State order: Array<[string, string]> = [
    ['订单编号', 'SO-20260908-001'],
    ['下单时间', '2026-09-08 14:32'],
    ['支付方式', '微信支付'],
    ['配送地址', '上海市浦东新区xx路 88 号']
  ]
  build() {
    Column({ space: {spacing-sm} }) {
      Text('订单信息').fontSize({font-size-md}).fontWeight(FontWeight.Medium)
      ForEach(this.order, (pair: [string, string]) => {
        Row() {
          Text(pair[0])
            .fontSize({font-size-sm})
            .fontColor({color-text-secondary})
            .width('32%')
          Text(pair[1])
            .fontSize({font-size-md})
            .layoutWeight(1)
        }
        .width('100%')
        .padding({ top: {spacing-xs}, bottom: {spacing-xs} })
      })
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-lg})
  }
}
```

## 场景 3:带边框的分块详情(border 场景)

```arkts
@Entry
@Component
struct BorderedDescriptionsPage {
  @State rows: Array<[string, string]> = [
    ['收货人', '张三'],
    ['联系电话', '138****8888'],
    ['发票类型', '电子普通发票']
  ]
  build() {
    Column() {
      ForEach(this.rows, (pair: [string, string], idx: number) => {
        Row() {
          Text(pair[0])
            .fontSize({font-size-sm})
            .fontColor({color-text-secondary})
            .width('32%')
            .padding({spacing-sm})
            .backgroundColor({color-bg-secondary})
          Text(pair[1])
            .fontSize({font-size-md})
            .padding({spacing-sm})
        }
        .width('100%')
        .border({ width: {border-hairline}, color: {color-border-default} })
      })
    }
    .borderRadius({radius-md})
    .clip(true)
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **数字等宽** — 统计值与金额列 MUST 开 `fontFeature('tnum on')`,滚动刷新时数字不跳动。
2. **delta 语义** — 涨跌色按业务定:GMV 涨=正向色;退款涨=负向色,勿一刀切红涨绿跌。
3. **键值宽比** — 键列建议 32%-40% 定宽,值列 `layoutWeight(1)`,长值换行不破列。
4. **数值字号** — KPI 数值 28-32vp + Bold;标签 sm 次要色;delta sm,对比度达标。
5. **无障碍** — 读屏按"标签 + 值"顺序播报;delta 文案勿只靠箭头,带"涨/跌"词。
