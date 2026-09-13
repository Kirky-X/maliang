# Popconfirm 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Popconfirm 气泡确认组件。** 通过 `bindPopup` 自定义气泡构建(危险色确认 + 取消按钮)或 `AlertDialog`(轻量确认弹窗)组合实现破坏性操作二次确认。

## 缺失原因

ArkUI 原生 `bindPopup` 仅提供简单文本气泡与系统确认气泡(`enableArrow` 形态),无"确认/取消双按钮 + 危险色"的 Popconfirm 完整形态。

## 替代方案(组合结构)

| 角色 | ArkTS 实现 |
| --- | --- |
| 气泡容器 | `bindPopup`(builder 自定义气泡内容) |
| 确认/取消按钮 | `Row` + `Button`(确认用危险色 `{color-error}`) |
| 轻量替代 | `AlertDialog.show()`(按钮含危险色确认) |

## 组合结构

```arkts
@Builder
function ConfirmPopup(onConfirm: () => void, onCancel: () => void) {
  Column({ space: {spacing-sm} }) {
    Text('确认删除该地址?').fontSize({font-size-sm})
    Row({ space: {spacing-sm} }) {
      Button('取消', { buttonStyle: ButtonStyleMode.TEXTUAL })
        .fontSize({font-size-sm}).onClick(onCancel)
      Button('删除', { buttonStyle: ButtonStyleMode.TEXTUAL })
        .fontSize({font-size-sm}).fontColor({color-error}).onClick(onConfirm)
    }
  }
  .padding({spacing-md})
  .backgroundColor({color-bg-primary})
  .borderRadius({radius-md})
}
```

## 最小示例

```arkts
@Entry
@Component
struct PopconfirmDemo {
  @State popup: boolean = false

  build() {
    Column({ space: {spacing-md} }) {
      Button('删除', { buttonStyle: ButtonStyleMode.NORMAL })
        .fontColor({color-error})
        .bindPopup(this.popup, {
          builder: ConfirmPopup(
            () => { // 确认:执行删除
              this.popup = false
              promptAction.showToast({ message: '已删除' })
            },
            () => this.popup = false // 取消
          ),
          placement: Placement.Top,
          popup: new PopupOptions({ message: '' })
        })
        .onClick(() => this.popup = !this.popup)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`dialog`](../dialog/component.md) — 重确认(不可逆操作升级弹窗)
- [`popover`](../popover/component.md) — 气泡容器基础
- [`message`](../message/component.md) — 确认后结果反馈

## 参考链接

- ArkTS API 参考 - Popup(气泡提示): https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-components-popup
- ArkTS API 参考 - AlertDialog: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/js-apis-alertdialog
