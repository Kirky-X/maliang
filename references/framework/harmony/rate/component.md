# Rating 组件 API 文档

> ArkTS 评分组件 `Rating`,星级输入,支持半星与只读展示。用于商品/内容评分录入与展示。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `Rating` | 星级选择(输入态)/ 星级展示(只读态) |

## 构造函数

```arkts
Rating(value?: {
  rating?: number
  indicator?: boolean   // true = 只读指示器(展示态)
  stars?: number        // 星星总数,默认 5
  stepSize?: number     // 步长(0.5 半星)
})
```

## 核心属性(链式)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| stars | number | 星星总数 |
| stepSize | number | 步长(0.5 支持半星) |
| fillColor | ResourceColor | 已选星星色 |
| foregroundColor | ResourceColor | 未选星星色 |

## 事件

| 事件 | 说明 |
| --- | --- |
| onChange | (value: number) => void 评分变化回调 |

## 最小示例

```arkts
@Entry
@Component
struct RatingDemo {
  @State score: number = 4
  build() {
    Column({ space: {spacing-md} }) {
      Text('给本单评分').fontSize({font-size-md})
      Rating({ rating: this.score, stars: 5, stepSize: 0.5 })
        .fillColor({color-warning})
        .foregroundColor({color-bg-secondary})
        .onChange((value: number) => this.score = value)
      Text(`评分:${this.score}`).fontSize({font-size-sm}).fontColor({color-text-secondary})
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`button`](../button/component.md) — 提交评分
- [`text`](../text/component.md) — 分数展示

## 参考链接

- ArkTS API 参考 - Rating: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-basic-components-rating
