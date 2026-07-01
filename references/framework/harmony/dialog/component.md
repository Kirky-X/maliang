# Dialog 组件 API 文档

> ArkTS 弹窗组件,包含 `CustomDialog`(自定义弹窗)、`AlertDialog`(确认弹窗)与 `promptAction`(命令式弹窗)。

## 组件定义

| 类型 | 用途 | 触发方式 |
| --- | --- | --- |
| `CustomDialog` | 自定义内容弹窗 | 声明式 + Controller |
| `AlertDialog` | 简单确认弹窗 | 静态方法 |
| `promptAction.showDialog` | 命令式弹窗 | API 调用 |

## CustomDialog 用法

```arkts
@CustomDialog
struct MyDialog {
  controller: CustomDialogController
  build() {
    Column() {
      Text('标题')
      Button('关闭').onClick(() => this.controller.close())
    }
  }
}

// 使用
dialogController: CustomDialogController = new CustomDialogController({
  builder: MyDialog(),
  autoCancel: true,
  alignment: DialogAlignment.Center
})
```

## CustomDialogController 配置

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| builder | CustomDialog | 弹窗内容构建器 |
| autoCancel | boolean | 点击遮罩是否关闭 |
| alignment | DialogAlignment | 对齐:Center/Top/Bottom |
| offset | { dx, dy } | 偏移量 |
| customStyle | boolean | 是否自定义样式(去除默认背景) |
| maskColor | ResourceColor | 遮罩颜色 |
| onWillDismiss | (DismissDialogAction) => void | 拦截关闭 |

## AlertDialog 用法

```arkts
AlertDialog.show({
  title: '提示',
  message: '确认删除?',
  primaryButton: { value: '取消', action: () => {} },
  secondaryButton: { value: '确认', fontColor: {color-danger}, action: () => {} }
})
```

## 最小示例

```arkts
@Entry
@Component
struct DialogDemo {
  dialogController: CustomDialogController = new CustomDialogController({ builder: MyDialog() })
  build() {
    Column() {
      Button('打开弹窗')
        .onClick(() => this.dialogController.open())
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`alert`](../alert/component.md) — 警告提示基于 AlertDialog
- [`message`](../message/component.md) — Toast 轻提示与 Dialog 区别
- [`drawer`](../drawer/component.md) — bindSheet 半模态与 Dialog 区别

## 参考链接

- ArkTS 官方文档 - 使用弹窗: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-use-dialog
- 弹出框 (Dialog): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-use-dialogs
- 基础自定义弹出框 (CustomDialog): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-custom-dialog
