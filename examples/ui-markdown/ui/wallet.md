---
name: wallet
description: 钱包(一级)—— 余额卡 + 账单列表
background: "{color-surface-base}"
components: [navigation, card, statistic, list]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 钱包(wallet)

**thesis**: 余额一眼可读,账单逐笔可查——钱的事不带噪音
**own-world**: 白卡大数居顶,账单行列表素色分隔,全页无彩色装饰
**first-viewport**: 余额卡(余额/可提现/累计收益)+ 首屏至少 3 行账单
**signature-interaction**: 长按余额卡在实值与掩码 •••• 间切换(隐私优先,松开恢复)

一级页面,自首页金刚区"钱包"进入(ui/home.md §3.2)。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"钱包" / 右侧客服。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=tap→ui/service.md(客服,`{icon-service}`); state=按下高亮

## 2. 余额卡

页面主体第 1 区,余额与收益统计卡。

| 参数       | 值                                                                                    |
| ---------- | ------------------------------------------------------------------------------------- |
| 组件类型 | `card` + `statistic`(P2,组合:余额卡容器 + 金额统计数值)                     |
| 卡片背景   | `{color-surface-card}`                                                                |
| 卡片圆角   | `{radius-lg}`                                                                         |
| padding    | `{spacing-md}`                                                                        |
| 阴影       | `{shadow-card}`                                                                       |
| 余额数值   | `{font-size-h1}` + `{font-weight-bold}` + `{font-family-display}`,颜色 `{color-text-primary}` |
| 货币单位   | `{font-size-body}`,颜色 `{color-text-secondary}`                                    |
| 统计标签   | `{font-size-caption}`,颜色 `{color-text-secondary}`                                 |
| 统计数值   | `{font-size-h2}` + `{font-weight-semibold}`,颜色 `{color-text-primary}`             |
| 展示内容   | 三项 statistic:余额(居左大号)/ 可提现 / 累计收益(并排其下)                    |
| intent     | 余额是本页唯一主角:h1 大数 + display 字族制造"一屏一个重心"的层级,其余信息让位       |
| action     | tap=展开收益明细(action:open-income-detail); state=按下高亮; db=无; api=GET /api/wallet/balance; long-press=切换金额掩码(实值与 •••• 互切) |

## 3. 账单列表

页面主体第 2 区,账单行列表,按时间倒序,滚动到底自动加载。

| 参数       | 值                                                                                    |
| ---------- | ------------------------------------------------------------------------------------- |
| 组件类型 | `list`(现有组件,组合:账单行列表)                                            |
| 行高       | 56px                                                                                  |
| padding    | 0 `{spacing-lg}`                                                                      |
| 分割线     | `{border-hairline}` + `{color-divider}`                                               |
| 标题字号   | `{font-size-body}`,颜色 `{color-text-primary}`                                      |
| 时间字号   | `{font-size-caption}`,颜色 `{color-text-secondary}`                                 |
| 金额字号   | `{font-size-body}` + `{font-weight-medium}`:收入 `{color-success}` / 支出 `{color-text-primary}` |
| intent     | 账单只读,分页游标加载;提现等写操作不在本页承载,列表保持纯浏览                        |
| action     | tap=打开账单详情(action:open-bill-detail,按需登记); state=按下高亮; db=无; api=GET /api/wallet/bills?cursor=?; long-press=无 |

### 3.1 账单 item 字段结构

每条账单是一个数据对象:

| 字段     | 类型   | 约束                            | 展示规则                       |
| -------- | ------ | ------------------------------- | ------------------------------ |
| `id`     | string | 必填,唯一,kebab-case           | 不展示,用作 key               |
| `title`  | string | 必填,≤12 字符                  | 行首账单名                     |
| `time`   | string | 必填,YYYY-MM-DD HH:mm 格式     | 标题下方时间                   |
| `amount` | string | 必填,带符号金额                | 行尾金额:收入带 + / 支出带 −  |
| `target` | string | 必填,`action:` 动作标识        | tap 动作目标(账单详情按需登记) |

### 3.2 默认账单内容

| 顺序 | id             | title          | time          | amount  | target              |
| ---- | -------------- | -------------- | ------------- | ------- | ------------------- |
| 1    | bill-commission | 插画约稿结算   | 2026-10-26 18:40 | +680.00 | action:open-bill-detail |
| 2    | bill-withdraw  | 提现至银行卡   | 2026-10-25 09:12 | -500.00 | action:open-bill-detail |
| 3    | bill-challenge | 每周挑战奖励   | 2026-10-24 20:05 | +20.00  | action:open-bill-detail |

## 4. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-divider}` → 暗色变体(低对比分割线)
- `{color-success}` → 暗色保持色相,略降饱和度(收入金额)
- `{shadow-card}` → 暗色随卡片底加深弱化

## 5. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"首页"——本页自首页金刚区进入,归属首页动线,选中态维持首页;tap"首页"返回 ui/home.md
