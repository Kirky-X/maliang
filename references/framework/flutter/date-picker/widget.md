# Flutter DatePicker Widget 定义

## Widget 定义

Flutter Material 的日期时间**录入**由对话框函数(`showDatePicker` / `showTimePicker`)与内嵌组件(`CalendarDatePicker` / `TimePickerSpinner` 能力经 `CupertinoDatePicker`)承担。与展示型 [`calendar`](../calendar/widget.md) 分工:选值用对话框,浏览日程才内嵌日历网格。

| DatePicker 类型 | API | 类别 | 用途 |
| --- | --- | --- | --- |
| 日期选择对话框 | `showDatePicker` | 异步函数 | 弹出 M3 日历对话框,返回 `Future<DateTime?>` |
| 日期范围对话框 | `showDateRangePicker` | 异步函数 | 区间选择(预订/筛选) |
| 时间选择对话框 | `showTimePicker` | 异步函数 | 弹出时钟拨盘,返回 `Future<TimeOfDay?>` |
| 内嵌日历选择 | `CalendarDatePicker` | StatefulWidget | 表单页内直接选择 |
| 内嵌范围选择 | `DateRangePicker` | StatefulWidget | 页面内区间选择 |
| iOS 风格 | `CupertinoDatePicker` | StatefulWidget | 滚轮式日期时间选择 |

## 核心 API

```dart
final DateTime? picked = await showDatePicker(
  context: context,
  initialDate: DateTime.now(),
  firstDate: DateTime(2020),
  lastDate: DateTime(2030),
  builder: (context, child) => Theme(data: theme, child: child!),
);

final TimeOfDay? time = await showTimePicker(
  context: context,
  initialTime: TimeOfDay.now(),
);

final DateTimeRange? range = await showDateRangePicker(
  context: context,
  firstDate: DateTime(2020),
  lastDate: DateTime(2030),
);
```

## 核心参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `initialDate` / `initialTime` | `DateTime` / `TimeOfDay` | 初始选中值 |
| `firstDate` / `lastDate` | `DateTime` | 可选范围(范围外禁选) |
| `initialEntryMode` | `DatePickerEntryMode` | calendar(日历)/ input(键入) |
| `helpText` / `cancelText` / `confirmText` | `String?` | 对话框文案 |
| `builder` | `TransitionBuilder` | 注入主题/本地化 |
| `useRootNavigator` | `bool` | 是否用根导航器(默认 true) |

## 最小示例

```dart
import 'package:flutter/material.dart';

/// DatePicker 最小示例:表单触发日期选择
class DatePickerSample extends StatefulWidget {
  const DatePickerSample({super.key});

  @override
  State<DatePickerSample> createState() => _DatePickerSampleState();
}

class _DatePickerSampleState extends State<DatePickerSample> {
  DateTime? _checkIn;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('DatePicker 示例')),
      body: Padding(
        padding: const EdgeInsets.all({spacing-md}),
        child: InkWell(
          borderRadius: BorderRadius.circular({radius-md}),
          onTap: () async {
            final picked = await showDatePicker(
              context: context,
              initialDate: _checkIn ?? DateTime.now(),
              firstDate: DateTime.now(),
              lastDate: DateTime(2030),
              helpText: '选择入住日期',
            );
            if (picked != null) setState(() => _checkIn = picked);
          },
          child: InputDecorator(
            decoration: const InputDecoration(
              labelText: '入住日期',
              border: OutlineInputBorder(),
              suffixIcon: Icon(Icons.calendar_today),
            ),
            child: Text(
              _checkIn == null ? '请选择' : '${_checkIn!.year}-${_checkIn!.month}-${_checkIn!.day}',
              style: TextStyle(
                color: _checkIn == null ? {color-text-secondary} : {color-text-primary},
              ),
            ),
          ),
        ),
      ),
    );
  }
}
```

## 参考链接

- API 参考 - showDatePicker: https://api.flutter.dev/flutter/material/showDatePicker.html
- API 参考 - showTimePicker: https://api.flutter.dev/flutter/material/showTimePicker.html
- API 参考 - CalendarDatePicker: https://api.flutter.dev/flutter/material/CalendarDatePicker-class.html
