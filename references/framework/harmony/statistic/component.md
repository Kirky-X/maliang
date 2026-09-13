# Statistic 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Statistic(统计数值)/ Descriptions(键值对详情)组件。** 通过 `Text` 组合(大数值 + 标签 + delta)与 `Row`/`Column` 两列布局组合实现轻量数据展示。

## 缺失原因

ArkUI 无统计/描述列表组件;数值强调与键值对详情属于排版组合,由基础布局组件表达。

## 替代方案(组合结构)

| 角色 | ArkTS 实现 |
| --- | --- |
| 统计值(statistic) | `Column`:`Text` 标签(sm)+ `Text` 数值(28-32vp,粗体)+ `Text` delta(升红降绿或按 token) |
| 键值对(descriptions) | `Column` + `ForEach`:`Row`(键 sm 次要色 40% + 值主色 60%)两列布局 |
| 数字等宽 | `Text.fontFeature('tnum')` 对齐 |

## 组合结构

```arkts
// 统计值
Column({ space: {spacing-xs} }) {
  Text('今日 GMV').fontSize({font-size-sm}).fontColor({color-text-secondary})
  Text('¥128,460').fontSize(30).fontWeight(FontWeight.Bold)
  Text('↑ 12.4%').fontSize({font-size-sm}).fontColor({color-error}) // 涨
}

// 键值对
Row() {
  Text('订单编号').fontSize({font-size-sm}).fontColor({color-text-secondary}).width('40%')
  Text('SO-20260908-001').fontSize({font-size-md}).width('60%')
}
```

## 最小示例

```arkts
@Entry
@Component
struct StatisticDemo {
  build() {
    Column({ space: {spacing-md} }) {
      Text('经营概况').fontSize({font-size-lg}).fontWeight(FontWeight.Bold)
      Row({ space: {spacing-md} }) {
        Column({ space: {spacing-xs} }) {
          Text('今日 GMV').fontSize({font-size-sm}).fontColor({color-text-secondary})
          Text('¥128,460')
            .fontSize(30)
            .fontWeight(FontWeight.Bold)
            .fontFeature('tnum on')
          Text('↑ 12.4%')
            .fontSize({font-size-sm})
            .fontColor({color-error})
        }
        .alignItems(HorizontalAlign.Start)

        Column({ space: {spacing-xs} }) {
          Text('退款金额').fontSize({font-size-sm}).fontColor({color-text-secondary})
          Text('¥2,180')
            .fontSize(30)
            .fontWeight(FontWeight.Bold)
            .fontFeature('tnum on')
          Text('↓ 3.1%')
            .fontSize({font-size-sm})
            .fontColor({color-success})
        }
        .alignItems(HorizontalAlign.Start)
      }
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`text`](../text/component.md) — 文本基础
- [`card`](../card/component.md) — KPI 卡容器
- [`progress`](../progress/component.md) — 目标完成度

## 参考链接

- Element Plus Statistic(对照系): https://element-plus.org/zh-CN/component/statistic
- Element Plus Descriptions(对照系): https://element-plus.org/zh-CN/component/descriptions
