# Popconfirm 使用场景与示例

> 列举 ArkTS 气泡确认的典型场景:删除、注销、退款等破坏性操作二次确认。规范:危险色 + 明确宾语 + 非危险默认。

## 场景 1:列表项删除(轻量气泡)

```arkts
@Entry
@Component
struct DeletePopconfirmPage {
  @State popupIndex: number = -1
  @State items: string[] = ['地址一', '地址二', '地址三']

  @Builder
  ConfirmBubble(idx: number) {
    Column({ space: {spacing-sm} }) {
      Text(`确认删除"${this.items[idx]}"?`).fontSize({font-size-sm})
      Row({ space: {spacing-md} }) {
        Button('取消', { buttonStyle: ButtonStyleMode.TEXTUAL })
          .fontSize({font-size-sm})
          .fontColor({color-text-primary})
          .onClick(() => this.popupIndex = -1)
        Button('删除', { buttonStyle: ButtonStyleMode.TEXTUAL })
          .fontSize({font-size-sm})
          .fontColor({color-error})
          .onClick(() => {
            this.items.splice(idx, 1)
            this.popupIndex = -1
            promptAction.showToast({ message: '已删除' })
          })
      }
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-md})
  }

  build() {
    List({ space: {spacing-sm} }) {
      ForEach(this.items, (item: string, idx: number) => {
        ListItem() {
          Row() {
            Text(item).fontSize({font-size-md}).layoutWeight(1)
            Button('删除', { buttonStyle: ButtonStyleMode.TEXTUAL })
              .fontColor({color-error})
              .bindPopup(this.popupIndex === idx, {
                builder: this.ConfirmBubble(idx),
                placement: Placement.Bottom
              })
              .onClick(() => this.popupIndex = idx)
          }
          .padding({spacing-md})
          .backgroundColor({color-bg-primary})
          .borderRadius({radius-md})
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:注销账户(升级为弹窗确认)

不可逆且后果严重的操作不使用气泡,升级 `AlertDialog`:

```arkts
@Entry
@Component
struct CancelAccountPage {
  build() {
    Button('注销账户', { buttonStyle: ButtonStyleMode.NORMAL })
      .fontColor({color-error})
      .onClick(() => {
        AlertDialog.show({
          title: '确认注销账户?',
          message: '注销后所有数据将被清空且无法恢复',
          primaryButton: {
            value: '取消',
            action: () => {}
          },
          secondaryButton: {
            value: '确认注销',
            fontColor: {color-error},
            action: () => {
              // 执行注销
            }
          },
          cancel: () => {}
        })
      })
  }
}
```

## 场景 3:退款确认(明确宾语 + 非危险默认)

```arkts
@Entry
@Component
struct RefundConfirmPage {
  @State popup: boolean = false

  build() {
    Column({ space: {spacing-md} }) {
      Button('申请退款')
        .bindPopup(this.popup, {
          builder: () => {
            Column({ space: {spacing-sm} }) {
              Text('确认申请退款 ¥128.00?').fontSize({font-size-sm})
              Text('退款将在 1-3 个工作日原路退回')
                .fontSize({font-size-sm}).fontColor({color-text-secondary})
              Row({ space: {spacing-md} }) {
                Button('再想想', { buttonStyle: ButtonStyleMode.TEXTUAL })
                  .fontSize({font-size-sm})
                  .onClick(() => this.popup = false)
                Button('确认申请', { buttonStyle: ButtonStyleMode.TEXTUAL })
                  .fontSize({font-size-sm})
                  .fontColor({color-primary})
                  .onClick(() => {
                    this.popup = false
                    promptAction.showToast({ message: '退款申请已提交' })
                  })
              }
            }
            .padding({spacing-md})
            .backgroundColor({color-bg-primary})
            .borderRadius({radius-md})
          },
          placement: Placement.Top
        })
        .onClick(() => this.popup = true)
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **确认按钮语义** — 确认按钮写具体动作("删除""确认注销"),不写"确定";取消为非危险默认样式。
2. **危险色仅用于破坏性动作** — `color-error` 只给不可逆/扣款动作;普通提交用 `{color-primary}`。
3. **明确宾语** — 气泡文案带对象(`"地址一"` / `¥128.00`),不含糊。
4. **分级** — 轻量删除用气泡;不可逆/大额用 AlertDialog 弹窗(明确后果)。
5. **无障碍** — 气泡获得焦点、Esc 可关;按钮带语义文本,读屏完整播报问题与选项。
