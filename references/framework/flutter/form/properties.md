# Flutter Form 属性列表与默认值

本文档汇总 `Form` / `FormField` / `FormState` 的属性、默认值与回调。

## Form 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `GlobalKey<FormState>?` | `null` | 状态访问键(调用 validate/save) |
| `child` | `Widget` | 必填 | 表单内容 |
| `onChanged` | `VoidCallback?` | `null` | 任一字段变化时触发 |
| `autovalidateMode` | `AutovalidateMode` | `AutovalidateMode.disabled` | 自动校验时机 |
| `canValidateContent` | `CanValidateContent` | `CanValidateContent.always` | 何时可校验(M3 新增) |

## FormField 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `builder` | `FormFieldBuilder<T>` | 必填 | 字段构建函数 |
| `validator` | `FormFieldValidator<T>?` | `null` | 校验函数(返回错误文本或 null) |
| `initialValue` | `T?` | `null` | 初始值 |
| `onSaved` | `FormFieldSetter<T>?` | `null` | 保存回调 |
| `onChanged` | `ValueChanged<T?>?` | `null` | 值变化回调 |
| `onReset` | `FormFieldSetter<T>?` | `null` | 重置回调 |
| `enabled` | `bool` | `true` | 是否启用 |
| `autovalidateMode` | `AutovalidateMode` | `AutovalidateMode.disabled` | 自动校验时机 |
| `restorationId` | `String?` | `null` | 状态恢复 ID |

## FormState 方法

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `save` | `void save()` | 调用所有字段 onSaved |
| `validate` | `bool validate()` | 调用所有字段 validator,返回是否有错 |
| `reset` | `void reset()` | 重置所有字段到 initialValue |
| `hasError` | `bool get hasError` | 当前是否有错误 |

## FormFieldState 方法

| 方法/属性 | 类型 | 说明 |
| --- | --- | --- |
| `value` | `T?` | 当前值(可读写) |
| `hasError` | `bool` | 是否有错误 |
| `errorText` | `String?` | 当前错误文本 |
| `isValid` | `bool` | 是否有效 |
| `validate()` | `bool` | 触发校验 |
| `save()` | `void` | 触发 onSaved |
| `reset()` | `void` | 重置到 initialValue |
| `didChange(T?)` | `void` | 主动更新值 |

## AutovalidateMode 取值

| 取值 | 行为 |
| --- | --- |
| `disabled` | 不自动校验(默认) |
| `onUserInteraction` | 用户交互后开始校验 |
| `always` | 总是校验(每次 build) |

## 完整示例

```dart
import 'package:flutter/material.dart';

class FormFullSample extends StatefulWidget {
  const FormFullSample({super.key});

  @override
  State<FormFullSample> createState() => _FormFullSampleState();
}

class _FormFullSampleState extends State<FormFullSample> {
  final _key = GlobalKey<FormState>();
  final _data = <String, dynamic>{};
  AutovalidateMode _mode = AutovalidateMode.disabled;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Form 完整示例')),
      body: Form(
        key: _key,
        autovalidateMode: _mode,
        onChanged: () => debugPrint('表单内容变化'),
        child: ListView(
          padding: const EdgeInsets.all({spacing-md}),
          children: [
            // 文本字段
            TextFormField(
              decoration: const InputDecoration(labelText: '用户名'),
              validator: (v) =>
                  (v == null || v.isEmpty) ? '必填' : null,
              onSaved: (v) => _data['name'] = v,
            ),
            TextFormField(
              decoration: const InputDecoration(labelText: '邮箱'),
              keyboardType: TextInputType.emailAddress,
              validator: (v) =>
                  (v == null || !v.contains('@')) ? '邮箱格式错误' : null,
              onSaved: (v) => _data['email'] = v,
            ),
            TextFormField(
              decoration: const InputDecoration(labelText: '年龄'),
              keyboardType: TextInputType.number,
              validator: (v) {
                final n = int.tryParse(v ?? '');
                if (n == null) return '需为数字';
                if (n < 0 || n > 150) return '范围 0-150';
                return null;
              },
              onSaved: (v) => _data['age'] = int.parse(v!),
            ),
            // 下拉字段
            DropdownButtonFormField<String>(
              decoration: const InputDecoration(labelText: '性别'),
              items: const [
                DropdownMenuItem(value: 'M', child: Text('男')),
                DropdownMenuItem(value: 'F', child: Text('女')),
              ],
              validator: (v) => v == null ? '请选择' : null,
              onSaved: (v) => _data['gender'] = v,
            ),
            const SizedBox(height: {spacing-lg}),
            Row(
              children: [
                FilledButton(
                  child: const Text('提交'),
                  onPressed: () {
                    if (_key.currentState!.validate()) {
                      _key.currentState!.save();
                      setState(() => _mode = AutovalidateMode.disabled);
                      debugPrint('数据: $_data');
                    } else {
                      // 校验失败后改为持续校验
                      setState(() =>
                          _mode = AutovalidateMode.always);
                    }
                  },
                ),
                const SizedBox(width: {spacing-sm}),
                TextButton(
                  child: const Text('重置'),
                  onPressed: () {
                    _key.currentState!.reset();
                    _data.clear();
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

## 注意事项

- `GlobalKey<FormState>` 必须稳定(`StatelessWidget` 重建时需保持 key 不变,通常放 `State` 字段)
- `validator` 返回 null 表示通过;返回字符串为错误文本
- `onSaved` 在 `FormState.save()` 时被调用,用于把字段值收集到模型对象
- `autovalidateMode: onUserInteraction` 是推荐策略,避免首次进入就报错
- 自定义 `FormField<T>` 时,在 `builder` 中通过 `FormFieldState` 的 `value`/`errorText` 渲染
- `reset()` 会恢复到 `initialValue`,不会清空(除非 initialValue 为 null)
- 表单提交失败后建议切到 `AutovalidateMode.always`,持续给用户反馈
