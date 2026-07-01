# Skeleton 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Skeleton 骨架屏组件。** 通过 `Stack`/`Column` + 占位块(灰色矩形)+ 闪烁动画组合实现。

## 缺失原因

ArkTS 没有 Ant Design `<Skeleton>` 那样的原生骨架屏。骨架屏本质是内容区的灰色占位形状,用 `Column`/`Row` 排列灰色矩形块,配合 `opacity` 闪烁动画即可。

## 替代方案

- **方案 1:占位块 + 闪烁动画** — 用灰色背景的 `Column`/`Row`/`Text` 占位,`opacity` 在 0.3-0.7 间循环动画。
- **方案 2:LoadingProgress 替代** — 简单场景用转圈替代;但骨架屏更贴近真实布局,体验更佳。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:占位块+动画) |
| Flutter | `Shimmer`(第三方包) |
| Element Plus | `<el-skeleton>` |

## 最小示例

```arkts
@Entry
@Component
struct SkeletonDemo {
  @State opacity: number = 0.5
  aboutToAppear() {
    animateTo({ duration: 800, iterations: -1, curve: Curve.EaseInOut }, () => {
      this.opacity = 1
    })
  }
  build() {
    Column({ space: {spacing-sm} }) {
      Row({ space: {spacing-sm} }) {
        Column().width(48).height(48).borderRadius({radius-full})
          .backgroundColor({color-bg-secondary}).opacity(this.opacity)
        Column({ space: {spacing-xs} }) {
          Column().width(120).height(12).backgroundColor({color-bg-secondary}).opacity(this.opacity)
          Column().width(80).height(12).backgroundColor({color-bg-secondary}).opacity(this.opacity)
        }
      }
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`loading`](../loading/component.md) — 加载动画
- [`card`](../card/component.md) — 骨架屏常模拟卡片布局

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`loading`](../loading/component.md) / [`animation`](../animation/component.md)
- 动画概述: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-animation
