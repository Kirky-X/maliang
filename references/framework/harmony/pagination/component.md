# Pagination 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 Pagination 分页组件。** 通过 `Button` 组合 + 状态管理实现分页控件。

## 缺失原因

ArkTS 没有原生分页组件。分页本质是页码按钮组 + 上下页按钮,用 `Row` + `Button` 组合,通过 `@State current` 管理当前页。

## 替代方案

- **方案 1:Row + Button 组合** — 上一页/页码/下一页按钮,数字页码用 `ForEach` 渲染。
- **方案 2:列表下拉加载** — 移动端优先用"加载更多"无限滚动,而非传统分页器。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生(本组合方案:Button 组合) |
| Flutter | 第三方分页包 |
| Element Plus | `<el-pagination>` |

## 最小示例

```arkts
@Entry
@Component
struct PaginationDemo {
  @State current: number = 1
  private total: number = 5
  build() {
    Row({ space: {spacing-sm} }) {
      Button('上一页')
        .enabled(this.current > 1)
        .backgroundColor({color-bg-secondary})
        .fontColor({color-text-primary})
        .onClick(() => this.current--)
      ForEach([1, 2, 3, 4, 5], (n: number) => {
        Button(`${n}`)
          .backgroundColor(this.current === n ? {color-button-primary-bg} : {color-bg-secondary})
          .fontColor(this.current === n ? {color-text-on-primary} : {color-text-primary})
          .onClick(() => this.current = n)
      })
      Button('下一页')
        .enabled(this.current < this.total)
        .backgroundColor({color-bg-secondary})
        .fontColor({color-text-primary})
        .onClick(() => this.current++)
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`list`](../list/component.md) — 列表分页加载
- [`grid`](../grid/component.md) — 网格分页

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`list`](../list/component.md)
- 创建列表 (List): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list
