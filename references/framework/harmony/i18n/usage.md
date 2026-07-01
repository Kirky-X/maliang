# I18n 使用场景与示例

> 列举 ArkTS 国际化的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础多语言($r 资源)

资源文件:
```json
// resources/base/element/string.json
{ "string": [ { "name": "hello", "value": "Hello" } ] }

// resources/zh_CN/element/string.json
{ "string": [ { "name": "hello", "value": "你好" } ] }
```

```arkts
@Entry
@Component
struct MultiLangPage {
  build() {
    Column() {
      Text($r('app.string.hello')).fontSize({font-size-lg})
      Button($r('app.string.submit'))
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:带参数的字符串

```json
// string.json
{ "name": "welcome", "value": "Welcome, %s!" }
```

```arkts
import { resourceManager } from '@kit.LocalizationKit'

@Entry
@Component
struct ParamStringPage {
  @State msg: string = ''
  aboutToAppear() {
    const rm = getContext(this).resourceManager
    rm.getStringByName('welcome').then((fmt: string) => {
      this.msg = fmt.replace('%s', 'Tom')
    })
  }
  build() {
    Text(this.msg).fontSize({font-size-md}).padding({spacing-md})
  }
}
```

## 场景 3:日期格式化(intl.DateTimeFormat)

```arkts
import { intl } from '@kit.LocalizationKit'

@Entry
@Component
struct DateFmtPage {
  private fmt() {
    const date = new Date()
    const dtf = new intl.DateTimeFormat('zh-CN', {
      year: 'numeric', month: '2-digit', day: '2-digit'
    })
    return dtf.format(date)
  }
  build() {
    Text(this.fmt()).fontSize({font-size-md}).padding({spacing-md})
  }
}
```

## 场景 4:数字/货币格式化

```arkts
import { intl } from '@kit.LocalizationKit'

@Entry
@Component
struct NumberFmtPage {
  private fmt() {
    const nf = new intl.NumberFormat('zh-CN', {
      style: 'currency', currency: 'CNY'
    })
    return nf.format(1234567.89)  // ¥1,234,567.89
  }
  build() {
    Text(this.fmt()).fontSize({font-size-md}).padding({spacing-md})
  }
}
```

## 场景 5:运行时切换语言

```arkts
import { common } from '@kit.AbilityKit'

@Entry
@Component
struct SwitchLangPage {
  appCtx: common.ApplicationContext = getContext(this).getApplicationContext()
  build() {
    Column({ space: {spacing-md} }) {
      Text($r('app.string.hello')).fontSize({font-size-lg})
      Button('切英文')
        .onClick(() => this.appCtx.setLanguage('en-US'))
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
      Button('切中文')
        .onClick(() => this.appCtx.setLanguage('zh-CN'))
        .backgroundColor({color-bg-secondary})
        .fontColor({color-text-primary})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **base 目录是兜底** — 当系统语言无对应限定目录时,回退到 `base/`;基础字符串必须有 base 版本。
2. **$r 返回 Resource 类型** — 不能直接拼接字符串;需运行时 `resourceManager.getStringByName` 取值。
3. **setLanguage 影响全应用** — 切换后所有 `$r` 重新取值;部分页面需重新进入才刷新。
4. **Intl 模块需导入** — `import { intl } from '@kit.LocalizationKit'`,日期/数字格式化能力在此。
5. **复数处理** — ArkTS 暂无原生 ICU 复数语法,需自行根据数量选不同 key。
6. **图片也需本地化** — 含文字的图片按语言目录放置;纯图形图无需本地化。
