# Tag 使用场景与示例

> 列举 ArkTS 标签的典型使用场景(基于 Text+装饰组合)。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:状态标签(列表项角标)

```arkts
@Entry
@Component
struct StatusTagPage {
  build() {
    Column({ space: {spacing-sm} }) {
      Row() {
        Text('订单 #12345').fontSize({font-size-md}).layoutWeight(1)
        Text('已完成')
          .fontSize({font-size-xs})
          .fontColor({color-text-on-primary})
          .backgroundColor({color-success})
          .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
          .borderRadius({radius-sm})
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
    }
  }
}
```

## 场景 2:多色标签组

```arkts
@Entry
@Component
struct MultiTagPage {
  build() {
    Row({ space: {spacing-sm} }) {
      Text('新品').fontSize({font-size-xs}).fontColor({color-text-on-primary})
        .backgroundColor({color-button-primary-bg})
        .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
        .borderRadius({radius-sm})
      Text('包邮').fontSize({font-size-xs}).fontColor({color-text-on-primary})
        .backgroundColor({color-success})
        .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
        .borderRadius({radius-sm})
      Text('限量').fontSize({font-size-xs}).fontColor({color-text-on-primary})
        .backgroundColor({color-danger})
        .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
        .borderRadius({radius-sm})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:描边标签(线框风格)

```arkts
@Entry
@Component
struct OutlineTagPage {
  build() {
    Row({ space: {spacing-sm} }) {
      Text('可选')
        .fontSize({font-size-xs})
        .fontColor({color-button-primary-bg})
        .backgroundColor({color-bg-primary})
        .border({ width: 1, color: {color-button-primary-bg} })
        .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
        .borderRadius({radius-sm})
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:可关闭标签

```arkts
@Entry
@Component
struct ClosableTagPage {
  @State tags: string[] = ['标签1', '标签2', '标签3']
  build() {
    Row({ space: {spacing-sm} }) {
      ForEach(this.tags, (tag: string, idx: number) => {
        Row({ space: {spacing-xs} }) {
          Text(tag).fontSize({font-size-xs}).fontColor({color-text-primary})
          SymbolGlyph($r('sys.symbol.xmark'))
            .fontSize({font-size-xs})
            .fontColor([{color-text-primary}])
            .onClick(() => this.tags.splice(idx, 1))
        }
        .backgroundColor({color-bg-secondary})
        .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
        .borderRadius({radius-full})
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:封装可复用 Tag

```arkts
@Component
struct Tag {
  text: string = ''
  color: ResourceColor = {color-button-primary-bg}
  build() {
    Text(this.text)
      .fontSize({font-size-xs})
      .fontColor({color-text-on-primary})
      .backgroundColor(this.color)
      .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
      .borderRadius({radius-sm})
  }
}
```

## 注意事项

1. **圆角区分** — 状态标签用 `{radius-sm}`(小圆角);胶囊标签用 `{radius-full}`(全圆角)。
2. **字号偏小** — 标签字号用 `{font-size-xs}`,避免与正文同大喧宾夺主。
3. **padding 紧凑** — 上下 padding 2vp,左右 `{spacing-sm}`;过大的 padding 显得臃肿。
4. **语义配色统一** — 同应用内"成功/警告/危险"标签颜色必须统一,避免混淆。
5. **可关闭标签** — 关闭图标用 `SymbolGlyph` xmark;`splice` 后 `@State` 数组触发刷新。
6. **列表内标签** — 列表项右侧标签用 `Row + Blank() + Tag` 布局。
