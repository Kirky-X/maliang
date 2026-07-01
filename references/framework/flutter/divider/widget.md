# Flutter Divider Widget 定义

## Widget 定义

Flutter Material Design 3 提供水平分隔线 `Divider` 与垂直分隔线 `VerticalDivider`,用于在列表、卡片、表单等场景中视觉分隔内容区块。

| Divider 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| Divider | `Divider` | `StatelessWidget` | 水平分隔线(横向布局中) |
| VerticalDivider | `VerticalDivider` | `StatelessWidget` | 垂直分隔线(纵向布局中) |

> 两者内部均通过 `Container` + `BoxDecoration` 或 `CustomPaint` 绘制。M3 默认色为 `dividerColor`(`{color-outline-variant}`),默认厚度 1,左右内边距 16。

## 构造函数

### Divider

```dart
const Divider({
  super.key,
  this.height,                // 占位总高度(含上下空白,默认 16)
  this.thickness,             // 线厚度(默认 0,实际绘制 1)
  this.indent,                // 左侧缩进
  this.endIndent,             // 右侧缩进
  this.color,                 // 颜色
})
```

### VerticalDivider

```dart
const VerticalDivider({
  super.key,
  this.width,                 // 占位总宽度(默认 36)
  this.thickness,             // 线厚度(默认 0,实际绘制 1)
  this.indent,                // 顶部缩进
  this.endIndent,             // 底部缩进
  this.color,                 // 颜色
})
```

## 核心属性

### Divider 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `height` | `double?` | 占位总高度(含上下空白) |
| `thickness` | `double?` | 线厚度 |
| `indent` | `double?` | 左侧缩进 |
| `endIndent` | `double?` | 右侧缩进 |
| `color` | `Color?` | 颜色 |

### VerticalDivider 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `width` | `double?` | 占位总宽度(含左右空白) |
| `thickness` | `double?` | 线厚度 |
| `indent` | `double?` | 顶部缩进 |
| `endIndent` | `double?` | 底部缩进 |
| `color` | `Color?` | 颜色 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Divider 最小示例:展示水平与垂直分隔线
class DividerSample extends StatelessWidget {
  const DividerSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Divider 示例')),
      body: Column(
        children: [
          // 1. 默认水平分隔线
          const ListTile(title: Text('项目 1')),
          const Divider(),
          const ListTile(title: Text('项目 2')),
          const Divider(),
          const ListTile(title: Text('项目 3')),
          SizedBox(height: {spacing-md}),
          // 2. 自定义缩进与厚度的水平分隔线
          const Divider(
            indent: 16,
            endIndent: 16,
            thickness: 2,
          ),
          SizedBox(height: {spacing-md}),
          // 3. 垂直分隔线(配合 Row)
          Row(
            children: [
              const Expanded(child: Text('左')),
              const VerticalDivider(),
              const Expanded(child: Text('中')),
              const VerticalDivider(),
              const Expanded(child: Text('右')),
            ],
          ),
        ],
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
// 自定义颜色与缩进的水平分隔线
Divider(
  height: {spacing-md},
  thickness: 1,
  indent: {spacing-md},
  endIndent: {spacing-md},
  color: {color-outline-variant},
)

// 自定义垂直分隔线
VerticalDivider(
  width: {spacing-md},
  thickness: 1,
  indent: {spacing-sm},
  endIndent: {spacing-sm},
  color: {color-outline-variant},
)

// 带文字的分隔线(非原生,自定义实现)
Row(
  children: [
    Expanded(
      child: Divider(
        endIndent: {spacing-sm},
        color: {color-outline-variant},
      ),
    ),
    Padding(
      padding: EdgeInsets.symmetric(horizontal: {spacing-sm}),
      child: Text(
        'OR',
        style: TextStyle(
          fontSize: {font-size-sm},
          color: {color-text-tertiary},
        ),
      ),
    ),
    Expanded(
      child: Divider(
        indent: {spacing-sm},
        color: {color-outline-variant},
      ),
    ),
  ],
)
```

> 注:示例中的 `{color-outline-variant}`、`{spacing-sm}`、`{spacing-md}`、`{font-size-sm}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Divider: https://api.flutter.dev/flutter/material/Divider-class.html
- API 参考 - VerticalDivider: https://api.flutter.dev/flutter/material/VerticalDivider-class.html
- API 参考 - DividerThemeData: https://api.flutter.dev/flutter/material/DividerThemeData-class.html
