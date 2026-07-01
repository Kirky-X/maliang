# Flutter a11y 属性列表与默认值

本文档汇总 Flutter 无障碍体系的完整属性、默认值与配置项。所有视觉属性以 design token 形式引用,不在文档中硬编码。

## Semantics 完整属性表

### 角色属性(布尔标识)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `button` | `bool?` | `null`(不设置) | 按钮角色 |
| `link` | `bool?` | `null` | 链接角色 |
| `checkbox` | `bool?` | `null` | 复选框角色 |
| `radio` | `bool?` | `null` | 单选按钮角色 |
| `switchWidget` | `bool?` | `null` | 开关角色 |
| `slider` | `bool?` | `null` | 滑块角色 |
| `textField` | `bool?` | `null` | 文本输入角色 |
| `header` | `bool?` | `null` | 标题角色 |
| `image` | `bool?` | `null` | 图像角色 |
| `tab` | `bool?` | `null` | Tab 角色 |
| `tooltip` | `bool?` | `null` | 工具提示角色 |
| `hidden` | `bool?` | `null` | 隐藏(不播报) |

### 状态属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enabled` | `bool?` | `null`(继承) | 是否可用 |
| `checked` | `bool?` | `null` | 复选框选中态 |
| `selected` | `bool?` | `null` | 选中态(单选/Tab) |
| `toggled` | `bool?` | `null` | 开关切换态 |
| `focused` | `bool?` | `null` | 焦点态 |
| `inMutuallyExclusiveGroup` | `bool?` | `null` | 互斥组(单选) |

### 文本属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `label` | `String?` | `null` | 节点名称(主标签) |
| `value` | `String?` | `null` | 节点当前值 |
| `hint` | `String?` | `null` | 操作提示 |
| `onTapHint` | `String?` | `null` | 点击提示(覆盖 hint) |
| `onLongPressHint` | `String?` | `null` | 长按提示 |
| `textDirection` | `TextDirection?` | `null`(取上游) | 文本方向 |
| `attributedLabel` | `AttributedString?` | `null` | 带属性的标签 |

### 行为回调

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `onTap` | `VoidCallback?` | 点击 |
| `onLongPress` | `VoidCallback?` | 长按 |
| `onScrollLeft` / `onScrollRight` | `VoidCallback?` | 横向滑动 |
| `onScrollUp` / `onScrollDown` | `VoidCallback?` | 纵向滑动 |
| `onIncrease` / `onDecrease` | `VoidCallback?` | 增加/减少(滑块、调节器) |
| `onCopy` / `onCut` / `onPaste` | `VoidCallback?` | 剪贴板操作 |
| `onDismiss` | `VoidCallback?` | 滑动取消 |
| `onMoveCursorForwardByCharacter` / `onMoveCursorBackwardByCharacter` | `MoveCursorHandler?` | 光标移动 |

### 结构属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `container` | `bool` | `false` | 强制独立语义节点 |
| `explicitChildNodes` | `bool` | `false` | 保留子节点语义 |
| `excludeSemantics` | `bool` | `false` | 排除子树语义 |
| `sortKey` | `SemanticsSortKey?` | `null` | 排序键 |
| `tagForChildren` | `SemanticsTag?` | `null` | 子节点标签(用于遍历过滤) |
| `child` | `Widget?` | `null` | 子节点 |

## MediaQuery 无障碍相关属性

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `accessibleNavigation` | `bool` | 是否启用辅助导航(TalkBack 等) |
| `boldText` | `bool` | 系统粗体文本设置 |
| `disableAnimations` | `bool` | 是否禁用动画(减少动效偏好) |
| `highContrast` | `bool` | 高对比度模式 |
| `invertColors` | `bool` | 反色模式 |
| `textScaler` | `TextScaler` | 文本缩放器(替代 `textScaleFactor`) |
| `textScaleFactor` | `double`(已废弃) | 文本缩放系数(1.0 基准) |
| `platformBrightness` | `Brightness` | 系统亮度模式(light/dark) |

## TextScaler 取值

| 取值 | 说明 |
| --- | --- |
| `TextScaler.noScaling` | 不缩放(1.0) |
| `TextScaler.linear(factor)` | 线性缩放(如 `TextScaler.linear(1.5)`) |
| `TextScaler.clamp({minLinearScaleFactor, maxLinearScaleFactor})` | 带上下限的缩放 |

> 自 Flutter 3.16 起,`textScaleFactor` 已废弃,统一使用 `TextScaler`;`TextScaler.linear(2.0)` 等价于旧 `textScaleFactor: 2.0`。

## FocusTraversalGroup 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `node` | `FocusTraversalNode?` | `null` | 焦点遍历节点 |
| `policy` | `FocusTraversalPolicy` | `ReadingOrderTraversalPolicy()` | 焦点遍历策略 |
| `child` | `Widget` | 必填 | 子节点 |
| `descendantsAreFocusable` | `bool` | `true` | 子树是否可聚焦 |
| `descendantsAreTraversable` | `bool` | `true` | 子树是否可遍历 |

## FocusTraversalPolicy 子类

| 子类 | 焦点顺序 |
| --- | --- |
| `ReadingOrderTraversalPolicy` | 阅读/视觉顺序(默认) |
| `OrderedTraversalPolicy` | 显式 `sortKey` 顺序 |
| `WidgetOrderTraversalPolicy` | Widget 树顺序 |
| `TabOrderTraversalPolicy` | 按 `tabIndex` 顺序 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class A11yFullSample extends StatelessWidget {
  const A11yFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    final mediaQuery = MediaQuery.of(context);
    final textScaler = mediaQuery.textScaler;

    return FocusTraversalGroup(
      policy: const OrderedTraversalPolicy(),
      child: Scaffold(
        appBar: AppBar(title: const Text('a11y 完整示例')),
        body: Padding(
          padding: const EdgeInsets.all({spacing-md}),
          child: Column(
            children: [
              // 1. 自适应字体缩放(避免超大字体破版)
              MediaQuery(
                data: mediaQuery.copyWith(
                  textScaler: textScaler.clamp(
                    maxScaleFactor: 1.4,
                  ),
                ),
                child: const Text(
                  '响应系统字体缩放,但限制最大 1.4 倍',
                  style: TextStyle(fontSize: {font-size-md}),
                ),
              ),
              // 2. 单选组:互斥语义
              MergeSemantics(
                child: Semantics(
                  inMutuallyExclusiveGroup: true,
                  child: Row(
                    children: [
                      Radio<bool>(
                        value: true,
                        groupValue: true,
                        onChanged: (_) {},
                      ),
                      const Text('选项 A'),
                    ],
                  ),
                ),
              ),
              // 3. 图像提供 label
              Semantics(
                label: '产品示意图:展示登录界面',
                image: true,
                child: Image.network(
                  'https://example.com/product.png',
                  width: {size-md},
                  height: {size-md},
                ),
              ),
              // 4. 高对比度适配
              if (mediaQuery.highContrast)
                Container(
                  padding: const EdgeInsets.all({spacing-sm}),
                  decoration: BoxDecoration(
                    border: Border.all(color: {color-text-primary}, width: 2),
                  ),
                  child: const Text('高对比度模式已启用'),
                ),
              // 5. 减少动效适配
              if (mediaQuery.disableAnimations)
                const Text('已禁用动画')
              else
                const TweenAnimationBuilder<double>(
                  tween: Tween(begin: 0, end: 1),
                  duration: Duration(milliseconds: 300),
                  builder: (_, v, child) =>
                      Opacity(opacity: v, child: child),
                  child: Text('动效已启用'),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## 注意事项

- `Semantics` 的 `container: true` 会创建独立节点,避免与父节点合并;**不要对装饰性节点使用**,会破坏语义树结构。
- `MergeSemantics` 会合并整棵子树为单一节点;**仅用于不可分割的复合控件**(如带图标的按钮),独立可操作的子项应保留独立语义。
- iOS VoiceOver 与 Android TalkBack 对 `hint` 播报时机不同:VoiceOver 在 `label` 之后立即播报,TalkBack 在用户停留时播报;重要提示放入 `label` 而非 `hint`。
- `MediaQuery.textScaler.clamp(maxScaleFactor: 1.4)` 仅作用于子树,**不要全局 clamp**,否则会让视障用户失去放大字体的能力(违反 WCAG 1.4.4)。
- `FocusTraversalGroup` 的 `descendantsAreFocusable: false` 会移除整个子树的键盘可达性,**仅用于装饰性容器**,交互组件应保留 `true`。
- 测试时务必开启 `semanticsDebugger`:运行 `flutter run --preview-dart-2 --enable-semantics-debugging`,或在代码中包裹 `SemanticsDebugger(child: app)`。
- Web 平台 a11y 由 `Semantics` 自动生成 ARIA 标签;但 `SemanticsService.announce` 在 Web 上仅触发 `aria-live=polite`,重要变更应使用 `assertive`。
