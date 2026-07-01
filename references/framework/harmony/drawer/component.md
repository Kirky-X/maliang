# Drawer 组件 API 文档

> ArkTS 抽屉/模态页组件。**注意:目录 slug 统一用 `drawer`,ArkTS 原生能力为 `bindSheet`(半模态)/ `bindContentCover`(全模态)。**

## 组件定义

| 能力 | API | 形态 |
| --- | --- | --- |
| 半模态页面 | `bindSheet(show, builder, options)` | 底部弹出,可拖拽高度 |
| 全模态页面 | `bindContentCover(show, builder, options)` | 全屏覆盖 |
| 侧边抽屉 | 自定义 `SideBarContainer` | 侧边滑出 |

## bindSheet 核心配置(BindSheetOptions)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| height | Length | 半模态高度 |
| detents | SheetSize[] | 可拖拽到的多个高度档位 |
| backgroundColor | ResourceColor | 背景色 |
| blurStyle | BlurStyle | 蒙层模糊 |
| showClose | boolean | 是否显示关闭按钮 |
| preferType | SheetMode | AUTO/FIT(自适应) |
| onDisappear | () => void | 关闭回调 |
| shouldDismiss | (action) => void | 拦截关闭 |

## bindContentCover 核心配置

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| modalTransition | ModalTransition | DEFAULT/NONE/ALPHA |
| backgroundColor | ResourceColor | 背景色 |
| onDisappear | () => void | 关闭回调 |

## 最小示例

```arkts
@Entry
@Component
struct DrawerDemo {
  @State show: boolean = false
  build() {
    Column() {
      Button('打开抽屉')
        .onClick(() => this.show = true)
        .bindSheet(this.show, this.sheetBuilder, {
          detents: [SheetSize.MEDIUM, SheetSize.LARGE],
          showClose: true
        })
    }
    .padding({spacing-md})
  }

  @Builder sheetBuilder() {
    Column() {
      Text('抽屉内容').fontSize({font-size-lg})
    }
    .padding({spacing-lg})
  }
}
```

## 关联组件

- [`dialog`](../dialog/component.md) — 弹窗(中心弹窗)
- [`navigation`](../navigation/component.md) — 页面导航

## 参考链接

- ArkTS 官方文档 - 绑定模态页面: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-bind-modal
- 绑定半模态页面 (bindSheet): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-sheet-page
- 绑定全模态页面 (bindContentCover): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-contentcover-page
