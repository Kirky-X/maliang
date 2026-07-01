# Dialog 使用场景与示例

> 列举 ArkTS 弹窗组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:确认弹窗(AlertDialog)

```arkts
@Entry
@Component
struct ConfirmDialogPage {
  build() {
    Column() {
      Button('删除')
        .backgroundColor({color-danger})
        .fontColor({color-text-on-primary})
        .onClick(() => this.confirmDelete())
    }
    .padding({spacing-md})
  }
  confirmDelete() {
    AlertDialog.show({
      title: '提示',
      message: '确认删除该项?删除后不可恢复',
      primaryButton: {
        value: '取消',
        action: () => console.info('取消')
      },
      secondaryButton: {
        value: '删除',
        fontColor: {color-danger},
        action: () => console.info('已删除')
      }
    })
  }
}
```

## 场景 2:自定义内容弹窗(CustomDialog)

```arkts
@CustomDialog
struct InputDialog {
  controller: CustomDialogController
  @State value: string = ''
  onConfirm: (v: string) => void = () => {}
  build() {
    Column({ space: {spacing-md} }) {
      Text('请输入备注').fontSize({font-size-lg})
      TextInput({ placeholder: '备注' })
        .height(44)
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-md})
        .onChange((v: string) => this.value = v)
      Row() {
        Button('取消')
          .layoutWeight(1)
          .backgroundColor({color-bg-secondary})
          .fontColor({color-text-primary})
          .onClick(() => this.controller.close())
        Button('确认')
          .layoutWeight(1)
          .backgroundColor({color-button-primary-bg})
          .fontColor({color-text-on-primary})
          .onClick(() => { this.onConfirm(this.value); this.controller.close() })
      }
    }
    .padding({spacing-lg})
  }
}

@Entry
@Component
struct CustomDialogPage {
  private controller: CustomDialogController = new CustomDialogController({
    builder: InputDialog({ onConfirm: (v: string) => console.info(v) }),
    autoCancel: true,
    alignment: DialogAlignment.Center
  })
  build() {
    Column() {
      Button('打开')
        .onClick(() => this.controller.open())
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:底部弹窗(BottomSheet 风格)

```arkts
@Entry
@Component
struct BottomDialogPage {
  private controller: CustomDialogController = new CustomDialogController({
    builder: MyDialog(),
    alignment: DialogAlignment.Bottom,
    customStyle: true
  })
  build() {
    Column() {
      Button('底部弹窗')
        .onClick(() => this.controller.open())
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:拦截关闭(onWillDismiss)

```arkts
private controller: CustomDialogController = new CustomDialogController({
  builder: MyDialog(),
  autoCancel: false,
  onWillDismiss: (action: DismissDialogAction) => {
    // 表单未保存时阻止关闭
    if (this.unsaved) {
      action.dismiss()  // 显式调用才关闭
    }
  }
})
```

## 注意事项

1. **Controller 生命周期** — `CustomDialogController` 必须作为组件成员变量声明,不能在 build 内 new。
2. **customStyle** — 自定义底部弹窗需设 `customStyle: true` 去除默认白色圆角背景,否则样式冲突。
3. **autoCancel** — 表单类弹窗建议 `autoCancel: false`,避免误触遮罩丢失输入。
4. **AlertDialog 已不推荐** — 官方建议用 `promptAction.showDialog` 替代 `AlertDialog.show`。
5. **嵌套弹窗** — 弹窗内再开弹窗需注意层级,后开的在上;避免栈过深。
6. **回调传参** — `CustomDialog` 向父组件传值用构造参数传入回调函数(如 `onConfirm`)。
