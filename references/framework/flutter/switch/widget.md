# Flutter Switch Widget 定义

## Widget 定义

Flutter Material Design 3 提供开关组件 `Switch`(StatelessWidget),用于在开/关两态之间切换。M3 版本相比 M2 视觉变化显著:取消轨道外凸拇指、增加状态图标、新增 `thumbIcon` 自定义图标。Cupertino 风格开关使用 `CupertinoSwitch`。

| Switch 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| M3 开关 | `Switch` | `StatelessWidget` | Material Design 3 开关 |
| 开关列表项 | `SwitchListTile` | `StatelessWidget` | 含标签/副标题的开关列表项 |
| iOS 风格开关 | `CupertinoSwitch` | `StatefulWidget` | Cupertino 风格(iOS) |

> `Switch` 是受控组件,状态由 `value` + `onChanged` 集中管理;`onChanged == null` 时禁用。

## 构造函数

### Switch(M3)

```dart
const Switch({
  Key? key,
  required bool value,
  required ValueChanged<bool>? onChanged,
  Color? activeColor,
  Color? activeTrackColor,
  Color? inactiveThumbColor,
  Color? inactiveTrackColor,
  ImageProvider? activeThumbImage,
  ImageProvider? onThumbImage,
  ImageProvider? inactiveThumbImage,
  MaterialStateProperty<Color?>? thumbColor,
  MaterialStateProperty<Color?>? trackColor,
  MaterialStateProperty<Icon?>? thumbIcon,
  MaterialStateProperty<Color?>? overlayColor,
  double? splashRadius,
  MaterialTapTargetSize? materialTapTargetSize,
  MouseCursor? mouseCursor,
  FocusNode? focusNode,
  ValueChanged<bool>? onFocusChange,
  bool autofocus = false,
  DragStartBehavior dragStartBehavior = DragStartBehavior.start,
})
```

### Switch.adaptive(平台自适应)

```dart
Switch.adaptive({
  ...同 Switch...
})
// iOS 上使用 CupertinoSwitch,其他平台使用 Switch
```

### SwitchListTile

```dart
const SwitchListTile({
  Key? key,
  required bool value,
  required ValueChanged<bool>? onChanged,
  Widget? title,
  Widget? subtitle,
  bool isThreeLine = false,
  bool? dense,
  Widget? secondary,
  bool selected = false,
  Color? activeColor,
  Color? activeTrackColor,
  Color? inactiveThumbColor,
  Color? inactiveTrackColor,
  ImageProvider? activeThumbImage,
  ImageProvider? inactiveThumbImage,
  ListTileControlAffinity controlAffinity = ListTileControlAffinity.platform,
  bool? enabled,
  Color? hoverColor,
  MaterialStateProperty<Color?>? overlayColor,
  MouseCursor? mouseCursor,
  FocusNode? focusNode,
  ValueChanged<bool>? onFocusChange,
  bool autofocus = false,
  EdgeInsetsGeometry? contentPadding,
  ShapeBorder? shape,
  Color? selectedTileColor,
  bool? enableFeedback,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `value` | `bool` | 当前开关状态 |
| `onChanged` | `ValueChanged<bool>?` | 状态变化回调;为 `null` 时禁用 |
| `activeColor` | `Color?` | 开启态拇指颜色(已废弃,用 thumbColor) |
| `activeTrackColor` | `Color?` | 开启态轨道颜色 |
| `inactiveThumbColor` | `Color?` | 关闭态拇指颜色 |
| `inactiveTrackColor` | `Color?` | 关闭态轨道颜色 |
| `thumbColor` | `MaterialStateProperty<Color?>?` | 拇指颜色(支持状态) |
| `trackColor` | `MaterialStateProperty<Color?>?` | 轨道颜色(支持状态) |
| `thumbIcon` | `MaterialStateProperty<Icon?>?` | 拇指图标(M3 新增) |
| `overlayColor` | `MaterialStateProperty<Color?>?` | 按压/悬停叠加色 |
| `splashRadius` | `double?` | 水波纹半径 |
| `materialTapTargetSize` | `MaterialTapTargetSize?` | 点击目标尺寸 |
| `mouseCursor` | `MouseCursor?` | 鼠标光标 |
| `focusNode` | `FocusNode?` | 焦点节点 |
| `autofocus` | `bool` | 自动获取焦点 |
| `dragStartBehavior` | `DragStartBehavior` | 拖拽开始时机 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Switch 最小示例:M3 开关 + SwitchListTile
class SwitchSample extends StatefulWidget {
  const SwitchSample({super.key});

  @override
  State<SwitchSample> createState() => _SwitchSampleState();
}

class _SwitchSampleState extends State<SwitchSample> {
  bool _wifi = true;
  bool _bluetooth = false;
  bool _airplane = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Switch 示例')),
      body: ListView(
        children: [
          SwitchListTile(
            value: _wifi,
            onChanged: (v) => setState(() => _wifi = v),
            title: const Text('Wi-Fi'),
            subtitle: const Text('开启无线网络'),
            secondary: const Icon(Icons.wifi),
            activeColor: {color-primary},
          ),
          SwitchListTile(
            value: _bluetooth,
            onChanged: (v) => setState(() => _bluetooth = v),
            title: const Text('蓝牙'),
            secondary: const Icon(Icons.bluetooth),
          ),
          // 自适应开关(iOS 上使用 Cupertino 风格)
          SwitchListTile.adaptive(
            value: _airplane,
            onChanged: (v) => setState(() => _airplane = v),
            title: const Text('飞行模式'),
            secondary: const Icon(Icons.flight),
          ),
          const Divider(),
          // 独立 Switch(无标签)
          Padding(
            padding: const EdgeInsets.all({spacing-md}),
            child: Row(
              children: [
                const Text('独立开关'),
                const Spacer(),
                Switch(
                  value: _wifi,
                  onChanged: (v) => setState(() => _wifi = v),
                ),
              ],
            ),
          ),
          // 禁用态
          const SwitchListTile(
            value: false,
            onChanged: null,
            title: Text('禁用项'),
            subtitle: Text('onChanged 为 null 时禁用'),
          ),
        ],
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射 + thumbIcon)

```dart
Switch(
  value: _value,
  onChanged: (v) => setState(() => _value = v),
  // M3 推荐用 thumbColor / trackColor 替代 activeColor 系列
  thumbColor: MaterialStateProperty.resolveWith((states) {
    if (states.contains(MaterialState.disabled)) {
      return {color-text-disabled};
    }
    if (states.contains(MaterialState.selected)) {
      return {color-on-primary};
    }
    return {color-surface-variant};
  }),
  trackColor: MaterialStateProperty.resolveWith((states) {
    if (states.contains(MaterialState.disabled)) {
      return {color-bg-disabled};
    }
    if (states.contains(MaterialState.selected)) {
      return {color-primary};
    }
    return {color-bg-tertiary};
  }),
  // M3 新增:开启时显示对勾,关闭时显示叉号
  thumbIcon: MaterialStateProperty.resolveWith((states) {
    if (states.contains(MaterialState.selected)) {
      return const Icon(Icons.check, size: 16);
    }
    return const Icon(Icons.close, size: 16);
  }),
  overlayColor: MaterialStateProperty.all({color-primary}),
)
```

> 注:示例中的 `{color-primary}`、`{spacing-md}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Switch: https://api.flutter.dev/flutter/material/Switch-class.html
- API 参考 - SwitchListTile: https://api.flutter.dev/flutter/material/SwitchListTile-class.html
- API 参考 - CupertinoSwitch: https://api.flutter.dev/flutter/cupertino/CupertinoSwitch-class.html
