---
name: activity
description: 活动(一级)—— 活动横幅 + 活动列表
background: "{color-surface-base}"
components: [navigation, image, list, card, tag]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 活动(activity)

**thesis**: 一张横幅定调当期主活动,列表承接其余活动的报名与回看
**own-world**: 通栏大图横幅压顶,下方白卡行列表,状态色只落在 tag 描边文字
**first-viewport**: 活动横幅 + 首屏至少 2 行活动(状态 tag 可读)
**signature-interaction**: 点横幅直达当期主活动详情,是本页唯一的大图动线

一级页面,自首页金刚区"活动"进入(ui/home.md §3.2)。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"活动" / 右侧无。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=无(本页无顶部操作)

## 2. 活动横幅

页面主体第 1 区,通栏当期主活动横幅。

| 参数       | 值                                                        |
| ---------- | --------------------------------------------------------- |
| 组件类型 | `image`(P0,组合:通栏活动横幅,当期主活动入口)    |
| 宽度       | match-parent − 2×`{spacing-lg}`                           |
| 高度       | 160px                                                     |
| 圆角       | `{radius-lg}`                                             |
| 缩放       | cover(裁切居中)                                         |
| 占位底色   | 加载中显示 `{color-surface-base}`                         |
| intent     | 横幅是本页唯一大图,承担"当期主活动"第一动线,其余活动退到列表 |
| action     | tap=打开当期主活动详情(action:open-activity-detail,按需登记); state=按下底色变 `{color-state-hover}`; db=无; api=GET /api/activities/banner; long-press=无 |

## 3. 活动列表

页面主体第 2 区,活动行卡列表,按开始时间倒序。

| 参数       | 值                                                                                            |
| ---------- | --------------------------------------------------------------------------------------------- |
| 组件类型 | `list` + `card` + `tag`(现有 + P2,组合:活动行卡 + 状态标签)                         |
| 行高       | 72px                                                                                          |
| 卡片背景   | `{color-surface-card}`                                                                        |
| 卡片圆角   | `{radius-rounded}`                                                                            |
| 行间距     | `{spacing-sm}`                                                                                |
| padding    | `{spacing-md}`                                                                                |
| 封面尺寸   | 88px × 88px,圆角 `{radius-rounded}`                                                          |
| 标题字号   | `{font-size-body}` + `{font-weight-medium}`,颜色 `{color-text-primary}`                     |
| 时间字号   | `{font-size-caption}`,颜色 `{color-text-secondary}`                                         |
| 状态 tag   | 文字 `{font-size-mini}`,描边 `{border-thin}` + `{color-border-base}`:进行中 `{color-success}` / 即将开始 `{color-warning}` / 已结束 `{color-text-disabled}` |
| intent     | 状态三分决定行为:进行中可报名、即将开始可提醒、已结束只可回看                                 |
| action     | tap=打开活动详情(action:open-activity-detail); state=按下高亮; db=无; api=GET /api/activities?cursor=?; long-press=无 |

### 3.1 活动项 item 字段结构

每个活动项是一个数据对象:

| 字段         | 类型   | 约束                                | 展示规则               |
| ------------ | ------ | ----------------------------------- | ---------------------- |
| `id`         | string | 必填,唯一,kebab-case               | 不展示,用作 key       |
| `cover`      | string | 必填,URL                           | 行首封面缩略图         |
| `title`      | string | 必填,≤16 字符                      | 封面右侧标题           |
| `start-time` | string | 必填,YYYY-MM-DD 格式               | 标题下方时间           |
| `status`     | string | 必填,枚举 ongoing/upcoming/ended   | 状态 tag 文案与颜色    |
| `target`     | string | 必填,`action:` 动作标识            | tap 动作目标(详情页按需登记) |

### 3.2 默认活动列表内容

| 顺序 | id                | title            | start-time | status | target          |
| ---- | ----------------- | ---------------- | ---------- | ------ | ------------ |
| 1    | act-spring-marathon | 新春设计马拉松 | 2026-11-01 | ongoing | action:open-activity-detail |
| 2    | act-weekly-challenge | 每周封面挑战赛 | 2026-11-09 | upcoming | action:open-activity-detail |
| 3    | act-type-review   | 字体设计复盘展   | 2026-10-12 | ended   | action:open-activity-detail |

## 4. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-text-disabled}` → 暗色变体(已结束状态)
- `{color-border-base}` → 暗色变体(tag 描边)
- `{color-success}` / `{color-warning}` → 暗色保持色相,略降饱和度(状态 tag)
- `{color-state-hover}` → 暗色变体(深底上的按压叠色)

## 5. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"首页"——本页自首页金刚区进入,归属首页动线,选中态维持首页;tap"首页"返回 ui/home.md
