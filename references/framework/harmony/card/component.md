# Card 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Card 组件。** 通过 `Column` 容器 + 装饰属性(背景色/圆角/阴影/边距)组合实现卡片效果。

## 缺失原因

ArkTS 没有 HTML `<div>` 或 Material `Card` 那样的专门卡片容器。卡片本质是带视觉装饰的容器,用 `Column` 配合 `backgroundColor` / `borderRadius` / `shadow` 即可实现。

## 替代方案

- **方案 1:Column + 装饰属性** — 最常用,直接组合背景色、圆角、阴影、内边距。
- **方案 2:封装自定义 @Component** — 将卡片样式抽为可复用组件,统一管理视觉规范。

## 通用卡片样式(参考)

| 属性 | 取值 |
| --- | --- |
| backgroundColor | `{color-bg-primary}` |
| borderRadius | `{radius-md}` |
| padding | `{spacing-md}` ~ `{spacing-lg}` |
| shadow | ShadowStyle.OUTER_DEFAULT_MD |

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:Column + 装饰) |
| Flutter | `Card` widget(内置圆角阴影) |
| Element Plus | `<el-card>` |

## 最小示例

```arkts
@Entry
@Component
struct CardDemo {
  build() {
    Column() {
      Column({ space: {spacing-sm} }) {
        Text('卡片标题').fontSize({font-size-md}).fontWeight(FontWeight.Bold)
        Text('卡片内容描述信息').fontSize({font-size-sm}).fontColor({color-text-primary})
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
      .borderRadius({radius-md})
      .shadow(ShadowStyle.OUTER_DEFAULT_MD)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`layout`](../layout/component.md) — 卡片基于 Column 布局
- [`divider`](../divider/component.md) — 卡片内分区

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`layout`](../layout/component.md)(阴影效果见动画章节)
- 阴影效果: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-shadow-effect
