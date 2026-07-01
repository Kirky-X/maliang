---
name: nav-bar
description: 顶部导航栏 —— 跨页面复用,页面首章引用
background: "{color-surface-card}"
components: [navigation, button, icon, text]
updated: 2026-07-02
version: 1.2.0
---

# 顶部导航栏(nav-bar)

页面顶部固定,承载返回 / 标题 / 操作。由各页面 markdown 的**首章**引用,不重复定义。

## 1. 参数

| 参数     | 值                                | 说明         |
| -------- | --------------------------------- | ------------ |
| 组件类型 | `navigation`(P1,导航容器)                                              |              |
| 宽度     | match-parent(375px 基准)          | 撑满屏宽     |
| 高度     | 44px                              | 导航栏高度   |
| 背景颜色 | `{color-surface-card}`                  | 引用 token   |
| 底部分割 | `{border-hairline}` + `{color-divider}` | 0.5px 分割线 |
| padding  | 0 `{spacing-lg}`                  | 左右安全区   |
| action   | tap=无(容器); state=无; db=无; api=无; long-press=无 | 容器无交互,交互在子组件 |

## 2. 子组件(从左到右)

### 2.1 左侧:返回按钮

| 参数     | 值                          |
| -------- | --------------------------- |
| 组件类型 | `button` + `icon`(P0 + P1,组合:可点击按钮 + 图标) |
| 图标     | icon-back, `{icon-size-lg}` |
| 热区     | `{icon-touch-target}`       |
| 字体颜色 | `{color-text-primary}`            |
| action   | tap=→上一页(history.back); state=无; db=无; api=无; long-press=无 |

### 2.2 中间:标题

| 参数     | 值                       |
| -------- | ------------------------ |
| 组件类型 | `text`(现有组件,文本展示)     |
| 字体大小 | `{font-size-h3}`         |
| 字重     | `{font-weight-semibold}` |
| 字体颜色 | `{color-text-primary}`         |
| 对齐     | center                   |
| action   | tap=无(纯展示); state=无; db=无; api=无; long-press=无 |

### 2.3 右侧:操作按钮

| 参数      | 值                                           |
| --------- | -------------------------------------------- |
| 组件类型 | `button` + `icon`(P0 + P1,组合:可点击按钮 + 图标)                |
| 图标/文字 | `{icon-size-lg}` / `{font-size-body}`        |
| 字体颜色  | `{color-text-primary}`(主操作用 `{color-brand-primary}`) |
| 热区      | `{icon-touch-target}`                        |
| action    | tap=→目标页或触发功能; state=按下高亮; db=视功能; api=视功能; long-press=无 |
