# Pagination 使用场景与示例

> ArkTS 无原生 Pagination,本文件给出基于 Button 组合的实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础分页器

```arkts
@Entry
@Component
struct BasicPaginationPage {
  @State current: number = 1
  private total: number = 5
  build() {
    Row({ space: {spacing-sm} }) {
      Button('上一页')
        .enabled(this.current > 1)
        .backgroundColor({color-bg-secondary})
        .fontColor({color-text-primary})
        .onClick(() => { if (this.current > 1) this.current-- })
      ForEach([1, 2, 3, 4, 5], (n: number) => {
        Button(`${n}`)
          .backgroundColor(this.current === n ? {color-button-primary-bg} : {color-bg-secondary})
          .fontColor(this.current === n ? {color-text-on-primary} : {color-text-primary})
          .onClick(() => this.current = n)
      })
      Button('下一页')
        .enabled(this.current < this.total)
        .backgroundColor({color-bg-secondary})
        .fontColor({color-text-primary})
        .onClick(() => { if (this.current < this.total) this.current++ })
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:省略号分页(大量页)

```arkts
@Entry
@Component
struct EllipsisPaginationPage {
  @State current: number = 1
  private total: number = 50
  private pages(): number[] {
    if (this.current <= 3) return [1, 2, 3, 4, 5]
    if (this.current >= this.total - 2) return [this.total - 4, this.total - 3, this.total - 2, this.total - 1, this.total]
    return [this.current - 2, this.current - 1, this.current, this.current + 1, this.current + 2]
  }
  build() {
    Row({ space: {spacing-sm} }) {
      Button('首页')
        .backgroundColor({color-bg-secondary}).fontColor({color-text-primary})
        .onClick(() => this.current = 1)
      Text('...').fontSize({font-size-sm}).fontColor({color-text-primary})
      ForEach(this.pages(), (n: number) => {
        Button(`${n}`)
          .backgroundColor(this.current === n ? {color-button-primary-bg} : {color-bg-secondary})
          .fontColor(this.current === n ? {color-text-on-primary} : {color-text-primary})
          .onClick(() => this.current = n)
      })
      Text('...').fontSize({font-size-sm}).fontColor({color-text-primary})
      Button('末页')
        .backgroundColor({color-bg-secondary}).fontColor({color-text-primary})
        .onClick(() => this.current = this.total)
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:封装可复用 Pagination

```arkts
@Component
struct Pagination {
  @Prop current: number
  private total: number = 1
  onChange: (page: number) => void = () => {}
  build() {
    Row({ space: {spacing-sm} }) {
      Button('<').backgroundColor({color-bg-secondary}).fontColor({color-text-primary})
        .onClick(() => { if (this.current > 1) this.onChange(this.current - 1) })
      ForEach(Array.from({ length: this.total }, (_, i) => i + 1), (n: number) => {
        Button(`${n}`)
          .backgroundColor(this.current === n ? {color-button-primary-bg} : {color-bg-secondary})
          .fontColor(this.current === n ? {color-text-on-primary} : {color-text-primary})
          .onClick(() => this.onChange(n))
      })
      Button('>').backgroundColor({color-bg-secondary}).fontColor({color-text-primary})
        .onClick(() => { if (this.current < this.total) this.onChange(this.current + 1) })
    }
  }
}
```

## 场景 4:移动端简化分页(上一页/下一页)

```arkts
@Entry
@Component
struct MobilePaginationPage {
  @State current: number = 1
  build() {
    Row() {
      Button('上一页')
        .layoutWeight(1)
        .backgroundColor({color-bg-secondary}).fontColor({color-text-primary})
        .onClick(() => this.current--)
      Text(`${this.current} / 10`)
        .fontSize({font-size-sm}).fontColor({color-text-primary})
        .margin({ left: {spacing-md}, right: {spacing-md} })
      Button('下一页')
        .layoutWeight(1)
        .backgroundColor({color-button-primary-bg}).fontColor({color-text-on-primary})
        .onClick(() => this.current++)
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **移动端优先无限滚动** — 手机端用 List + onReachEnd 加载更多,体验优于分页器;分页器适合平板/PC。
2. **enabled 控制边界** — 首页禁用"上一页",末页禁用"下一页";避免越界。
3. **省略号逻辑** — 页数 > 7 时显示首末页 + 当前页附近;中间用 `...` 省略。
4. **onChange 回调** — 封装组件用 `onChange(page)` 回调通知父组件,父组件请求数据。
5. **页码宽度** — 数字按钮宽度固定,避免 1→10 切换时布局抖动。
6. **加载状态** — 切页时显示 LoadingProgress,数据返回后隐藏。
