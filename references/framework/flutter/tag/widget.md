# Flutter Tag Widget 定义

## Widget 定义

Flutter Material Design 3 提供"标签/Chip"系列 Widget,涵盖信息标签、可删除标签、选择标签、过滤标签等场景。

| Tag 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| Chip | `Chip` | `StatelessWidget` | 基础信息标签(头像+文字+删除按钮) |
| ActionChip | `ActionChip` | `Chip` | 可点击操作标签 |
| ChoiceChip | `ChoiceChip` | `Chip` | 单选标签(配合 `selected`) |
| FilterChip | `FilterChip` | `Chip` | 多选过滤标签 |
| InputChip | `InputChip` | `Chip` | 用户输入产生的标签(可删除) |

> M3 体系下 `Chip` 为基类,其余变体扩展交互能力。所有 Chip 均为 `StatelessWidget`,通过 `onDeleted` / `onPressed` / `onSelected` 提供交互。

## 构造函数

### Chip(基础)

```dart
const Chip({
  super.key,
  this.avatar,                    // 头像(左侧)
  required this.label,            // 标签文字(通常为 Text)
  this.labelStyle,                // 标签文字样式
  this.labelPadding,              // 标签内边距
  this.deleteIcon,                // 删除图标
  this.onDeleted,                 // 删除回调(为 null 时不显示删除图标)
  this.deleteIconColor,           // 删除图标颜色
  this.deleteButtonTooltipMessage,// 删除按钮 tooltip
  this.onPressed,                 // 点击回调(为 null 时无水波纹)
  this.pressElevation,            // 按下时高度
  this.color,                     // 背景色(MaterialStateProperty)
  this.backgroundColor,           // 背景色(已被 color 取代)
  this.shadowColor,               // 阴影色
  this.surfaceTintColor,          // M3 表面染色
  this.elevation,                 // 高度
  this.padding,                   // 内边距
  this.visualDensity,             // 视觉密度
  this.shape,                     // 形状
  this.side,                      // 边框
  this.borderRadius,              // 圆角(优先级低于 shape)
  this.clipBehavior = Clip.none,  // 裁剪行为
  this.materialTapTargetSize,     // 点击区域
  this.avatarBoxConstraints,      // 头像约束
})
```

### ChoiceChip / FilterChip / InputChip / ActionChip

```dart
// ChoiceChip:单选
ChoiceChip({
  required this.label,
  this.selected = false,           // 是否选中
  this.onSelected,                 // 选择回调
  ...其余同 Chip...
})

// FilterChip:多选
FilterChip({
  required this.label,
  this.selected = false,
  this.onSelected,
  this.showCheckmark = true,       // 选中时显示对勾
  ...其余同 Chip...
})

// InputChip:可删除
InputChip({
  required this.label,
  this.onDeleted,
  this.onPressed,
  this.onSelected,
  this.selected = false,
  ...其余同 Chip...
})

// ActionChip:可点击
ActionChip({
  required this.label,
  required this.onPressed,
  ...其余同 Chip...
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `label` | `Widget` | 标签文字 |
| `avatar` | `Widget?` | 头像(左侧,通常为 `CircleAvatar` 或 `Icon`) |
| `onPressed` | `VoidCallback?` | 点击回调(`ActionChip` 必填) |
| `onSelected` | `ValueChanged<bool>??` | 选择回调(`ChoiceChip` / `FilterChip`) |
| `selected` | `bool` | 是否选中(`ChoiceChip` / `FilterChip`) |
| `onDeleted` | `VoidCallback?` | 删除回调(`InputChip`) |
| `deleteIcon` | `Widget?` | 删除图标 |
| `color` | `MaterialStateProperty<Color?>?` | 背景色(状态驱动) |
| `shape` | `OutlinedBorder?` | 形状 |
| `side` | `BorderSide?` | 边框 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Tag 最小示例:展示五种 Chip 变体
class TagSample extends StatefulWidget {
  const TagSample({super.key});

  @override
  State<TagSample> createState() => _TagSampleState();
}

class _TagSampleState extends State<TagSample> {
  int? _choiceIndex;
  final Set<String> _filters = {};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tag 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. Chip(基础标签)
            const Chip(label: Text('基础标签')),
            // 2. ActionChip(操作标签)
            ActionChip(
              avatar: const Icon(Icons.add),
              label: const Text('添加'),
              onPressed: () {},
            ),
            // 3. ChoiceChip(单选)
            Wrap(
              spacing: {spacing-xs},
              children: List.generate(3, (i) {
                return ChoiceChip(
                  label: Text('选项 $i'),
                  selected: _choiceIndex == i,
                  onSelected: (s) => setState(() => _choiceIndex = s ? i : null),
                );
              }),
            ),
            // 4. FilterChip(多选)
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
            // 5. InputChip(可删除)
            Wrap(
              spacing: {spacing-xs},
              children: ['用户1', '用户2'].map((name) {
                return InputChip(
                  avatar: const CircleAvatar(child: Icon(Icons.person)),
                  label: Text(name),
                  onDeleted: () {},
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

## 自定义样式(MD3 主题映射)

```dart
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
    side: BorderSide(color: {color-outline-variant}),
  ),
  padding: EdgeInsets.symmetric(
    horizontal: {spacing-sm},
    vertical: {spacing-xs},
  ),
  materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
)
```

> 注:示例中的 `{color-secondary-container}`、`{color-on-secondary-container}`、`{color-outline-variant}`、`{spacing-sm}`、`{radius-full}`、`{icon-size-sm}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Chip: https://api.flutter.dev/flutter/material/Chip-class.html
- API 参考 - ChoiceChip: https://api.flutter.dev/flutter/material/ChoiceChip-class.html
- API 参考 - FilterChip: https://api.flutter.dev/flutter/material/FilterChip-class.html
- API 参考 - InputChip: https://api.flutter.dev/flutter/material/InputChip-class.html
- API 参考 - ActionChip: https://api.flutter.dev/flutter/material/ActionChip-class.html
