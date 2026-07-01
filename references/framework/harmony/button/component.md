# Button 组件 API 文档

> ArkTS 声明式 UI 框架内置的按钮组件,用于触发用户交互动作。基于 `@Component` 装饰器,声明于 `build()` 方法内。

## 组件定义

`Button` 是 ArkTS 通用组件之一,通过 `Button(...)` 构造函数创建,支持文本标签、自定义子组件两种形式。常用于表单提交、导航跳转、动作触发等场景。

## 构造函数

```arkts
// 文本按钮:直接传入字符串标签
Button(label?: string, options?: { type?: ButtonType; stateEffect?: boolean })

// 自定义内容按钮:在闭包内放置子组件(图标/文本/混合)
Button(options?: { type?: ButtonType; stateEffect?: boolean; controller?: ButtonController })
```

## 核心属性表

| 属性            | 类型                              | 默认值                     | 说明                                          |
| --------------- | --------------------------------- | -------------------------- | --------------------------------------------- |
| type            | ButtonType                        | `ButtonType.Capsule`       | 按钮形状:`Capsule`(胶囊)/`Circle`(圆形)/`Normal`(矩形) |
| stateEffect     | boolean                           | `true`                     | 是否显示按压态视觉反馈                         |
| labelStyle      | LabelStyle                        | -                          | 文本标签样式(字号/字重/颜色)                  |
| fontSize        | number \| string \| Resource      | `{font-size-md}`           | 文本字号                                      |
| fontColor       | ResourceColor                     | `{color-text-on-primary}`  | 文本颜色                                      |
| fontWeight      | number \| FontWeight              | `FontWeight.Medium`        | 字重                                          |
| backgroundColor | ResourceColor                     | `{color-button-primary-bg}`| 背景色                                        |
| borderRadius    | number \| string \| Resource      | `{radius-md}`              | 圆角(仅 `Normal` 类型生效)                    |
| borderColor     | ResourceColor                     | -                          | 边框颜色                                      |
| borderWidth     | number \| string \| Resource      | `0`                         | 边框宽度                                      |
| enabled         | boolean                           | `true`                     | 是否启用;`false` 时进入禁用态                 |
| opacity         | number \| Resource                | `1`                         | 透明度,禁用态使用 `{opacity-disabled}`        |
| onClick         | (event: ClickEvent) => void       | -                          | 点击事件回调                                  |
| stateStyles     | StateStyles                       | -                          | 各状态(pressed/normal/disabled)样式           |

## ButtonType 枚举

| 值        | 描述                              | 使用场景               |
| --------- | --------------------------------- | ---------------------- |
| `Capsule` | 胶囊形,圆角=高度/2(默认)         | 主要/次要操作按钮      |
| `Circle`  | 正圆形                            | 图标按钮、工具栏操作   |
| `Normal`  | 矩形,圆角由 `borderRadius` 控制   | 表单、工具栏按钮       |

## 最小示例

```arkts
@Entry
@Component
struct ButtonDemo {
  build() {
    Column() {
      // 文本按钮(默认胶囊形)
      Button('点击我')
        .fontSize({font-size-md})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-button-primary-bg})
        .onClick(() => {
          console.info('按钮被点击')
        })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`Text`](../text/component.md) — 按钮内文本样式可参考 Text 的字体属性
- [`List`](../list/component.md) — 列表项内常嵌入 Button 作为操作入口
