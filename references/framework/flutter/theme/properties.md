# Flutter Theme 属性列表与默认值

本文档汇总 `ThemeData` / `ColorScheme` / `TextTheme` 的属性、默认值。颜色/尺寸默认值以 design token 形式给出。

## ThemeData 属性(常用)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `brightness` | `Brightness` | `Brightness.light` | 明暗 |
| `colorScheme` | `ColorScheme` | 由 primaryColor 派生 | M3 配色 |
| `useMaterial3` | `bool` | `true`(3.16+) | 是否 M3 |
| `visualDensity` | `VisualDensity` | `VisualDensity.standard` | 视觉密度 |
| `textTheme` | `TextTheme` | 默认 Typography | 文本样式 |
| `primaryColor` | `Color` | `Colors.blue` | 主色 |
| `primaryColorDark` | `Color` | `Colors.blue[700]` | 暗主色 |
| `primaryColorLight` | `Color` | `Colors.blue[100]` | 亮主色 |
| `scaffoldBackgroundColor` | `Color` | `Colors.grey[50]` | Scaffold 背景 |
| `cardColor` | `Color` | `Colors.white` | Card 背景 |
| `dividerColor` | `Color` | `Colors.grey[300]` | 分割线 |
| `hintColor` | `Color` | `Colors.grey[600]` | 提示色 |
| `disabledColor` | `Color` | `Colors.grey[400]` | 禁用色 |
| `highlightColor` | `Color` | `Colors.grey[200]` | 高亮 |
| `splashColor` | `Color` | `Colors.grey[400]` | 水波纹 |
| `iconTheme` | `IconThemeData` | 黑色 0.87 | 图标主题 |
| `platform` | `TargetPlatform?` | `null`(自动) | 目标平台 |
| `materialTapTargetSize` | `MaterialTapTargetSize` | `padded` | 点击目标尺寸 |

## ColorScheme 属性

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `brightness` | `Brightness` | 明暗 |
| `primary` | `Color` | 主色 |
| `onPrimary` | `Color` | 主色上文本色 |
| `primaryContainer` | `Color` | 主色容器(浅) |
| `onPrimaryContainer` | `Color` | 容器上文本色 |
| `secondary` | `Color` | 次要色 |
| `onSecondary` | `Color` | 次要色上文本色 |
| `secondaryContainer` | `Color` | 次要色容器 |
| `tertiary` | `Color` | 第三色 |
| `onTertiary` | `Color` | 第三色上文本色 |
| `error` | `Color` | 错误色 |
| `onError` | `Color` | 错误色上文本色 |
| `errorContainer` | `Color` | 错误容器 |
| `surface` | `Color` | 表面色(M3) |
| `onSurface` | `Color` | 表面文本色 |
| `surfaceVariant` / `surfaceContainerHighest` | `Color` | 表面变体 |
| `outline` | `Color` | 描边 |
| `outlineVariant` | `Color` | 描边变体 |
| `shadow` | `Color` | 阴影 |
| `scrim` | `Color` | 遮罩 |
| `inverseSurface` | `Color` | 反表面 |

## TextTheme 属性(M3)

| 属性名 | M3 默认样式 | 用途 |
| --- | --- | --- |
| `displayLarge` | 57px / regular | 大标题(数字) |
| `displayMedium` | 45px / regular | 大标题 |
| `displaySmall` | 36px / regular | 大标题 |
| `headlineLarge` | 32px / regular | 标题 |
| `headlineMedium` | 28px / regular | 标题 |
| `headlineSmall` | 24px / regular | 标题 |
| `titleLarge` | 22px / medium | 标题 |
| `titleMedium` | 16px / medium | 标题 |
| `titleSmall` | 14px / medium | 标题 |
| `bodyLarge` | 16px / regular | 正文 |
| `bodyMedium` | 14px / regular | 正文(默认) |
| `bodySmall` | 12px / regular | 正文(小) |
| `labelLarge` | 14px / medium | 按钮 |
| `labelMedium` | 12px / medium | 标签 |
| `labelSmall` | 11px / medium | 标签(小) |

## ColorScheme 工厂构造

| 构造 | 说明 |
| --- | --- |
| `ColorScheme.fromSeed({seedColor, brightness})` | 从种子色生成 M3 配色(推荐) |
| `ColorScheme.light({...})` | 浅色手动配置 |
| `ColorScheme.dark({...})` | 深色手动配置 |
| `ColorScheme.fromSwatch({primarySwatch, ...})` | 从 Material Swatch 派生(旧) |

## 组件主题(部分)

| 组件主题 | 类型 | 配置对象 |
| --- | --- | --- |
| `appBarTheme` | `AppBarTheme` | AppBar 样式 |
| `elevatedButtonTheme` | `ElevatedButtonThemeData` | ElevatedButton 样式 |
| `filledButtonTheme` | `FilledButtonThemeData` | FilledButton 样式 |
| `outlinedButtonTheme` | `OutlinedButtonThemeData` | OutlinedButton 样式 |
| `textButtonTheme` | `TextButtonThemeData` | TextButton 样式 |
| `cardTheme` | `CardTheme` | Card 样式 |
| `chipTheme` | `ChipThemeData` | Chip 样式 |
| `dialogTheme` | `DialogTheme` | Dialog 样式 |
| `inputDecorationTheme` | `InputDecorationTheme` | 输入框样式 |
| `listTileTheme` | `ListTileThemeData` | ListTile 样式 |
| `navigationBarTheme` | `NavigationBarThemeData` | NavigationBar 样式 |
| `snackBarTheme` | `SnackbarThemeData` | SnackBar 样式 |
| `tabBarTheme` | `TabBarTheme` | TabBar 样式 |
| `tooltipTheme` | `TooltipThemeData` | Tooltip 样式 |

## ThemeExtension(自定义扩展)

```dart
class MyColors extends ThemeExtension<MyColors> {
  final Color brand;
  final Color danger;
  const MyColors({required this.brand, required this.danger});

  @override
  MyColors copyWith({Color? brand, Color? danger}) =>
      MyColors(brand: brand ?? this.brand, danger: danger ?? this.danger);

  @override
  MyColors lerp(MyColors? other, double t) => MyColors(
    brand: Color.lerp(brand, other?.brand, t)!,
    danger: Color.lerp(danger, other?.danger, t)!,
  );
}

// 注入
ThemeData(extensions: [const MyColors(brand: {color-primary}, danger: {color-danger})])

// 读取
final my = Theme.of(context).extension<MyColors>()!;
Container(color: my.brand);
```

## 完整示例

```dart
import 'package:flutter/material.dart';

class ThemeFullSample extends StatelessWidget {
  const ThemeFullSample({super.key});

  static final _light = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: {color-primary},
      brightness: Brightness.light,
    ),
    textTheme: const TextTheme(
      bodyLarge: TextStyle(fontSize: {font-size-md}),
      titleLarge: TextStyle(fontSize: {font-size-lg}, fontWeight: FontWeight.w600),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: {color-primary},
        foregroundColor: {color-text-on-primary},
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular({radius-md}),
        ),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular({radius-md}),
      ),
      filled: true,
      fillColor: {color-bg-secondary},
    ),
    cardTheme: const CardThemeData(
      color: {color-bg-primary},
      elevation: 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular({radius-md})),
      ),
    ),
  );

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Theme 完整示例',
      theme: _light,
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: {color-primary},
          brightness: Brightness.dark,
        ),
      ),
      themeMode: ThemeMode.system,
      home: Builder(builder: (context) {
        final theme = Theme.of(context);
        return Scaffold(
          appBar: AppBar(title: const Text('Theme 完整示例')),
          body: ListView(
            padding: const EdgeInsets.all({spacing-md}),
            children: [
              Text('primary: ${theme.colorScheme.primary}',
                  style: theme.textTheme.bodyMedium),
              Text('标题', style: theme.textTheme.titleLarge),
              ElevatedButton(
                onPressed: () {},
                child: const Text('主题按钮'),
              ),
              const SizedBox(height: {spacing-sm}),
              const TextField(decoration: InputDecoration(labelText: '主题输入框')),
              const SizedBox(height: {spacing-sm}),
              const Card(child: ListTile(title: Text('主题卡片'))),
            ],
          ),
        );
      }),
    );
  }
}
```

## 注意事项

- `ColorScheme.fromSeed` 是 M3 推荐方式,自动生成全套配色(含容器色/变体色)
- `useMaterial3: true`(3.16+ 默认)启用 M3,否则回退 M2
- `Theme.of(context)` 依赖祖先 `Theme`/`MaterialApp`,在 `MaterialApp` 之外调用会抛异常
- 局部覆盖主题用 `Theme(data: ..., child: ...)`
- 深色模式:`darkTheme` + `themeMode: ThemeMode.system`,跟随系统切换
- 自定义颜色用 `ThemeExtension`,避免在 `ThemeData` 上塞非标字段
- 组件主题优先级:`Widget` 显式属性 > 组件主题 > `ThemeData` 全局 > M3 默认
