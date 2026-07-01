# Theme 使用场景与示例

> 列举 ArkTS 主题设置的典型使用场景。所有颜色、间距通过 design token 或资源引用,不硬编码。

## 场景 1:跟随系统深浅色(默认)

资源目录分流,代码用 `$r` 引用,无需判断 ColorMode。

```arkts
@Entry
@Component
struct SystemThemePage {
  build() {
    Column() {
      Text('自动跟随系统').fontSize({font-size-md})
        .fontColor($r('app.color.text_primary'))
    }
    .width('100%').height('100%')
    .backgroundColor($r('app.color.bg_primary'))
  }
}
```

## 场景 2:应用内手动切换深浅色

```arkts
import { common } from '@kit.AbilityKit'
import { ConfigurationConstant } from '@ohos.app.ability.ConfigurationConstant'

@Entry
@Component
struct ManualThemePage {
  @State isDark: boolean = false
  appCtx: common.ApplicationContext = getContext(this).getApplicationContext()

  build() {
    Column({ space: {spacing-md} }) {
      Text(this.isDark ? '深色模式' : '浅色模式')
        .fontSize({font-size-md})
        .fontColor($r('app.color.text_primary'))
      Button('切换')
        .onClick(() => {
          this.isDark = !this.isDark
          this.appCtx.setColorMode(this.isDark
            ? ConfigurationConstant.ColorMode.DARK
            : ConfigurationConstant.ColorMode.LIGHT)
        })
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .width('100%').height('100%')
    .backgroundColor($r('app.color.bg_primary'))
    .padding({spacing-md})
  }
}
```

## 场景 3:多皮肤(主题包)

通过资源文件名前缀区分主题,运行时加载不同资源包。

```arkts
@Entry
@Component
struct MultiSkinPage {
  @State skin: string = 'default'  // default | red | blue
  build() {
    Column({ space: {spacing-sm} }) {
      Button('红色主题')
        .backgroundColor($r('app.color.theme_red_primary'))
        .onClick(() => this.skin = 'red')
      Button('蓝色主题')
        .backgroundColor($r('app.color.theme_blue_primary'))
        .onClick(() => this.skin = 'blue')
    }
    .padding({spacing-md})
    .backgroundColor($r('app.color.bg_primary'))
  }
}
```

## 场景 4:监听系统主题变化

```arkts
import { AbilityConstant } from '@kit.AbilityKit'

@Entry
@Component
struct ListenThemePage {
  aboutToAppear() {
    const ctx = getContext(this)
    ctx.on('environment', (env) => {
      console.info('系统主题变化')
    })
  }
  build() {
    Text('监听主题').fontColor($r('app.color.text_primary')).padding({spacing-md})
  }
}
```

## 注意事项

1. **优先用资源分流** — `$r('app.color.xxx')` + `dark/` 目录是首选方案,自动适配无需代码判断。
2. **setColorMode 影响全应用** — 设置后所有 `$r` 资源重新取值,需在 UIAbility 启动时调用。
3. **图片资源也要分流** — 深色背景下的浅色图标需在 `resources/dark/media/` 放置对应文件。
4. **硬编码颜色无法适配** — 直接写 `'#FFFFFF'` 不会随主题变化,必须用 `$r` 或 design token。
5. **AUTO 模式** — 默认跟随系统;若应用内固定模式用 `LIGHT`/`DARK` 覆盖。
6. **状态栏配色** — 深色模式下状态栏图标需切白,通过 `window.setSystemBarProperties` 设置。
