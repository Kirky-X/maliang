# 选择器交互模式命名词汇

> 模式词汇库。超越"下拉列表"的选择器交互模式命名:圆周手势、速度物理、径向菜单、跟手放大。键盘下拉部分与 [`forms.md`](forms.md) 互补。

## 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `picker-knob-dial` | 旋钮转盘:绕圆心转动,刻度逐格吸附,中心数字跟随滚动;拟态变体:指示点/进度圆弧/数值三元素同频联动,外围细刻度辅助读数(收编挂接见 [`pro-motion.md`](pro-motion.md) `picker-rotary-knob`) | 计时器、金额转盘、调参面板 |
| `picker-wheel-decay` | 滚轮速度衰减吸附:松手后速度逐帧衰减,快停时吸附最近格;联动列随选中值级联刷新(选二月,天数列变 28) | iOS 式时间/日期滚轮、高度/体重选择、级联选择(月→天数、省→市) |
| `picker-radial-arc` | 弧形径向菜单:按住主按钮沿圆弧依次弹出选项,滑到哪个哪个放大,松手执行 | 快捷操作(工具、画笔、发送方式);单手高频场景 |
| `picker-magnify-strip` | 跟手放大图标排:一排图标随手指距离呈波浪缩放,松手选中当前项;工具条变体:经过的图标依次放大,当前工具名实时跟着切换,松手才作用于画布 | 表情/图标选择、相册帧选择、画布工具条 |
| `picker-before-after` | 前后对比滑块:分割线跟手,左右两态(改前/改后)同位叠加 | 修图对比、方案对比、价格切换 |
| `picker-group-sticky` | 分组下拉 sticky 组标题:组标题不可选,滚动时钉在列表顶部 | 长选项列表按类分组(国家、分类) |
| `picker-searchable-dropdown` | 可搜索下拉:输入过滤 + 键盘上下移动 + 回车确认,全程不碰鼠标 | 选项 > 15 的后台表单(与 [`tables.md`](tables.md) 筛选联动) |
| `picker-single-collapse` | 单选下拉:固定少量选项,选完自动收起 | ≤ 5 个固定选项 |
| `picker-stepper-roll` | 数量步进滚动:点 +/- 数字逐格上翻/下翻(非瞬换),按住连加且间隔递减加速,按钮按压缩放回弹 | 数量/件数选择(数字只动变化位见 [`number-motion.md`](number-motion.md) `num-ticker-partial`;加入按钮展开成步进器的形变见 [`pro-motion.md`](pro-motion.md) `btn-stepper-morph`) |
| `picker-segment-linked-sync` | 分段切换数据联动:选中态、下方图表、数值高亮同帧一起变(切换即换一整套数据视图) | 概览页周期/维度切换(联动前提见 [`charts.md`](charts.md) `chart-hover-link`:数据源须同源;指示条形变本身走 [`navigation.md`](navigation.md) `nav-tab-liquid`) |
| `input-auto-format` | 智能格式化输入框:日期自动补 `/`、时间补 `:`,框内常驻单位与字数 | 手机号/银行卡/日期金额录入(归 forms 亦通) |
| `picker-type-dial` | 字号刻度拨盘:一排横向刻度数字,当前值居中高亮、两侧渐隐;拨动时目标属性实时联动,停下列吸附最近刻度;固定指针变体:指针不动、刻度尺从其下滑过,数值/预览/外圈多处读数实时同步 | 键盘附件条/格式工具条(字号、笔刷粗细等连续档位)、亮度/音量刻度条 |
| `picker-swatch-strip` | 滑动选色条:横向色块排,经过的色块依次放大弹起,松手选中,界面主题色随之平滑过渡 | 主题色/标签色选择(`picker-magnify-strip` 的选色变体,增量为主题色全局联动) |
| `picker-bubble-cluster` | 圆泡云选:大小不一的圆泡堆叠半屏,选中项放大突出、周围泡让位后重新聚拢,选中态靠尺寸与位置表达,不靠勾选框 | 标签/兴趣/心情挑选等无框化单选 |
| `picker-image-color-extract` | 图中取色:从图片提取五枚代表色成色块排,点选即同步更新预览与 HEX/RGB 值(可复制) | 从照片/品牌图取主色、主题色冷启动(与 [`forms.md`](forms.md) 取色三型口径互见:彼条光谱/网格/HSB 主动选色,本条从既有图取样) |
| `picker-slot-range-drag` | 拖动连选时段:按住拖过相邻格子连选合并成一条,两端把手可单独调整起止,时间实时回显 | 排期/预约的时间段选择 |
| `picker-range-slider` | 双头区间滑块:按住的圆点放大承接焦点,数值随拖滚动,松手吸附最近整数;双柄最小间距用橡皮筋阻尼,禁重叠 | 价格区间、筛选区间(与 `picker-slot-range-drag` 互见:彼条离散格子连选合并,本条连续轨道吸附) |
| `picker-calendar-range-sweep` | 日历区间拖选:按住起始日拖过日期格,像荧光笔逐格涂亮(禁整段瞬亮),晚数计数同步滚动 | 酒店/租期预订(浏览型日历;录入域分界见 [`forms.md`](forms.md) `field-date`) |
| `picker-date-strip` | 横向周日期条:选中底色滑到所点日期,左右滑整周翻页,月份标题同步更新 | 日程/打卡类首页的日期切换 |

## 使用规则

- 吸附类(`picker-wheel-decay` / `picker-knob-dial` / `picker-type-dial`)松手判定 = 距离 + 速度双阈值,速度参与格数(见 [`../motion-skeletons/gesture-arbitration.md`](../motion-skeletons/gesture-arbitration.md) 速度语义)
- 吸附落格必须有 ≤ 120ms 的对齐动画 + 触觉反馈(vibration ≤ 10ms,见 [`micro-interactions.md`](../micro-interactions.md))
- `picker-radial-arc` 展开项 3-6 个,扇区角度 ≥ 45°(触控热区 ≥ 44px);移动端禁用悬停态
- `picker-magnify-strip` 缩放峰值 ≤ 1.5 倍,相邻联动衰减按高斯分布,松手才确认(滑动过程不触发选择)
- `picker-before-after` 分割线必须带把手(≥ 44px 触控),键盘可左右箭头步进 5%
- 选择器键盘可达性:`picker-searchable-dropdown` 必须支持 ↑↓ 移动 + Enter 确认 + Esc 关闭(见 [`accessibility.md`](../meta/accessibility.md))
- `input-auto-format` 只做展示层分隔,提交值保持纯数据;禁止格式化吞掉用户正在编辑的光标位置
- 选项 ≤ 5 用 `picker-single-collapse` 或分段控件,> 15 必须可搜索;两档之间用 `picker-group-sticky`

## 在 draw-md 中的写法

```markdown
## Picker (duration-select)
- pattern: picker-wheel-decay
- items: 1-60min, snap: velocity+distance, haptic: 10ms
- a11y: keyboard-up-down, aria-live=selected-value

## Input (birthday)
- pattern: input-auto-format
- mask: YYYY/MM/DD, unit: none, counter: none
```
