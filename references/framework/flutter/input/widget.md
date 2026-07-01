# Flutter Input Widget 定义

## Widget 定义

Flutter 文本输入由 `TextField`(继承自 `StatefulWidget`)承载,结合 `InputDecoration` 控制外观、`TextEditingController` 控制文本、`FocusNode` 控制焦点。表单校验场景用 `TextFormField`(继承自 `TextField`,实现 `FormField<String>`),通过 `Form` 祖先统一管理校验。

| Widget | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `TextField` | `TextField` | `StatefulWidget` | 通用文本输入 |
| `TextFormField` | `TextFormField` | `FormField<String>` | 表单内带校验的输入 |
| `InputDecoration` | `InputDecoration` | - | 外观配置(标签/边框/图标) |
| `TextEditingController` | `TextEditingController` | `ValueNotifier` | 文本控制器 |
| `FocusNode` | `FocusNode` | `ChangeNotifier` | 焦点节点 |
| `KeyboardType` | `KeyboardType` | - | 键盘类型(数字/邮箱/电话) |

## 构造函数

### TextField

```dart
const TextField({
  super.key,
  TextEditingController? controller,
  FocusNode? focusNode,
  InputDecoration? decoration = const InputDecoration(),
  TextInputType? keyboardType,
  TextInputAction? textInputAction,
  TextCapitalization textCapitalization = TextCapitalization.none,
  TextStyle? style,
  StrutStyle? strutStyle,
  TextAlign textAlign = TextAlign.start,
  TextAlignVertical? textAlignVertical,
  TextDirection? textDirection,
  bool readOnly = false,
  bool? showCursor,
  bool autofocus = false,
  String obscuringCharacter = '•',
  bool obscureText = false,
  bool autocorrect = true,
  SmartDashesType? smartDashesType,
  bool enableSuggestions = true,
  int? maxLines = 1,
  int? minLines,
  bool expands = false,
  int? maxLength,
  MaxLengthEnforcement? maxLengthEnforcement,
  ValueChanged<String>? onChanged,         // 文本变化
  ValueChanged<String>? onSubmitted,       // 提交(回车)
  VoidCallback? onEditingComplete,
  VoidCallback? onTap,
  TapRegionCallback? onTapOutside,
  List<TextInputFormatter>? inputFormatters,
  bool? enabled,
  bool? ignorePointers,
  double cursorWidth = 2.0,
  Color? cursorColor,
  Radius? cursorRadius,
  bool? cursorHeight,
  Brightness? keyboardAppearance,
  EdgeInsets scrollPadding = const EdgeInsets.all(20),
  ...
})
```

### TextFormField

构造参数与 `TextField` 基本一致,额外增加表单校验字段:

```dart
TextFormField({
  ... // TextField 全部参数
  FormFieldValidator<String>? validator,   // 校验函数
  String? initialValue,
  AutovalidateMode autovalidateMode = AutovalidateMode.disabled,
  ValueChanged<String?>? onSaved,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `controller` | `TextEditingController?` | 文本控制器(读写文本) |
| `focusNode` | `FocusNode?` | 焦点控制 |
| `decoration` | `InputDecoration?` | 外观配置 |
| `keyboardType` | `TextInputType?` | 键盘类型 |
| `obscureText` | `bool` | 是否密文(密码) |
| `maxLines` | `int?` | 最大行数(null 为多行不限) |
| `maxLength` | `int?` | 最大字符数 |
| `readOnly` | `bool` | 只读(可选中文但不可编辑) |
| `enabled` | `bool?` | 是否启用(false 时禁用) |
| `onChanged` | `ValueChanged<String>?` | 文本变化回调 |
| `onSubmitted` | `ValueChanged<String>?` | 回车提交回调 |
| `inputFormatters` | `List<TextInputFormatter>?` | 输入格式化(限制/过滤) |
| `validator` | `FormFieldValidator<String>?` | 校验函数(仅 TextFormField) |
| `autovalidateMode` | `AutovalidateMode` | 自动校验时机 |

## 最小示例

```dart
import 'package:flutter/material.dart';

class InputSample extends StatefulWidget {
  const InputSample({super.key});

  @override
  State<InputSample> createState() => _InputSampleState();
}

class _InputSampleState extends State<InputSample> {
  final _controller = TextEditingController();
  String _text = '';

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Input 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                labelText: '用户名',
                hintText: '请输入用户名',
                prefixIcon: const Icon(Icons.person),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular({radius-md}),
                ),
              ),
              onChanged: (v) => setState(() => _text = v),
            ),
            const SizedBox(height: {spacing-sm}),
            Text('当前输入: $_text'),
          ],
        ),
      ),
    );
  }
}
```

## 参考链接

- Flutter 官方文档 - 输入 & 表单: https://docs.flutter.cn/ui/interactivity/input
- Cookbook - 创建输入框并调整样式: https://docs.flutter.cn/cookbook/forms/text-input
- Cookbook - 读取输入框内容: https://docs.flutter.cn/cookbook/forms/retrieve-input
- Cookbook - 处理输入框内容变动: https://docs.flutter.cn/cookbook/forms/text-field-changes
- Cookbook - 管理输入框之间的焦点: https://docs.flutter.cn/cookbook/forms/focus
- API 参考 - TextField: https://api.flutter.dev/flutter/material/TextField-class.html
- API 参考 - TextFormField: https://api.flutter.dev/flutter/material/TextFormField-class.html
- API 参考 - InputDecoration: https://api.flutter.dev/flutter/material/InputDecoration-class.html
