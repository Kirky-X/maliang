# Message 使用场景与示例

> 列举 ArkTS Toast 即时反馈的典型使用场景(slug 统一 message,ArkTS 原生名 Toast)。所有颜色、间距通过 design token 引用。

## 场景 1:操作成功提示

```arkts
import { promptAction } from '@kit.ArkUI'

@Entry
@Component
struct SuccessToastPage {
  build() {
    Column() {
      Button('保存')
        .onClick(() => {
          // 保存逻辑
          promptAction.showToast({
            message: '保存成功',
            duration: 1500
          })
        })
        .backgroundColor({color-success})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:错误提示

```arkts
import { promptAction } from '@kit.ArkUI'

@Entry
@Component
struct ErrorToastPage {
  @State phone: string = ''
  build() {
    Column() {
      TextInput({ placeholder: '手机号' })
        .fontSize({font-size-md})
        .backgroundColor({color-bg-primary})
        .onChange((v: string) => this.phone = v)
      Button('提交')
        .onClick(() => {
          if (this.phone.length !== 11) {
            promptAction.showToast({ message: '手机号格式错误', duration: 2000 })
            return
          }
          promptAction.showToast({ message: '提交成功' })
        })
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:加载中提示(Toast + Loading)

```arkts
import { promptAction } from '@kit.ArkUI'

@Entry
@Component
struct LoadingToastPage {
  build() {
    Column() {
      Button('加载数据')
        .onClick(() => {
          promptAction.showToast({
            message: '加载中...',
            duration: 2000
          })
          // 异步加载
        })
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:位置控制(bottom)

```arkts
import { promptAction } from '@kit.ArkUI'

@Entry
@Component
struct BottomToastPage {
  build() {
    Column() {
      Button('底部提示')
        .onClick(() => {
          promptAction.showToast({
            message: '操作完成',
            duration: 1500,
            bottom: '100vp'
          })
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:对话框(showDialog)

需要用户确认时用 `showDialog` 而非 Toast。

```arkts
import { promptAction } from '@kit.ArkUI'

@Entry
@Component
struct ConfirmPage {
  build() {
    Column() {
      Button('退出')
        .onClick(() => {
          promptAction.showDialog({
            title: '提示',
            message: '确认退出登录?',
            buttons: [
              { text: '取消', color: {color-text-primary} },
              { text: '确认', color: {color-danger} }
            ]
          }).then((res) => {
            if (res.index === 1) {
              promptAction.showToast({ message: '已退出' })
            }
          })
        })
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **Toast 不可交互** — Toast 显示期间点击无响应;需用户操作用 Dialog/ActionSheet。
2. **duration 推荐值** — 1500ms(短)/ 3000ms(长);过短看不清,过长干扰。
3. **message 资源化** — 生产代码用 `$r('app.string.xxx')` 而非硬编码,支持国际化。
4. **Toast 会排队** — 多次连续调用会依次显示;避免高频触发导致堆叠。
5. **showDialog 返回 Promise** — 用 `.then` 或 `await` 获取点击索引(从 0 开始)。
6. **与 Snackbar 区别** — ArkTS 无原生 Snackbar;带操作按钮的反馈用 Dialog 或自定义 Popup。
