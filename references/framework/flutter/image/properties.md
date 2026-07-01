# Flutter Image 属性列表与默认值

本文档汇总 `Image` 系列图片 Widget 的属性、默认值与缩放模式。颜色/尺寸默认值以 design token 形式给出。

## 通用构造参数

`Image.asset` / `Image.network` / `Image.file` / `Image.memory` 共享以下参数(首参为数据源)。

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `scale` | `double` | `1.0` | 显示缩放比例 |
| `loadingBuilder` | `ImageLoadingBuilder?` | `null` | 加载进度构建器 |
| `errorBuilder` | `ImageErrorWidgetBuilder?` | `null` | 错误态构建器 |
| `semanticLabel` | `String?` | `null` | 无障碍描述 |
| `excludeFromSemantics` | `bool` | `false` | 是否排除无障碍 |
| `color` | `Color?` | `null` | 着色(配合 colorBlendMode) |
| `opacity` | `Animation<double>?` | `null` | 透明度动画 |
| `colorBlendMode` | `BlendMode?` | `null` | 混合模式 |
| `fit` | `BoxFit?` | `null` | 缩放模式 |
| `alignment` | `AlignmentGeometry` | `Alignment.center` | 对齐 |
| `repeat` | `ImageRepeat` | `ImageRepeat.noRepeat` | 平铺 |
| `centerSlice` | `Rect?` | `null` | 九宫格拉伸中心区 |
| `matchTextDirection` | `bool` | `false` | 是否跟随文本方向 |
| `gaplessPlayback` | `bool` | `false` | 切换图片源时是否保留旧图 |
| `filterQuality` | `FilterQuality` | `FilterQuality.low` | 滤镜质量 |
| `width` / `height` | `double?` | `null` | 显示尺寸 |
| `cacheWidth` / `cacheHeight` | `int?` | `null` | 解码目标尺寸(物理像素) |

## BoxFit 取值

| 取值 | 行为 |
| --- | --- |
| `fill` | 填满目标区域,可能变形 |
| `contain` | 完整显示,保留比例(可能留白) |
| `cover` | 填满区域,保留比例(可能裁剪) |
| `fitWidth` | 宽度填满,高度自适应 |
| `fitHeight` | 高度填满,宽度自适应 |
| `none` | 原始尺寸,居中(可能溢出) |
| `scaleDown` | 居中,超出则缩小(不放大) |

## ImageRepeat 取值

| 取值 | 行为 |
| --- | --- |
| `noRepeat` | 不平铺(默认) |
| `repeat` | 双向平铺 |
| `repeatX` | 水平平铺 |
| `repeatY` | 垂直平铺 |

## 加载状态处理

### loadingBuilder

```dart
Image.network(
  'https://example.com/photo.jpg',
  loadingBuilder: (BuildContext context, Widget child,
      ImageChunkEvent? progress) {
    if (progress == null) return child;
    return CircularProgressIndicator(
      value: progress.expectedTotalBytes != null
          ? progress.cumulativeBytesLoaded /
              progress.expectedTotalBytes!
          : null,
    );
  },
)
```

### errorBuilder

```dart
Image.network(
  'https://example.com/photo.jpg',
  errorBuilder: (BuildContext context, Object error, StackTrace? stack) {
    return Container(
      color: {color-bg-secondary},
      child: Icon(Icons.broken_image, color: {color-text-primary}),
    );
  },
)
```

## 完整示例

```dart
import 'package:flutter/material.dart';

class ImageFullSample extends StatelessWidget {
  const ImageFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Image 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. BoxFit 各种模式
          SizedBox(
            height: 120,
            child: Row(
              children: [
                _fitBox('cover', BoxFit.cover),
                const SizedBox(width: {spacing-sm}),
                _fitBox('contain', BoxFit.contain),
                const SizedBox(width: {spacing-sm}),
                _fitBox('fill', BoxFit.fill),
              ],
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 2. 圆角图片(ClipRRect)
          ClipRRect(
            borderRadius: BorderRadius.circular({radius-lg}),
            child: Image.network(
              'https://example.com/card.png',
              height: 160,
              width: double.infinity,
              fit: BoxFit.cover,
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 3. 圆形头像(ClipOval)
          ClipOval(
            child: Image.network(
              'https://example.com/avatar.png',
              width: 64, height: 64,
              fit: BoxFit.cover,
              cacheWidth: 128, // 性能:解码到 128px
            ),
          ),
          const SizedBox(height: {spacing-md}),
          // 4. 加载 + 错误 + 占位
          Image.network(
            'https://example.com/large.jpg',
            loadingBuilder: (context, child, progress) => progress == null
                ? child
                : LinearProgressIndicator(
                    value: progress.expectedTotalBytes != null
                        ? progress.cumulativeBytesLoaded /
                            progress.expectedTotalBytes!
                        : null,
                  ),
            errorBuilder: (context, error, stack) => Container(
              height: 100,
              color: {color-bg-secondary},
              alignment: Alignment.center,
              child: Text('图片加载失败',
                  style: TextStyle(color: {color-text-primary})),
            ),
          ),
        ],
      ),
    );
  }

  Widget _fitBox(String label, BoxFit fit) => Expanded(
        child: Column(
          children: [
            Expanded(
              child: Container(
                color: {color-bg-secondary},
                child: Image.network('https://example.com/p.png',
                    fit: fit),
              ),
            ),
            Text(label, style: TextStyle(fontSize: {font-size-xs})),
          ],
        ),
      );
}
```

## 注意事项

- 网络图片默认缓存上限 1000 张 / 100MB(`PaintingBinding.instance.imageCache`),可调但需谨慎
- `cacheWidth` / `cacheHeight` 是性能优化利器:解码大图时按目标尺寸解码,显著降低内存
- `color` + `colorBlendMode` 可实现图标着色(如 `BlendMode.srcIn`)
- `centerSlice` 用于九宫格拉伸(如气泡背景),要求图片有可拉伸中心区
- `gaplessPlayback: true` 在切换图片源时保留上一帧,避免闪烁
- 圆角/圆形图片推荐用 `ClipRRect` / `ClipOVal` 包裹,而非 `BoxDecoration` 内切(后者在 `fit: cover` 时易出错)
