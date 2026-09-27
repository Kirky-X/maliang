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
| `micro-icon-morph`    | 图标在两个命名状态间形变(菜单↔关闭、播放↔暂停)   | 图标级状态切换(见 [`icon.md`](../dimensions/icon.md) 动效图标节) |
| `micro-hold-confirm`  | hold-to-confirm:长按 2s 环形填充,松手 200ms 回弹 | 破坏性操作防误触(删除/清空/支付)      |

## 频率法则:该不该动

> 动画成本按操作频率判断,不是"越动越好"。来源:interface-design;中间档、键盘否决与 utility 法则:find-animation-opportunities + apple-design + prototype + web-design-pascalorg 四源印证,2026-09 吸收。

| 使用频率                                     | 动画策略                     |
| -------------------------------------------- | ---------------------------- |
| 每天 100+ 次的操作(快捷键、命令面板等)     | 禁止动画,延迟即成本         |
| 每天几十次的操作(hover 状态、列表导航、频繁 toggle) | 否决,或仅近乎无感的反馈(快而轻) |
| 偶发表面(modal / drawer / toast / popover) | 标准入场 / 退场动画          |
| 首次运行(onboarding / 空状态)              | 才可加惊喜动效               |

**键盘一票否决**:键盘发起的操作(命令面板、快捷键、焦点跳转)是一票否决项,不是判断题——这类操作每天重复上百次,动画让它们显得慢、迟滞、与手脱节。参照 Raycast:无任何开合动画,就是最优体验。

**utility 法则(多模态反馈的节制)**:动效 / 声音 / 触觉只在有意义时刻给(成功、错误、提交、吸附落定);过度反馈会训练用户忽略一切反馈。三条判据:因果性(反馈必须明显由真实触发事件引起,且性格匹配动作的物理感)、同帧性(视觉 / 声音 / 触觉同帧触发,相互延迟即穿帮)、效用性(只在值得处给——本条即频率表与上方两段的统一口径,不另设第二套节制标准)。

## 时长预算表

> 按组件类型的 duration 上限;全局上限 UI 一律 < 300ms(仅 modal / drawer 类大表面可放宽到 400ms)。来源:interface-design。

| 组件类型          | 时长预算   |
| ----------------- | ---------- |
| 按压反馈          | 100-160ms  |
| tooltip / popover | 125-200ms  |
| dropdown / menu   | 150-250ms  |
| modal / drawer    | 200-400ms  |

> **全库统一分层口径**(其他文档涉及动效时长时以此为准,冲突数值保留但须注"见 micro-interactions 分层口径"):
> 1. **反馈类**(按压 / tooltip / toast 等元素级反馈)duration **< 300ms**;
> 2. **浮层转场**(modal / drawer / popover 入退场)**≤ 400ms**——`validate-draw-md.py` 检查 11 硬门(ERROR);如确需更长转场,须同步调整脚本阈值并说明理由,或改用 `{duration-*}` token 引用(不含字面量 ms,脚本自然跳过)。**弹簧路线豁免**:弹簧无固定时长,声明为弹簧驱动(`motion-model: spring`)且显式给出弹簧参数(damping / response 等)的行不受 400ms 硬门约束,脚本仅留 WARN 痕;只写 spring 不写参数仍按违规报 ERROR(豁免是显式条件,不是阈值放宽,见 [`interruptible-motion.md`](../motion-skeletons/interruptible-motion.md) 弹簧两参数模型);
> 3. **装饰 / 骨架类长动效**(滚动揭示、skeleton shimmer 等非入场循环 / 长动效)**≤ 600ms** 且**必须可跳过**(prefers-reduced-motion 降级或用户可跳过)。**入场 / 转场类不适用本档**,一律按第 2 层 ≤400ms 执行(2026-09 整合收敛:原「缓动库入场 150-600ms」与 validate-draw-md 检查 11、preview-check 5.9.3 两道 400ms 硬门冲突,按预览侧既有收敛决策统一)。本档 >400ms 的动效在 draw-md 规格中必须以 `{duration-*}` token 引用表达(不含字面量 ms,检查 11 自然跳过),禁直写字面量 ms;preview 实现侧受 preview-check 5.9.3 无条件 400ms 门约束,>400ms 装饰档要在实现层落地,须预览验证组先在其脚本开显式豁免口径(参照检查 11 弹簧豁免的显式条件模式),未开前实现一律 ≤400ms;
> 4. **stagger 间隔单档 ≤ 80ms**;装饰档放宽到 ≤ 120ms 须 MOTION_INTENSITY ≥ 8(见 [`dials.md`](../meta/dials.md))。
>
> 上表数值是第 1/2 层的按组件细分;骨架 / 滚动揭示等装饰类长动效不受本表上限约束,按第 3 层执行(缓动库入场 ≤400ms、dials L4-7 ≤400ms、motion-skeletons ≤600ms 装饰循环与之相容)。

## 使用规则

- 所有交互元素必须实现 `micro-press-scale` + `micro-focus-ring`(强制,见 [`principles.md`](../meta/principles.md) 第 14 定律)
- `micro-haptic` 仅移动端,且 vibration ≤ 50ms
- `micro-cursor-custom` 慎用,会破坏无障碍(见 [`accessibility.md`](../meta/accessibility.md))
- Loading 反馈:≤ 200ms 不显示,200ms-1s 用 spinner,> 1s 用 skeleton(见 [`principles.md`](../meta/principles.md) 第 14 定律)
- 入场**禁止** `ease-in` 类加速曲线(首帧可见延迟,像卡顿);入场一律用 ease-out `cubic-bezier(0.23, 1, 0.32, 1)`
- **禁止**元素从 `scale(0)` 出现(突变突兀);从 `scale(0.95) + opacity: 0` 起步,popover / dropdown 从触发器原点缩放
- 退场必须比入场**更快更轻**(时长约为入场的 60-80%,幅度更小)
- **动效降级三档**(2026-09 维护者裁决采用三档分级,取代旧「所有微交互一律降级」口径;思想来源 morphicons `reducedMotion` 策略,2026-09 吸收):
  - **`user`(默认档)**——小幅沟通性微转场(第 1 层 <300ms 元素级反馈、icon morph):跟随系统 `prefers-reduced-motion` 设置,开启时直达**静止终态**即可,静止终态必须完整传达状态;无需专门设计降级编排;
  - **`always`(强制降级档)**——功能性与大幅动效(第 2 层浮层转场、入场编排,第 3 层滚动揭示 / skeleton):**必须**自带降级形态(位移改淡入、编排改瞬时切换、循环改静止),不做降级视为未完成;
  - **`never`(例外档)**——动效即交互本体、降级即功能损坏的场合(拖拽跟手、弹簧物理反馈):允许不降级,须在使用处说明理由。
- `micro-hold-confirm` 的「2s」是**长按判定窗口**(随按压持续的进度填充),非一次性转场时长,不受 400ms 硬门约束;draw-md 产物中勿写成 `duration: 2000ms`(会触发检查 11),应写 `long-press=hold 2s` 类交互语义
- Web 端入场过渡可渐进增强 `@starting-style`(元素首次渲染 / 从 `display:none` 出现时的过渡起点)

> **@starting-style 注记(仅 Web)**:兼容性 Chrome 117+ / Edge 117+ / Safari 17.5+ / Firefox 129+(2024 Baseline Newly Available,来源 caniuse/MDN);且 `@supports at-rule (@starting-style)` 特性检测尚不可用(CSSWG #10648)。**不可作唯一入场路径**——不支持浏览器中元素会直接以终态出现,这本身可接受;但若初态依赖它隐藏元素(如从 `opacity:0` 过渡),必须保证无支持时不残缺:默认态写终态,起点只放进 `@starting-style` 块;JS fallback 为元素插入后强制 reflow 再移除初始 class,或直接接受无动画直显。HarmonyOS / Flutter 无对应概念,n/a。

## 声音反馈

> 小篇幅决策节,不升级为独立维度。来源:web-design-pascalorg(候选 6),2026-09 吸收。

| 场景                       | 用声? | 说明                         |
| -------------------------- | ----- | ---------------------------- |
| 支付成功 / 提交完成        | 用    | 有意义的结果时刻             |
| 错误 / 告警                | 用    | 需要穿透视觉注意力时         |
| 吸附落定 / 拖拽完成        | 可用  | 与触觉成对,同帧触发         |
| 打字 / hover / 普通导航    | 禁    | 高频操作加声是噪声(见频率法则 utility 法则) |

**三硬规则**:
1. 每个声音必须有**视觉等价物**——声音是增强通道,禁作唯一反馈(无障碍底线);
2. 必须有**关闭开关**——应用内静音开关,且默认跟随系统静音状态;
3. **尊重系统偏好**——系统静音 / 勿扰模式下不发声,不打破用户全局预期。

**三框架落点(各一行)**:Web → Web Audio API 预解码短音效(禁 `<audio>` 元素即时播放,加载延迟毁掉因果性);HarmonyOS → soundPool 短音效(`@ohos.multimedia`,API 细节以官方现行文档为准);Flutter → audioplayers / soundpool 类插件预加载播放。

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
| `ease-out-expo`  | `cubic-bezier(0.23, 1, 0.32, 1)` | 入场标准 ease-out(快起步,长尾减速) | 微交互入场一律用此(三禁令指定;来源:interface-design) |

**使用规则**:
- 状态过渡 duration ≤ 150ms → 用 `ease-snappy`
- 入场动画 duration 150-400ms(入场属转场节奏,受两道脚本 400ms 硬门;2026-09 收敛,原 150-600ms 作废,不入第 3 层装饰档)→ 用 `ease-out-soft`
- 退场动画 → 用 `ease-in-soft`
- MOTION_INTENSITY ≥ 7 且需弹性 → 用 `ease-spring`(过冲 ≤ 1.2,防眩晕)
- Liquid Glass 元素(见 [`glass-advanced.md`](../dimensions/glass-advanced.md))→ 用 `ease-glass`
- **禁止**全场用 `ease-spring`(弹性疲劳)、**禁止**用 `linear`(机械感,无生命)
