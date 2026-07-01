# Menu 使用场景与示例

> 列举 ArkTS 菜单组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:点击菜单(bindMenu 数组式)

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

## 场景 2:长按上下文菜单(bindContextMenu)

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

## 场景 3:图标 + 文字菜单(Builder 式)

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

## 场景 4:分组菜单

```arkts
@Builder groupMenu() {
  Menu() {
    MenuItem({ content: '新建' }).action(() => {})
    MenuItem({ content: '打开' }).action(() => {})
    // 分隔线(无内容项)
    MenuItem({ content: '' }).enabled(false)
    MenuItem({ content: '退出' }).action(() => {})
  }
}
```

## 注意事项

1. **数组式 vs Builder 式** — 简单文字菜单用数组式更简洁;需图标/分组/复杂样式用 Builder 式。
2. **bindContextMenu 触发类型** — `ResponseType.LongPress`(移动端长按)/ `RightClick`(鼠标右键),按平台选择。
3. **菜单自动关闭** — 点击 MenuItem 后菜单自动关闭,无需手动 dismiss。
4. **action 必须有** — 数组式缺 action 静默无响应;Builder 式缺 action 仅关闭不执行。
5. **图标尺寸** — MenuItem 内置图标尺寸固定,无需自行设置 width/height。
6. **分组分隔线** — 暂无原生 Divider,用 `MenuItem({ content: '' }).enabled(false)` 模拟分隔。
