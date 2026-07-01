# Flutter Text 属性列表与默认值

本文档列出 `Text` Widget 的完整属性、默认值与回调说明。涉及字号/颜色/间距的默认值以 design token 形式给出,不在文档中硬编码。

## Text 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `data` | `String` | 必填(默认构造) | 文本内容 |
| `textSpan` | `InlineSpan` | 必填(`Text.rich`) | 富文本 span 树 |
| `style` | `TextStyle?` | `null`(继承 `DefaultTextStyle`) | 文本样式 |
| `strutStyle` | `StrutStyle?` | `null` | 基线/行高强制约束 |
| `textAlign` | `TextAlign?` | `null`(按 `textDirection` 默认 start) | 水平对齐 |
| `textDirection` | `TextDirection?` | `null`(由 `Directionality` 提供) | 文字方向(ltr/rtl) |
| `locale` | `Locale?` | `null`(由 `Localizations` 提供) | 区域设置 |
| `softWrap` | `bool?` | `true` | 是否允许换行 |
| `overflow` | `TextOverflow?` | `TextOverflow.clip` | 溢出处理 |
| `textScaler` | `TextScaler?` | `TextScaler.noScaling` | 无障碍缩放 |
| `maxLines` | `int?` | `null`(不限) | 最大行数 |
| `semanticsLabel` | `String?` | `null` | 无障碍语义标签 |
| `textWidthBasis` | `TextWidthBasis?` | `TextWidthBasis.parent` | 宽度计算基准 |
| `textHeightBehavior` | `TextHeightBehavior?` | `null`(取 `MediaQuery`) | 行高应用策略 |
| `selectionColor` | `Color?` | `null`(取主题) | 选中态背景色 |

## TextStyle 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `inherit` | `bool` | `true` | 是否继承父样式 |
| `color` | `Color?` | `{color-on-surface}` | 文本颜色 |
| `backgroundColor` | `Color?` | `null` | 背景色 |
| `fontSize` | `double?` | `{font-size-md}`(body) | 字号(逻辑像素) |
| `fontWeight` | `FontWeight?` | `FontWeight.w400` | 字重 |
| `fontStyle` | `FontStyle?` | `FontStyle.normal` | 正常/斜体 |
| `letterSpacing` | `double?` | `null`(自然) | 字间距(逻辑像素) |
| `wordSpacing` | `double?` | `null`(自然) | 词间距 |
| `textBaseline` | `TextBaseline?` | `null` | 基线(alphabetic/ideographic) |
| `height` | `double?` | `null`(自然行高) | 行高倍数 |
| `leadingDistribution` | `TextLeadingDistribution?` | `TextLeadingDistribution.proportional` | 行距分配 |
| `locale` | `Locale?` | `null` | 区域 |
| `foreground` | `Paint?` | `null` | 前景画笔(优先于 `color`) |
| `background` | `Paint?` | `null` | 背景画笔(优先于 `backgroundColor`) |
| `shadows` | `List<Shadow>?` | `null` | 阴影列表 |
| `fontFeatures` | `List<FontFeature>?` | `null` | OpenType 特性(如等宽数字) |
| `fontVariations` | `List<FontVariation>?` | `null` | 可变字体轴 |
| `decoration` | `TextDecoration?` | `TextDecoration.none` | 装饰线(下划线/删除线) |
| `decorationColor` | `Color?` | `null`(取 `color`) | 装饰线颜色 |
| `decorationStyle` | `TextDecorationStyle?` | `TextDecorationStyle.solid` | 装饰线样式 |
| `decorationThickness` | `double?` | `1.0` | 装饰线粗细倍数 |
| `debugLabel` | `String?` | `null` | 调试标签 |
| `fontFamily` | `String?` | `null`(主题字体) | 字体族 |
| `fontFamilyFallback` | `List<String>?` | `null` | 字体回退列表 |
| `package` | `String?` | `null` | 自定义字体包名 |
| `overflow` | `TextOverflow?` | `null` | 样式级溢出处理 |

## TextOverflow 枚举

| 值 | 说明 |
| --- | --- |
| `clip` | 直接裁剪溢出部分(默认) |
| `ellipsis` | 末尾显示省略号 `…` |
| `fade` | 渐隐 |
| `visible` | 不裁剪,允许溢出边界 |

## TextAlign 枚举

| 值 | 说明 |
| --- | --- |
| `left` / `right` | 左/右对齐(与方向无关) |
| `center` | 居中 |
| `justify` | 两端对齐(末行除外) |
| `start` / `end` | 起始/结束对齐(受 `textDirection` 影响,推荐) |

## 事件回调

`Text` 本身不直接暴露手势回调,需通过 `GestureDetector` 或 `SelectableText`(第三方)组合实现。常见组合:

| 组合方式 | 回调 | 说明 |
| --- | --- | --- |
| `GestureDetector(onTap: ...)` | `VoidCallback` | 点击整段文本 |
| `GestureDetector(onLongPress: ...)` | `VoidCallback` | 长按整段文本 |
| `TextSpan` + `TapGestureRecognizer` | `VoidCallback` | 点击某个 span(富文本超链接) |

> Flutter 官方未提供 `SelectableText`(部分平台需 `SelectionArea` 包裹才能选中文本)。从 Flutter 3.3 起可用 `SelectionArea` 包裹启用全树文本选择。

## 完整示例

```dart
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

/// Text 完整示例:涵盖样式、对齐、溢出、富文本、点击回调
class TextFullSample extends StatelessWidget {
  const TextFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Text 完整示例')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. 主题样式(从 textTheme 取,颜色用 token)
            Text(
              '标题(titleLarge)',
              style: theme.textTheme.titleLarge?.copyWith(
                color: {color-on-surface},
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: {spacing-sm}),

            // 2. 多行 + 两端对齐
            const Text(
              '这是一段较长的正文文本,用于演示 maxLines 与 TextOverflow.ellipsis 的行为。'
              '当文本超过指定行数时,将以省略号收尾。',
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.justify,
              style: TextStyle(height: 1.5),
            ),
            const SizedBox(height: {spacing-sm}),

            // 3. 富文本 + 行内点击(协议条款)
            Text.rich(
              TextSpan(
                style: TextStyle(
                  fontSize: {font-size-md},
                  color: {color-on-surface},
                ),
                children: [
                  const TextSpan(text: '阅读并同意 '),
                  TextSpan(
                    text: '《用户协议》',
                    style: TextStyle(
                      color: {color-primary},
                      decoration: TextDecoration.underline,
                      decorationColor: {color-primary},
                    ),
                    recognizer: TapGestureRecognizer()
                      ..onTap = () => debugPrint('点击 用户协议'),
                  ),
                  const TextSpan(text: ' 与 '),
                  TextSpan(
                    text: '《隐私政策》',
                    style: TextStyle(
                      color: {color-primary},
                      decoration: TextDecoration.underline,
                    ),
                    recognizer: TapGestureRecognizer()
                      ..onTap = () => debugPrint('点击 隐私政策'),
                  ),
                ],
              ),
            ),
            const SizedBox(height: {spacing-sm}),

            // 4. 整段点击(GestureDetector 组合)
            GestureDetector(
              onTap: () => debugPrint('点击整段文本'),
              onLongPress: () => debugPrint('长按整段文本'),
              child: const Text(
                '点击或长按我(整段响应)',
                style: TextStyle(decoration: TextDecoration.underline),
              ),
            ),
            const SizedBox(height: {spacing-sm}),

            // 5. SelectionArea 包裹(启用文本选择)
            const SelectionArea(
              child: Text(
                '这段文本可被长按选中并复制到剪贴板。',
                style: TextStyle(fontSize: {font-size-md}),
              ),
            ),
            const SizedBox(height: {spacing-sm}),

            // 6. 字间距 / 字重 / 行高组合
            Text(
              'Styled Text',
              style: TextStyle(
                fontSize: {font-size-lg},
                fontWeight: FontWeight.bold,
                letterSpacing: 2.0,
                height: 1.4,
                color: {color-primary},
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

在 `ThemeData.textTheme` 与 `ColorScheme` 中集中定义所有排版 token:

```dart
ThemeData(
  textTheme: const TextTheme(
    titleLarge: TextStyle(
      fontSize: {font-size-title-lg},
      fontWeight: FontWeight.w600,
      color: {color-on-surface},
    ),
    bodyMedium: TextStyle(
      fontSize: {font-size-body-md},
      height: 1.5,
    ),
  ),
  colorScheme: ColorScheme(
    // ...token 解析
  ),
)
```
