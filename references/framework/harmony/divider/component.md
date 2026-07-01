# Divider 组件 API 文档

> ArkTS 分割线组件 `Divider`,用于在内容间添加水平/垂直分隔线。

## 组件定义

`Divider` 是独立组件,默认水平分割线;通过 `vertical(true)` 改为垂直。常置于 `Column`/`Row` 间分隔内容块。

## 构造函数

```arkts
Divider()
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| color | ResourceColor | 线颜色,用 `{color-border-default}` |
| strokeWidth | Length | 线宽,默认 1 |
| vertical | boolean | 是否垂直,默认 false |
| lineCap | LineCapStyle | 端点样式 |
| strokeDashArray | Length[] | 虚线段 |

## 最小示例

```arkts
@Entry
@Component
struct DividerDemo {
  build() {
    Column() {
      Text('内容一').fontSize({font-size-md})
      Divider().color({color-border-default}).strokeWidth(1)
      Text('内容二').fontSize({font-size-md})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`list`](../list/component.md) — 列表项间分隔
- [`shape`](../shape/component.md) — 自定义虚线用 Line

## 参考链接

- ArkTS 官方文档:无独立章节(Divider 属通用组件,散见布局文档)
- 相关组件:[`list`](../list/component.md)
- 组件布局: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development
