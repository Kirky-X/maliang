# Flutter Tag 属性列表与默认值

本文档汇总 Material Design 3 标签/Chip 系列(`Chip` / `ActionChip` / `ChoiceChip` / `FilterChip` / `InputChip`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## Chip 基类属性

所有 Chip 变体共享以下属性(继承自 `Chip`)。

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `avatar` | `Widget?` | `null` | 头像(左侧) |
| `label` | `Widget` | 必填 | 标签文字 |
| `labelStyle` | `TextStyle?` | `{font-size-sm}` / `{color-on-surface}` | 标签文字样式 |
| `labelPadding` | `EdgeInsetsGeometry?` | `EdgeInsets.symmetric(horizontal: 4)` | 标签内边距 |
| `deleteIcon` | `Widget?` | `Icon(Icons.cancel)` | 删除图标 |
| `onDeleted` | `VoidCallback?` | `null` | 删除回调 |
| `deleteIconColor` | `Color?` | `{color-on-surface-variant}` | 删除图标颜色 |
| `deleteButtonTooltipMessage` | `String?` | `'Delete'` | 删除按钮 tooltip |
| `onPressed` | `VoidCallback?` | `null` | 点击回调 |
| `pressElevation` | `double?` | `{elevation-sm}` | 按下时高度 |
| `color` | `MaterialStateProperty<Color?>?` | `null` | 背景色(状态驱动,M3 推荐) |
| `backgroundColor` | `Color?` | `{color-surface-variant}`(已废弃,用 color) | 背景色 |
| `shadowColor` | `Color?` | `{color-shadow}` | 阴影色 |
| `surfaceTintColor` | `Color?` | `{color-surface-variant}` | M3 表面染色 |
| `elevation` | `double?` | `0` | 高度 |
| `padding` | `EdgeInsetsGeometry?` | `EdgeInsets.all(4)` | 内边距 |
| `visualDensity` | `VisualDensity?` | `VisualDensity.standard` | 视觉密度 |
| `shape` | `OutlinedBorder?` | `StadiumBorder`(全圆角) | 形状 |
| `side` | `BorderSide?` | `null` | 边框 |
| `borderRadius` | `BorderRadius?` | `null` | 圆角(优先级低于 shape) |
| `clipBehavior` | `Clip` | `Clip.none` | 裁剪行为 |
| `materialTapTargetSize` | `MaterialTapTargetSize?` | `padded` | 点击区域 |
| `avatarBoxConstraints` | `BoxConstraints?` | `null` | 头像约束 |

## ChoiceChip 特有属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `selected` | `bool` | `false` | 是否选中 |
| `onSelected` | `ValueChanged<bool>?` | `null` | 选择回调 |
| `selectedColor` | `Color?` | `{color-secondary-container}` | 选中态背景色 |
| `disabledColor` | `Color?` | `{color-surface-variant}` | 禁用态背景色 |

## FilterChip 特有属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `selected` | `bool` | `false` | 是否选中 |
| `onSelected` | `ValueChanged<bool>?` | `null` | 选择回调 |
| `selectedColor` | `Color?` | `{color-secondary-container}` | 选中态背景色 |
| `checkmarkColor` | `Color?` | `{color-on-secondary-container}` | 对勾颜色 |
| `showCheckmark` | `bool` | `true` | 是否显示对勾 |

## InputChip 特有属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `selected` | `bool` | `false` | 是否选中 |
| `onSelected` | `ValueChanged<bool>?` | `null` | 选择回调 |
| `onDeleted` | `VoidCallback?` | `null` | 删除回调 |
| `onPressed` | `VoidCallback?` | `null` | 点击回调 |
| `selectedColor` | `Color?` | `{color-secondary-container}` | 选中态背景色 |
| `disabledColor` | `Color?` | `{color-surface-variant}` | 禁用态背景色 |

## ActionChip 特有属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `onPressed` | `VoidCallback` | 必填 | 点击回调 |
| `pressElevation` | `double?` | `{elevation-sm}` | 按下时高度 |

> ActionChip 不支持 `onDeleted` / `onSelected` / `selected`。

## MaterialState 状态映射

通过 `color` 属性的 `MaterialStateProperty` 可按状态设置背景色:

| 状态 | 触发场景 | 默认背景色 |
| --- | --- | --- |
| `MaterialState.disabled` | `onPressed == null`(ActionChip) | `{color-surface-variant}` |
| `MaterialState.selected` | `selected == true` | `{color-secondary-container}` |
| `MaterialState.pressed` | 按压中 | 叠加 `{color-on-surface}` 12% |
| `MaterialState.hovered` | 鼠标悬停 | 叠加 `{color-on-surface}` 8% |
| `MaterialState.focused` | 焦点获取 | 叠加 `{color-on-surface}` 12% |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Tag 完整示例:展示自定义样式与状态回调
class TagFullSample extends StatefulWidget {
  const TagFullSample({super.key});

  @override
  State<TagFullSample> createState() => _TagFullSampleState();
}

class _TagFullSampleState extends State<TagFullSample> {
  int? _choiceIndex;
  final Set<String> _filters = {};
  final List<String> _inputs = ['Apple', 'Banana'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tag 完整示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. 自定义样式 Chip
            Chip(
              avatar: Icon(Icons.star, size: {icon-size-sm}, color: {color-primary}),
              label: Text(
                '推荐',
                style: TextStyle(
                  fontSize: {font-size-sm},
                  color: {color-on-secondary-container},
                ),
              ),
              color: MaterialStatePropertyAll({color-secondary-container}),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular({radius-full}),
              ),
              padding: EdgeInsets.symmetric(
                horizontal: {spacing-sm},
                vertical: {spacing-xs},
              ),
            ),
            SizedBox(height: {spacing-md}),
            // 2. ChoiceChip 单选组
            const Text('单选:'),
            Wrap(
              spacing: {spacing-xs},
              children: List.generate(3, (i) {
                return ChoiceChip(
                  label: Text('选项 $i'),
                  selected: _choiceIndex == i,
                  selectedColor: {color-primary-container},
                  labelStyle: TextStyle(
                    color: _choiceIndex == i
                        ? {color-on-primary-container}
                        : {color-text-primary},
                  ),
                  onSelected: (s) => setState(() => _choiceIndex = s ? i : null),
                );
              }),
            ),
            SizedBox(height: {spacing-md}),
            // 3. FilterChip 多选组
            const Text('多选:'),
            Wrap(
              spacing: {spacing-xs},
              children: ['A', 'B', 'C'].map((label) {
                return FilterChip(
                  label: Text(label),
                  selected: _filters.contains(label),
                  onSelected: (s) => setState(() {
                    if (s) _filters.add(label);
                    else _filters.remove(label);
                  }),
                );
              }).toList(),
            ),
            SizedBox(height: {spacing-md}),
            // 4. InputChip 可删除
            const Text('已添加:'),
            Wrap(
              spacing: {spacing-xs},
              children: _inputs.map((name) {
                return InputChip(
                  avatar: CircleAvatar(
                    backgroundColor: {color-primary-container},
                    child: Text(name[0], style: TextStyle(color: {color-on-primary-container})),
                  ),
                  label: Text(name),
                  onDeleted: () => setState(() => _inputs.remove(name)),
                  deleteIconColor: {color-on-surface-variant},
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

```dart
ThemeData(
  chipTheme: ChipThemeData(
    backgroundColor: {color-surface-variant},
    selectedColor: {color-secondary-container},
    disabledColor: {color-surface-variant},
    labelStyle: TextStyle(
      fontSize: {font-size-sm},
      color: {color-on-surface},
    ),
    secondaryLabelStyle: TextStyle(
      fontSize: {font-size-sm},
      color: {color-on-secondary-container},
    ),
    padding: EdgeInsets.symmetric(horizontal: {spacing-sm}, vertical: {spacing-xs}),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-full}),
    ),
    side: BorderSide(color: {color-outline-variant}),
  ),
)
```

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Chip: https://api.flutter.dev/flutter/material/Chip-class.html
- API 参考 - ChoiceChip: https://api.flutter.dev/flutter/material/ChoiceChip-class.html
- API 参考 - FilterChip: https://api.flutter.dev/flutter/material/FilterChip-class.html
- API 参考 - InputChip: https://api.flutter.dev/flutter/material/InputChip-class.html
- API 参考 - ActionChip: https://api.flutter.dev/flutter/material/ActionChip-class.html
- API 参考 - ChipThemeData: https://api.flutter.dev/flutter/material/ChipThemeData-class.html
