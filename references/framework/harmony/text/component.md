# Text 组件 API 文档

> ArkTS 声明式 UI 框架内置的文本展示组件,用于显示单行或多行文字。声明于 `build()` 方法内。

## 组件定义

`Text` 是 ArkTS 基础组件之一,通过 `Text(content)` 构造函数创建,展示一段文本。配合 `Span`、`ImageSpan` 可实现富文本(混排文字、图片、点击事件)。

## 构造函数

```arkts
// 普通文本
Text(content?: string | Resource)

// 富文本:在闭包内拼接 Span / ImageSpan 子组件
Text(content?: string | Resource) {
  Span('片段1')
  Span('片段2')
  ImageSpan($r('app.media.icon'))
}
```

## 核心属性表

| 属性           | 类型                              | 默认值                  | 说明                                            |
| -------------- | --------------------------------- | ----------------------- | ----------------------------------------------- |
| fontSize       | number \| string \| Resource      | `{font-size-body}`      | 字号                                            |
| fontColor      | ResourceColor                     | `{color-text-primary}`  | 文字颜色                                        |
| fontWeight     | number \| FontWeight              | `FontWeight.Regular`    | 字重                                            |
| fontFamily     | string \| Resource                | -                       | 字体族                                          |
| fontStyle      | FontStyle                         | `FontStyle.Normal`      | 字体样式:`Normal` / `Italic`                    |
| textAlign      | TextAlign                         | `TextAlign.Start`       | 对齐方式:`Start` / `Center` / `End` / `Justify` |
| lineHeight     | number \| string \| Resource      | -                       | 行高                                            |
| maxLines       | number                            | -                       | 最大行数;超出按 `textOverflow` 处理             |
| textOverflow   | TextOverflow                      | `TextOverflow.Clip`     | 溢出处理:`Clip` / `Ellipsis` / `None`           |
| letterSpacing  | number \| string                  | `0`                      | 字间距                                          |
| textDecoration | TextDecoration                    | `TextDecoration.None`   | 文字装饰:`None` / `Underline` / `LineThrough`   |
| copyOption     | CopyOptions                       | `CopyOptions.None`      | 是否允许长按复制:`None` / `LocalDevice` / `CrossDevice` |
| baselineOffset | number \| string                  | `0`                      | 基线偏移                                        |
| textShadow     | ShadowOptions                     | -                       | 文字阴影                                        |

## TextAlign 枚举

| 值        | 描述       | 使用场景                          |
| --------- | ---------- | --------------------------------- |
| `Start`   | 左对齐(默认) | 段落正文、列表项                  |
| `Center`  | 居中对齐   | 标题、按钮文字、空状态提示        |
| `End`     | 右对齐     | 数值、时间戳                      |
| `Justify` | 两端对齐   | 多行长文本(文章正文)            |

## 最小示例

```arkts
@Entry
@Component
struct TextDemo {
  build() {
    Column() {
      Text('Hello ArkTS')
        .fontSize({font-size-md})
        .fontColor({color-text-primary})
        .textAlign(TextAlign.Center)
        .width('100%')
    }
    .padding({spacing-md})
  }
}
```

## 富文本子组件

### Span — 文本片段

```arkts
Text() {
  Span('协议阅读')
    .fontColor({color-text-secondary})
  Span('《用户协议》')
    .fontColor({color-text-link})
    .decoration({ type: TextDecorationType.Underline })
}
```

### ImageSpan — 行内图片

```arkts
Text() {
  Span('提示')
  ImageSpan($r('app.media.icon_info'))
    .width(16)
    .height(16)
    .verticalAlign(ImageSpanAlignment.CENTER)
}
```

## 关联组件

- [`Button`](../button/component.md) — 按钮内文本由 Button 自身管理,不嵌套 Text
- [`List`](../list/component.md) — ListItem 内常用 Text 展示标题与描述
