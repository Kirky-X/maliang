# A11y 组件 API 文档

> ArkTS 无障碍与适老化,通过通用属性(`accessibilityText`/`accessibilityDescription`/`accessibilityLevel`)与适老化配置实现。

## 核心:无障碍通用属性

所有组件均支持以下无障碍属性(无需引入额外组件):

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| accessibilityText | string \| Resource | 读屏朗读文案(替代组件内文字) |
| accessibilityDescription | string \| Resource | 补充说明(朗读在 accessibilityText 之后) |
| accessibilityLevel | string | `'auto'` / `'yes'`(可聚焦)/ `'no'`(忽略) |
| accessibilityRole | AccessibilityRole | 角色:Button/Image/Text/Tab 等 |
| accessibilityGroup | boolean | 是否将子节点合并为一个可聚焦单元 |
| accessibilityChecked | boolean | 勾选状态(开关类) |
| accessibilitySelected | boolean | 选中状态 |
| onClick(callback) | - | 无障碍点击事件(支持键盘/读屏激活) |

## 适老化能力

| 能力 | 实现 |
| --- | --- |
| 字体放大 | 响应 `fontSize` 跟随系统字号(`fp` 单位) |
| 高对比度 | 资源限定目录 + 增强色彩对比 |
| 焦点导航 | `focusable(true)` + `tabIndex` |
| 语音朗读 | `accessibilityText` 自动被读屏读取 |

## 最小示例

```arkts
@Entry
@Component
struct A11yDemo {
  build() {
    Column() {
      Button('收藏')
        .accessibilityText('收藏按钮')
        .accessibilityDescription('点击收藏当前内容')
        .accessibilityLevel('yes')
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`theme`](../theme/component.md) — 高对比度与主题协同
- [`icon`](../icon/component.md) — 纯图标必须设 accessibilityText

## 参考链接

- ArkTS 官方文档 - 无障碍与适老化: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-support-accessibility-friendliness
- 无障碍开发指导: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-universal-attributes-accessibility
- 支持适老化: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkui-support-for-aging-adaptation
