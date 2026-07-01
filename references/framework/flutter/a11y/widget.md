# Flutter a11y Widget 定义

## Widget 定义

Flutter 提供完整的无障碍(Accessibility,简称 a11y)体系,核心由 `Semantics` Widget 与 `SemanticsConfiguration` 承载,辅助技术(屏幕阅读器、TalkBack、VoiceOver)通过语义树读取界面信息。所有交互组件均应满足 WCAG 2.1 AA 标准。

| a11y 机制 | 类 / API | 用途 |
| --- | --- | --- |
| 语义标注 | `Semantics` | Widget 注入语义属性(label/hint/value/role) |
| 合并模式 | `MergeSemantics` / `ExcludeSemantics` | 合并子树语义 / 排除子树语义 |
| 语义事件 | `SemanticsService` | 主动向辅助技术播报 |
| 文本缩放 | `MediaQuery.textScaleFactor` / `TextScaler` | 系统字体缩放 |
| 焦点导航 | `Focus` / `FocusNode` / `FocusTraversalGroup` | 键盘 / TalkBack 焦点链 |
| 可选区 | `SelectionRegistrar` / `SelectableRegion` | 全屏文本选择 |
| 高对比度 | `MediaQuery.highContrast` | 高对比度模式适配 |

> Material / Cupertino 组件内置默认语义,业务层仅需补充 `label` / `hint` / `enabled` 等业务字段。

## 构造函数

### Semantics

```dart
const Semantics({
  Key? key,
  Widget? child,
  bool container = false,
  bool explicitChildNodes = false,
  bool excludeSemantics = false,
  bool? enabled,
  bool? checked,
  bool? selected,
  bool? toggled,
  bool? button,
  bool? slider,
  bool? checkbox,
  bool? radio,
  bool? switchWidget,
  bool? textField,
  bool? link,
  bool? header,
  bool? hidden,
  String? label,
  String? value,
  String? hint,
  String? onTapHint,
  String? onLongPressHint,
  TextDirection? textDirection,
  VoidCallback? onTap,
  VoidCallback? onLongPress,
  VoidCallback? onScrollLeft,
  VoidCallback? onScrollRight,
  VoidCallback? onScrollUp,
  VoidCallback? onScrollDown,
  VoidCallback? onIncrease,
  VoidCallback? onDecrease,
  VoidCallback? onCopy,
  VoidCallback? onCut,
  VoidCallback? onPaste,
  SemanticsSortKey? sortKey,
  SemanticsTag? tagForChildren,
})
```

### MergeSemantics / ExcludeSemantics

```dart
const MergeSemantics({ Key? key, Widget? child })
const ExcludeSemantics({
  Key? key,
  Widget? child,
  bool excluding = true,
  bool? explicitChildNodes,
})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `container` | `bool` | 是否强制创建独立语义节点(默认 `false`,与子节点合并) |
| `explicitChildNodes` | `bool` | 是否保留子节点语义(覆盖合并) |
| `excludeSemantics` | `bool` | 是否排除子树语义 |
| `label` | `String?` | 节点可访问名称(屏幕阅读器播报主文) |
| `value` | `String?` | 节点当前值(如开关的"开"/"关") |
| `hint` | `String?` | 操作提示(如"双击切换") |
| `enabled` | `bool?` | 是否可用 |
| `checked` | `bool?` | 复选框选中态 |
| `selected` | `bool?` | 选中态(单选 / Tab) |
| `button` / `link` / `header` | `bool?` | 角色(语义角色) |
| `onTap` / `onLongPress` | `VoidCallback?` | 语义事件回调(辅助技术触发) |
| `sortKey` | `SemanticsSortKey?` | 节点排序键 |
| `textDirection` | `TextDirection?` | 文本方向(LTR/RTL) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// a11y 最小示例:展示语义标注、合并、排除
class A11ySample extends StatelessWidget {
  const A11ySample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('a11y 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          children: [
            // 1. 为图标按钮提供语义标签(无文本时必须)
            Semantics(
              label: '收藏',
              hint: '双击切换收藏状态',
              button: true,
              child: IconButton(
                onPressed: () {},
                icon: const Icon(Icons.favorite_border),
              ),
            ),
            // 2. 合并语义:整个卡片视为一个可点击单元
            MergeSemantics(
              child: GestureDetector(
                onTap: () {},
                child: Container(
                  padding: const EdgeInsets.all({spacing-sm}),
                  decoration: BoxDecoration(
                    color: {color-surface},
                    borderRadius: BorderRadius.circular({radius-md}),
                  ),
                  child: Row(
                    children: const [
                      Icon(Icons.person),
                      SizedBox(width: {spacing-sm}),
                      Text('用户名'),
                    ],
                  ),
                ),
              ),
            ),
            // 3. 装饰性图标:排除语义(避免噪声)
            ExcludeSemantics(
              child: Icon(
                Icons.deblur,
                color: {color-bg-secondary},
              ),
            ),
            // 4. 标题节点:header 角色
            const Semantics(
              header: true,
              child: Text('章节标题', style: TextStyle(fontSize: {font-size-lg})),
            ),
            // 5. 主动播报
            ElevatedButton(
              onPressed: () {
                SemanticsService.announce(
                  '操作已完成',
                  TextDirection.ltr,
                );
              },
              child: const Text('触发播报'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 自定义语义(MD3 主题映射)

为自定义组件(非 Material)补充语义角色,使屏幕阅读器识别为标准控件:

```dart
Semantics(
  button: true,
  enabled: true,
  label: '自定义按钮',
  onTap: _handleTap,
  child: Container(
    padding: const EdgeInsets.symmetric(
      horizontal: {spacing-md},
      vertical: {spacing-sm},
    ),
    decoration: BoxDecoration(
      color: {color-primary},
      borderRadius: BorderRadius.circular({radius-md}),
    ),
    child: Text(
      '自定义按钮',
      style: TextStyle(color: {color-on-primary}),
    ),
  ),
)
```

> 注:示例中的 `{color-primary}`、`{spacing-md}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - 无障碍: https://docs.flutter.cn/ui/accessibility
- UI 设计 & 样式: https://docs.flutter.cn/ui/accessibility/ui-design-and-styling
- 辅助技术: https://docs.flutter.cn/ui/accessibility/assistive-technologies
- 测试无障碍: https://docs.flutter.cn/ui/accessibility/accessibility-testing
- Web 无障碍: https://docs.flutter.cn/ui/accessibility/web-accessibility
- Widget 目录 - Accessibility: https://docs.flutter.cn/ui/widgets/accessibility
- API 参考 - Semantics: https://api.flutter.dev/flutter/widgets/Semantics-class.html
