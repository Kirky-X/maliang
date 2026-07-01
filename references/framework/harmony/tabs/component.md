# Tabs 组件 API 文档

> ArkTS 选项卡组件,用于在多个视图间切换。`Tabs` 为容器,`TabContent` 为单页内容。

## 组件定义

`Tabs` 通过 `TabContent` 子组件组织多个标签页,提供顶部/底部/侧边标签栏,支持滑动切换。

## 构造函数

```arkts
Tabs(value?: { barPosition?: BarPosition; index?: number; controller?: TabsController })

TabContent(value?: { tabBar?: TabBarOptions | SubTabBarStyle | BottomTabBarStyle })
```

## 核心属性表

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| barPosition | BarPosition | `Start` | 标签栏位置:Start(顶部)/End(底部) |
| barMode | BarMode | `Fixed` | 标签栏模式:Fixed/Scrollable |
| index | number | `0` | 当前激活页索引 |
| controller | TabsController | - | 控制器,用于编程式切换 |
| scrollable | boolean | `true` | 是否可滑动切换 |
| animationMode | AnimationMode | - | 切换动画模式 |
| onChange | (index: number) => void | - | 页面切换回调 |
| tabBar | SubTabBarStyle \| BottomTabBarStyle | - | 标签样式 |

## BarPosition 枚举

| 值 | 描述 | 场景 |
| --- | --- | --- |
| `Start` | 顶部 | 内容浏览(默认) |
| `End` | 底部 | 主导航 |

## 最小示例

```arkts
@Entry
@Component
struct TabsDemo {
  build() {
    Tabs() {
      TabContent() {
        Text('首页').fontSize({font-size-md})
      }.tabBar('首页')

      TabContent() {
        Text('我的').fontSize({font-size-md})
      }.tabBar('我的')
    }
    .barPosition(BarPosition.Start)
    .onChange((i: number) => console.info(`切换到 ${i}`))
  }
}
```

## 关联组件

- [`navigation`](../navigation/component.md) — 顶部 Tab 常与 Navigation 配合做主导航
- [`layout`](../layout/component.md) — Tabs 内部基于线性布局

## 参考链接

- ArkTS 官方文档 - 选项卡 (Tabs): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-navigation-tabs
