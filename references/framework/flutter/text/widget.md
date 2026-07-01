# Flutter Text Widget 定义

## Widget 定义

`Text` 是 Flutter 中用于显示一段(或多段)文本的基础 Widget,继承自 `StatelessWidget`。它通过 `build()` 方法将字符串渲染为 `RichText`,并依据 `TextStyle`、`TextAlign`、`TextDirection`、`Locale` 等参数决定排版。

Material Design 3 中,`Text` 的字号 / 字重 / 行高 / 颜色应从 `ThemeData.textTheme`(`displayLarge` ~ `labelSmall`)与 `ColorScheme` 获取,即对应 design token。

### 相关类

| 类 | 基类 | 说明 |
| --- | --- | --- |
| `Text` | `StatelessWidget` | 单一样式文本 |
| `Text.rich` | `Text`(`StatelessWidget`) | 多样化样式(内联 `InlineSpan`) |
| `RichText` | `MultiChildRenderObjectWidget` | 底层渲染 Widget,由 `Text` 内部使用 |
| `TextSpan` | `InlineSpan` | 树状样式片段 |
| `TextStyle` | — | 文本样式描述 |

## 构造函数

### Text(默认构造)

```dart
const Text(
  String data, {              // 文本内容
  super.key,
  this.style,                 // TextStyle?
  this.strutStyle,            // StrutStyle?(基线/行高约束)
  this.textAlign,             // TextAlign?
  this.textDirection,         // TextDirection?
  this.locale,                // Locale?
  this.softWrap,              // bool?
  this.overflow,              // TextOverflow?
  this.textScaleFactor,       // double?(已弃用,3.16+ 改用 textScaler)
  this.textScaler,            // TextScaler?
  this.maxLines,              // int?
  this.semanticsLabel,        // String?
  this.textWidthBasis,        // TextWidthBasis?
  this.textHeightBehavior,    // TextHeightBehavior?
  this.selectionColor,        // Color?(选中高亮)
})
```

### Text.rich(内联多样式)

```dart
const Text.rich(
  InlineSpan textSpan, {      // TextSpan,可嵌套子 span
  super.key,
  this.style,
  this.strutStyle,
  this.textAlign,
  this.textDirection,
  this.locale,
  this.softWrap,
  this.overflow,
  this.textScaler,
  this.maxLines,
  this.semanticsLabel,
  this.textWidthBasis,
  this.textHeightBehavior,
  this.selectionColor,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `String` | 文本内容(默认构造) |
| `style` | `TextStyle?` | 字号、颜色、字重、行高、装饰线等 |
| `strutStyle` | `StrutStyle?` | 强制基线/行高约束 |
| `textAlign` | `TextAlign?` | 对齐方式(left/right/center/justify/start/end) |
| `textDirection` | `TextDirection?` | 文字方向(ltr/rtl) |
| `locale` | `Locale?` | 区域,影响字形选择 |
| `softWrap` | `bool?` | 是否允许换行 |
| `overflow` | `TextOverflow?` | 溢出处理(clip/ellipsis/fade/visible) |
| `textScaler` | `TextScaler?` | 文本缩放(无障碍) |
| `maxLines` | `int?` | 最大行数 |
| `textWidthBasis` | `TextWidthBasis?` | 宽度计算基准(parent/longestLine) |
| `textHeightBehavior` | `TextHeightBehavior?` | 行高应用策略 |
| `selectionColor` | `Color?` | 选中态背景色 |
| `semanticsLabel` | `String?` | 语义标签(无障碍朗读) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Text 最小示例:展示单行、多行、溢出、富文本
class TextSample extends StatelessWidget {
  const TextSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Text 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. 最简文本
            const Text('Hello, Flutter'),

            // 2. 应用样式(颜色用 token 引用)
            Text(
              '主题色文本',
              style: TextStyle(
                fontSize: {font-size-md},
                fontWeight: FontWeight.w500,
                color: {color-primary},
              ),
            ),

            // 3. 多行 + 对齐
            const Text(
              '这是一段多行文本\n用于演示 textAlign 与 maxLines 的效果。',
              textAlign: TextAlign.start,
            ),

            // 4. 单行溢出省略号
            const Text(
              '一行很长的文本,超出宽度后将显示省略号',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),

            // 5. 富文本(Text.rich)
            Text.rich(
              TextSpan(
                text: '混合 ',
                style: TextStyle(
                  fontSize: {font-size-md},
                  color: {color-on-surface},
                ),
                children: [
                  TextSpan(
                    text: '加粗',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: {color-primary},
                    ),
                  ),
                  const TextSpan(text: ' 与普通文本。'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 主题样式(Design Token 映射)

通过 `Theme.of(context).textTheme` 取 MD3 排版 token,颜色取 `colorScheme`:

```dart
Text(
  'MD3 标题',
  style: Theme.of(context).textTheme.titleLarge?.copyWith(
        color: {color-primary},   // 覆盖颜色 token
      ),
)
```

| MD3 textTheme 字段 | 对应 token(字号) | 用途 |
| --- | --- | --- |
| `displayLarge` ~ `displaySmall` | `{font-size-display-*}` | 大号展示 |
| `headlineLarge` ~ `headlineSmall` | `{font-size-headline-*}` | 标题 |
| `titleLarge` ~ `titleSmall` | `{font-size-title-*}` | 子标题/卡片标题 |
| `bodyLarge` ~ `bodySmall` | `{font-size-body-*}` | 正文 |
| `labelLarge` ~ `labelSmall` | `{font-size-label-*}` | 按钮/标签 |

详见 `properties.md`。
