# Collapse 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Collapse 折叠面板组件。** 通过 `List` + `if` 条件渲染 + 展开状态管理实现。

## 缺失原因

ArkTS 没有原生折叠面板(类似 Ant Design `<Collapse>`)。折叠本质是点击标题切换内容显隐,用 `if (expanded)` 控制内容区渲染,配合 `transition` 动画。

## 替代方案

- **方案 1:List + if 条件渲染** — 每个 `ListItem` 标题点击切换 `@State expanded`,内容区用 `if` 控制。
- **方案 2:Column + transition 动画** — 用 `transition` 给展开/收起加渐显动画,体验更流畅。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:List+if) |
| Flutter | `ExpansionTile` |
| Element Plus | `<el-collapse>` |

## 最小示例

```arkts
@Entry
@Component
struct CollapseDemo {
  @State expanded: boolean = false
  build() {
    Column() {
      Row() {
        Text('标题').fontSize({font-size-md}).layoutWeight(1)
        SymbolGlyph(this.expanded ? $r('sys.symbol.chevron_down') : $r('sys.symbol.chevron_right'))
          .fontColor([{color-text-primary}])
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
      .onClick(() => this.expanded = !this.expanded)

      if (this.expanded) {
        Text('折叠内容,点击标题展开/收起。')
          .fontSize({font-size-sm})
          .padding({spacing-md})
          .backgroundColor({color-bg-secondary})
      }
    }
  }
}
```

## 关联组件

- [`list`](../list/component.md) — 折叠基于 List
- [`animation`](../animation/component.md) — 展开动画 transition
- [`tree`](../tree/component.md) — 树形展开机制类似

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`list`](../list/component.md) / [`animation`](../animation/component.md)
- 创建列表 (List): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list
