# Progress 组件 API 文档

> ArkTS 进度条组件,包含 `Progress`(线性/环形/刻度进度)与 `LoadingProgress`(加载转圈)。

## 组件定义

| 组件 | 用途 |
| --- | --- |
| `Progress` | 已知进度的进度条(0-100%) |
| `LoadingProgress` | 不定进度加载动画(转圈) |

## Progress 构造函数

```arkts
Progress(options: {
  value: number          // 当前值
  total?: number         // 总值,默认 100
  type?: ProgressType    // 类型:Linear/Ring/ScaleRing/Eclipse
})
```

## 核心属性表

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| value | number | 当前值 |
| total | number | 总值 |
| type | ProgressType | Linear(线性)/Ring(环形)/ScaleRing(刻度)/Eclipse(月牙) |
| color | ResourceColor | 进度色,用 `{color-button-primary-bg}` |
| backgroundColor | ResourceColor | 轨道色,用 `{color-bg-secondary}` |
| strokeWidth | Length | 线宽(Ring 类型) |
| scaleCount / scaleWidth | number | 刻度数与宽度(ScaleRing) |

## ProgressType 枚举

| 值 | 描述 | 场景 |
| --- | --- | --- |
| `Linear` | 线性条 | 文件下载/上传 |
| `Ring` | 环形 | 进度百分比展示 |
| `ScaleRing` | 刻度环 | 仪表盘风格 |
| `Eclipse` | 月牙 | 圆形进度 |

## 最小示例

```arkts
@Entry
@Component
struct ProgressDemo {
  @State value: number = 30
  build() {
    Column() {
      Progress({ value: this.value, total: 100, type: ProgressType.Linear })
        .width('100%')
        .color({color-button-primary-bg})
        .backgroundColor({color-bg-secondary})
    }
    .padding({spacing-md})
  }
}
```

## 关联组件

- [`loading`](../loading/component.md) — 加载动画(LoadingProgress)
- [`dialog`](../dialog/component.md) — 弹窗内常嵌入 Progress

## 参考链接

- ArkTS 官方文档 - 进度条 (Progress): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-progress-indicator
