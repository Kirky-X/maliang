# Loading 组件 API 文档

> ArkTS 加载组件 `LoadingProgress`,显示不定进度加载动画(转圈)。值已知用 `Progress`(见 progress 组件)。

## 组件定义

`LoadingProgress` 无需参数,展示旋转加载动画,通过 `color` 控制颜色,`width/height` 控制尺寸。

## 构造函数

```arkts
LoadingProgress()
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| color | ResourceColor | 动画颜色,用 `{color-button-primary-bg}` |
| width / height | Length | 尺寸 |
| enableLoading | boolean | 是否启用动画(API 10+) |

## 最小示例

```arkts
@Entry
@Component
struct LoadingDemo {
  build() {
    Column({ space: {spacing-sm} }) {
      LoadingProgress()
        .width(48).height(48)
        .color({color-button-primary-bg})
      Text('加载中...').fontSize({font-size-sm}).fontColor({color-text-primary})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`progress`](../progress/component.md) — 已知进度用 Progress
- [`skeleton`](../skeleton/component.md) — 骨架屏(占位加载)
- [`dialog`](../dialog/component.md) — 弹窗内加载

## 参考链接

- ArkTS 官方文档 - 进度条 (Progress/LoadingProgress): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-progress-indicator
