# Breadcrumb 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 部分支持(无原生 Breadcrumb)。** 通过 `Text` + 分隔符图标(`SymbolGlyph`)组合实现面包屑导航。

## 缺失原因

ArkTS 没有原生面包屑组件。面包屑本质是水平排列的文字链 + 分隔符,用 `Row` + `Text` + `SymbolGlyph` 组合,点击触发路由返回即可。

## 替代方案

- **方案 1:Row + Text + SymbolGlyph** — 横向排列,分隔符用 `chevron-right` 图标,末级为不可点击文字。
- **方案 2:Navigation title 区** — Navigation 组件的标题栏可显示层级,但样式固定。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:Row+Text+Icon) |
| Flutter | `Breadcrumbs`(第三方) |
| Element Plus | `<el-breadcrumb>` |

## 最小示例

```arkts
@Entry
@Component
struct BreadcrumbDemo {
  private crumbs: string[] = ['首页', '商品', '详情']
  build() {
    Row({ space: {spacing-xs} }) {
      ForEach(this.crumbs, (c: string, idx: number) => {
        Text(c)
          .fontSize({font-size-sm})
          .fontColor(idx === this.crumbs.length - 1 ? {color-text-primary} : {color-button-primary-bg})
        if (idx < this.crumbs.length - 1) {
          SymbolGlyph($r('sys.symbol.chevron_right'))
            .fontSize({font-size-xs})
            .fontColor([{color-text-primary}])
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`navigation`](../navigation/component.md) — 面包屑触发页面跳转
- [`icon`](../icon/component.md) — 分隔符图标

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`navigation`](../navigation/component.md)
- 组件导航 (Navigation): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-navigation-navigation
