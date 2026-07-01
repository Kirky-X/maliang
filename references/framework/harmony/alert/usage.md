# Alert 使用场景与示例

> 列举 ArkTS 警告提示的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:删除确认弹窗

```arkts
@Entry
@Component
struct DeleteAlertPage {
  build() {
    Column() {
      Button('删除项目')
        .backgroundColor({color-danger})
        .fontColor({color-text-on-primary})
        .onClick(() => {
          AlertDialog.show({
            title: '确认删除',
            message: '删除后将无法恢复,是否继续?',
            primaryButton: {
              value: '取消',
              action: () => console.info('取消')
            },
            secondaryButton: {
              value: '删除',
              fontColor: {color-danger},
              action: () => this.doDelete()
            }
          })
        })
    }
    .padding({spacing-md})
  }
  doDelete() { console.info('已删除') }
}
```

## 场景 2:退出登录确认(promptAction)

```arkts
import { promptAction } from '@kit.ArkUI'

@Entry
@Component
struct LogoutAlertPage {
  build() {
    Column() {
      Button('退出登录')
        .onClick(() => {
          promptAction.showDialog({
            title: '提示',
            message: '确认退出当前账号?',
            buttons: [
              { text: '取消', color: {color-text-primary} },
              { text: '退出', color: {color-danger} }
            ]
          }).then((res) => {
            if (res.index === 1) console.info('已退出')
          })
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:自定义内容告警(CustomDialog)

```arkts
@CustomDialog
struct WarningDialog {
  controller: CustomDialogController
  message: string = ''
  onConfirm: () => void = () => {}
  build() {
    Column({ space: {spacing-md} }) {
      Row({ space: {spacing-sm} }) {
        SymbolGlyph($r('sys.symbol.exclamationmark_triangle'))
          .fontColor([{color-warning}])
          .fontSize({font-size-lg})
        Text('警告').fontSize({font-size-md}).fontWeight(FontWeight.Bold)
      }
      Text(this.message).fontSize({font-size-sm}).fontColor({color-text-primary})
      Row() {
        Button('取消').layoutWeight(1).backgroundColor({color-bg-secondary}).fontColor({color-text-primary})
          .onClick(() => this.controller.close())
        Button('确认').layoutWeight(1).backgroundColor({color-warning}).fontColor({color-text-on-primary})
          .onClick(() => { this.onConfirm(); this.controller.close() })
      }
    }
    .padding({spacing-lg})
  }
}

@Entry
@Component
struct CustomAlertPage {
  private controller: CustomDialogController = new CustomDialogController({
    builder: WarningDialog({ message: '余额不足,请充值', onConfirm: () => console.info('去充值') }),
    alignment: DialogAlignment.Center
  })
  build() {
    Column() {
      Button('查看余额')
        .onClick(() => this.controller.open())
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **AlertDialog 已不推荐** — 官方建议用 `promptAction.showDialog`,功能等价且 API 更现代。
2. **危险操作用 CustomDialog** — 需自定义图标/颜色警示时用 CustomDialog;简单确认用 AlertDialog。
3. **按钮顺序** — primaryButton 在左(取消),secondaryButton 在右(确认);遵循平台习惯。
4. **fontColor 强调** — 危险按钮 `fontColor: {color-danger}` 区分语义;不可全部同色。
5. **避免滥用** — Alert 是中断式反馈,仅用于必须用户决策的场景;普通结果用 Toast。
6. **回调异步** — `promptAction.showDialog` 返回 Promise,用 `.then` 取索引;不要依赖同步返回。
