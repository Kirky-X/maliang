# Flutter Steps Widget 定义

## Widget 定义

Flutter Material Design 3 提供 `Stepper` Widget,用于展示分步骤流程(如注册、下单、向导)。每个步骤由 `Step` 表示,包含标题、副标题、内容、状态。

| Steps 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| Stepper | `Stepper` | `StatefulWidget` | 分步骤流程容器 |
| Step | `Step` | - | 单个步骤(标题+内容+状态) |

> `Stepper` 默认竖向布局,可通过 `type: StepperType.horizontal` 切换为横向。每步含 `index`(序号圆圈)、`title`、`subtitle`、`content`,并通过 `StepState` 控制视觉状态。

## 构造函数

### Stepper

```dart
Stepper({
  super.key,
  required this.steps,                 // 步骤列表(List<Step>)
  this.physics,                       // 滚动物理
  this.type = StepperType.vertical,   // 类型(vertical / horizontal)
  this.currentStep = 0,               // 当前步骤索引
  this.onStepTapped,                  // 点击步骤回调
  this.onStepContinue,                // 继续按钮回调
  this.onStepCancel,                  // 取消按钮回调
  this.controlsBuilder,               // 自定义按钮构建器
  this.margin,                        // 外边距
  this.connectorColor,                // 连接线颜色(M3 新增)
  this.numberColor,                   // 圆圈数字颜色(M3 新增)
})
```

### Step

```dart
const Step({
  required this.title,                // 标题
  this.subtitle,                      // 副标题
  required this.content,              // 内容
  this.state = StepState.indexed,     // 状态(indexed/editing/complete/disabled/error)
  this.isActive = false,              // 是否当前激活
})
```

## 核心属性(Stepper)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `steps` | `List<Step>` | 步骤列表 |
| `currentStep` | `int` | 当前步骤索引(默认 0) |
| `type` | `StepperType` | 类型(`vertical` / `horizontal`) |
| `onStepTapped` | `ValueChanged<int>?` | 点击步骤回调 |
| `onStepContinue` | `VoidCallback?` | 继续按钮回调 |
| `onStepCancel` | `VoidCallback?` | 取消按钮回调 |
| `controlsBuilder` | `ControlsWidgetBuilder?` | 自定义按钮构建器 |
| `physics` | `ScrollPhysics?` | 滚动物理 |
| `connectorColor` | `Color?` | 连接线颜色(M3) |
| `numberColor` | `Color?` | 圆圈数字颜色(M3) |

## StepState 取值

| 取值 | 圆圈显示 | 用途 |
| --- | --- | --- |
| `StepState.indexed` | 数字 | 默认(未开始) |
| `StepState.editing` | 铅笔图标 | 编辑中 |
| `StepState.complete` | 勾选图标 | 已完成 |
| `StepState.disabled` | 数字(灰色) | 禁用 |
| `StepState.error` | 警告图标 | 错误 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Steps 最小示例:展示垂直 Stepper
class StepsSample extends StatefulWidget {
  const StepsSample({super.key});

  @override
  State<StepsSample> createState() => _StepsSampleState();
}

class _StepsSampleState extends State<StepsSample> {
  int _current = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Steps 示例')),
      body: Stepper(
        currentStep: _current,
        onStepContinue: () {
          setState(() {
            if (_current < 2) _current++;
          });
        },
        onStepCancel: () {
          setState(() {
            if (_current > 0) _current--;
          });
        },
        onStepTapped: (i) => setState(() => _current = i),
        steps: const [
          Step(title: Text('填写信息'), content: Text('请填写注册信息')),
          Step(title: Text('验证邮箱'), content: Text('请验证您的邮箱')),
          Step(title: Text('完成注册'), content: Text('注册成功!')),
        ],
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
Stepper(
  type: StepperType.horizontal,
  currentStep: _current,
  connectorColor: {color-outline-variant},
  numberColor: {color-on-primary},
  controlsBuilder: (context, details) {
    return Row(
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
          child: Text(details.stepIndex == 2 ? '完成' : '继续'),
        ),
        SizedBox(width: {spacing-sm}),
        TextButton(
          onPressed: details.onStepCancel,
          child: Text(
            '返回',
            style: TextStyle(color: {color-text-secondary}),
          ),
        ),
      ],
    );
  },
  onStepContinue: () => setState(() {
    if (_current < 2) _current++;
  }),
  onStepCancel: () => setState(() {
    if (_current > 0) _current--;
  }),
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
      content: const Text('请验证邮箱'),
      state: _current > 1
          ? StepState.complete
          : _current == 1
              ? StepState.editing
              : StepState.indexed,
      isActive: _current >= 1,
    ),
    Step(
      title: Text('步骤 3'),
      content: const Text('注册成功!'),
      state: _current > 2 ? StepState.complete : StepState.indexed,
      isActive: _current >= 2,
    ),
  ],
)
```

> 注:示例中的 `{color-primary}`、`{color-on-primary}`、`{color-text-primary}`、`{color-text-secondary}`、`{color-text-tertiary}`、`{color-outline-variant}`、`{spacing-sm}`、`{spacing-md}`、`{font-size-md}`、`{font-size-sm}`、`{radius-md}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Stepper: https://api.flutter.dev/flutter/material/Stepper-class.html
- API 参考 - Step: https://api.flutter.dev/flutter/material/Step-class.html
- API 参考 - StepState: https://api.flutter.dev/flutter/material/StepState.html
- API 参考 - StepperType: https://api.flutter.dev/flutter/material/StepperType.html
