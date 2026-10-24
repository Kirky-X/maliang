# Flutter DatePicker 属性列表与默认值

本文档汇总 `showDatePicker` / `showTimePicker` / `CalendarDatePicker` 的完整参数与回调。所有颜色默认值以 design token 形式给出。

## showDatePicker 参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `initialDate` | `DateTime` | 必填 | 初始选中日期(必须在 first/last 之间) |
| `firstDate` | `DateTime` | 必填 | 可选最早日期 |
| `lastDate` | `DateTime` | 必填 | 可选最晚日期 |
| `initialDatePickerMode` | `DatePickerMode` | `day` | `day` 日历 / `year` 年份 |
| `initialEntryMode` | `DatePickerEntryMode` | `calendar` | calendar / input / calendarOnly / inputOnly |
| `selectableDayPredicate` | `SelectableDayPredicate?` | `null` | 逐日判定可选(禁选周末等) |
| `helpText` | `String?` | 取本地化 | 对话框标题文案 |
| `cancelText` / `confirmText` | `String?` | 取本地化 | 按钮文案 |
| `errorFormatText` / `errorInvalidText` | `String?` | 取本地化 | 错误提示文案 |
| `fieldHintText` / `fieldLabelText` | `String?` | 取本地化 | input 模式输入框文案 |
| `currentDate` | `DateTime` | `DateTime.now()` | "今天"标记 |
| `builder` | `TransitionBuilder?` | `null` | 注入 Theme/Locale |
| `useRootNavigator` | `bool` | `true` | 根导航器弹出 |

## showTimePicker 参数(增量)

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `initialTime` | `TimeOfDay` | 必填 | 初始时间 |
| `initialEntryMode` | `TimePickerEntryMode` | `dial` | `dial` 时钟拨盘 / `input` 键入 |
| `use24HourFormat` | — | 取平台 | 24 小时制(经 builder MediaQuery 覆写) |
| `helpText` / `cancelText` / `confirmText` | `String?` | 取本地化 | 文案 |

## CalendarDatePicker 参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `initialDate` | `DateTime` | 必填 | 初始选中 |
| `firstDate` / `lastDate` | `DateTime` | 必填 | 可选范围 |
| `onDateChanged` | `ValueChanged<DateTime>` | 必填 | 选中变化(实时) |
| `onDisplayedMonthChanged` | `ValueChanged<DateTime>` | `null` | 翻页回调 |
| `initialCalendarMode` | `DatePickerMode` | `day` | day / year |
| `selectableDayPredicate` | `SelectableDayPredicate?` | `null` | 逐日可选判定 |

## 返回值与状态

| API | 返回 | 取消时 |
| --- | --- | --- |
| `showDatePicker` | `Future<DateTime?>` | `null` |
| `showDateRangePicker` | `Future<DateTimeRange?>` | `null` |
| `showTimePicker` | `Future<TimeOfDay?>` | `null` |

## 完整示例

```dart
import 'package:flutter/material.dart';

class DatePickerFullSample extends StatefulWidget {
  const DatePickerFullSample({super.key});

  @override
  State<DatePickerFullSample> createState() => _DatePickerFullSampleState();
}

class _DatePickerFullSampleState extends State<DatePickerFullSample> {
  DateTimeRange? _range;
  TimeOfDay? _reminder;

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all({spacing-md}),
      children: [
        ListTile(
          leading: const Icon(Icons.date_range),
          title: Text(_range == null
              ? '选择入住区间'
              : '${_range!.start.month}/${_range!.start.day} - ${_range!.end.month}/${_range!.end.day}'),
          trailing: const Icon(Icons.chevron_right),
          onTap: () async {
            final r = await showDateRangePicker(
              context: context,
              firstDate: DateTime.now(),
              lastDate: DateTime(2030),
              helpText: '选择入住与离店日期',
            );
            if (r != null) setState(() => _range = r);
          },
        ),
        ListTile(
          leading: const Icon(Icons.alarm),
          title: Text(_reminder == null ? '提醒时间' : _reminder!.format(context)),
          trailing: const Icon(Icons.chevron_right),
          onTap: () async {
            final t = await showTimePicker(
              context: context,
              initialTime: TimeOfDay.now(),
              helpText: '选择提醒时间',
            );
            if (t != null) setState(() => _reminder = t);
          },
        ),
      ],
    );
  }
}
```

## 注意事项

- `initialDate` 越界(first/last 之外)会断言崩溃,先 clamp 再传入。
- `initialDate`/`lastDate` 在 Flutter 3.13+ 已标 `canUpdate` 弃用告警的 `initialDatePickerMode` 组合注意写法;新代码统一走 `initialDatePickerMode`。
- 返回 `null` 表示用户取消,**必须判空**再更新状态。
- 主题经 `builder` 注入,保证对话框配色与暗色模式、token 体系一致。
- 无障碍:对话框自动焦点管理;触发器用 `ListTile`/`InputDecorator` 提供 label 语义,选中值对读屏完整播报。
- 语义分工:选值用本类对话框;浏览型日程用 calendar 类,不混用。

## DatePickerDialog 属性

继承自 `Dialog`,包含 `CalendarDatePicker` 全部参数,并增加:

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `initialEntryMode` | `DatePickerEntryMode` | `DatePickerEntryMode.calendar` | 入口模式(`calendar` / `calendarOnly` / `input` / `inputOnly`) |
| `cancelText` | `String?` | `null`(默认"取消") | 取消按钮文字 |
| `confirmText` | `String?` | `null`(默认"确认") | 确认按钮文字 |
| `helpText` | `String?` | `null` | 帮助文字(标题旁) |
| `errorFormatText` | `String?` | `null` | 格式错误文字 |
| `errorInvalidText` | `String?` | `null` | 无效错误文字 |
| `fieldHintText` | `String?` | `null` | 输入框提示 |
| `fieldLabelText` | `String?` | `null` | 输入框标签 |
| `restorationId` | `String?` | `null` | 状态恢复 ID |

## showDateRangePicker 函数参数

| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `context` | `BuildContext` | 必填 | 上下文 |
| `initialDateRange` | `DateTimeRange?` | `null` | 初始范围 |
| `firstDate` | `DateTime` | 必填 | 最早日期 |
| `lastDate` | `DateTime` | 必填 | 最晚日期 |
| `currentDate` | `DateTime?` | `DateTime.now()` | 当前日期 |
| `helpText` | `String?` | `null` | 帮助文字 |
| `cancelText` | `String?` | `null` | 取消按钮 |
| `confirmText` | `String?` | `null` | 确认按钮 |
| `saveText` | `String?` | `null` | 保存按钮 |
| `errorFormatText` | `String?` | `null` | 格式错误 |
| `errorInvalidText` | `String?` | `null` | 无效错误 |
| `errorInvalidRangeText` | `String?` | `null` | 范围错误 |
| `fieldStartHintText` | `String?` | `null` | 起始输入框提示 |
| `fieldEndHintText` | `String?` | `null` | 结束输入框提示 |
| `fieldStartLabelText` | `String?` | `null` | 起始输入框标签 |
| `fieldEndLabelText` | `String?` | `null` | 结束输入框标签 |
| `initialEntryMode` | `DatePickerEntryMode` | `calendar` | 入口模式 |
| `locale` | `Locale?` | `null` | 区域 |
| `useRootNavigator` | `bool` | `true` | 是否使用根 Navigator |
| `builder` | `TransitionBuilder?` | `null` | 主题定制构建器 |

## DatePickerThemeData 属性

通过 `ThemeData.datePickerTheme` 注入主题级样式。

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `backgroundColor` | `Color?` | `{color-surface}` | 背景色 |
| `surfaceTintColor` | `Color?` | `{color-surface-variant}` | M3 表面染色 |
| `shadowColor` | `Color?` | `{color-shadow}` | 阴影色 |
| `elevation` | `double?` | `6.0` | 高度 |
| `shape` | `ShapeBorder?` | `RoundedRectangleBorder(borderRadius: 28)` | 形状 |
| `headerBackgroundColor` | `Color?` | `{color-surface-variant}` | 头部背景 |
| `headerForegroundColor` | `Color?` | `{color-on-surface}` | 头部前景 |
| `headerHeadlineStyle` | `TextStyle?` | `{font-size-lg}` | 头部标题样式 |
| `headerHelpStyle` | `TextStyle?` | `{font-size-sm}` | 头部帮助样式 |
| `weekdayStyle` | `TextStyle?` | `{font-size-sm}` / `{color-on-surface-variant}` | 星期样式 |
| `dayStyle` | `TextStyle?` | `{font-size-md}` | 日期样式 |
| `dayForegroundColor` | `MaterialStateProperty<Color?>?` | 见下表 | 日期前景色 |
| `dayBackgroundColor` | `MaterialStateProperty<Color?>?` | 见下表 | 日期背景色 |
| `dayOverlayColor` | `MaterialStateProperty<Color?>?` | `{color-on-surface}` 12% | 日期叠加色 |
| `dayShape` | `MaterialStateProperty<OutlinedBorder?>?` | `CircleBorder` | 日期形状 |
| `todayForegroundColor` | `MaterialStateProperty<Color?>?` | `{color-primary}` | 今天前景 |
| `todayBackgroundColor` | `MaterialStateProperty<Color?>?` | 透明 | 今天背景 |
| `todayBorder` | `BorderSide?` | `{color-outline}` 1px | 今天边框 |
| `yearStyle` | `TextStyle?` | `{font-size-md}` | 年份样式 |
| `yearForegroundColor` | `MaterialStateProperty<Color?>?` | 见下表 | 年份前景 |
| `yearBackgroundColor` | `MaterialStateProperty<Color?>?` | 见下表 | 年份背景 |
| `yearOverlayColor` | `MaterialStateProperty<Color?>?` | `{color-on-surface}` 12% | 年份叠加 |
| `rangePickerBackgroundColor` | `Color?` | `{color-surface}` | 范围选择背景 |
| `rangePickerElevation` | `double?` | `6.0` | 范围选择高度 |
| `rangePickerShadowColor` | `Color?` | `{color-shadow}` | 范围选择阴影 |
| `rangePickerShape` | `ShapeBorder?` | 同 `shape` | 范围选择形状 |
| `rangeSelectionBackgroundColor` | `Color?` | `{color-primary-container}` | 范围选中背景 |
| `rangeSelectionOverlayColor` | `MaterialStateProperty<Color?>?` | `{color-on-surface}` 12% | 范围选中叠加 |
| `dividerColor` | `Color?` | `{color-outline-variant}` | 分隔线 |

## MaterialState 状态映射(dayForegroundColor / dayBackgroundColor)

| 状态 | dayForegroundColor | dayBackgroundColor |
| --- | --- | --- |
| `selected` | `{color-on-primary}` | `{color-primary}` |
| `disabled` | `{color-on-surface}` 38% | 透明 |
| `hovered` | 同 default | `{color-on-surface}` 8% |
| `focused` | 同 default | `{color-on-surface}` 12% |
| `pressed` | 同 default | `{color-on-surface}` 12% |
| default | `{color-on-surface}` | 透明 |

