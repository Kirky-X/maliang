# Menu Usage Scenarios and Examples

> Lists typical usage scenarios for ArkTS menu components. All colors, spacing, and border-radius are referenced via design tokens.

## Scenario 1: Click Menu (bindMenu Array Style)

```arkts
@Entry
@Component
struct ClickMenuPage {
  build() {
    Column() {
      Button('更多')
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
        .bindMenu([
          { value: '分享', icon: $r('app.media.ic_share'), action: () => console.info('分享') },
          { value: '收藏', icon: $r('app.media.ic_star'), action: () => console.info('收藏') },
          { value: '删除', icon: $r('app.media.ic_del'), action: () => console.info('删除') }
        ])
    }
    .padding({spacing-md})
  }
}
```

## Scenario 2: Long-press Context Menu (bindContextMenu)

```arkts
@Entry
@Component
struct ContextMenuPage {
  build() {
    Column() {
      Text('长按我弹出菜单')
        .fontSize({font-size-md})
        .padding({spacing-md})
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-md})
        .bindContextMenu(this.menuBuilder, ResponseType.LongPress)
    }
    .padding({spacing-md})
  }

  @Builder menuBuilder() {
    Menu() {
      MenuItem({ content: '复制' })
        .icon($r('app.media.ic_copy'))
        .action(() => console.info('复制'))
      MenuItem({ content: '剪切' })
        .icon($r('app.media.ic_cut'))
        .action(() => console.info('剪切'))
      MenuItem({ content: '删除' })
        .icon($r('app.media.ic_del'))
        .action(() => console.info('删除'))
    }
  }
}
```

## Scenario 3: Icon + Text Menu (Builder Style)

```arkts
@Entry
@Component
struct IconMenuPage {
  build() {
    Button('操作')
      .bindMenu(this.menu)
      .backgroundColor({color-button-primary-bg})
      .fontColor({color-text-on-primary})
      .padding({spacing-md})
  }
  @Builder menu() {
    Menu() {
      MenuItem({ content: '编辑', startIcon: $r('app.media.ic_edit') })
      MenuItem({ content: '置顶', startIcon: $r('app.media.ic_top') })
      MenuItem({ content: '屏蔽', endIcon: $r('app.media.ic_block') })
    }
  }
}
```

## Scenario 4: Grouped Menu

```arkts
@Builder groupMenu() {
  Menu() {
    MenuItem({ content: '新建' }).action(() => {})
    MenuItem({ content: '打开' }).action(() => {})
    // Separator (empty item)
    MenuItem({ content: '' }).enabled(false)
    MenuItem({ content: '退出' }).action(() => {})
  }
}
```

## Notes

1. **Array style vs Builder style** — simple text menus use array style for conciseness; icons/groups/complex styles use Builder style.
2. **bindContextMenu trigger type** — `ResponseType.LongPress` (mobile long-press) / `RightClick` (mouse right-click), choose by platform.
3. **Menu auto-closes** — menu automatically closes after clicking MenuItem, no manual dismiss needed.
4. **action must be present** — array style without action silently does nothing; Builder style without action only closes without executing.
5. **Icon size** — MenuItem built-in icon size is fixed, no need to set width/height manually.
6. **Group separator** — no native Divider available, simulate with `MenuItem({ content: '' }).enabled(false)`.