# Radio 使用场景与示例

> 列举 ArkTS 单选框组件的典型使用场景。所有颜色、间距、圆角通过 design token 引用。

## 场景 1:性别选择(RadioGroup)

```arkts
@Entry
@Component
struct GenderRadioPage {
  @State gender: string = 'male'
  build() {
    Column({ space: {spacing-md} }) {
      Text('性别').fontSize({font-size-md})
      RadioGroup({ group: 'gender' }) {
        Row({ space: {spacing-lg} }) {
          Row({ space: {spacing-sm} }) {
            Radio({ group: 'gender', value: 'male' }).checked(this.gender === 'male')
            Text('男').fontSize({font-size-md})
          }
          Row({ space: {spacing-sm} }) {
            Radio({ group: 'gender', value: 'female' }).checked(this.gender === 'female')
            Text('女').fontSize({font-size-md})
          }
        }
      }
      .onChange((v: string) => this.gender = v)
      Text(`已选: ${this.gender}`).fontSize({font-size-sm}).fontColor({color-text-primary})
    }
    .padding({spacing-md})
  }
}
```

## 场景 2:列表式单选(ForEach)

```arkts
@Entry
@Component
struct ListRadioPage {
  private opts: string[] = ['选项一', '选项二', '选项三', '选项四']
  @State selected: string = '选项一'
  build() {
    Column({ space: {spacing-sm} }) {
      ForEach(this.opts, (opt: string) => {
        Row() {
          Text(opt).fontSize({font-size-md}).layoutWeight(1)
          Radio({ group: 'opts', value: opt }).checked(this.selected === opt)
        }
        .width('100%')
        .padding({spacing-md})
        .backgroundColor({color-bg-primary})
        .borderRadius({radius-md})
        .onClick(() => this.selected = opt)
      })
    }
    .padding({spacing-md})
  }
}
```

## 场景 3:卡片式单选

```arkts
@Entry
@Component
struct CardRadioPage {
  private items: string[] = ['基础版', '专业版', '企业版']
  @State picked: string = '基础版'
  build() {
    Column({ space: {spacing-sm} }) {
      ForEach(this.items, (item: string) => {
        Row() {
          Column() {
            Text(item).fontSize({font-size-md})
            Text('¥99/月').fontSize({font-size-sm}).fontColor({color-text-primary})
          }.alignItems(HorizontalAlign.Start).layoutWeight(1)
          Radio({ group: 'plan', value: item }).checked(this.picked === item)
        }
        .padding({spacing-md})
        .backgroundColor(this.picked === item ? {color-bg-secondary} : {color-bg-primary})
        .borderRadius({radius-md})
        .border({
          width: this.picked === item ? 2 : 0,
          color: {color-button-primary-bg}
        })
        .onClick(() => this.picked = item)
      })
    }
    .padding({spacing-md})
  }
}
```

## 注意事项

1. **group 必须一致** — 同组 Radio 必须用相同 group 名才能互斥;否则各选各的。
2. **checked 与 onChange** — `checked` 单向控制选中态;`onChange` 回调手动更新 `@State`。
3. **RadioGroup 自动管理** — 用 `RadioGroup` 包裹时,组内 Radio 互斥由容器管理,无需手动判断。
4. **onClick 替代点 Radio** — 列表式单选常在 Row 上设 onClick,点击整行触发选中,体验更好。
5. **value 是字符串** — Radio 的 value 仅支持 string;复杂对象需建立 value→object 映射表。
6. **无障碍** — 单选组建议设 `accessibilityRole(Radio)`,配合 `accessibilityChecked` 同步状态。
