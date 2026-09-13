# Flutter Select Widget 定义

## Widget 定义

Flutter Material 提供**数据录入型**下拉选择器(区别于 `PopupMenuButton` 动作菜单):M2 经典 `DropdownButton<T>`、M3 菜单式 `DropdownMenu<T>` 与表单内 `DropdownButtonFormField<T>`。用于从选项集中选定一个值回填表单/筛选状态。

| Select 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 经典下拉 | `DropdownButton<T>` | `StatefulWidget` | M2 风格,轻量触发器 + 选项列表 |
| 表单下拉 | `DropdownButtonFormField<T>` | `FormField<T>` | 配合 `Form` 校验的下拉选择 |
| M3 下拉 | `DropdownMenu<T>` | `StatefulWidget` | M3 菜单式下拉(推荐,支持搜索过滤) |

> 与动作菜单 [`menu`](../menu/widget.md)(`PopupMenuButton`)区分:Select 提交值,PopupMenuButton 触发命令。

## 构造函数

### DropdownButtonFormField

```dart
const DropdownButtonFormField<T>({
  Key? key,
  required List<DropdownMenuItem<T>>? items,
  T? value,
  ValueChanged<T?>? onChanged,
  FormFieldValidator<T>? validator,
  InputDecoration decoration = const InputDecoration(),
  int elevation = 8,
  Widget? icon,
  double iconSize = 24.0,
  bool isExpanded = false,
  bool autofocus = false,
  FocusNode? focusNode,
  AutovalidateMode? autovalidateMode,
})
```

### DropdownMenu(M3)

```dart
const DropdownMenu<T>({
  Key? key,
  required List<DropdownMenuEntry<T>> entries,
  TextEditingController? controller,
  bool enableSearch = true,
  bool enableFilter = false,
  ValueChanged<T?>? onSelected,
  InputDecorationTheme? inputDecorationTheme,
  DropdownMenuTextStyle textStyle = const DropdownMenuTextStyle(),
  double? menuHeight,
  int? initialSelection,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `items` / `entries` | `List<DropdownMenuItem<T>>` / `List<DropdownMenuEntry<T>>` | 选项列表 |
| `value` / `initialSelection` | `T?` / `int?` | 当前选中值 / 初始选中索引 |
| `onChanged` / `onSelected` | `ValueChanged<T?>?` | 选中回调 |
| `hint` | `Widget?` | 未选择时占位提示 |
| `isExpanded` | `bool` | 触发器是否撑满可用宽度 |
| `icon` | `Widget?` | 触发器箭头图标(默认 `arrow_drop_down`) |
| `validator` | `FormFieldValidator<T>?` | 表单校验(FormField 系列) |
| `enableSearch` | `bool` | DropdownMenu 内置搜索(对齐 `select-searchable`) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Select 最小示例:表单内常规选择(3-10 项)
class SelectSample extends StatefulWidget {
  const SelectSample({super.key});

  @override
  State<SelectSample> createState() => _SelectSampleState();
}

class _SelectSampleState extends State<SelectSample> {
  String? _city;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Select 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: DropdownButtonFormField<String>(
          value: _city,
          hint: const Text('请选择城市'),
          decoration: const InputDecoration(
            labelText: '城市',
            border: OutlineInputBorder(),
          ),
          items: ['上海', '北京', '广州']
              .map((c) => DropdownMenuItem(value: c, child: Text(c)))
              .toList(),
          onChanged: (v) => setState(() => _city = v),
        ),
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
DropdownMenu<String>(
  initialSelection: 0,
  dropdownMenuEntries: [
    const DropdownMenuEntry(value: '综合排序', label: '综合排序'),
    const DropdownMenuEntry(value: '价格从低到高', label: '价格从低到高'),
    const DropdownMenuEntry(value: '最新发布', label: '最新发布'),
  ],
  onSelected: (v) => setState(() => _sort = v),
  inputDecorationTheme: const InputDecorationTheme(
    filled: true,
    fillColor: {color-bg-secondary},
    border: OutlineInputBorder(
      borderRadius: BorderRadius.all(Radius.circular({radius-full})),
    ),
  ),
)
```

> 注:示例中的 `{color-bg-secondary}`、`{radius-full}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- API 参考 - DropdownButton: https://api.flutter.dev/flutter/material/DropdownButton-class.html
- API 参考 - DropdownMenu: https://api.flutter.dev/flutter/material/DropdownMenu-class.html
- Material 3 - Select menus: https://m3.material.io/components/select-menus
