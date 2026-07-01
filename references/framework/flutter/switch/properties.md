# Flutter Switch 属性列表与默认值

本文档汇总 `Switch` / `SwitchListTile` / `CupertinoSwitch` 的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## Switch 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `bool` | 必填 | 当前开关状态 |
| `onChanged` | `ValueChanged<bool>?` | 必填 | 状态变化回调;为 `null` 时禁用 |
| `activeColor` | `Color?` | `null`(取主题) | 开启态拇指颜色(已废弃) |
| `activeTrackColor` | `Color?` | `null`(取主题) | 开启态轨道颜色(已废弃) |
| `inactiveThumbColor` | `Color?` | `null`(取主题) | 关闭态拇指颜色(已废弃) |
| `inactiveTrackColor` | `Color?` | `null`(取主题) | 关闭态轨道颜色(已废弃) |
| `activeThumbImage` | `ImageProvider?` | `null` | 开启态拇指图像 |
| `onThumbImage` | `ImageProvider?` | `null` | 开启态拇指图像(等价 activeThumbImage) |
| `inactiveThumbImage` | `ImageProvider?` | `null` | 关闭态拇指图像 |
| `thumbColor` | `MaterialStateProperty<Color?>?` | `null` | 拇指颜色(支持状态) |
| `trackColor` | `MaterialStateProperty<Color?>?` | `null` | 轨道颜色(支持状态) |
| `thumbIcon` | `MaterialStateProperty<Icon?>?` | `null` | 拇指图标(M3 新增) |
| `overlayColor` | `MaterialStateProperty<Color?>?` | `null` | 按压/悬停/聚焦叠加色 |
| `splashRadius` | `double?` | `null`(默认 24.0) | 水波纹半径 |
| `materialTapTargetSize` | `MaterialTapTargetSize?` | `null`(取主题) | 点击目标尺寸 |
| `mouseCursor` | `MouseCursor?` | `null` | 鼠标光标 |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `onFocusChange` | `ValueChanged<bool>?` | `null` | 焦点变化回调 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |
| `dragStartBehavior` | `DragStartBehavior` | `DragStartBehavior.start` | 拖拽开始时机 |

## SwitchListTile 构造参数(增量)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `title` | `Widget?` | `null` | 标题 |
| `subtitle` | `Widget?` | `null` | 副标题 |
| `isThreeLine` | `bool` | `false` | 是否三行布局 |
| `dense` | `bool?` | `null`(取主题) | 紧凑模式 |
| `secondary` | `Widget?` | `null` | 前置图标 |
| `selected` | `bool` | `false` | 整行高亮(选中态) |
| `controlAffinity` | `ListTileControlAffinity` | `ListTileControlAffinity.platform` | 开关位置 |
| `enabled` | `bool?` | `null` | 是否可用 |
| `hoverColor` | `Color?` | `null` | 悬停色 |
| `contentPadding` | `EdgeInsetsGeometry?` | `null`(取主题) | 内容内边距 |
| `shape` | `ShapeBorder?` | `null` | 形状 |
| `selectedTileColor` | `Color?` | `null` | 选中态背景色 |
| `enableFeedback` | `bool?` | `null` | 触觉反馈 |

## CupertinoSwitch 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `value` | `bool` | 必填 | 当前状态 |
| `onChanged` | `ValueChanged<bool>?` | 必填 | 状态变化回调 |
| `activeColor` | `Color?` | `null`(取主题绿) | 开启态轨道颜色 |
| `trackColor` | `Color?` | `null`(取主题灰) | 关闭态轨道颜色 |
| `thumbColor` | `Color?` | `null`(取白) | 拇指颜色 |
| `dragStartBehavior` | `DragStartBehavior` | `DragStartBehavior.start` | 拖拽开始时机 |
| `focusNode` | `FocusNode?` | `null` | 焦点节点 |
| `onFocusChange` | `ValueChanged<bool>?` | `null` | 焦点变化回调 |
| `autofocus` | `bool` | `false` | 自动获取焦点 |
| `applyTheme` | `bool` | `false` | 是否应用 Material 主题色 |

## MaterialState 状态(MD3)

`thumbColor` / `trackColor` / `overlayColor` 通过 `MaterialStateProperty` 响应:

| 状态 | 触发条件 | thumbColor MD3 默认 | trackColor MD3 默认 |
| --- | --- | --- | --- |
| `MaterialState.selected` | `value == true` | `{color-on-primary}` | `{color-primary}` |
| `MaterialState.disabled` | `onChanged == null` | `{color-text-disabled}` | `{color-bg-disabled}` |
| `MaterialState.hovered` | 鼠标悬停 | (继承) | (继承) |
| `MaterialState.focused` | 焦点获取 | (继承) | (继承) |
| `MaterialState.pressed` | 按压 | (继承) | (继承) |
| (默认) | `value == false` | `{color-surface-variant}` | `{color-bg-tertiary}` |

## thumbIcon 状态映射

| 状态 | 推荐图标 |
| --- | --- |
| `MaterialState.selected` | `Icons.check`(对勾) |
| (默认) | `Icons.close`(叉号)或 `null`(无图标) |

## MaterialTapTargetSize 取值

| 取值 | 说明 |
| --- | --- |
| `MaterialTapTargetSize.padded` | 48 × 48(MD3 默认,符合无障碍) |
| `MaterialTapTargetSize.shrinkWrap` | 紧贴视觉边界 |

## 事件回调

| 回调 | 签名 | 触发时机 |
| --- | --- | --- |
| `onChanged` | `void Function(bool)` | 用户点击/拖动改变状态 |
| `onFocusChange` | `void Function(bool)` | 焦点获取/失去 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class SwitchFullSample extends StatefulWidget {
  const SwitchFullSample({super.key});

  @override
  State<SwitchFullSample> createState() => _SwitchFullSampleState();
}

class _SwitchFullSampleState extends State<SwitchFullSample> {
  bool _notifications = true;
  bool _sounds = false;
  bool _vibration = true;
  bool _autoUpdate = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Switch 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-sm}),
        children: [
          // 1. 基础 SwitchListTile
          SwitchListTile(
            value: _notifications,
            onChanged: (v) => setState(() => _notifications = v),
            title: const Text('推送通知'),
            subtitle: const Text('接收应用通知'),
            secondary: const Icon(Icons.notifications),
            thumbColor: MaterialStateProperty.resolveWith((states) {
              if (states.contains(MaterialState.disabled)) {
                return {color-text-disabled};
              }
              return states.contains(MaterialState.selected)
                  ? {color-on-primary}
                  : {color-surface-variant};
            }),
            trackColor: MaterialStateProperty.resolveWith((states) {
              if (states.contains(MaterialState.disabled)) {
                return {color-bg-disabled};
              }
              return states.contains(MaterialState.selected)
                  ? {color-primary}
                  : {color-bg-tertiary};
            }),
          ),
          // 2. M3 thumbIcon 示例
          SwitchListTile(
            value: _sounds,
            onChanged: (v) => setState(() => _sounds = v),
            title: const Text('声音'),
            secondary: const Icon(Icons.volume_up),
            // 通过 Switch 自定义 thumbIcon 需使用 Switch 而非 SwitchListTile
          ),
          Switch(
            value: _sounds,
            onChanged: (v) => setState(() => _sounds = v),
            thumbIcon: MaterialStateProperty.resolveWith((states) {
              if (states.contains(MaterialState.selected)) {
                return const Icon(Icons.check, size: 16);
              }
              return const Icon(Icons.close, size: 16);
            }),
          ),
          const Divider(),
          // 3. 三行布局
          SwitchListTile(
            value: _vibration,
            onChanged: (v) => setState(() => _vibration = v),
            title: const Text('震动反馈'),
            subtitle: const Text('操作时震动反馈\n仅在支持震动设备上生效'),
            isThreeLine: true,
            secondary: const Icon(Icons.vibration),
            controlAffinity: ListTileControlAffinity.trailing,
          ),
          const Divider(),
          // 4. 自适应(iOS 上使用 CupertinoSwitch)
          SwitchListTile.adaptive(
            value: _autoUpdate,
            onChanged: (v) => setState(() => _autoUpdate = v),
            title: const Text('自动更新'),
            subtitle: const Text('iOS 上显示 Cupertino 风格'),
            secondary: const Icon(Icons.system_update),
          ),
          const Divider(),
          // 5. 禁用态
          const SwitchListTile(
            value: false,
            onChanged: null,
            title: Text('禁用开关'),
            subtitle: Text('onChanged 为 null 时禁用'),
            secondary: Icon(Icons.lock),
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- `Switch` 是受控组件,状态完全由 `value` 决定;不要依赖内部状态,所有变化必须通过 `onChanged` + `setState` 回写。
- `activeColor` / `activeTrackColor` / `inactiveThumbColor` / `inactiveTrackColor` 在 M3 中已废弃,优先使用 `thumbColor` + `trackColor`(支持 `MaterialStateProperty`)。
- M3 `thumbIcon` 是新特性(Flutter 3.7+),仅 Material 风格 `Switch` 支持;`CupertinoSwitch` 不支持。
- `Switch.adaptive` 在 iOS/macOS 上自动使用 `CupertinoSwitch`,其他平台使用 Material `Switch`;若需统一视觉,显式选择 `Switch` 或 `CupertinoSwitch`。
- `CupertinoSwitch` 不支持 `MaterialStateProperty`,只能用单一颜色;若需状态色,需自行用 `value` 判断。
- `SwitchListTile` 的 `selected: true` 会让整行高亮(类似选中态),与开关状态无关;仅在配合列表选择语义时使用。
- 滑动手势与 `ListView` 滑动可能冲突,`dragStartBehavior: DragStartBehavior.down` 可让滑动立即响应(默认 `start` 需达到手势阈值)。
