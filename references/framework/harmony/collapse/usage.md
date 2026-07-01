# Collapse 使用场景与示例

> ArkTS 无原生 Collapse,本文件给出基于 List+条件渲染的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:单个折叠面板

```arkts
@Entry
@Component
struct SingleCollapsePage {
  @State expanded: boolean = false
  build() {
    Column() {
      Row() {
        Text('什么是 ArkTS?').fontSize({font-size-md}).layoutWeight(1)
        SymbolGlyph(this.expanded ? $r('sys.symbol.chevron_down') : $r('sys.symbol.chevron_right'))
          .fontSize({font-size-sm}).fontColor([{color-text-primary}])
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
      .onClick(() => this.expanded = !this.expanded)

      if (this.expanded) {
        Text('ArkTS 是鸿蒙应用开发的主要语言,基于 TypeScript 扩展。')
          .fontSize({font-size-sm})
          .fontColor({color-text-primary})
          .padding({spacing-md})
          .backgroundColor({color-bg-secondary})
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:手风琴模式(同时只展开一个)

```arkts
@Entry
@Component
struct AccordionCollapsePage {
  @State activeIdx: number = -1
  private items: string[] = ['面板一', '面板二', '面板三']
  build() {
    Column({ space: {spacing-sm} }) {
      ForEach(this.items, (item: string, idx: number) => {
        Column() {
          Row() {
            Text(item).fontSize({font-size-md}).layoutWeight(1)
            SymbolGlyph(this.activeIdx === idx ? $r('sys.symbol.chevron_down') : $r('sys.symbol.chevron_right'))
              .fontSize({font-size-sm}).fontColor([{color-text-primary}])
          }
          .padding({spacing-md})
          .backgroundColor({color-bg-primary})
          .onClick(() => this.activeIdx = this.activeIdx === idx ? -1 : idx)

          if (this.activeIdx === idx) {
            Text(`${item} 的详细内容,手风琴模式下其他面板自动收起。`)
              .fontSize({font-size-sm}).fontColor({color-text-primary})
              .padding({spacing-md})
              .backgroundColor({color-bg-secondary})
          }
        }
        .borderRadius({radius-md})
        .clip(true)
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:带过渡动画(transition)

```arkts
@Entry
@Component
struct AnimatedCollapsePage {
  @State expanded: boolean = false
  build() {
    Column() {
      Row() {
        Text('点击展开').fontSize({font-size-md}).layoutWeight(1)
        SymbolGlyph(this.expanded ? $r('sys.symbol.chevron_down') : $r('sys.symbol.chevron_right'))
          .fontColor([{color-text-primary}])
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
      .onClick(() => this.expanded = !this.expanded)

      if (this.expanded) {
        Text('带动画的展开内容')
          .fontSize({font-size-sm})
          .padding({spacing-md})
          .backgroundColor({color-bg-secondary})
          .transition({ type: TransitionType.Insert, translate: { y: -20 }, opacity: 0 })
          .transition({ type: TransitionType.Delete, opacity: 0 })
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:封装可复用 Collapse

```arkts
@Component
struct Collapse {
  title: string = ''
  @State expanded: boolean = false
  @BuilderParam content: () => void
  build() {
    Column() {
      Row() {
        Text(this.title).fontSize({font-size-md}).layoutWeight(1)
        SymbolGlyph(this.expanded ? $r('sys.symbol.chevron_down') : $r('sys.symbol.chevron_right'))
          .fontColor([{color-text-primary}])
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
      .onClick(() => this.expanded = !this.expanded)
      if (this.expanded) {
        this.content()
      }
    }
  }
}
```

## 注意事项

1. **手风琴用单变量** — `activeIdx` 记录当前展开项,设为 -1 表示全部收起;切换时自动收起其他。
2. **transition 配合 if** — `transition` 仅在 `if` 插入/移除时触发;常驻内容无动画。
3. **clip(true)** — 折叠面板设 `clip(true)`,展开内容超出圆角时自动裁剪。
4. **大数据展开** — 折叠内容含长列表时,展开时再渲染(if 惰性),避免初始全渲染。
5. **图标旋转** — 展开/收起图标可用 `rotate({ angle: expanded ? 180 : 0 })` 替代切换不同图标。
6. **无障碍** — 折叠标题设 `accessibilityText('标题,已展开/已收起')`,读屏播报状态。
