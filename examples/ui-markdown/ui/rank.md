---
name: rank
description: 排行榜(一级)—— 周期切换 + 榜单列表
background: "{color-surface-base}"
components: [navigation, tabs, list, card, badge, avatar]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 排行榜(rank)

**thesis**: 谁在榜上一眼可读——周期切换贴顶,名次序号即视觉锚
**own-world**: 白卡行列表压在灰底上,前三名徽标是全页唯一彩色,其余保持素色
**first-viewport**: 日/周/总 tabs + 首屏至少 5 行榜单(前三名徽标可见)
**signature-interaction**: 切换周期时榜单行按名次错峰入场({motion-duration-fast} 内完成,可跳过)

一级页面,自首页金刚区"排行榜"进入(ui/home.md §3.2)。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"排行榜" / 右侧分享。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=tap=唤起系统分享面板(action:share-sheet,`{icon-share}`); state=按下高亮

## 2. 榜单 tabs

页面主体第 1 区,周期切换:日榜 / 周榜 / 总榜,默认选中"日榜"。

| 参数       | 值                                                                                      |
| ---------- | --------------------------------------------------------------------------------------- |
| 组件类型 | `tabs`(P0,组合:横排周期切换标签)                                              |
| 高度       | 44px                                                                                    |
| 选中态     | 文字 `{color-text-primary}` + `{font-weight-semibold}` + 底部 2px `{color-brand-primary}` 指示条 |
| 未选中态   | 文字 `{color-text-secondary}` + `{font-weight-regular}`                                 |
| 字体大小   | `{font-size-body}`                                                                      |
| aria-label | 容器 aria-label="榜单周期切换",每个 tab 用对应文字(日榜/周榜/总榜)                    |
| intent     | 周期是本页唯一状态轴,选中语义走图形指示条,不用品牌色小字(对齐 dock.md 选中态决策)     |
| action     | tap=切换周期并刷新榜单; state=指示条滑动 + 榜单错峰入场; db=UPDATE user_settings SET rank_period=?; api=GET /api/rank?period=?; long-press=无 |

## 3. 榜单列表

页面主体第 2 区,行卡列表,前三名带徽标。

| 参数       | 值                                                                                        |
| ---------- | ----------------------------------------------------------------------------------------- |
| 组件类型 | `list` + `card` + `badge` + `avatar`(现有 + P2,组合:榜单行卡 + 前三名徽标 + 用户头像) |
| 行高       | 56px                                                                                      |
| 卡片背景   | `{color-surface-card}`                                                                    |
| 卡片圆角   | `{radius-rounded}`                                                                        |
| 行间距     | `{spacing-sm}`                                                                            |
| padding    | `{spacing-md}`                                                                            |
| 名次字号   | `{font-size-h3}` + `{font-weight-semibold}`,颜色 `{color-text-primary}`                 |
| 昵称字号   | `{font-size-body}`,颜色 `{color-text-primary}`                                          |
| 分数字号   | `{font-size-caption}`,颜色 `{color-text-secondary}`                                     |
| 头像尺寸   | 32px,圆形 `{radius-full}`                                                                |
| 排名徽标   | 前三名行首用 `badge`:底色 `{color-warning}`,名次数字 `{color-text-on-brand}` + `{font-size-mini}`;第 4 名起无徽标,名次文字 `{color-text-secondary}` |
| aria-label | 行容器 aria-label="榜单列表",每行朗读"第 N 名 + 昵称 + 分数"                            |
| intent     | 前三名徽标是本页唯一彩色,让"看谁登顶"的视线动线零成本;徽标色底对比度按 token.md ⚠ 注记如实保留 |
| action     | tap=打开用户主页(action:open-user-profile,按需登记); state=按下高亮; db=无; api=GET /api/rank?period=?; long-press=无 |

### 3.1 榜单 item 字段结构

每个榜单项是一个数据对象:

| 字段     | 类型   | 约束                            | 展示规则                   |
| -------- | ------ | ------------------------------- | -------------------------- |
| `id`     | string | 必填,唯一,kebab-case           | 不展示,用作 key           |
| `rank`   | number | 必填,≥1                        | 行首名次,前三名带徽标     |
| `name`   | string | 必填,≤12 字符                  | 昵称                       |
| `avatar` | string | 必填,URL                       | 圆形头像                   |
| `score`  | number | 必填,≥0                        | 行尾得分/票数              |
| `delta`  | number | 选填                            | 名次变化,上升 `{color-success}` / 下降 `{color-danger}` |
| `target` | string | 必填,`action:` 动作标识        | tap 动作目标(用户主页按需登记) |

### 3.2 默认榜单内容(日榜)

| 名次 | id          | name | avatar      | score | target     |
| ---- | ----------- | ---- | ----------- | ----- | ---------- |
| 1    | user-mist   | 山雾 | /img/u1.jpg | 9821  | action:open-user-profile |
| 2    | user-forest | 林一 | /img/u2.jpg | 9410  | action:open-user-profile |
| 3    | user-deer   | 白鹿 | /img/u3.jpg | 9188  | action:open-user-profile |
| 4    | user-stone  | 石青 | /img/u4.jpg | 8955  | action:open-user-profile |
| 5    | user-reed   | 芦芽 | /img/u5.jpg | 8733  | action:open-user-profile |

## 4. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-brand-primary}` → 暗色保持色相,略降饱和度
- `{color-warning}` → 暗色保持色相,略降饱和度(前三名徽标)
- `{color-success}` / `{color-danger}` → 暗色保持色相,略降饱和度(名次变化)

## 5. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"首页"——本页自首页金刚区进入,归属首页动线,选中态维持首页;tap"首页"返回 ui/home.md
