# Flutter Avatar 属性列表与默认值

本文档汇总 Material Design 3 头像(`CircleAvatar`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## CircleAvatar 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `child` | `Widget?` | `null` | 子节点(无图片时显示文字/图标) |
| `backgroundColor` | `Color?` | `{color-secondary-container}` | 背景色(无图片时生效) |
| `backgroundImage` | `ImageProvider?` | `null` | 背景图片 |
| `foregroundImage` | `ImageProvider?` | `null` | 前景图片(叠加在 backgroundImage 上) |
| `foregroundColor` | `Color?` | `{color-on-secondary-container}` | 前景色(影响 child) |
| `radius` | `double?` | `20.0` | 半径(与 minRadius/maxRadius 互斥) |
| `minRadius` | `double?` | `null` | 最小半径 |
| `maxRadius` | `double?` | `null` | 最大半径 |
| `onBackgroundImageError` | `ImageErrorListener?` | `null` | 背景图片加载错误回调 |
| `onForegroundImageError` | `ImageErrorListener?` | `null` | 前景图片加载错误回调 |
| `backgroundImageErrorBuilder` | `ImageErrorWidgetBuilder?` | `null` | 背景图片错误构建器(M3 新增) |
| `foregroundImageErrorBuilder` | `ImageErrorWidgetBuilder?` | `null` | 前景图片错误构建器(M3 新增) |
| `clipBehavior` | `Clip` | `Clip.antiAlias` | 裁剪行为 |

## radius / minRadius / maxRadius 行为

| 配置 | 行为 |
| --- | --- |
| 仅 `radius` | 固定半径,`minRadius` / `maxRadius` 必须为 `null` |
| 仅 `minRadius` | 最小半径,实际由父约束决定 |
| 仅 `maxRadius` | 最大半径,实际由父约束决定 |
| `minRadius` + `maxRadius` | 半径在区间内由父约束决定 |
| 全部为 `null` | 默认 `radius = 20.0` |

## 尺寸与半径对应关系

| 半径(radius) | 直径 | 用途 |
| --- | --- | --- |
| `12` | `24` | 列表项小头像 |
| `16` | `32` | 紧凑列表 |
| `20`(默认) | `40` | 标准头像 |
| `24` | `48` | 卡片头像 |
| `32` | `64` | 详情页头像 |
| `48` | `96` | 个人主页大头像 |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Avatar 完整示例:展示文字/图标/图片/边框/Badge 组合
class AvatarFullSample extends StatelessWidget {
  const AvatarFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Avatar 完整示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. 不同尺寸文字头像
            const Text('尺寸对比:'),
            Row(
              children: [
                CircleAvatar(
                  radius: {size-xs},
                  backgroundColor: {color-primary-container},
                  foregroundColor: {color-on-primary-container},
                  child: const Text('XS'),
                ),
                SizedBox(width: {spacing-sm}),
                CircleAvatar(
                  radius: {size-sm},
                  backgroundColor: {color-primary-container},
                  foregroundColor: {color-on-primary-container},
                  child: const Text('S'),
                ),
                SizedBox(width: {spacing-sm}),
                CircleAvatar(
                  radius: {size-md},
                  backgroundColor: {color-primary-container},
                  foregroundColor: {color-on-primary-container},
                  child: const Text('M'),
                ),
                SizedBox(width: {spacing-sm}),
                CircleAvatar(
                  radius: {size-lg},
                  backgroundColor: {color-primary-container},
                  foregroundColor: {color-on-primary-container},
                  child: const Text('L'),
                ),
              ],
            ),
            SizedBox(height: {spacing-lg}),
            // 2. 图标头像
            const Text('图标头像:'),
            CircleAvatar(
              radius: {size-md},
              backgroundColor: {color-secondary-container},
              foregroundColor: {color-on-secondary-container},
              child: Icon(Icons.person, size: {icon-size-md}),
            ),
            SizedBox(height: {spacing-lg}),
            // 3. 图片头像(网络图片 + 错误回退)
            const Text('图片头像:'),
            CircleAvatar(
              radius: {size-md},
              backgroundColor: {color-surface-variant},
              backgroundImage: const NetworkImage('https://example.com/avatar.png'),
              onBackgroundImageError: (exception, stackTrace) {
                debugPrint('头像加载失败: $exception');
              },
              child: const Icon(Icons.person, color: Colors.white),
            ),
            SizedBox(height: {spacing-lg}),
            // 4. 带 Badge 的头像
            const Text('带未读数头像:'),
            Badge(
              label: const Text('99+'),
              backgroundColor: {color-error},
              textColor: {color-on-error},
              offset: const Offset(-3, -3),
              child: CircleAvatar(
                radius: {size-md},
                backgroundImage: const NetworkImage('https://example.com/avatar.png'),
              ),
            ),
            SizedBox(height: {spacing-lg}),
            // 5. 带边框的自定义方形头像
            const Text('方形头像:'),
            Container(
              width: {size-lg},
              height: {size-lg},
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular({radius-md}),
                image: const DecorationImage(
                  image: NetworkImage('https://example.com/avatar.png'),
                  fit: BoxFit.cover,
                ),
                border: Border.all(color: {color-outline-variant}, width: 1),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 头像背景色(无图片) | `{color-primary-container}` / `{color-secondary-container}` |
| 头像文字色 | `{color-on-primary-container}` / `{color-on-secondary-container}` |
| 头像默认半径 | `{size-sm}`(列表) / `{size-md}`(详情) / `{size-lg}`(主页) |
| 边框色 | `{color-outline-variant}` |
| 未读数背景 | `{color-error}` |
| 未读数文字 | `{color-on-error}` |
| 加载失败图标 | `{color-on-surface-variant}` |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - CircleAvatar: https://api.flutter.dev/flutter/material/CircleAvatar-class.html
- API 参考 - Badge: https://api.flutter.dev/flutter/material/Badge-class.html
- API 参考 - ImageIcon: https://api.flutter.dev/flutter/widgets/ImageIcon-class.html
