# Navigation 使用场景与示例

> 列举 ArkTS 导航组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础页面跳转(push/pop)

```arkts
// 路由表(在入口文件或单独文件注册)
@Builder
function PageMap(name: string) {
  if (name === 'detail') {
    DetailPage()
  }
}

@Component
struct DetailPage {
  pathStack: NavPathStack = new NavPathStack()
  build() {
    NavDestination() {
      Column() {
        Text('详情页').fontSize({font-size-lg})
        Button('返回')
          .onClick(() => this.pathStack.pop())
          .backgroundColor({color-button-primary-bg})
          .fontColor({color-text-on-primary})
      }
    }
    .title('详情')
  }
}

@Entry
@Component
struct NavBasicPage {
  pathStack: NavPathStack = new NavPathStack()
  build() {
    Navigation(this.pathStack) {
      Column() {
        Button('查看详情')
          .onClick(() => this.pathStack.pushPath({ name: 'detail' }))
          .backgroundColor({color-button-primary-bg})
          .fontColor({color-text-on-primary})
      }
    }
    .navDestination(PageMap)
    .title('首页')
  }
}
```

## 场景 2:携带参数跳转

```arkts
// 推入
this.pathStack.pushPath({ name: 'detail', param: { id: 123 } })

// 取参(NavDestination)
@Component
struct DetailPage {
  @Consume pathStack: NavPathStack
  aboutToAppear() {
    const param = this.pathStack.getParamByName('detail')[0] as Record<string, number>
    console.info(`id = ${param.id}`)
  }
  build() { NavDestination() { Text('详情') } }
}
```

## 场景 3:分栏模式(平板适配)

```arkts
@Entry
@Component
struct SplitNavPage {
  pathStack: NavPathStack = new NavPathStack()
  build() {
    Navigation(this.pathStack) {
      List() {
        ForEach([1, 2, 3], (i: number) => {
          ListItem() {
            Text(`项 ${i}`).fontSize({font-size-md})
              .onClick(() => this.pathStack.pushPath({ name: 'detail', param: { id: i } }))
          }
        })
      }
    }
    .mode(NavigationMode.Split)
    .navBarWidth('40%')
    .title('列表')
  }
}
```

## 场景 4:底部主导航 + Navigation

```arkts
@Entry
@Component
struct TabNavPage {
  build() {
    Tabs({ barPosition: BarPosition.End }) {
      TabContent() {
        Navigation(new NavPathStack()) { Text('首页') }.title('首页')
      }.tabBar('首页')
      TabContent() {
        Navigation(new NavPathStack()) { Text('我的') }.title('我的')
      }.tabBar('我的')
    }
    .scrollable(false)
  }
}
```

## 注意事项

1. **必须注册 navDestination** — `Navigation().navDestination(PageMap)` 指向 `@Builder` 函数,否则 push 后白屏。
2. **NavPathStack 实例隔离** — 每个 Navigation 应使用独立栈实例;Tabs 内多 Tab 不可共享同一栈。
3. **NavDestination 取参** — 用 `pathStack.getParamByName(name)` 返回数组,取 `[0]`。
4. **mode=Auto** — 宽屏自动分栏,窄屏单栏;固定模式用 `Split` / `Stack`。
5. **Router 已不推荐** — `@ohos.router` 不支持分栏与跨包路由,新代码统一用 Navigation。
6. **转场动画** — 默认转场;自定义用 `customNavContentTransition`。
