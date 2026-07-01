# Flutter Button 属性列表与默认值

本文档汇总 Material Design 3 按钮(`ElevatedButton` / `FilledButton` / `OutlinedButton` / `TextButton`)的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## 通用构造参数

四种按钮共享同一组构造参数(继承自 `ButtonStyleButton`)。

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `onPressed` | `VoidCallback?` | 必填 | 点击回调;为 `null` 时按钮禁用 |
| `onLongPress` | `VoidCallback?` | `null` | 长按回调 |
| `onHover` | `ValueChanged<bool>?` | `null` | 鼠标悬停状态变化 |
| `onFocusChange` | `ValueChanged<bool>?` | `null` | 焦点获取/失去回调 |
| `style` | `ButtonStyle?` | `null`(取主题默认) | 按钮样式,覆盖主题 |
| `focusNode` | `FocusNode?` | `null` | 焦点控制节点 |
| `autofocus` | `bool` | `false` | 是否自动获取焦点 |
| `clipBehavior` | `Clip` | `Clip.none` | 子节点裁剪行为 |
| `statesController` | `MaterialStatesController?` | `null` | 状态控制器,可监听 pressed/hovered/focused/disabled |
| `child` | `Widget` | 必填 | 按钮内容,通常为 `Text` |

## ButtonStyle 属性(MaterialStateProperty)

通过 `style` 字段传入,优先级高于主题。下表列出 MD3 主题下的默认取值(以 token 引用表示)。

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `textStyle` | `MaterialStateProperty<TextStyle?>` | `{font-size-md}` / `{font-weight-medium}` | 文本样式 |
| `backgroundColor` | `MaterialStateProperty<Color?>` | 见下表 | 背景色 |
| `foregroundColor` | `MaterialStateProperty<Color?>` | 见下表 | 前景色(文本/图标) |
| `overlayColor` | `MaterialStateProperty<Color?>` | `{color-on-surface}` 12% | 按压/悬停叠加色 |
| `shadowColor` | `MaterialStateProperty<Color?>` | `{color-shadow}` | 阴影色 |
| `surfaceTintColor` | `MaterialStateProperty<Color?>` | `{color-primary}` | 表面染色(M3 elevation tint) |
| `elevation` | `MaterialStateProperty<double?>` | 见下表 | z 轴高度 |
| `padding` | `MaterialStateProperty<EdgeInsetsGeometry?>` | 左右 `{spacing-md}`,上下 `{spacing-sm}` | 内边距 |
| `minimumSize` | `MaterialStateProperty<Size?>` | `Size(64, 40)` | 最小尺寸 |
| `fixedSize` | `MaterialStateProperty<Size?>` | `null` | 固定尺寸 |
| `maximumSize` | `MaterialStateProperty<Size?>` | `Size.infinite` | 最大尺寸 |
| `side` | `MaterialStateProperty<BorderSide?>` | 见下表 | 边框 |
| `shape` | `MaterialStateProperty<OutlinedBorder?>` | `StadiumBorder` | 形状(MD3 默认全圆角) |
| `enabledMouseCursor` | `MaterialStateProperty<MouseCursor?>` | `SystemMouseCursors.click` | 启用态鼠标光标 |
| `disabledMouseCursor` | `MaterialStateProperty<MouseCursor?>` | `SystemMouseCursors.basic` | 禁用态鼠标光标 |
| `visualDensity` | `VisualDensity?` | `VisualDensity.standard` | 视觉密度 |
| `tapTargetSize` | `MaterialTapTargetSize?` | `MaterialTapTargetSize.padded` | 点击目标尺寸 |
| `animationDuration` | `Duration?` | `kThemeChangeDuration`(~200ms) | 状态切换动画时长 |
| `enableFeedback` | `bool?` | `true` | 触觉/声音反馈 |
| `alignment` | `AlignmentGeometry?` | `Alignment.center` | 子节点对齐 |

## 各按钮 MD3 默认值对比

| 按钮 | `backgroundColor` | `foregroundColor` | `elevation` | `side` |
| --- | --- | --- | --- | --- |
| `ElevatedButton` | `{color-surface}` | `{color-on-surface}` | 启用 `{elevation-sm}`,禁用 `0` | `BorderSide.none` |
| `FilledButton` | `{color-primary}` | `{color-on-primary}` | `0` | `BorderSide.none` |
| `FilledButton.tonal` | `{color-secondary-container}` | `{color-on-secondary-container}` | `0` | `BorderSide.none` |
| `OutlinedButton` | `Colors.transparent` | `{color-primary}` | `0` | `{color-outline}` 1px |
| `TextButton` | `Colors.transparent` | `{color-primary}` | `0` | `BorderSide.none` |

禁用态:`backgroundColor` 通常降级为 `{color-surface}` 系低对比色,`foregroundColor` 降级为 `{color-on-surface}` 38%。

## 事件回调

| 回调 | 签名 | 触发时机 |
| --- | --- | --- |
| `onPressed` | `void Function()` | 点击释放(且未长按) |
| `onLongPress` | `void Function()` | 长按超过 `kLongPressTimeout`(500ms) |
| `onHover` | `void Function(bool isHovered)` | 鼠标进入/离开(桌面/Web) |
| `onFocusChange` | `void Function(bool hasFocus)` | 焦点获取/失去 |

> `onPressed` 与 `onLongPress` 互斥:长按触发后不会再触发 `onPressed`。
> `onPressed == null` 时按钮处于禁用态,所有交互回调均不触发。

## 状态监听

通过 `statesController` 可监听 `MaterialState` 集合变化(pressed / hovered / focused / disabled):

```dart
final statesController = MaterialStatesController();

ElevatedButton(
  statesController: statesController,
  onPressed: () {},
  child: const Text('监听状态'),
);

statesController.addListener(() {
  final states = statesController.value;
  if (states.contains(MaterialState.pressed)) {
    // 按压中
  }
  if (states.contains(MaterialState.disabled)) {
    // 禁用态
  }
});
```

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Button 完整示例:涵盖四种按钮、自定义样式、状态回调
class ButtonFullSample extends StatefulWidget {
  const ButtonFullSample({super.key});

  @override
  State<ButtonFullSample> createState() => _ButtonFullSampleState();
}

class _ButtonFullSampleState extends State<ButtonFullSample> {
  String _lastEvent = '无事件';
  bool _isHovering = false;

  void _log(String event) {
    setState(() => _lastEvent = event);
    debugPrint(event);
  }

  @override
  Widget build(BuildContext context) {
    // 自定义 ButtonStyle:颜色全部引用 design token
    final primaryStyle = ElevatedButton.styleFrom(
      backgroundColor: {color-primary},
      foregroundColor: {color-on-primary},
      disabledBackgroundColor: {color-surface-variant},
      disabledForegroundColor: {color-on-surface},
      elevation: {elevation-sm},
      padding: const EdgeInsets.symmetric(
        horizontal: {spacing-md},
        vertical: {spacing-sm},
      ),
      minimumSize: const Size(96, 40),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular({radius-md}),
      ),
      textStyle: const TextStyle(
        fontSize: {font-size-md},
        fontWeight: FontWeight.w500,
      ),
      enableFeedback: true,
    );

    return Scaffold(
      appBar: AppBar(title: const Text('Button 完整示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 1. ElevatedButton
            ElevatedButton(
              style: primaryStyle,
              onPressed: () => _log('ElevatedButton 点击'),
              onLongPress: () => _log('ElevatedButton 长按'),
              child: const Text('ElevatedButton'),
            ),
            // 2. FilledButton
            FilledButton(
              onPressed: () => _log('FilledButton 点击'),
              child: const Text('FilledButton'),
            ),
            // 3. FilledButton.tonal
            FilledButton.tonal(
              onPressed: () => _log('FilledButton.tonal 点击'),
              child: const Text('FilledButton.tonal'),
            ),
            // 4. OutlinedButton
            OutlinedButton(
              onPressed: () => _log('OutlinedButton 点击'),
              child: const Text('OutlinedButton'),
            ),
            // 5. TextButton
            TextButton(
              onPressed: () => _log('TextButton 点击'),
              child: const Text('TextButton'),
            ),
            // 6. 带图标 + 悬停监听
            ElevatedButton.icon(
              style: primaryStyle,
              onPressed: () => _log('ElevatedButton.icon 点击'),
              onHover: (hovered) {
                setState(() => _isHovering = hovered);
                _log('Hover: $hovered');
              },
              onFocusChange: (focused) => _log('Focus: $focused'),
              icon: const Icon(Icons.download),
              label: const Text('下载'),
            ),
            // 7. 禁用态
            const ElevatedButton(
              onPressed: null,
              child: Text('禁用态'),
            ),
            const SizedBox(height: {spacing-md}),
            // 事件展示区
            Text('最近事件: $_lastEvent'),
            Text('悬停中: $_isHovering'),
          ],
        ),
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

在 `ThemeData` 中通过 `elevatedButtonTheme` / `filledButtonTheme` / `outlinedButtonTheme` / `textButtonTheme` 注入主题级样式,所有 token 在此集中解析:

```dart
ThemeData(
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: {color-primary},
      foregroundColor: {color-on-primary},
      // ...其余 token
    ),
  ),
)
```
