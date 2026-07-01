# Drawer 使用场景与示例

> 列举 ArkTS 抽屉/模态页的典型使用场景(slug 统一 drawer,原生 bindSheet/bindContentCover)。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:半模态选择器(bindSheet)

```arkts
@Entry
@Component
struct SheetSelectPage {
  @State show: boolean = false
  @State picked: string = ''
  private items: string[] = ['北京', '上海', '广州', '深圳']
  build() {
    Column() {
      Text(`已选: ${this.picked || '请选择'}`).fontSize({font-size-md})
      Button('选择城市')
        .onClick(() => this.show = true)
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
        .bindSheet(this.show, this.sheetContent, {
          detents: [SheetSize.MEDIUM, SheetSize.LARGE],
          showClose: true,
          backgroundColor: {color-bg-primary}
        })
    }
    .padding({spacing-md})
  }

  @Builder sheetContent() {
    Column({ space: {spacing-sm} }) {
      Text('选择城市').fontSize({font-size-lg}).padding({spacing-md})
      ForEach(this.items, (city: string) => {
        Text(city)
          .width('100%')
          .padding({spacing-md})
          .fontSize({font-size-md})
          .backgroundColor(this.picked === city ? {color-bg-secondary} : {color-bg-primary})
          .onClick(() => { this.picked = city; this.show = false })
      })
    }
  }
}
```

## 场景 2:全屏模态(bindContentCover)

```arkts
@Entry
@Component
struct FullCoverPage {
  @State show: boolean = false
  build() {
    Column() {
      Button('打开全屏')
        .onClick(() => this.show = true)
        .bindContentCover(this.show, this.fullBuilder, {
          modalTransition: ModalTransition.DEFAULT
        })
    }
    .padding({spacing-md})
  }

  @Builder fullBuilder() {
    Column() {
      Text('全屏内容').fontSize({font-size-xl}).fontColor({color-text-on-primary})
      Button('关闭')
        .onClick(() => this.show = false)
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .width('100%').height('100%')
    .backgroundColor({color-bg-secondary})
    .padding({spacing-lg})
  }
}
```

## 场景 3:多档位拖拽(detents)

```arkts
@Entry
@Component
struct DetentsSheetPage {
  @State show: boolean = false
  build() {
    Column() {
      Button('打开')
        .onClick(() => this.show = true)
        .bindSheet(this.show, this.content, {
          detents: [200, 400, SheetSize.LARGE],
          showClose: false
        })
    }
    .padding({spacing-md})
  }

  @Builder content() {
    Text('可上下拖拽高度').padding({spacing-lg}).fontSize({font-size-md})
  }
}
```

## 场景 4:拦截关闭(shouldDismiss)

```arkts
.bindSheet(this.show, this.content, {
  detents: [SheetSize.MEDIUM],
  shouldDismiss: (sheetDismiss: SheetDismiss) => {
    if (this.unsaved) {
      // 阻止关闭,提示用户
      promptAction.showToast({ message: '请先保存' })
    } else {
      sheetDismiss.dismiss()
    }
  }
})
```

## 场景 5:侧边抽屉(SideBarContainer)

```arkts
@Entry
@Component
struct SideBarPage {
  build() {
    SideBarContainer(SideBarContainerType.Embed) {
      Column() {
        Text('侧边菜单').fontSize({font-size-md})
        Text('设置').fontSize({font-size-sm}).padding({spacing-sm})
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-secondary})

      Column() {
        Text('主内容').fontSize({font-size-md})
      }
      .padding({spacing-md})
    }
    .showSideBar(true)
  }
}
```

## 注意事项

1. **bindSheet 是绑定属性** — 写在触发组件上,非独立组件;builder 传入 `@Builder`。
2. **detents 档位** — 数组定义可拖拽到的多个高度;用户拖拽吸附到最近档位。
3. **bindContentCover 全屏** — 用于详情/编辑等需全屏的模态;半模态用 bindSheet。
4. **shouldDismiss 拦截** — 表单未保存时拦截关闭,提示用户;`sheetDismiss.dismiss()` 显式放行。
5. **builder 内状态** — builder 内引用父组件 `@State` 需注意作用域;复杂逻辑建议抽为子组件。
6. **SideBarContainer 适合平板** — 分栏侧栏;手机端推荐 bindSheet。
