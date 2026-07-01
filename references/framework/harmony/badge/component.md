# Badge 组件 API 文档

> ArkTS 徽章组件 `Badge`,用于在子组件右上角/内容上叠加计数或圆点提示。

## 组件定义

`Badge` 是容器组件,包裹目标组件(如图标/头像),在其角标位置显示数字/圆点/文字。

## 构造函数

```arkts
Badge(value: {
  count?: number              // 计数(0 不显示)
  maxCount?: number           // 最大显示数,默认 99
  position?: BadgePosition    // 位置
  style?: BadgeStyle          // 样式
})
```

## BadgeStyle 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| badgeSize | Length | 徽章尺寸 |
| badgeColor | ResourceColor | 徽章颜色,用 `{color-danger}` |
| badgeTextColor | ResourceColor | 文字颜色 |
| badgeFont | Font | 文字样式 |
| borderColor | ResourceColor | 边框色(与底色区分) |
| borderWidth | Length | 边框宽度 |

## BadgePosition 枚举

| 值 | 说明 |
| --- | --- |
| RightTop | 右上(默认) |
| Right | 右侧中 |
| Left | 左侧中 |

## 最小示例

```arkts
@Entry
@Component
struct BadgeDemo {
  build() {
    Badge({ count: 5, style: { badgeColor: {color-danger}, badgeSize: 16 } }) {
      SymbolGlyph($r('sys.symbol.bell'))
        .fontSize({font-size-lg})
        .fontColor([{color-text-primary}])
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`avatar`](../avatar/component.md) — 头像角标
- [`icon`](../icon/component.md) — 图标徽章

## 参考链接

- ArkTS 官方文档:无独立章节(Badge 属通用组件,散见于各组件文档)
- 相关组件:[`avatar`](../avatar/component.md) / [`icon`](../icon/component.md)
- 按钮与选择组件概述: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-forms-overview
