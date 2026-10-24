# Steps 步骤条组件 API 文档

> **基线结论(ArkUI 有原生组件)**:ArkUI 官方提供 `Stepper`/`StepperItem` 步骤导航器组件(API 8 起支持,基线 API 20 内可用;API 22 起废弃,官方建议用 `Swiper` 自定义替代,弃用说明见参考链接)。注意语义差异:`Stepper` 是**整页步骤导航器**(wizard,一屏一步),与 Element `<el-steps>` 的**页内联指示条**并非严格等价物;页内指示条场景用下方组合方案。

## 缺失原因(准确表述)

- 原生存在:`Stepper`/`StepperItem`(API 8+,API 22 起废弃)——**整页向导**语义,每步独占一屏,由组件自身管理步骤切换与手势。
- 需要组合的场景:**页内联步骤指示条**(同屏多步进度,类似 `<el-steps>`/`el-step`)没有等价原生组件——节点(圆/图标)+连接线+文字,用 `Row`(横)/`Column`(竖)+ `ForEach` 组合实现,即本文件的最小示例。
- 基线路径选择:向导式流程 → 优先 `Stepper`(基线内可用;升级前评估 `Swiper` 替代);页内指示条 → 组合方案。

## 替代方案

- **方案 1(基线首选):`Stepper` + `StepperItem`** —— 整页向导(注册/下单流程),原生手势与无障碍能力免费;API 22 起废弃,新项目在基线内可用,升级时评估方案 2。
- **方案 2(基线备选):`Swiper` 自定义步骤页** —— 官方弃用 `Stepper` 后建议的替代路径,`Swiper` 翻页 + 自绘指示条组合。
- **方案 3(页内联指示条):Row + Icon + 连接线(横)** —— 节点用 `Circle` 或 `SymbolGlyph`,连接线用 `Divider`/`Column`。
- **方案 4(竖向):Column + 连接线** —— 竖向步骤,结构同 timeline。

## 步骤状态语义

| 状态 | 节点样式 | 颜色 |
| --- | --- | --- |
| finish(已完成) | 对勾图标 | `{color-success}` |
| process(进行中) | 数字/高亮 | `{color-button-primary-bg}` |
| wait(未开始) | 数字/灰 | `{color-bg-secondary}` |

## 跨框架对照

| 框架 | 实现 |
| --- | --- |
| ArkTS | 原生 `Stepper`/`StepperItem`(整页向导,API 22 起废弃);页内联指示条用本组合方案(Row+Icon) |
| Flutter | 第三方 steps 包 |
| Element Plus | `<el-steps>` |

## 最小示例

```arkts
@Entry
@Component
struct StepsDemo {
  private steps: string[] = ['下单', '付款', '发货', '收货']
  @State current: number = 1
  build() {
    Row() {
      ForEach(this.steps, (step: string, idx: number) => {
        Column({ space: {spacing-xs} }) {
          Circle({ width: 24, height: 24 })
            .fill(idx <= this.current ? {color-button-primary-bg} : {color-bg-secondary})
          Text(step).fontSize({font-size-xs})
            .fontColor(idx <= this.current ? {color-text-primary} : {color-text-primary})
        }.alignItems(HorizontalAlign.Center)
        if (idx < this.steps.length - 1) {
          Column().width(40).height(2)
            .backgroundColor(idx < this.current ? {color-button-primary-bg} : {color-bg-secondary})
        }
      })
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`timeline`](../timeline/component.md) — timeline 与 steps 结构相似
- [`icon`](../icon/component.md) — 步骤节点图标

## 参考链接

- Stepper/StepperItem 官方文档(含 API 22 弃用说明与 Swiper 替代建议):https://gitee.com/openharmony/docs/blob/master/en/application-dev/reference/apis-arkui/arkui-ts/ts-basic-components-stepper.md
- Swiper 组件(方案 2 载体):https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-container-swiper
- 创建列表(List):https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list
