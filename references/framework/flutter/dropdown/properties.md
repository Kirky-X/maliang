# Flutter Dropdown 属性列表与默认值

本文档汇总 Material Design 3 下拉选择(`DropdownMenu` / `DropdownButton` / `DropdownButtonFormField`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## DropdownMenu<T> 属性(M3 推荐)

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `dropdownMenuEntries` | `List<DropdownMenuEntry<T>>` | 必填 | 选项列表 |
| `initialSelection` | `T?` | `null` | 初始选中值 |
| `onSelected` | `ValueChanged<T?>?` | `null` | 选择回调 |
| `controller` | `TextEditingController?` | `null` | 文本控制器(配合搜索) |
| `textEditingController` | `TextEditingController?` | `null` | 文本控制器(M3 新增,优先级高于 controller) |
| `label` | `Widget?` | `null` | 标签 |
| `enabled` | `bool` | `true` | 是否启用 |
| `width` | `double?` | `null`(默认 240) | 宽度 |
| `menuHeight` | `double?` | `null` | 菜单高度 |
| `leadingIcon` | `Widget?` | `null` | 前置图标 |
| `trailingIcon` | `Widget?` | `Icon(Icons.arrow_drop_down)` | 后置图标 |
| `selectedTrailingIcon` | `Widget?` | `Icon(Icons.arrow_drop_down)` | 选中态后置图标 |
| `inputDecorationTheme` | `InputDecorationTheme?` | `null` | 输入框主题 |
| `menuStyle` | `MenuStyle?` | `null` | 菜单样式 |
| `enableSearch` | `bool` | `true` | 是否启用搜索 |
| `enableFilter` | `bool` | `false` | 是否启用输入过滤 |
| `handleRequestFocusOnTap` | `bool?` | `null` | 点击时是否请求焦点 |
| `expandedInsets` | `EdgeInsets?` | `null` | 撑满边界 |
| `alignmentOffset` | `Offset?` | `null` | 弹出位置偏移 |

## DropdownMenuEntry<T> 属性

继承自 `MenuItemButton`。

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `T` | 必填 | 选项值 |
| `label` | `String` | 必填 | 显示文本 |
| `leadingIcon` | `Widget?` | `null` | 前置图标 |
| `trailingIcon` | `Widget?` | `null` | 后置图标 |
| `enabled` | `bool` | `true` | 是否启用 |
| `style` | `ButtonStyle?` | `null` | 样式 |
| `onTap` | `VoidCallback?` | `null` | 点击回调 |

## DropdownButton<T> 属性(M2 经典)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `T?` | 必填 | 当前选中值 |
| `items` | `List<DropdownMenuItem<T>>?` | 必填 | 选项列表 |
| `onChanged` | `ValueChanged<T?>?` | 必填 | 选择回调 |
| `onTap` | `VoidCallback?` | `null` | 点击回调 |
| `elevation` | `int` | `8` | 弹出菜单高度 |
| `style` | `TextStyle?` | `null`(取主题) | 文字样式 |
| `underline` | `Widget?` | 默认灰色线 | 下划线(传 `null` 隐藏) |
| `icon` | `Widget?` | `Icon(Icons.arrow_drop_down)` | 右侧图标 |
| `iconDisabledColor` | `Color?` | `null` | 禁用态图标色 |
| `iconEnabledColor` | `Color?` | `null` | 启用态图标色 |
| `iconSize` | `double` | `24.0` | 图标尺寸 |
| `isExpanded` | `bool` | `false` | 是否撑满宽度 |
| `itemHeight` | `double` | `kMinInteractiveDimension`(48) | 选项高度 |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `autofocus` | `bool` | `false` | 自动获焦 |
| `dropdownColor` | `Color?` | `{color-surface}` | 弹出菜单背景色 |
| `menuMaxHeight` | `double?` | `null` | 菜单最大高度 |
| `alignment` | `AlignmentGeometry` | `AlignmentDirectional.centerStart` | 对齐 |
| `borderRadius` | `BorderRadius?` | `null` | 菜单圆角(M3 新增) |

## DropdownMenuItem<T> 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `T` | 必填 | 选项值 |
| `child` | `Widget` | 必填 | 显示内容 |
| `enabled` | `bool` | `true` | 是否启用 |
| `alignment` | `AlignmentGeometry` | `AlignmentDirectional.centerStart` | 对齐 |
| `onTap` | `VoidCallback?` | `null` | 点击回调 |

## DropdownButtonFormField<T> 属性

继承自 `FormField<T>`,增加 Form 集成能力。

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `T?` | 必填 | 当前值 |
| `items` | `List<DropdownMenuItem<T>>?` | 必填 | 选项 |
| `onChanged` | `ValueChanged<T?>?` | 必填 | 选择回调 |
| `decoration` | `InputDecoration` | 必填 | 装饰(含 label/border 等) |
| `validator` | `FormFieldValidator<T>?` | `null` | 校验器 |
| `onSaved` | `FormFieldSetter<T>?` | `null` | 保存回调 |
| `restorationId` | `String?` | `null` | 状态恢复 ID |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Dropdown 完整示例:展示 M3 DropdownMenu + DropdownButtonFormField
class DropdownFullSample extends StatefulWidget {
  const DropdownFullSample({super.key});

  @override
  State<DropdownFullSample> createState() => _DropdownFullSampleState();
}

class _DropdownFullSampleState extends State<DropdownFullSample> {
  String? _selectedColor;
  final _formKey = GlobalKey<FormState>();
  String? _formValue;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Dropdown 完整示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. M3 DropdownMenu(带搜索)
            DropdownMenu<String>(
              width: {size-xl},
              label: const Text('选择颜色'),
              enableSearch: true,
              initialSelection: _selectedColor,
              onSelected: (v) => setState(() => _selectedColor = v),
              leadingIcon: Icon(Icons.palette, size: {icon-size-sm}, color: {color-primary}),
              menuStyle: MenuStyle(
                backgroundColor: MaterialStatePropertyAll({color-surface}),
                elevation: MaterialStatePropertyAll({elevation-md}),
                shape: MaterialStatePropertyAll(
                  RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular({radius-md}),
                  ),
                ),
              ),
              dropdownMenuEntries: const [
                DropdownMenuEntry(value: 'red', label: '红色'),
                DropdownMenuEntry(value: 'green', label: '绿色'),
                DropdownMenuEntry(value: 'blue', label: '蓝色'),
              ],
            ),
            SizedBox(height: {spacing-md}),
            // 2. DropdownButtonFormField(表单内)
            Form(
              key: _formKey,
              child: DropdownButtonFormField<String>(
                value: _formValue,
                decoration: InputDecoration(
                  labelText: '选择类型',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular({radius-sm}),
                  ),
                ),
                items: const [
                  DropdownMenuItem(value: 'type1', child: Text('类型 1')),
                  DropdownMenuItem(value: 'type2', child: Text('类型 2')),
                ],
                onChanged: (v) => setState(() => _formValue = v),
                validator: (v) => v == null ? '请选择类型' : null,
              ),
            ),
            SizedBox(height: {spacing-md}),
            FilledButton(
              onPressed: () {
                if (_formKey.currentState?.validate() ?? false) {
                  debugPrint('表单提交: $_formValue');
                }
              },
              child: const Text('提交'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

```dart
ThemeData(
  menuTheme: MenuThemeData(
    style: MenuStyle(
      backgroundColor: MaterialStatePropertyAll({color-surface}),
      surfaceTintColor: MaterialStatePropertyAll({color-surface-variant}),
      elevation: MaterialStatePropertyAll({elevation-md}),
      shape: MaterialStatePropertyAll(
        RoundedRectangleBorder(
          borderRadius: BorderRadius.circular({radius-md}),
        ),
      ),
    ),
  ),
)
```

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - DropdownMenu: https://api.flutter.dev/flutter/material/DropdownMenu-class.html
- API 参考 - DropdownMenuEntry: https://api.flutter.dev/flutter/material/DropdownMenuEntry-class.html
- API 参考 - DropdownButton: https://api.flutter.dev/flutter/material/DropdownButton-class.html
- API 参考 - DropdownMenuItem: https://api.flutter.dev/flutter/material/DropdownMenuItem-class.html
- API 参考 - DropdownButtonFormField: https://api.flutter.dev/flutter/material/DropdownButtonFormField-class.html
