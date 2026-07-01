# I18n 组件 API 文档

> ArkTS UI 国际化,通过 `$r` 资源引用 + 限定目录(`zh_CN`/`en_US`)+ `Intl` 模块实现多语言。

## 机制说明

| 能力 | 实现 |
| --- | --- |
| 文本国际化 | `$r('app.string.xxx')` + `resources/<locale>/element/string.json` |
| 图片国际化 | `$r('app.media.xxx')` + `resources/<locale>/media/` |
| 数字/日期格式化 | `@ohos.intl` 模块(NumberFormat/DateTimeFormat) |
| 复数/性别 | ICU MessageFormat 风格字符串 |
| 语言切换 | `applicationContext.setLanguage()` |

## 资源目录结构

```
resources/
  base/element/string.json       -> 默认(英文)
  en_US/element/string.json      -> 英语
  zh_CN/element/string.json      -> 简体中文
  zh_HK/element/string.json      -> 繁体中文
```

## 核心 API

| API | 说明 |
| --- | --- |
| `$r('app.string.key')` | 引用字符串资源(返回 Resource) |
| `$rawfile('xxx')` | 引用 rawfile 资源 |
| `intl.NumberFormat` | 数字格式化 |
| `intl.DateTimeFormat` | 日期格式化 |
| `intl.RelativeTimeFormat` | 相对时间 |
| `intl.Collator` | 字符串排序 |

## 最小示例

```arkts
@Entry
@Component
struct I18nDemo {
  build() {
    Column() {
      Text($r('app.string.hello'))  // 自动按系统语言取值
        .fontSize({font-size-md})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`theme`](../theme/component.md) — 主题与 i18n 共用资源体系

## 参考链接

- ArkTS 官方文档 - UI国际化: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-internationalization
