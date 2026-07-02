# 无障碍 —— WCAG 对比度 + prefers-* 用户偏好

> 规范层。Accessibility 是 CRITICAL 优先级(见 [`rules-priority.md`](./rules-priority.md)),高于所有其他规则,**不可妥协**。本文列出对比度阈值与三种用户偏好的强制支持。来源:ui-ux-pro-max-skill + taste-skill。

## 1. WCAG 对比度阈值(强制)

| 文本类型           | AA(最低) | AAA(增强) | 说明                                  |
| ------------------ | --------- | ---------- | ------------------------------------- |
| 正文(< 18pt / 14pt bold) | 4.5:1     | 7:1        | 任何页面默认值,违反 = CRITICAL 失败  |
| 大文本(≥ 18pt / 14pt bold) | 3:1       | 4.5:1      | 标题与大字                            |
| 非文本对比(UI 组件) | 3:1       | —          | 按钮、表单边框、图标与相邻背景        |
| 非文本对比(图形)   | 3:1       | —          | 图表线条、图标 active 态              |

### 强制规则

- DESIGN.md 中每个 `colors.*` 与背景配对必须通过 AA(4.5:1 正文 / 3:1 大字),design-md lint 阶段自动检查(见 [`design-md.md`](../commands/design-md.md) Phase 3 Lint)
- preview 阶段 Pre-Flight Check 必须扫描所有文字色与背景色对,违反 = 硬性失败
- AAA(7:1)为目标但非强制,用于医疗/政府/无障碍优先产品时升为强制
- 禁止用纯红/纯绿表达信息(色盲不友好),必须加形状/文字辅助
- `placeholder` 文字也必须满足 4.5:1,不可用 `text-gray-300` 凑数

### 对比度计算

相对亮度公式:`L = 0.2126 * R + 0.7152 * G + 0.0722 * B`(其中 R/G/B 经 gamma 校正)。对比度 = `(L_lighter + 0.05) / (L_darker + 0.05)`。

工具:`npx @google/design.md lint` 自动计算;或 WebAIM Contrast Checker。

## 2. prefers-reduced-motion(降低动效偏好)

**强制支持**。用户在系统设置中开启"减少动态效果"时,UI 必须降级。

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**强制规则**:

- 所有装饰性动画(入场、视差、stagger)在 reduced-motion 下退化为瞬时显示
- 功能性动画(loading 进度、状态切换反馈)允许保留,但 duration ≤ 150ms
- MOTION_INTENSITY(见 [`dials.md`](./dials.md))在 reduced-motion 下强制 ≤ 3
- 视差滚动 / pin sticky / 横向平移必须**完全禁用**(非降级,是关闭)
- preview 阶段必须双跑:默认 + reduced-motion,对比截图无信息丢失

## 3. prefers-color-scheme(颜色方案偏好)

**强制支持**。用户系统设置 dark / light 时,DESIGN.md 的语义 token 必须自动切换。

```css
:root {
  --color-bg-primary: #ffffff;
  --color-text-primary: #1a1c1e;
}
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: #1a1c1e;
    --color-text-primary: #f7f5f2;
  }
}
```

**强制规则**:

- 暗色模式不是简单反色(见 [`color.md`](../dimensions/color.md) 第 5 节),必须独立设计
- 暗色模式下对比度仍必须满足 AA(暗色背景上的浅灰文字易不达标)
- 用户主动选择的主题(切换器)优先级 > `prefers-color-scheme`,但需在 localStorage 持久化
- 强调色在暗色下饱和度应下调,避免暗底过刺

## 4. prefers-reduced-transparency(降低透明度偏好)

**强制支持**(2024+ 浏览器)。用户开启"减少透明度"时,`backdrop-filter` / `opacity` / `rgba` 半透明背景必须降级为不透明。

```css
.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
}
@media (prefers-reduced-transparency: reduce) {
  .glass-card {
    background: var(--color-bg-primary); /* 不透明替代 */
    backdrop-filter: none;
  }
}
```

**强制规则**:

- 所有 `backdrop-filter` 使用必须配 reduced-transparency 降级(见 [`glass-effect.md`](../dimensions/glass-effect.md))
- 半透明叠加层(modal mask)降级为不透明 + 较低 `--color-overlay` 明度
- preview 必须双跑:默认 + reduced-transparency,确认降级后可读性不丢失

## 5. 其他无障碍强制项

| 项目                | 规则                                                                     |
| ------------------- | ------------------------------------------------------------------------ |
| 键盘可达            | 所有交互元素 Tab 可达,focus ring 可见(不可 `outline: none` 不补替代)  |
| 屏幕阅读器          | 图片必 `alt`(装饰性 `alt=""`),按钮必 `aria-label`(无文字时)          |
| 表单标签            | `<label>` 关联或 `aria-label`,占位符不替代标签                          |
| 跳转链接            | 页面首项 "Skip to main content",Tab 可聚焦                              |
| 移动端热区          | 触摸目标 ≥ 44pt × 44pt(Touch CRITICAL,见 [`rules-priority.md`](./rules-priority.md)) |
| 焦点顺序            | DOM 顺序 = 视觉顺序,不靠 `tabindex` 正整数手动调                       |
| 动态内容            | `aria-live="polite"`(通知)/ `aria-live="assertive"`(错误)            |

## 6. Preview 阶段无障碍检查

Pre-Flight Check 中以下为硬性失败项(见 [`preview.md`](../commands/preview.md)):

- [ ] 任一文字对比度 < 4.5:1(正文)/ 3:1(大字)
- [ ] 装饰性动画无 `prefers-reduced-motion` 降级
- [ ] 暗色模式 token 缺失或对比度不达标
- [ ] `backdrop-filter` 无 `prefers-reduced-transparency` 降级
- [ ] 交互元素无 focus ring(`outline: none` 无替代)
- [ ] 触摸目标 < 44pt
- [ ] 图片缺 `alt`

## 与其他文档的关系

- 对比度的具体颜色规则在 [`color.md`](../dimensions/color.md) 第 6 节(增强)
- Touch 与 Accessibility 同为 CRITICAL,共同覆盖移动端可达性
- 动画降级与 [`dials.md`](./dials.md) MOTION_INTENSITY 联动
- 所有 CRITICAL 项不可被任何其他规则覆盖,见 [`rules-priority.md`](./rules-priority.md) 第 4 条
