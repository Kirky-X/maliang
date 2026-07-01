# Flutter i18n 属性列表与默认值

本文档汇总 Flutter 国际化体系的完整属性、默认值与配置项。所有显示文案通过 design token 形式引用资源 key,不在文档中硬编码具体语言文案。

## Localizations 构造参数

`Localizations` Widget 用于向子树注入本地化资源。

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Key?` | `null` | Widget 标识 |
| `delegates` | `List<LocalizationsDelegate<dynamic>>` | 必填 | 本地化代理列表 |
| `locale` | `Locale?` | `null` | 当前 Locale,`null` 时取上游 `Localizations.localeOf` |
| `child` | `Widget` | 必填 | 子节点 |

## LocalizationsDelegate 属性

抽象类,子类需实现三个方法。

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `load` | `Future<T> load(Locale locale)` | 异步加载对应 Locale 的资源 |
| `isSupported` | `bool isSupported(Locale locale)` | 判断是否支持该 Locale |
| `reload` | `bool shouldReload(LocalizationsDelegate<T> old)` | 是否需要重新加载(默认返回 `false`) |

## AppLocalizations(gen-l10n 生成)

由 `flutter gen-l10n` 自动生成,常用访问方式:

| 访问点 | 类型 | 说明 |
| --- | --- | --- |
| `AppLocalizations.delegate` | `LocalizationsDelegate<AppLocalizations>` | 注入到 `localizationsDelegates` |
| `AppLocalizations.of(context)` | `AppLocalizations?` | 在子树获取实例 |
| `AppLocalizations.supportedLocales` | `List<Locale>` | 支持的 Locale 列表 |

## MaterialApp 国际化相关参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `localizationsDelegates` | `Iterable<LocalizationsDelegate<dynamic>>?` | `null` | 本地化代理列表 |
| `supportedLocales` | `Iterable<Locale>` | `[Locale('en', 'US')]` | 支持的 Locale 列表 |
| `locale` | `Locale?` | `null` | 强制指定 Locale,`null` 时跟随系统 |
| `localeListResolutionCallback` | `LocaleResolutionCallback?` | `null` | Locale 列表解析回调 |
| `localeResolutionCallback` | `LocaleResolutionCallback?` | `null` | 单 Locale 解析回调 |
| `onGenerateTitle` | `GenerateAppTitle?` | `null` | 根据 Locale 生成应用标题 |

## intl 包核心 API

| API | 说明 |
| --- | --- |
| `Intl.message(content, {name, args, desc, examples})` | 标记可翻译字符串 |
| `Intl.plural(count, {zero, one, other, ...})` | 复数处理 |
| `Intl.gender(gender, {male, female, other})` | 性别处理 |
| `Intl.select(choices, key)` | 选择性翻译 |
| `Intl.date(date, {format, locale})` | 日期格式化 |
| `Intl.number(number, {format, locale})` | 数字格式化 |
| `NumberFormat.currency({locale, symbol})` | 货币格式化 |
| `DateFormat.yMd(locale)` | 日期格式化器 |

## 系统级本地化代理(必填)

| 代理 | 作用 |
| --- | --- |
| `GlobalMaterialLocalizations.delegate` | Material 组件文案(按钮、对话框等) |
| `GlobalWidgetsLocalizations.delegate` | 通用 Widget 文本方向、默认文案 |
| `GlobalCupertinoLocalizations.delegate` | Cupertino 组件文案 |

> 缺失上述代理会导致 `DatePicker`、`TimePicker` 等组件报 `Localizations not found` 异常。

## l10n.yaml 配置文件

```yaml
arb-dir: lib/l10n/arb
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
preferred-supported-locales: [en, zh]
synthetic-package: false
nullable-getter: true
```

| 字段 | 默认值 | 说明 |
| --- | --- | --- |
| `arb-dir` | `lib/l10n` | ARB 资源目录 |
| `template-arb-file` | `app_en.arb` | 模板 ARB 文件(其他语言的基准) |
| `output-localization-file` | `app_localizations.dart` | 生成的 Dart 文件名 |
| `output-class` | `AppLocalizations` | 生成的类名 |
| `preferred-supported-locales` | `[en]` | 优先支持的 Locale 顺序 |
| `synthetic-package` | `true` | 是否生成到 synthetic package |
| `nullable-getter` | `true` | `of(context)` 是否返回可空类型 |

## ARB 文件示例

```json
{
  "@@locale": "zh",
  "appTitle": "马良设计系统",
  "@appTitle": {
    "description": "应用标题"
  },
  "welcomeMessage": "欢迎,{user}",
  "@welcomeMessage": {
    "placeholders": {
      "user": { "type": "String" }
    }
  },
  "itemCount": "{count} 项",
  "@itemCount": {
    "placeholders": {
      "count": { "type": "int" }
    }
  }
}
```

## 完整示例

```dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart';
import 'l10n/app_localizations.dart';

class I18nFullSample extends StatefulWidget {
  const I18nFullSample({super.key});

  @override
  State<I18nFullSample> createState() => _I18nFullSampleState();
}

class _I18nFullSampleState extends State<I18nFullSample> {
  Locale _currentLocale = const Locale('zh');

  void _switchLocale(Locale locale) {
    setState(() => _currentLocale = locale);
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final now = DateTime.now();

    return MaterialApp(
      locale: _currentLocale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: Scaffold(
        appBar: AppBar(
          title: Text(l10n.appTitle),
          actions: [
            IconButton(
              onPressed: () => _switchLocale(const Locale('zh')),
              icon: const Text('中'),
            ),
            IconButton(
              onPressed: () => _switchLocale(const Locale('en')),
              icon: const Text('EN'),
            ),
          ],
        ),
        body: Padding(
          padding: const EdgeInsets.all({spacing-md}),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                l10n.welcomeMessage('设计师'),
                style: TextStyle(fontSize: {font-size-md}),
              ),
              Text(
                Intl.message('今天', name: 'today'),
                style: TextStyle(color: {color-text-secondary}),
              ),
              Text(
                DateFormat.yMd(_currentLocale.toString()).format(now),
              ),
              Text(
                Intl.plural(
                  3,
                  one: '1 项',
                  other: '${3} 项',
                  name: 'itemCount',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## 注意事项

- ARB 文件中 `@key` 对象的 `description` 字段为翻译者提供上下文,**必填**;缺失会导致 `gen-l10n` 警告。
- `Intl.plural` 仅支持 `zero/one/two/few/many/other` 六种规则,部分语言(俄语、阿拉伯语)需完整规则。
- 切换 Locale 后,MaterialApp 子树会自动重建;若使用 `stateful` 持久化 Locale,需在 `initState` 中读取持久化值后再构建。
- `DateFormat` / `NumberFormat` 实例**不要缓存为全局静态变量**,Locale 变更后会使用错误格式。
- Web 平台下 `window.locale` 与 Flutter `Locale` 解析顺序可能不一致,务必设置 `localeResolutionCallback` 显式回退逻辑。
