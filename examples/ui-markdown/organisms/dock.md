---
name: dock
description: 底部 dock 栏(标签栏)—— 跨页面复用,页面末章引用
background: "{color-surface-card}"
components: [navigation, button, icon, text]
updated: 2026-07-02
version: 1.2.0
---

# 底部 dock 栏(dock)

页面底部固定,承载 3-5 个一级页面入口。由各页面 markdown 的**末章**引用,不重复定义。

## 1. 参数

| 参数     | 值                                | 说明         |
| -------- | --------------------------------- | ------------ |
| 组件类型 | `navigation`(P1,导航容器)                                |              |
| 宽度     | match-parent                      | 撑满屏宽     |
| 高度     | 56px + safe-area-inset-bottom     | 含底部安全区 |
| 背景颜色 | `{color-surface-card}`                  | 引用 token   |
| 顶部分割 | `{border-hairline}` + `{color-divider}` | 0.5px 分割线 |
| padding  | `{spacing-sm}` 0 0 0              | 顶部内边距   |
| action   | tap=无(容器); state=无; db=无; api=无; long-press=无 | 容器自身无交互,交互在子 item |

## 2. 子组件(从左到右:tab 项)

每个 tab:图标(上)+ 文字(下)。

> **组件类型**:`button` + `icon` + `text`(P0 + P1 + 现有组件,组合:可点击 tab 按钮 + 图标 + 文字)

| 参数     | 选中态                | 未选中态              |
| -------- | --------------------- | --------------------- |
| 图标风格 | 填充(filled)          | 线性(stroke)          |
| 图标尺寸 | `{icon-size-lg}`      | `{icon-size-lg}`      |
| 字体颜色 | `{color-text-primary}`      | `{color-text-secondary}`    |
| 字体大小 | `{font-size-mini}`    | `{font-size-mini}`    |
| 热区     | `{icon-touch-target}` | `{icon-touch-target}` |
| aria-label | 每个 tab 用对应 label 字段值(如"首页"/"发现"),容器 aria-label="底部导航" | 同左 |
| action   | tap=跳转至 §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无 | tap=跳转至 §3.1 target 声明的一级页面; state=切换选中态; db=无; api=无; long-press=无 |

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
| 3    | messages | 消息  | icon-messages-filled | icon-messages-stroke | ui/messages.md     | false            |
| 4    | mine     | 我的  | icon-mine-filled     | icon-mine-stroke     | ui/mine.md         | false            |

各页面引用本组件时,**末章必须明确列出本页 dock 的 tab 文字与选中项**(如"首页(选中) / 发现 / 消息 / 我的"),禁止只写"引用 dock"而无文字内容。

### 3.2 item 展示规则

- 选中态:图标用 `icon-filled`(brand-primary),文字色 `{color-text-primary}`,图标上方可加 2px 高 `{color-brand-primary}` 顶条指示。**设计决策(2026-10)**:选中文字色不用 brand-primary——label 为 10px 小字,brand-primary 在 `{color-surface-card}` 上对比度仅 3.46:1 < 4.5:1,过不了自家对比度门(preview-check 5.3);选中语义由 icon-filled + brand-primary 顶条承载(图形元素 ≥3:1 达标)
- 未选中态:图标用 `icon-stroke`,文字色 `{color-text-secondary}`
- 切换动画:图标 200ms 渐变,文字色 150ms 渐变
- badge 角标:右上角 8px 圆点 `{color-danger}`,数字>99 显示"99+"

## 4. 中心凸起位(可选)

dock 可含 1 个中心凸起主操作位(发布/创作类一级动作),位于中间两个 tab 之间。凸起必须同时声明三要素——凸起量、水平锚定、与相邻 tab 的基线关系(判据见 [`alignment.md`](../../../references/dimensions/alignment.md) 凸起与越界关系;缺任一即 G45)。

> **组件类型**:`button` + `icon`(P0 + P1,组合:圆形主操作按钮 + 图标)

| 参数     | 值                                 | 说明                                   |
| -------- | ---------------------------------- | -------------------------------------- |
| 组件类型 | `button` + `icon`                  | 圆形按钮 + 图标组合                     |
| 宽度     | 56px                               | 圆形直径,满足触控 ≥44px                 |
| 高度     | 56px                               | 同上                                    |
| 凸起量   | `{spacing-lg}`(24px),≤ 按钮高的 50% | 超出即与相邻 tab 基线断裂(G45)          |
| 水平锚定 | dock 水平中轴,偏差 ≤ 2px            | 两侧 tab 与凸起位等距                    |
| 基线关系 | 两侧 tab 的图标顶/文字基线与其余 tab 保持同一水平线,不为凸起让位 | 见 [`alignment.md`](../../../references/dimensions/alignment.md) 同排等高 |
| 圆角     | `{radius-full}`                    | 圆形                                    |
| 背景颜色 | `{color-brand-primary}`            | 主操作唯一实心(ux-rules primary-solid-unique) |
| 图标     | `{icon-compose-stroke}`,`{icon-size-xl}`,线性,颜色继承按钮反白文字色 | 图标定框,禁内容天然高度决定行位 |
| aria-label | 主操作名(如"发布")              |                                         |
| action   | tap=跳转至发布页或弹出版创面板(按页面声明); state=按下缩放 0.96(200ms); db=无; api=无; long-press=无 | 交互在按钮,不在容器 |

无中心凸起位时,本节整节省略,dock 退化为纯 tab 栏。

## 5. 暗色模式

本组件暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-card}` → 暗色变体(深卡片底)
- `{color-brand-primary}` → 暗色保持色相
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-divider}` → 暗色变体(低对比分割线)
