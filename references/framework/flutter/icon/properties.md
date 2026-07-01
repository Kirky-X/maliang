# Flutter Icon 属性列表与默认值

本文档汇总 `Icon` / `IconButton` / `ImageIcon` 的属性、默认值与回调。颜色/尺寸默认值以 design token 形式给出。

## Icon 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `icon` | `IconData?` | `null` | 图标数据(codePoint+fontFamily) |
| `size` | `double?` | `24.0`(取 `IconTheme`) | 尺寸 |
| `color` | `Color?` | `null`(取 `IconTheme`) | 颜色 |
| `fill` | `double?` | `0.0` | 填充(0.0~1.0,部分图标支持) |
| `weight` | `double?` | `null` | 字重(100~700,部分图标) |
| `grade` | `double?` | `null` | 等级(-25~200) |
| `opticalSize` | `double?` | `null` | 光学尺寸(20~48) |
| `shadows` | `List<Shadow>?` | `null` | 阴影 |
| `semanticLabel` | `String?` | `null` | 无障碍标签 |
| `textDirection` | `TextDirection?` | `null`(取 `Directionality`) | 方向(方向性图标如 arrow_back) |
| `applyTextScaling` | `bool?` | `null` | 是否跟随文本缩放 |
| `blendMode` | `BlendMode?` | `BlendMode.srcIn` | 颜色混合模式 |

## IconButton 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `icon` | `Widget?` | 必填 | 图标内容(通常 Icon) |
| `iconSize` | `double?` | `24.0` | 图标尺寸 |
| `onPressed` | `VoidCallback?` | 必填 | 点击回调(null 禁用) |
| `color` | `Color?` | `null`(主题) | 图标颜色 |
| `focusColor` | `Color?` | `null` | 焦点态颜色 |
| `hoverColor` | `Color?` | `null` | 悬停态颜色 |
| `highlightColor` | `Color?` | `null` | 按压态颜色 |
| `disabledColor` | `Color?` | `null` | 禁用态颜色 |
| `tooltip` | `String?` | `null` | 悬停提示(长按或鼠标悬停) |
| `padding` | `EdgeInsetsGeometry` | `EdgeInsets.all(8)` | 内边距 |
| `alignment` | `AlignmentGeometry` | `Alignment.center` | 对齐 |
| `splashRadius` | `double?` | `null`(默认 20) | 水波纹半径 |
| `constraints` | `BoxConstraints?` | `null` | 尺寸约束 |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |
| `mouseCursor` | `MouseCursor?` | `null` | 鼠标光标 |
| `enableFeedback` | `bool` | `true` | 触觉/声音反馈 |
| `visualDensity` | `VisualDensity?` | `null` | 视觉密度 |
| `isSelected` | `bool?` | `null`(selected 变体) | 选中态(M3 toggle) |
| `selectedIcon` | `Widget?` | `null` | 选中态图标(selected 变体) |

## IconButton M3 变体

| 变体 | 背景样式 | 用途 |
| --- | --- | --- |
| `IconButton()` | 透明 | 默认(低强调) |
| `IconButton.filled()` | primary 填充 | 高强调 |
| `IconButton.tonal()` | secondaryContainer 填充 | 中强调 |
| `IconButton.outlined()` | 描边 | 中强调 |
| `IconButton.selected()` | 选中态切换 | toggle |

## ImageIcon 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `image` | `ImageProvider` | 必填 | 图标图片源 |
| `size` | `double?` | `24.0` | 尺寸 |
| `color` | `Color?` | `null` | 颜色(混合) |
| `semanticLabel` | `String?` | `null` | 无障碍标签 |

## IconData 属性

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `codePoint` | `int` | 图标码点 |
| `fontFamily` | `String?` | 字体族(Material/Cupertino/自定义) |
| `fontPackage` | `String?` | 包名(外部包字体) |
| `matchTextDirection` | `bool` | 是否匹配文本方向 |

## IconTheme(继承主题)

通过 `IconTheme` 或 `IconThemeData` 设置默认值:

```dart
IconTheme(
  data: const IconThemeData(
    color: {color-text-primary},
    size: 20,
    opacity: 0.8,
  ),
  child: Row(children: const [
    Icon(Icons.star),    // 继承主题:20px,primary 色
    Icon(Icons.favorite),
  ]),
)
```

## 完整示例

```dart
import 'package:flutter/material.dart';

class IconFullSample extends StatelessWidget {
  const IconFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Icon 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 不同尺寸/颜色
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: const [
              Icon(Icons.star, size: 16, color: {color-warning}),
              Icon(Icons.star, size: 24, color: {color-warning}),
              Icon(Icons.star, size: 32, color: {color-warning}),
              Icon(Icons.star, size: 48, color: {color-warning}),
            ],
          ),
          const SizedBox(height: {spacing-md}),
          // 2. 方向性图标
          const Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Icon(Icons.arrow_back),
              Icon(Icons.arrow_forward),
              Icon(Icons.arrow_upward),
              Icon(Icons.arrow_downward),
            ],
          ),
          const SizedBox(height: {spacing-md}),
          // 3. IconButton + tooltip
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              IconButton(
                icon: const Icon(Icons.search),
                tooltip: '搜索',
                onPressed: () {},
              ),
              IconButton.filled(
                icon: const Icon(Icons.add),
                tooltip: '新增',
                onPressed: () {},
              ),
              IconButton.tonal(
                icon: const Icon(Icons.edit),
                tooltip: '编辑',
                onPressed: () {},
              ),
              IconButton.outlined(
                icon: const Icon(Icons.delete),
                tooltip: '删除',
                onPressed: () {},
              ),
              const IconButton(
                icon: Icon(Icons.lock),
                onPressed: null, // 禁用态
              ),
            ],
          ),
          const SizedBox(height: {spacing-md}),
          // 4. toggle IconButton.selected
          ToggleIconSample(),
          const SizedBox(height: {spacing-md}),
          // 5. IconTheme 统一主题
          const IconTheme(
            data: IconThemeData(color: {color-primary}, size: 28),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Icon(Icons.home),
                Icon(Icons.person),
                Icon(Icons.settings),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ToggleIconSample extends StatefulWidget {
  @override
  State<ToggleIconSample> createState() => _ToggleIconSampleState();
}

class _ToggleIconSampleState extends State<ToggleIconSample> {
  bool _selected = false;

  @override
  Widget build(BuildContext context) => IconButton(
        icon: Icon(_selected ? Icons.favorite : Icons.favorite_border),
        color: _selected ? {color-danger} : {color-text-primary},
        onPressed: () => setState(() => _selected = !_selected),
      );
}
```

## 注意事项

- `Icon` 默认从 `IconThemeData` 取 `size`/`color`,显式设置会覆盖
- `IconButton` 的 `onPressed: null` 触发禁用态,显示 `disabledColor`
- Material Icons 字体需在 `pubspec.yaml` 配置(默认已含),自定义字体需 `fontFamily`
- `tooltip` 在桌面/Web 上鼠标悬停显示,在移动端长按显示
- `Icons` 类图标的 `year2023` 后缀(如 `Icons.star_year2023`)为 M3 新版样式
- `IconButton.filled` / `.tonal` / `.outlined` 是 M3 新增,需 `useMaterial3: true`
- 自定义字体图标用 `IconData(0xe800, fontFamily: 'MyFont')`,字体文件放 assets 并在 pubspec 声明
