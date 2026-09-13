# Select 使用场景与示例

> 列举 ArkTS 下拉选择器的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:表单内常规选择(3-10 项)

```arkts
@Entry
@Component
struct FormSelectPage {
  @State category: string = ''
  private opts: SelectOption[] = [
    { value: '数码' }, { value: '家电' }, { value: '服饰' }, { value: '食品' }
  ]
  build() {
    Column({ space: {spacing-md} }) {
      Text('商品分类').fontSize({font-size-md}).fontColor({color-text-primary})
      Select(this.opts)
        .value(this.category === '' ? '请选择分类' : this.category)
        .font({ size: {font-size-md} })
        .fontColor(this.category === '' ? {color-text-secondary} : {color-text-primary})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .optionWidth({spacing-xxxl})
        .onSelected((index: number, value: string) => this.category = value)
    }
    .alignItems(HorizontalAlign.Start)
    .padding({spacing-md})
  }
}
```

## 场景 2:列表筛选条(单值筛选)

```arkts
@Entry
@Component
struct FilterSelectPage {
  @State sort: string = '综合排序'
  private sorts: SelectOption[] = [
    { value: '综合排序', icon: $r('app.media.ic_sort') },
    { value: '价格从低到高' },
    { value: '价格从高到低' },
    { value: '最新发布' }
  ]
  build() {
    Row({ space: {spacing-sm} }) {
      Select(this.sorts)
        .selected(0)
        .value(this.sort)
        .font({ size: {font-size-sm} })
        .fontColor({color-text-primary})
        .backgroundColor({color-bg-secondary})
        .borderRadius({radius-full})
        .onSelected((index: number, value: string) => this.sort = value)
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:滚轮备选(TextPicker,档位交互)

选项需要滚轮滑选交互时用 `TextPicker`(级联/大选项集另见 vocabulary `select-searchable`):

```arkts
@Entry
@Component
struct PickerPage {
  @State height: string = '170'
  private ranges: string[] = ['150', '160', '170', '180', '190']
  build() {
    Column({ space: {spacing-md} }) {
      Text('身高(cm)').fontSize({font-size-md})
      TextPicker({ range: this.ranges, selected: 2 })
        .onChange((value: string | string[], index: number | number[]) => this.height = value as string)
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **与 dropdown 的分工** — Select 用于表单/筛选的数据录入,`Menu`/`bindMenu`(dropdown 类)用于动作菜单;选值场景禁用动作菜单模拟。
2. **选项量级** — 3-10 项用 Select;>10 项或需搜索改用组合方案(`TextInput` + `Menu` 列表,对齐 vocabulary `select-searchable`)。
3. **占位文案** — 未选择时 `value` 用占位文案并配 `color-text-secondary`,选中后切主文本色。
4. **无障碍** — `Select` 自带展开/收起语义;`accessibilityText` 描述当前选中值。
5. **触控目标** — 触发器高度 SHOULD ≥44vp(默认约 40vp 时外层补 padding)。
