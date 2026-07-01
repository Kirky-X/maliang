# Flutter Avatar Widget 定义

## Widget 定义

Flutter Material Design 3 提供圆形头像 `CircleAvatar` 与方形/自定义形状头像能力。M3 还引入 `Badge` 配合头像展示未读数(详见 `badge/widget.md`)。

| Avatar 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| CircleAvatar | `CircleAvatar` | `StatelessWidget` | 圆形头像(图片/文字/图标) |
| 自定义形状 | `Container` + `BoxDecoration` + `ClipPath` | - | 方形/圆角矩形/任意形状头像 |

> `CircleAvatar` 自动处理 `radius` / `minRadius` / `maxRadius` / `backgroundImage` / `child` 关系,内部用 `CircleAvatar` 自绘圆形并裁剪。

## 构造函数

### CircleAvatar

```dart
const CircleAvatar({
  super.key,
  this.child,                       // 子节点(文字/图标,与 backgroundImage 互斥优先)
  this.backgroundColor,             // 背景色(默认主题 secondary)
  this.backgroundImage,             // 背景图片(ImageProvider)
  this.foregroundImage,             // 前景图片(ImageProvider,叠加在 backgroundImage 上)
  this.foregroundColor,             // 前景色(影响 child 文字色)
  this.radius,                      // 半径(与 minRadius/maxRadius 互斥)
  this.minRadius,                   // 最小半径
  this.maxRadius,                   // 最大半径
  this.onBackgroundImageError,      // 背景图片加载错误回调
  this.onForegroundImageError,      // 前景图片加载错误回调
  this.backgroundImageErrorBuilder, // 背景图片错误构建器(M3 新增)
  this.foregroundImageErrorBuilder, // 前景图片错误构建器(M3 新增)
  this.clipBehavior = Clip.antiAlias, // 裁剪行为
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `child` | `Widget?` | 子节点(无图片时显示文字/图标) |
| `backgroundColor` | `Color?` | 背景色(无图片时生效) |
| `backgroundImage` | `ImageProvider?` | 背景图片 |
| `foregroundImage` | `ImageProvider?` | 前景图片(叠加在背景上) |
| `foregroundColor` | `Color?` | 前景色(影响 child) |
| `radius` | `double?` | 半径(默认 20) |
| `minRadius` | `double?` | 最小半径 |
| `maxRadius` | `double?` | 最大半径 |
| `onBackgroundImageError` | `ImageErrorListener?` | 背景图片错误回调 |
| `onForegroundImageError` | `ImageErrorListener?` | 前景图片错误回调 |
| `clipBehavior` | `Clip` | 裁剪行为(默认 `Clip.antiAlias`) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Avatar 最小示例:展示 CircleAvatar 三种用法
class AvatarSample extends StatelessWidget {
  const AvatarSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Avatar 示例')),
      body: Center(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            // 1. 文字头像
            CircleAvatar(
              radius: {size-sm},
              backgroundColor: {color-primary-container},
              foregroundColor: {color-on-primary-container},
              child: Text('A'),
            ),
            // 2. 图标头像
            CircleAvatar(
              radius: {size-sm},
              backgroundColor: {color-secondary-container},
              foregroundColor: {color-on-secondary-container},
              child: Icon(Icons.person, size: {icon-size-md}),
            ),
            // 3. 图片头像
            CircleAvatar(
              radius: {size-sm},
              backgroundImage: const NetworkImage('https://example.com/avatar.png'),
              onBackgroundImageError: (exception, stackTrace) {
                debugPrint('头像加载失败: $exception');
              },
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
// 文字头像 + 边框
CircleAvatar(
  radius: {size-md},
  backgroundColor: {color-primary-container},
  foregroundColor: {color-on-primary-container},
  child: Text(
    '王',
    style: TextStyle(
      fontSize: {font-size-md},
      fontWeight: FontWeight.w600,
    ),
  ),
)

// 图片头像 + 前景叠加(如加蒙版)
CircleAvatar(
  radius: {size-md},
  backgroundColor: {color-surface-variant},
  backgroundImage: const NetworkImage('https://example.com/avatar.png'),
  foregroundImage: const NetworkImage('https://example.com/overlay.png'),
  onBackgroundImageError: (_, __) {},
)

// 自定义方形头像(非 CircleAvatar)
Container(
  width: {size-lg},
  height: {size-lg},
  decoration: BoxDecoration(
    borderRadius: BorderRadius.circular({radius-md}),
    image: const DecorationImage(
      image: NetworkImage('https://example.com/avatar.png'),
      fit: BoxFit.cover,
    ),
    border: Border.all(color: {color-outline-variant}),
  ),
)

// 配合 Badge 展示未读数
Badge(
  label: const Text('3'),
  backgroundColor: {color-error},
  textColor: {color-on-error},
  child: CircleAvatar(
    radius: {size-md},
    backgroundImage: const NetworkImage('https://example.com/avatar.png'),
  ),
)
```

> 注:示例中的 `{color-primary-container}`、`{color-on-primary-container}`、`{color-secondary-container}`、`{color-outline-variant}`、`{size-sm}`、`{size-md}`、`{size-lg}`、`{icon-size-md}`、`{font-size-md}`、`{radius-md}`、`{color-error}`、`{color-on-error}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - CircleAvatar: https://api.flutter.dev/flutter/material/CircleAvatar-class.html
- API 参考 - Badge: https://api.flutter.dev/flutter/material/Badge-class.html
- API 参考 - ImageIcon: https://api.flutter.dev/flutter/widgets/ImageIcon-class.html
