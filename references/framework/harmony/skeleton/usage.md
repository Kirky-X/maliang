# Skeleton 使用场景与示例

> ArkTS 无原生 Skeleton,本文件给出基于占位块 + 动画的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:列表骨架屏

```arkts
@Component
struct SkeletonRow {
  @State opacity: number = 0.4
  aboutToAppear() {
    animateTo({ duration: 1000, iterations: -1, curve: Curve.EaseInOut }, () => {
      this.opacity = 0.8
    })
  }
  build() {
    Row({ space: {spacing-sm} }) {
      Column().width(40).height(40).borderRadius({radius-full})
        .backgroundColor({color-bg-secondary}).opacity(this.opacity)
      Column({ space: {spacing-xs} }) {
        Column().width('70%').height(12).borderRadius({radius-sm})
          .backgroundColor({color-bg-secondary}).opacity(this.opacity)
        Column().width('40%').height(12).borderRadius({radius-sm})
          .backgroundColor({color-bg-secondary}).opacity(this.opacity)
      }.layoutWeight(1)
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
  }
}

@Entry
@Component
struct ListSkeletonPage {
  @State loading: boolean = true
  build() {
    Column() {
      if (this.loading) {
        ForEach([1, 2, 3, 4], () => { SkeletonRow() })
      } else {
        Text('真实内容').fontSize({font-size-md})
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:卡片骨架屏

```arkts
@Entry
@Component
struct CardSkeletonPage {
  @State opacity: number = 0.4
  aboutToAppear() {
    animateTo({ duration: 800, iterations: -1, curve: Curve.EaseInOut }, () => {
      this.opacity = 0.7
    })
  }
  build() {
    Column({ space: {spacing-sm} }) {
      Column().width('100%').height(120).borderRadius({radius-md})
        .backgroundColor({color-bg-secondary}).opacity(this.opacity)
      Column().width('60%').height(16).borderRadius({radius-sm})
        .backgroundColor({color-bg-secondary}).opacity(this.opacity)
      Column().width('90%').height(12).borderRadius({radius-sm})
        .backgroundColor({color-bg-secondary}).opacity(this.opacity)
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-md})
  }
}
```

## 场景 3:封装可复用骨架组件

```arkts
@Component
struct SkeletonBlock {
  width: Length = '100%'
  height: Length = 12
  @State opacity: number = 0.4
  aboutToAppear() {
    animateTo({ duration: 1000, iterations: -1, curve: Curve.EaseInOut }, () => {
      this.opacity = 0.7
    })
  }
  build() {
    Column()
      .width(this.width).height(this.height)
      .borderRadius({radius-sm})
      .backgroundColor({color-bg-secondary})
      .opacity(this.opacity)
  }
}

// 使用: SkeletonBlock({ width: '60%', height: 16 })
```

## 注意事项

1. **闪烁动画 iterations=-1** — 无限循环;内容加载完成后销毁骨架屏组件停止动画。
2. **opacity 区间** — 0.4-0.8 之间过渡自然;过暗看不出闪烁,过亮刺眼。
3. **占位形状贴合真实** — 骨架尺寸应与真实内容一致,避免加载后布局跳动。
4. **避免动画泄露** — 加载完成切回真实内容时,骨架组件被销毁,动画自动停止。
5. **大数据用骨架** — 列表首屏用骨架屏,后续加载更多用 LoadingProgress。
6. **颜色用 bg-secondary** — 占位块用次级背景色,与卡片底色形成层次。
