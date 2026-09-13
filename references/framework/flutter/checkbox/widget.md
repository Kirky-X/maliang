# Flutter Checkbox Widget 定义

## Widget 定义

Flutter Material Design 3 提供复选框 `Checkbox`(StatelessWidget),用于多项选择。M3 支持**三态**(tristate):选中/未选中/半选(空框内短横线),`tristate: true` 时值在 `true`/`false`/`null` 间循环。`Checkbox` 仅渲染方框,不含标签;用 `CheckboxListTile` 添加标题/副标题。

| Checkbox 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 复选框 | `Checkbox` | `StatelessWidget` | 方框复选(M3,tristate 原生支持) |
| 复选列表项 | `CheckboxListTile` | `StatelessWidget` | 含标题/副标题/前后置的列表项 |
| 自适应复选 | `CupertinoCheckbox` | `StatelessWidget` | iOS 风格复选(Cupertino) |

> `Checkbox` 是受控组件,状态由父级通过 `value` + `onChanged` 集中管理。

## 构造函数

### Checkbox

```dart
const Checkbox({
  Key? key,
  required bool? value,
  required ValueChanged<bool?>? onChanged,
  bool tristate = false,
  MouseCursor? mouseCursor,
  Color? activeColor,
  MaterialStateProperty<Color?>? fillColor,
  Color? checkColor,
  Color? hoverColor,
  Color? overlayColor,
  double? splashRadius,
  MaterialTapTargetSize? materialTapTargetSize,
  VisualDensity? visualDensity,
  FocusNode? focusNode,
  bool autofocus = false,
  OutlinedBorder? shape,
  BorderSide? side,
})
```

### CheckboxListTile

```dart
const CheckboxListTile({
  Key? key,
  required bool? value,
  required ValueChanged<bool?>? onChanged,
  required Widget title,
  Widget? subtitle,
  bool tristate = false,
  bool isThreeLine = false,
  bool? dense,
  Widget? secondary,
  bool selected = false,
  Color? activeColor,
  ListTileControlAffinity controlAffinity = ListTileControlAffinity.platform,
  bool? enabled,
  EdgeInsetsGeometry? contentPadding,
  ShapeBorder? shape,
  Color? tileColor,
  BorderSide? side,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `value` | `bool?` | 选中态;`tristate` 时 `null` 表示半选 |
| `onChanged` | `ValueChanged<bool?>?` | 变化回调;为 `null` 时禁用 |
| `tristate` | `bool` | 是否启用三态(默认 `false`) |
| `activeColor` | `Color?` | 选中态填充色 |
| `fillColor` | `MaterialStateProperty<Color?>?` | 填充色(支持状态) |
| `checkColor` | `Color?` | 对勾颜色 |
| `shape` | `OutlinedBorder?` | 框形状(M3 默认圆角方形) |
| `side` | `BorderSide?` | 未选中态边框样式 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Checkbox 最小示例:三态全选 + 子项列表
class CheckboxSample extends StatefulWidget {
  const CheckboxSample({super.key});

  @override
  State<CheckboxSample> createState() => _CheckboxSampleState();
}

class _CheckboxSampleState extends State<CheckboxSample> {
  bool? _all = false;
  final List<bool> _items = [true, false, false];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Checkbox 示例')),
      body: Column(
        children: [
          CheckboxListTile(
            value: _all,
            tristate: true, // 三态:true 全选 / null 半选 / false 全不选
            onChanged: (v) => setState(() {
              _all = v;
              _items.setAll(0, [for (final _ in _items) v ?? false]);
            }),
            title: const Text('全选'),
            activeColor: {color-primary},
          ),
          for (var i = 0; i < _items.length; i++)
            CheckboxListTile(
              value: _items[i],
              onChanged: (v) => setState(() => _items[i] = v ?? false),
              title: Text('选项 ${i + 1}'),
              activeColor: {color-primary},
            ),
        ],
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
Checkbox(
  value: _checked,
  tristate: true,
  onChanged: (v) => setState(() => _checked = v),
  fillColor: MaterialStateProperty.resolveWith((states) {
    if (states.contains(MaterialState.disabled)) {
      return {color-text-disabled};
    }
    if (states.contains(MaterialState.selected)) {
      return {color-primary};
    }
    return {color-bg-primary};
  }),
  checkColor: {color-text-inverse},
  side: const BorderSide(color: {color-border-default}),
)
```

> 注:示例中的 `{color-primary}`、`{color-bg-primary}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- API 参考 - Checkbox: https://api.flutter.dev/flutter/material/Checkbox-class.html
- API 参考 - CheckboxListTile: https://api.flutter.dev/flutter/material/CheckboxListTile-class.html
- Material 3 - Checkbox: https://m3.material.io/components/checkbox
