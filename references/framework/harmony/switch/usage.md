# Switch 使用场景与示例

> 列举 ArkTS Toggle 组件的典型使用场景(slug 统一 switch,ArkTS 原生名 Toggle)。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:设置项开关(ToggleType.Switch)

```arkts
@Entry
@Component
struct SettingsSwitchPage {
  @State darkMode: boolean = false
  @State notify: boolean = true
  build() {
    Column() {
      Row() {
        Text('深色模式').fontSize({font-size-md}).layoutWeight(1)
        Toggle({ type: ToggleType.Switch, isOn: this.darkMode })
          .selectedColor({color-button-primary-bg})
          .onChange((v: boolean) => this.darkMode = v)
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})

      Row() {
        Text('消息通知').fontSize({font-size-md}).layoutWeight(1)
        Toggle({ type: ToggleType.Switch, isOn: this.notify })
          .selectedColor({color-success})
          .onChange((v: boolean) => this.notify = v)
      }
      .padding({spacing-md})
      .backgroundColor({color-bg-primary})
    }
  }
}
```

## 场景 2:复选框(ToggleType.Checkbox)

```arkts
@Entry
@Component
struct CheckboxPage {
  @State agree: boolean = false
  build() {
    Row({ space: {spacing-sm} }) {
      Toggle({ type: ToggleType.Checkbox, isOn: this.agree })
        .selectedColor({color-button-primary-bg})
        .onChange((v: boolean) => this.agree = v)
      Text('我已阅读并同意《用户协议》').fontSize({font-size-sm})
        .fontColor({color-text-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:按钮切换(ToggleType.Button)

```arkts
@Entry
@Component
struct ButtonTogglePage {
  @State grid: boolean = false
  build() {
    Row({ space: {spacing-sm} }) {
      Toggle({ type: ToggleType.Button, isOn: !this.grid })
        .selectedColor({color-button-primary-bg})
        .onChange((v: boolean) => { if (v) this.grid = false })
      Text('列表').fontSize({font-size-sm})

      Toggle({ type: ToggleType.Button, isOn: this.grid })
        .selectedColor({color-button-primary-bg})
        .onChange((v: boolean) => { if (v) this.grid = true })
      Text('网格').fontSize({font-size-sm})
    }
    .padding({spacing-md})
  }
}
```

## 场景 4:多选列表(Checkbox + List)

```arkts
@Entry
@Component
struct MultiSelectPage {
  private items: string[] = ['苹果', '香蕉', '橙子', '葡萄']
  @State checked: boolean[] = [false, false, false, false]
  build() {
    Column({ space: {spacing-sm} }) {
      ForEach(this.items, (item: string, idx: number) => {
        Row() {
          Text(item).fontSize({font-size-md}).layoutWeight(1)
          Toggle({ type: ToggleType.Checkbox, isOn: this.checked[idx] })
            .selectedColor({color-button-primary-bg})
            .onChange((v: boolean) => this.checked[idx] = v)
        }
        .padding({spacing-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
      })
      Text(`已选 ${this.checked.filter(x => x).length} 项`)
        .fontSize({font-size-sm}).fontColor({color-text-primary})
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **selectedColor 区别** — Switch 形态是开启态轨道色;Checkbox 是勾选框色;Button 是选中态背景色。
2. **isOn 单向控制** — `isOn` 需绑定 `@State`,在 `onChange` 中更新;否则点击后状态不持久。
3. **Checkbox 多选独立** — 每个 Checkbox 独立 `isOn`,不像 Radio 互斥;多选用数组管理状态。
4. **Button 形态互斥需手动** — ToggleType.Button 不自动互斥,多个按钮单选需在 onChange 手动处理。
5. **switchPointColor** — 仅 Switch 形态有效,控制圆点颜色;其他形态忽略。
6. **协议勾选** — 表单提交前校验 `agree` 必须为 true,否则禁用提交按钮。
