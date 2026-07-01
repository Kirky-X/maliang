# Flutter Badge 属性列表与默认值

本文档汇总 Material Design 3 徽标(`Badge` / `Badge.count`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## Badge 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `label` | `Widget?` | `null` | 徽标内容(`null` 时仅显示小圆点) |
| `child` | `Widget?` | `null` | 被标记的子节点 |
| `backgroundColor` | `Color?` | `{color-error}` | 背景色 |
| `textColor` | `Color?` | `{color-on-error}` | 文字色(label 为 Text 时生效) |
| `isLabelVisible` | `bool` | `true` | 是否显示 label(为 `false` 时仅显示小圆点) |
| `smallSize` | `double?` | `6.0` | 小圆点尺寸(无 label 时) |
| `largeSize` | `double?` | `16.0` | 含 label 时尺寸 |
| `labelStyle` | `TextStyle?` | `{font-size-xs}` / `{color-on-error}` | label 文字样式 |
| `padding` | `EdgeInsetsGeometry?` | `EdgeInsets.symmetric(horizontal: 4)` | label 内边距 |
| `alignment` | `AlignmentGeometry` | `Alignment.topEnd` | 徽标对齐位置 |
| `offset` | `Offset?` | `null` | 位置偏移 |
| `textStyle` | `TextStyle?` | 已废弃 | 旧文字样式(请用 `labelStyle`) |
| `elevation` | `double?` | `null`(默认 0) | 高度 |
| `shape` | `ShapeBorder?` | `CircleBorder`(小圆点) / `StadiumBorder`(含 label) | 形状 |

## Badge.count 工厂参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `count` | `int` | 必填 | 数字(>= 1000 显示 `999+`,>= 100 显示 `99+`) |
| `child` | `Widget?` | `null` | 子节点 |
| `backgroundColor` | `Color?` | `{color-error}` | 背景色 |
| `textColor` | `Color?` | `{color-on-error}` | 文字色 |
| `isLabelVisible` | `bool` | `true` | 是否显示 label |
| `alignment` | `AlignmentGeometry` | `Alignment.topEnd` | 对齐 |
| `offset` | `Offset?` | `null` | 偏移 |
| 其余 | - | - | 同 `Badge` |

## alignment 取值与位置对应

| 取值 | 位置 |
| --- | --- |
| `Alignment.topEnd` | 右上(默认) |
| `Alignment.topStart` | 左上 |
| `Alignment.bottomEnd` | 右下 |
| `Alignment.bottomStart` | 左下 |
| `Alignment.center` | 正中(不推荐) |

## 尺寸行为

| 配置 | 显示效果 | 默认尺寸 |
| --- | --- | --- |
| `label == null` 且 `isLabelVisible == false` | 仅小圆点 | `smallSize`(6) |
| `label == null` 且 `isLabelVisible == true` | 仅小圆点(同上) | `smallSize`(6) |
| `label != null` 且 `isLabelVisible == true` | 含内容徽标 | `largeSize`(16) |
| `label != null` 且 `isLabelVisible == false` | 仅小圆点(忽略 label) | `smallSize`(6) |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Badge 完整示例:展示小圆点/数字/自定义/位置偏移
class BadgeFullSample extends StatelessWidget {
  const BadgeFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Badge 完整示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. 小圆点徽标
            const Text('小圆点:'),
            Badge(
              isLabelVisible: false,
              smallSize: {size-xxs},
              backgroundColor: {color-error},
              child: Icon(Icons.notifications, size: {icon-size-md}, color: {color-on-surface-variant}),
            ),
            SizedBox(height: {spacing-lg}),
            // 2. 数字徽标
            const Text('数字徽标:'),
            Row(
              children: [
                Badge(
                  label: const Text('3'),
                  backgroundColor: {color-error},
                  textColor: {color-on-error},
                  child: const Icon(Icons.mail, size: {icon-size-md}),
                ),
                SizedBox(width: {spacing-md}),
                // Badge.count 自动 99+ 截断
                Badge.count(
                  count: 99,
                  backgroundColor: {color-error},
                  textColor: {color-on-error},
                  child: const Icon(Icons.shopping_cart, size: {icon-size-md}),
                ),
                SizedBox(width: {spacing-md}),
                Badge.count(
                  count: 999,
                  backgroundColor: {color-error},
                  textColor: {color-on-error},
                  child: const Icon(Icons.chat, size: {icon-size-md}),
                ),
              ],
            ),
            SizedBox(height: {spacing-lg}),
            // 3. 自定义样式徽标
            const Text('自定义样式:'),
            Badge(
              label: Text(
                'NEW',
                style: TextStyle(
                  fontSize: {font-size-xxs},
                  fontWeight: FontWeight.w700,
                  color: {color-on-primary},
                ),
              ),
              backgroundColor: {color-primary},
              padding: EdgeInsets.symmetric(
                horizontal: {spacing-xs},
                vertical: 2,
              ),
              alignment: Alignment.topEnd,
              offset: const Offset(-4, -4),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular({radius-full}),
              ),
              child: Icon(Icons.star, size: {icon-size-md}, color: {color-on-surface-variant}),
            ),
            SizedBox(height: {spacing-lg}),
            // 4. 头像上的徽标(在线状态)
            const Text('头像在线状态:'),
            Badge(
              label: const Icon(Icons.circle, size: 8),
              backgroundColor: {color-success},
              alignment: Alignment.bottomEnd,
              offset: const Offset(-2, -2),
              child: CircleAvatar(
                radius: {size-sm},
                backgroundImage: const NetworkImage('https://example.com/avatar.png'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

```dart
ThemeData(
  badgeTheme: BadgeThemeData(
    backgroundColor: {color-error},
    textColor: {color-on-error},
    smallSize: {size-xxs},
    largeSize: {size-xs},
    labelStyle: TextStyle(
      fontSize: {font-size-xs},
      fontWeight: FontWeight.w600,
      color: {color-on-error},
    ),
    padding: EdgeInsets.symmetric(horizontal: {spacing-xs}),
    alignment: Alignment.topEnd,
    offset: const Offset(-3, -3),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-full}),
    ),
  ),
)
```

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Badge: https://api.flutter.dev/flutter/material/Badge-class.html
- API 参考 - BadgeThemeData: https://api.flutter.dev/flutter/material/BadgeThemeData-class.html
