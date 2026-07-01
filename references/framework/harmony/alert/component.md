# Alert 组件 API 文档

> ArkTS 警告提示,基于 `AlertDialog`(确认弹窗)与 `promptAction`(命令式弹窗)实现。用于重要操作确认与错误警示。

## 组件定义

| 能力 | API | 场景 |
| --- | --- | --- |
| 确认弹窗 | `AlertDialog.show()` | 危险操作确认 |
| 命令式弹窗 | `promptAction.showDialog()` | 推荐用法 |
| 自定义弹窗 | `CustomDialog` | 复杂内容告警 |

## AlertDialog.show 参数

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| title | string \| Resource | 标题 |
| message | string \| Resource | 内容 |
| primaryButton | { value, action, fontColor } | 主按钮(左) |
| secondaryButton | { value, action, fontColor } | 次按钮(右) |
| alignment | DialogAlignment | 对齐 |

## 语义配色(参考)

| 语义 | token |
| --- | --- |
| 成功 | `{color-success}` |
| 警告 | `{color-warning}` |
| 危险 | `{color-danger}` |
| 信息 | `{color-info}` |

## 最小示例

```arkts
@Entry
@Component
struct AlertDemo {
  build() {
    Column() {
      Button('删除')
        .onClick(() => {
          AlertDialog.show({
            title: '警告',
            message: '确认删除?此操作不可恢复',
            primaryButton: { value: '取消', action: () => {} },
            secondaryButton: { value: '删除', fontColor: {color-danger}, action: () => {} }
          })
        })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`dialog`](../dialog/component.md) — 弹窗基础能力
- [`message`](../message/component.md) — Toast 轻提示

## 参考链接

- ArkTS 官方文档 - 弹出框 (Dialog): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-use-dialogs
- 即时反馈 (Toast): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-create-toast
