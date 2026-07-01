# Navigation 组件 API 文档

> ArkTS 页面导航与路由组件,推荐使用 `Navigation` 组件(支持分栏、转场、跨包路由);`@ohos.router` 已不推荐但仍可用。

## 组件定义

`Navigation` 是容器型导航组件,通过 `NavDestination` 定义子页面,`NavPathStack` 管理路由栈。替代旧版 `@ohos.router` 的命令式路由。

## 核心组成

| 组成 | 说明 |
| --- | --- |
| `Navigation` | 导航容器,承载首页内容与子页面 |
| `NavDestination` | 子页面组件,通过 `@Builder` 注册到路由表 |
| `NavPathStack` | 路由栈,管理 push/pop/replace |
| `NavRouter` | 触发导航的入口(已弱化,推荐直接操作 NavPathStack) |

## Navigation 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| mode | NavigationMode | Auto(自适应)/Split(分栏)/Stack(单栏) |
| navBarWidth | Length | 分栏左侧宽度 |
| title | string \| CustomBuilder \| NavigationCommonTitle | 标题 |
| hideNavBar | boolean | 是否隐藏导航栏 |
| toolBar | CustomBuilder | 底部工具栏 |
| navPathStack | NavPathStack | 路由栈实例 |

## NavPathStack 常用方法

```arkts
pushPath({ name: string, param?: object })   // 入栈
pop()                                          // 出栈
popToName(name: string)                        // 出栈到指定页
replacePath({ name, param })                   // 替换栈顶
clear()                                        // 清空栈
```

## 最小示例

```arkts
@Entry
@Component
struct NavDemo {
  pathStack: NavPathStack = new NavPathStack()
  build() {
    Navigation(this.pathStack) {
      Column() {
        Button('跳详情')
          .onClick(() => this.pathStack.pushPath({ name: 'detail' }))
      }
    }
    .title('首页')
    .mode(NavigationMode.Auto)
  }
}
```

## 关联组件

- [`tabs`](../tabs/component.md) — 顶部 Tab 常作为 Navigation 首页内容
- [`drawer`](../drawer/component.md) — 模态页面(bindSheet)与导航互补

## 参考链接

- ArkTS 官方文档 - 设置组件导航和页面路由: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-set-navigation-routing
- 组件导航 (Navigation): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-navigation-navigation
- Navigation 子页面 (NavDestination): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-navigation-navdestination
- 页面路由 (@ohos.router)(不推荐): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-routing
