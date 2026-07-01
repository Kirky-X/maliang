# Input 使用场景与示例

> 列举 ArkTS 文本输入组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:登录表单(用户名 + 密码)

```arkts
@Entry
@Component
struct LoginFormPage {
  @State username: string = ''
  @State password: string = ''
  build() {
    Column({ space: {spacing-md} }) {
      TextInput({ placeholder: '用户名' })
        .height(48)
        .fontSize({font-size-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .onChange((v: string) => this.username = v)

      TextInput({ placeholder: '密码' })
        .type(InputType.Password)
        .height(48)
        .fontSize({font-size-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .onChange((v: string) => this.password = v)

      Button('登录')
        .width('100%')
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-lg})
  }
}
```

## 场景 2:搜索框(Search)

```arkts
@Entry
@Component
struct SearchPage {
  @State keyword: string = ''
  build() {
    Column() {
      Search({ placeholder: '搜索商品' })
        .height(40)
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-full})
        .onChange((v: string) => this.keyword = v)
        .onSubmit(() => this.doSearch())
    }
    .padding({spacing-md})
  }
  doSearch() { console.info(`搜索: ${this.keyword}`) }
}
```

## 场景 3:多行文本(TextArea)

```arkts
@Entry
@Component
struct TextAreaPage {
  @State content: string = ''
  build() {
    Column() {
      TextArea({ placeholder: '请输入备注,最多200字' })
        .width('100%').height(120)
        .fontSize({font-size-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .maxLength(200)
        .onChange((v: string) => this.content = v)
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:数字输入(回车键 Next)

```arkts
@Entry
@Component
struct NumberInputPage {
  build() {
    Column({ space: {spacing-md} }) {
      TextInput({ placeholder: '手机号' })
        .type(InputType.PhoneNumber)
        .maxLength(11)
        .enterKeyType(EnterKeyType.Next)
        .backgroundColor({color-bg-primary})
      TextInput({ placeholder: '验证码' })
        .type(InputType.Number)
        .maxLength(6)
        .enterKeyType(EnterKeyType.Done)
        .backgroundColor({color-bg-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:双向绑定($$ 语法)

```arkts
@Entry
@Component
struct BindingInputPage {
  @State value: string = ''
  build() {
    Column() {
      TextInput({ text: $$this.value })
        .backgroundColor({color-bg-primary})
      Text(`已输入: ${this.value}`)
        .fontSize({font-size-sm})
        .fontColor({color-text-primary})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **$$ 双向绑定** — `$$this.value` 直接绑定状态变量,无需在 `onChange` 手动赋值;仅系统组件支持。
2. **密码类型** — `InputType.Password` 会自动隐藏字符,无需自行处理。
3. **enterKeyType** — 影响键盘回车键文案,但不自动切换焦点;需在 `onSubmit` 中调用 `focusControl` 切换。
4. **maxLength** — 限制字符数(非字节);中文按 1 字符计。
5. **软键盘遮挡** — 输入框位于屏幕底部时,用 `expandSafeArea` 或监听键盘高度上移布局。
6. **Search 的 onSubmit** — 仅点击搜索图标或回车触发;实时搜索监听 `onChange`。
