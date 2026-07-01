# Table 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Table 组件。** 通过 `Grid`(网格)或 `List`(列表)组合实现表格效果。

## 缺失原因

ArkTS 没有 HTML `<table>` 那样的二维表格组件。表格本质是行列网格,用 `Grid` + `columnsTemplate` 定义列,`GridItem` 承载单元格即可实现。

## 替代方案

- **方案 1:Grid 实现表格** — 列固定用 `columnsTemplate`,每行数据展开为多个 `GridItem`。适合列数固定的表格。
- **方案 2:List + Row 实现表格** — 每个 `ListItem` 是一行 `Row`,行内用 `layoutWeight` 分列。适合行高可变、含交互的表格。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:Grid/List) |
| Flutter | `DataTable` / `Table` widget |
| Element Plus | `<el-table>` |

## 最小示例(Grid 实现)

```arkts
@Entry
@Component
struct TableDemo {
  private rows: string[][] = [['张三', '90'], ['李四', '85']]
  build() {
    Grid() {
      GridItem() { Text('姓名').fontSize({font-size-sm}).fontWeight(FontWeight.Bold) }
      GridItem() { Text('成绩').fontSize({font-size-sm}).fontWeight(FontWeight.Bold) }
      ForEach(this.rows, (row: string[]) => {
        GridItem() { Text(row[0]).fontSize({font-size-sm}) }
        GridItem() { Text(row[1]).fontSize({font-size-sm}) }
      })
    }
    .columnsTemplate('1fr 1fr')
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
  }
}
```

## 关联组件

- [`grid`](../grid/component.md) — 网格容器
- [`list`](../list/component.md) — 列表容器

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`grid`](../grid/component.md) / [`list`](../list/component.md)
- 创建网格 (Grid): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-grid
