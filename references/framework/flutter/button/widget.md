# Flutter Button Widget 定义

## Widget 定义

Flutter Material Design 3 提供一组继承自 `ButtonStyleButton` 的按钮 Widget,均基于 `StatelessWidget` 实现(内部由 `Material` + `InkResponse` 维护交互态)。所有按钮通过 `build()` 方法构造,核心差异在于默认 `ButtonStyle`(颜色、形状、elevation)。

| Button 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| ElevatedButton | `ElevatedButton` | `ButtonStyleButton` | 高优先级操作,带阴影的凸起按钮 |
| FilledButton | `FilledButton` | `ButtonStyleButton` | 重要操作(M3 推荐),填充背景 |
| FilledButton.tonal | `FilledButton` | `ButtonStyleButton` | 次重要操作,次级色调填充 |
| OutlinedButton | `OutlinedButton` | `ButtonStyleButton` | 中等优先级,带边框 |
| TextButton | `TextButton` | `ButtonStyleButton` | 低优先级,仅文本(用于对话框/工具栏) |

> 所有按钮都遵循 MD3 规范,禁用态由 `onPressed == null` 控制。

## 构造函数

### ElevatedButton

```dart
const ElevatedButton({
  super.key,
  required super.onPressed,    // 点击回调;为 null 时按钮处于禁用态
  super.onLongPress,           // 长按回调
  super.onHover,               // 悬停回调
  super.onFocusChange,         // 焦点变化回调
  super.style,                 // ButtonStyle,覆盖主题默认样式
  super.focusNode,
  super.autofocus = false,
  super.clipBehavior = Clip.none,
  super.statesController,
  required super.child,        // 子节点,通常为 Text 或 Icon
})
```

### FilledButton / FilledButton.tonal

```dart
const FilledButton({
  super.key,
  required super.onPressed,
  super.onLongPress,
  super.onHover,
  super.onFocusChange,
  super.style,
  super.focusNode,
  super.autofocus = false,
  super.clipBehavior = Clip.none,
  super.statesController,
  required super.child,
})

// 工厂构造:次级色调填充
const FilledButton.tonal({ ... 同上 ... })
```

### OutlinedButton

```dart
const OutlinedButton({
  super.key,
  required super.onPressed,
  super.onLongPress,
  super.onHover,
  super.onFocusChange,
  super.style,
  super.focusNode,
  super.autofocus = false,
  super.clipBehavior = Clip.none,
  super.statesController,
  required super.child,
})
```

### TextButton

```dart
const TextButton({
  super.key,
  required super.onPressed,
  super.onLongPress,
  super.onHover,
  super.onFocusChange,
  super.style,
  super.focusNode,
  super.autofocus = false,
  super.clipBehavior = Clip.none,
  super.statesController,
  required super.child,
})
```

### 图标按钮构造器(`.icon` 命名构造)

每种按钮均提供 `.icon` 工厂构造,用于在文本前置一个图标:

```dart
ElevatedButton.icon({
  required super.onPressed,
  super.onLongPress,
  super.style,
  required Widget icon,    // 图标
  required Widget label,   // 文本
  ...
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `onPressed` | `VoidCallback?` | 点击事件回调;为 `null` 时按钮禁用 |
| `onLongPress` | `VoidCallback?` | 长按事件回调 |
| `onHover` | `ValueChanged<bool>?` | 鼠标悬停状态变化(MD3 hover 态) |
| `onFocusChange` | `ValueChanged<bool>?` | 焦点变化 |
| `style` | `ButtonStyle?` | 覆盖主题样式,通过 `ButtonStyle` 或 `styleFrom` 工厂构造 |
| `focusNode` | `FocusNode?` | 控制焦点 |
| `autofocus` | `bool` | 是否自动获取焦点,默认 `false` |
| `clipBehavior` | `Clip` | 裁剪行为,默认 `Clip.none` |
| `statesController` | `MaterialStatesController?` | 控制并监听交互状态 |
| `child` | `Widget` | 按钮内容,通常为 `Text` |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// 按钮最小示例:展示 MD3 四种基础按钮
class ButtonSample extends StatelessWidget {
  const ButtonSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Button 示例')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 凸起按钮
            ElevatedButton(
              onPressed: () => _handlePress('ElevatedButton'),
              child: const Text('ElevatedButton'),
            ),
            // 填充按钮(M3 推荐)
            FilledButton(
              onPressed: () => _handlePress('FilledButton'),
              child: const Text('FilledButton'),
            ),
            // 次级色调填充
            FilledButton.tonal(
              onPressed: () => _handlePress('FilledButton.tonal'),
              child: const Text('FilledButton.tonal'),
            ),
            // 描边按钮
            OutlinedButton(
              onPressed: () => _handlePress('OutlinedButton'),
              child: const Text('OutlinedButton'),
            ),
            // 文本按钮
            TextButton(
              onPressed: () => _handlePress('TextButton'),
              child: const Text('TextButton'),
            ),
            // 带图标的按钮
            ElevatedButton.icon(
              onPressed: () => _handlePress('ElevatedButton.icon'),
              icon: const Icon(Icons.add),
              label: const Text('新增'),
            ),
            // 禁用态:onPressed 为 null
            const ElevatedButton(
              onPressed: null,
              child: Text('禁用态'),
            ),
          ],
        ),
      ),
    );
  }

  void _handlePress(String name) {
    // 实际项目中替换为业务逻辑
    debugPrint('点击了 $name');
  }
}
```

## 自定义样式(MD3 主题映射)

通过 `ElevatedButton.styleFrom`(或对应类的 `styleFrom`)快速覆盖样式,颜色值统一使用 design token 引用,不在代码中硬编码:

```dart
ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: {color-primary},        // 背景 token
    foregroundColor: {color-on-primary},     // 前景 token
    elevation: {elevation-md},               // 高度 token
    padding: const EdgeInsets.symmetric(
      horizontal: {spacing-md},
      vertical: {spacing-sm},
    ),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-md}),
    ),
    textStyle: TextStyle(fontSize: {font-size-md}),
  ),
  onPressed: () {},
  child: const Text('自定义样式'),
)
```

> 注:示例中的 `{color-primary}`、`{font-size-md}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。
