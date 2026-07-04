---
name: home
description: 首页 —— 搜索 + 金刚区入口 + 内容流
background: "{color-surface-base}"
components: [navigation, input, icon, grid, button, list, card]
updated: 2026-07-02
version: 1.2.0
---

# 首页(home)

## 1. 顶部导航

<!-- 布局组织见 ../../references/dimensions/layout.md -->

引用 [`organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧菜单 / 中间标题"首页" / 右侧消息。
- nav-bar action:左=tap→抽屉菜单; 中=无; 右=tap→ui/message.md

## 2. 搜索栏

页面主体第 1 区。椭圆形搜索框,右侧搜索图标(填充样式),左侧 hint 占位文案。**真输入框**(非搜索入口),submit 触发搜索跳转。

| 参数          | 值                              |
| ------------- | ------------------------------- |
| 组件类型      | `input` + `icon`(P0 + P1,组合:搜索输入框 + 右侧搜索图标,引用 framework/index.md) |
| 宽度          | match-parent − 2×`{spacing-lg}` |
| 高度          | 44px                            |
| 圆角          | `{radius-full}`(胶囊形)         |
| 背景颜色      | `{color-surface-base}`(灰底胶囊)      |
| 字体颜色      | `{color-text-placeholder}`            |
| padding       | 0 `{spacing-md}`                |
| input-type    | search                          |
| placeholder   | "请输入搜索的关键词"            |
| maxlength     | 30                              |
| aria-label    | "搜索框"                        |
| icon-right    | `{icon-search-filled}`,`{icon-size-md}`,填充样式,位于右侧,aria-label="搜索" |
| action        | submit=→ui/search.md?q={input-value}; focus=聚焦变白底+弹出键盘; blur=失焦收起键盘; input=实时联想(可选); db=无; api=GET /api/search/suggest?q=?; long-press=无 |

## 3. 金刚区入口

页面主体第 2 区,4-8 个图标入口网格。

| 参数     | 值                    |
| -------- | --------------------- |
| 组件类型 | `grid` + `button` + `icon`(P0 + P0 + P1,组合:网格容器 + 可点击图标按钮) |
| 图标尺寸 | `{icon-size-xl}`      |
| 图标颜色 | `{color-brand-primary}`     |
| 字体大小 | `{font-size-caption}` |
| 字体颜色 | `{color-text-secondary}`    |
| 间距     | `{spacing-md}`        |
| aria-label | 每个 item 用对应 label(如"信息流"/"排行榜"),容器 aria-label="金刚区入口" |
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
| 组件类型 | `list` + `card`(P0 + P2,组合:瀑布流列表 + 卡片项) |
| 卡片背景 | `{color-surface-card}`   |
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

## 5. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-brand-primary}` → 暗色保持色相,略降饱和度

## 6. 底部 dock

引用 [`organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:详见 organisms/dock.md 第 2 节,tap=→对应一级页面; state=切换选中态
