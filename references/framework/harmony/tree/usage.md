# Tree Usage Scenarios and Examples

> ArkTS does not have a native Tree component. This file provides a combined implementation solution based on List recursion. All colors, spacing, and border-radius are referenced via design tokens.

## Scenario 1: File Directory Tree

```arkts
interface TreeNode { name: string; children?: TreeNode[]; isLeaf?: boolean }

@Component
struct TreeItem {
  @Prop node: TreeNode
  @Prop level: number
  @State expanded: boolean = false
  build() {
    Column() {
      Row({ space: {spacing-sm} }) {
        if (!this.node.isLeaf) {
          SymbolGlyph(this.expanded ? $r('sys.symbol.chevron_down') : $r('sys.symbol.chevron_right'))
            .fontSize({font-size-sm})
            .fontColor([{color-text-primary}])
            .onClick(() => this.expanded = !this.expanded)
        }
        SymbolGlyph(this.node.isLeaf ? $r('sys.symbol.doc') : $r('sys.symbol.folder'))
          .fontSize({font-size-sm})
          .fontColor([{color-warning}])
        Text(this.node.name).fontSize({font-size-md})
      }
      .width('100%')
      .padding({ left: this.level * 20, top: {spacing-xs}, bottom: {spacing-xs} })
      .onClick(() => { if (!this.node.isLeaf) this.expanded = !this.expanded })

      if (this.expanded && this.node.children) {
        ForEach(this.node.children, (child: TreeNode) => {
          TreeItem({ node: child, level: this.level + 1 })
        })
      }
    }
  }
}

@Entry
@Component
struct FileTreePage {
  private data: TreeNode[] = [
    {
      name: 'src', children: [
        { name: 'main', children: [{ name: 'index.ets', isLeaf: true }] },
        { name: 'test', children: [{ name: 'test.ets', isLeaf: true }] }
      ]
    },
    { name: 'README.md', isLeaf: true }
  ]
  build() {
    List() {
      ForEach(this.data, (node: TreeNode) => {
        ListItem() { TreeItem({ node: node, level: 0 }) }
      })
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
  }
}
```

## Scenario 2: Organization Chart Tree (with Selection)

```arkts
@Component
struct OrgTreeItem {
  @Prop node: TreeNode
  @Prop level: number
  @State expanded: boolean = true
  @State checked: boolean = false
  build() {
    Column() {
      Row({ space: {spacing-sm} }) {
        Toggle({ type: ToggleType.Checkbox, isOn: this.checked })
          .selectedColor({color-button-primary-bg})
          .onChange((v: boolean) => this.checked = v)
        Text(this.node.name).fontSize({font-size-md}).layoutWeight(1)
        if (this.node.children?.length) {
          SymbolGlyph(this.expanded ? $r('sys.symbol.chevron_down') : $r('sys.symbol.chevron_right'))
            .fontSize({font-size-sm})
            .onClick(() => this.expanded = !this.expanded)
        }
      }
      .padding({ left: this.level * 20, top: {spacing-xs}, bottom: {spacing-xs} })
      if (this.expanded && this.node.children) {
        ForEach(this.node.children, (c: TreeNode) => {
          OrgTreeItem({ node: c, level: this.level + 1 })
        })
      }
    }
  }
}
```

## Notes

1. **@Prop is one-way** — tree nodes use `@Prop` to pass data, avoid child components modifying parent data; expand state uses child component `@State`.
2. **Recursive @Component** — tree node component self-references to render children; ArkTS supports component recursion.
3. **Large data uses flattening** — deep hierarchy/multi-node recursion may cause stack overflow; flattened array (with parentId/level) rendering is more stable.
4. **Lazy load child nodes** — when node children are loaded asynchronously, trigger request on expand, update `@State` after loading.
5. **Indentation uses margin left** — `padding({ left: level * 20 })` expresses hierarchy; avoid using nested Column to increase depth.
6. **Parent-child linkage** — parent check linking to children requires manual traversal logic; complex scenarios recommend flattening + Map management.