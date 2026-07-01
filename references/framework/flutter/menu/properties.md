# Flutter Menu 属性列表与默认值

本文档汇总 Flutter M3 菜单体系(`MenuBar` / `MenuAnchor` / `MenuItemButton` / `SubmenuButton`)的完整属性、默认值与回调。所有视觉属性以 design token 形式引用,不在文档中硬编码。

## MenuBar 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<MenuChildren>` | 必填 | 顶层菜单项(通常为 `SubmenuButton`) |
| `alignment` | `AlignmentGeometry` | `Alignment.center` | 整体对齐 |
| `style` | `MenuStyle?` | `null`(取主题) | 菜单栏样式 |
| `trailing` | `Widget?` | `null` | 尾部附加 Widget |

## MenuAnchor 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` / `builder` | `Widget?` / `WidgetBuilder?` | `null` | 锚点 Widget |
| `menuChildren` | `List<MenuChildren>` | 必填 | 菜单项列表 |
| `controller` | `MenuController?` | `null` | 控制器(程序化打开/关闭) |
| `alignmentOffset` | `Offset?` | `null` | 弹出位置偏移 |
| `consumeOutsideTaps` | `bool` | `true` | 外部点击关闭菜单 |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 裁剪行为 |
| `crossAxisAlignment` | `CrossAxisAlignment` | `CrossAxisAlignment.center` | 锚点与触发器对齐 |
| `enableSafeArea` | `bool?` | `null` | 避免被系统 UI 遮挡 |
| `style` | `MenuStyle?` | `null` | 菜单样式 |

## MenuItemButton 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `onPressed` | `VoidCallback?` | `null` | 点击回调;`null` 时禁用 |
| `onHover` | `VoidCallback?` | `null` | 鼠标悬停回调 |
| `leadingIcon` | `Widget?` | `null` | 前置图标 |
| `trailingIcon` | `Widget?` | `null` | 后置图标(快捷键提示) |
| `label` | `Widget?` | `null` | 菜单文本(与 `child` 等效) |
| `enabled` | `bool` | `true` | 是否可用 |
| `style` | `MenuItemStyle?` | `null` | 菜单项样式 |

## SubmenuButton 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `menuChildren` | `List<MenuChildren>` | 必填 | 子菜单项列表 |
| `menuStyle` | `MenuStyle?` | `null` | 子菜单容器样式 |
| `alignmentOffset` | `Offset?` | `null` | 子菜单弹出位置偏移 |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 裁剪行为 |
| `enabled` | `bool` | `true` | 是否可用 |
| `leadingIcon` | `Widget?` | `null` | 前置图标 |
| `trailingIcon` | `Widget?` | `null` | 后置图标(默认箭头) |
| `label` | `Widget?` | `null` | 菜单文本 |

## CheckboxMenuButton 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `bool` | 必填 | 是否选中 |
| `onChanged` | `ValueChanged<bool?>?` | 必填 | 选中状态变化回调 |
| `groupValue` | `T?` | `null` | 单选组值(若用于单选) |
| `toggleable` | `bool` | `false` | 是否允许三态切换 |
| `trailingIcon` | `Widget?` | `null` | 后置图标 |
| `label` | `Widget?` | `null` | 菜单文本 |

## RadioMenuButton 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `T` | 必填 | 当前项值 |
| `groupValue` | `T?` | 必填 | 单选组当前值 |
| `onChanged` | `ValueChanged<T?>?` | 必填 | 选择变化回调 |
| `toggleable` | `bool` | `false` | 是否允许取消选择 |
| `label` | `Widget?` | `null` | 菜单文本 |

## MenuStyle 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `backgroundColor` | `MaterialStateProperty<Color?>` | `{color-surface}` | 背景色 |
| `shadowColor` | `MaterialStateProperty<Color?>` | `{color-shadow}` | 阴影色 |
| `surfaceTintColor` | `MaterialStateProperty<Color?>` | `{color-primary}` | 表面染色 |
| `elevation` | `MaterialStateProperty<double?>` | `{elevation-md}` | z 轴高度 |
| `shape` | `MaterialStateProperty<OutlinedBorder?>` | `RoundedRectangleBorder(8dp)` | 形状 |
| `padding` | `MaterialStateProperty<EdgeInsetsGeometry?>` | 上下 `{spacing-sm}` | 内边距 |
| `visualDensity` | `VisualDensity?` | `VisualDensity.standard` | 视觉密度 |
| `alignment` | `AlignmentGeometry?` | `null` | 子节点整体对齐 |
| `side` | `MaterialStateProperty<BorderSide?>` | `BorderSide.none` | 边框 |

## MenuItemStyle 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `backgroundColor` | `MaterialStateProperty<Color?>` | 透明 / hover `{color-bg-hover}` | 背景 |
| `foregroundColor` | `MaterialStateProperty<Color?>` | `{color-text-primary}` | 前景 |
| `overlayColor` | `MaterialStateProperty<Color?>` | `{color-primary}` 8% | 按压叠加 |
| `minimumSize` | `MaterialStateProperty<Size?>` | `Size.fromHeight(48)` | 最小尺寸 |
| `padding` | `MaterialStateProperty<EdgeInsetsGeometry?>` | 左右 `{spacing-md}` | 内边距 |
| `elevation` | `MaterialStateProperty<double?>` | `0` | 高度 |
| `shape` | `MaterialStateProperty<OutlinedBorder?>` | `StadiumBorder` | 形状 |
| `labelTextStyle` | `MaterialStateProperty<TextStyle?>` | `{font-size-md}` | 标签样式 |
| `iconColor` | `MaterialStateProperty<Color?>` | `{color-icon-default}` | 图标颜色 |
| `iconSize` | `MaterialStateProperty<double?>` | `{icon-size-sm}` | 图标尺寸 |

## MenuController 方法

| 方法 | 说明 |
| --- | --- |
| `open()` | 打开菜单 |
| `open(position: Offset)` | 在指定位置打开 |
| `close()` | 关闭菜单 |
| `closeAll()` | 关闭所有打开的菜单(级联) |
| `isOpen` | `bool` 当前是否打开 |
| `addListener / removeListener` | 监听开关状态 |

## 事件回调

| 回调 | 触发时机 |
| --- | --- |
| `MenuItemButton.onPressed` | 点击释放 |
| `MenuItemButton.onHover` | 鼠标进入/离开(桌面端) |
| `CheckboxMenuButton.onChanged` | 勾选状态变化 |
| `RadioMenuButton.onChanged` | 单选变化 |
| `MenuController` `addListener` | 菜单打开/关闭状态变化 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class MenuFullSample extends StatefulWidget {
  const MenuFullSample({super.key});

  @override
  State<MenuFullSample> createState() => _MenuFullSampleState();
}

class _MenuFullSampleState extends State<MenuFullSample> {
  bool _autoSave = true;
  String _theme = 'light';
  final MenuController _controller = MenuController();

  @override
  void dispose() {
    _controller.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Menu 完整示例'),
        actions: [
          // 1. MenuAnchor + 复选菜单项 + 单选菜单项
          MenuAnchor(
            controller: _controller,
            builder: (context, controller, child) {
              return IconButton(
                icon: const Icon(Icons.settings),
                onPressed: () => controller.open(),
              );
            },
            menuChildren: [
              // 复选菜单项
              CheckboxMenuButton(
                value: _autoSave,
                onChanged: (v) {
                  setState(() => _autoSave = v ?? false);
                },
                child: const Text('自动保存'),
              ),
              const Divider(),
              // 单选菜单项组
              RadioMenuButton<String>(
                value: 'light',
                groupValue: _theme,
                onChanged: (v) => setState(() => _theme = v!),
                child: const Text('浅色主题'),
              ),
              RadioMenuButton<String>(
                value: 'dark',
                groupValue: _theme,
                onChanged: (v) => setState(() => _theme = v!),
                child: const Text('深色主题'),
              ),
              RadioMenuButton<String>(
                value: 'system',
                groupValue: _theme,
                onChanged: (v) => setState(() => _theme = v!),
                child: const Text('跟随系统'),
              ),
              const Divider(),
              // 级联子菜单
              SubmenuButton(
                menuChildren: [
                  MenuItemButton(
                    onPressed: () {},
                    leadingIcon: const Icon(Icons.import_export),
                    child: const Text('从文件'),
                  ),
                  MenuItemButton(
                    onPressed: () {},
                    leadingIcon: const Icon(Icons.cloud_download),
                    child: const Text('从云端'),
                  ),
                ],
                child: const Text('导入'),
              ),
              const Divider(),
              MenuItemButton(
                onPressed: () => _controller.close(),
                trailingIcon: const Text('Esc'),
                child: const Text('关闭菜单'),
              ),
            ],
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('自动保存: $_autoSave'),
            Text('当前主题: $_theme'),
          ],
        ),
      ),
    );
  }
}
```

## 注意事项

- `MenuBar` 用于桌面端顶部菜单栏;移动端弹出菜单使用 `MenuAnchor`。
- `MenuItemButton` 的 `label` 与 `child` 二选一;`label` 自带 M3 文本样式,`child` 用于自定义 Widget。
- `SubmenuButton` 的级联深度无硬性限制,但建议 ≤ 2 级,过深的级联影响键盘导航体验。
- 键盘导航:`Tab` 在同级移动,`Enter` 触发,`→` 展开子菜单,`←` 收起子菜单,`Esc` 关闭;务必测试键盘可达性。
- `MenuStyle.elevation` 与 `shadowColor` 共同决定阴影效果;若使用 `surfaceTintColor`(M3 elevation tint),`shadowColor` 会失效。
- 助记符(`&`)通过 `MenuAcceleratorLabel` 实现,仅桌面端(macOS/Windows/Linux)生效,移动端忽略。
- 移动端菜单默认占满宽度;若需约束宽度,通过 `MenuStyle.maximumSize` 限制。
