# Flutter Popover 属性列表与默认值

> **本框架无原生 Popover Widget,以下为替代方案的属性汇总。**

## 占位说明

Flutter 不存在 `Popover` 类。本文档汇总替代实现(`MenuAnchor` / `Tooltip` / `OverlayEntry` / `showDialog`)的关键属性,供设计 token 映射参考。详细属性请参阅对应组件的 `properties.md`。

## 替代方案 1:MenuAnchor(菜单弹出)

详见 `menu/properties.md`。核心属性:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `menuChildren` | `List<MenuChildren>` | 必填 | 菜单项列表 |
| `controller` | `MenuController?` | `null` | 控制器 |
| `alignmentOffset` | `Offset?` | `null` | 弹出位置偏移 |
| `consumeOutsideTaps` | `bool` | `true` | 外部点击关闭 |
| `style` | `MenuStyle?` | `null` | 样式(背景色/阴影/形状) |

## 替代方案 2:Tooltip(信息提示)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `message` | `String` | 必填 | 提示文本 |
| `child` | `Widget` | 必填 | 触发 Widget |
| `waitDuration` | `Duration?` | `null`(默认 0) | 显示前等待时长 |
| `showDuration` | `Duration?` | `null`(默认 1.5s) | 显示时长 |
| `exitDuration` | `Duration?` | `null`(默认 100ms) | 消失动画时长 |
| `preferBelow` | `bool` | `true` | 是否优先显示在下方 |
| `verticalOffset` | `double` | `24.0` | 垂直偏移 |
| `margin` | `EdgeInsetsGeometry` | `EdgeInsets.all(0)` | 外边距 |
| `padding` | `EdgeInsetsGeometry` | `EdgeInsets.symmetric(horizontal: 16, vertical: 4)` | 内边距 |
| `decoration` | `Decoration?` | `null`(默认圆角矩形) | 装饰 |
| `textStyle` | `TextStyle?` | `null`(取主题) | 文本样式 |
| `textAlign` | `TextAlign` | `TextAlign.start` | 文本对齐 |
| `triggerMode` | `TooltipTriggerMode` | `TooltipTriggerMode.longPress` | 触发模式(M3 默认长按) |
| `enableFeedback` | `bool` | `true` | 触觉反馈 |
| `excludeFromSemantics` | `bool` | `false` | 是否排除语义 |

## 替代方案 3:OverlayEntry(自定义浮层)

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `builder` | `WidgetBuilder` | 浮层内容构建器 |
| `opaque` | `bool` | 是否不透明(默认 `false`,允许穿透) |
| `canSizeOverlay` | `bool` | 是否影响后续 Overlay 尺寸 |
| `opaque` | `bool` | 是否完全遮挡下层 |

### OverlayEntry 方法

| 方法 | 说明 |
| --- | --- |
| `remove()` | 从 Overlay 移除 |
| `markNeedsBuild()` | 标记需要重建 |

### Overlay.of 静态方法

```dart
Overlay.of(context, {bool rootOverlay = false, Widget? debugRequiredFor})
```

## 替代方案 4:showDialog(模态对话框)

详见 `dialog/properties.md`。核心参数:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `context` | `BuildContext` | 必填 | 上下文 |
| `builder` | `WidgetBuilder` | 必填 | 对话框构建器 |
| `barrierDismissible` | `bool` | `true` | 点击遮罩关闭 |
| `barrierColor` | `Color?` | `Colors.black54` | 遮罩颜色 |
| `useSafeArea` | `bool` | `true` | 是否避开系统 UI |
| `useRootNavigator` | `bool` | `true` | 是否使用根 Navigator |
| `routeSettings` | `RouteSettings?` | `null` | 路由设置 |
| `routeSettings.arguments` | `Object?` | `null` | 路由参数 |

## 第三方包 popover 属性

`popover` 包(https://pub.flutter-io.cn/packages/popover)提供:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget` | 必填 | 触发 Widget |
| `bodyBuilder` | `PopoverBuilder` | 必填 | 浮层内容构建器 |
| `direction` | `PopoverDirection` | `PopoverDirection.bottom` | 弹出方向 |
| `popoverDuration` | `Duration` | `Duration(seconds: 5)` | 显示时长(0 表示持续) |
| `radius` | `double` | `8.0` | 圆角 |
| `arrowWidth` | `double` | `20.0` | 箭头宽度 |
| `arrowHeight` | `double` | `10.0` | 箭头高度 |
| `backgroundColor` | `Color` | `Colors.white` | 背景色 |
| `shadowColor` | `Color` | `Colors.black26` | 阴影色 |
| `shadowBlur` | `double` | `10.0` | 阴影模糊 |
| `barrierColor` | `Color` | `Colors.transparent` | 遮罩色 |
| `contentDxOffset` | `double` | `0.0` | 内容横向偏移 |
| `contentDyOffset` | `double` | `0.0` | 内容纵向偏移 |
| `constraints` | `BoxConstraints?` | `null` | 尺寸约束 |

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 浮层背景 | `{color-surface}` |
| 浮层阴影 | `{color-shadow}` / `{elevation-md}` |
| 浮层圆角 | `{radius-md}` |
| 浮层内边距 | `{spacing-sm}` |
| 浮层文字 | `{font-size-md}` / `{color-text-primary}` |
| 遮罩色 | `{color-mask}`(通常为黑色 50% 透明度) |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Tooltip: https://api.flutter.dev/flutter/material/Tooltip-class.html
- API 参考 - OverlayEntry: https://api.flutter.dev/flutter/widgets/OverlayEntry-class.html
- API 参考 - showDialog: https://api.flutter.dev/flutter/material/showDialog.html
- pub.dev - popover: https://pub.flutter-io.cn/packages/popover
