# List 使用场景与示例

> 列举 HarmonyOS 应用中 List 组件的典型使用场景、完整代码示例与注意事项。所有颜色/间距通过 design token 引用,不硬编码。

## 场景 1:基础纵向列表

设置页、菜单页等线性数据展示,使用 `ForEach` 渲染固定数据。ListItem 之间用 `space` 控制间距,`divider` 控制分割线。

```arkts
@Entry
@Component
struct BasicListPage {
  private items: string[] = ['账号设置', '通知管理', '隐私安全', '帮助与反馈', '关于']

  build() {
    List({ space: 0 }) {
      ForEach(this.items, (item: string) => {
        ListItem() {
          Row() {
            Text(item)
              .fontSize({font-size-md})
              .fontColor({color-text-primary})
              .layoutWeight(1)

            Text('>')
              .fontSize({font-size-md})
              .fontColor({color-text-tertiary})
          }
          .width('100%')
          .height(56)
          .padding({ left: {spacing-md}, right: {spacing-md} })
        }
      }, (item: string) => item)
    }
    .divider({
      strokeWidth: 1,
      color: {color-border-default},
      startMargin: {spacing-md},
      endMargin: 0
    })
    .width('100%')
    .height('100%')
  }
}
```

## 场景 2:横向滚动列表

横向滚动展示分类标签、卡片轮播等内容,设置 `listDirection(Axis.Horizontal)`。

```arkts
@Entry
@Component
struct HorizontalListPage {
  private tags: string[] = ['推荐', '科技', '设计', '产品', '运营', '市场']

  build() {
    List({ space: {spacing-sm} }) {
      ForEach(this.tags, (tag: string) => {
        ListItem() {
          Text(tag)
            .fontSize({font-size-sm})
            .fontColor({color-text-primary})
            .backgroundColor({color-bg-secondary})
            .padding({ left: {spacing-md}, right: {spacing-md}, top: {spacing-xs}, bottom: {spacing-xs} })
            .borderRadius({radius-sm})
        }
      }, (tag: string) => tag)
    }
    .listDirection(Axis.Horizontal)
    .scrollBar(BarState.Off)
    .padding({ left: {spacing-md}, right: {spacing-md} })
    .width('100%')
    .height(48)
  }
}
```

## 场景 3:分组列表(带粘性头部)

通讯录、城市选择等场景使用 `ListItemGroup` 分组,配合 `sticky` 让组头在滚动时悬浮。

```arkts
@Entry
@Component
struct GroupedListPage {
  @Builder groupHeader(title: string) {
    Text(title)
      .fontSize({font-size-sm})
      .fontColor({color-text-tertiary})
      .backgroundColor({color-bg-tertiary})
      .padding({ left: {spacing-md}, top: {spacing-sm}, bottom: {spacing-sm} })
      .width('100%')
  }

  build() {
    List() {
      ListItemGroup({ header: this.groupHeader('A') }) {
        ListItem() {
          Text('Alice')
            .fontSize({font-size-md})
            .fontColor({color-text-primary})
            .padding({spacing-md})
            .width('100%')
        }
        ListItem() {
          Text('Anna')
            .fontSize({font-size-md})
            .fontColor({color-text-primary})
            .padding({spacing-md})
            .width('100%')
        }
      }

      ListItemGroup({ header: this.groupHeader('B') }) {
        ListItem() {
          Text('Bob')
            .fontSize({font-size-md})
            .fontColor({color-text-primary})
            .padding({spacing-md})
            .width('100%')
        }
      }
    }
    .sticky(StickyStyle.Header)
    .divider({
      strokeWidth: 1,
      color: {color-border-default},
      startMargin: {spacing-md},
      endMargin: {spacing-md}
    })
    .width('100%')
    .height('100%')
  }
}
```

## 场景 4:懒加载长列表(LazyForEach)

数据量超过 100 条时,必须使用 `LazyForEach` 配合 `cachedCount` 实现按需渲染,避免一次性渲染导致卡顿。

```arkts
// 数据源必须实现 IDataSource 接口
class BasicDataSource implements IDataSource {
  private list: string[] = []
  private listeners: DataChangeListener[] = []

  totalCount(): number { return this.list.length }
  getData(idx: number): string { return this.list[idx] }

  pushData(data: string) {
    this.list.push(data)
    this.listeners.forEach(l => l.onDataChange(this.list.length - 1))
  }

  registerDataChangeListener(l: DataChangeListener) { this.listeners.push(l) }
  unregisterDataChangeListener(l: DataChangeListener) {
    const i = this.listeners.indexOf(l)
    if (i >= 0) this.listeners.splice(i, 1)
  }
}

@Entry
@Component
struct LazyListPage {
  private data: BasicDataSource = new BasicDataSource()

  aboutToAppear() {
    // 模拟初始化数据
    for (let i = 0; i < 50; i++) {
      this.data.pushData(`第 ${i + 1} 项`)
    }
  }

  build() {
    List({ space: {spacing-sm} }) {
      LazyForEach(this.data, (item: string) => {
        ListItem() {
          Text(item)
            .fontSize({font-size-md})
            .fontColor({color-text-primary})
            .padding({spacing-md})
            .width('100%')
            .backgroundColor({color-bg-primary})
            .borderRadius({radius-sm})
        }
      }, (item: string) => item)
    }
    .cachedCount(5)  // 预渲染 5 项,平衡流畅度与内存
    .divider({ strokeWidth: 1, color: {color-border-default} })
    .width('100%')
    .height('100%')
  }
}
```

## 场景 5:下拉刷新与上拉加载

配合 `onReachStart` / `onReachEnd` 回调实现分页加载与下拉刷新,使用 `Scroller` 控制滚动位置。

```arkts
@Entry
@Component
struct PullRefreshPage {
  private data: string[] = []
  @State isLoading: boolean = false
  private scroller: Scroller = new Scroller()
  private page: number = 1

  aboutToAppear() {
    this.loadMore()
  }

  private loadMore() {
    if (this.isLoading) return
    this.isLoading = true
    // 模拟异步请求
    setTimeout(() => {
      for (let i = 0; i < 20; i++) {
        this.data.push(`第 ${this.page} 页 - 第 ${i + 1} 条`)
      }
      this.page++
      this.isLoading = false
    }, 500)
  }

  build() {
    Column() {
      List({ scroller: this.scroller }) {
        ForEach(this.data, (item: string, idx: number) => {
          ListItem() {
            Row() {
              Text(item)
                .fontSize({font-size-md})
                .fontColor({color-text-primary})
                .layoutWeight(1)
              Text(`#${idx + 1}`)
                .fontSize({font-size-sm})
                .fontColor({color-text-tertiary})
            }
            .padding({spacing-md})
            .width('100%')
          }
        }, (item: string) => item)
      }
      .divider({ strokeWidth: 1, color: {color-border-default}, startMargin: {spacing-md} })
      .onReachStart(() => {
        console.info('已到达顶部,可触发下拉刷新')
      })
      .onReachEnd(() => {
        console.info('已到达底部,触发上拉加载')
        this.loadMore()
      })
      .edgeEffect(EdgeEffect.Spring)
      .layoutWeight(1)
      .width('100%')

      if (this.isLoading) {
        Text('加载中...')
          .fontSize({font-size-sm})
          .fontColor({color-text-tertiary})
          .padding({spacing-md})
          .width('100%')
          .textAlign(TextAlign.Center)
      }
    }
    .width('100%')
    .height('100%')
  }
}
```

## 注意事项

1. **LazyForEach vs ForEach** — 数据量 > 100 条必须使用 `LazyForEach`,否则一次性渲染所有 ListItem 会导致首屏卡顿与内存暴涨;< 50 条可使用 `ForEach`。
2. **cachedCount 调优** — 默认 `1` 偏小,滚动时易出现白屏;建议设为 5~10,平衡预渲染流畅度与内存占用。值过大反而抵消懒加载收益。
3. **ListItem 唯一键** — `ForEach` / `LazyForEach` 的第三个参数(键生成器)必须返回稳定唯一值,否则数据更新时会出现错位、闪烁。禁止用数组索引作为键。
4. **List 不能嵌套 List** — ArkTS 限制 List 不能作为 List 的直接子组件;横向 + 纵向混合布局应使用 `Scroll` + `Column` 包裹横向 List。
5. **space 与 divider 冲突** — 同时设置 `space` 和 `divider` 会在 ListItem 之间产生双重间距,建议二选一。需要分割线时优先用 `divider`,需要纯间距时用 `space`。
6. **侧滑操作性能** — `swipeAction` 在长列表中会影响滚动性能,建议仅在必要场景使用,且关闭 `edgeEffect` 以避免手势冲突。
7. **滚动到指定项** — 使用 `Scroller.scrollToIndex(idx)` 实现锚点跳转,注意索引需在数据范围内,且 `LazyForEach` 模式下需确保目标项已渲染。
