# Flutter Select 属性列表与默认值

本文档汇总 `DropdownButtonFormField<T>` 与 `DropdownMenu<T>` 的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## DropdownButtonFormField 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `items` | `List<DropdownMenuItem<T>>?` | 必填 | 选项列表 |
| `value` | `T?` | `null` | 当前选中值 |
| `onChanged` | `ValueChanged<T?>?` | 必填 | 选中回调;`null` 时禁用 |
| `validator` | `FormFieldValidator<T>?` | `null` | 表单校验函数 |
| `decoration` | `InputDecoration` | `InputDecoration()` | 输入框装饰(label/hint/border) |
| `elevation` | `int` | `8` | 下拉面板海拔 |
| `icon` | `Widget?` | `arrow_drop_down` | 触发器箭头 |
| `iconSize` | `double` | `24.0` | 箭头尺寸 |
| `isExpanded` | `bool` | `false` | 触发器撑满宽度 |
| `isDense` | `bool` | `false` | 紧凑高度 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |
| `autovalidateMode` | `AutovalidateMode?` | `null` | 校验触发时机 |

## DropdownMenu(M3)构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `entries` | `List<DropdownMenuEntry<T>>` | 必填 | 选项列表(label + leadingIcon + trailingIcon) |
| `initialSelection` | `int?` | `null` | 初始选中索引 |
| `controller` | `TextEditingController?` | `null` | 触发器文本控制器 |
| `enableSearch` | `bool` | `true` | 键入过滤选项(`select-searchable` 语义) |
| `enableFilter` | `bool` | `false` | 过滤模式 |
| `onSelected` | `ValueChanged<T?>?` | `null` | 选中回调 |
| `inputDecorationTheme` | `InputDecorationTheme?` | `null` | 触发器装饰主题 |
| `menuHeight` | `double?` | `null`(默认 ≤ 40% 视口) | 下拉面板最大高度 |
| `expandedInsets` | `EdgeInsets?` | `null` | 设置后触发器撑满宽度 |

## DropdownMenuItem 关键参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `T` | 必填 | 该项的值 |
| `child` | `Widget` | 必填 | 该项内容 |
| `enabled` | `bool` | `true` | 是否可选 |
| `alignment` | `AlignmentDirectional` | `centerStart` | 内容对齐 |

## 状态(MD3)

| 状态 | 触发条件 | 建议样式 |
| --- | --- | --- |
| 未选择 | `value == null` | hint 用 `{color-text-secondary}` |
| 已选择 | `value != null` | 文本 `{color-text-primary}` |
| 禁用 | `onChanged == null` | `{color-text-disabled}` |
| 错误 | `validator` 不通过 | `{color-error}` 边框 + errorText |

## 事件回调

| 回调 | 签名 | 触发时机 |
| --- | --- | --- |
| `onChanged` | `void Function(T?)` | 选中某项;面板收起后触发 |
| `onSaved`(FormField) | `void Function(T?)` | `Form.save()` 时 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class SelectFullSample extends StatefulWidget {
  const SelectFullSample({super.key});

  @override
  State<SelectFullSample> createState() => _SelectFullSampleState();
}

class _SelectFullSampleState extends State<SelectFullSample> {
  final _formKey = GlobalKey<FormState>();
  String? _category;
  String _sort = '综合排序';

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          DropdownButtonFormField<String>(
            value: _category,
            hint: const Text('请选择分类'),
            decoration: const InputDecoration(labelText: '商品分类'),
            items: ['数码', '家电', '服饰', '食品']
                .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                .toList(),
            validator: (v) => v == null ? '请选择分类' : null,
            onChanged: (v) => setState(() => _category = v),
          ),
          const SizedBox(height: {spacing-md}),
          DropdownMenu<String>(
            initialSelection: 0,
            enableSearch: true,
            inputDecorationTheme: const InputDecorationTheme(
              filled: true,
              fillColor: {color-bg-secondary},
            ),
            dropdownMenuEntries: const [
              DropdownMenuEntry(value: '综合排序', label: '综合排序'),
              DropdownMenuEntry(value: '价格从低到高', label: '价格从低到高'),
              DropdownMenuEntry(value: '价格从高到低', label: '价格从高到低'),
              DropdownMenuEntry(value: '最新发布', label: '最新发布'),
            ],
            onSelected: (v) => setState(() => _sort = v ?? _sort),
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- **与动作菜单分工** — 表单/筛选选值用 `DropdownButtonFormField` / `DropdownMenu`;命令触发用 `PopupMenuButton`(menu 类),不得互相替代。
- `DropdownMenuItem.value` 在组内必须唯一;`value` 必须匹配某个 item,否则触发断言。
- 选项 >10 时启用 `DropdownMenu(enableSearch: true)`(对齐 vocabulary `select-searchable`),或改组合方案(`TextField` + `Overlay` 列表)。
- 面板过高的长列表设 `menuHeight`,内部自动滚动;项目内容用 `DropdownMenuItem(child: ListTile(...))` 支持双行。
- 无障碍:`labelText` 必填语义;展开面板自动挂载语义节点,方向键 + Enter 可选。
