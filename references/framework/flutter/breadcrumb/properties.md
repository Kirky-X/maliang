# Flutter Breadcrumb 属性列表与默认值

> **本框架无原生 Breadcrumb Widget,以下为替代方案的属性汇总。**

## 占位说明

Flutter 不存在 `Breadcrumb` 类。本文档汇总替代实现(`Wrap` + `TextButton` + `MenuAnchor`)的关键属性,供设计 token 映射参考。

## 替代方案 1:Wrap(布局容器)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<Widget>` | 必填 | 子节点列表 |
| `direction` | `Axis` | `Axis.horizontal` | 主轴方向 |
| `alignment` | `WrapAlignment` | `WrapAlignment.start` | 主轴对齐 |
| `spacing` | `double` | `0.0` | 主轴间距 |
| `runAlignment` | `WrapAlignment` | `WrapAlignment.start` | 交叉轴对齐 |
| `runSpacing` | `double` | `0.0` | 交叉轴间距 |
| `crossAxisAlignment` | `WrapCrossAlignment` | `WrapCrossAlignment.start` | 子项交叉对齐 |
| `textDirection` | `TextDirection?` | `null` | 文本方向 |
| `verticalDirection` | `VerticalDirection` | `VerticalDirection.down` | 垂直方向 |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 裁剪行为 |

## 替代方案 2:TextButton(可点击节点)

详见 `button/properties.md`。核心属性:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `onPressed` | `VoidCallback?` | 必填 | 点击回调 |
| `child` | `Widget` | 必填 | 子节点 |
| `style` | `ButtonStyle?` | `null` | 样式(可压缩 padding) |

### TextButton.styleFrom 紧凑样式

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `padding` | `EdgeInsetsGeometry?` | 内边距(可设 `EdgeInsets.zero`) |
| `minimumSize` | `Size?` | 最小尺寸(可设 `Size.zero`) |
| `tapTargetSize` | `MaterialTapTargetSize?` | 点击区域(`shrinkWrap` 压缩) |
| `foregroundColor` | `Color?` | 前景色 |

## 替代方案 3:MenuAnchor(下拉节点)

详见 `menu/properties.md`。核心属性:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `menuChildren` | `List<MenuChildren>` | 必填 | 菜单项列表 |
| `controller` | `MenuController?` | `null` | 控制器 |
| `alignmentOffset` | `Offset?` | `null` | 弹出位置偏移 |
| `consumeOutsideTaps` | `bool` | `true` | 外部点击关闭 |
| `style` | `MenuStyle?` | `null` | 样式 |

## 替代方案 4:Icon(分隔符)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `icon` | `IconData` | 必填 | 图标(常用 `Icons.chevron_right`) |
| `size` | `double?` | `null`(默认 24) | 尺寸 |
| `color` | `Color?` | `null`(取主题) | 颜色 |
| `semanticLabel` | `String?` | `null` | 无障碍标签 |
| `textDirection` | `TextDirection?` | `null` | 文本方向 |

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 已访问节点文字 | `{color-text-secondary}` |
| 当前节点文字 | `{color-text-primary}` / `{font-weight-medium}` |
| 分隔符图标 | `{color-text-tertiary}` / `{icon-size-sm}` |
| 节点间距 | `{spacing-xs}` |
| 节点文字大小 | `{font-size-md}` |
| 下拉触发图标 | `{color-primary}` |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Wrap: https://api.flutter.dev/flutter/widgets/Wrap-class.html
- API 参考 - TextButton: https://api.flutter.dev/flutter/material/TextButton-class.html
- API 参考 - MenuAnchor: https://api.flutter.dev/flutter/material/MenuAnchor-class.html
- API 参考 - Icon: https://api.flutter.dev/flutter/widgets/Icon-class.html
