# Flutter Steps 属性列表与默认值

本文档汇总 Material Design 3 分步骤流程(`Stepper` / `Step`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## Stepper 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `steps` | `List<Step>` | 必填 | 步骤列表 |
| `physics` | `ScrollPhysics?` | `null` | 滚动物理 |
| `type` | `StepperType` | `StepperType.vertical` | 类型(`vertical` / `horizontal`) |
| `currentStep` | `int` | `0` | 当前步骤索引 |
| `onStepTapped` | `ValueChanged<int>?` | `null` | 点击步骤回调 |
| `onStepContinue` | `VoidCallback?` | `null` | 继续按钮回调 |
| `onStepCancel` | `VoidCallback?` | `null` | 取消按钮回调 |
| `controlsBuilder` | `ControlsWidgetBuilder?` | `null` | 自定义按钮构建器 |
| `margin` | `EdgeInsetsGeometry?` | `EdgeInsets.all(24)` | 外边距 |
| `connectorColor` | `Color?` | `{color-outline-variant}` | 连接线颜色(M3 新增) |
| `numberColor` | `Color?` | `{color-on-primary}` | 圆圈数字颜色(M3 新增) |

## Step 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `title` | `Widget` | 必填 | 标题 |
| `subtitle` | `Widget?` | `null` | 副标题 |
| `content` | `Widget` | 必填 | 内容 |
| `state` | `StepState` | `StepState.indexed` | 状态 |
| `isActive` | `bool` | `false` | 是否当前激活 |

## StepState 枚举

| 取值 | 圆圈图标 | 适用场景 |
| --- | --- | --- |
| `StepState.indexed` | 数字(步骤索引+1) | 默认(未开始) |
| `StepState.editing` | `Icons.edit`(铅笔) | 当前正在编辑 |
| `StepState.complete` | `Icons.check`(勾选) | 已完成 |
| `StepState.disabled` | 数字(灰色) | 禁用 |
| `StepState.error` | `Icons.warning`(警告) | 错误 |

## StepperType 枚举

| 取值 | 布局 | 连接线方向 |
| --- | --- | --- |
| `StepperType.vertical` | 垂直(默认) | 纵向 |
| `StepperType.horizontal` | 水平 | 横向(标题下方) |

## ControlsWidgetBuilder 签名

```dart
typedef ControlsWidgetBuilder =
  Widget Function(BuildContext context, ControlsDetails details);
```

### ControlsDetails 属性

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `currentStep` | `int` | 当前步骤索引 |
| `stepIndex` | `int` | 步骤索引(同 currentStep) |
| `onStepContinue` | `VoidCallback?` | 继续回调 |
| `onStepCancel` | `VoidCallback?` | 取消回调 |

## 完整示例

```dart
import 'package:flutter/material.dart';

/// Steps 完整示例:展示自定义 controlsBuilder 与各 StepState
class StepsFullSample extends StatefulWidget {
  const StepsFullSample({super.key});

  @override
  State<StepsFullSample> createState() => _StepsFullSampleState();
}

class _StepsFullSampleState extends State<StepsFullSample> {
  int _current = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Steps 完整示例')),
      body: Stepper(
        type: StepperType.horizontal,
        currentStep: _current,
        connectorColor: {color-outline-variant},
        numberColor: {color-on-primary},
        controlsBuilder: (context, details) {
          final isLast = details.stepIndex == 2;
          return Padding(
            padding: const EdgeInsets.only(top: {spacing-md}),
            child: Row(
              children: [
                FilledButton(
                  onPressed: details.onStepContinue,
                  style: FilledButton.styleFrom(
                    backgroundColor: {color-primary},
                    foregroundColor: {color-on-primary},
                    padding: EdgeInsets.symmetric(
                      horizontal: {spacing-md},
                      vertical: {spacing-sm},
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular({radius-md}),
                    ),
                  ),
                  child: Text(isLast ? '完成' : '继续'),
                ),
                SizedBox(width: {spacing-sm}),
                if (details.stepIndex > 0)
                  TextButton(
                    onPressed: details.onStepCancel,
                    child: Text(
                      '返回',
                      style: TextStyle(color: {color-text-secondary}),
                    ),
                  ),
              ],
            ),
          );
        },
        onStepContinue: () => setState(() {
          if (_current < 2) _current++;
        }),
        onStepCancel: () => setState(() {
          if (_current > 0) _current--;
        }),
        onStepTapped: (i) => setState(() => _current = i),
        steps: [
          Step(
            title: Text(
              '步骤 1',
              style: TextStyle(
                fontSize: {font-size-md},
                fontWeight: FontWeight.w600,
                color: _current >= 0 ? {color-text-primary} : {color-text-tertiary},
              ),
            ),
            subtitle: Text(
              '填写信息',
              style: TextStyle(fontSize: {font-size-sm}, color: {color-text-secondary}),
            ),
            content: Text(
              '请填写注册信息',
              style: TextStyle(fontSize: {font-size-md}, color: {color-text-secondary}),
            ),
            state: _current > 0 ? StepState.complete : StepState.indexed,
            isActive: _current >= 0,
          ),
          Step(
            title: Text('步骤 2'),
            subtitle: const Text('验证邮箱'),
            content: const Text('请验证您的邮箱地址'),
            state: _current > 1
                ? StepState.complete
                : _current == 1
                    ? StepState.editing
                    : StepState.indexed,
            isActive: _current >= 1,
          ),
          Step(
            title: Text('步骤 3'),
            subtitle: const Text('完成注册'),
            content: const Text('恭喜!注册成功'),
            state: _current == 2 ? StepState.editing : StepState.indexed,
            isActive: _current >= 2,
          ),
        ],
      ),
    );
  }
}
```

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 当前步骤圆圈背景 | `{color-primary}` |
| 当前步骤圆圈数字 | `{color-on-primary}` |
| 已完成步骤圆圈背景 | `{color-primary}` |
| 已完成步骤圆圈图标 | `{color-on-primary}` |
| 未完成步骤圆圈背景 | `{color-surface-variant}` |
| 未完成步骤圆圈数字 | `{color-on-surface-variant}` |
| 连接线 | `{color-outline-variant}` |
| 当前步骤标题 | `{font-size-md}` / `{color-text-primary}` |
| 未完成步骤标题 | `{color-text-tertiary}` |
| 步骤副标题 | `{font-size-sm}` / `{color-text-secondary}` |
| 步骤内容 | `{font-size-md}` / `{color-text-secondary}` |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Stepper: https://api.flutter.dev/flutter/material/Stepper-class.html
- API 参考 - Step: https://api.flutter.dev/flutter/material/Step-class.html
- API 参考 - StepState: https://api.flutter.dev/flutter/material/StepState.html
- API 参考 - StepperType: https://api.flutter.dev/flutter/material/StepperType.html
