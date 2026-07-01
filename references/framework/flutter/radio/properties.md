# Flutter Radio 属性列表与默认值

本文档汇总 `Radio<T>` 与 `RadioListTile<T>` 的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## Radio 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `T` | 必填 | 当前项的值 |
| `groupValue` | `T?` | 必填 | 单选组当前选中值 |
| `onChanged` | `ValueChanged<T?>?` | 必填 | 选择变化回调;为 `null` 时禁用 |
| `toggleable` | `bool` | `false` | 是否允许二次点击取消 |
| `activeColor` | `Color?` | `null`(取主题) | 选中态颜色(已废弃) |
| `fillColor` | `MaterialStateProperty<Color?>?` | `null` | 填充色(支持状态) |
| `hoverColor` | `Color?` | `null` | 悬停色(已废弃,用 overlayColor) |
| `overlayColor` | `MaterialStateProperty<Color?>?` | `null` | 按压/悬停/聚焦叠加色 |
| `splashRadius` | `double?` | `null`(默认 24.0) | 水波纹半径 |
| `mouseCursor` | `MouseCursor?` | `null` | 鼠标光标 |
| `visualDensity` | `VisualDensity?` | `null`(取主题) | 视觉密度 |
| `materialTapTargetSize` | `MaterialTapTargetSize?` | `null`(取主题) | 点击目标尺寸 |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |

## RadioListTile 构造参数(增量)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `title` | `Widget?` | `null` | 标题 |
| `subtitle` | `Widget?` | `null` | 副标题 |
| `isThreeLine` | `bool` | `false` | 是否三行布局(需配合 subtitle) |
| `dense` | `bool?` | `null`(取主题) | 紧凑模式 |
| `secondary` | `Widget?` | `null` | 前置图标/Widget |
| `selected` | `bool` | `false` | 整行是否高亮(选中态) |
| `controlAffinity` | `ListTileControlAffinity` | `ListTileControlAffinity.platform` | 按钮位置(leading/trailing/platform) |
| `enabled` | `bool?` | `null` | 是否可用 |
| `contentPadding` | `EdgeInsetsGeometry?` | `null`(取主题) | 内容内边距 |
| `shape` | `ShapeBorder?` | `null` | 形状 |
| `selectedTileColor` | `Color?` | `null` | 选中态背景色 |
| `onFocusChange` | `ValueChanged<bool>?` | `null` | 焦点变化回调 |
| `enableFeedback` | `bool?` | `null` | 触觉反馈 |

## MaterialState 状态(MD3)

`fillColor` / `overlayColor` 通过 `MaterialStateProperty` 响应状态:

| 状态 | 触发条件 | fillColor MD3 默认 |
| --- | --- | --- |
| `MaterialState.selected` | `value == groupValue` | `{color-primary}` |
| `MaterialState.disabled` | `onChanged == null` | `{color-text-disabled}` |
| `MaterialState.hovered` | 鼠标悬停 | (overlayColor 处理) |
| `MaterialState.focused` | 焦点获取 | (overlayColor 处理) |
| `MaterialState.pressed` | 按压 | (overlayColor 处理) |
| `MaterialState.error` | 表单错误 | `{color-error}` |

## MaterialTapTargetSize 取值

| 取值 | 说明 |
| --- | --- |
| `MaterialTapTargetSize.padded` | 48 × 48(MD3 默认,符合无障碍最小尺寸) |
| `MaterialTapTargetSize.shrinkWrap` | 紧贴视觉边界(忽略无障碍尺寸) |
| `MaterialTapTargetSize.unshrinkable` | 不收缩(≥ 48) |

## ListTileControlAffinity 取值

| 取值 | 按钮位置 |
| --- | --- |
| `ListTileControlAffinity.platform` | 跟随平台(iOS leading,Android trailing) |
| `ListTileControlAffinity.leading` | 前置(标题左侧) |
| `ListTileControlAffinity.trailing` | 后置(标题右侧) |

## VisualDensity 取值

| 取值 | 说明 |
| --- | --- |
| `VisualDensity.standard` | 标准密度(默认) |
| `VisualDensity.compact` | 紧凑 |
| `VisualDensity.comfortable` | 宽松 |
| `VisualDensity(horizontal, vertical)` | 自定义 |

## 事件回调

| 回调 | 签名 | 触发时机 |
| --- | --- | --- |
| `onChanged` | `void Function(T?)` | 点击未选中项时触发;`toggleable: true` 时点击已选中项触发并传 `null` |
| `onFocusChange`(ListTile) | `void Function(bool)` | 焦点获取/失去 |

> `onChanged == null` 时按钮处于禁用态,所有交互均不触发。

## 完整示例

```dart
import 'package:flutter/material.dart';

class RadioFullSample extends StatefulWidget {
  const RadioFullSample({super.key});

  @override
  State<RadioFullSample> createState() => _RadioFullSampleState();
}

enum ThemeMode { system, light, dark }
enum LayoutDensity { compact, comfortable, standard }

class _RadioFullSampleState extends State<RadioFullSample> {
  ThemeMode _theme = ThemeMode.system;
  LayoutDensity _density = LayoutDensity.standard;
  bool _toggleable = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Radio 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 主题模式单选组(使用 RadioListTile)
          Text('主题模式', style: Theme.of(context).textTheme.titleMedium),
          for (final mode in ThemeMode.values)
            RadioListTile<ThemeMode>(
              value: mode,
              groupValue: _theme,
              onChanged: (v) => setState(() => _theme = v!),
              title: Text(_themeLabel(mode)),
              subtitle: Text(_themeDesc(mode)),
              toggleable: _toggleable,
              fillColor: MaterialStateProperty.resolveWith((states) {
                if (states.contains(MaterialState.disabled)) {
                  return {color-text-disabled};
                }
                if (states.contains(MaterialState.selected)) {
                  return {color-primary};
                }
                return {color-border-default};
              }),
              controlAffinity: ListTileControlAffinity.trailing,
            ),
          const Divider(),
          // 2. 布局密度单选组(使用 Radio + Row 自定义布局)
          Text('布局密度', style: Theme.of(context).textTheme.titleMedium),
          Wrap(
            spacing: {spacing-sm},
            children: LayoutDensity.values.map((d) {
              return Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Radio<LayoutDensity>(
                    value: d,
                    groupValue: _density,
                    onChanged: (v) => setState(() => _density = v!),
                    fillColor: MaterialStateProperty.all({color-primary}),
                  ),
                  Text(_densityLabel(d)),
                ],
              );
            }).toList(),
          ),
          const Divider(),
          // 3. toggleable 开关演示
          SwitchListTile(
            value: _toggleable,
            onChanged: (v) => setState(() => _toggleable = v),
            title: const Text('允许二次点击取消选择'),
            subtitle: const Text('开启后点击已选中项会清除选择'),
          ),
          const Divider(),
          // 4. 禁用态
          RadioListTile<ThemeMode>(
            value: ThemeMode.dark,
            groupValue: _theme,
            onChanged: null,
            title: const Text('禁用项'),
            subtitle: const Text('onChanged 为 null 时禁用'),
          ),
        ],
      ),
    );
  }

  String _themeLabel(ThemeMode m) {
    switch (m) {
      case ThemeMode.system: return '跟随系统';
      case ThemeMode.light: return '浅色';
      case ThemeMode.dark: return '深色';
    }
  }

  String _themeDesc(ThemeMode m) => '当前: ${_themeLabel(m)}';
  String _densityLabel(LayoutDensity d) {
    switch (d) {
      case LayoutDensity.compact: return '紧凑';
      case LayoutDensity.comfortable: return '宽松';
      case LayoutDensity.standard: return '标准';
    }
  }
}
```

## 注意事项

- `Radio` 是受控组件,`groupValue` 由父级管理;**不要在 `Radio` 内部维护选中态**,会导致状态不同步。
- `value` 与 `groupValue` 必须类型一致且可比较;若使用自定义类型,需重写 `==` 与 `hashCode`。
- `toggleable: true` 允许取消选择(传入 `null`),但 `groupValue` 类型必须为 `T?`;若为非空类型会导致编译错误。
- `activeColor` 已废弃,优先使用 `fillColor`(支持状态);`fillColor` 未设置时取 `ThemeData.radioTheme.fillColor`。
- 单选按钮的点击区域由 `materialTapTargetSize` 决定,默认 `padded`(48 × 48);若需缩小,使用 `shrinkWrap`,但**会破坏无障碍可达性**(违反 WCAG 2.5.5)。
- M3 推荐用 `RadioListTile` 而非纯 `Radio`,带标签可读性更好且 TalkBack 能播报完整信息。
- 多个单选组必须使用不同的 `groupValue` 状态变量,共享会导致跨组互斥。
