---
name: search
description: 搜索(一级)—— 搜索框 + 热门搜索 + 结果列表
background: "{color-surface-base}"
components: [navigation, input, icon, grid, button, list, card]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 搜索(search)

**thesis**: 输入即出发——搜索框常驻贴顶,submit 才出结果,过程不打断输入
**own-world**: 胶囊搜索框贴顶,热门词 chip 平铺其下,结果卡与首页内容流同构,关键词品牌色高亮是唯一强调
**first-viewport**: 进入即聚焦搜索框 + 热门搜索一排可见
**signature-interaction**: 热搜词 chip 一点即搜(等效 submit),联想只落下拉不整页刷新

一级页面,自首页搜索栏 submit 进入(ui/home.md §2),信息流页导航右侧同入口(ui/feed.md §1)。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"搜索" / 右侧无。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=无

## 2. 搜索框

页面主体第 1 区,真输入框(非搜索入口),submit 触发搜索,与首页搜索栏同构。

| 参数       | 值                                                                                     |
| ---------- | --------------------------------------------------------------------------------------- |
| 组件类型 | `input` + `icon`(P0 + P1,组合:搜索输入框 + 右侧搜索图标,与首页搜索栏同构)          |
| 宽度       | match-parent − 2×`{spacing-lg}`                                                         |
| 高度       | 44px                                                                                    |
| 圆角       | `{radius-full}`(胶囊形)                                                               |
| 背景颜色   | `{color-surface-card}`                                                                  |
| 字体颜色   | `{color-text-primary}`                                                                  |
| padding    | 0 `{spacing-md}`                                                                        |
| input-type | search                                                                                  |
| placeholder | "搜索作品、话题或作者"                                                                |
| maxlength  | 30                                                                                      |
| aria-label | "搜索框"                                                                                |
| icon-right | `{icon-search-filled}`,`{icon-size-md}`,位于右侧,aria-label="搜索"                    |
| intent     | 与首页搜索栏同构(胶囊形 + submit 触发 + aria-label),进入本页即聚焦,零迁移成本     |
| action     | submit=执行搜索并滚动至结果区; focus=弹出键盘; input=实时联想(仅下拉,不整页刷新); db=INSERT search_history (keyword, user_id); api=GET /api/search?q={input-value}; long-press=清空输入 |

## 3. 热门搜索

页面主体第 2 区,热搜词 chip 网格,按平台热度排序,每小时更新。

| 参数       | 值                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------- |
| 组件类型 | `grid` + `button` + `icon`(P1 + 现有 + P1,组合:chip 网格 + 可点击热搜词 + 热度图标语义)   |
| 列数       | 按词长流式排布,自动换行                                                                        |
| 高度       | 44px(含热区)                                                                                  |
| 圆角       | `{radius-full}`                                                                                 |
| 背景颜色   | `{color-surface-base}`                                                                          |
| 字体大小   | `{font-size-caption}`,颜色 `{color-text-primary}`                                              |
| 图标       | `{icon-search-stroke}`,`{icon-size-sm}`(搜索语义;前三名热词图标语义为"上升趋势",token.md 现表未登记,按需登记后替换) |
| 间距       | `{spacing-sm}`                                                                                  |
| padding    | 0 `{spacing-lg}`                                                                                |
| aria-label | 每个 chip 用对应热搜词(如"渐变教程"),容器 aria-label="热门搜索"                            |
| intent     | 热搜词是冷启动的主要出口:chip 一点即搜省去打字,排名只以序号表达,不做颜色强调              |
| action     | tap=以该词执行搜索(等效 submit); state=按下高亮; db=INSERT search_history (keyword, user_id); api=GET /api/search/hot; long-press=无 |

## 4. 结果列表

页面主体第 3 区,搜索结果流,与首页内容流同构,命中关键词高亮。

| 参数       | 值                                                                                      |
| ---------- | ----------------------------------------------------------------------------------------- |
| 组件类型 | `list` + `card`(现有 + P2,组合:结果流容器 + 内容结果卡)                             |
| 卡片背景   | `{color-surface-card}`                                                                    |
| 卡片圆角   | `{radius-rounded}`                                                                        |
| 卡片间距   | `{spacing-sm}`                                                                            |
| padding    | `{spacing-sm}`                                                                            |
| 标题字号   | `{font-size-body}` + `{font-weight-medium}`,颜色 `{color-text-primary}`                 |
| 命中摘要   | `{font-size-caption}`,颜色 `{color-text-secondary}`,命中词高亮 `{color-brand-primary}`  |
| intent     | 结果卡与首页内容流同构:命中词在标题/摘要中品牌色高亮,其余视觉归零                    |
| action     | tap=打开内容详情(action:open-post,详情页按需登记); state=按下底色变 `{color-state-hover}`; db=无; api=GET /api/search?q={input-value}; long-press=无 |

无结果时结果区展示空状态:`{icon-info}` + "没有找到相关内容" + 换个关键词的建议;热门搜索区不清空,方便改词重搜。

### 4.1 item 字段结构

每条结果是内容卡数据对象(字段与 ui/home.md §4.1 一致,新增命中摘要):

| 字段      | 类型   | 约束                  | 展示规则                   |
| --------- | ------ | --------------------- | -------------------------- |
| `id`      | string | 必填,唯一,kebab-case | 不展示,用作 key           |
| `cover`   | string | 必填,URL              | 卡片顶部封面图             |
| `title`   | string | 必填,≤20 字符         | 封面下方标题,命中词高亮   |
| `author`  | string | 选填                  | 标题下方作者名             |
| `snippet` | string | 选填,≤40 字符         | 命中摘要,命中词高亮       |
| `target`  | string | 必填,`action:` 动作标识 | tap 动作目标(详情页按需登记) |

### 4.2 默认结果内容(样例关键词"渐变")

| 顺序 | id            | cover       | title              | author | snippet                | target     |
| ---- | ------------- | ----------- | ------------------ | ------ | ---------------------- | ---------- |
| 1    | post-aurora   | /img/a1.jpg | 极光渐变的三种用法 | 山雾   | 渐变端点要落在色相环…  | action:open-post |
| 2    | post-gradient | /img/a5.jpg | 双色渐变避坑指南   | 林一   | 渐变中间调易发灰       | action:open-post |
| 3    | post-mesh     | /img/a6.jpg | 网格渐变入门       | 白鹿   | 网格渐变的锚点布局     | action:open-post |

## 5. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-brand-primary}` → 暗色保持色相,略降饱和度(命中词高亮)
- `{color-state-hover}` → 暗色变体(深底上的按压叠色)

## 6. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"首页"——本页自首页搜索栏 submit 进入,归属首页动线,选中态维持首页;tap"首页"返回 ui/home.md
