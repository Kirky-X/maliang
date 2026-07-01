# Flutter Menu Widget 定义

## Widget 定义

Flutter 自 3.0 起提供基于 M3 规范的菜单体系(`MenuBar` / `MenuAnchor` / `MenuItemButton` / `SubmenuButton`),替代旧版 `PopupMenuButton`。菜单体系基于 `MenuItemButton` 抽象类,支持级联子菜单、键盘导航、平台原生快捷键适配。

| Menu 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 菜单栏 | `MenuBar` | `StatefulWidget` | 顶部菜单栏(File/Edit/View),桌面端原生风格 |
| 弹出菜单锚点 | `MenuAnchor` | `StatefulWidget` | 绑定触发器(按钮/长按),弹出 `MenuChildren` |
| 菜单项 | `MenuItemButton` | `MenuItemButton` | 可点击菜单项(对应旧 `PopupMenuItem`) |
| 子菜单 | `SubmenuButton` | `MenuItemButton` | 含子级菜单的可展开项 |
| 复选菜单项 | `CheckboxMenuButton` | `MenuItemButton` | 带勾选框的菜单项 |
| 单选菜单项 | `RadioMenuButton` | `MenuItemButton` | 单选菜单项 |
| 分隔线 | `MenuAcceleratorLabel` / `Divider` | - | 分隔线或带助记符标签 |

> 旧版 `PopupMenuButton` / `PopupMenuItem` 仍可用,但 M3 推荐使用 `MenuAnchor` + `MenuItemButton`。

## 构造函数

### MenuBar

```dart
const MenuBar({
  Key? key,
  required List<MenuChildren> children,
  AlignmentGeometry alignment = Alignment.center,
  MenuStyle? style,
  Widget? trailing,
})
```

### MenuAnchor

```dart
const MenuAnchor({
  Key? key,
  Widget? child,
  WidgetBuilder? builder,
  AlignmentOffset? alignmentOffset,
  MenuStyle? style,
  Clip clipBehavior = Clip.hardEdge,
  CrossAxisAlignment crossAxisAlignment = CrossAxisAlignment.center,
  bool consumeOutsideTaps = true,
  required List<MenuChildren> menuChildren,
  Offset? alignmentOffset,
  bool? enableSafeArea,
  MenuController? controller,
})
```

### MenuItemButton

```dart
const MenuItemButton({
  Key? key,
  VoidCallback? onPressed,
  VoidCallback? onHover,
  Widget? leadingIcon,
  Widget? trailingIcon,
  Widget? closeProgress,
  Widget? label,
  bool enabled = true,
  MenuItemStyle? style,
})
```

### SubmenuButton

```dart
const SubmenuButton({
  Key? key,
  MenuStyle? menuStyle,
  AlignmentOffset? alignmentOffset,
  Clip clipBehavior = Clip.hardEdge,
  bool enabled = true,
  required Widget menuChildren,
  Widget? leadingIcon,
  Widget? trailingIcon,
  Widget? label,
})
```

## 核心属性

### MenuAnchor

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `child` / `builder` | `Widget?` / `WidgetBuilder?` | 锚点 Widget(触发器) |
| `menuChildren` | `List<MenuChildren>` | 菜单项列表 |
| `controller` | `MenuController?` | 控制器,程序化打开/关闭 |
| `alignmentOffset` | `Offset?` | 弹出位置偏移 |
| `consumeOutsideTaps` | `bool` | 外部点击是否关闭菜单(默认 `true`) |
| `clipBehavior` | `Clip` | 裁剪行为 |
| `enableSafeArea` | `bool?` | 是否避免被系统 UI 遮挡 |

### MenuItemButton

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `onPressed` | `VoidCallback?` | 点击回调;为 `null` 时禁用 |
| `onHover` | `VoidCallback?` | 鼠标悬停回调 |
| `leadingIcon` | `Widget?` | 前置图标 |
| `trailingIcon` | `Widget?` | 后置图标(常用于快捷键提示) |
| `label` | `Widget?` | 菜单文本 |
| `enabled` | `bool` | 是否可用(默认 `true`) |
| `style` | `MenuItemStyle?` | 菜单项样式 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Menu 最小示例:MenuAnchor + MenuItemButton
class MenuSample extends StatelessWidget {
  const MenuSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Menu 示例')),
      body: Center(
        child: MenuAnchor(
          builder: (context, controller, child) {
            return FilledButton(
              onPressed: () {
                controller.isOpen ? controller.close() : controller.open();
              },
              child: const Text('打开菜单'),
            );
          },
          menuChildren: [
            MenuItemButton(
              onPressed: () => _handle('新建'),
              leadingIcon: const Icon(Icons.add),
              child: const Text('新建'),
            ),
            MenuItemButton(
              onPressed: () => _handle('打开'),
              leadingIcon: const Icon(Icons.folder_open),
              child: const Text('打开'),
            ),
            MenuItemButton(
              onPressed: () => _handle('保存'),
              leadingIcon: const Icon(Icons.save),
              trailingIcon: const Text('⌘S'),
              child: const Text('保存'),
            ),
            const Divider(),
            MenuItemButton(
              onPressed: null,
              child: const Text('导出(禁用)'),
            ),
          ],
        ),
      ),
    );
  }

  void _handle(String action) {
    debugPrint('点击了 $action');
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
MenuAnchor(
  style: MenuStyle(
    backgroundColor: MaterialStateProperty.all({color-surface}),
    elevation: MaterialStateProperty.all({elevation-md}),
    shape: MaterialStateProperty.all(
      RoundedRectangleBorder(
        borderRadius: BorderRadius.circular({radius-md}),
      ),
    ),
    padding: MaterialStateProperty.all(
      const EdgeInsets.symmetric(vertical: {spacing-sm}),
    ),
  ),
  menuChildren: [
    MenuItemButton(
      style: MenuItemButton.styleFrom(
        foregroundColor: MaterialStateProperty.resolveWith((states) {
          return states.contains(MaterialState.disabled)
              ? {color-text-disabled}
              : {color-text-primary};
        }),
        backgroundColor: MaterialStateProperty.resolveWith((states) {
          return states.contains(MaterialState.hovered)
              ? {color-bg-hover}
              : Colors.transparent;
        }),
      ),
      onPressed: () {},
      child: const Text('自定义样式菜单项'),
    ),
  ],
  builder: (context, controller, child) {
    return TextButton(
      onPressed: () => controller.open(),
      child: const Text('触发'),
    );
  },
)
```

> 注:示例中的 `{color-surface}`、`{spacing-sm}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - MenuBar: https://api.flutter.dev/flutter/material/MenuBar-class.html
- API 参考 - MenuAnchor: https://api.flutter.dev/flutter/material/MenuAnchor-class.html
- API 参考 - MenuItemButton: https://api.flutter.dev/flutter/material/MenuItemButton-class.html
- API 参考 - SubmenuButton: https://api.flutter.dev/flutter/material/SubmenuButton-class.html
- API 参考 - CheckboxMenuButton: https://api.flutter.dev/flutter/material/CheckboxMenuButton-class.html
