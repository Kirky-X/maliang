---
name: service
description: 客服(一级)—— 帮助中心入口 + FAQ 列表 + 联系客服主按钮
background: "{color-surface-base}"
components: [navigation, grid, button, icon, list]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 客服(service)

**thesis**: 先自助后人工——帮助主题与 FAQ 前置分流,联系客服是走完自助仍无解后的最后一步
**own-world**: 灰底白卡三段式(入口网格 / FAQ 手风琴 / 主按钮),品牌色全页只落在"联系客服"一处实心
**first-viewport**: 2×2 帮助入口 + 首屏至少 2 条 FAQ + 主按钮入镜
**signature-interaction**: FAQ 行 tap 原位展开答案(手风琴互斥),不跳页不打断排障节奏

一级页面,自首页金刚区"客服"进入(ui/home.md §3.2),钱包页导航右侧同入口(ui/wallet.md §1)。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"客服" / 右侧无。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=无

## 2. 帮助中心入口

页面主体第 1 区,2×2 帮助主题网格,高频问题分类直达。

| 参数       | 值                                                                                  |
| ---------- | ------------------------------------------------------------------------------------ |
| 组件类型 | `grid` + `button` + `icon`(P1 + 现有 + P1,组合:网格容器 + 可点击入口 + 主题图标) |
| 列数       | 2                                                                                    |
| 入口高度   | 96px                                                                                 |
| 图标尺寸   | `{icon-size-xl}`                                                                     |
| 图标颜色   | `{color-brand-primary}`                                                              |
| 字体大小   | `{font-size-caption}`                                                                |
| 字体颜色   | `{color-text-primary}`                                                               |
| 间距       | `{spacing-sm}`                                                                       |
| padding    | `{spacing-md}`                                                                       |
| aria-label | 每个 item 用对应 label(如"账号申诉"/"支付与钱包"),容器 aria-label="帮助主题入口"  |
| intent     | 高频四类前置分流,降低人工会话量:入口直达 FAQ 对应分组,而非全部涌向在线客服        |
| action     | tap=展开对应 FAQ 分组(action:expand-faq-group); state=按下高亮; db=无; api=GET /api/help/topics; long-press=无 |

### 2.1 item 字段结构

每个帮助入口是一个数据对象:

| 字段     | 类型   | 约束                  | 展示规则         |
| -------- | ------ | --------------------- | ---------------- |
| `id`     | string | 必填,唯一,kebab-case | 不展示,用作 key |
| `label`  | string | 必填,≤6 中文字符      | 图标下方文字     |
| `icon`   | token  | 必填,引用 `{icon-*}` | 入口图标         |
| `target` | string | 必填,`action:` 动作标识 | tap 定位目标     |

### 2.2 默认帮助主题内容

| 顺序 | id      | label      | icon            | target            |
| ---- | ------- | ---------- | --------------- | ----------------- |
| 1    | account | 账号申诉   | {icon-settings} | action:faq-account |
| 2    | payment | 支付与钱包 | {icon-wallet}   | action:faq-payment |
| 3    | report  | 内容举报   | {icon-shield}   | action:faq-report |
| 4    | suggest | 功能建议   | {icon-feedback} | action:faq-suggest |

## 3. FAQ 列表

页面主体第 2 区,常见问题手风琴列表,默认全部收起,按更新时间排序。

| 参数       | 值                                                                     |
| ---------- | ----------------------------------------------------------------------- |
| 组件类型 | `list`(现有组件,组合:FAQ 行列表,行内含问题与可展开答案)           |
| 行高       | 48px(收起态)                                                         |
| padding    | 0 `{spacing-lg}`                                                        |
| 问题字号   | `{font-size-body}`,颜色 `{color-text-primary}`                         |
| 答案字号   | `{font-size-caption}`,颜色 `{color-text-secondary}`                    |
| 分割线     | `{border-hairline}` + `{color-divider}`                                 |
| aria-label | 行用对应问题文字,展开态标注 expanded,容器 aria-label="常见问题列表" |
| intent     | 手风琴原位展开不跳页:答案多数两行以内,跳新页反而打断自助排障节奏    |
| action     | tap=展开/收起该条答案(手风琴互斥); state=展开图标旋转 180 度 + 答案区插入; db=无; api=GET /api/help/faq; long-press=无 |

### 3.1 item 字段结构

每条 FAQ 是一个数据对象:

| 字段       | 类型   | 约束                  | 展示规则           |
| ---------- | ------ | --------------------- | ------------------ |
| `id`       | string | 必填,唯一,kebab-case | 不展示,用作 key   |
| `group`    | string | 必填,§2.2 分组标识    | 分组锚点           |
| `question` | string | 必填,≤24 中文字符     | 收起态行文字       |
| `answer`   | string | 必填,≤200 中文字符    | 展开态答案文本     |

### 3.2 默认 FAQ 内容

| 顺序 | id           | group   | question           | answer(节选)                   |
| ---- | ------------ | ------- | ------------------ | -------------------------------- |
| 1    | faq-withdraw | payment | 提现多久到账       | 银行卡 1-3 个工作日,余额实时    |
| 2    | faq-unban    | account | 账号被误封如何申诉 | 提交申诉后 48 小时内人工复核     |
| 3    | faq-report   | report  | 举报后多久处理     | 24 小时内出结果,站内通知告知    |
| 4    | faq-suggest  | suggest | 建议被采纳有何反馈 | 采纳后通过系统通知告知           |

## 4. 联系客服主按钮

页面主体第 3 区,人工客服入口,本页唯一实心主按钮。

| 参数       | 值                                                  |
| ---------- | ---------------------------------------------------- |
| 组件类型 | `button`(现有组件,组合:通栏胶囊主按钮)           |
| 宽度       | match-parent − 2×`{spacing-lg}`                      |
| 高度       | 48px                                                 |
| 圆角       | `{radius-full}`                                      |
| 背景颜色   | `{color-brand-primary}`                              |
| 文字颜色   | `{color-text-on-brand}`                              |
| 字体大小   | `{font-size-h2}` + `{font-weight-semibold}`          |
| margin     | `{spacing-md}` `{spacing-lg}`                        |
| aria-label | "联系在线客服"                                       |
| intent     | 主按钮是全页唯一品牌色实心:自助路径走完仍无解时,一步进入人工会话 |
| action     | tap=创建会话并进入客服对话(action:open-support-chat); state=按下变深,`{motion-duration-fast}` 内恢复; db=INSERT support_sessions (id, user_id, channel); api=POST /api/support/session; long-press=无 |

## 5. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-divider}` → 暗色变体(低对比分割线)
- `{color-brand-primary}` → 暗色保持色相,略降饱和度(主按钮底色)

## 6. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"首页"——本页自首页金刚区进入,归属首页动线,选中态维持首页;tap"首页"返回 ui/home.md
