# Layout 使用场景与示例

> 列举 ArkTS 布局容器的典型使用场景。所有颜色、间距、圆角通过 design token 引用,不硬编码。

## 场景 1:垂直表单布局(Column)

表单字段纵向排列,使用 `Column` 容器配合 `justifyContent` 与间距。

```arkts
@Entry
@Component
struct FormLayoutPage {
  build() {
    Column({ space: {spacing-md} }) {
      TextInput({ placeholder: '用户名' })
        .height(48)
      TextInput({ placeholder: '密码' })
        .height(48)
      Button('登录')
        .width('100%')
    }
    .padding({spacing-lg})
  }
}
```

## 场景 2:水平双栏(Row + layoutWeight)

底部双按钮均分宽度,使用 `layoutWeight` 分配剩余空间。

```arkts
@Entry
@Component
struct RowWeightPage {
  build() {
    Row() {
      Button('取消')
        .layoutWeight(1)
        .backgroundColor({color-bg-secondary})
        .fontColor({color-text-primary})
      Button('确认')
        .layoutWeight(1)
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:层叠布局(Stack)

在背景之上叠加内容,如头像角标、封面叠加播放按钮。

```arkts
@Entry
@Component
struct StackPage {
  build() {
    Stack({ alignContent: Alignment.BottomEnd }) {
      Image($r('app.media.cover'))
        .width('100%').height(200)
        .borderRadius({radius-lg})
      Text('HD')
        .fontSize({font-size-xs})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-danger})
        .padding({spacing-xs})
        .borderRadius({radius-sm})
        .margin({spacing-sm})
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:相对布局(RelativeContainer)

通过锚点对齐,适合复杂相对关系场景。

```arkts
@Entry
@Component
struct RelativePage {
  build() {
    RelativeContainer() {
      Text('标题')
        .id('title')
        .fontSize({font-size-lg})
      Text('副标题')
        .id('subtitle')
        .fontSize({font-size-sm})
        .fontColor({color-text-primary})
        .alignRules({ top: { anchor: 'title', align: VerticalAlign.Bottom } })
    }
    .width('100%')
    .padding({spacing-md})
  }
}
```

## 场景 5:响应式栅格(GridRow/GridCol)

根据断点切换列数,适配折叠屏/平板。

```arkts
@Entry
@Component
struct GridRowPage {
  build() {
    GridRow({ breakpoints: { value: ['600vp', '840vp'] } }) {
      ForEach([1, 2, 3, 4], (item: number) => {
        GridCol({ span: { sm: 6, md: 4, lg: 3 } }) {
          Column() {
            Text(`卡片${item}`)
          }
          .padding({spacing-md})
          .backgroundColor({color-bg-secondary})
          .borderRadius({radius-md})
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **layoutWeight 仅在线性主轴生效** — `Row` 控制水平权重,`Column` 控制垂直权重,交叉轴无效。
2. **Stack 默认居中** — 用 `alignContent` 改变子节点对齐,否则所有子节点堆叠在中心。
3. **RelativeContainer 必须设 id** — 被引用为锚点的子节点需通过 `.id('xxx')` 声明,否则 alignRules 失效。
4. **GridRow 断点** — 默认断点 `sm/md/lg`,通过 `breakpoints` 自定义阈值;`span` 控制每列占用的栅格数(共 12 格)。
5. **嵌套层级** — 避免超过 5 层嵌套,层级过深影响性能与可读性。
6. **Flex 与 Row/Column** — `Flex` 支持换行与收缩,功能更全但开销略大;简单线性排列优先用 `Row`/`Column`。
