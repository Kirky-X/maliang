# Flutter SegmentedButton 属性列表与默认值

本文档汇总 `SegmentedButton<T>` 与 `ButtonSegment<T>` 的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出。

## SegmentedButton 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `segments` | `Set<ButtonSegment<T>>` | 必填 | 分段定义 |
| `selected` | `Set<T>` | 必填 | 选中值集合(互斥时长度 1) |
| `onSelectionChanged` | `ValueChanged<Set<T>>?` | 必填 | 选中变化回调;`null` 时禁用 |
| `multiSelectionEnabled` | `bool` | `false` | 多选模式 |
| `emptySelectionAllowed` | `bool` | `false` | 是否允许空选 |
| `selectedIcon` | `Widget?` | `check` 图标 | 选中段前缀图标 |
| `unselectedIcon` | `Widget?` | `null` | 未选段占位图标(多选) |
| `style` | `ButtonStyle?` | 取主题 | 覆盖样式 |
| `side` | `BorderSide?` | 取主题 | 外边框 |
| `borderRadius` | `BorderRadiusGeometry?` | 取主题(M3 全圆角) | 圆角 |

## styleFrom 常用覆盖

| 属性 | 建议值 | 说明 |
| --- | --- | --- |
| `selectedBackgroundColor` | `{color-primary}` | 选中段背景 |
| `selectedForegroundColor` | `{color-text-inverse}` | 选中段前景 |
| `backgroundColor` | `{color-bg-secondary}` | 底色 |
| `foregroundColor` | `{color-text-primary}` | 未选前景 |
| `disabledForegroundColor` | `{color-text-disabled}` | 禁用前景 |
| `visualDensity` | `VisualDensity.standard` | 密度(compact 收窄) |

## ButtonSegment 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `T` | 必填 | 段值(组内唯一) |
| `label` | `Widget` | 必填 | 段文本 |
| `icon` | `Widget?` | `null` | 段前置图标 |
| `avatar` | `Widget?` | `null` | 段前置圆形标识 |
| `enabled` | `bool` | `true` | 是否可用 |
| `tooltip` | `String?` | `null` | 悬停提示 |

## 完整示例(多选标签筛选)

```dart
import 'package:flutter/material.dart';

enum FilterTag { free, express, official, newOnly }

class MultiSegmentSample extends StatefulWidget {
  const MultiSegmentSample({super.key});

  @override
  State<MultiSegmentSample> createState() => _MultiSegmentSampleState();
}

class _MultiSegmentSampleState extends State<MultiSegmentSample> {
  Set<FilterTag> _tags = {FilterTag.free};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('筛选')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SegmentedButton<FilterTag>(
              segments: const [
                ButtonSegment(value: FilterTag.free, label: Text('免邮')),
                ButtonSegment(value: FilterTag.express, label: Text('顺丰')),
                ButtonSegment(value: FilterTag.official, label: Text('自营')),
                ButtonSegment(value: FilterTag.newOnly, label: Text('新品')),
              ],
              selected: _tags,
              multiSelectionEnabled: true,
              showSelectedIcon: (_) => false, // 多选时隐藏 check
              onSelectionChanged: (s) => setState(() => _tags = s),
              style: SegmentedButton.styleFrom(
                selectedBackgroundColor: {color-primary},
                selectedForegroundColor: {color-text-inverse},
                backgroundColor: {color-bg-secondary},
              ),
            ),
            const SizedBox(height: {spacing-md}),
            Text('已选:${_tags.length} 项',
                style: Theme.of(context).textTheme.bodySmall),
          ],
        ),
      ),
    );
  }
}
```

## 注意事项

- 项数 2-5 段为宜;超出用 `TabBar`(tabs 类)。
- 互斥模式 `selected` 必须恰含 1 个值;`emptySelectionAllowed: false` 时清空会断言。
- 多选模式建议 `showSelectedIcon: (_) => false` 隐藏 check,避免图标喧宾夺主。
- 无障碍:按钮自带 `role="radio"` 语义组;段文字自明,图标段必须补 `tooltip`/语义标签。
- 触控目标:单段高度 M3 默认 40dp,达标;`visualDensity: compact` 时检查是否仍 ≥36dp 视觉且热区充足。
- 语义分工:视图/筛选状态切换用本类;页面级内容切换用 tabs;表单录入用 radio。
