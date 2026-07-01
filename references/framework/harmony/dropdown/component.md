# Dropdown 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Dropdown 下拉选择。** 通过 `Button` + `bindMenu`(或 `Menu` + `MenuItem`)组合实现。

## 缺失原因

ArkTS 没有原生 `<select>` 风格的下拉选择器。下拉本质是触发按钮 + 弹出菜单,用 `Button` 触发 `bindMenu`,选中后更新按钮文字。

## 替代方案

- **方案 1:Button + bindMenu** — 最简洁,点击按钮弹出菜单,选中更新状态。适合选项少且固定的场景。
- **方案 2:Select 组件(API 10+)** — 部分版本有 `Select` 组件,内置下拉;若可用优先使用。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:Button+Menu) |
| Flutter | `DropdownButton` |
| Element Plus | `<el-select>` |

## 最小示例

```arkts
@Entry
@Component
struct DropdownDemo {
  @State picked: string = '请选择'
  private opts: string[] = ['选项1', '选项2', '选项3']
  build() {
    Button(this.picked)
      .backgroundColor({color-bg-primary})
      .fontColor({color-text-primary})
      .bindMenu(this.opts.map(o => ({
        value: o,
        action: () => this.picked = o
      })))
  }
}
```

## 关联组件

- [`menu`](../menu/component.md) — 下拉基于 Menu
- [`input`](../input/component.md) — 搜索型下拉可配合 Search

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`menu`](../menu/component.md)
- 菜单控制 (Menu): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-popup-and-menu-components-menu
