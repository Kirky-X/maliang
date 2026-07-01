# Flutter Divider 属性列表与默认值

本文档汇总 Material Design 3 分隔线(`Divider` / `VerticalDivider`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## Divider 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `height` | `double?` | `16.0` | 占位总高度(含上下空白) |
| `thickness` | `double?` | `0.0`(实际绘制 1.0) | 线厚度 |
| `indent` | `double?` | `0.0` | 左侧缩进 |
| `endIndent` | `double?` | `0.0` | 右侧缩进 |
| `color` | `Color?` | `ThemeData.dividerColor`(`{color-outline-variant}`) | 颜色 |

> `height` 与 `thickness` 关系:`height` 是分隔线在父布局中占用的总高度(含上下空白),`thickness` 是实际绘制的线厚度。当 `thickness` 为 0 时,实际绘制 1.0 逻辑像素。

## VerticalDivider 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `width` | `double?` | `36.0` | 占位总宽度(含左右空白) |
| `thickness` | `double?` | `0.0`(实际绘制 1.0) | 线厚度 |
| `indent` | `double?` | `0.0` | 顶部缩进 |
| `endIndent` | `double?` | `0.0` | 底部缩进 |
| `color` | `Color?` | `ThemeData.dividerColor`(`{color-outline-variant}`) | 颜色 |

## DividerThemeData 属性

通过 `ThemeData.dividerTheme` 注入主题级样式。

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `color` | `Color?` | `{color-outline-variant}` | 颜色 |
| `thickness` | `double?` | `1.0` | 厚度 |
| `space` | `double?` | `16.0` | 占位空间(Divider 为高度,VerticalDivider 为宽度) |
| `indent` | `double?` | `0.0` | 缩进 |
| `endIndent` | `double?` | `0.0` | 末端缩进 |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Divider 完整示例:展示水平/垂直/带文字分隔线与主题配置
class DividerFullSample extends StatelessWidget {
  const DividerFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Divider 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 默认水平分隔线
          const ListTile(title: Text('默认分隔线之上')),
          const Divider(),
          const ListTile(title: Text('默认分隔线之下')),
          SizedBox(height: {spacing-md}),

          // 2. 自定义缩进与厚度
          const ListTile(title: Text('自定义缩进分隔线之上')),
          Divider(
            height: {spacing-md},
            thickness: 2,
            indent: {spacing-md},
            endIndent: {spacing-md},
            color: {color-outline-variant},
          ),
          const ListTile(title: Text('自定义缩进分隔线之下')),
          SizedBox(height: {spacing-md}),

          // 3. 垂直分隔线(配合 Row)
          const Text('垂直分隔线:'),
          SizedBox(height: {spacing-sm}),
          SizedBox(
            height: {size-lg},
            child: Row(
              children: [
                const Expanded(child: Center(child: Text('左'))),
                VerticalDivider(
                  width: {spacing-md},
                  thickness: 1,
                  indent: {spacing-sm},
                  endIndent: {spacing-sm},
                  color: {color-outline-variant},
                ),
                const Expanded(child: Center(child: Text('中'))),
                VerticalDivider(
                  width: {spacing-md},
                  thickness: 1,
                  indent: {spacing-sm},
                  endIndent: {spacing-sm},
                  color: {color-outline-variant},
                ),
                const Expanded(child: Center(child: Text('右'))),
              ],
            ),
          ),
          SizedBox(height: {spacing-lg}),

          // 4. 带文字的分隔线(自定义实现)
          const Text('带文字分隔线:'),
          SizedBox(height: {spacing-sm}),
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
          ),
        ],
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

```dart
ThemeData(
  dividerTheme: DividerThemeData(
    color: {color-outline-variant},
    thickness: 1,
    space: {spacing-md},
    indent: 0,
    endIndent: 0,
  ),
  dividerColor: {color-outline-variant},
)
```

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 默认分隔线颜色 | `{color-outline-variant}` |
| 强调分隔线颜色 | `{color-outline}` |
| 默认厚度 | 1 |
| 强调厚度 | 2 |
| 默认占位空间 | `{spacing-md}`(16) |
| 列表项分隔线缩进 | `{spacing-md}`(16) |
| 带文字分隔线文字 | `{font-size-sm}` / `{color-text-tertiary}` |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Divider: https://api.flutter.dev/flutter/material/Divider-class.html
- API 参考 - VerticalDivider: https://api.flutter.dev/flutter/material/VerticalDivider-class.html
- API 参考 - DividerThemeData: https://api.flutter.dev/flutter/material/DividerThemeData-class.html
