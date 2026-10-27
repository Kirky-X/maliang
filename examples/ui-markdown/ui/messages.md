---
name: messages
description: 消息(一级)—— 会话列表 + 未读角标
background: "{color-surface-base}"
components: [navigation, list, image, text, badge]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 消息(messages)

**thesis**: 会话即时间线——最近聊过的在上,未读数是唯一抢注意的信号
**own-world**: 白卡行列表铺满,48px 圆头像对齐成列,未读红角标是全页唯一的红色
**first-viewport**: 首屏至少 4 行会话,头像 / 会话名 / 预览 / 时间四要素齐备
**signature-interaction**: 长按会话行唤起置顶/免打扰/删除菜单,tap 进入会话即清零该行未读

一级页面,即 dock"消息"tab 落地页(organisms/dock.md §3.1 target=ui/messages.md)。系统通知在 ui/message.md,与本页分工:本页只收人与人的会话。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"消息" / 右侧发起新会话。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=tap=发起新会话(action:new-chat,`{icon-compose-stroke}`); state=按下高亮

## 2. 会话列表

页面主体第 1 区,会话行列表,按最后消息时间倒序,置顶会话固定在前,滚动到底自动加载。

| 参数       | 值                                                                                                  |
| ---------- | ---------------------------------------------------------------------------------------------------- |
| 组件类型 | `list` + `image` + `text` + `badge`(现有 + P0 + 现有 + P2,组合:行列表容器 + 头像图 + 会话名/预览文字 + 未读角标) |
| 行高       | 72px                                                                                                 |
| 头像尺寸   | 48px,圆形 `{radius-full}`,image 作头像语义                                                          |
| 会话名字号 | `{font-size-body}` + `{font-weight-medium}`,颜色 `{color-text-primary}`                            |
| 预览字号   | `{font-size-caption}`,颜色 `{color-text-secondary}`,超宽省略号截断                                |
| 时间字号   | `{font-size-mini}`,颜色 `{color-text-secondary}`                                                    |
| 未读角标   | `badge` 语义:未读数 >0 显示,底 `{color-danger}`,圆角 `{radius-full}`,白字 `{font-size-mini}`,>99 显示 99+ |
| 分割线     | `{border-hairline}` + `{color-divider}`                                                              |
| padding    | 0 `{spacing-lg}`                                                                                     |
| aria-label | 每行用对应会话名,未读行追加"未读 N 条",容器 aria-label="会话列表"                                |
| intent     | 置顶会话不打断时间线语义:置顶组仅以浅底区分,排序仍以最后消息时间为锚                              |
| action     | tap=进入会话并清零该行未读(action:open-chat,会话页按需登记); state=按下高亮; db=UPDATE conversations SET unread_count=0; api=GET /api/conversations?cursor=?; long-press=唤起会话操作菜单(置顶/免打扰/删除) |

### 2.1 item 字段结构

每个会话是一个数据对象:

| 字段      | 类型    | 约束                    | 展示规则                       |
| --------- | ------- | ----------------------- | ------------------------------ |
| `id`      | string  | 必填,唯一,kebab-case   | 不展示,用作 key               |
| `avatar`  | string  | 必填,URL               | 行首圆形头像图                 |
| `name`    | string  | 必填,≤12 中文字符       | 头像右侧会话名                 |
| `preview` | string  | 必填,≤30 字符           | 会话名下最后一条消息预览       |
| `time`    | string  | 必填,HH:mm 或相对时间   | 行尾时间                       |
| `unread`  | number  | 选填,≥0                 | 行尾未读角标,0/缺省不显示     |
| `pinned`  | boolean | 选填,默认 false         | 是否置顶                       |
| `target`  | string  | 必填,`action:` 动作标识 | tap 动作目标(会话页按需登记)   |

### 2.2 默认会话内容

| 顺序 | id          | avatar      | name   | preview            | time | unread | pinned | target     |
| ---- | ----------- | ----------- | ------ | ------------------ | ---- | ------ | ------ | ---------- |
| 1    | conv-official | /img/av1.jpg | 官方助手 | 你的作品已通过审核 | 14:32 | 2      | true   | action:open-chat |
| 2    | conv-shanwu | /img/av2.jpg | 山雾   | 网格稿明天给你     | 14:05 | 0      | false  | action:open-chat |
| 3    | conv-linyi  | /img/av3.jpg | 林一   | 那张渐变再压一档   | 11:47 | 1      | false  | action:open-chat |
| 4    | conv-bailu  | /img/av4.jpg | 白鹿   | 收到,周内交       | 昨天  | 0      | false  | action:open-chat |

## 3. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-divider}` → 暗色变体(低对比分割线)
- `{color-danger}` → 暗色保持色相,略降饱和度(未读角标底色)

## 4. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页 / 发现 / **消息(选中)** / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"消息"——本页即"消息"tab 落地页(dock §3.1 target=ui/messages.md);再次 tap"消息"回到列表顶部并刷新未读数
