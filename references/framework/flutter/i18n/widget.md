# Flutter i18n Widget 定义

## Widget 定义

Flutter 国际化(i18n)通过 `Localizations`(注入 locale 资源到子树)+ `AppLocalizations`(生成的本地化类)+ `intl` 包(消息格式化)实现。`LocalizationsDelegate<T>` 负责按 locale 加载资源。`MaterialApp` 的 `localizationsDelegates` + `supportedLocales` 配置应用多语言。

| Widget/类 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `Localizations` | `Localizations` | `StatefulWidget` | 注入 locale 资源到子树 |
| `LocalizationsDelegate<T>` | `LocalizationsDelegate<T>` | - | 抽象资源加载委托 |
| `AppLocalizations` | `AppLocalizations` | - | 自动生成的本地化类(gen-l10n) |
| `Locale` | `Locale` | - | 语言区域(zh_CN/en_US) |
| `intl` | 包 | - | 消息格式化(日期/数字/复数) |
| `MaterialLocalizations` | `MaterialLocalizations` | - | Material 内置文案本地化 |

## 构造函数

### Localizations

```dart
const Localizations({
  super.key,
  required Locale locale,
  required List<LocalizationsDelegate<dynamic>> delegates,
  Widget? child,
})
```

### LocalizationsDelegate<T>(抽象类,需继承)

```dart
abstract class LocalizationsDelegate<T> {
  bool isSupported(Locale locale);              // 是否支持该 locale
  Future<T> load(Locale locale);                // 加载资源(返回 T)
  bool shouldReload(covariant LocalizationsDelegate<T> old);
}
```

### MaterialApp 配置

```dart
MaterialApp(
  localizationsDelegates: [
    AppLocalizations.delegate,                  // 应用资源
    GlobalMaterialLocalizations.delegate,       // Material 内置文案
    GlobalWidgetsLocalizations.delegate,        // 文本方向等
    GlobalCupertinoLocalizations.delegate,
  ],
  supportedLocales: const [
    Locale('en'),
    Locale('zh'),
  ],
  locale: const Locale('zh'),                   // 固定(可选)
  localeResolutionCallback: (deviceLocale, supported) {
    // 自定义 locale 解析
  },
  ...
)
```

### AppLocalizations(gen-l10n 生成)

```dart
// 由 flutter gen-l10n 根据 l10n.yaml + lib/l10n/app_*.arb 生成
class AppLocalizations {
  static AppLocalizations of(BuildContext context) =>
      Localizations.of<AppLocalizations>(context, AppLocalizations)!;

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  String get hello;       // 来自 .arb 的 key
  String greeting(String name);  // 带参数
}
```

## 核心属性

### MaterialApp i18n 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `localizationsDelegates` | `List<LocalizationsDelegate>` | 资源加载委托列表 |
| `supportedLocales` | `List<Locale>` | 支持的 locale |
| `locale` | `Locale?` | 当前 locale(为 null 时跟随系统) |
| `localeResolutionCallback` | `LocaleResolutionCallback?` | locale 解析回调 |
| `localeListResolutionCallback` | `LocaleListResolutionCallback?` | 多 locale 解析(Android 7+) |

### Locale 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `languageCode` | `String` | 语言代码(zh/en) |
| `countryCode` | `String?` | 国家代码(CN/US) |
| `scriptCode` | `String?` | 脚本代码(Hans/Hant) |

## 最小示例

```dart
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'i18n 示例',
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [Locale('en'), Locale('zh')],
      home: const I18nSample(),
    );
  }
}

class I18nSample extends StatelessWidget {
  const I18nSample({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(l10n?.title ?? 'i18n 示例')),
      body: Center(child: Text(l10n?.greeting('World') ?? 'Hello World')),
    );
  }
}
```

> 需在 `l10n.yaml` 配置生成参数,`pubspec.yaml` 添加 `flutter_localizations` 与 `generate: true`。

## 参考链接

- Flutter 官方文档 - 国际化 (i18n): https://docs.flutter.cn/ui/internationalization
- API 参考 - Localizations: https://api.flutter.dev/flutter/widgets/Localizations-class.html
- API 参考 - LocalizationsDelegate: https://api.flutter.dev/flutter/widgets/LocalizationsDelegate-class.html
- API 参考 - Locale: https://api.flutter.dev/flutter/dart-ui/Locale-class.html
- pub.dev - intl: https://pub.flutter-io.cn/packages/intl
- pub.dev - flutter_localizations: https://pub.flutter-io.cn/packages/flutter_localizations
