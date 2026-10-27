---
name: message
description: 通知(一级)—— 系统通知列表 + 已读/未读两态
background: "{color-surface-base}"
components: [navigation, list, icon]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 通知(message)

**thesis**: 通知只报事实——谁在何时对你做了什么,已读未读一眼分清
**own-world**: 左图标右文案的两栏行式,未读只用圆点与字重两个低噪声信号,不上整行底色
**first-viewport**: 首屏至少 4 行通知,其中至少 1 行未读(圆点 + 加粗标题)
**signature-interaction**: tap 单行即标记已读(圆点消失、字重回落),导航右侧一键全部已读

一级页面,自首页导航右侧消息图标进入(ui/home.md §1)。系统通知在 ui/message.md,与 ui/messages.md(会话)分工:本页只收系统下发。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"通知" / 右侧全部已读。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=tap=全部标记已读(action:mark-all-read); state=按下高亮

## 2. 系统通知列表

页面主体第 1 区,通知行列表,按下发时间倒序,滚动到底自动加载。

| 参数       | 值                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------ |
| 组件类型 | `list` + `icon`(现有 + P1,组合:通知行列表 + 左侧类型图标)                               |
| 行高       | 56px                                                                                             |
| 图标       | `{icon-size-md}`,颜色 `{color-text-secondary}`,未读行 `{color-brand-primary}`                  |
| 标题字号   | 未读行 `{font-size-body}` + `{font-weight-semibold}` / 已读行 `{font-weight-regular}`,颜色 `{color-text-primary}` |
| 摘要字号   | `{font-size-caption}`,颜色 `{color-text-secondary}`                                            |
| 时间字号   | `{font-size-mini}`,颜色 `{color-text-secondary}`                                                |
| 未读圆点   | 8px 圆点,`{color-brand-primary}`,位于行首图标右上角                                           |
| 分割线     | `{border-hairline}` + `{color-divider}`                                                          |
| padding    | 0 `{spacing-lg}`                                                                                 |
| aria-label | 每行用对应通知标题 + 已读/未读态(如"审核结果,未读"),容器 aria-label="系统通知列表"        |
| intent     | 已读/未读只用圆点与字重区分,不用整行底色:通知页不能比内容本身还吵                            |
| action     | tap=标记该行已读并展开摘要全文; state=圆点消失 + 标题字重回落(`{motion-duration-fast}`); db=UPDATE notifications SET read_at=?; api=GET /api/notifications; long-press=删除该行通知 |

### 2.1 item 字段结构

每条通知是一个数据对象:

| 字段      | 类型    | 约束                                    | 展示规则                 |
| --------- | ------- | --------------------------------------- | ------------------------ |
| `id`      | string  | 必填,唯一,kebab-case                   | 不展示,用作 key         |
| `type`    | string  | 必填,枚举 announce/review/activity/wallet | 决定左侧类型图标       |
| `icon`    | token   | 必填,引用 `{icon-*}`                   | 行首类型图标             |
| `title`   | string  | 必填,≤16 中文字符                       | 行标题                   |
| `summary` | string  | 选填,≤60 中文字符                       | 标题下摘要,tap 展开全文  |
| `time`    | string  | 必填,相对时间(如 10 分钟前)          | 行尾时间                 |
| `read`    | boolean | 必填,默认 true                          | 已读/未读两态            |

### 2.2 默认通知内容

| 顺序 | id              | type     | icon           | title            | summary                  | time     | read  |
| ---- | --------------- | -------- | -------------- | ---------------- | ------------------------ | -------- | ----- |
| 1    | ntf-review-pass | review   | {icon-shield}  | 你的作品已通过审核 | 「雾中山色」已进入推荐池 | 10 分钟前 | false |
| 2    | ntf-activity    | activity | {icon-activity} | 每周挑战已开启   | 本期主题:纸上城市        | 2 小时前 | false |
| 3    | ntf-wallet      | wallet   | {icon-wallet}  | 提现已到账       | 500.00 元已到银行卡      | 昨天     | true  |
| 4    | ntf-version     | announce | {icon-version} | 新版本 v1.1.0 上线 | 修复若干问题,优化性能   | 3 天前   | true  |

## 3. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-divider}` → 暗色变体(低对比分割线)
- `{color-brand-primary}` → 暗色保持色相,略降饱和度(未读圆点与未读行图标)

## 4. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"首页"——本页自首页导航右侧消息图标进入,动线归属首页,选中态维持首页;tap dock"消息"切至 ui/messages.md(会话列表)
