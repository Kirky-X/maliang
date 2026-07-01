# Input 组件 API 文档

> ArkTS 文本输入组件,包含 `TextInput`(单行)、`TextArea`(多行)、`Search`(搜索框)三类。

## 组件定义

| 组件 | 用途 | 形态 |
| --- | --- | --- |
| `TextInput` | 单行文本输入 | 单行 |
| `TextArea` | 多行文本输入 | 多行可滚动 |
| `Search` | 搜索框(带搜索/清除图标) | 单行 + 图标 |

## 构造函数

```arkts
TextInput(value?: { placeholder?: string | Resource; text?: string | Resource; controller?: TextInputController })

TextArea(value?: { placeholder?: string | Resource; text?: string | Resource; controller?: TextAreaController })

Search(value?: { placeholder?: string | Resource; icon?: string | Resource })
```

## 核心属性表

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| type | InputType | 输入类型:Normal/Password/Email/Number/PhoneNumber |
| placeholderColor | ResourceColor | 占位文字颜色 |
| placeholderFont | Font | 占位文字样式 |
| caretColor | ResourceColor | 光标颜色 |
| maxLength | number | 最大字符数 |
| enterKeyType | EnterKeyType | 回车键类型:Go/Search/Send/Done/Next |
| fontSize | Length | 字号,用 `{font-size-md}` |
| fontColor | ResourceColor | 文字颜色,用 `{color-text-primary}` |
| backgroundColor | ResourceColor | 背景色,用 `{color-bg-primary}` |
| textAlign | TextAlign | 对齐方式 |
| copyOption | CopyOptions | 是否允许复制 |
| enableKeyboardOnFocus | boolean | 聚焦是否唤起键盘 |
| onChange | (value: string) => void | 输入变化回调 |
| onSubmit | (enterKey: EnterKeyType) => void | 回车回调 |
| onEditChange | (isEditing: boolean) => void | 编辑状态回调 |

## 最小示例

```arkts
@Entry
@Component
struct InputDemo {
  @State text: string = ''
  build() {
    Column() {
      TextInput({ placeholder: '请输入' })
        .fontSize({font-size-md})
        .fontColor({color-text-primary})
        .backgroundColor({color-bg-primary})
        .placeholderColor({color-text-primary})
        .onChange((v: string) => this.text = v)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`form`](../form/component.md) — 表单由多个输入组件组合(ArkTS 无原生 Form 容器)

## 参考链接

- ArkTS 官方文档 - 文本输入 (TextInput/TextArea/Search): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-text-input
- 管理软键盘: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-manage-keyboard
