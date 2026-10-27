---
name: feed
description: 信息流(一级)—— 排序切换 + 内容瀑布流
background: "{color-surface-base}"
components: [navigation, tabs, list, card]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 信息流(feed)

**thesis**: 一屏只做"看内容"——排序贴顶,瀑布流铺满其余空间
**own-world**: 灰底上两列白卡瀑布流,排序 tab 吸顶不随滚动消失,品牌色只落在选中指示条
**first-viewport**: 排序 tabs(综合/最新/最热)+ 首屏至少 3 张内容卡
**signature-interaction**: 长按内容卡唤起分享/收藏/举报菜单,排序切换触发整列刷新

一级页面,自首页金刚区"信息流"进入(ui/home.md §3.2)。内容瀑布流与首页内容流同构(`list` + `card`),保证从首页进入后阅读节奏不变。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"信息流" / 右侧搜索。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=tap→ui/search.md(搜索,`{icon-search-stroke}`); state=按下高亮

## 2. 排序 tabs

页面主体第 1 区,吸顶排序切换:综合 / 最新 / 最热,默认选中"综合"。

| 参数       | 值                                                                                      |
| ---------- | --------------------------------------------------------------------------------------- |
| 组件类型 | `tabs`(P0,组合:横排排序标签,吸顶不随内容滚动)                                  |
| 高度       | 44px                                                                                    |
| 选中态     | 文字 `{color-text-primary}` + `{font-weight-semibold}` + 底部 2px `{color-brand-primary}` 指示条 |
| 未选中态   | 文字 `{color-text-secondary}` + `{font-weight-regular}`                                 |
| 字体大小   | `{font-size-body}`                                                                      |
| 指示条动效 | `{motion-duration-fast}` + `{motion-ease-default}`,滑动跟随                              |
| aria-label | 容器 aria-label="排序切换",每个 tab 用对应文字(综合/最新/最热)                        |
| intent     | 排序是本页唯一状态轴:吸顶 + 底部指示条,让当前排序在任意滚动位置可读                    |
| action     | tap=切换排序并回到列表顶部刷新; state=指示条滑动 + 列表 loading; db=UPDATE user_settings SET feed_sort=?; api=GET /api/feed?sort=?&cursor=?; long-press=无 |

## 3. 内容瀑布流

页面主体第 2 区,两列瀑布流,卡片结构与首页内容流同构。

| 参数     | 值                                                                        |
| -------- | ------------------------------------------------------------------------- |
| 组件类型 | `list` + `card`(现有 + P2,组合:瀑布流列表容器 + 内容卡)          |
| 列数     | 2(按卡片高度交错排布)                                                    |
| 卡片背景 | `{color-surface-card}`                                                    |
| 卡片圆角 | `{radius-rounded}`                                                        |
| 卡片间距 | `{spacing-sm}`                                                            |
| padding  | `{spacing-sm}`                                                            |
| 标题字号 | `{font-size-body}` + `{font-weight-medium}`,颜色 `{color-text-primary}` |
| 辅助字号 | `{font-size-caption}`,颜色 `{color-text-secondary}`                     |
| intent   | 卡片只保留封面 + 标题 + 作者 + 互动数,正文留给详情页                      |
| action   | tap=打开内容详情(action:open-post,详情页按需登记); state=按下底色变 `{color-state-hover}`; db=无; api=GET /api/feed?sort=?&cursor=?; long-press=弹出菜单(分享/收藏/举报) |

### 3.1 卡片 item 字段结构

每张内容卡片是一个数据对象:

| 字段        | 类型   | 约束                            | 展示规则                  |
| ----------- | ------ | ------------------------------- | ------------------------- |
| `id`        | string | 必填,唯一,kebab-case           | 不展示,用作 key          |
| `cover`     | string | 必填,URL                       | 卡片顶部封面图            |
| `title`     | string | 必填,≤20 字符                  | 封面下方标题              |
| `author`    | string | 选填                            | 标题下方作者名            |
| `stats`     | object | 选填,含 likes/comments 两键    | 右下角点赞/评论数         |
| `card-type` | string | 必填,枚举 single/multi/video   | 决定卡片布局              |
| `target`    | string | 必填,`action:` 动作标识        | tap 动作目标(详情页按需登记) |

### 3.2 默认数据样例

| 顺序 | id          | cover       | title               | author | card-type | target     |
| ---- | ----------- | ----------- | ------------------- | ------ | --------- | ---------- |
| 1    | post-aurora | /img/a1.jpg | 极光渐变的三种用法  | 山雾   | single    | action:open-post |
| 2    | post-grid   | /img/a2.jpg | 网格系统的 8px 节奏 | 林一   | multi     | action:open-post |
| 3    | post-motion | /img/a3.mp4 | 入场动效的克制边界  | 白鹿   | video     | action:open-post |

## 4. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-brand-primary}` → 暗色保持色相,略降饱和度
- `{color-state-hover}` → 暗色变体(深底上的按压叠色)

## 5. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"首页"——本页自首页金刚区进入,归属首页动线,选中态维持首页;tap"首页"返回 ui/home.md
