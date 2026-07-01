# Table 使用场景与示例

> ArkTS 无原生 Table,本文件给出基于 Grid/List 的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础数据表格(Grid 实现)

```arkts
@Entry
@Component
struct GridTablePage {
  private header: string[] = ['姓名', '年龄', '城市']
  private rows: string[][] = [
    ['张三', '25', '北京'],
    ['李四', '30', '上海'],
    ['王五', '28', '广州']
  ]
  build() {
    Grid() {
      ForEach(this.header, (h: string) => {
        GridItem() {
          Text(h).fontSize({font-size-sm}).fontWeight(FontWeight.Bold).padding({spacing-sm})
        }.backgroundColor({color-bg-secondary})
      })
      ForEach(this.rows, (row: string[]) => {
        ForEach(row, (cell: string) => {
          GridItem() {
            Text(cell).fontSize({font-size-sm}).padding({spacing-sm})
          }.backgroundColor({color-bg-primary})
        })
      })
    }
    .columnsTemplate('1fr 1fr 1fr')
    .borderRadius({radius-md})
    .clip(true)
    .padding({spacing-md})
  }
}
```

## 场景 2:可交互表格(List + Row)

```arkts
@Entry
@Component
struct ListTablePage {
  private rows: string[][] = [['张三', '90'], ['李四', '85']]
  @State selected: number = -1
  build() {
    Column() {
      // 表头
      Row() {
        Text('姓名').layoutWeight(1).fontSize({font-size-sm}).fontWeight(FontWeight.Bold)
        Text('成绩').layoutWeight(1).fontSize({font-size-sm}).fontWeight(FontWeight.Bold)
      }
      .padding({spacing-sm}).backgroundColor({color-bg-secondary})

      // 数据行
      List() {
        ForEach(this.rows, (row: string[], idx: number) => {
          ListItem() {
            Row() {
              Text(row[0]).layoutWeight(1).fontSize({font-size-sm})
              Text(row[1]).layoutWeight(1).fontSize({font-size-sm})
            }
            .padding({spacing-sm})
            .backgroundColor(this.selected === idx ? {color-bg-secondary} : {color-bg-primary})
            .onClick(() => this.selected = idx)
          }
        })
      }
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-md})
  }
}
```

## 场景 3:带分隔线的表格(Divider)

```arkts
@Entry
@Component
struct DividerTablePage {
  private rows: string[][] = [['A', '100'], ['B', '95']]
  build() {
    Column() {
      ForEach(this.rows, (row: string[]) => {
        Row() {
          Text(row[0]).layoutWeight(1).fontSize({font-size-sm})
          Text(row[1]).layoutWeight(1).fontSize({font-size-sm})
        }
        .padding({spacing-md})
        Divider().color({color-border-default})
      })
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
  }
}
```

## 注意事项

1. **Grid 表头处理** — GridItem 按顺序填充,表头需先 push 再 push 数据行;或用 `columnStart/columnEnd` 跨列。
2. **List 表格更灵活** — 行高可变、含点击交互的表格用 List + Row;纯展示用 Grid 更紧凑。
3. **列宽控制** — Grid 用 `columnsTemplate('1fr 2fr 1fr')` 比例分列;List 用 `layoutWeight` 等分。
4. **大数据用 LazyForEach** — 千级行数据务必懒加载,否则一次性渲染卡顿。
5. **横向滚动表格** — 列多用 `Scroll(Horizontal)` 包裹 Grid,设置固定列宽 `columnsTemplate('100vp 100vp ...')`。
6. **排序/编辑** — 表格排序需自行实现状态管理;单元格编辑用 `TextInput` 替换 `Text`。
