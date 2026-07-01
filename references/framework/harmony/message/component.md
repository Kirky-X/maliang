# Message 组件 API 文档

> ArkTS 即时反馈组件。**注意:目录 slug 统一用 `message`,ArkTS 原生能力为 `Toast`(通过 `promptAction.showToast`)。** 用于短暂提示操作结果。

## 组件定义

`Toast` 通过命令式 API `promptAction.showToast()` 触发,不依赖组件树,全局居中显示,定时消失。

## 核心 API

```arkts
import { promptAction } from '@kit.ArkUI'

promptAction.showToast({
  message: string | Resource,
  duration?: number,        // 显示时长(ms),默认 1500
  bottom?: string | number, // 距底部距离
  showMode?: ToastShowMode  // DEFAULT / TOP
})
```

## showToast 参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| message | string \| Resource | 提示内容 |
| duration | number | 时长,1500/3000 为推荐值 |
| bottom | Length | 距底距离 |
| showMode | ToastShowMode | 显示模式 |

## openToast / showDialog / showActionMenu

| API | 用途 |
| --- | --- |
| `showToast` | 轻提示 |
| `showDialog` | 模态对话框 |
| `showActionMenu` | 操作菜单 |

## 最小示例

```arkts
import { promptAction } from '@kit.ArkUI'

@Entry
@Component
struct MessageDemo {
  build() {
    Column() {
      Button('保存')
        .onClick(() => {
          promptAction.showToast({ message: '保存成功', duration: 1500 })
        })
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`dialog`](../dialog/component.md) — 模态弹窗(需用户确认)
- [`popover`](../popover/component.md) — 锚定气泡(可交互)
- [`alert`](../alert/component.md) — 警告提示

## 参考链接

- ArkTS 官方文档 - 即时反馈 (Toast): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-create-toast
