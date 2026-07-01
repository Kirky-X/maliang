# Flutter Card Widget 定义

## Widget 定义

Flutter Material Design 3 提供 `Card`(StatelessWidget)实现卡片容器,常用于承载相关联的信息组(如文章列表项、商品卡片)。`Card` 本身不可点击,需通过 `InkWell` 或 `GestureDetector` 包裹实现交互。M3 版本支持 `Card.filled` / `Card.outlined` 变体。

| Card 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 标准卡片 | `Card` | `StatelessWidget` | 阴影投影卡片(M3 默认 elevation 1) |
| 填充卡片 | `Card.filled` | `StatelessWidget` | 背景填充(无阴影,无边框) |
| 描边卡片 | `Card.outlined` | `StatelessWidget` | 边框卡片(无阴影) |
| 可点击卡片 | `InkWell` + `Card` | - | 通过 InkWell 包裹实现点击 |
| 列表项卡片 | `Card` + `ListTile` | - | 卡片内含 ListTile |

> `Card` 是装饰容器,内部内容自由组合;M3 推荐 `Card` + `Column` + `ListTile` 的结构。

## 构造函数

### Card

```dart
const Card({
  Key? key,
  Color? color,
  Color? shadowColor,
  Color? surfaceTintColor,
  double? elevation,
  ShapeBorder? shape,
  bool borderOnForeground = true,
  EdgeInsetsGeometry? margin,
  Clip? clipBehavior,
  Widget? child,
  bool semanticContainer = true,
})
```

### Card.filled / Card.outlined(M3 变体)

```dart
const Card.filled({
  Key? key,
  Widget? child,
  Color? color,
  Color? shadowColor,
  double? elevation,  // 固定为 0
  ShapeBorder? shape,
  bool borderOnForeground = true,
  EdgeInsetsGeometry? margin,
  Clip? clipBehavior,
  bool semanticContainer = true,
})

const Card.outlined({
  Key? key,
  Widget? child,
  Color? color,
  Color? shadowColor,
  Color? surfaceTintColor,
  double? elevation,  // 固定为 0
  ShapeBorder? shape,
  bool borderOnForeground = true,
  EdgeInsetsGeometry? margin,
  Clip? clipBehavior,
  bool semanticContainer = true,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `child` | `Widget?` | 卡片内容 |
| `color` | `Color?` | 背景色 |
| `shadowColor` | `Color?` | 阴影色 |
| `surfaceTintColor` | `Color?` | 表面染色(M3 elevation tint) |
| `elevation` | `double?` | 阴影高度(M3 默认 1.0) |
| `shape` | `ShapeBorder?` | 形状(M3 默认 12dp 圆角矩形) |
| `borderOnForeground` | `bool` | 边框是否在前台(默认 `true`) |
| `margin` | `EdgeInsetsGeometry?` | 外边距 |
| `clipBehavior` | `Clip?` | 裁剪行为(默认 `Clip.none`) |
| `semanticContainer` | `bool` | 是否为语义容器(默认 `true`) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Card 最小示例:三种变体 + 可点击卡片
class CardSample extends StatelessWidget {
  const CardSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Card 示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 标准卡片(elevation)
          Card(
            child: Padding(
              padding: const EdgeInsets.all({spacing-md}),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('标准卡片', style: TextStyle(fontSize: {font-size-lg})),
                  const SizedBox(height: {spacing-sm}),
                  Text('带阴影的卡片', style: TextStyle(color: {color-text-secondary})),
                ],
              ),
            ),
          ),
          // 2. 填充卡片(无阴影)
          Card.filled(
            child: Padding(
              padding: const EdgeInsets.all({spacing-md}),
              child: const Text('填充卡片(背景色填充)'),
            ),
          ),
          // 3. 描边卡片(边框)
          Card.outlined(
            child: Padding(
              padding: const EdgeInsets.all({spacing-md}),
              child: const Text('描边卡片(边框)'),
            ),
          ),
          // 4. 可点击卡片(InkWell 包裹)
          Card(
            clipBehavior: Clip.antiAlias,
            child: InkWell(
              onTap: () => debugPrint('点击卡片'),
              child: Padding(
                padding: const EdgeInsets.all({spacing-md}),
                child: const Text('点击我'),
              ),
            ),
          ),
          // 5. 列表项卡片
          Card(
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.person),
                  title: const Text('张三'),
                  subtitle: const Text('设计师'),
                ),
                ListTile(
                  leading: const Icon(Icons.person),
                  title: const Text('李四'),
                  subtitle: const Text('工程师'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
Card(
  color: {color-surface},
  shadowColor: {color-shadow},
  surfaceTintColor: {color-primary},
  elevation: {elevation-md},
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular({radius-lg}),
    side: BorderSide(color: {color-border-default}, width: 1),
  ),
  margin: const EdgeInsets.all({spacing-md}),
  clipBehavior: Clip.antiAlias,
  child: InkWell(
    onTap: () {},
    child: Padding(
      padding: const EdgeInsets.all({spacing-md}),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 图片头部
          ClipRRect(
            borderRadius: BorderRadius.circular({radius-md}),
            child: Image.network(
              'https://example.com/image.jpg',
              height: {size-lg},
              width: double.infinity,
              fit: BoxFit.cover,
            ),
          ),
          const SizedBox(height: {spacing-sm}),
          Text(
            '卡片标题',
            style: TextStyle(fontSize: {font-size-md}, fontWeight: FontWeight.w600),
          ),
          Text(
            '卡片描述内容',
            style: TextStyle(color: {color-text-secondary}, fontSize: {font-size-sm}),
          ),
        ],
      ),
    ),
  ),
)
```

> 注:示例中的 `{color-surface}`、`{spacing-md}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Card: https://api.flutter.dev/flutter/material/Card-class.html
- API 参考 - InkWell: https://api.flutter.dev/flutter/material/InkWell-class.html
