# Dropdown 使用场景与示例

> ArkTS 无原生 Dropdown,本文件给出基于 Button+Menu 的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础下拉选择

```arkts
@Entry
@Component
struct BasicDropdownPage {
  @State picked: string = '请选择城市'
  private opts: string[] = ['北京', '上海', '广州', '深圳']
  build() {
    Row({ space: {spacing-sm} }) {
      Text('城市').fontSize({font-size-md})
      Button(this.picked)
        .backgroundColor({color-bg-primary})
        .fontColor({color-text-primary})
        .fontSize({font-size-md})
        .bindMenu(this.opts.map(o => ({
          value: o,
          action: () => this.picked = o
        })))
      SymbolGlyph($r('sys.symbol.chevron_down'))
        .fontSize({font-size-sm})
        .fontColor([{color-text-primary}])
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:带图标的下拉

```arkts
@Entry
@Component
struct IconDropdownPage {
  @State picked: string = '列表视图'
  build() {
    Button(this.picked)
      .backgroundColor({color-bg-secondary})
      .fontColor({color-text-primary})
      .bindMenu([
        { value: '列表视图', icon: $r('app.media.ic_list'), action: () => this.picked = '列表视图' },
        { value: '网格视图', icon: $r('app.media.ic_grid'), action: () => this.picked = '网格视图' },
        { value: '卡片视图', icon: $r('app.media.ic_card'), action: () => this.picked = '卡片视图' }
      ])
    .padding({spacing-md})
  }
}
```

## 场景 3:封装可复用 Dropdown 组件

```arkts
@Component
struct Dropdown {
  @State picked: string = ''
  private options: string[] = []
  private placeholder: string = '请选择'
  onSelect: (v: string) => void = () => {}
  build() {
    Button(this.picked || this.placeholder)
      .backgroundColor({color-bg-primary})
      .fontColor(this.picked ? {color-text-primary} : {color-text-primary})
      .fontSize({font-size-md})
      .borderRadius({radius-md})
      .bindMenu(this.options.map(o => ({
        value: o,
        action: () => { this.picked = o; this.onSelect(o) }
      })))
  }
}

@Entry
@Component
struct ReuseDropdownPage {
  build() {
    Column({ space: {spacing-md} }) {
      Dropdown({
        options: ['苹果', '香蕉', '橙子'],
        onSelect: (v: string) => console.info(`选了 ${v}`)
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:搜索型下拉(Menu + Search)

```arkts
@Entry
@Component
struct SearchDropdownPage {
  @State picked: string = ''
  private allOpts: string[] = ['北京', '上海', '广州', '深圳', '杭州', '成都']
  build() {
    Column() {
      Button(this.picked || '搜索城市')
        .bindMenu(this.allOpts.map(o => ({
          value: o,
          action: () => this.picked = o
        })))
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **bindMenu 自动关闭** — 选中后菜单自动关闭,无需手动 dismiss。
2. **picked 占位** — 未选时显示 placeholder,选中后显示实际值;用 `||` 切换。
3. **大量选项** — 选项 > 10 个时 bindMenu 体验差;建议改用 bindSheet 弹出列表选择。
4. **禁用态** — 不可选时 `enabled(false)`,但仍可点击触发;需额外判断或改用 Text 展示。
5. **Select 组件优先** — 若目标 API 版本支持 `Select` 组件,优先用它(内置下拉箭头与状态)。
6. **图标对齐** — bindMenu 数组式 icon 与文字自动对齐;Builder 式需自行排版。
