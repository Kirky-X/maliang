# Flutter Table Widget 定义

## Widget 定义

Flutter 提供两种表格实现:`Table`(基于行列网格的布局 Widget,所有行同列数)与 `DataTable`(Material 风格数据表格,含排序、选择、分页能力)。M3 推荐使用 `DataTable` 或第三方 `paginated_data_table` / `pluto_grid` 实现复杂表格。

| Table 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 布局表格 | `Table` | `RenderObjectWidget` | 行列对齐布局(所有行同列数) |
| 数据表格(M3) | `DataTable` | `StatelessWidget` | Material 数据表格(含表头、排序) |
| 数据表格项 | `DataRow` | `DataRow` | 数据行(可选中、可点击) |
| 数据单元格 | `DataCell` | `DataCell` | 单元格(含 Widget) |
| 分页表格 | `PaginatedDataTable` | `StatefulWidget` | 分页数据表格 |
| 第三方高级表格 | `PlutoGrid` / `SfDataGrid` | - | 复杂业务表格(虚拟滚动、编辑) |

> `Table` 是布局 Widget,适合简单对齐;`DataTable` 是数据组件,适合列表数据展示。

## 构造函数

### Table

```dart
const Table({
  Key? key,
  List<TableRow> children = const <TableRow>[],
  Map<int, TableColumnWidth> columnWidths,
  TableColumnWidth defaultColumnWidth = const FlexColumnWidth(1.0),
  TextDirection? textDirection,
  TableBorder? border,
  TableCellVerticalAlignment defaultVerticalAlignment = TableCellVerticalAlignment.top,
  TextBaseline? textBaseline,
})
```

### DataTable

```dart
const DataTable({
  Key? key,
  required List<DataColumn> columns,
  required List<DataRow> rows,
  double? dividerThickness,
  double? columnSpacing,
  double? headingRowHeight,
  double? dataRowHeight,
  double? horizontalMargin,
  Widget? checkboxHorizontalMargin,
  bool showCheckboxColumn = true,
  bool? showBottomBorder,
  Map<int, TableColumnWidth>? columnWidths,
  TableColumnWidth? defaultColumnWidth,
  Decoration? headingRowColor,
  Decoration? dataRowColor,
  bool? dataRowMinHeight,
  bool? dataRowMaxHeight,
})
```

### DataColumn / DataRow / DataCell

```dart
const DataColumn({
  required Widget label,
  String? tooltip,
  bool numeric = false,
  VoidCallback? onSort,
  EdgeInsetsGeometry? headingPadding,
})
const DataRow({
  LocalKey? key,
  bool selected = false,
  ValueChanged<bool?>? onSelectChanged,
  ValueChanged<bool?>? onLongPress,
  List<DataCell> cells = const <DataCell>[],
  Color? color,
})
const DataCell(Widget child, {bool placeholder = false, bool showEditIcon = false, VoidCallback? onTap, GestureTapUpCallback? onTapUp, GestureTapDownCallback? onTapDown, GestureTapCancelCallback? onTapCancel})
```

### PaginatedDataTable

```dart
const PaginatedDataTable({
  Key? key,
  Widget? header,
  required List<DataColumn> columns,
  int? rowsPerPage,
  ValueChanged<int?>? onRowsPerPageChanged,
  required DataTableSource source,
  int currentPage = 0,
  ValueChanged<int>? onPageChanged,
  double? dataRowHeight,
  double? headingRowHeight,
  double? horizontalMargin,
  List<Widget>? actions,
})
```

> 属性与方法明细以 [properties.md](properties.md) 为唯一维护处；本文件只讲定义、构造与示例。

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Table 最小示例:Table 布局 + DataTable 数据表格
class TableSample extends StatelessWidget {
  const TableSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Table 示例')),
      body: ListView(
        children: [
          // 1. Table 布局(简单对齐)
          Padding(
            padding: const EdgeInsets.all({spacing-md}),
            child: Table(
              border: TableBorder.all(color: {color-border-default}),
              defaultColumnWidth: const IntrinsicColumnWidth(),
              defaultVerticalAlignment: TableCellVerticalAlignment.middle,
              children: [
                TableRow(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all({spacing-sm}),
                      child: Text('姓名', style: TextStyle(fontWeight: FontWeight.w600)),
                    ),
                    Padding(
                      padding: const EdgeInsets.all({spacing-sm}),
                      child: const Text('张三'),
                    ),
                  ],
                ),
                TableRow(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all({spacing-sm}),
                      child: Text('职位', style: TextStyle(fontWeight: FontWeight.w600)),
                    ),
                    Padding(
                      padding: const EdgeInsets.all({spacing-sm}),
                      child: const Text('设计师'),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const Divider(),
          // 2. DataTable 数据表格
          DataTable(
            columns: const [
              DataColumn(label: Text('姓名')),
              DataColumn(label: Text('职位'), numeric: true),
              DataColumn(label: Text('部门')),
            ],
            rows: const [
              DataRow(cells: [
                DataCell(Text('张三')),
                DataCell(Text('设计师')),
                DataCell(Text('设计部')),
              ]),
              DataRow(cells: [
                DataCell(Text('李四')),
                DataCell(Text('工程师')),
                DataCell(Text('研发部')),
              ]),
            ],
          ),
        ],
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
DataTable(
  headingRowColor: MaterialStateProperty.all({color-bg-secondary}),
  dataRowColor: MaterialStateProperty.resolveWith((states) {
    return states.contains(MaterialState.selected)
        ? {color-primary-container}
        : Colors.transparent;
  }),
  dividerThickness: 1,
  columnSpacing: {spacing-md},
  headingRowHeight: {size-md},
  dataRowHeight: {size-md},
  horizontalMargin: {spacing-md},
  columns: [
    DataColumn(
      label: Text('姓名', style: TextStyle(color: {color-text-primary})),
      onSort: (columnIndex, ascending) {},
    ),
  ],
  rows: [],
)
```

> 注:示例中的 `{color-bg-secondary}`、`{spacing-md}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录: https://docs.flutter.cn/ui/widgets
- API 参考 - Table: https://api.flutter.dev/flutter/widgets/Table-class.html
- API 参考 - DataTable: https://api.flutter.dev/flutter/material/DataTable-class.html
- API 参考 - PaginatedDataTable: https://api.flutter.dev/flutter/material/PaginatedDataTable-class.html
- API 参考 - DataTableSource: https://api.flutter.dev/flutter/material/DataTableSource-class.html
- pub.dev - pluto_grid: https://pub.flutter-io.cn/packages/pluto_grid
