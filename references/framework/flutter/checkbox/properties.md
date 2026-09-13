# Flutter Checkbox 属性列表与默认值

本文档汇总 `Checkbox` 与 `CheckboxListTile` 的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## Checkbox 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `bool?` | 必填 | 选中态;`tristate` 时 `null` = 半选 |
| `onChanged` | `ValueChanged<bool?>?` | 必填 | 变化回调;`null` 时禁用 |
| `tristate` | `bool` | `false` | 三态开关(选中/未选/半选循环) |
| `activeColor` | `Color?` | `null`(取主题) | 选中态填充色 |
| `fillColor` | `MaterialStateProperty<Color?>?` | `null` | 填充色(支持状态) |
| `checkColor` | `Color?` | `null`(取主题) | 对勾颜色 |
| `focusColor` | `Color?` | `null` | 聚焦色 |
| `hoverColor` | `Color?` | `null` | 悬停色 |
| `overlayColor` | `Color?` | `null` | 按压叠加色 |
| `splashRadius` | `double?` | `null`(默认 20.0) | 水波纹半径 |
| `materialTapTargetSize` | `MaterialTapTargetSize?` | `null`(取主题) | 点击目标尺寸 |
| `visualDensity` | `VisualDensity?` | `null`(取主题) | 视觉密度 |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |
| `shape` | `OutlinedBorder?` | `null`(M3 圆角方形) | 框形状 |
| `side` | `BorderSide?` | `null` | 未选中态边框 |
| `mouseCursor` | `MouseCursor?` | `null` | 鼠标光标 |

## CheckboxListTile 构造参数(增量)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `title` | `Widget` | 必填 | 标题 |
| `subtitle` | `Widget?` | `null` | 副标题 |
| `isThreeLine` | `bool` | `false` | 三行布局(需配合 subtitle) |
| `dense` | `bool?` | `null`(取主题) | 紧凑模式 |
| `secondary` | `Widget?` | `null` | 前置/后置 Widget |
| `selected` | `bool` | `false` | 整行高亮(选中态) |
| `controlAffinity` | `ListTileControlAffinity` | `platform` | 复选框位置 |
| `contentPadding` | `EdgeInsetsGeometry?` | `null` | 内容内边距 |
| `tileColor` | `Color?` | `null` | 列表项背景色 |

## 三态语义(MD3 / Carbon 对齐)

| value | 视觉 | 语义 |
| --- | --- | --- |
| `false` | 空框 | 未选中(unchecked) |
| `true` | 对勾填充 | 选中(checked) |
| `null`(需 `tristate: true`) | 空框内短横线 | 半选(indeterminate,子项部分选中) |

> `tristate: false` 时 `value` 只能为 `true`/`false`;传 `null` 视为未选中。半选态仅作展示,再次点击进入全选。

## MaterialState 状态(MD3)

| 状态 | 触发条件 | fillColor 建议 |
| --- | --- | --- |
| `MaterialState.selected` | `value == true` | `{color-primary}` |
| `MaterialState.disabled` | `onChanged == null` | `{color-text-disabled}` |
| `MaterialState.hovered` / `focused` / `pressed` | 交互态 | overlayColor 处理 |

## 事件回调

| 回调 | 签名 | 触发时机 |
| --- | --- | --- |
| `onChanged` | `void Function(bool?)` | 点击时触发;三态下按 false → null → true 循环(或反向) |

## 完整示例

```dart
import 'package:flutter/material.dart';

class CheckboxFullSample extends StatefulWidget {
  const CheckboxFullSample({super.key});

  @override
  State<CheckboxFullSample> createState() => _CheckboxFullSampleState();
}

class _CheckboxFullSampleState extends State<CheckboxFullSample> {
  bool? _agree = false;
  bool? _selectAll = false;
  List<bool> _rows = [false, true, false];

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all({spacing-md}),
      children: [
        CheckboxListTile(
          value: _agree,
          onChanged: (v) => setState(() => _agree = v),
          title: const Text('同意服务条款'),
          subtitle: const Text('提交前必读'),
          controlAffinity: ListTileControlAffinity.leading,
          activeColor: {color-primary},
        ),
        const Divider(),
        CheckboxListTile(
          value: _selectAll,
          tristate: true,
          onChanged: (v) => setState(() {
            _selectAll = v;
            _rows = [for (final _ in _rows) v ?? false];
          }),
          title: const Text('全选订单'),
          activeColor: {color-primary},
        ),
        for (var i = 0; i < _rows.length; i++)
          CheckboxListTile(
            value: _rows[i],
            onChanged: (v) => setState(() => _rows[i] = v ?? false),
            title: Text('订单 100${i + 1}'),
            activeColor: {color-primary},
          ),
      ],
    );
  }
}
```

## 注意事项

- `Checkbox` 是受控组件,**不要在内部维护选中态**;半选态由父级按子项勾选数推导(`null`)。
- 三态场景必须显式 `tristate: true`,否则 `null` 值不产生半选视觉。
- 点击区域默认 `materialTapTargetSize.padded`(48 × 48,满足无障碍);用 `shrinkWrap` 缩小会破坏可达性(WCAG 2.5.5)。
- 批量列表操作优先 `CheckboxListTile`:整行可点、标签可读、TalkBack 播报完整。
- 全选与子项联动须手动推导:子项全选 → `true`,部分 → `null`,全无 → `false`。
