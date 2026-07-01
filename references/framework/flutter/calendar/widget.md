# Flutter Calendar Widget 定义

## Widget 定义

Flutter Material Design 3 提供日历选择能力,核心由 `CalendarDatePicker`(M3 网格日历)、`DatePicker`(日历对话框)、`showDatePicker`(弹出日历)组成,底层共用 `MonthController` / `YearController`。

| Calendar 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| CalendarDatePicker | `CalendarDatePicker` | `StatefulWidget` | 内嵌日历选择器(网格) |
| DatePickerDialog | `DatePickerDialog` | `StatefulWidget` | 日历对话框(配合 `showDatePicker`) |
| showDatePicker | 函数 | - | 弹出日历对话框,返回 `DateTime?` |
| showDateRangePicker | 函数 | - | 弹出日期范围选择,返回 `DateTimeRange?` |
| TableCalendar(第三方) | - | - | 完整自定义日历(需 `table_calendar` 包) |

## 构造函数

### CalendarDatePicker

```dart
CalendarDatePicker({
  super.key,
  required this.initialDate,           // 初始日期
  required this.firstDate,             // 可选最早日期
  required this.lastDate,              // 可选最晚日期
  this.currentDate,                    // 当前日期(用于高亮"今天")
  this.onDateChanged,                  // 选择回调
  this.onDisplayedMonthChanged,        // 显示月份变化回调
  this.initialCalendarMode = DatePickerMode.day,  // 初始模式(day/year)
  this.selectableDayPredicate,         // 可选日期判断函数
  this.keyboardSwitchButtonFocusNode,
  this.calendarStyle,                  // 日历样式(M3 新增)
})
```

### DatePickerDialog

```dart
DatePickerDialog({
  super.key,
  required this.initialDate,
  required this.firstDate,
  required this.lastDate,
  this.currentDate,
  this.initialEntryMode = DatePickerEntryMode.calendar,  // 入口模式
  this.selectableDayPredicate,
  this.cancelText,                     // 取消按钮文字
  this.confirmText,                    // 确认按钮文字
  this.helpText,                       // 帮助文字
  this.initialCalendarMode = DatePickerMode.day,
  this.errorFormatText,                // 格式错误文字
  this.errorInvalidText,               // 无效错误文字
  this.fieldHintText,                  // 输入框提示
  this.fieldLabelText,                 // 输入框标签
  this.keyboardSwitchButtonFocusNode,
  this.restorationId,
})
```

### showDatePicker 函数

```dart
Future<DateTime?> showDatePicker({
  required BuildContext context,
  required DateTime initialDate,
  required DateTime firstDate,
  required DateTime lastDate,
  DateTime? currentDate,
  DatePickerEntryMode initialEntryMode = DatePickerEntryMode.calendar,
  SelectableDayPredicate? selectableDayPredicate,
  String? helpText,
  String? cancelText,
  String? confirmText,
  Locale? locale,
  bool useRootNavigator = true,
  RouteSettings? routeSettings,
  TextDirection? textDirection,
  DatePickerMode initialCalendarMode = DatePickerMode.day,
  ValueChanged<DateTime>? onDatePickerModeChange,
  ErrorInvalidDateHandler? errorInvalidDateHandler,
})
```

## 核心属性(CalendarDatePicker)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `initialDate` | `DateTime` | 初始选中日期 |
| `firstDate` | `DateTime` | 可选最早日期 |
| `lastDate` | `DateTime` | 可选最晚日期 |
| `currentDate` | `DateTime?` | 当前日期(高亮"今天") |
| `onDateChanged` | `ValueChanged<DateTime>?` | 选择回调 |
| `onDisplayedMonthChanged` | `ValueChanged<DateTime>?` | 显示月份变化 |
| `initialCalendarMode` | `DatePickerMode` | 初始模式(`day` / `year`) |
| `selectableDayPredicate` | `SelectableDayPredicate?` | 自定义可选日期判断 |
| `calendarStyle` | `CalendarDatePickerStyles?` | 日历样式 |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Calendar 最小示例:展示 showDatePicker 弹出日历
class CalendarSample extends StatelessWidget {
  const CalendarSample({super.key});

  Future<void> _pickDate(BuildContext context) async {
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
    );
    if (picked != null) {
      debugPrint('选择日期: $picked');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Calendar 示例')),
      body: Center(
        child: FilledButton.icon(
          onPressed: () => _pickDate(context),
          icon: const Icon(Icons.calendar_today),
          label: const Text('选择日期'),
        ),
      ),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
showDatePicker(
  context: context,
  initialDate: DateTime.now(),
  firstDate: DateTime(2020),
  lastDate: DateTime(2030),
  helpText: '请选择日期',
  cancelText: '取消',
  confirmText: '确认',
  builder: (context, child) {
    return Theme(
      data: Theme.of(context).copyWith(
        datePickerTheme: DatePickerThemeData(
          backgroundColor: {color-surface},
          surfaceTintColor: {color-surface-variant},
          headerForegroundColor: {color-on-surface},
          headerHeadlineStyle: TextStyle(
            fontSize: {font-size-md},
            fontWeight: FontWeight.w600,
            color: {color-text-primary},
          ),
          dayForegroundColor: MaterialStateProperty.resolveWith((states) {
            if (states.contains(MaterialState.selected)) {
              return {color-on-primary};
            }
            if (states.contains(MaterialState.disabled)) {
              return {color-on-surface}.withOpacity(0.38);
            }
            return {color-on-surface};
          }),
          dayBackgroundColor: MaterialStateProperty.resolveWith((states) {
            if (states.contains(MaterialState.selected)) {
              return {color-primary};
            }
            return Colors.transparent;
          }),
          todayForegroundColor: MaterialStatePropertyAll({color-primary}),
          todayBorder: const BorderSide(color: {color-primary}, width: 1),
          yearForegroundColor: MaterialStatePropertyAll({color-on-surface}),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular({radius-lg}),
          ),
        ),
      ),
      child: child!,
    );
  },
)
```

> 注:示例中的 `{color-primary}`、`{color-on-primary}`、`{color-on-surface}`、`{color-surface}`、`{color-surface-variant}`、`{font-size-md}`、`{radius-lg}`、`{color-text-primary}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - CalendarDatePicker: https://api.flutter.dev/flutter/material/CalendarDatePicker-class.html
- API 参考 - showDatePicker: https://api.flutter.dev/flutter/material/showDatePicker.html
- API 参考 - showDateRangePicker: https://api.flutter.dev/flutter/material/showDateRangePicker.html
- API 参考 - DatePickerDialog: https://api.flutter.dev/flutter/material/DatePickerDialog-class.html
- API 参考 - DatePickerThemeData: https://api.flutter.dev/flutter/material/DatePickerThemeData-class.html
