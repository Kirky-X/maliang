# Notification 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生应用内 Notification(消息中心/横幅)组件。** 系统通知(`notificationManager`)属系统级推送;应用内常驻通知条通过 `Stack` 顶部横幅 + 状态管理组合实现。

## 缺失原因

ArkUI 仅提供 `promptAction.showToast`(即席 toast)与系统级 `notificationManager` 推送;应用内"常驻、可关闭、带操作"的消息中心横幅无原生 UI 组件。

## 替代方案(组合结构)

| 角色 | ArkTS 实现 |
| --- | --- |
| 常驻横幅 | `Stack` 顶部层 + 自定义 `Row`(图标 + 多行文本 + 操作按钮 + 关闭) |
| 展示/退出动画 | `animateTo`(位移 + 透明度) |
| 自动消失 | 定时器控制(横幅型建议不自动消失或 ≥8s) |
| 消息中心 | 页面右上角入口 + `List` 消息列表(应用层状态管理) |

## 组合结构

```arkts
// 横幅状态模型
interface AppNotification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  actions?: string[]   // 操作按钮文案
  sticky?: boolean     // 常驻:不自动消失
}
```

## 最小示例

```arkts
@Entry
@Component
struct NotificationBannerPage {
  @State banner: AppNotification | null = {
    id: 'n1', type: 'warning',
    title: '同步失败',
    message: '网络连接不稳定,3 条变更未同步',
    actions: ['重试'], sticky: true
  }

  @Builder
  Banner(n: AppNotification) {
    Row({ space: {spacing-sm} }) {
      Text(n.title).fontSize({font-size-md}).fontWeight(FontWeight.Bold)
      Text(n.message).fontSize({font-size-sm}).layoutWeight(1)
      ForEach(n.actions ?? [], (a: string) => {
        Button(a, { buttonStyle: ButtonStyleMode.TEXTUAL }).fontSize({font-size-sm})
      })
      Image($r('sys.media.ohos_ic_public_cancel'))
        .width(20).height(20)
        .onClick(() => this.banner = null)
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-secondary})
    .borderRadius({radius-md})
  }

  build() {
    Stack({ alignContent: Alignment.Top }) {
      Column() {
        Text('页面主体').fontSize({font-size-md})
      }.width('100%')
      if (this.banner) {
        this.Banner(this.banner!)
          .margin({ top: {spacing-sm}, left: {spacing-md}, right: {spacing-md} })
      }
    }
    .width('100%')
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`message`](../message/component.md) — toast(短暂、单条、无操作位)
- [`alert`](../alert/component.md) — 静态警告提示

## 参考链接

- ArkTS 官方文档 - Stack 堆叠容器: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-container-stack
- ArkTS API 参考 - notificationManager(系统通知): https://developer.huawei.com/consumer/cn/doc/harmonyos-references/js-apis-notificationmanager
