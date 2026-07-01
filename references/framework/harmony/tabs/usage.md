# Tabs 使用场景与示例

> 列举 ArkTS Tabs 组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:顶部选项卡(子页面切换)

```arkts
@Entry
@Component
struct TopTabsPage {
  build() {
    Tabs({ barPosition: BarPosition.Start }) {
      TabContent() {
        Column() { Text('推荐内容').fontSize({font-size-md}) }.width('100%')
      }.tabBar('推荐')

      TabContent() {
        Column() { Text('关注内容').fontSize({font-size-md}) }.width('100%')
      }.tabBar('关注')

      TabContent() {
        Column() { Text('热门内容').fontSize({font-size-md}) }.width('100%')
      }.tabBar('热门')
    }
    .barMode(BarMode.Fixed)
    .onChange((i: number) => console.info(`当前 ${i}`))
  }
}
```

## 场景 2:底部导航栏(主导航)

```arkts
@Entry
@Component
struct BottomTabsPage {
  build() {
    Tabs({ barPosition: BarPosition.End }) {
      TabContent() {
        Column() { Text('首页').fontSize({font-size-md}) }
      }.tabBar(this.tabStyle('首页', $r('app.media.ic_home')))

      TabContent() {
        Column() { Text('我的').fontSize({font-size-md}) }
      }.tabBar(this.tabStyle('我的', $r('app.media.ic_me')))
    }
    .scrollable(false)
  }

  tabStyle(text: string, icon: Resource) {
    return ({ normalIcon: icon, selectedIcon: icon, text: text } as BottomTabBarStyle)
  }
}
```

## 场景 3:可滚动标签栏(多分类)

```arkts
@Entry
@Component
struct ScrollTabsPage {
  private cats: string[] = ['全部', '科技', '财经', '体育', '娱乐', '教育', '健康', '旅行']
  build() {
    Tabs({ barPosition: BarPosition.Start }) {
      ForEach(this.cats, (cat: string) => {
        TabContent() {
          Column() { Text(`${cat}内容`).fontSize({font-size-md}) }
        }.tabBar(cat)
      })
    }
    .barMode(BarMode.Scrollable)
  }
}
```

## 场景 4:编程式切换(控制器)

```arkts
@Entry
@Component
struct ControllerTabsPage {
  private controller: TabsController = new TabsController()
  @State current: number = 0

  build() {
    Column() {
      Tabs({ controller: this.controller }) {
        TabContent() { Text('第1页') }.tabBar('1')
        TabContent() { Text('第2页') }.tabBar('2')
      }
      .onChange((i: number) => this.current = i)

      Button('跳到第2页')
        .onClick(() => this.controller.changeIndex(1))
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **底部主导航禁用滑动** — 主导航 `scrollable(false)`,避免误触切换页面。
2. **barMode Scrollable** — 标签数超过 5 个时启用 `Scrollable`,标签栏可横向滚动。
3. **controller.changeIndex** — 编程式切换会触发 `onChange`,需注意循环触发风险。
4. **BottomTabBarStyle** — 底部导航需用 `BottomTabBarStyle` 设置图标与文字,普通 `tabBar('文本')` 无图标。
5. **TabContent 必须有 tabBar** — 缺失 `tabBar` 的 TabContent 不会显示标签。
6. **状态保持** — 默认切换会销毁非当前页;需保持状态用 `@State` 提升或 Navigation 管理。
