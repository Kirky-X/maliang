# Button 使用场景与示例

> 列举 HarmonyOS 应用中 Button 组件的典型使用场景、完整代码示例与注意事项。所有颜色值通过 design token 引用,不硬编码。

## 场景 1:主操作按钮(Primary Action)

主操作按钮用于触发页面核心动作,如"登录"、"提交"、"确认"。视觉权重最高,采用胶囊形 + 主色背景。

```arkts
@Entry
@Component
struct PrimaryButtonPage {
  build() {
    Column() {
      Button('登录')
        .type(ButtonType.Capsule)
        .fontSize({font-size-md})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-button-primary-bg})
        .width('100%')
        .height(48)
        .onClick(() => {
          // 触发登录逻辑
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:次操作按钮(线框样式)

次操作按钮用于辅助操作(取消、返回),采用线框样式降低视觉权重,常与主按钮成对出现。

```arkts
@Entry
@Component
struct SecondaryButtonPage {
  build() {
    Row() {
      Button('取消')
        .type(ButtonType.Capsule)
        .fontSize({font-size-md})
        .fontColor({color-text-primary})
        .backgroundColor({color-bg-transparent})
        .border({ width: 1, color: {color-border-default} })
        .onClick(() => {
          // 取消操作
        })

      Button('确定')
        .type(ButtonType.Capsule)
        .fontSize({font-size-md})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-button-primary-bg})
        .onClick(() => {
          // 确认操作
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:禁用态按钮

表单未填完整或异步操作进行中时,按钮进入禁用态。置 `enabled = false`,框架自动应用 `{opacity-disabled}` 视觉。

```arkts
@Entry
@Component
struct DisabledButtonPage {
  @State isFormValid: boolean = false

  build() {
    Column() {
      Button('提交')
        .type(ButtonType.Capsule)
        .enabled(this.isFormValid)
        .fontSize({font-size-md})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-button-primary-bg})
        .opacity(this.isFormValid ? 1 : {opacity-disabled})
        .onClick(() => {
          // 仅在 isFormValid=true 时触发
        })
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:图标按钮(圆形)

图标按钮使用 `ButtonType.Circle` + 自定义子组件构造,常用于工具栏、导航返回操作。

```arkts
@Entry
@Component
struct IconButtonPage {
  build() {
    Row() {
      Button({ type: ButtonType.Circle }) {
        Image($r('app.media.icon_back'))
          .width(24)
          .height(24)
      }
      .width(48)
      .height(48)
      .backgroundColor({color-bg-secondary})
      .onClick(() => {
        // 返回上一页
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 5:按钮组(底部双按钮)

成组出现的按钮(底部双按钮、向导步骤切换),使用 `Row` 容器配合 `layoutWeight` 均匀分布。

```arkts
@Entry
@Component
struct ButtonGroupPage {
  build() {
    Row() {
      Button('上一步')
        .layoutWeight(1)
        .type(ButtonType.Capsule)
        .fontSize({font-size-md})
        .fontColor({color-text-primary})
        .backgroundColor({color-bg-secondary})

      Button('下一步')
        .layoutWeight(1)
        .type(ButtonType.Capsule)
        .fontSize({font-size-md})
        .fontColor({color-text-on-primary})
        .backgroundColor({color-button-primary-bg})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **避免硬编码颜色** — 所有颜色值必须通过 design token 引用(如 `{color-button-primary-bg}`),便于主题切换与暗色模式适配。
2. **触控区域** — 按钮高度建议 ≥ 44vp,保证触控体验;圆形按钮尺寸建议 ≥ 48vp。
3. **禁用态语义** — 不要用改变颜色模拟禁用,必须使用 `enabled(false)` 属性,框架会自动应用 `{opacity-disabled}` 与无障碍语义。
4. **type 与 borderRadius 冲突** — `ButtonType.Capsule` 与 `ButtonType.Circle` 会忽略 `borderRadius` 设置;只有 `Normal` 类型支持自定义圆角。
5. **stateEffect** — 默认开启按压态视觉反馈;若自定义按压态样式,可设为 `false` 后用 `stateStyles` 控制。
6. **标签国际化** — 直接传字符串仅适用于 Demo;生产代码应使用 `$r('app.string.xxx')` 资源引用以支持多语言。
