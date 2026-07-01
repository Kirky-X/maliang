# Flutter Badge Widget 定义

## Widget 定义

Flutter Material Design 3 提供 `Badge` Widget,用于在子节点(通常是图标/头像)右上角展示小圆点、数字或自定义文本。M3 推荐通过 `Badge` 替代早期 `new Badge`。

| Badge 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| Badge | `Badge` | `StatelessWidget` | M3 标准徽标(小圆点/数字/自定义) |
| Badge.count | `Badge` 工厂 | - | 数字徽标(自动 99+ 截断) |
| 自定义徽标 | `Stack` + `Positioned` | - | 完全自定义位置与样式 |

> `Badge` 内部用 `Stack` + `Positioned` 实现,自动处理子节点尺寸与徽标位置。

## 构造函数

### Badge

```dart
const Badge({
  super.key,
  this.label,                  // 徽标内容(Widget,通常为 Text)
  this.child,                  // 子节点(被标记的 Widget)
  this.backgroundColor,        // 背景色
  this.textColor,              // 文字色(label 为 Text 时生效)
  this.isLabelVisible = true,  // 是否显示 label(为 false 时仅显示小圆点)
  this.smallSize,              // 小圆点尺寸(无 label 时)
  this.largeSize,              // 含 label 时尺寸
  this.labelStyle,             // label 文字样式
  this.padding,                // label 内边距
  this.alignment = Alignment.topEnd,  // 徽标对齐位置
  this.offset,                 // 位置偏移
  this.textStyle,              // 已废弃,使用 labelStyle
  this.elevation,              // 高度(M3 新增)
  this.shape,                  // 形状(M3 新增)
})
```

### Badge.count(数字徽标工厂)

```dart
Badge.count({
  super.key,
  required int count,          // 数字(>= 1000 显示 999+,>= 100 显示 99+)
  this.child,
  this.backgroundColor,
  this.textColor,
  ...其余同 Badge...
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `label` | `Widget?` | 徽标内容(`null` 时仅显示小圆点) |
| `child` | `Widget?` | 被标记的子节点 |
| `backgroundColor` | `Color?` | 背景色 |
| `textColor` | `Color?` | 文字色 |
| `isLabelVisible` | `bool` | 是否显示 label |
| `smallSize` | `double?` | 小圆点尺寸(无 label,默认 6) |
| `largeSize` | `double?` | 含 label 时尺寸(默认 16) |
| `alignment` | `AlignmentGeometry` | 徽标对齐(默认 `topEnd`) |
| `offset` | `Offset?` | 位置偏移 |
| `elevation` | `double?` | 高度 |
| `shape` | `ShapeBorder?` | 形状 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Badge 最小示例:展示三种徽标用法
class BadgeSample extends StatelessWidget {
  const BadgeSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Badge 示例')),
      body: Center(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            // 1. 小圆点徽标
            const Badge(
              child: Icon(Icons.notifications, size: {icon-size-md}),
            ),
            // 2. 数字徽标
            Badge(
              label: const Text('3'),
              backgroundColor: {color-error},
              textColor: {color-on-error},
              child: const Icon(Icons.mail, size: {icon-size-md}),
            ),
            // 3. 数字徽标(Badge.count 工厂)
            Badge.count(
              count: 99,
              backgroundColor: {color-error},
              textColor: {color-on-error},
              child: const Icon(Icons.shopping_cart, size: {icon-size-md}),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
// 标准数字徽标
Badge(
  label: Text(
    '99+',
    style: TextStyle(
      fontSize: {font-size-xs},
      fontWeight: FontWeight.w600,
      color: {color-on-error},
    ),
  ),
  backgroundColor: {color-error},
  padding: EdgeInsets.symmetric(
    horizontal: {spacing-xs},
    vertical: 2,
  ),
  alignment: Alignment.topEnd,
  offset: const Offset(-3, -3),
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular({radius-full}),
  ),
  child: Icon(Icons.notifications, size: {icon-size-md}, color: {color-on-surface-variant}),
)

// 小圆点徽标
Badge(
  isLabelVisible: false,
  smallSize: {size-xxs},
  alignment: Alignment.topEnd,
  offset: const Offset(-2, -2),
  child: Icon(Icons.notifications, size: {icon-size-md}),
)
```

> 注:示例中的 `{color-error}`、`{color-on-error}`、`{color-on-surface-variant}`、`{font-size-xs}`、`{icon-size-md}`、`{size-xxs}`、`{spacing-xs}`、`{radius-full}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Badge: https://api.flutter.dev/flutter/material/Badge-class.html
- API 参考 - BadgeThemeData: https://api.flutter.dev/flutter/material/BadgeThemeData-class.html
