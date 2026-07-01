# Flutter Table 属性列表与默认值

本文档汇总 `Table` / `DataTable` / `PaginatedDataTable` 的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## Table 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<TableRow>` | `[]` | 行列表 |
| `columnWidths` | `Map<int, TableColumnWidth>?` | `null` | 各列宽度 |
| `defaultColumnWidth` | `TableColumnWidth` | `FlexColumnWidth(1.0)` | 默认列宽 |
| `border` | `TableBorder?` | `null` | 边框 |
| `defaultVerticalAlignment` | `TableCellVerticalAlignment` | `TableCellVerticalAlignment.top` | 默认垂直对齐 |
| `textDirection` | `TextDirection?` | `null` | 文本方向 |
| `textBaseline` | `TextBaseline?` | `null` | 文本基线 |

## TableColumnWidth 子类

| 子类 | 说明 |
| --- | --- |
| `FixedColumnWidth(double)` | 固定宽度 |
| `FlexColumnWidth(double flex)` | 弹性宽度(默认 `1.0`) |
| `FractionColumnWidth(double fraction)` | 按总宽比例(0.0-1.0) |
| `IntrinsicColumnWidth()` | 按内容自适应 |
| `MaxColumnWidth(TableColumnWidth, double)` | 最大值约束 |
| `MinColumnWidth(TableColumnWidth, double)` | 最小值约束 |

## TableCellVerticalAlignment 取值

| 取值 | 说明 |
| --- | --- |
| `top` | 顶部对齐(默认) |
| `middle` | 居中对齐 |
| `bottom` | 底部对齐 |
| `baseline` | 基线对齐(需 `textBaseline`) |
| `fill` | 填充 |

## TableBorder 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `top` | `BorderSide` | `BorderSide.none` | 上边框 |
| `right` | `BorderSide` | `BorderSide.none` | 右边框 |
| `bottom` | `BorderSide` | `BorderSide.none` | 下边框 |
| `left` | `BorderSide` | `BorderSide.none` | 左边框 |
| `horizontalInside` | `BorderSide` | `BorderSide.none` | 行间分隔线 |
| `verticalInside` | `BorderSide` | `BorderSide.none` | 列间分隔线 |
| `borderRadius` | `BorderRadius` | `BorderRadius.zero` | 圆角 |

## DataTable 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `columns` | `List<DataColumn>` | 必填 | 列定义 |
| `rows` | `List<DataRow>` | 必填 | 行数据 |
| `dividerThickness` | `double?` | `1.0` | 分隔线厚度 |
| `columnSpacing` | `double?` | `56.0` | 列间距 |
| `headingRowHeight` | `double?` | `56.0` | 表头行高 |
| `dataRowHeight` | `double?` | `48.0`(M3 最小 48) | 数据行高 |
| `horizontalMargin` | `double?` | `24.0` | 水平外边距 |
| `checkboxHorizontalMargin` | `double?` | `null`(取 horizontalMargin) | 复选框水平边距 |
| `showCheckboxColumn` | `bool` | `true` | 是否显示复选列 |
| `showBottomBorder` | `bool?` | `false` | 是否显示底部边框 |
| `columnWidths` | `Map<int, TableColumnWidth>?` | `null` | 各列宽度 |
| `defaultColumnWidth` | `TableColumnWidth?` | `null` | 默认列宽 |
| `headingRowColor` | `MaterialStateProperty<Color?>?` | `null` | 表头背景色 |
| `dataRowColor` | `MaterialStateProperty<Color?>?` | `null` | 数据行背景色 |
| `dataRowMinHeight` | `double?` | `null`(默认 48) | 数据行最小高度(M3) |
| `dataRowMaxHeight` | `double?` | `null`(默认 64) | 数据行最大高度(M3) |

## DataColumn 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `label` | `Widget` | 必填 | 列标签 |
| `tooltip` | `String?` | `null` | 列提示(悬停) |
| `numeric` | `bool` | `false` | 是否为数值列(右对齐) |
| `onSort` | `DataColumnSortCallback?` | `null` | 排序回调 |
| `headingPadding` | `EdgeInsetsGeometry?` | `null` | 表头内边距 |

## DataRow 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `LocalKey?` | `null` | 行标识 |
| `selected` | `bool` | `false` | 是否选中 |
| `onSelectChanged` | `ValueChanged<bool?>?` | `null` | 选择变化回调 |
| `onLongPress` | `VoidCallback?` | `null` | 长按回调 |
| `cells` | `List<DataCell>` | `[]` | 单元格列表 |
| `color` | `MaterialStateProperty<Color?>?` | `null` | 行背景色 |

## DataCell 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget` | 必填 | 单元格内容 |
| `placeholder` | `bool` | `false` | 是否占位(灰色显示) |
| `showEditIcon` | `bool` | `false` | 是否显示编辑图标 |
| `onTap` | `VoidCallback?` | `null` | 点击回调 |
| `onTapUp` | `GestureTapUpCallback?` | `null` | 点击释放回调 |
| `onTapDown` | `GestureTapDownCallback?` | `null` | 点击按下回调 |
| `onTapCancel` | `GestureTapCancelCallback?` | `null` | 点击取消回调 |

## PaginatedDataTable 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `header` | `Widget?` | `null` | 表格标题 |
| `columns` | `List<DataColumn>` | 必填 | 列定义 |
| `rowsPerPage` | `int?` | `defaultRowsPerPage`(10) | 每页行数 |
| `onRowsPerPageChanged` | `ValueChanged<int?>?` | `null` | 每页行数变化 |
| `source` | `DataTableSource` | 必填 | 数据源(分页加载) |
| `currentPage` | `int` | `0` | 当前页(M3 已废弃,用 initialFirstRowIndex) |
| `initialFirstRowIndex` | `int` | `0` | 初始首行索引 |
| `onPageChanged` | `ValueChanged<int>?` | `null` | 翻页回调 |
| `dataRowHeight` | `double?` | `48.0` | 数据行高 |
| `headingRowHeight` | `double?` | `56.0` | 表头行高 |
| `horizontalMargin` | `double?` | `24.0` | 水平外边距 |
| `actions` | `List<Widget>?` | `null` | 头部操作按钮 |

## DataTableSource 抽象类方法

| 方法 | 返回 | 说明 |
| --- | --- | --- |
| `getRowCount()` | `int` | 总行数 |
| `getRow(int index)` | `DataRow?` | 获取指定行 |
| `selectedRowCount` | `int` | 选中行数(默认 0) |
| `addListener / removeListener` | `void` | 监听器(数据变化时通知) |
| `notifyListeners()` | `void` | 通知数据变化 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class TableFullSample extends StatefulWidget {
  const TableFullSample({super.key});

  @override
  State<TableFullSample> createState() => _TableFullSampleState();
}

class _TableFullSampleState extends State<TableFullSample> {
  int? _sortColumnIndex;
  bool _sortAscending = true;
  final List<_Person> _data = [
    _Person('张三', '设计师', '设计部', 28),
    _Person('李四', '工程师', '研发部', 32),
    _Person('王五', '产品经理', '产品部', 35),
    _Person('赵六', '测试', '质量部', 26),
  ];

  void _sort(int column, bool ascending) {
    setState(() {
      _sortColumnIndex = column;
      _sortAscending = ascending;
      _data.sort((a, b) {
        int cmp;
        switch (column) {
          case 0: cmp = a.name.compareTo(b.name); break;
          case 1: cmp = a.role.compareTo(b.role); break;
          case 2: cmp = a.dept.compareTo(b.dept); break;
          case 3: cmp = a.age.compareTo(b.age); break;
          default: cmp = 0;
        }
        return ascending ? cmp : -cmp;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Table 完整示例')),
      body: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: DataTable(
          sortColumnIndex: _sortColumnIndex,
          sortAscending: _sortAscending,
          columnSpacing: {spacing-md},
          horizontalMargin: {spacing-md},
          headingRowHeight: {size-md},
          dataRowMinHeight: {size-sm},
          dataRowMaxHeight: {size-md},
          headingRowColor: MaterialStateProperty.all({color-bg-secondary}),
          dataRowColor: MaterialStateProperty.resolveWith((states) {
            return states.contains(MaterialState.selected)
                ? {color-primary-container}
                : Colors.transparent;
          }),
          dividerThickness: 1,
          showCheckboxColumn: true,
          columns: [
            DataColumn(
              label: const Text('姓名'),
              onSort: _sort,
            ),
            DataColumn(label: const Text('职位'), onSort: _sort),
            DataColumn(label: const Text('部门'), onSort: _sort),
            DataColumn(label: const Text('年龄'), numeric: true, onSort: _sort),
          ],
          rows: _data.map((p) => DataRow(
            cells: [
              DataCell(Text(p.name), onTap: () => debugPrint('点击 ${p.name}')),
              DataCell(Text(p.role)),
              DataCell(Text(p.dept)),
              DataCell(Text('${p.age}')),
            ],
          )).toList(),
        ),
      ),
    );
  }
}

class _Person {
  final String name;
  final String role;
  final String dept;
  final int age;
  _Person(this.name, this.role, this.dept, this.age);
}
```

## 注意事项

- `Table` 要求所有 `TableRow` 子节点数量一致;不一致会抛异常。
- `DataTable` 不支持横向滚动,需用 `SingleChildScrollView(scrollDirection: Axis.horizontal)` 包裹;否则列过多会溢出。
- `DataTable` 不支持虚拟滚动,数据量大(> 1000 行)时性能差;**大数据集使用 `PaginatedDataTable` 或第三方 `pluto_grid`**。
- `PaginatedDataTable` 需实现 `DataTableSource` 抽象类;数据变化时调用 `notifyListeners()` 通知表格刷新。
- `DataRow.selected` 与 `onSelectChanged` 配合实现选择;`showCheckboxColumn: false` 隐藏复选列但保留 `onSelectChanged`。
- `DataColumn.onSort` 回调签名 `void Function(int columnIndex, bool ascending)`,需自行实现排序逻辑并 `setState`。
- `dataRowMinHeight` / `dataRowMaxHeight` 是 M3 新增(Flutter 3.7+),替代旧的 `dataRowHeight`;支持行高范围。
- M3 推荐使用 `dataRowColor: MaterialStateProperty` 替代旧的 `DataRow.color`,支持状态(如 selected)。
- 表格文字默认不换行;长文本需在 `DataCell` 内用 `Flexible` + `Text(softWrap: true)` 包裹。
