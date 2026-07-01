# Menu 组件 API 文档

> ArkTS 菜单组件,`Menu`(菜单容器)+ `MenuItem`(菜单项)。通过 `bindMenu` / `bindContextMenu` 绑定到触发组件。

## 组件定义

`Menu` 不直接渲染,需通过 `bindMenu(builder)` 或 `bindContextMenu(builder, type)` 绑定到组件,点击/长按触发弹出。

## 绑定方法

| 方法 | 触发方式 |
| --- | --- |
| `bindMenu(builder \| array)` | 点击触发 |
| `bindContextMenu(builder, type)` | 长按/右键触发(ResponseType.LongPress / RightClick) |

## MenuItem 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| content | string \| Resource | 菜单文字 |
| icon | Resource | 菜单图标 |
| symbolStyle | SymbolGlyphStyle | 符号图标样式 |
| enabled | boolean | 是否可用 |
| action | () => void | 点击回调 |
| labelInfo | string \| Resource | 辅助说明 |
| startIcon / endIcon | Resource | 起始/末尾图标 |

## 数组式 bindMenu(简化用法)

```arkts
.bindMenu([
  { value: '复制', icon: $r('app.media.ic_copy'), action: () => {} },
  { value: '删除', action: () => {} }
])
```

## 最小示例

```arkts
@Entry
@Component
struct MenuDemo {
  build() {
    Column() {
      Text('更多')
        .fontSize({font-size-md})
        .bindMenu([
          { value: '分享', action: () => console.info('分享') },
          { value: '删除', action: () => console.info('删除') }
        ])
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`dropdown`](../dropdown/component.md) — 下拉选择基于 Menu 组合
- [`popover`](../popover/component.md) — 气泡提示(Popup)

## 参考链接

- ArkTS 官方文档 - 菜单: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-use-menu
- 菜单控制 (Menu): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-popup-and-menu-components-menu
- 全局菜单 (openMenu): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-popup-and-menu-components-uicontext-menu
