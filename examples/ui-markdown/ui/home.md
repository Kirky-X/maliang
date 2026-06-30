---
name: home
description: 首页 —— 搜索 + 金刚区入口 + 内容流
background: "{surface-base}"
updated: 2026-06-30
version: 1.1.0
---

# 首页(home)

## 1. 顶部导航

引用 [`organisms/nav-bar.md`](../organisms/nav-bar.md):左侧菜单 / 中间标题"首页" / 右侧消息。
- nav-bar action:左=tap→抽屉菜单; 中=无; 右=tap→ui/message.md

## 2. 搜索栏

页面主体第 1 区。

| 参数     | 值                              |
| -------- | ------------------------------- |
| 宽度     | match-parent − 2×`{spacing-lg}` |
| 高度     | 36px                            |
| 圆角     | `{radius-full}`                 |
| 背景颜色 | `{surface-base}`(灰底胶囊)      |
| 字体颜色 | `{text-placeholder}`            |
| padding  | 0 `{spacing-md}`                |
| action   | tap=→ui/search.md; state=聚焦变白底; db=无; api=无; long-press=无 |

## 3. 金刚区入口

页面主体第 2 区,4-8 个图标入口网格。

| 参数     | 值                    |
| -------- | --------------------- |
| 图标尺寸 | `{icon-size-xl}`      |
| 图标颜色 | `{brand-primary}`     |
| 字体大小 | `{font-size-caption}` |
| 字体颜色 | `{text-secondary}`    |
| 间距     | `{spacing-md}`        |
| action   | tap=→对应目标页; state=按下高亮; db=无; api=无; long-press=无 |

### 3.1 item 字段结构

每个金刚区入口是一个数据对象:

| 字段        | 类型    | 约束                          | 展示规则          |
| ----------- | ------- | ----------------------------- | ----------------- |
| `id`        | string  | 必填,唯一,kebab-case          | 不展示,用作 key   |
| `label`     | string  | 必填,≤4 中文字符              | 图标下方文字      |
| `icon`      | token   | 必填,引用 `{icon-*}`          | 图标展示          |
| `target`    | string  | 必填,页面路径                 | tap 跳转目标      |
| `badge`     | number  | 选填,≥0                       | 右上角角标        |
| `sort-order`| number  | 必填,≥1                       | 网格排列顺序      |

### 3.2 默认金刚区内容

| 顺序 | id        | label | icon           | target           |
| ---- | --------- | ----- | -------------- | ---------------- |
| 1    | feed      | 信息流 | icon-feed      | ui/feed.md       |
| 2    | rank      | 排行榜 | icon-rank      | ui/rank.md       |
| 3    | category  | 分类  | icon-category  | ui/category.md   |
| 4    | activity  | 活动  | icon-activity  | ui/activity.md   |
| 5    | wallet    | 钱包  | icon-wallet    | ui/wallet.md     |
| 6    | service   | 客服  | icon-service   | ui/service.md    |

## 4. 内容流

页面主体第 3 区,卡片瀑布流。

| 参数     | 值                 |
| -------- | ------------------ |
| 卡片背景 | `{surface-card}`   |
| 卡片圆角 | `{radius-rounded}` |
| 卡片间距 | `{spacing-md}`     |
| padding  | `{spacing-md}`     |
| action   | tap=→卡片详情页; state=按下底色变浅; db=无; api=GET /api/feed?cursor=?; long-press=弹出菜单(分享/收藏/举报) |

### 4.1 卡片 item 字段结构

每张内容卡片是一个数据对象:

| 字段          | 类型    | 约束                  | 展示规则              |
| ------------- | ------- | --------------------- | --------------------- |
| `id`          | string  | 必填,唯一             | 不展示,用作 key       |
| `cover`       | string  | 必填,URL              | 卡片顶部封面图        |
| `title`       | string  | 必填,≤20 字符         | 封面下方标题          |
| `author`      | string  | 选填                  | 标题下方作者名        |
| `stats`       | object  | 选填,{likes,comments} | 右下角点赞/评论数     |
| `card-type`   | string  | 必填,枚举(single/multi/video) | 决定卡片布局 |
| `target`      | string  | 必填,详情页路径       | tap 跳转目标          |

## 5. 底部 dock

引用 [`organisms/dock.md`](../organisms/dock.md):首页(选中) / 发现 / 消息 / 我的。
- dock action:详见 organisms/dock.md 第 2 节,tap=→对应一级页面; state=切换选中态
