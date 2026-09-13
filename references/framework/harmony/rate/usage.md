# Rating 使用场景与示例

> 列举 ArkTS 评分组件的典型场景:评分输入(买后评价)、评分展示(只读)、无分控评。

## 场景 1:评价表单(半星输入 + 提交)

```arkts
@Entry
@Component
struct ReviewRatingPage {
  @State score: number = 0
  @State comment: string = ''
  build() {
    Column({ space: {spacing-md} }) {
      Text('宝贝满足你的期待吗?').fontSize({font-size-md})
      Rating({ rating: this.score, stars: 5, stepSize: 0.5 })
        .fillColor({color-warning})
        .foregroundColor({color-bg-secondary})
        .onChange((value: number) => this.score = value)
      Text(['', '很差', '较差', '一般', '满意', '超预期'][Math.ceil(this.score)])
        .fontSize({font-size-sm}).fontColor({color-text-secondary})
      TextInput({ placeholder: '说说你的使用体验' })
        .fontSize({font-size-md})
        .onChange((v: string) => this.comment = v)
      Button('提交评价').enabled(this.score > 0)
        .onClick(() => {
          // 提交后 promptAction.showToast('感谢评价')
        })
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
  }
}
```

## 场景 2:商品列表评分展示(只读)

```arkts
@Entry
@Component
struct RatingDisplayPage {
  build() {
    Row({ space: {spacing-sm} }) {
      Rating({ rating: 4.5, indicator: true, stars: 5 }) // indicator 只读
        .fillColor({color-warning})
        .foregroundColor({color-bg-secondary})
        .stars(5)
        .stepSize(0.5)
      Text('4.5').fontSize({font-size-sm}).fontColor({color-text-primary})
      Text('(2.3 万条)').fontSize({font-size-sm}).fontColor({color-text-secondary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:无分控评(零分兜底)

无评分数据时展示占位文案而非 0 星(避免误导):

```arkts
@Entry
@Component
struct NoRatingPage {
  @State score: number = 0 // 后端无数据
  build() {
    Row({ space: {spacing-sm} }) {
      if (this.score > 0) {
        Rating({ rating: this.score, indicator: true }).fillColor({color-warning})
        Text(`${this.score}`).fontSize({font-size-sm})
      } else {
        Text('暂无评分').fontSize({font-size-sm}).fontColor({color-text-secondary})
      }
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **输入 vs 展示** — 录入用默认 `indicator: false`;列表/详情展示用 `indicator: true` 只读,避免误触改分。
2. **半星步长** — `stepSize: 0.5` 支持半星;展示侧分数保留一位小数。
3. **星级色** — 评分惯例用警示黄/橙({color-warning});改用主题色需全站统一。
4. **无分控评** — 0 分/无数据显示"暂无评分",不渲染空星阵。
5. **无障碍** — Rating 自带滑杆语义;`accessibilityText` 播报"4.5 分,满分 5 分"。
