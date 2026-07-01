# Flutter Dropdown Widget 定义

## Widget 定义

Flutter Material Design 3 提供两套下拉选择 Widget:经典 `DropdownButton<T>`(M2 风格,仍可用)与 M3 新增的 `DropdownMenu<T>`(推荐使用)。`DropdownButtonFormField<T>` 用于表单场景。

| Dropdown 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| DropdownButton | `DropdownButton<T>` | `StatefulWidget` | 经典下拉选择(M2 风格) |
| DropdownButtonFormField | `DropdownButtonFormField<T>` | `FormField<T>` | 表单内下拉选择(配合 `Form`) |
| DropdownMenu(M3) | `DropdownMenu<T>` | `StatefulWidget` | M3 菜单式下拉(推荐) |
| DropdownMenuEntry(M3) | `DropdownMenuEntry<T>` | `MenuItemButton` | M3 下拉菜单项 |

> M3 推荐 `DropdownMenu`,支持搜索过滤、自定义宽度、键盘导航,UI 与 `MenuAnchor` 一致。

## 构造函数

### DropdownButton<T>

```dart
DropdownButton<T>({
  super.key,
  required this.value,                    // 当前选中值
  required this.items,                    // 选项列表(List<DropdownMenuItem<T>>)
  this.onChanged,                         // 选择回调
  this.onTap,                             // 点击回调
  this.elevation = 8,                     // 弹出菜单高度
  this.style,                             // 文字样式
  this.underline,                         // 下划线(默认灰色线,null 表示无)
  this.icon,                              // 右侧图标
  this.iconDisabledColor,                 // 禁用态图标色
  this.iconEnabledColor,                  // 启用态图标色
  this.iconSize = 24.0,                   // 图标尺寸
  this.isExpanded = false,                // 是否撑满宽度
  this.itemHeight = kMinInteractiveDimension,  // 选项高度(默认 48)
  this.focusNode,
  this.autofocus = false,
  this.dropdownColor,                     // 弹出菜单背景色
  this.menuMaxHeight,                     // 菜单最大高度
  this.enableFeedback,
  this.alignment = AlignmentDirectional.centerStart,
  this.borderRadius,                      // 菜单圆角(M3 新增)
})
```

### DropdownMenu<T>(M3)

```dart
DropdownMenu<T>({
  super.key,
  required this.dropdownMenuEntries,      // 选项列表(List<DropdownMenuEntry<T>>)
  this.initialSelection,                  // 初始选中值
  this.onSelected,                        // 选择回调
  this.controller,                        // 文本控制器(用于搜索过滤)
  this.label,                             // 标签(显示在输入框上方)
  this.enabled = true,
  this.width,                             // 宽度
  this.menuHeight,                        // 菜单高度
  this.leadingIcon,                       // 前置图标
  this.trailingIcon,                      // 后置图标(默认下拉箭头)
  this.selectedTrailingIcon,              // 选中态后置图标
  this.inputDecorationTheme,              // 输入框主题
  this.menuStyle,                         // 菜单样式
  this.enableSearch = true,               // 是否启用搜索过滤
  this.enableFilter = false,              // 是否启用输入过滤
  this.requestFocusOnTap = true,
  this.expandedInsets,                    // 撑满边界(M3 新增)
  this.alignmentOffset,
  this.textEditingController,
})
```

## 核心属性(DropdownMenu M3)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `dropdownMenuEntries` | `List<DropdownMenuEntry<T>>` | 选项列表 |
| `initialSelection` | `T?` | 初始选中值 |
| `onSelected` | `ValueChanged<T?>?` | 选择回调 |
| `controller` | `TextEditingController?` | 文本控制器(配合搜索) |
| `label` | `Widget?` | 标签 |
| `width` | `double?` | 宽度 |
| `leadingIcon` | `Widget?` | 前置图标 |
| `trailingIcon` | `Widget?` | 后置图标 |
| `enableSearch` | `bool` | 是否启用搜索 |
| `enableFilter` | `bool` | 是否启用过滤 |
| `menuStyle` | `MenuStyle?` | 菜单样式 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Dropdown 最小示例:展示 M3 DropdownMenu
class DropdownSample extends StatefulWidget {
  const DropdownSample({super.key});

  @override
  State<DropdownSample> createState() => _DropdownSampleState();
}

class _DropdownSampleState extends State<DropdownSample> {
  String? _selected;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Dropdown 示例')),
      body: Center(
        child: DropdownMenu<String>(
          width: {size-xl},
          label: const Text('选择颜色'),
          initialSelection: _selected,
          onSelected: (value) => setState(() => _selected = value),
          dropdownMenuEntries: const [
            DropdownMenuEntry(value: 'red', label: '红色'),
            DropdownMenuEntry(value: 'green', label: '绿色'),
            DropdownMenuEntry(value: 'blue', label: '蓝色'),
          ],
        ),
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
DropdownMenu<String>(
  width: {size-xl},
  label: Text(
    '选择颜色',
    style: TextStyle(fontSize: {font-size-sm}, color: {color-text-secondary}),
  ),
  menuStyle: MenuStyle(
    backgroundColor: MaterialStatePropertyAll({color-surface}),
    surfaceTintColor: MaterialStatePropertyAll({color-surface-variant}),
    elevation: MaterialStatePropertyAll({elevation-md}),
    shape: MaterialStatePropertyAll(
      RoundedRectangleBorder(
        borderRadius: BorderRadius.circular({radius-md}),
      ),
    ),
  ),
  leadingIcon: Icon(Icons.palette, size: {icon-size-sm}, color: {color-primary}),
  trailingIcon: Icon(Icons.arrow_drop_down, size: {icon-size-md}, color: {color-text-secondary}),
  selectedTrailingIcon: Icon(Icons.check, size: {icon-size-sm}, color: {color-primary}),
  dropdownMenuEntries: [
    DropdownMenuEntry(
      value: 'red',
      label: '红色',
      style: MenuItemButton.styleFrom(
        foregroundColor: {color-text-primary},
        backgroundColor: {color-surface},
      ),
    ),
  ],
)
```

> 注:示例中的 `{color-primary}`、`{color-surface}`、`{elevation-md}`、`{radius-md}`、`{size-xl}`、`{icon-size-sm}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - DropdownMenu: https://api.flutter.dev/flutter/material/DropdownMenu-class.html
- API 参考 - DropdownMenuEntry: https://api.flutter.dev/flutter/material/DropdownMenuEntry-class.html
- API 参考 - DropdownButton: https://api.flutter.dev/flutter/material/DropdownButton-class.html
- API 参考 - DropdownButtonFormField: https://api.flutter.dev/flutter/material/DropdownButtonFormField-class.html
