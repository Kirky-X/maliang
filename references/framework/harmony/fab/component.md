# FloatingActionButton 组件 API 文档

> **本组件为 maliang 组合方案,ArkTS 无原生 FAB 悬浮按钮组件。** 通过 `Stack` 右下角定位 + 圆形 `Button`(或 `SymbolGlyph` 图标)组合实现移动端"新建/发布/写"一级操作入口。

## 缺失原因

ArkUI 未提供 Material 风格的 FloatingActionButton;悬浮操作入口由 Stack 层叠 + 圆形按钮组合表达。

## 替代方案(组合结构)

| 角色 | ArkTS 实现 |
| --- | --- |
| 悬浮定位 | `Stack`(alignContent: BottomEnd)+ margin |
| 按钮 | `Button`(type: Circle)+ `SymbolGlyph`/图标 |
| 出现/收起联动 | 监听 `Scroller.onScroll` 驱动 `@State` 显隐 + `animateTo` |
| 扩展 FAB(带文案) | 胶囊 `Button`(图标 + 文本) |

## 组合结构

```arkts
// FAB 状态
@State fabVisible: boolean = true
@State scroller: Scroller = new Scroller()

// 滚动联动:下滑显示、上滑收起(见 usage.md 场景 2)
```

## 最小示例

```arkts
@Entry
@Component
struct FabDemo {
  build() {
    Stack({ alignContent: Alignment.BottomEnd }) {
      Column() {
        Text('列表主体').fontSize({font-size-md})
      }
      .width('100%')
      .layoutWeight(1)

      Button() {
        SymbolGlyph($r('sys.symbol.plus'))
          .fontSize(24)
          .fontColor([({color-text-inverse})])
      }
      .type(ButtonType.Circle)
      .width(56)
      .height(56)
      .backgroundColor({color-primary})
      .shadow({ radius: 8, color: 'rgba(0,0,0,0.15)', offsetY: 2 })
      .margin({ right: {spacing-lg}, bottom: {spacing-xxl} })
      .onClick(() => {
        // 打开新建页
      })
    }
    .width('100%')
    .height('100%')
  }
}
```

## 关联组件

- [`button`](../button/component.md) — 按钮基础
- [`navigation`](../navigation/component.md) — 与底部导航的层级与避让关系

## 参考链接

- Material 3 - FAB 规范参考: https://m3.material.io/components/floating-action-button
- ArkTS API 参考 - Stack: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-container-stack
