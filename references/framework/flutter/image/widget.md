# Flutter Image Widget 定义

## Widget 定义

Flutter 提供多种图片加载 Widget,均基于 `Image` 类(继承自 `StatefulWidget`)。区别在于图片来源:资源(`Image.asset`)、网络(`Image.network`)、文件(`Image.file`)、内存(`Image.memory`)。Material 风格的 `Image` + `ImageProvider` 体系负责解码、缓存、缩放。

| Widget | 工厂构造 | 来源 | 用途 |
| --- | --- | --- | --- |
| `Image.asset` | `Image.asset(String name)` | assets 资源 | 打包内置图片 |
| `Image.network` | `Image.network(String src)` | URL | 网络图片 |
| `Image.file` | `Image.file(File file)` | 本地文件 | 设备存储 |
| `Image.memory` | `Image.memory(Uint8List bytes)` | 内存字节 | 动态生成图片 |
| `Image` | `Image(image: ImageProvider)` | 任意 ImageProvider | 通用入口 |
| `CircleAvatar` | `CircleAvatar` | 子节点/图片 | 圆形头像(见 avatar) |

> 推荐使用 `Image` 通用构造 + 具体 `ImageProvider`(如 `AssetImage`/`NetworkImage`),便于复用与测试。

## 构造函数

### Image.network

```dart
Image.network(
  String src, {
  super.key,
  double scale = 1.0,
  Widget? loadingBuilder,            // 加载态构建器
  Widget? errorBuilder,             // 错误态构建器
  String? semanticLabel,
  bool excludeFromSemantics = false,
  Color? color,
  Animation<double>? opacity,
  BlendMode? colorBlendMode,
  BoxFit? fit,                      // 缩放模式
  AlignmentGeometry alignment = Alignment.center,
  ImageRepeat repeat = ImageRepeat.noRepeat,
  Rect? centerSlice,
  bool matchTextDirection = false,
  bool gaplessPlayback = false,
  FilterQuality filterQuality = FilterQuality.low,
  int? cacheWidth,                  // 解码目标宽(性能优化)
  int? cacheHeight,
})
```

### Image.asset

构造参数与 `Image.network` 基本一致,首个参数为资源路径 `String name`,额外支持 `AssetBundle? bundle`。

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `image` | `ImageProvider` | 图片数据源 |
| `fit` | `BoxFit?` | 缩放模式(fill/contain/cover/fitWidth/fitHeight/none/scaleDown) |
| `alignment` | `AlignmentGeometry` | 对齐,默认 `Alignment.center` |
| `repeat` | `ImageRepeat` | 平铺,默认 `noRepeat` |
| `width` / `height` | `double?` | 显示尺寸 |
| `color` / `colorBlendMode` | `Color?` / `BlendMode?` | 着色与混合 |
| `loadingBuilder` | `Widget Function(BuildContext, Widget, ImageChunkEvent?)` | 加载进度 |
| `errorBuilder` | `Widget Function(BuildContext, Object, StackTrace?)` | 加载失败 |
| `cacheWidth` / `cacheHeight` | `int?` | 解码目标尺寸(降低内存) |
| `filterQuality` | `FilterQuality` | 滤镜质量,默认 `low` |
| `semanticLabel` | `String?` | 无障碍描述 |

## 最小示例

```dart
import 'package:flutter/material.dart';

class ImageSample extends StatelessWidget {
  const ImageSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Image 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          children: [
            // 网络图片 + 加载/错误处理
            ClipRRect(
              borderRadius: BorderRadius.circular({radius-md}),
              child: Image.network(
                'https://example.com/avatar.png',
                width: 120, height: 120,
                fit: BoxFit.cover,
                loadingBuilder: (context, child, progress) =>
                    progress == null ? child : const CircularProgressIndicator(),
                errorBuilder: (context, error, stack) => Container(
                      width: 120, height: 120,
                      color: {color-bg-secondary},
                      child: Icon(Icons.broken_image,
                          color: {color-text-primary}),
                    ),
              ),
            ),
            const SizedBox(height: {spacing-md}),
            // 资源图片
            Image.asset(
              'assets/images/logo.png',
              width: 80,
              fit: BoxFit.contain,
            ),
          ],
        ),
      ),
    );
  }
}
```

## 参考链接

- Flutter 官方文档 - 添加资源和图片: https://docs.flutter.cn/ui/assets/assets-and-images
- Cookbook - 加载网络图片: https://docs.flutter.cn/cookbook/images/network-image
- Cookbook - 从占位图过渡到图片: https://docs.flutter.cn/cookbook/images/fading-in-images
- Widget 目录 - Assets: https://docs.flutter.cn/ui/widgets/assets
- API 参考 - Image: https://api.flutter.dev/flutter/widgets/Image-class.html
