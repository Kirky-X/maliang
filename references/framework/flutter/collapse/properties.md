# Flutter Collapse 属性列表与默认值

本文档汇总 Material Design 3 折叠面板(`ExpansionTile` / `ExpansionPanelList` / `ExpansionPanel`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## ExpansionTile 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `leading` | `Widget?` | `null` | 头部 Widget |
| `title` | `Widget` | 必填 | 标题 |
| `subtitle` | `Widget?` | `null` | 副标题 |
| `onExpansionChanged` | `ValueChanged<bool>?` | `null` | 展开/折叠回调 |
| `children` | `List<Widget>` | `const []` | 子节点 |
| `initiallyExpanded` | `bool` | `false` | 初始是否展开 |
| `maintainState` | `bool` | `false` | 折叠时是否保持子项状态 |
| `tilePadding` | `EdgeInsetsGeometry` | `EdgeInsets.symmetric(horizontal: 16, vertical: 4)` | 标题内边距 |
| `expandedCrossAxisAlignment` | `CrossAxisAlignment?` | `null` | 展开后子项交叉轴对齐 |
| `expandedAlignment` | `AlignmentGeometry?` | `null` | 展开后子项对齐 |
| `childrenPadding` | `EdgeInsetsGeometry` | `EdgeInsets.symmetric(horizontal: 16)` | 子项区域内边距 |
| `backgroundColor` | `Color?` | `{color-surface-variant}` | 展开时背景色 |
| `collapsedBackgroundColor` | `Color?` | `{color-surface}` | 折叠时背景色 |
| `textColor` | `Color?` | `{color-primary}` | 展开时文字色 |
| `collapsedTextColor` | `Color?` | `{color-text-primary}` | 折叠时文字色 |
| `iconColor` | `Color?` | `{color-primary}` | 展开时图标色 |
| `collapsedIconColor` | `Color?` | `{color-text-tertiary}` | 折叠时图标色 |
| `shape` | `ShapeBorder?` | `RoundedRectangleBorder(borderRadius: 12)` | 展开时形状 |
| `collapsedShape` | `ShapeBorder?` | `RoundedRectangleBorder(borderRadius: 12)` | 折叠时形状 |
| `clipBehavior` | `Clip` | `Clip.none` | 裁剪行为 |
| `controlAffinity` | `ListTileControlAffinity` | `ListTileControlAffinity.platform` | 展开图标位置 |
| `dense` | `bool?` | `null` | 紧凑模式 |

## ListTileControlAffinity 取值

| 取值 | 图标位置 |
| --- | --- |
| `ListTileControlAffinity.platform` | 平台默认(通常 trailing) |
| `ListTileControlAffinity.leading` | 左侧(leading 之后) |
| `ListTileControlAffinity.trailing` | 右侧(title 之后) |

## ExpansionPanelList 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `children` | `List<ExpansionPanel>` | `const []` | 面板列表 |
| `expansionCallback` | `ExpansionPanelCallback` | 必填 | 展开/折叠回调 |
| `animationDuration` | `Duration` | `kThemeExpandDuration`(200ms) | 动画时长 |
| `elevation` | `double?` | `null`(M3 默认 0) | 面板高度 |
| `expandHeaderPadding` | `EdgeInsetsGeometry` | `EdgeInsets.symmetric(vertical: 16)` | 头部内边距 |
| `dividerColor` | `Color?` | `{color-outline-variant}` | 分隔线颜色 |
| `materialGapSize` | `double?` | `null`(M3 默认 4) | 面板间距 |

## ExpansionPanel 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `headerBuilder` | `ExpansionPanelHeaderBuilder` | 必填 | 头部构建器 |
| `body` | `Widget` | 必填 | 面板内容 |
| `bodyBuilder` | `ExpansionPanelBodyBuilder?` | `null`(M3 新增) | 内容构建器(可获焦) |
| `isExpanded` | `bool` | `false` | 是否展开 |
| `canTapOnHeader` | `bool` | `false` | 头部是否可点击 |
| `backgroundColor` | `Color?` | `null` | 背景色 |

## ExpansionPanelRadio 属性(单选式)

继承自 `ExpansionPanel`,增加:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `Object` | 必填 | 唯一标识(用于单选互斥) |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Collapse 完整示例:展示 ExpansionTile 与 ExpansionPanelList.radio
class CollapseFullSample extends StatefulWidget {
  const CollapseFullSample({super.key});

  @override
  State<CollapseFullSample> createState() => _CollapseFullSampleState();
}

class _CollapseFullSampleState extends State<CollapseFullSample> {
  int? _radioPanel;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Collapse 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 自定义样式 ExpansionTile
          ExpansionTile(
            title: Text(
              '自定义面板',
              style: TextStyle(
                fontSize: {font-size-md},
                fontWeight: FontWeight.w600,
                color: {color-text-primary},
              ),
            ),
            subtitle: Text(
              '3 项',
              style: TextStyle(fontSize: {font-size-sm}, color: {color-text-secondary}),
            ),
            leading: Icon(Icons.expand_more, size: {icon-size-sm}, color: {color-primary}),
            backgroundColor: {color-surface-variant},
            collapsedBackgroundColor: {color-surface},
            textColor: {color-primary},
            collapsedTextColor: {color-text-primary},
            iconColor: {color-primary},
            collapsedIconColor: {color-text-tertiary},
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular({radius-md}),
              side: BorderSide(color: {color-outline-variant}),
            ),
            tilePadding: EdgeInsets.symmetric(horizontal: {spacing-md}),
            childrenPadding: EdgeInsets.symmetric(horizontal: {spacing-md}),
            children: const [
              ListTile(title: Text('子项 1')),
              ListTile(title: Text('子项 2')),
              ListTile(title: Text('子项 3')),
            ],
          ),
          SizedBox(height: {spacing-lg}),
          // 2. ExpansionPanelList.radio(单选式手风琴)
          ExpansionPanelList.radio(
            elevation: 0,
            materialGapSize: {spacing-xs},
            dividerColor: {color-outline-variant},
            expansionCallback: (i, expanded) {
              setState(() {
                _radioPanel = expanded ? i : null;
              });
            },
            children: [
              ExpansionPanelRadio(
                value: 0,
                canTapOnHeader: true,
                headerBuilder: (_, __) => const Text('面板 1'),
                body: const ListTile(title: Text('内容 1')),
                isExpanded: _radioPanel == 0,
              ),
              ExpansionPanelRadio(
                value: 1,
                canTapOnHeader: true,
                headerBuilder: (_, __) => const Text('面板 2'),
                body: const ListTile(title: Text('内容 2')),
                isExpanded: _radioPanel == 1,
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
  expansionTileTheme: ExpansionTileThemeData(
    backgroundColor: {color-surface-variant},
    collapsedBackgroundColor: {color-surface},
    textColor: {color-primary},
    collapsedTextColor: {color-text-primary},
    iconColor: {color-primary},
    collapsedIconColor: {color-text-tertiary},
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-md}),
    ),
    collapsedShape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-md}),
    ),
    tilePadding: EdgeInsets.symmetric(horizontal: {spacing-md}),
    childrenPadding: EdgeInsets.symmetric(horizontal: {spacing-md}),
  ),
  dividerTheme: DividerThemeData(
    color: {color-outline-variant},
    thickness: 1,
    space: 1,
  ),
)
```

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - ExpansionTile: https://api.flutter.dev/flutter/material/ExpansionTile-class.html
- API 参考 - ExpansionPanelList: https://api.flutter.dev/flutter/material/ExpansionPanelList-class.html
- API 参考 - ExpansionPanel: https://api.flutter.dev/flutter/material/ExpansionPanel-class.html
- API 参考 - ExpansionPanelRadio: https://api.flutter.dev/flutter/material/ExpansionPanelRadio-class.html
- API 参考 - ExpansionTileThemeData: https://api.flutter.dev/flutter/material/ExpansionTileThemeData-class.html
