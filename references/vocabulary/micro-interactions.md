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

## 高端技法(进阶微交互)

> 以下技法为 Apple iOS 26 / macOS 26 Liquid Glass 设计语言的高端交互模式,适用于 MOTION_INTENSITY ≥ 6(见 [`dials.md`](../meta/dials.md))的场景。低档位禁用,避免过度装饰。来源:taste-skill + liquid-glass 生态。

### Double-Bezel(双层边框玻璃)

- **视觉**:玻璃元素双层边框,外层 1px 高光 + 内层 1px 暗影,模拟玻璃边缘的折射带
- **实现**:`box-shadow: inset 0 0 0 1px rgba(255,255,255,0.2), inset 0 0 0 2px rgba(0,0,0,0.1)`
- **适用**:导航栏、Dock、浮层卡片(配 [`glass-effect.md`](../dimensions/glass-effect.md) 或 [`glass-advanced.md`](../dimensions/glass-advanced.md))
- **禁止**:非玻璃元素使用(失去语义)

### Button-in-Button(嵌套按钮)

- **视觉**:主按钮内嵌一个次按钮(如主按钮"保存"内嵌次按钮"另存为"),hover 时次按钮展开
- **实现**:主按钮 `position: relative`,次按钮 `position: absolute` + `transform: scaleX(0)` → hover `scaleX(1)`
- **适用**:空间受限的工具栏、批量操作按钮
- **禁止**:移动端(触摸目标冲突)、表单提交(语义混乱)

### Fluid Island(流动岛屿布局)

- **视觉**:多个玻璃岛屿浮动于背景之上,滚动时岛屿间有视差 + 形变(轻微 scale + translate)
- **实现**:每个 island 用 `position: sticky` + `transform` 滚动插值,配 GSAP ScrollTrigger
- **适用**:品牌叙事页、产品发布页(MOTION_INTENSITY ≥ 8)
- **禁止**:信息密集页(岛屿形变干扰阅读)、无障碍优先场景

### Magnetic Button(磁吸按钮)

- **视觉**:鼠标接近按钮时,按钮轻微向鼠标方向位移(磁吸感),离开回弹
- **实现**:`mousemove` 监听父容器,计算鼠标到按钮中心的距离,`transform: translate(dx, dy)`(位移 ≤ 8px)
- **适用**:Hero CTA、核心转化按钮、创意站
- **禁止**:表单提交按钮(干扰点击精度)、移动端(无鼠标)
- **降级**:`prefers-reduced-motion: reduce` 时关闭磁吸,回 `micro-hover-lift`

### Scroll Interpolation(滚动插值)

- **视觉**:滚动时元素属性(translate / opacity / scale)按滚动进度插值,非线性映射
- **实现**:GSAP ScrollTrigger + `scrub: true` + 自定义 ease,或原生 `IntersectionObserver` + `requestAnimationFrame`
- **适用**:滚动叙事、Hero → Content 过渡、数字计数动画
- **禁止**:文档站、后台(干扰浏览)、MOTION_INTENSITY ≤ 5

### cubic-bezier 缓动曲线库

> 替代默认 `linear` / `ease`,统一缓动语言。所有动画 MUST 从下表选,禁止自造曲线(除非 DESIGN.md 显式声明)。

| 曲线名           | cubic-bezier          | 语义                  | 适用场景                  |
| ---------------- | --------------------- | --------------------- | ------------------------- |
| `ease-out-soft`  | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` | 柔和减速(出场)       | 入场动画、reveal          |
| `ease-in-soft`   | `cubic-bezier(0.55, 0.085, 0.68, 0.53)` | 柔和加速(退场)       | 退场动画、dismiss         |
| `ease-in-out`    | `cubic-bezier(0.645, 0.045, 0.355, 1)` | 对称缓动(状态切换)   | 状态过渡、tab 切换        |
| `ease-spring`    | `cubic-bezier(0.34, 1.56, 0.64, 1)` | 弹性(过冲回弹)       | 按下回弹、卡片落下(MOTION ≥ 7) |
| `ease-snappy`    | `cubic-bezier(0.16, 1, 0.3, 1)` | 干脆(快速减速)       | 按钮反馈、toggle          |
| `ease-glass`     | `cubic-bezier(0.32, 0.72, 0, 1)` | 液态玻璃感(平滑长尾) | Liquid Glass 元素过渡     |

**使用规则**:
- 状态过渡 duration ≤ 150ms → 用 `ease-snappy`
- 入场动画 duration 150-600ms → 用 `ease-out-soft`
- 退场动画 → 用 `ease-in-soft`
- MOTION_INTENSITY ≥ 7 且需弹性 → 用 `ease-spring`(过冲 ≤ 1.2,防眩晕)
- Liquid Glass 元素(见 [`glass-advanced.md`](../dimensions/glass-advanced.md))→ 用 `ease-glass`
- **禁止**全场用 `ease-spring`(弹性疲劳)、**禁止**用 `linear`(机械感,无生命)
