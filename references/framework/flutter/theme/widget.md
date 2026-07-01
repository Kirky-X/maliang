# Flutter Theme Widget 定义

## Widget 定义

Flutter 主题通过 `ThemeData`(不可变配置对象)集中描述颜色、字体、组件样式。`Theme` Widget(继承自 `StatelessWidget`)将 `ThemeData` 注入子树,子节点通过 `Theme.of(context)` 读取。Material 3 用 `ColorScheme` 驱动配色。

| Widget/类 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `ThemeData` | `ThemeData` | `Diagnosticable` | 主题配置(颜色/字体/组件样式) |
| `Theme` | `Theme` | `StatelessWidget` | 注入主题到子树 |
| `ColorScheme` | `ColorScheme` | `Diagnosticable` | M3 配色方案(primary/secondary/...) |
| `TextTheme` | `TextTheme` | `Diagnosticable` | 文本样式集合 |
| `MaterialApp` | `MaterialApp` | `StatefulWidget` | 应用根(可配置 theme/darkTheme) |
| `ThemeExtension` | `ThemeExtension<T>` | - | 自定义主题扩展 |

## 构造函数

### ThemeData

```dart
ThemeData({
  Brightness? brightness,                  // light/dark
  ColorScheme? colorScheme,                // M3 配色(推荐)
  bool? useMaterial3,                      // 是否启用 M3(默认 true)
  VisualDensity? visualDensity,
  Typography? typography,
  TextTheme? textTheme,
  Color? primaryColor,
  Color? scaffoldBackgroundColor,
  Color? cardColor,
  Color? dividerColor,
  Color? hintColor,
  Color? disabledColor,
  Color? iconTheme,
  // 组件主题(每种组件可单独配置)
  AppBarTheme? appBarTheme,
  ButtonThemeData? buttonTheme,
  ElevatedButtonThemeData? elevatedButtonTheme,
  FilledButtonThemeData? filledButtonTheme,
  OutlinedButtonThemeData? outlinedButtonTheme,
  TextButtonThemeData? textButtonTheme,
  CardTheme? cardTheme,
  ChipThemeData? chipTheme,
  DialogTheme? dialogTheme,
  InputDecorationTheme? inputDecorationTheme,
  ListTileThemeData? listTileTheme,
  NavigationBarThemeData? navigationBarTheme,
  SnackbarThemeData? snackBarTheme,
  TabBarTheme? tabBarTheme,
  TooltipThemeData? tooltipTheme,
  // ...更多组件主题
  Iterable<ThemeExtension<dynamic>>? extensions,
})
```

### ColorScheme

```dart
const ColorScheme({
  required Brightness brightness,
  required Color primary,
  required Color onPrimary,
  Color? primaryContainer,
  Color? onPrimaryContainer,
  required Color secondary,
  required Color onSecondary,
  Color? secondaryContainer,
  Color? onSecondaryContainer,
  required Color tertiary,
  required Color onTertiary,
  required Color error,
  required Color onError,
  required Color surface,           // M3 表面色
  required Color onSurface,
  Color? surfaceContainerHighest,
  Color? outline,
  Color? outlineVariant,
  Color? shadow,
  Color? scrim,
  ...
})
```

### Theme

```dart
const Theme({
  super.key,
  required ThemeData data,
  Widget? child,
})
```

## 核心属性

### ThemeData 常用属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `brightness` | `Brightness` | light/dark |
| `colorScheme` | `ColorScheme` | M3 配色 |
| `useMaterial3` | `bool` | 是否 M3 |
| `textTheme` | `TextTheme` | 文本样式 |
| `primaryColor` | `Color` | 主色 |
| `scaffoldBackgroundColor` | `Color` | Scaffold 背景 |
| `cardColor` | `Color` | Card 背景 |
| `dividerColor` | `Color` | 分割线色 |
| `iconTheme` | `IconThemeData` | 图标主题 |
| `extensions` | `Map<Type, ThemeExtension>` | 自定义扩展 |

### ColorScheme 常用属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `primary` | `Color` | 主色 |
| `onPrimary` | `Color` | 主色上的文本/图标色 |
| `primaryContainer` | `Color` | 主色容器(浅色变体) |
| `secondary` | `Color` | 次要色 |
| `tertiary` | `Color` | 第三色 |
| `error` | `Color` | 错误色 |
| `surface` | `Color` | 表面色 |
| `onSurface` | `Color` | 表面文本色 |
| `outline` | `Color` | 描边色 |
| `brightness` | `Brightness` | light/dark |

## 最小示例

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Theme 示例',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: {color-primary}),
        fontFamily: 'Roboto',
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontSize: {font-size-md}),
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: {color-primary},
          brightness: Brightness.dark,
        ),
      ),
      themeMode: ThemeMode.system, // 跟随系统
      home: const ThemeSample(),
    );
  }
}

class ThemeSample extends StatelessWidget {
  const ThemeSample({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Theme 示例')),
      body: Container(
        color: theme.colorScheme.surface,
        child: Text(
          '主色: ${theme.colorScheme.primary}',
          style: theme.textTheme.bodyLarge,
        ),
      ),
    );
  }
}
```

## 参考链接

- Flutter 官方文档 - 设计 & 主题: https://docs.flutter.cn/ui/design
- Flutter 官方文档 - Material 设计: https://docs.flutter.cn/ui/design/material
- Cookbook - 共享主题样式: https://docs.flutter.cn/cookbook/design/themes
- 迁移至 Material 3: https://docs.flutter.cn/release/breaking-changes/material-3-migration
- Widget 目录 - Styling: https://docs.flutter.cn/ui/widgets/styling
- API 参考 - ThemeData: https://api.flutter.dev/flutter/material/ThemeData-class.html
- API 参考 - Theme: https://api.flutter.dev/flutter/material/Theme-class.html
- API 参考 - ColorScheme: https://api.flutter.dev/flutter/material/ColorScheme-class.html
