# Flutter Layout 属性列表与默认值

本文档汇总 Flutter 布局 Widget 的属性、默认值与布局行为。颜色/尺寸默认值以 design token 形式给出。

## Row / Column 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `mainAxisAlignment` | `MainAxisAlignment` | `MainAxisAlignment.start` | 主轴对齐 |
| `mainAxisSize` | `MainAxisSize` | `MainAxisSize.max` | 主轴尺寸(max 占满/min 收缩) |
| `crossAxisAlignment` | `CrossAxisAlignment` | `CrossAxisAlignment.center` | 交叉轴对齐 |
| `textDirection` | `TextDirection?` | `null`(取 `Directionality`) | 文本方向 |
| `verticalDirection` | `VerticalDirection` | `VerticalDirection.down` | 垂直方向 |
| `textBaseline` | `TextBaseline?` | `null` | 文本基线(对齐 baseline 时必填) |
| `children` | `List<Widget>` | `const []` | 子节点 |

### MainAxisAlignment 取值

| 取值 | 行为 |
| --- | --- |
| `start` | 主轴起点对齐 |
| `center` | 居中 |
| `end` | 主轴终点对齐 |
| `spaceBetween` | 首尾贴边,中间均分 |
| `spaceAround` | 每个子节点两侧等距 |
| `spaceEvenly` | 全程均分(含两端) |

## Expanded / Flexible 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `flex` | `int` | `1` | 弹性比例 |
| `fit` | `FlexFit` | `Flexible.loose` / `Expanded.tight` | tight 强制填满,loose 不超过 |
| `child` | `Widget?` | `null` | 子节点 |

> `Expanded` 等价于 `Flexible(fit: FlexFit.tight)`。

## Stack / Positioned 属性

### Stack

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `alignment` | `AlignmentGeometry` | `AlignmentDirectional.topStart` | 默认对齐 |
| `fit` | `StackFit` | `StackFit.loose` | 子节点约束 |
| `clipBehavior` | `Clip` | `Clip.hardEdge` | 超出裁剪 |

### Positioned

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `left` / `right` / `top` / `bottom` | `double?` | `null` | 距各边距离 |
| `width` / `height` | `double?` | `null` | 固定尺寸(需与位置约束兼容) |

## Container 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `alignment` | `AlignmentGeometry?` | `null` | 子节点对齐 |
| `padding` | `EdgeInsetsGeometry?` | `null` | 内边距 |
| `color` | `Color?` | `null` | 背景色(与 decoration 互斥) |
| `decoration` | `Decoration?` | `null` | 装饰(边框/圆角/渐变) |
| `width` / `height` | `double?` | `null` | 尺寸 |
| `constraints` | `BoxConstraints?` | `null` | 约束 |
| `margin` | `EdgeInsetsGeometry?` | `null` | 外边距 |
| `transform` | `Matrix4?` | `null` | 变换矩阵 |
| `child` | `Widget?` | `null` | 子节点 |

## Padding / SizedBox / Align 属性

| Widget | 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `Padding` | `padding` | `EdgeInsetsGeometry` | 必填 | 内边距 |
| `SizedBox` | `width` / `height` | `double?` | `null` | 固定尺寸 |
| `Align` | `alignment` | `AlignmentGeometry` | `Alignment.center` | 对齐 |
| `Align` | `widthFactor` / `heightFactor` | `double?` | `null` | 尺寸因子(子节点尺寸倍数) |

## 布局约束规则(BoxConstraints)

Flutter 布局遵循"约束向下,尺寸向上"单向传递:

1. 父节点向子节点传递 `BoxConstraints(minWidth, maxWidth, minHeight, maxHeight)`
2. 子节点在约束内确定自身尺寸并返回父节点
3. 父节点据此定位子节点

常见约束 Widget:`ConstrainedBox`(min/max)、`SizedBox`(固定)、`AspectRatio`(宽高比)、`LimitedBox`(无界时限制)、`FractionallySizedBox`(比例)。

## 完整示例

```dart
import 'package:flutter/material.dart';

class LayoutFullSample extends StatelessWidget {
  const LayoutFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Layout 完整示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: Column(
          children: [
            // 1. MainAxisAlignment.spaceEvenly
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [Text('A'), Text('B'), Text('C')],
            ),
            const SizedBox(height: {spacing-md}),
            // 2. CrossAxisAlignment.stretch 让子节点撑满交叉轴
            IntrinsicHeight(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Expanded(child: Container(color: {color-primary})),
                  Expanded(flex: 2, child: Container(color: {color-bg-secondary})),
                ],
              ),
            ),
            const SizedBox(height: {spacing-md}),
            // 3. Container 装饰
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(
                horizontal: {spacing-md}, vertical: {spacing-sm}),
              decoration: BoxDecoration(
                color: {color-bg-primary},
                borderRadius: BorderRadius.circular({radius-md}),
                border: Border.all(color: {color-border-default}),
              ),
              child: Text('容器内容',
                style: TextStyle(fontSize: {font-size-md})),
            ),
            const SizedBox(height: {spacing-md}),
            // 4. Stack + Positioned 完整定位
            SizedBox(
              height: 100,
              child: Stack(
                fit: StackFit.expand,
                children: [
                  Container(color: {color-bg-secondary}),
                  Positioned(
                    left: {spacing-sm}, top: {spacing-sm},
                    child: Text('左上',
                      style: TextStyle(color: {color-text-primary})),
                  ),
                  Positioned(
                    right: {spacing-sm}, bottom: {spacing-sm},
                    child: Text('右下',
                      style: TextStyle(color: {color-text-primary})),
                  ),
                ],
              ),
            ),
            const SizedBox(height: {spacing-md}),
            // 5. Spacer 推开两侧
            Row(children: [
              const Text('左'),
              const Spacer(),
              const Text('右'),
            ]),
          ],
        ),
      ),
    );
  }
}
```

## 注意事项

- `Row` 嵌套 `Row` 或 `Column` 嵌套 `Column` 时,内层若需占满主轴需用 `Expanded` 包裹,否则抛 "RenderFlex overflowed" 异常
- `Stack` 的非 `Positioned` 子节点按 `alignment` 定位;`Positioned` 子节点需至少设置 2 个方向(水平/垂直各 1 个)
- `Container` 的 `color` 与 `decoration` 互斥,需背景色 + 边框时使用 `decoration: BoxDecoration(color: ...)`
- `SizedBox(width: double.infinity, ...)` 可让子节点撑满父级宽度
- `mainAxisSize: MainAxisSize.min` 让 Row/Column 收缩到子节点尺寸,常用于内嵌按钮行
