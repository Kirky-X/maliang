# A11y 使用场景与示例

> 列举 ArkTS 无障碍与适老化的典型使用场景。所有颜色、间距通过 design token 引用。

## 场景 1:纯图标按钮(必须设 accessibilityText)

读屏无法朗读图标,必须补充语义文案。

```arkts
@Entry
@Component
struct IconBtnA11yPage {
  build() {
    Row() {
      Button({ type: ButtonType.Circle }) {
        Image($r('app.media.icon_back')).width(24).height(24)
      }
      .width(48).height(48)
      .backgroundColor({color-bg-secondary})
      .accessibilityText('返回')
      .accessibilityDescription('返回上一页')
      .accessibilityRole(AccessibilityRole.BUTTON)
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:合并子节点(accessibilityGroup)

卡片整体作为一个焦点,而非逐个子元素朗读。

```arkts
@Entry
@Component
struct GroupA11yPage {
  build() {
    Column() {
      Text('商品标题').fontSize({font-size-md})
      Text('¥99').fontSize({font-size-sm}).fontColor({color-danger})
    }
    .padding({spacing-md})
    .backgroundColor({color-bg-primary})
    .borderRadius({radius-md})
    .accessibilityGroup(true)
    .accessibilityText('商品标题,价格99元')
    .accessibilityLevel('yes')
  }
}
```

## 场景 3:开关无障碍(accessibilityChecked)

```arkts
@Entry
@Component
struct ToggleA11yPage {
  @State on: boolean = false
  build() {
    Row() {
      Text('深色模式').fontSize({font-size-md})
      Toggle({ type: ToggleType.Switch, isOn: this.on })
        .onChange((v: boolean) => this.on = v)
        .accessibilityText('深色模式开关')
        .accessibilityChecked(this.on)
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:字体随系统放大(fp 单位)

```arkts
@Entry
@Component
struct LargeTextPage {
  build() {
    Text('适老化大字')
      .fontSize('20fp')  // fp 跟随系统字号缩放
      .padding({spacing-md})
  }
}
```

## 场景 5:焦点导航(tabIndex)

```arkts
@Entry
@Component
struct FocusNavPage {
  build() {
    Column({ space: {spacing-md} }) {
      TextInput({ placeholder: '输入1' }).focusOnTouch(true).tabIndex(1)
      TextInput({ placeholder: '输入2' }).focusOnTouch(true).tabIndex(2)
      Button('提交').tabIndex(3)
        .backgroundColor({color-button-primary-bg})
        .fontColor({color-text-on-primary})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **图标必设 accessibilityText** — 纯图标按钮缺语义,读屏只会读"按钮",无法表达功能。
2. **accessibilityGroup** — 卡片/列表项设为 true,避免逐个朗读子元素造成噪音。
3. **fp vs vp** — 字号用 `fp` 跟随系统字号;尺寸间距用 `vp` 不缩放,保证布局稳定。
4. **accessibilityLevel 'no'** — 装饰性元素(背景图/分隔线)设为 'no' 跳过朗读。
5. **对比度** — 文字与背景对比度建议 ≥ 4.5:1;深色模式尤其注意。
6. **勾选状态同步** — 开关类组件需 `accessibilityChecked(state)` 同步状态,读屏才能正确播报"已勾选"。
