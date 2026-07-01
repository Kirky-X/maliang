# Flutter Calendar 属性列表与默认值

本文档汇总 Material Design 3 日历(`CalendarDatePicker` / `DatePickerDialog` / `showDatePicker` / `showDateRangePicker`)的完整属性与默认值。所有颜色默认值以 design token 形式给出。

## CalendarDatePicker 属性

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `initialDate` | `DateTime` | 必填 | 初始选中日期 |
| `firstDate` | `DateTime` | 必填 | 可选最早日期 |
| `lastDate` | `DateTime` | 必填 | 可选最晚日期 |
| `currentDate` | `DateTime?` | `DateTime.now()` | 当前日期(高亮"今天") |
| `onDateChanged` | `ValueChanged<DateTime>?` | `null` | 选择回调 |
| `onDisplayedMonthChanged` | `ValueChanged<DateTime>?` | `null` | 显示月份变化 |
| `initialCalendarMode` | `DatePickerMode` | `DatePickerMode.day` | 初始模式(`day` / `year`) |
| `selectableDayPredicate` | `SelectableDayPredicate?` | `null` | 自定义可选日期判断 |
| `calendarStyle` | `CalendarDatePickerStyles?` | `null` | 日历样式 |
| `keyboardSwitchButtonFocusNode` | `FocusNode?` | `null` | 键盘切换按钮焦点 |

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

## showDatePicker 函数参数

| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `context` | `BuildContext` | 必填 | 上下文 |
| `initialDate` | `DateTime` | 必填 | 初始日期 |
| `firstDate` | `DateTime` | 必填 | 最早日期 |
| `lastDate` | `DateTime` | 必填 | 最晚日期 |
| `currentDate` | `DateTime?` | `DateTime.now()` | 当前日期 |
| `initialEntryMode` | `DatePickerEntryMode` | `calendar` | 入口模式 |
| `selectableDayPredicate` | `SelectableDayPredicate?` | `null` | 可选日期判断 |
| `helpText` | `String?` | `null` | 帮助文字 |
| `cancelText` | `String?` | `null` | 取消按钮 |
| `confirmText` | `String?` | `null` | 确认按钮 |
| `locale` | `Locale?` | `null` | 区域 |
| `useRootNavigator` | `bool` | `true` | 是否使用根 Navigator |
| `routeSettings` | `RouteSettings?` | `null` | 路由设置 |
| `textDirection` | `TextDirection?` | `null` | 文本方向 |
| `initialCalendarMode` | `DatePickerMode` | `day` | 初始模式 |
| `onDatePickerModeChange` | `ValueChanged<DatePickerEntryMode>?` | `null` | 模式变化回调 |
| `errorInvalidDateHandler` | `ErrorInvalidDateHandler?` | `null` | 错误处理器 |
| `builder` | `TransitionBuilder?` | `null` | 主题定制构建器 |

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

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - CalendarDatePicker: https://api.flutter.dev/flutter/material/CalendarDatePicker-class.html
- API 参考 - showDatePicker: https://api.flutter.dev/flutter/material/showDatePicker.html
- API 参考 - showDateRangePicker: https://api.flutter.dev/flutter/material/showDateRangePicker.html
- API 参考 - DatePickerDialog: https://api.flutter.dev/flutter/material/DatePickerDialog-class.html
- API 参考 - DatePickerThemeData: https://api.flutter.dev/flutter/material/DatePickerThemeData-class.html
