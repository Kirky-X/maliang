# Tree Component API Documentation

> **This component is a maliang combined solution; ArkTS has no native Tree control.** Implemented via `List` + recursive `@Builder` + indentation for tree structure.

## Reason for Absence

ArkTS has no native tree control like Element `<el-tree>`. Trees are essentially recursive lists, using `List` to hold nodes, expressing hierarchy through indentation (`margin.left`) and expand/collapse state.

## Alternative Solutions

- **Solution 1: List + recursive @Builder** — define recursive builder, render child nodes based on node children, indentation expresses hierarchy. Most flexible.
- **Solution 2: Flattened List** — maintain flattened array (with level field), recalculate array on expand/collapse, simple rendering. Suitable for large data volumes.

## Cross-Framework Comparison

| Framework | Implementation |
| --- | --- |
| ArkTS | No native (this combined solution: List recursion) |
| Flutter | `TreeView` (third-party package) |
| Element Plus | `<el-tree>` |

## Minimal Example

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

## Related Components

- [`list`](../list/component.md) — Tree based on List
- [`collapse`](../collapse/component.md) — Collapse/expand mechanism

## Reference Links

- ArkTS Official Documentation: No independent chapter (this component is a maliang combined solution)
- Related components: [`list`](../list/component.md)
- Creating Lists (List): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list