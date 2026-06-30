---
name: dock
description: 底部 dock 栏(标签栏)—— 跨页面复用,页面末章引用
background: "{surface-card}"
updated: 2026-06-30
version: 1.1.0
---

# 底部 dock 栏(dock)

页面底部固定,承载 3-5 个一级页面入口。由各页面 markdown 的**末章**引用,不重复定义。

## 1. 参数

| 参数     | 值                                | 说明         |
| -------- | --------------------------------- | ------------ |
| 宽度     | match-parent                      | 撑满屏宽     |
| 高度     | 56px + safe-area-inset-bottom     | 含底部安全区 |
| 背景颜色 | `{surface-card}`                  | 引用 token   |
| 顶部分割 | `{border-hairline}` + `{divider}` | 0.5px 分割线 |
| padding  | `{spacing-sm}` 0 0 0              | 顶部内边距   |
| action   | tap=无(容器); state=无; db=无; api=无; long-press=无 | 容器自身无交互,交互在子 item |

## 2. 子组件(从左到右:tab 项)

每个 tab:图标(上)+ 文字(下)。

| 参数     | 选中态                | 未选中态              |
| -------- | --------------------- | --------------------- |
| 图标风格 | 填充(filled)          | 线性(stroke)          |
| 图标尺寸 | `{icon-size-lg}`      | `{icon-size-lg}`      |
| 字体颜色 | `{brand-primary}`     | `{text-secondary}`    |
| 字体大小 | `{font-size-mini}`    | `{font-size-mini}`    |
| 热区     | `{icon-touch-target}` | `{icon-touch-target}` |
| action   | tap=→目标页; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无 | tap=→目标页; state=切换选中态; db=无; api=无; long-press=无 |

tab 数 ≤ 5(米勒定律)。

## 3. tab item 字段结构

每个 tab item 是一个数据对象,完整字段如下:

| 字段              | 类型    | 约束                          | 展示规则                          |
| ----------------- | ------- | ----------------------------- | --------------------------------- |
| `id`              | string  | 必填,唯一,kebab-case          | 不展示,用作 key                   |
| `label`           | string  | 必填,≤4 中文字符              | 图标下方文字                      |
| `icon-filled`     | token   | 必填,引用 `{icon-*}`          | 选中态显示                        |
| `icon-stroke`     | token   | 必填,引用 `{icon-*}`          | 未选中态显示                      |
| `target`          | string  | 必填,页面路径(如 `ui/home.md`)| tap 跳转目标                      |
| `default-selected`| boolean | 选填,默认 false               | 页面加载时是否选中                |
| `badge`           | number  | 选填,≥0                       | 右上角红点角标,0/缺省=不显示      |

### 3.1 默认 dock 文字内容(一级页面配置)

应用默认 dock 含 4 个 tab,从左到右文字与配置如下:

| 顺序 | id     | label | icon-filled         | icon-stroke         | target            | default-selected |
| ---- | ------ | ----- | ------------------- | ------------------- | ----------------- | ---------------- |
| 1    | home   | 首页  | icon-home-filled    | icon-home-stroke    | ui/home.md        | true             |
| 2    | discover | 发现 | icon-discover-filled| icon-discover-stroke| ui/discover.md    | false            |
| 3    | message | 消息  | icon-message-filled | icon-message-stroke | ui/message.md     | false            |
| 4    | profile | 我的  | icon-profile-filled | icon-profile-stroke | ui/profile.md     | false            |

各页面引用本组件时,**末章必须明确列出本页 dock 的 tab 文字与选中项**(如"首页(选中) / 发现 / 消息 / 我的"),禁止只写"引用 dock"而无文字内容。

### 3.2 item 展示规则

- 选中态:图标用 `icon-filled`,文字色 `{brand-primary}`,图标上方可加 2px 高 `{brand-primary}` 顶条指示
- 未选中态:图标用 `icon-stroke`,文字色 `{text-secondary}`
- 切换动画:图标 200ms 渐变,文字色 150ms 渐变
- badge 角标:右上角 8px 圆点 `{danger}`,数字>99 显示"99+"
