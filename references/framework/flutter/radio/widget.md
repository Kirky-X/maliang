# Flutter Radio Widget 定义

## Widget 定义

Flutter Material Design 3 提供单选按钮 `Radio<T>`(StatelessWidget),用于在互斥组中选择一项。`Radio` 仅渲染圆形按钮,不含标签;通常用 `ListTile` / `Row` 包裹以添加文本。状态由 `groupValue` 集中管理,所有 `Radio` 共享同一 `groupValue`。

| Radio 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 单选按钮 | `Radio<T>` | `StatelessWidget` | 圆形单选按钮(M3) |
| 单选列表项 | `RadioListTile<T>` | `StatelessWidget` | 含标签/副标题的单选列表项 |
| 自适应单选 | `CupertinoRadio` | `StatelessWidget` | iOS 风格单选(Cupertino) |

> `Radio` 不维护自身选中态,所有状态由父级通过 `groupValue` + `onChanged` 集中管理(受控组件模式)。

## 构造函数

### Radio

```dart
const Radio<T>({
  Key? key,
  required T value,
  required T? groupValue,
  required ValueChanged<T?>? onChanged,
  MouseCursor? mouseCursor,
  bool toggleable = false,
  Color? activeColor,
  MaterialStateProperty<Color?>? fillColor,
  Color? hoverColor,
  MaterialStateProperty<Color?>? overlayColor,
  double? splashRadius,
  VisualDensity? visualDensity,
  MaterialTapTargetSize? materialTapTargetSize,
  FocusNode? focusNode,
  bool autofocus = false,
})
```

### RadioListTile

```dart
const RadioListTile<T>({
  Key? key,
  required T value,
  required T? groupValue,
  required ValueChanged<T?>? onChanged,
  Widget? title,
  Widget? subtitle,
  bool isThreeLine = false,
  bool dense,
  Widget? secondary,
  bool selected = false,
  bool toggleable = false,
  Color? activeColor,
  MaterialStateProperty<Color?>? fillColor,
  Color? hoverColor,
  MaterialStateProperty<Color?>? overlayColor,
  double? splashRadius,
  ListTileControlAffinity controlAffinity = ListTileControlAffinity.platform,
  bool? enabled,
  MouseCursor? mouseCursor,
  FocusNode? focusNode,
  bool autofocus = false,
  EdgeInsetsGeometry? contentPadding,
  ShapeBorder? shape,
  Color? selectedTileColor,
  ValueChanged<bool>? onFocusChange,
  bool? enableFeedback,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `value` | `T` | 当前项的值 |
| `groupValue` | `T?` | 单选组当前选中值 |
| `onChanged` | `ValueChanged<T?>?` | 选择变化回调;为 `null` 时禁用 |
| `toggleable` | `bool` | 是否允许二次点击取消选择(默认 `false`) |
| `activeColor` | `Color?` | 选中态颜色(已废弃,优先用 `fillColor`) |
| `fillColor` | `MaterialStateProperty<Color?>?` | 填充色(支持状态) |
| `hoverColor` | `Color?` | 悬停色 |
| `overlayColor` | `MaterialStateProperty<Color?>?` | 按压叠加色 |
| `splashRadius` | `double?` | 水波纹半径 |
| `mouseCursor` | `MouseCursor?` | 鼠标光标 |
| `focusNode` | `FocusNode?` | 焦点节点 |
| `autofocus` | `bool` | 自动获取焦点 |
| `visualDensity` | `VisualDensity?` | 视觉密度 |
| `materialTapTargetSize` | `MaterialTapTargetSize?` | 点击目标尺寸 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Radio 最小示例:互斥单选组
class RadioSample extends StatefulWidget {
  const RadioSample({super.key});

  @override
  State<RadioSample> createState() => _RadioSampleState();
}

enum Gender { male, female, other }

class _RadioSampleState extends State<RadioSample> {
  Gender? _selected = Gender.male;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Radio 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: Gender.values.map((g) {
            return RadioListTile<Gender>(
              value: g,
              groupValue: _selected,
              onChanged: (v) => setState(() => _selected = v),
              title: Text(_label(g)),
              subtitle: Text(_desc(g)),
              activeColor: {color-primary},
            );
          }).toList(),
        ),
      ),
    );
  }

  String _label(Gender g) {
    switch (g) {
      case Gender.male: return '男';
      case Gender.female: return '女';
      case Gender.other: return '其他';
    }
  }

  String _desc(Gender g) => '选择了 $_label(g)';
}
```

## 自定义样式(MD3 主题映射)

```dart
Radio<Gender>(
  value: Gender.male,
  groupValue: _selected,
  onChanged: (v) => setState(() => _selected = v),
  fillColor: MaterialStateProperty.resolveWith((states) {
    if (states.contains(MaterialState.disabled)) {
      return {color-text-disabled};
    }
    if (states.contains(MaterialState.selected)) {
      return {color-primary};
    }
    return {color-border-default};
  }),
  overlayColor: MaterialStateProperty.all({color-primary}),
  splashRadius: {radius-sm},
)
```

> 注:示例中的 `{color-primary}`、`{spacing-md}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Radio: https://api.flutter.dev/flutter/material/Radio-class.html
- API 参考 - RadioListTile: https://api.flutter.dev/flutter/material/RadioListTile-class.html
