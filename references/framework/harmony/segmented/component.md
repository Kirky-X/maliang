# SegmentButton 组件 API 文档

> ArkTS 分段控件 `SegmentButton`(`@ohos.arkui.advanced.SegmentButton`,API 11+ 高级组件),用于 2-5 项的互斥视图切换/筛选,介于 tabs 与 radio 之间。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `SegmentButton` | 分段按钮(单项文本/图标+文本),`SegmentButtonOptions` 声明形态 |

## 构造函数

```arkts
import { SegmentButton, SegmentButtonOptions } from '@ohos.arkui.advanced.SegmentButton'

SegmentButton({
  options: SegmentButtonOptions,   // 按钮组形态与样式
  selectedIndexes: number[],       // 当前选中索引(互斥时长度 1)
  onItemSelected?: (index: number) => void // 选中某段回调
})
```

## SegmentButtonOptions 工厂

| 工厂 | 说明 |
| --- | --- |
| `SegmentButtonOptions.capsule(...)` | 胶囊型(文本/图标+文本) |
| `SegmentButtonOptions.text(...)` | 文本型分段 |
| `buttonArray` | 按钮数组(`{ text?: string; icon?: ResourceStr }[]`) |

## 事件

| 事件 | 说明 |
| --- | --- |
| onItemSelected(构造参数) | (index: number) => void 选中某段回调 |
| selectedIndexes(@State 双向) | 状态驱动选中,同步更新实现受控 |

## 最小示例

```arkts
import { SegmentButton, SegmentButtonOptions } from '@ohos.arkui.advanced.SegmentButton'

@Entry
@Component
struct SegmentDemo {
  @State selectedIndexes: number[] = [0]
  private options: SegmentButtonOptions = SegmentButtonOptions.capsule({
    buttonArray: [
      { text: '日' },
      { text: '周' },
      { text: '月' }
    ],
    selectedColor: {color-primary},
    normalColor: {color-bg-secondary},
    selectedFontColor: {color-text-inverse},
    normalFontColor: {color-text-primary}
  })
  build() {
    Column({ space: {spacing-md} }) {
      SegmentButton({
        options: this.options,
        selectedIndexes: this.selectedIndexes,
        onItemSelected: (index: number) => this.selectedIndexes = [index]
      })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`tabs`](../tabs/component.md) — 大页面级切换(含内容区)
- [`radio`](../radio/component.md) — 表单互斥录入

## 参考链接

- ArkTS API 参考 - SegmentButton: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ui-stats-segmentbutton
