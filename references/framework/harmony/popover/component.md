# Popover 组件 API 文档

> ArkTS 气泡提示组件。**注意:目录 slug 统一用 `popover`,ArkTS 原生组件名为 `Popup`。** 通过 `bindPopup` 绑定到触发组件。

## 组件定义

`Popup` 不独立渲染,通过 `bindPopup(show, options)` 绑定,点击/长按触发,常用于按钮提示、图标说明。

## 绑定方法

```arkts
.bindPopup(this.showPopup, {
  message: '提示内容',
  placement: Placement.Top,
  ...
})
```

## 核心配置(PopupOptions)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| message | string \| Resource | 提示文字 |
| placement | Placement | 位置:Top/Bottom/Left/Right 等 |
| color | ResourceColor | 背景色 |
| textColor | ResourceColor | 文字色 |
| duration | number | 显示时长(ms),默认 10000 |
| keepArrow | boolean | 是否保留箭头 |
| enableArrow | boolean | 是否显示箭头 |
| onStateChange | (state) => void | 显隐状态回调 |

## CustomPopupOptions(自定义内容)

```arkts
.bindPopup(this.show, {
  builder: this.popupBuilder,
  placement: Placement.Bottom,
  ...
})
```

## Placement 枚举(常用)

| 值 | 说明 |
| --- | --- |
| Top / Bottom | 上 / 下 |
| Left / Right | 左 / 右 |
| TopLeft / TopRight | 左上 / 右上 |
| BottomLeft / BottomRight | 左下 / 右下 |

## 最小示例

```arkts
@Entry
@Component
struct PopoverDemo {
  @State show: boolean = false
  build() {
    Column() {
      Button('提示')
        .onClick(() => this.show = !this.show)
        .bindPopup(this.show, {
          message: '这是一个气泡提示',
          placement: Placement.Top
        })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`menu`](../menu/component.md) — 菜单(Menu)与气泡区别
- [`message`](../message/component.md) — Toast 即时反馈

## 参考链接

- ArkTS 官方文档 - 气泡提示: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-use-popup
- 气泡提示 (Popup): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-popup-and-menu-components-popup
- 全局气泡提示 (openPopup): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-popup-and-menu-components-uicontext-popup
