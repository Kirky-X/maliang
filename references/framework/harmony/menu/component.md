# Menu Component API Documentation

> ArkTS menu components: `Menu` (menu container) + `MenuItem` (menu item). Bound to trigger components via `bindMenu` / `bindContextMenu`.

## Component Definition

`Menu` does not render directly; it must be bound to components via `bindMenu(builder)` or `bindContextMenu(builder, type)`, triggered by click/long-press to pop up.

## Binding Methods

| Method | Trigger |
| --- | --- |
| `bindMenu(builder \| array)` | Click trigger |
| `bindContextMenu(builder, type)` | Long-press/right-click trigger (ResponseType.LongPress / RightClick) |

## MenuItem Properties

| Property | Type | Description |
| --- | --- | --- |
| content | string \| Resource | Menu text |
| icon | Resource | Menu icon |
| symbolStyle | SymbolGlyphStyle | Symbol icon style |
| enabled | boolean | Whether enabled |
| action | () => void | Click callback |
| labelInfo | string \| Resource | Auxiliary description |
| startIcon / endIcon | Resource | Start/end icons |

## Array-style bindMenu (Simplified Usage)

```arkts
.bindMenu([
  { value: '复制', icon: $r('app.media.ic_copy'), action: () => {} },
  { value: '删除', action: () => {} }
])
```

## Minimal Example

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

## Related Components

- [`dropdown`](../dropdown/component.md) — Dropdown selection based on Menu combination
- [`popover`](../popover/component.md) — Bubble prompt (Popup)

## Reference Links

- ArkTS Official Documentation - Menu: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-use-menu
- Menu Control (Menu): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-popup-and-menu-components-menu
- Global Menu (openMenu): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-popup-and-menu-components-uicontext-menu