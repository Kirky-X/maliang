# Switch 组件 API 文档

> ArkTS 切换按钮组件。**注意:目录 slug 统一用 `switch`,ArkTS 原生组件名为 `Toggle`。** 支持开关(Switch)、按钮(Toggle Button)、复选(Checkbox)三种形态。

## 组件定义

`Toggle` 通过 `type` 区分形态:`ToggleType.Switch`(开关)/ `ToggleType.Button`(按钮)/ `ToggleType.Checkbox`(复选)。

## 构造函数

```arkts
Toggle(value: { type: ToggleType; isOn: boolean })
```

## ToggleType 枚举

| 值 | 形态 | 场景 |
| --- | --- | --- |
| `Switch` | iOS 风格开关 | 设置项开/关 |
| `Button` | 按钮切换(选中高亮) | 工具栏选中态 |
| `Checkbox` | 复选框 | 多选 |

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| isOn | boolean | 当前开/关 |
| selectedColor | ResourceColor | 开启态颜色,用 `{color-button-primary-bg}` |
| switchPointColor | ResourceColor | 圆点颜色(Switch 形态) |
| onChange | (isOn: boolean) => void | 状态变化回调 |

## 最小示例

```arkts
@Entry
@Component
struct SwitchDemo {
  @State on: boolean = false
  build() {
    Row() {
      Text('深色模式').fontSize({font-size-md})
      Toggle({ type: ToggleType.Switch, isOn: this.on })
        .selectedColor({color-button-primary-bg})
        .onChange((v: boolean) => this.on = v)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`radio`](../radio/component.md) — 单选(Radio)互斥选择
- [`input`](../input/component.md) — 表单输入

## 参考链接

- ArkTS 官方文档 - 切换按钮 (Toggle): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-switch
