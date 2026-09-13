# SegmentButton 使用场景与示例

> 列举 ArkTS 分段控件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:数据视图切换(日/周/月)

```arkts
import { SegmentButton, SegmentButtonOptions } from '@ohos.arkui.advanced.SegmentButton'

@Entry
@Component
struct TrendSegmentPage {
  @State indexes: number[] = [1]
  private opts: SegmentButtonOptions = SegmentButtonOptions.capsule({
    buttonArray: [{ text: '日' }, { text: '周' }, { text: '月' }],
    selectedColor: {color-primary},
    normalColor: {color-bg-secondary},
    selectedFontColor: {color-text-inverse},
    normalFontColor: {color-text-primary}
  })
  build() {
    Column({ space: {spacing-md} }) {
      Row() {
        Text('数据趋势').fontSize({font-size-lg}).layoutWeight(1)
        SegmentButton({
          options: this.opts,
          selectedIndexes: this.indexes,
          onItemSelected: (index: number) => this.indexes = [index]
        })
      }
      .width('100%')
      // 依据 indexes[0] 切换图表数据
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:图标 + 文本分段(地图/相机模式)

```arkts
import { SegmentButton, SegmentButtonOptions } from '@ohos.arkui.advanced.SegmentButton'

@Entry
@Component
struct IconSegmentPage {
  @State indexes: number[] = [0]
  private opts: SegmentButtonOptions = SegmentButtonOptions.capsule({
    buttonArray: [
      { text: '标准', icon: $r('app.media.ic_map') },
      { text: '卫星', icon: $r('app.media.ic_satellite') },
      { text: '路况', icon: $r('app.media.ic_traffic') }
    ],
    selectedColor: {color-primary},
    normalColor: {color-bg-secondary},
    selectedFontColor: {color-text-inverse},
    normalFontColor: {color-text-primary}
  })
  build() {
    Column() {
      SegmentButton({
        options: this.opts,
        selectedIndexes: this.indexes,
        onItemSelected: (index: number) => this.indexes = [index]
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:互斥筛选(排序方式)

```arkts
import { SegmentButton, SegmentButtonOptions } from '@ohos.arkui.advanced.SegmentButton'

@Entry
@Component
struct SortSegmentPage {
  @State indexes: number[] = [0]
  private opts: SegmentButtonOptions = SegmentButtonOptions.text({
    buttonArray: [
      { text: '综合' },
      { text: '销量' },
      { text: '价格' },
      { text: '好评' }
    ],
    selectedColor: {color-primary},
    normalColor: {color-bg-secondary},
    selectedFontColor: {color-text-inverse},
    normalFontColor: {color-text-primary}
  })
  build() {
    Column({ space: {spacing-sm} }) {
      SegmentButton({
        options: this.opts,
        selectedIndexes: this.indexes,
        onItemSelected: (index: number) => this.indexes = [index]
      })
      Text(`已选:第 ${this.indexes[0] + 1} 项`)
        .fontSize({font-size-sm}).fontColor({color-text-secondary})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **项数约束** — 2-5 项;>5 项改 tabs,单视图二选一用 switch/checkbox。
2. **与 tabs 的分工** — segmented 切换"视图/筛选状态",不承载页面级内容区;带内容区联动的页面切换用 tabs。
3. **互斥语义** — 互斥时 `selectedIndexes` 保持长度 1;选择器内展示态切换可用其表达"选中即生效"。
4. **无障碍** — SegmentButton 自带按钮语义;每段文字应自明(避免纯图标无 label)。
5. **触控目标** — 单段高度建议 ≥36vp 且整段可点,热区不足时外层补 padding。
