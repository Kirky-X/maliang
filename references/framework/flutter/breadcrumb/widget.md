# Flutter Breadcrumb Widget 定义

> **本框架无原生 Breadcrumb Widget。**

## 占位说明

Flutter Material Design 3 **未提供名为 `Breadcrumb` 的独立 Widget**。其他框架(Ant Design `Breadcrumb`、Element `el-breadcrumb`)中的面包屑导航,在 Flutter 中通过以下方式实现:

| 其他框架的 Breadcrumb 场景 | Flutter 对应实现 |
| --- | --- |
| 简单路径展示 | `Wrap` + `Text` + `Icon(Icons.chevron_right)` |
| 可点击导航 | `Wrap` + `TextButton` + 分隔符 |
| 带下拉的面包屑 | `Wrap` + `MenuAnchor` + `MenuItemButton` |
| 移动端折叠 | `Wrap` + `PopupMenuButton`(溢出项) |

## 推荐替代方案

### 1. 简单路径展示 → Wrap + Text

```dart
Wrap(
  spacing: {spacing-xs},
  crossAxisAlignment: WrapCrossAlignment.center,
  children: [
    Text('首页', style: TextStyle(color: {color-text-secondary})),
    Icon(Icons.chevron_right, size: {icon-size-sm}, color: {color-text-tertiary}),
    Text('分类', style: TextStyle(color: {color-text-secondary})),
    Icon(Icons.chevron_right, size: {icon-size-sm}, color: {color-text-tertiary}),
    Text('详情', style: TextStyle(color: {color-text-primary}, fontWeight: FontWeight.w600)),
  ],
)
```

### 2. 可点击导航 → Wrap + TextButton

```dart
class BreadcrumbItem {
  const BreadcrumbItem({required this.label, required this.onTap});
  final String label;
  final VoidCallback onTap;
}

class Breadcrumb extends StatelessWidget {
  const Breadcrumb({super.key, required this.items, this.current});

  final List<BreadcrumbItem> items;
  final String? current;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: {spacing-xs},
      crossAxisAlignment: WrapCrossAlignment.center,
      children: [
        for (final item in items) ...[
          TextButton(
            onPressed: item.onTap,
            style: TextButton.styleFrom(
              padding: EdgeInsets.zero,
              minimumSize: Size.zero,
              tapTargetSize: MaterialTapTargetSize.shrinkWrap,
              foregroundColor: {color-text-secondary},
              textStyle: TextStyle(fontSize: {font-size-md}),
            ),
            child: Text(item.label),
          ),
          Icon(Icons.chevron_right, size: {icon-size-sm}, color: {color-text-tertiary}),
        ],
        if (current != null)
          Text(
            current!,
            style: TextStyle(
              fontSize: {font-size-md},
              fontWeight: FontWeight.w600,
              color: {color-text-primary},
            ),
          ),
      ],
    );
  }
}
```

### 3. 带下拉的面包屑 → MenuAnchor

```dart
MenuAnchor(
  menuChildren: [
    MenuItemButton(onPressed: () {}, child: const Text('首页')),
    MenuItemButton(onPressed: () {}, child: const Text('分类 A')),
    MenuItemButton(onPressed: () {}, child: const Text('分类 B')),
  ],
  builder: (_, controller, __) => TextButton.icon(
    onPressed: () => controller.open(),
    icon: const Icon(Icons.arrow_drop_down),
    label: const Text('更多'),
  ),
)
```

> 注:示例中的 `{color-text-primary}`、`{spacing-xs}`、`{icon-size-sm}`、`{font-size-md}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Wrap: https://api.flutter.dev/flutter/widgets/Wrap-class.html
- API 参考 - TextButton: https://api.flutter.dev/flutter/material/TextButton-class.html
- API 参考 - MenuAnchor: https://api.flutter.dev/flutter/material/MenuAnchor-class.html
