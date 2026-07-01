# Breadcrumb 使用场景与示例

> ArkTS 无原生 Breadcrumb,本文件给出基于 Row+Text+Icon 的组合实现方案。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:基础面包屑(可点击跳转)

```arkts
@Entry
@Component
struct BasicBreadcrumbPage {
  private crumbs: Array<{ name: string; path: string }> = [
    { name: '首页', path: 'home' },
    { name: '商品列表', path: 'list' },
    { name: '商品详情', path: 'detail' }
  ]
  build() {
    Row({ space: {spacing-xs} }) {
      ForEach(this.crumbs, (c, idx: number) => {
        Text(c.name)
          .fontSize({font-size-sm})
          .fontColor(idx === this.crumbs.length - 1 ? {color-text-primary} : {color-button-primary-bg})
          .onClick(() => {
            if (idx < this.crumbs.length - 1) console.info(`跳转 ${c.path}`)
          })
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

## 场景 2:长面包屑(省略中间)

```arkts
@Entry
@Component
struct EllipsisBreadcrumbPage {
  private crumbs: string[] = ['首页', '分类', '子分类', '子子分类', '详情页']
  build() {
    Row({ space: {spacing-xs} }) {
      // 始终显示首项
      Text(this.crumbs[0])
        .fontSize({font-size-sm}).fontColor({color-button-primary-bg})
      SymbolGlyph($r('sys.symbol.chevron_right')).fontSize({font-size-xs}).fontColor([{color-text-primary}])

      // 中间省略
      if (this.crumbs.length > 3) {
        Text('...')
          .fontSize({font-size-sm}).fontColor({color-text-primary})
        SymbolGlyph($r('sys.symbol.chevron_right')).fontSize({font-size-xs}).fontColor([{color-text-primary}])
      }

      // 倒数第二项
      Text(this.crumbs[this.crumbs.length - 2])
        .fontSize({font-size-sm}).fontColor({color-button-primary-bg})
      SymbolGlyph($r('sys.symbol.chevron_right')).fontSize({font-size-xs}).fontColor([{color-text-primary}])

      // 末项(当前页)
      Text(this.crumbs[this.crumbs.length - 1])
        .fontSize({font-size-sm}).fontColor({color-text-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:封装可复用面包屑

```arkts
interface Crumb { name: string; path?: string }

@Component
struct Breadcrumb {
  private items: Crumb[] = []
  onNavigate: (path: string) => void = () => {}
  build() {
    Row({ space: {spacing-xs} }) {
      ForEach(this.items, (item, idx: number) => {
        Text(item.name)
          .fontSize({font-size-sm})
          .fontColor(idx === this.items.length - 1 ? {color-text-primary} : {color-button-primary-bg})
          .onClick(() => { if (item.path && idx < this.items.length - 1) this.onNavigate(item.path) })
        if (idx < this.items.length - 1) {
          SymbolGlyph($r('sys.symbol.chevron_right'))
            .fontSize({font-size-xs}).fontColor([{color-text-primary}])
        }
      })
    }
  }
}
```

## 注意事项

1. **末级不可点击** — 当前页用 `{color-text-primary}` 区分;非当前页用主色表达可点击。
2. **分隔符方向** — RTL 语言需翻转 chevron 方向;默认 LTR 用 `chevron_right`。
3. **省略中间项** — 层级 > 3 时省略中间,首尾保留;避免横向溢出。
4. **与 Navigation 配合** — 点击用 `pathStack.popToName()` 跳到对应页,而非 push。
5. **移动端慎用** — 移动端空间有限,面包屑主要用于平板/折叠屏;手机端用返回箭头。
6. **无障碍** — 整体设 `accessibilityGroup(true)`,朗读为"首页 商品列表 商品详情"。
