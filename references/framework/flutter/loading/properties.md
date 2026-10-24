# Flutter Loading 属性列表与默认值

> 参数唯一真源见 [progress](../progress/properties.md)(CircularProgressIndicator / Linear / Refresh 全部属性);本文件只保留加载场景的基类 token 默认值与行为差异,不复述特有属性表(防双份漂移)。

本文档汇总 Material Design 3 加载指示器(`CircularProgressIndicator` / `LinearProgressIndicator` / `RefreshProgressIndicator`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## ProgressIndicator 基类属性

`CircularProgressIndicator` 与 `LinearProgressIndicator` 共同继承自 `ProgressIndicator`。

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `value` | `double?` | `null`(indeterminate) | 进度值 0.0~1.0;`null` 表示无限旋转加载态 |
| `backgroundColor` | `Color?` | `{color-surface-variant}` | 背景轨道色 |
| `valueColor` | `Animation<Color?>?` | `{color-primary}` | 前景指示色,通过 `AlwaysStoppedAnimation<Color>(token)` 提供 |
| `semanticsLabel` | `String?` | `null` | 无障碍标签 |
| `semanticsValue` | `String?` | `null` | 无障碍进度值文本 |

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

