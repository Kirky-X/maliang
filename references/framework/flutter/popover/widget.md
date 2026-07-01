# Flutter Popover Widget 定义

> **本框架无原生 Popover Widget。**

## 占位说明

Flutter Material Design 3 **未提供名为 `Popover` 的独立 Widget**。其他框架(Ant Design / Element Plus)中的"气泡卡片/弹出层"组件,在 Flutter 中通过以下 Widget 组合实现:

| 其他框架的 Popover 场景 | Flutter 对应实现 |
| --- | --- |
| 菜单弹出 | `MenuAnchor` + `MenuItemButton`(M3 菜单体系) |
| 信息提示气泡 | `Tooltip`(悬停提示,无交互) |
| 卡片式弹出层 | `showDialog` + `Dialog` / `AlertDialog`(模态) |
| 非模态弹出层 | `Overlay` + `OverlayEntry`(自定义非模态浮层) |
| 列表选择弹出 | `PopupMenuButton` + `PopupMenuItem`(旧版菜单) |
| 上下文菜单 | `ContextMenuController` + `ContextMenuController` |

## 推荐替代方案

### 1. 菜单弹出 → MenuAnchor

```dart
MenuAnchor(
  builder: (context, controller, child) {
    return FilledButton(
      onPressed: () => controller.open(),
      child: const Text('打开菜单'),
    );
  },
  menuChildren: [
    MenuItemButton(
      onPressed: () {},
      child: const Text('选项 1'),
    ),
    MenuItemButton(
      onPressed: () {},
      child: const Text('选项 2'),
    ),
  ],
)
```

详见 `menu/widget.md`。

### 2. 信息提示 → Tooltip

```dart
Tooltip(
  message: '这是提示信息',
  child: const Icon(Icons.info_outline),
)
```

### 3. 模态卡片 → showDialog

```dart
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: const Text('标题'),
    content: const Text('内容'),
    actions: [
      TextButton(onPressed: () => Navigator.pop(context), child: const Text('关闭')),
    ],
  ),
)
```

详见 `dialog/widget.md`。

### 4. 非模态自定义浮层 → Overlay + OverlayEntry

```dart
final overlay = Overlay.of(context);
late OverlayEntry entry;
entry = OverlayEntry(
  builder: (context) => Positioned(
    top: 100,
    left: 50,
    child: Material(
      color: Colors.transparent,
      child: Container(
        padding: const EdgeInsets.all({spacing-sm}),
        decoration: BoxDecoration(
          color: {color-surface},
          borderRadius: BorderRadius.circular({radius-md}),
          boxShadow: [
            BoxShadow(color: {color-shadow}, blurRadius: 8),
          ],
        ),
        child: const Text('自定义浮层'),
      ),
    ),
  ),
);
overlay.insert(entry);
// 关闭:entry.remove();
```

> 注:`Overlay` + `OverlayEntry` 是最灵活的方式,但需要自行处理位置计算、点击外部关闭、动画等;优先考虑 `MenuAnchor`。

## 第三方包

如需 Ant Design 风格的气泡 Popover,可使用第三方包:

- `popover` (https://pub.flutter-io.cn/packages/popover):提供 `Popover` Widget,支持箭头方向、自定义内容
- `super_bubble` (https://pub.flutter-io.cn/packages/super_bubble):气泡组件

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - MenuAnchor: https://api.flutter.dev/flutter/material/MenuAnchor-class.html
- API 参考 - Tooltip: https://api.flutter.dev/flutter/material/Tooltip-class.html
- API 参考 - Overlay: https://api.flutter.dev/flutter/widgets/Overlay-class.html
- pub.dev - popover: https://pub.flutter-io.cn/packages/popover
