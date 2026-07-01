# Flutter Skeleton 属性列表与默认值

> **本框架无原生 Skeleton Widget,以下为替代方案的属性汇总。**

## 占位说明

Flutter 不存在 `Skeleton` 类。本文档汇总替代实现(`shimmer` 包 / 自定义 `SkeletonBox`)的关键属性,供设计 token 映射参考。

## 替代方案 1:shimmer 包

`shimmer` 包(https://pub.flutter-io.cn/packages/shimmer)提供 `Shimmer` / `Shimmer.fromColors`:

### Shimmer.fromColors 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget` | 必填 | 包裹的子节点(通常为灰色 Container) |
| `baseColor` | `Color` | 必填 | 基础色(骨架静态色) |
| `highlightColor` | `Color` | 必填 | 高亮色(动画扫光色) |
| `period` | `Duration` | `Duration(milliseconds: 1500)` | 动画周期 |
| `direction` | `ShimmerDirection` | `ShimmerDirection.ltr` | 扫光方向(`ltr` / `rtl` / `ttb` / `btt`) |
| `loop` | `int` | `0`(无限循环) | 循环次数(0 表示无限) |

### Shimmer(渐变版)属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget` | 必填 | 子节点 |
| `gradient` | `Gradient` | 必填 | 渐变(包含 base 与 highlight) |
| `direction` | `ShimmerDirection` | `ShimmerDirection.ltr` | 扫光方向 |
| `period` | `Duration` | `Duration(milliseconds: 1500)` | 动画周期 |
| `loop` | `int` | `0` | 循环次数 |

## 替代方案 2:自定义 SkeletonBox 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `width` | `double` | `double.infinity` | 占位宽度 |
| `height` | `double` | `{size-sm}` | 占位高度 |
| `borderRadius` | `Radius` | `Radius.circular({radius-sm})` | 圆角 |
| `baseColor` | `Color` | `{color-surface-variant}` | 基础色 |
| `highlightColor` | `Color` | `{color-surface}` | 高亮色 |
| `duration` | `Duration` | `Duration(milliseconds: 1000)` | 动画时长 |

## 替代方案 3:FadeInImage(图片占位)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `placeholder` | `ImageProvider` | 必填 | 占位图(可用 `AssetImage`) |
| `image` | `ImageProvider` | 必填 | 实际图片 |
| `fadeInDuration` | `Duration` | `Duration(milliseconds: 500)` | 渐入时长 |
| `fadeOutDuration` | `Duration` | `Duration(milliseconds: 1000)` | 渐出时长 |
| `fit` | `BoxFit?` | `null` | 适配方式 |
| `width` / `height` | `double?` | `null` | 尺寸 |

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 骨架基础色 | `{color-surface-variant}` |
| 骨架高亮色 | `{color-surface}` |
| 文本骨架高度 | `{size-sm}` |
| 标题骨架高度 | `{size-md}` |
| 头像骨架尺寸 | `{size-lg}` |
| 骨架圆角 | `{radius-sm}` / `{radius-full}`(圆形) |
| 骨架间距 | `{spacing-sm}` |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- pub.dev - shimmer: https://pub.flutter-io.cn/packages/shimmer
- API 参考 - AnimatedBuilder: https://api.flutter.dev/flutter/widgets/AnimatedBuilder-class.html
- API 参考 - FadeInImage: https://api.flutter.dev/flutter/widgets/FadeInImage-class.html
