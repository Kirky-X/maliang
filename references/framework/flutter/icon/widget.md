# Flutter Icon Widget 定义

## Widget 定义

Flutter 图标体系:`Icon`(基于 `IconData` 的字形图标,Material Icons 字体)、`IconButton`(可点击图标按钮)、`ImageIcon`(基于 `ImageProvider` 的位图图标)、`FontIcon`(自定义字体图标)。Material Icons 内置 1000+ 图标(在 `Icons` 类中)。

| Widget | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `Icon` | `Icon` | `StatelessWidget` | 字形图标(Material/Cupertino) |
| `IconButton` | `IconButton` | `StatelessWidget` | 可点击图标按钮 |
| `ImageIcon` | `ImageIcon` | `StatelessWidget` | 位图图标(基于 ImageProvider) |
| `IconData` | `IconData` | - | 图标数据(codePoint + fontFamily) |
| `Icons` | `Icons` | - | Material 图标常量集合 |
| `CupertinoIcons` | `CupertinoIcons` | - | Cupertino 图标常量集合 |

## 构造函数

### Icon

```dart
const Icon(
  super.key,
  IconData? icon,                  // 图标数据(可为 null)
  double? size,                    // 尺寸(默认 24)
  double? fill,                    // 填充(0.0~1.0,部分图标支持)
  double? weight,                  // 字重
  double? grade,                   // 等级
  double? opticalSize,             // 光学尺寸
  Color? color,                    // 颜色
  List<Shadow>? shadows,           // 阴影
  String? semanticLabel,           // 无障碍标签
  TextDirection? textDirection,    // 文本方向(部分图标有方向)
  bool? applyTextScaling,          // 是否跟随文本缩放
  BlendMode? blendMode,            // 混合模式
})
```

### IconButton

```dart
const IconButton({
  super.key,
  double? iconSize = 24.0,
  VisualDensity? visualDensity,
  EdgeInsetsGeometry padding = const EdgeInsets.all(8),
  AlignmentGeometry alignment = Alignment.center,
  double? splashRadius,
  Color? color,
  Color? focusColor,
  Color? hoverColor,
  Color? highlightColor,
  Color? disabledColor,
  VoidCallback? onPressed,         // null 时禁用
  MouseCursor? mouseCursor,
  FocusNode? focusNode,
  bool autofocus = false,
  String? tooltip,                 // 悬停提示
  bool enableFeedback = true,
  BoxConstraints? constraints,
  Widget? icon,                    // 图标内容
  ...
})

// 带选中态的变体
IconButton.filled({...})           // 填充型
IconButton.tonal({...})            // 次级色调
IconButton.outlined({...})         // 描边型
IconButton.selected({...})         // 选中态切换(M3)
```

### ImageIcon

```dart
const ImageIcon(
  ImageProvider image,             // 图标图片源
  {super.key, double? size, Color? color, String? semanticLabel}
)
```

## 核心属性

### Icon 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `icon` | `IconData?` | 图标数据 |
| `size` | `double?` | 尺寸(默认 24) |
| `color` | `Color?` | 颜色 |
| `fill` | `double?` | 填充(0.0~1.0) |
| `weight` | `double?` | 字重 |
| `grade` | `double?` | 等级 |
| `opticalSize` | `double?` | 光学尺寸 |
| `shadows` | `List<Shadow>?` | 阴影 |
| `semanticLabel` | `String?` | 无障碍标签 |
| `textDirection` | `TextDirection?` | 方向(部分图标如 arrow_back) |

### IconButton 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `icon` | `Widget?` | 图标(通常 Icon) |
| `iconSize` | `double?` | 图标尺寸(默认 24) |
| `onPressed` | `VoidCallback?` | 点击回调(null 禁用) |
| `color` | `Color?` | 图标颜色 |
| `tooltip` | `String?` | 悬停提示 |
| `padding` | `EdgeInsetsGeometry` | 内边距(默认 8) |
| `splashRadius` | `double?` | 水波纹半径 |
| `focusNode` | `FocusNode?` | 焦点节点 |
| `autofocus` | `bool` | 自动获取焦点 |

## 最小示例

```dart
import 'package:flutter/material.dart';

class IconSample extends StatelessWidget {
  const IconSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Icon 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          children: [
            const Icon(Icons.star, size: 48, color: {color-warning}),
            const SizedBox(height: {spacing-sm}),
            const Icon(Icons.favorite, size: 32, color: {color-danger}),
            IconButton(
              icon: const Icon(Icons.settings),
              color: {color-primary},
              tooltip: '设置',
              onPressed: () => debugPrint('点击设置'),
            ),
            const ImageIcon(AssetImage('assets/icons/custom.png'), size: 32),
          ],
        ),
      ),
    );
  }
}
```

## 参考链接

- Flutter 官方文档:无独立教程页(本 widget 在聚合页中介绍)
- Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- Material Icons 搜索: https://fonts.google.com/icons
- API 参考 - Icon: https://api.flutter.dev/flutter/widgets/Icon-class.html
- API 参考 - IconButton: https://api.flutter.dev/flutter/material/IconButton-class.html
- API 参考 - ImageIcon: https://api.flutter.dev/flutter/widgets/ImageIcon-class.html
- API 参考 - Icons: https://api.flutter.dev/flutter/material/Icons-class.html
