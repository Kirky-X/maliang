# 微交互模式命名词汇

> 模式词汇库。元素级反馈的微交互模式,补充 [`principles.md`](../meta/principles.md) 第 14 定律的"Tactile Feedback"。来源:taste-skill。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `micro-hover-lift`    | hover 时元素上浮 2-4px + 阴影加深                | 卡片、链接、按钮                      |
| `micro-press-scale`   | 按下时 scale 0.97 + 短促过渡                     | 按钮、可点击卡片                      |
| `micro-focus-ring`    | 键盘聚焦时显示 ring(outline 替代)               | 所有交互元素(强制)                  |
| `micro-ripple`        | 点击位置涟漪扩散                                  | Material 风、移动按钮                 |
| `micro-tooltip`       | hover 延迟 500ms 显示 tooltip                     | 图标按钮、密度高的工具栏              |
| `micro-skeleton`      | Loading 时显示骨架占位                            | 数据加载、列表、详情                  |
| `micro-shimmer`       | 骨架上的微光扫过                                  | 骨架占位的进阶版                      |
| `micro-toast`         | 操作反馈 toast(成功 / 失败)                     | 表单提交、删除、加入购物车            |
| `micro-haptic`        | 触觉反馈(振动)                                  | 移动端按钮、长按、滑动                |
| `micro-cursor-custom` | 自定义光标                                        | 创意站、品牌站(慎用)                |
| `micro-drag-handle`   | 拖拽手柄 hover 显示                                | 可拖拽列表、可调大小面板              |
| `micro-loading-spinner` | 转 spinner                                       | 短时加载(< 1s)                      |
| `micro-loading-bar`   | 顶部进度条                                        | 长时加载 / 页面切换                   |

## 使用规则

- 所有交互元素必须实现 `micro-press-scale` + `micro-focus-ring`(强制,见 [`principles.md`](../meta/principles.md) 第 14 定律)
- `micro-haptic` 仅移动端,且 vibration ≤ 50ms
- `micro-cursor-custom` 慎用,会破坏无障碍(见 [`accessibility.md`](../meta/accessibility.md))
- Loading 反馈:≤ 200ms 不显示,200ms-1s 用 spinner,> 1s 用 skeleton(见 [`principles.md`](../meta/principles.md) 第 14 定律)
- 所有微交互必须实现 `prefers-reduced-motion` 降级

## 在 draw-md 中的写法

```markdown
## Button (primary)
- pattern: button-primary
- micro_interactions:
  - hover: micro-hover-lift (translateY -2px, shadow lg)
  - pressed: micro-press-scale (scale 0.97, duration 100ms)
  - focused: micro-focus-ring (outline 2px, color brand)
  - loading: micro-loading-spinner (size 16px, color inherit)
  - success: micro-toast (text "已添加", duration 2000ms)
```
