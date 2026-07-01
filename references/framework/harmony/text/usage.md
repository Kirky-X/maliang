# Text 使用场景与示例

> 列举 HarmonyOS 应用中 Text 组件的典型使用场景、完整代码示例与注意事项。所有颜色/字号通过 design token 引用,不硬编码。

## 场景 1:标题与正文

页面标题、正文段落使用不同字号与字重区分层级,构成基础排版结构。

```arkts
@Entry
@Component
struct TitleBodyPage {
  build() {
    Column() {
      // 大标题
      Text('应用说明')
        .fontSize({font-size-title-lg})
        .fontColor({color-text-primary})
        .fontWeight(FontWeight.Bold)
        .textAlign(TextAlign.Start)
        .width('100%')

      // 正文
      Text('本应用用于演示 ArkTS 声明式 UI 组件的典型用法,包含 Button、Text、List 三类基础组件。')
        .fontSize({font-size-body})
        .fontColor({color-text-secondary})
        .lineHeight(24)
        .textAlign(TextAlign.Start)
        .width('100%')
        .margin({ top: {spacing-sm} })
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:文本溢出省略

列表项标题、卡片摘要受容器宽度限制,需配合 `maxLines` + `textOverflow` 实现单行/多行省略。

```arkts
@Entry
@Component
struct EllipsisPage {
  build() {
    Column() {
      // 单行省略
      Text('这是一段非常长的标题文字,超出容器宽度后将显示省略号')
        .fontSize({font-size-md})
        .fontColor({color-text-primary})
        .maxLines(1)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
        .width('100%')

      // 两行省略
      Text('这是一段较长的描述文字,允许显示两行,超出后以省略号结尾。常用于列表项描述、卡片摘要等场景。')
        .fontSize({font-size-body})
        .fontColor({color-text-secondary})
        .maxLines(2)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
        .width('100%')
        .margin({ top: {spacing-sm} })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:辅助文本(说明/时间戳)

次级文字使用 `{color-text-secondary}` / `{color-text-tertiary}` 降低视觉权重,常用于说明、时间戳、计数。

```arkts
@Entry
@Component
struct CaptionPage {
  build() {
    Column() {
      Text('订单号:20260701000123')
        .fontSize({font-size-md})
        .fontColor({color-text-primary})

      // 时间戳,使用更小的字号 + 次级颜色
      Text('更新于 2026-07-01 14:30')
        .fontSize({font-size-sm})
        .fontColor({color-text-tertiary})
        .margin({ top: {spacing-xs} })
    }
    .padding({spacing-md})
    .alignItems(HorizontalAlign.Start)
  }
}
```

## 场景 4:富文本(协议链接)

用户协议、隐私政策等场景使用 `Span` 拼接,链接片段使用不同颜色 + 下划线,并绑定点击事件。

```arkts
@Entry
@Component
struct RichTextPage {
  build() {
    Column() {
      Text() {
        Span('我已阅读并同意')
          .fontColor({color-text-secondary})
          .fontSize({font-size-body})

        Span('《用户协议》')
          .fontColor({color-text-link})
          .fontSize({font-size-body})
          .decoration({ type: TextDecorationType.Underline, color: {color-text-link} })
          .onClick(() => {
            // 跳转用户协议页
          })

        Span('与')
          .fontColor({color-text-secondary})
          .fontSize({font-size-body})

        Span('《隐私政策》')
          .fontColor({color-text-link})
          .fontSize({font-size-body})
          .decoration({ type: TextDecorationType.Underline, color: {color-text-link} })
          .onClick(() => {
            // 跳转隐私政策页
          })
      }
      .textAlign(TextAlign.Start)
      .width('100%')
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:可复制文本

验证码、订单号等需要用户长按复制的内容,设置 `copyOption` 开启复制能力。

```arkts
@Entry
@Component
struct CopyablePage {
  build() {
    Column() {
      Text('验证码:836492')
        .fontSize({font-size-title-md})
        .fontColor({color-text-primary})
        .fontWeight(FontWeight.Medium)
        .copyOption(CopyOptions.LocalDevice)
        .textAlign(TextAlign.Center)
        .width('100%')

      Text('长按上方文字可复制验证码')
        .fontSize({font-size-sm})
        .fontColor({color-text-tertiary})
        .margin({ top: {spacing-xs} })
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **字号层级** — 标题/正文/辅助文字必须使用不同 token(`{font-size-title-lg}` / `{font-size-body}` / `{font-size-sm}`),建立清晰的视觉层级,避免全篇统一字号。
2. **颜色语义** — 主文字用 `{color-text-primary}`,次级用 `{color-text-secondary}`,提示用 `{color-text-tertiary}`,链接用 `{color-text-link}`;禁止硬编码颜色值。
3. **maxLines 与 textOverflow 配套** — 单独设置 `maxLines` 而不设 `textOverflow`,超出部分会被截断而非省略,体验差;两者必须配套使用。
4. **富文本事件** — `Span` 上的 `onClick` 在低版本可能存在兼容问题,优先使用 `Text` 整体点击或 `RichEditor` 组件。
5. **行高单位** — `lineHeight` 默认单位为 vp,推荐设为字号的 1.4~1.6 倍以保证可读性(如字号 14 → 行高 22)。
6. **多语言长度** — 同一文案在多语言下长度差异较大,UI 布局必须预留弹性宽度,避免德语/俄语场景下文字溢出。
