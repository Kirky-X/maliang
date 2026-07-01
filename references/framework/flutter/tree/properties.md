# Flutter Tree 属性列表与默认值

> **本框架无原生 Tree Widget,以下为替代方案的属性汇总。**

## 占位说明

Flutter 不存在 `Tree` 类。本文档汇总替代实现(`ExpansionTile` / `ExpansionPanelList` / 第三方 `flutter_simple_treeview`)的关键属性,供设计 token 映射参考。

## 替代方案 1:ExpansionTile(简单二级展开)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `leading` | `Widget?` | `null` | 头部 Widget(通常为图标) |
| `title` | `Widget` | 必填 | 标题 |
| `subtitle` | `Widget?` | `null` | 副标题 |
| `backgroundColor` | `Color?` | `null`(取主题) | 展开时背景色 |
| `collapsedBackgroundColor` | `Color?` | `null` | 折叠时背景色 |
| `textColor` | `Color?` | `null` | 展开时文字色 |
| `collapsedTextColor` | `Color?` | `null` | 折叠时文字色 |
| `iconColor` | `Color?` | `null` | 展开时图标色 |
| `collapsedIconColor` | `Color?` | `null` | 折叠时图标色 |
| `shape` | `ShapeBorder?` | `null` | 展开时形状 |
| `collapsedShape` | `ShapeBorder?` | `null` | 折叠时形状 |
| `tilePadding` | `EdgeInsetsGeometry` | `EdgeInsets.symmetric(horizontal: 16, vertical: 4)` | 标题内边距 |
| `expandedAlignment` | `AlignmentGeometry?` | `null` | 子项对齐 |
| `expandedCrossAxisAlignment` | `CrossAxisAlignment?` | `null` | 子项交叉轴对齐 |
| `initiallyExpanded` | `bool` | `false` | 初始是否展开 |
| `maintainState` | `bool` | `false` | 折叠时是否保持子项状态 |
| `controlAffinity` | `ListTileControlAffinity` | `ListTileControlAffinity.platform` | 展开图标位置 |
| `childrenPadding` | `EdgeInsetsGeometry` | `EdgeInsets.symmetric(horizontal: 16)` | 子项区域内边距 |
| `clipBehavior` | `Clip` | `Clip.none` | 裁剪行为 |
| `onExpansionChanged` | `ValueChanged<bool>?` | `null` | 展开/折叠回调 |

## 替代方案 2:ExpansionPanelList(多面板展开)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<ExpansionPanel>` | 必填 | 面板列表 |
| `expansionCallback` | `ExpansionPanelCallback` | 必填 | 展开/折叠回调 |
| `animationDuration` | `Duration` | `kThemeExpandDuration`(200ms) | 动画时长 |
| `elevation` | `double?` | `null`(M3 默认 0) | 面板高度 |
| `expandHeaderPadding` | `EdgeInsetsGeometry` | `EdgeInsets.symmetric(vertical: 16)` | 展开头部内边距 |
| `dividerColor` | `Color?` | `null` | 分隔线颜色 |
| `materialGapSize` | `double?` | `null`(M3 默认 4) | 面板间距 |

### ExpansionPanel 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `headerBuilder` | `ExpansionPanelHeaderBuilder` | 必填 | 头部构建器 |
| `body` | `Widget` | 必填 | 面板内容 |
| `bodyBuilder` | `ExpansionPanelBodyBuilder?` | `null`(M3 新增) | 内容构建器(可获焦) |
| `isExpanded` | `bool` | `false` | 是否展开 |
| `canTapOnHeader` | `bool` | `false` | 头部是否可点击 |
| `backgroundColor` | `Color?` | `null` | 背景色 |

## 替代方案 3:第三方包 flutter_simple_treeview

`flutter_simple_treeview` 包(https://pub.flutter-io.cn/packages/flutter_simple_treeview)提供 `Tree` / `TreeNode`:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Tree.nodes` | `List<TreeNode>` | 必填 | 根节点列表 |
| `Tree.indent` | `double` | `24.0` | 缩进量 |
| `Tree.icon` | `Icon?` | `null`(默认展开/折叠图标) | 节点图标 |
| `TreeNode.content` | `Widget` | 必填 | 节点内容 |
| `TreeNode.children` | `List<TreeNode>` | `const []` | 子节点 |
| `TreeNode.isExpanded` | `bool` | `false` | 初始是否展开 |

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 节点背景 | `{color-surface}` |
| 节点展开态背景 | `{color-secondary-container}` |
| 节点文字 | `{font-size-md}` / `{color-text-primary}` |
| 节点图标 | `{color-primary}` / `{icon-size-sm}` |
| 层级缩进 | `{spacing-sm}`(每级) |
| 分隔线 | `{color-outline-variant}` |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - ExpansionTile: https://api.flutter.dev/flutter/material/ExpansionTile-class.html
- API 参考 - ExpansionPanelList: https://api.flutter.dev/flutter/material/ExpansionPanelList-class.html
- API 参考 - ExpansionPanel: https://api.flutter.dev/flutter/material/ExpansionPanel-class.html
- pub.dev - flutter_simple_treeview: https://pub.flutter-io.cn/packages/flutter_simple_treeview
