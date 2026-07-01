# Divider 使用场景与示例

> 列举 ArkTS Divider 分割线的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:列表项分隔

```arkts
@Entry
@Component
struct ListDividerPage {
  private items: string[] = ['项目一', '项目二', '项目三']
  build() {
    Column() {
      ForEach(this.items, (item: string, idx: number) => {
        Text(item)
          .fontSize({font-size-md})
          .width('100%')
          .padding({spacing-md})
        if (idx < this.items.length - 1) {
          Divider().color({color-border-default}).margin({ left: {spacing-md} })
        }
      })
    }
    .backgroundColor({color-bg-primary})
  }
}
```

## 场景 2:内容区块分隔

```arkts
@Entry
@Component
struct SectionDividerPage {
  build() {
    Column() {
      Text('基本信息').fontSize({font-size-md}).fontWeight(FontWeight.Bold).padding({spacing-md})
      Text('姓名: 张三').fontSize({font-size-sm}).padding({ left: {spacing-md}, right: {spacing-md} })

      Divider().color({color-border-default}).strokeWidth(1).margin({ top: {spacing-md}, bottom: {spacing-md} })

      Text('联系方式').fontSize({font-size-md}).fontWeight(FontWeight.Bold).padding({spacing-md})
      Text('电话: 13800138000').fontSize({font-size-sm}).padding({ left: {spacing-md}, right: {spacing-md} })
    }
    .backgroundColor({color-bg-primary})
  }
}
```

## 场景 3:垂直分割线(分隔按钮)

```arkts
@Entry
@Component
struct VerticalDividerPage {
  build() {
    Row() {
      Text('登录').fontSize({font-size-md}).fontColor({color-button-primary-bg}).padding({spacing-md})
      Divider().vertical(true).color({color-border-default}).height(20)
      Text('注册').fontSize({font-size-md}).fontColor({color-button-primary-bg}).padding({spacing-md})
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:虚线分割

```arkts
@Entry
@Component
struct DashedDividerPage {
  build() {
    Column() {
      Text('上方内容').fontSize({font-size-md}).padding({spacing-md})
      Divider()
        .color({color-border-default})
        .strokeDashArray([6, 4])
        .strokeWidth(1)
      Text('下方内容').fontSize({font-size-md}).padding({spacing-md})
    }
  }
}
```

## 场景 5:带文字的分割线(组合)

```arkts
@Entry
@Component
struct TextDividerPage {
  build() {
    Row() {
      Column().layoutWeight(1).height(1).backgroundColor({color-border-default})
      Text('或').fontSize({font-size-xs}).fontColor({color-text-primary}).margin({ left: {spacing-sm}, right: {spacing-sm} })
      Column().layoutWeight(1).height(1).backgroundColor({color-border-default})
    }
    .padding({spacing-md})
    .alignItems(VerticalAlign.Center)
  }
}
```

## 注意事项

1. **Divider 默认占满宽度** — 水平 Divider 自动撑满父容器宽度;垂直 Divider 需显式设 height。
2. **列表分隔省略末项** — `if (idx < length - 1)` 避免最后一项后多余分隔线。
3. **vertical 需 height** — 垂直分割线必须设 `height`,否则高度为 0 不可见。
4. **缩进分隔线** — 列表分隔线常需左缩进对齐文字,用 `margin({ left: spacing-md })`。
5. **strokeDashArray 虚线** — 数组 `[实线长, 间隙长]`,如 `[6, 4]`;粗细用 strokeWidth。
6. **带文字分隔** — 无原生支持,用 `Row` + 两个 `Column`(作线) + `Text` 组合实现。
