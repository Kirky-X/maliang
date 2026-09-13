# Checkbox 使用场景与示例

> 列举 ArkTS 复选框组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:CheckboxGroup 全选联动

```arkts
@Entry
@Component
struct GroupCheckboxPage {
  @State selectAll: boolean = false
  build() {
    Column({ space: {spacing-md} }) {
      Row({ space: {spacing-sm} }) {
        CheckboxGroup({ group: 'items' })
          .selectAll(this.selectAll)
          .selectedColor({color-primary})
          .onChange((result: CheckboxGroupResult) => this.selectAll = result.status === SelectStatus.All)
        Text('全选').fontSize({font-size-md})
      }
      Row({ space: {spacing-sm} }) {
        Checkbox({ name: 'a', group: 'items' }).selectedColor({color-primary})
        Text('选项 A').fontSize({font-size-md})
      }
      Row({ space: {spacing-sm} }) {
        Checkbox({ name: 'b', group: 'items' }).selectedColor({color-primary})
        Text('选项 B').fontSize({font-size-md})
      }
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:表格行多选(列表批量操作)

```arkts
@Entry
@Component
struct SelectableListPage {
  @State items: Array<[string, boolean]> = [['订单 1001', false], ['订单 1002', true], ['订单 1003', false]]
  build() {
    Column({ space: {spacing-sm} }) {
      ForEach(this.items, (item: [string, boolean], idx: number) => {
        Row() {
          Checkbox({ name: item[0], group: 'rows' })
            .select(item[1])
            .selectedColor({color-primary})
            .onChange((isChecked: boolean) => this.items[idx][1] = isChecked)
          Text(item[0]).fontSize({font-size-md}).layoutWeight(1)
        }
        .width('100%')
        .padding({spacing-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .onClick(() => this.items[idx][1] = !this.items[idx][1])
      })
      Button('删除选中项').enabled(this.items.some((i: [string, boolean]) => i[1]))
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:半选态(部分子项选中)

ArkTS `Checkbox` 无内置 indeterminate 属性,半选态用父级 `CheckboxGroup.onChange` 返回的 `SelectStatus.Some` 驱动父级 Checkbox 样式,或叠加自定义样式表达:

```arkts
@Entry
@Component
struct IndeterminatePage {
  @State selectAll: SelectStatus = SelectStatus.Some
  build() {
    Row({ space: {spacing-sm} }) {
      CheckboxGroup({ group: 'children' })
        .selectAll(this.selectAll === SelectStatus.All)
        .onChange((result: CheckboxGroupResult) => this.selectAll = result.status)
      Text('全选').fontSize({font-size-md})
      if (this.selectAll === SelectStatus.Some) {
        Text('(部分选中)').fontSize({font-size-sm}).fontColor({color-text-secondary})
      }
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **group 一致** — 同组 Checkbox 必须使用相同 group 名,否则 CheckboxGroup 联动失效。
2. **select 与 onChange** — `select` 单向控制选中态;`onChange` 回调手动更新 `@State`,避免状态漂移。
3. **半选态依赖组管理** — 单个 Checkbox 不支持半选,部分选中语义由 CheckboxGroup 的 `SelectStatus.Some` 表达(与 Carbon 三态规范对齐:checked/unchecked/indeterminate)。
4. **无障碍** — 复选框建议设 `accessibilityRole(Checkbox)` 并用 `accessibilityChecked` 同步状态;标签文字紧邻复选框,整体可点。
5. **触控目标** — 视觉尺寸可小,但点击热区 SHOULD ≥44vp,不足时外层 Row 补 padding。
