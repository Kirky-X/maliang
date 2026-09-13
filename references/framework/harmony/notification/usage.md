# Notification 使用场景与示例

> 列举 ArkTS 应用内通知横幅/消息中心的典型场景。与 message(toast)的分工:notification 常驻、可操作、支持多行;toast 短暂即逝。

## 场景 1:离线/同步状态常驻横幅

```arkts
@Entry
@Component
struct OfflineBannerPage {
  @State offline: boolean = true
  build() {
    Stack({ alignContent: Alignment.Top }) {
      Column() {
        Text('内容区').fontSize({font-size-md})
      }.width('100%')
      if (this.offline) {
        Row({ space: {spacing-sm} }) {
          Image($r('sys.media.ohos_ic_public_fail'))
            .width(20).height(20).fillColor({color-warning})
          Text('当前处于离线状态,数据将在联网后同步')
            .fontSize({font-size-sm}).layoutWeight(1)
        }
        .width('100%')
        .padding({spacing-md})
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-md})
        .margin({ top: {spacing-sm} })
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:带操作按钮的失败通知(重试)

```arkts
@Entry
@Component
struct ActionBannerPage {
  @State show: boolean = true
  build() {
    Stack({ alignContent: Alignment.Top }) {
      Text('主体内容').fontSize({font-size-md})
      if (this.show) {
        Row({ space: {spacing-md} }) {
          Column({ space: 4 }) {
            Text('上传失败').fontSize({font-size-md}).fontWeight(FontWeight.Bold)
            Text('3 个附件未完成上传').fontSize({font-size-sm}).fontColor({color-text-secondary})
          }.alignItems(HorizontalAlign.Start).layoutWeight(1)
          Button('重试', { buttonStyle: ButtonStyleMode.TEXTUAL })
            .fontSize({font-size-sm})
            .fontColor({color-primary})
          Image($r('sys.media.ohos_ic_public_cancel'))
            .width(20).height(20)
            .onClick(() => this.show = false)
        }
        .width('100%')
        .padding({spacing-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .border({ width: 1, color: {color-border-default} })
        .margin({ top: {spacing-sm} })
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:消息中心入口 + 列表(应用层)

```arkts
@Entry
@Component
struct InboxPage {
  @State items: Array<{ title: string, unread: boolean }> = [
    { title: '订单已发货', unread: true },
    { title: '优惠券到账', unread: true },
    { title: '登录提醒', unread: false }
  ]
  build() {
    Column() {
      Row() {
        Text('消息中心').fontSize({font-size-lg}).layoutWeight(1)
        Badge({ value: this.items.filter((i: { unread: boolean }) => i.unread).length }) {
          Image($r('sys.media.ohos_ic_public_clock')).width(24).height(24)
        }
      }
      .width('100%')
      .padding({spacing-md})
      List({ space: {spacing-sm} }) {
        ForEach(this.items, (n: { title: string, unread: boolean }) => {
          ListItem() {
            Row({ space: {spacing-sm} }) {
              Text(n.title).fontSize({font-size-md}).layoutWeight(1)
              if (n.unread) {
                Circle({ width: 8, height: 8 }).fill({color-primary})
              }
            }
            .padding({spacing-md})
            .backgroundColor({color-bg-primary})
            .borderRadius({radius-md})
          }
        })
      }
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **与 toast 的选型** — 需要用户处理(重试/查看)或长时间驻留的用横幅;即发即忘的轻反馈用 toast。
2. **常驻语义** — sticky 横幅不自动消失,必须提供关闭按钮;非 sticky 自动消失时长建议 ≥8s(toast 为 1.5-5s)。
3. **最多一条横幅** — 顶部横幅同一时刻最多 1 条,多条排队或并入消息中心,避免堆叠遮挡。
4. **无障碍** — 横幅出现时用 `accessibilityText` 播报;关闭按钮必须有语义描述。
5. **层级** — 横幅位于 Stack 顶层,页面内容区避让高度(或覆盖式但可关闭)。
