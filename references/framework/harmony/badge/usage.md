# Badge 使用场景与示例

> 列举 ArkTS Badge 徽章组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:消息计数徽章

```arkts
@Entry
@Component
struct MessageBadgePage {
  @State count: number = 8
  build() {
    Row({ space: {spacing-lg} }) {
      Badge({ count: this.count, maxCount: 99, style: { badgeColor: {color-danger}, badgeSize: 16 } }) {
        SymbolGlyph($r('sys.symbol.bell'))
          .fontSize({font-size-xl})
          .fontColor([{color-text-primary}])
      }
      .onClick(() => this.count = Math.max(0, this.count - 1))
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:红点提示(count=0 不显示)

```arkts
@Entry
@Component
struct DotBadgePage {
  @State hasUpdate: boolean = true
  build() {
    Badge({
      count: this.hasUpdate ? 1 : 0,
      style: { badgeColor: {color-danger}, badgeSize: 8 }
    }) {
      SymbolGlyph($r('sys.symbol.gear'))
        .fontSize({font-size-xl})
        .fontColor([{color-text-primary}])
    }
    .onClick(() => this.hasUpdate = false)
    .padding({spacing-md})
  }
}
```

## 场景 3:头像在线状态(右下圆点)

```arkts
@Entry
@Component
struct AvatarBadgePage {
  build() {
    Badge({
      count: 0,
      position: BadgePosition.Right,
      style: { badgeColor: {color-success}, badgeSize: 12, borderColor: {color-bg-primary}, borderWidth: 2 }
    }) {
      Image($r('app.media.user1'))
        .width(48).height(48)
        .objectFit(ImageFit.Cover)
        .borderRadius({radius-full})
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:列表项未读计数

```arkts
@Entry
@Component
struct ListBadgePage {
  private items: Array<{ name: string; unread: number }> = [
    { name: '工作群', unread: 5 },
    { name: '家庭群', unread: 0 },
    { name: '通知', unread: 99 }
  ]
  build() {
    List() {
      ForEach(this.items, (item) => {
        ListItem() {
          Row() {
            Text(item.name).fontSize({font-size-md}).layoutWeight(1)
            Badge({
              count: item.unread,
              maxCount: 99,
              style: { badgeColor: {color-danger}, badgeSize: 16 }
            }) {
              Text('').width(1).height(1)
            }
          }
          .padding({spacing-md})
          .backgroundColor({color-bg-primary})
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:Tab 标签角标

```arkts
@Entry
@Component
struct TabBadgePage {
  build() {
    Tabs() {
      TabContent() { Text('消息') }.tabBar(this.msgTab())
      TabContent() { Text('我的') }.tabBar('我的')
    }
  }
  @Builder msgTab() {
    Badge({ count: 5, style: { badgeColor: {color-danger} } }) {
      Text('消息').fontSize({font-size-md}).padding({spacing-sm})
    }
  }
}
```

## 注意事项

1. **count=0 不显示** — Badge 在 count 为 0 时自动隐藏;红点提示用 count=1 控制。
2. **maxCount 默认 99** — 超过显示 "99+";自定义上限改 maxCount。
3. **badgeSize 含文字** — 计数徽章的 size 需容纳两位数,建议 ≥ 16。
4. **borderColor 与底色区分** — 头像上的角标需设 border(底色)避免与头像融合。
5. **子组件必须有内容** — Badge 内子组件为空(如 width:1)仅显示徽章本身,用于列表右侧角标。
6. **TabBar 角标** — tabBar 用 `@Builder` 返回 Badge 包裹的 Text,需注意 TabContent 的 tabBar 支持自定义 builder。
