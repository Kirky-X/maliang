---
name: mine
description: 我的(一级)—— 头像资料 + 概览数据 + 设置入口列表
background: "{color-surface-base}"
components: [navigation, image, text, list, button, icon]
updated: 2026-09-05
version: 1.0.0
---

# 我的(mine)

一级页面(P0 必备,见 [`../../../references/default-pages/app.md`](../../../references/default-pages/app.md))。示例链路演示:本页 `ui/mine.md` → `ui/setting/about.md` 的跨层级跳转关系,可由 `scripts/ui-graph.py check-nav` 验证。

## 1. 顶部导航

<!-- 布局组织见 ../../references/dimensions/layout.md -->

引用 [`../../organisms/nav-bar.md`](../../organisms/nav-bar.md)(组件类型:`navigation`):左侧返回(一级页隐藏) / 中间标题"我的" / 右侧扫一扫。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=tap=唤起扫码; state=按下高亮

## 2. 资料卡

页面主体第 1 区,头像 + 昵称 + 签名。

| 参数       | 值                       | 说明 |
| ---------- | ------------------------ | ---- |
| 组件类型 | `image` + `text`(P0 + 现有组件,组合:头像图 + 昵称/签名文本) | |
| 头像尺寸   | 64px                     | 圆形 |
| 头像圆角   | `{radius-full}`          | |
| 昵称字号   | `{font-size-h3}`         | |
| 昵称字重   | `{font-weight-semibold}` | |
| 字体颜色   | `{color-text-primary}`   | |
| 签名字号   | `{font-size-caption}`    | |
| 签名颜色   | `{color-text-secondary}` | |
| padding    | `{spacing-lg}`           | |
| intent     | 资料卡是本页身份锚点,故 64px 大头像 + h3 昵称置于首屏顶部,建立"这是谁的空间"的第一认知 | 决定理由 |
| action     | tap=唤起编辑资料弹层(action:edit-profile); state=按下头像变亮; db=无; api=GET /api/user/profile; long-press=无 | |

## 3. 设置列表

页面主体第 2 区,设置项行列表。

| 参数     | 值                                |
| -------- | --------------------------------- |
| 组件类型 | `list` + `button` + `icon`(现有组件 + P0 + P1,组合:行列表容器 + 可点击行 + 左侧图标) |
| 行高     | 48px                              |
| padding  | 0 `{spacing-lg}`                  |
| 字体大小 | `{font-size-body}`                |
| 字体颜色 | `{color-text-primary}`            |
| 分割线   | `{border-hairline}` + `{color-divider}` |
| aria-label | 每行用对应 label 字段值(如"设置"/"关于"),容器 aria-label="设置列表" |
| intent   | "关于"入口是本页唯一跨层级跳转边(mine → setting/about),用于演示 ui-graph 层级关系 |
| action   | tap=→ui/setting/about.md; 其余行=按 §3.2 item.target 跳转; state=按下高亮; db=无; api=无; long-press=无 |

### 3.1 item 字段结构

每个设置项是一个数据对象:

| 字段          | 类型    | 约束                          | 展示规则                |
| ------------- | ------- | ----------------------------- | ----------------------- |
| `id`          | string  | 必填,唯一,kebab-case          | 不展示,用作 key         |
| `label`       | string  | 必填,≤10 中文字符             | 行左侧文字              |
| `icon-left`   | token   | 选填,引用 `{icon-*}`          | 行最左侧图标(可选)      |
| `value-right` | string  | 选填                          | 行右侧文字(如版本号)    |
| `arrow`       | boolean | 选填,默认 true                | 行右侧是否显示箭头      |
| `target`      | string  | 必填,目标页或动作标识         | tap 跳转目标            |

### 3.2 默认设置列表内容

| 顺序 | id          | label   | icon-left      | value-right | target                    |
| ---- | ----------- | ------- | -------------- | ----------- | ------------------------- |
| 1    | settings    | 设置    | icon-settings  |             | action:open-settings      |
| 2    | wallet      | 钱包    | icon-wallet    |             | action:open-wallet        |
| 3    | about       | 关于    | icon-info      | v1.0.0      | ui/setting/about.md       |
| 4    | feedback    | 意见反馈 | icon-feedback |             | action:open-feedback      |

## 4. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-divider}` → 暗色变体(低对比分割线)

## 5. 底部 dock

引用 [`../../organisms/dock.md`](../../organisms/dock.md)(组件类型:`navigation`):首页 / 发现 / 消息 / **我的(选中)**。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
