# Flutter Input 属性列表与默认值

本文档汇总 `TextField` / `TextFormField` 的属性、默认值与回调。颜色/尺寸默认值以 design token 形式给出。

## TextField 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `controller` | `TextEditingController?` | `null` | 文本控制器(读写文本/选区) |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `decoration` | `InputDecoration?` | `const InputDecoration()` | 外观配置 |
| `keyboardType` | `TextInputType?` | `null`(按 maxLines 推断) | 键盘类型 |
| `textInputAction` | `TextInputAction?` | `null` | 回车键动作 |
| `textCapitalization` | `TextCapitalization` | `TextCapitalization.none` | 自动大写策略 |
| `style` | `TextStyle?` | `null`(取主题) | 文本样式 |
| `textAlign` | `TextAlign` | `TextAlign.start` | 文本对齐 |
| `readOnly` | `bool` | `false` | 只读 |
| `showCursor` | `bool?` | `null` | 是否显示光标 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |
| `obscuringCharacter` | `String` | `'•'` | 密文字符 |
| `obscureText` | `bool` | `false` | 密文(密码) |
| `autocorrect` | `bool` | `true` | 自动纠错 |
| `enableSuggestions` | `bool` | `true` | 联想建议 |
| `maxLines` | `int?` | `1` | 最大行数(null 不限) |
| `minLines` | `int?` | `null` | 最小行数 |
| `expands` | `bool` | `false` | 撑满父级高度 |
| `maxLength` | `int?` | `null` | 最大字符数 |
| `maxLengthEnforcement` | `MaxLengthEnforcement?` | `null` | 超长处理策略 |
| `onChanged` | `ValueChanged<String>?` | `null` | 文本变化 |
| `onSubmitted` | `ValueChanged<String>?` | `null` | 回车提交 |
| `onEditingComplete` | `VoidCallback?` | `null` | 编辑完成 |
| `onTap` | `VoidCallback?` | `null` | 点击输入框 |
| `onTapOutside` | `TapRegionCallback?` | `null` | 点击外部(用于失焦) |
| `inputFormatters` | `List<TextInputFormatter>?` | `null` | 输入格式化 |
| `enabled` | `bool?` | `null`(取主题 disabled) | 是否启用 |
| `cursorWidth` | `double` | `2.0` | 光标宽度 |
| `cursorColor` | `Color?` | `null`(取主题) | 光标颜色 |
| `scrollPadding` | `EdgeInsets` | `EdgeInsets.all(20)` | 键盘弹出时滚动留白 |

## InputDecoration 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `icon` | `Widget?` | `null` | 输入框外前置图标 |
| `labelText` | `String?` | `null` | 标签(浮动) |
| `labelStyle` | `TextStyle?` | `null` | 标签样式 |
| `helperText` | `String?` | `null` | 辅助文本(底部) |
| `helperStyle` | `TextStyle?` | `null` | 辅助文本样式 |
| `hintText` | `String?` | `null` | 占位提示 |
| `hintStyle` | `TextStyle?` | `null` | 提示样式 |
| `errorText` | `String?` | `null` | 错误文本(覆盖 helperText) |
| `errorStyle` | `TextStyle?` | `null` | 错误样式 |
| `prefixIcon` | `Widget?` | `null` | 前置图标(框内) |
| `prefixText` | `String?` | `null` | 前置文本 |
| `suffixIcon` | `Widget?` | `null` | 后置图标(框内) |
| `suffixText` | `String?` | `null` | 后置文本 |
| `counterText` | `String?` | `null` | 计数器文本 |
| `border` | `InputBorder?` | `null` | 边框(默认 UnderlineInputBorder) |
| `enabledBorder` | `InputBorder?` | `null` | 启用态边框 |
| `focusedBorder` | `InputBorder?` | `null` | 聚焦态边框 |
| `errorBorder` | `InputBorder?` | `null` | 错误态边框 |
| `focusedErrorBorder` | `InputBorder?` | `null` | 聚焦且错误态边框 |
| `filled` | `bool` | `false` | 是否填充背景 |
| `fillColor` | `Color?` | `null` | 填充色 |
| `contentPadding` | `EdgeInsetsGeometry?` | `null` | 内边距 |

## TextInputType 常用取值

| 取值 | 用途 |
| --- | --- |
| `text` | 普通文本(默认) |
| `number` | 数字(无小数点) |
| `numberWithOptions` | 数字(可带小数/符号) |
| `emailAddress` | 邮箱(显示 @ . 键) |
| `phone` | 电话(显示数字 + # *) |
| `url` | URL(显示 / . 键) |
| `multiline` | 多行(回车换行) |
| `visiblePassword` | 可见密码(关闭自动纠错) |

## 事件回调

| 回调 | 签名 | 触发时机 |
| --- | --- | --- |
| `onChanged` | `void Function(String)` | 文本变化(每次按键) |
| `onSubmitted` | `void Function(String)` | 回车提交(单行) |
| `onEditingComplete` | `void Function()` | 编辑完成(回车) |
| `onTap` | `void Function()` | 点击输入框 |
| `onTapOutside` | `void Function(PointerDownEvent)` | 点击输入框外部 |

## TextEditingController 常用方法

| 方法/属性 | 说明 |
| --- | --- |
| `text` | 当前完整文本(可读写) |
| `selection` | 当前选区(TextSelection) |
| `value` | TextEditingValue(text + selection + composing) |
| `addListener(callback)` | 监听变化(配合 setState 刷新 UI) |
| `clear()` | 清空文本 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class InputFullSample extends StatefulWidget {
  const InputFullSample({super.key});

  @override
  State<InputFullSample> createState() => _InputFullSampleState();
}

class _InputFullSampleState extends State<InputFullSample> {
  final _formKey = GlobalKey<FormState>();
  final _emailCtrl = TextEditingController();
  final _pwdCtrl = TextEditingController();
  bool _obscure = true;

  @override
  void dispose() {
    _emailCtrl.dispose();
    _pwdCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Input 完整示例')),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all({spacing-md}),
          children: [
            // 邮箱(带校验)
            TextFormField(
              controller: _emailCtrl,
              keyboardType: TextInputType.emailAddress,
              decoration: InputDecoration(
                labelText: '邮箱',
                hintText: 'name@example.com',
                prefixIcon: const Icon(Icons.email),
                filled: true,
                fillColor: {color-bg-secondary},
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular({radius-md}),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular({radius-md}),
                  borderSide: BorderSide(color: {color-primary}, width: 2),
                ),
              ),
              validator: (v) => (v == null || !v.contains('@'))
                  ? '请输入有效邮箱'
                  : null,
            ),
            const SizedBox(height: {spacing-md}),
            // 密码(密文 + 显隐切换)
            TextFormField(
              controller: _pwdCtrl,
              obscureText: _obscure,
              maxLength: 20,
              decoration: InputDecoration(
                labelText: '密码',
                prefixIcon: const Icon(Icons.lock),
                suffixIcon: IconButton(
                  icon: Icon(_obscure ? Icons.visibility : Icons.visibility_off),
                  onPressed: () => setState(() => _obscure = !_obscure),
                ),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular({radius-md}),
                ),
              ),
              validator: (v) => (v == null || v.length < 6)
                  ? '密码至少 6 位'
                  : null,
            ),
            const SizedBox(height: {spacing-md}),
            // 数字输入(限制)
            TextFormField(
              keyboardType: TextInputType.number,
              inputFormatters: [FilteringTextInputFormatter.digitsOnly],
              decoration: const InputDecoration(
                labelText: '手机号',
                prefixText: '+86 ',
              ),
            ),
            const SizedBox(height: {spacing-lg}),
            FilledButton(
              onPressed: () {
                if (_formKey.currentState!.validate()) {
                  debugPrint('提交: ${_emailCtrl.text}');
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

## 注意事项

- `TextEditingController` 必须在 `dispose()` 中释放,避免内存泄漏
- `obscureText: true` 时自动关闭 `autocorrect` 与 `enableSuggestions`
- `maxLines: null` 表示多行不限,但需配合 `expands` 或父级有界高度
- `onTapOutside` 用于点击外部收起键盘:`(e) => FocusManager.instance.primaryFocus?.unfocus()`
- `inputFormatters` 优先级高于 `maxLength`,可用 `LengthLimitingTextInputFormatter` 限制长度
- 表单校验场景必须用 `TextFormField` + `Form` 祖先,`Form.validate()` 触发所有子级 `validator`
