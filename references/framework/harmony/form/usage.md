# Form 使用场景与示例

> ArkTS 无原生 Form 容器,本文件给出基于 Column + 状态管理的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础登录表单(Column 组合)

```arkts
@Entry
@Component
struct LoginFormPage {
  @State username: string = ''
  @State password: string = ''
  @State errorMsg: string = ''

  build() {
    Column({ space: {spacing-md} }) {
      Text('登录').fontSize({font-size-xl}).fontWeight(FontWeight.Bold)

      TextInput({ placeholder: '用户名' })
        .height(48)
        .fontSize({font-size-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .onChange((v: string) => this.username = v)

      TextInput({ placeholder: '密码' })
        .type(InputType.Password)
        .height(48)
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .onChange((v: string) => this.password = v)

      if (this.errorMsg.length > 0) {
        Text(this.errorMsg)
          .fontSize({font-size-sm})
          .fontColor({color-danger})
      }

      Button('提交')
        .width('100%')
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
        .onClick(() => this.submit())
    }
    .padding({spacing-lg})
  }

  submit() {
    if (this.username.length === 0) {
      this.errorMsg = '请输入用户名'
      return
    }
    this.errorMsg = ''
    // 提交逻辑
  }
}
```

## 场景 2:配置化表单(ForEach 渲染)

```arkts
interface FieldConfig { key: string; label: string; placeholder: string }

@Entry
@Component
struct ConfigFormPage {
  private fields: FieldConfig[] = [
    { key: 'name', label: '姓名', placeholder: '请输入姓名' },
    { key: 'phone', label: '电话', placeholder: '请输入电话' },
    { key: 'email', label: '邮箱', placeholder: '请输入邮箱' }
  ]
  @State values: Record<string, string> = {}

  build() {
    Column({ space: {spacing-md} }) {
      ForEach(this.fields, (f: FieldConfig) => {
        Column() {
          Text(f.label).fontSize({font-size-sm}).fontColor({color-text-primary})
          TextInput({ placeholder: f.placeholder })
            .height(44)
            .backgroundColor({color-bg-primary})
            .borderRadius({radius-md})
            .onChange((v: string) => this.values[f.key] = v)
        }
      })
      Button('保存')
        .width('100%')
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-lg})
  }
}
```

## 注意事项

1. **无内置校验** — 校验逻辑需在 `onClick` 手动实现,逐字段检查并展示错误信息。
2. **状态聚合** — 多字段建议用 `Record<string, string>` 或对象统一存储,避免大量 `@State`。
3. **键盘遮挡** — 底部提交按钮可能被键盘遮挡,监听键盘高度上移或用 `expandSafeArea`。
4. **复选协议** — 表单含协议勾选时,用 `Toggle` + `Text` 组合,无原生 checkbox 组件。
