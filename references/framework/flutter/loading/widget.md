# Flutter Loading Widget 定义

## Widget 定义

Flutter Material Design 3 提供"加载指示器"系列 Widget,涵盖圆形/线性进度条、旋转加载、骨架屏占位等场景。

| Loading 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 圆形进度 | `CircularProgressIndicator` | `ProgressIndicator` | 不确定/确定的圆形旋转加载 |
| 线性进度 | `LinearProgressIndicator` | `ProgressIndicator` | 顶部/底部线性进度条 |
| 刷新指示 | `RefreshProgressIndicator` | `CircularProgressIndicator` | 配合 `RefreshIndicator` 拉刷新 |
| 旋转图标 | `SpinKitRing` 等第三方 | - | 自定义动画加载(需 `flutter_spinkit` 包) |

> 与 `progress` 组件的关系:`progress` 侧重"任务进度可视化"(determinate 进度占比),`loading` 侧重"加载状态指示"(indeterminate 持续旋转)。Flutter 中两者共用同一组 Widget,通过 `value` 参数区分:`value == null` 为 indeterminate(加载态),`value` 为 0~1 时为 determinate(进度态)。

## 构造函数

### CircularProgressIndicator

```dart
const CircularProgressIndicator({
  super.key,
  super.value,                  // 0.0~1.0;为 null 表示 indeterminate(无限旋转)
  super.backgroundColor,        // 背景轨道色(M3 新增)
  super.valueColor,             // 前景指示色(AlwaysStoppedAnimation<Color>)
  super.strokeWidth,            // 线宽(M3 默认 4.0)
  super.semanticsLabel,         // 无障碍标签
  super.semanticsValue,         // 无障碍进度值
  this.strokeAlign,             // 描边对齐(M3 新增,默认 center)
  this.strokeCap,               // 描边端点形状(默认 round)
  this.trackColor,              // 轨道色(M3 替代 backgroundColor)
  this.strokeGap,               // 描边间隙(M3 新增,显示进度时使用)
  this.borderRadius,            // 圆角(M3 新增)
  this.constraints,             // 尺寸约束(默认 36x36)
})
```

### LinearProgressIndicator

```dart
const LinearProgressIndicator({
  super.key,
  super.value,                  // 0.0~1.0;为 null 表示 indeterminate
  super.backgroundColor,        // 背景轨道色
  super.valueColor,             // 前景指示色
  super.minHeight,              // 最小高度(默认 4.0)
  super.semanticsLabel,
  super.semanticsValue,
  this.borderRadius,            // 圆角(M3 新增)
  this.trackColor,
  this.strokeAlign,
  this.strokeCap,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `value` | `double?` | 进度值(0.0~1.0);`null` 表示 indeterminate |
| `valueColor` | `Animation<Color?>?` | 前景指示色,通过 `AlwaysStoppedAnimation<Color>(token)` 提供 |
| `backgroundColor` / `trackColor` | `Color?` | 背景轨道色(M3 推荐 `trackColor`) |
| `strokeWidth` | `double` | 圆形指示器线宽 |
| `minHeight` | `double` | 线性指示器高度 |
| `strokeAlign` | `double` | 描边对齐(`-1` 内、`0` 中、`1` 外) |
| `strokeCap` | `StrokeCap?` | 描边端点形状(`round` / `square` / `butt`) |
| `borderRadius` | `BorderRadius?` | 圆角(M3 新增) |
| `constraints` | `BoxConstraints` | 尺寸约束(圆形指示器) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Loading 最小示例:展示圆形与线性加载指示器
class LoadingSample extends StatelessWidget {
  const LoadingSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Loading 示例')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 1. 圆形加载(indeterminate)
            CircularProgressIndicator(
              strokeWidth: {stroke-width-sm},
              backgroundColor: {color-surface-variant},
              valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
            ),
            const SizedBox(height: {spacing-lg}),
            // 2. 圆形进度(determinate 50%)
            CircularProgressIndicator(
              value: 0.5,
              strokeWidth: {stroke-width-sm},
              backgroundColor: {color-surface-variant},
              valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
            ),
            const SizedBox(height: {spacing-lg}),
            // 3. 线性加载(indeterminate)
            LinearProgressIndicator(
              minHeight: {size-xs},
              backgroundColor: {color-surface-variant},
              valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
            ),
            const SizedBox(height: {spacing-lg}),
            // 4. 线性进度(determinate 70%)
            LinearProgressIndicator(
              value: 0.7,
              minHeight: {size-xs},
              backgroundColor: {color-surface-variant},
              valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
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
// 自定义圆形加载(配合 design token)
SizedBox(
  width: {size-md},
  height: {size-md},
  child: CircularProgressIndicator(
    value: null, // indeterminate
    strokeWidth: {stroke-width-sm},
    strokeAlign: 0,
    strokeCap: StrokeCap.round,
    borderRadius: BorderRadius.circular({radius-full}),
    backgroundColor: {color-surface-variant},
    valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
    semanticsLabel: '加载中',
  ),
)

// 自定义线性加载
LinearProgressIndicator(
  value: null,
  minHeight: {size-xs},
  borderRadius: BorderRadius.circular({radius-full}),
  backgroundColor: {color-surface-variant},
  valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
)
```

> 注:示例中的 `{color-primary}`、`{color-surface-variant}`、`{spacing-lg}`、`{size-xs}`、`{stroke-width-sm}`、`{radius-full}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - CircularProgressIndicator: https://api.flutter.dev/flutter/material/CircularProgressIndicator-class.html
- API 参考 - LinearProgressIndicator: https://api.flutter.dev/flutter/material/LinearProgressIndicator-class.html
- API 参考 - ProgressIndicator: https://api.flutter.dev/flutter/material/ProgressIndicator-class.html
