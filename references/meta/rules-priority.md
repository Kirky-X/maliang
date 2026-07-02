# 规则优先级系统 —— 10 类规则覆盖关系

> 规范层。当多条设计规则在同一处冲突时,按本表优先级裁决:高优先级覆盖低优先级,同级冲突需人工决策并显式记录。来源:ui-ux-pro-max-skill。

## 优先级表

| 优先级    | 规则类别       | 关键内容(摘要)                                                |
| --------- | -------------- | --------------------------------------------------------------- |
| CRITICAL  | Accessibility  | WCAG AA/AAA 对比度、键盘可达、屏幕阅读器、`prefers-*` 偏好       |
| CRITICAL  | Touch          | 44pt 热区、防误触、手势不与系统冲突                              |
| HIGH      | Performance    | LCP<2.5s / INP<200ms / CLS<0.1,只动 transform/opacity           |
| HIGH      | Style          | 60-30-10、AI Tells 黑名单、单一强调色                            |
| HIGH      | Layout         | 网格一致性、间距档位、容器宽度差异化                              |
| HIGH      | Navigation     | 信息架构、面包屑、返回路径、深链可达                              |
| MEDIUM    | Typography     | 字体层级、行高、字距、display/UI 字体分工                        |
| MEDIUM    | Animation      | 动画动机(见 [`principles.md`](./principles.md) 第 13 定律)、缓动 |
| MEDIUM    | Forms          | 标签位置、错误反馈、必填标记、自动填充                            |
| LOW       | Charts         | 调色板、轴标签、tooltip、图例                                    |

## 冲突裁决规则

1. **CRITICAL > HIGH > MEDIUM > LOW**:高优先级无条件覆盖低优先级。例如美观的浅灰文字违反 WCAG AA,必须改深,即使破坏 Style 意图。
2. **同级冲突**:不自动裁决,在产物中显式标注冲突并提请人工决策。例:Performance 与 Style 同为 HIGH,若一个装饰动画拖慢 LCP 但贡献品牌识别,需用户拍板。
3. **跨优先级妥协**:低优先级规则被覆盖时,在代码注释中标注 `// overridden by <rule>(<priority>)`,保留意图可追溯。
4. **CRITICAL 不可妥协**:Accessibility 与 Touch 永远胜出,即使用户要求"美观优先"也不可让步——只能用替代美学方案满足。

## 典型冲突场景

### 场景 A · Style vs Accessibility

- 冲突:设计师要 `text-gray-400 on bg-white`(对比度 2.3:1),Style 上轻量好看
- 裁决:Accessibility(CRITICAL) 胜,必须降到 `text-gray-600`(4.6:1)或更深
- 替代:用字号变小 + 字重加粗 + 深一档灰,既保留层级又满足对比

### 场景 B · Animation vs Performance

- 冲突:视差滚动动效(MOTION_INTENSITY Level 8)拖慢 LCP 到 3.2s
- 裁决:Performance(HIGH) 胜于 Animation(MEDIUM),视差降级或仅非首屏使用
- 替代:首屏静态,滚动到 viewport 后再触发视差

### 场景 C · Layout vs Navigation

- 冲突:设计师要把导航项收到 hamburger(Layout 想要简洁),Navigation 要求主要功能 1 tap 可达
- 裁决:同为 HIGH,需人工决策。建议:核心 3 项常驻 tab,次要项入 hamburger

### 场景 D · Typography vs Style

- 冲突:Style 要求品牌 display 字体(衬线),Typography 建议统一 UI 字体
- 裁决:Typography(MEDIUM) 服从 Style(HIGH),display 用于标题即可
- 注:这是常见覆盖方向,不算冲突,但需在 token 中显式记录两套字体族

### 场景 E · Charts vs Style

- 冲突:Style 要求单色极简,Charts 要求多色区分类目
- 裁决:Charts(LOW) 服从 Style(HIGH),用形状 / 图案 + 单色相区分,而非引入第二色相

## 自检触发点

- **design-md 阶段**:写 Do's and Don'ts 时,每条标注所属规则类别与优先级
- **draw-md 阶段**:输出 UI markdown 时,组件参数表加 `priority` 字段记录覆盖关系
- **preview 阶段**:Pre-Flight Check 中扫描"违反 CRITICAL 的产出",硬性失败
- **draw-* 阶段**:框架代码注释中保留 `// priority: <rule>(<level>)` 标注,便于后续维护

## 与其他文档的关系

- 各类别规则的**具体内容**分散在专门文档:Accessibility → [`accessibility.md`](./accessibility.md)、Performance → [`performance.md`](./performance.md)、Style → [`ai-tells.md`](./ai-tells.md) + [`color.md`](../dimensions/color.md)、Typography → [`font.md`](../dimensions/font.md)、Animation → [`principles.md`](./principles.md) 第 13 定律
- 本文只管**优先级裁决**,不重复规则内容
- 优先级表是 closed set,不随意新增类别;新增需同步更新本表与相关 reference 文档
