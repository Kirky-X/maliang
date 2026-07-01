# Loading 使用场景与示例

> 列举 ArkTS LoadingProgress 加载组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:全屏加载(居中转圈)

```arkts
@Entry
@Component
struct FullLoadingPage {
  @State loading: boolean = true
  build() {
    Stack() {
      if (this.loading) {
        Column({ space: {spacing-sm} }) {
          LoadingProgress().width(48).height(48).color({color-button-primary-bg})
          Text('加载中...').fontSize({font-size-sm}).fontColor({color-text-primary})
        }
      } else {
        Text('内容').fontSize({font-size-md})
      }
    }
    .width('100%').height('100%')
    .alignContent(Alignment.Center)
  }
}
```

## 场景 2:列表底部加载更多

```arkts
@Entry
@Component
struct ListLoadingPage {
  private data: number[] = [1, 2, 3, 4, 5]
  @State loadingMore: boolean = false
  build() {
    Column() {
      List() {
        ForEach(this.data, (n: number) => {
          ListItem() { Text(`项 ${n}`).padding({spacing-md}).fontSize({font-size-md}) }
        })
        if (this.loadingMore) {
          ListItem() {
            Row({ space: {spacing-sm} }) {
              LoadingProgress().width(24).height(24).color({color-button-primary-bg})
              Text('加载更多...').fontSize({font-size-sm}).fontColor({color-text-primary})
            }
            .width('100%').justifyContent(FlexAlign.Center)
            .padding({spacing-md})
          }
        }
      }
      .onReachEnd(() => { this.loadingMore = true; this.loadMore() })
    }
    .padding({spacing-md})
  }
  loadMore() { setTimeout(() => this.loadingMore = false, 1000) }
}
```

## 场景 3:按钮内加载(提交中)

```arkts
@Entry
@Component
struct ButtonLoadingPage {
  @State submitting: boolean = false
  build() {
    Column() {
      Button() {
        Row({ space: {spacing-xs} }) {
          if (this.submitting) {
            LoadingProgress().width(16).height(16).color({color-text-on-primary})
          }
          Text(this.submitting ? '提交中' : '提交').fontSize({font-size-md})
        }
      }
      .enabled(!this.submitting)
      .backgroundColor({color-button-primary-bg})
      .fontColor({color-text-on-primary})
      .onClick(() => { this.submitting = true; setTimeout(() => this.submitting = false, 2000) })
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:弹窗内加载

```arkts
@CustomDialog
struct LoadingDialog {
  controller: CustomDialogController
  build() {
    Column({ space: {spacing-md} }) {
      LoadingProgress().width(40).height(40).color({color-button-primary-bg})
      Text('处理中,请稍候').fontSize({font-size-sm}).fontColor({color-text-primary})
    }
    .padding({spacing-lg})
  }
}
```

## 注意事项

1. **LoadingProgress 无进度值** — 仅转圈动画;有百分比用 `Progress(Linear/Ring)`。
2. **color 控制** — 默认跟随主题;自定义用 `color({color-xxx})`。
3. **尺寸用 width/height** — 加载圈大小由宽高决定,建议 24-48 之间。
4. **避免全屏遮罩滥用** — 全屏加载遮挡操作,优先用局部加载或骨架屏。
5. **按钮内加载** — 提交中 `enabled(false)` 防重复点击,配合 LoadingProgress 反馈。
6. **加载完成清理** — 异步完成后将 `loading` 置 false,避免动画常驻耗电。
