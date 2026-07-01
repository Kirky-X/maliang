# Flutter Loading 属性列表与默认值

本文档汇总 Material Design 3 加载指示器(`CircularProgressIndicator` / `LinearProgressIndicator` / `RefreshProgressIndicator`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## ProgressIndicator 基类属性

`CircularProgressIndicator` 与 `LinearProgressIndicator` 共同继承自 `ProgressIndicator`。

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `value` | `double?` | `null`(indeterminate) | 进度值 0.0~1.0;`null` 表示无限旋转加载态 |
| `backgroundColor` | `Color?` | `{color-surface-variant}` | 背景轨道色(M3 推荐使用 `trackColor`) |
| `valueColor` | `Animation<Color?>?` | `{color-primary}` | 前景指示色,通过 `AlwaysStoppedAnimation<Color>(token)` 提供 |
| `semanticsLabel` | `String?` | `null` | 无障碍标签 |
| `semanticsValue` | `String?` | `null` | 无障碍进度值文本 |

## CircularProgressIndicator 特有属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `strokeWidth` | `double` | `4.0` | 描边线宽 |
| `strokeAlign` | `double` | `0.0`(center) | 描边对齐(`-1` 内、`0` 中、`1` 外) |
| `strokeCap` | `StrokeCap?` | `StrokeCap.round` | 描边端点形状 |
| `trackColor` | `Color?` | `{color-surface-variant}` | 轨道色(M3 替代 `backgroundColor`) |
| `strokeGap` | `double?` | `null`(M3 默认 3.0) | 描边间隙(显示进度时使用) |
| `borderRadius` | `BorderRadius?` | `null` | 圆角(M3 新增) |
| `constraints` | `BoxConstraints` | `BoxConstraints.tightFor(Size(36, 36))` | 尺寸约束 |

## LinearProgressIndicator 特有属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `minHeight` | `double` | `4.0` | 最小高度(也是默认高度) |
| `borderRadius` | `BorderRadius?` | `BorderRadius.all(Radius.circular(2))` | 圆角(M3 新增) |
| `trackColor` | `Color?` | `{color-surface-variant}` | 轨道色 |
| `strokeAlign` | `double` | `0.0` | 描边对齐 |
| `strokeCap` | `StrokeCap?` | `null` | 描边端点形状 |

## RefreshProgressIndicator 特有属性

继承自 `CircularProgressIndicator`,主要用于 `RefreshIndicator`。

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `backgroundColor` | `Color?` | `{color-surface}` | 背景 |
| `valueColor` | `Animation<Color?>?` | `{color-primary}` | 前景色 |
| `strokeWidth` | `double` | `2.5` | 线宽 |
| `semanticsLabel` | `String?` | 自动 | 无障碍标签 |

## Determinate vs Indeterminate 行为差异

| 行为 | `value` 取值 | 显示效果 |
| --- | --- | --- |
| Determinate(确定进度) | `0.0 ~ 1.0` | 静态显示对应比例,无旋转动画 |
| Indeterminate(加载态) | `null` | 圆形旋转动画 / 线性来回滑动动画 |
| 完成态 | `1.0` | 静态填满,无旋转动画 |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Loading 完整示例:展示 indeterminate/determinate/刷新三种加载
class LoadingFullSample extends StatefulWidget {
  const LoadingFullSample({super.key});

  @override
  State<LoadingFullSample> createState() => _LoadingFullSampleState();
}

class _LoadingFullSampleState extends State<LoadingFullSample> {
  double _progress = 0.0;
  bool _isLoading = false;

  void _startProgress() {
    setState(() {
      _progress = 0.0;
      _isLoading = true;
    });
    Future.delayed(const Duration(milliseconds: 100), () {
      _tick();
    });
  }

  void _tick() {
    if (!mounted) return;
    setState(() => _progress += 0.1);
    if (_progress < 1.0) {
      Future.delayed(const Duration(milliseconds: 300), _tick);
    } else {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Loading 完整示例')),
      body: RefreshIndicator(
        onRefresh: () async {
          await Future.delayed(const Duration(seconds: 2));
        },
        child: ListView(
          padding: EdgeInsets.all({spacing-md}),
          children: [
            // 1. Indeterminate 圆形
            const Center(
              child: CircularProgressIndicator(
                strokeWidth: {stroke-width-sm},
                strokeCap: StrokeCap.round,
                backgroundColor: {color-surface-variant},
                valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
              ),
            ),
            SizedBox(height: {spacing-lg}),
            // 2. Determinate 圆形
            Center(
              child: CircularProgressIndicator(
                value: _progress,
                strokeWidth: {stroke-width-sm},
                strokeCap: StrokeCap.round,
                backgroundColor: {color-surface-variant},
                valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
                semanticsLabel: '进度 ${(_progress * 100).round()}%',
                semanticsValue: '${(_progress * 100).round()}%',
              ),
            ),
            SizedBox(height: {spacing-lg}),
            // 3. Indeterminate 线性
            const LinearProgressIndicator(
              minHeight: {size-xs},
              borderRadius: BorderRadius.all(Radius.circular({radius-full})),
              backgroundColor: {color-surface-variant},
              valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
            ),
            SizedBox(height: {spacing-md}),
            // 4. Determinate 线性
            LinearProgressIndicator(
              value: _progress,
              minHeight: {size-xs},
              borderRadius: const BorderRadius.all(Radius.circular({radius-full})),
              backgroundColor: {color-surface-variant},
              valueColor: AlwaysStoppedAnimation<Color>({color-primary}),
            ),
            SizedBox(height: {spacing-md}),
            // 5. 操作按钮
            FilledButton(
              onPressed: _isLoading ? null : _startProgress,
              child: Text(_isLoading ? '加载中...' : '开始加载'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 主题层配置(Design Token 解析点)

在 `ThemeData` 中通过 `progressIndicatorTheme` 注入主题级样式:

```dart
ThemeData(
  progressIndicatorTheme: ProgressIndicatorThemeData(
    color: {color-primary},
    linearTrackColor: {color-surface-variant},
    circularTrackColor: {color-surface-variant},
    linearMinHeight: {size-xs},
    borderWidth: {stroke-width-sm},
    strokeAlign: 0,
    strokeCap: StrokeCap.round,
    borderRadius: BorderRadius.all(Radius.circular({radius-full})),
    constraints: BoxConstraints.tightFor(Size({size-md}, {size-md})),
  ),
)
```

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - CircularProgressIndicator: https://api.flutter.dev/flutter/material/CircularProgressIndicator-class.html
- API 参考 - LinearProgressIndicator: https://api.flutter.dev/flutter/material/LinearProgressIndicator-class.html
- API 参考 - RefreshProgressIndicator: https://api.flutter.dev/flutter/material/RefreshProgressIndicator-class.html
- API 参考 - ProgressIndicator: https://api.flutter.dev/flutter/material/ProgressIndicator-class.html
- API 参考 - ProgressIndicatorThemeData: https://api.flutter.dev/flutter/material/ProgressIndicatorThemeData-class.html
