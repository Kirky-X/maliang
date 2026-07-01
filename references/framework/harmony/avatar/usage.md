# Avatar 使用场景与示例

> ArkTS 无原生 Avatar,本文件给出基于 Image 圆形裁剪的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础图片头像

```arkts
@Entry
@Component
struct ImageAvatarPage {
  build() {
    Row({ space: {spacing-sm} }) {
      Image($r('app.media.user1'))
        .width(48).height(48)
        .objectFit(ImageFit.Cover)
        .borderRadius({radius-full})
        .border({ width: 1, color: {color-border-default} })
      Column() {
        Text('用户名').fontSize({font-size-md})
        Text('简介').fontSize({font-size-xs}).fontColor({color-text-primary})
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:首字母占位头像(无图片)

```arkts
@Entry
@Component
struct InitialAvatarPage {
  build() {
    Row({ space: {spacing-sm} }) {
      // 文字头像
      Text('张')
        .width(48).height(48)
        .textAlign(TextAlign.Center)
        .fontSize({font-size-lg})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-button-primary-bg})
        .borderRadius({radius-full})
      Text('张三').fontSize({font-size-md})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:带在线状态角标(Badge)

```arkts
@Entry
@Component
struct StatusAvatarPage {
  build() {
    Badge({ count: 0, position: BadgePosition.RightTop, style: { badgeSize: 12, badgeColor: {color-success} } }) {
      Image($r('app.media.user1'))
        .width(48).height(48)
        .objectFit(ImageFit.Cover)
        .borderRadius({radius-full})
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:头像组(叠加显示)

```arkts
@Entry
@Component
struct AvatarGroupPage {
  private users: Resource[] = [$r('app.media.u1'), $r('app.media.u2'), $r('app.media.u3')]
  build() {
    Stack() {
      ForEach(this.users, (img: Resource, idx: number) => {
        Image(img)
          .width(32).height(32)
          .objectFit(ImageFit.Cover)
          .borderRadius({radius-full})
          .border({ width: 2, color: {color-bg-primary} })
          .margin({ left: idx * 24 })
      })
    }
    .alignContent(Alignment.Start)
    .padding({spacing-md})
  }
}
```

## 场景 5:可点击头像(进个人页)

```arkts
@Entry
@Component
struct ClickAvatarPage {
  build() {
    Image($r('app.media.user1'))
      .width(48).height(48)
      .objectFit(ImageFit.Cover)
      .borderRadius({radius-full})
      .onClick(() => console.info('进个人页'))
      .padding({spacing-md})
  }
}
```

## 注意事项

1. **objectFit(Cover)** — 头像需 Cover 填充,避免留白;非正方形图片用 Contain 会变形。
2. **borderRadius-full** — 圆形头像用 `{radius-full}`(50%);非圆形用 `{radius-md}`。
3. **border 描边** — 头像组叠加时 border 用底色,分隔相邻头像。
4. **首字母头像** — 无图片资源时,取姓名首字 + 主色背景;颜色可按姓名 hash 分配。
5. **尺寸规范** — 列表头像 40-48vp;导航栏 32vp;个人主页 80-96vp。
6. **点击区域** — 小头像点击区域不足 44vp 时,外层包透明 Button 扩大触控区。
