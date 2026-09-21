# 选择器交互模式命名词汇

> 模式词汇库。超越"下拉列表"的选择器交互模式命名:圆周手势、速度物理、径向菜单、跟手放大。来源:UI 交互教学视频转录提取(2026-09,叨叨AI/西瓜同学);键盘下拉部分与 [`forms.md`](forms.md) 互补。

## 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `picker-knob-dial` | 旋钮转盘:绕圆心转动,刻度逐格吸附,中心数字跟随滚动 | 计时器、金额转盘、调参面板 |
| `picker-wheel-decay` | 滚轮速度衰减吸附:松手后速度逐帧衰减,快停时吸附最近格 | iOS 式时间/日期滚轮、高度/体重选择 |
| `picker-radial-arc` | 弧形径向菜单:按住主按钮沿圆弧依次弹出选项,滑到哪个哪个放大,松手执行 | 快捷操作(工具、画笔、发送方式);单手高频场景 |
| `picker-magnify-strip` | 跟手放大图标排:一排图标随手指距离呈波浪缩放,松手选中当前项 | 表情/图标选择、相册帧选择 |
| `picker-before-after` | 前后对比滑块:分割线跟手,左右两态(改前/改后)同位叠加 | 修图对比、方案对比、价格切换 |
| `picker-group-sticky` | 分组下拉 sticky 组标题:组标题不可选,滚动时钉在列表顶部 | 长选项列表按类分组(国家、分类) |
| `picker-searchable-dropdown` | 可搜索下拉:输入过滤 + 键盘上下移动 + 回车确认,全程不碰鼠标 | 选项 > 15 的后台表单(与 [`tables.md`](tables.md) 筛选联动) |
| `picker-single-collapse` | 单选下拉:固定少量选项,选完自动收起 | ≤ 5 个固定选项 |
| `input-auto-format` | 智能格式化输入框:日期自动补 `/`、时间补 `:`,框内常驻单位与字数 | 手机号/银行卡/日期金额录入(归 forms 亦通) |

## 使用规则

- 吸附类(`picker-wheel-decay` / `picker-knob-dial`)松手判定 = 距离 + 速度双阈值,速度参与格数(见 [`../motion-skeletons/gesture-arbitration.md`](../motion-skeletons/gesture-arbitration.md) 速度语义)
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
