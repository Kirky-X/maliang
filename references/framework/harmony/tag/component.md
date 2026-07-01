# Tag 组件 API 文档

> ArkTS 标签组件,通过 `Badge`(徽标组件)或 `Text` + 背景装饰实现小标签。用于状态标记、分类标识。

## 组件定义

ArkTS 无独立 `Tag` 组件,但 `Badge` 可作标签容器;简单标签用 `Text` + `backgroundColor` + `borderRadius` 组合。

## 实现方式

| 方式 | 说明 |
| --- | --- |
| `Text` + 装饰 | 最简单,文字 + 背景色 + 圆角 |
| `Badge` 容器 | 带计数/圆点的标签,可包裹内容 |
| `SymbolGlyph` + `Text` | 图标 + 文字组合标签 |

## 语义配色(参考)

| 语义 | 背景色 | 文字色 |
| --- | --- | --- |
| 主色 | `{color-button-primary-bg}` | `{color-text-on-primary}` |
| 成功 | `{color-success}` | `{color-text-on-primary}` |
| 警告 | `{color-warning}` | `{color-text-on-primary}` |
| 危险 | `{color-danger}` | `{color-text-on-primary}` |
| 信息 | `{color-info}` | `{color-text-on-primary}` |
| 中性 | `{color-bg-secondary}` | `{color-text-primary}` |

## 最小示例

```arkts
@Entry
@Component
struct TagDemo {
  build() {
    Row({ space: {spacing-sm} }) {
      Text('新品')
        .fontSize({font-size-xs})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-button-primary-bg})
        .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
        .borderRadius({radius-sm})
      Text('热门')
        .fontSize({font-size-xs})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-danger})
        .padding({ left: {spacing-sm}, right: {spacing-sm}, top: 2, bottom: 2 })
        .borderRadius({radius-sm})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`badge`](../badge/component.md) — 徽章(带计数)
- [`card`](../card/component.md) — 卡片上常挂标签

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为组合方案)
- 相关组件:[`badge`](../badge/component.md)
- Badge 组件见通用属性文档
