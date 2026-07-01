# Flutter Form Widget 定义

## Widget 定义

Flutter 表单由 `Form`(继承自 `StatefulWidget`)作为容器,统一下属 `FormField<T>` 子节点(如 `TextFormField`、`DropdownButtonFormField`)。`FormState` 提供 `validate()` / `save()` / `reset()` 批量操作。每个 `FormField` 通过 `validator` 校验、`onSaved` 提取值。

| Widget/类 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `Form` | `Form` | `StatefulWidget` | 表单容器(统一校验/保存) |
| `FormField<T>` | `FormField<T>` | `StatefulWidget` | 抽象表单字段 |
| `FormState` | `FormState` | `State<Form>` | 表单状态(校验/保存/重置) |
| `TextFormField` | `TextFormField` | `FormField<String>` | 文本输入字段 |
| `DropdownButtonFormField` | `DropdownButtonFormField<T>` | `FormField<T>` | 下拉选择字段 |
| `FormFieldValidator<T>` | - | - | 校验函数类型 `String? Function(T?)` |

## 构造函数

### Form

```dart
const Form({
  super.key,
  required Widget child,
  VoidCallback? onChanged,                 // 任一字段变化触发
  AutovalidateMode autovalidateMode = AutovalidateMode.disabled,
  CanValidateContent canValidateContent = CanValidateContent.always,
})
```

### FormField<T>

```dart
const FormField({
  super.key,
  required FormFieldBuilder<T> builder,    // 字段构建函数
  FormFieldValidator<T>? validator,        // 校验函数
  T? initialValue,                          // 初始值
  AutovalidateMode autovalidateMode = AutovalidateMode.disabled,
  bool enabled = true,
  FormFieldSetter<T>? onSaved,              // 保存回调
  ValueChanged<T?>? onChanged,
  FormFieldSetter<T>? onReset,
  Widget? restorationId,
})
```

### FormState 常用方法

```dart
class FormState extends State<Form> {
  void save();                                  // 触发所有字段 onSaved
  bool validate();                              // 触发所有字段 validator
  void reset();                                 // 重置所有字段到初始值
  bool hasError;                                // 是否存在错误
  Iterable<FormFieldState> fields;              // 所有字段状态
}
```

## 核心属性

### Form 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `child` | `Widget` | 表单内容(含 FormField 子节点) |
| `onChanged` | `VoidCallback?` | 任一字段变化时触发 |
| `autovalidateMode` | `AutovalidateMode` | 自动校验时机(disabled/onUserInteraction/always) |

### FormField 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `builder` | `FormFieldBuilder<T>` | 字段构建函数 |
| `validator` | `FormFieldValidator<T>?` | 校验函数(返回错误文本或 null) |
| `initialValue` | `T?` | 初始值 |
| `onSaved` | `FormFieldSetter<T>?` | 保存回调 |
| `onChanged` | `ValueChanged<T?>?` | 值变化回调 |
| `autovalidateMode` | `AutovalidateMode` | 自动校验时机 |

### AutovalidateMode 取值

| 取值 | 行为 |
| --- | --- |
| `disabled` | 不自动校验(需手动调 validate) |
| `onUserInteraction` | 用户交互后开始自动校验 |
| `always` | 总是自动校验 |

## 最小示例

```dart
import 'package:flutter/material.dart';

class FormSample extends StatefulWidget {
  const FormSample({super.key});

  @override
  State<FormSample> createState() => _FormSampleState();
}

class _FormSampleState extends State<FormSample> {
  final _key = GlobalKey<FormState>();
  String _email = '';
  String _pwd = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Form 示例')),
      body: Form(
        key: _key,
        child: Padding(
          padding: const EdgeInsets.all({spacing-md}),
          child: Column(
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: '邮箱'),
                validator: (v) =>
                    (v == null || !v.contains('@')) ? '邮箱无效' : null,
                onSaved: (v) => _email = v ?? '',
              ),
              TextFormField(
                obscureText: true,
                decoration: const InputDecoration(labelText: '密码'),
                validator: (v) =>
                    (v == null || v.length < 6) ? '至少 6 位' : null,
                onSaved: (v) => _pwd = v ?? '',
              ),
              const SizedBox(height: {spacing-lg}),
              FilledButton(
                child: const Text('提交'),
                onPressed: () {
                  if (_key.currentState!.validate()) {
                    _key.currentState!.save();
                    debugPrint('提交: $_email / $_pwd');
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## 参考链接

- Flutter 官方文档 - 输入 & 表单: https://docs.flutter.cn/ui/interactivity/input
- Cookbook - 构建具有校验功能的表单: https://docs.flutter.cn/cookbook/forms/validation
- Cookbook - 管理输入框之间的焦点: https://docs.flutter.cn/cookbook/forms/focus
- API 参考 - Form: https://api.flutter.dev/flutter/widgets/Form-class.html
- API 参考 - FormField: https://api.flutter.dev/flutter/widgets/FormField-class.html
- API 参考 - FormState: https://api.flutter.dev/flutter/widgets/FormState-class.html
