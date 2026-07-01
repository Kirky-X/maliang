# Theme 组件 API 文档

> ArkTS 主题设置,包含深浅色适配(ColorMode)与应用内换肤。通过资源限定目录与 `ConfigurationContext` 切换。

## 机制说明

ArkTS 主题基于资源限定符目录:
- `resources/dark/element/` — 深色资源
- `resources/base/element/` — 默认(浅色)资源
- `resources/base/media/` 与 `resources/dark/media/` — 图片资源

系统 `ColorMode` 跟随系统深浅色,应用内通过 `ApplicationContext.setColorMode()` 强制切换。

## 核心 API

| API | 说明 |
| --- | --- |
| `ConfigurationConstant.ColorMode` | LIGHT / DARK / AUTO(跟随系统) |
| `applicationContext.setColorMode(mode)` | 设置应用级颜色模式 |
| `applicationContext.getColorMode()` | 获取当前模式 |
| `@ohos.app.ability.configurationConstant` | 颜色模式枚举 |
| `$r('app.color.xxx')` | 资源引用,自动按 ColorMode 取值 |

## 资源文件示例

```
resources/
  base/element/color.json    -> { "color": { "text_primary": "#333333" } }
  dark/element/color.json    -> { "color": { "text_primary": "#FFFFFF" } }
```

## 最小示例

```arkts
import { common } from '@kit.AbilityKit'
import { ConfigurationConstant } from '@ohos.app.ability.ConfigurationConstant'

@Entry
@Component
struct ThemeDemo {
  build() {
    Column() {
      Text('主题示例')
        .fontColor($r('app.color.text_primary'))  // 自动适配深浅色
        .fontSize({font-size-md})
    }
    .padding({spacing-md})
    .backgroundColor($r('app.color.bg_primary'))
  }
}

// 强制深色
function forceDark(ctx: common.UIAbilityContext) {
  ctx.getApplicationContext().setColorMode(ConfigurationConstant.ColorMode.DARK)
}
```

## 关联组件

- [`i18n`](../i18n/component.md) — 国际化与主题共用资源体系
- [`a11y`](../a11y/component.md) — 适老化与深浅色协同

## 参考链接

- ArkTS 官方文档 - 主题设置: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-theme
- 应用深浅色适配: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ui-dark-light-color-adaptation
- 设置应用内主题换肤: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/theme_skinning
