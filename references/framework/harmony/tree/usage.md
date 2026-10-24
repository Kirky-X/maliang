# Tree 使用场景与示例

> ArkTS 无原生 Tree 组件。本文件提供基于 List 递归的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:文件目录树

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

## 场景 2:组织架构树(带选择)

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

## 注意事项

1. **@Prop 单向** — 树节点用 `@Prop` 传递数据,避免子组件修改父组件数据;展开状态用子组件 `@State`。
2. **递归 @Component** — 树节点组件自引用渲染子节点;ArkTS 支持组件递归。
3. **大数据量用扁平化** — 层级深/节点多时递归可能栈溢出;用扁平数组(含 parentId/level)渲染更稳定。
4. **懒加载子节点** — 节点 children 异步加载时,展开时触发请求,加载完成后再更新 `@State`。
5. **缩进用 margin left** — 用 `padding({ left: level * 20 })` 表达层级;避免用嵌套 Column 增加深度。
6. **父子联动** — 父选中联动子节点需手动遍历逻辑;复杂场景建议扁平化 + Map 管理。
