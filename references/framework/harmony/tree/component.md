# Tree 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Tree 树形控件。** 通过 `List` + 递归 `@Builder` + 缩进实现树形结构。

## 缺失原因

ArkTS 没有 Element `<el-tree>` 那样的原生树控件。树本质是递归列表,用 `List` 承载节点,通过缩进(`margin.left`)与展开/折叠状态表达层级关系。

## 替代方案

- **方案 1:List + 递归 @Builder** — 定义递归 builder,根据节点 children 渲染子节点,缩进表达层级。最灵活。
- **方案 2:扁平化 List** — 维护扁平化数组(含 level 字段),展开/折叠时重算数组,渲染简单。适合大数据量。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:List 递归) |
| Flutter | `TreeView`(第三方包) |
| Element Plus | `<el-tree>` |

## 最小示例

```arkts
interface TreeNode { name: string; children?: TreeNode[] }

@Entry
@Component
struct TreeDemo {
  private data: TreeNode[] = [
    { name: '根', children: [{ name: '子1' }, { name: '子2' }] }
  ]
  build() {
    List() {
      ForEach(this.data, (node: TreeNode) => {
        ListItem() { TreeNodeItem({ node: node, level: 0 }) }
      })
    }
    .padding({spacing-md})
  }
}

@Component
struct TreeNodeItem {
  @Prop node: TreeNode
  @Prop level: number
  @State expanded: boolean = false
  build() {
    Column() {
      Row() {
        if (this.node.children?.length) {
          SymbolGlyph(this.expanded ? $r('sys.symbol.chevron_down') : $r('sys.symbol.chevron_right'))
            .fontSize({font-size-sm})
        }
        Text(this.node.name).fontSize({font-size-md})
      }
      .width('100%')
      .padding({ left: this.level * 16, top: {spacing-xs}, bottom: {spacing-xs} })
      .onClick(() => this.expanded = !this.expanded)

      if (this.expanded && this.node.children?.length) {
        ForEach(this.node.children, (child: TreeNode) => {
          TreeNodeItem({ node: child, level: this.level + 1 })
        })
      }
    }
  }
}
```

## 关联组件

- [`list`](../list/component.md) — 树基于 List
- [`collapse`](../collapse/component.md) — 折叠/展开机制

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`list`](../list/component.md)
- 创建列表 (List): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list
