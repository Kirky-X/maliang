---
name: discover
description: 发现(一级)—— 精选横幅 + 话题卡片流
background: "{color-surface-base}"
components: [navigation, image, text, grid, card]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 发现(discover)

**thesis**: 逛的起点——横幅承载编辑推荐,话题流负责无限下翻的闲逛欲
**own-world**: 通栏渐变横幅打头,双列白卡话题流承接,底色与首页同源,品牌色只落在参与数
**first-viewport**: 精选横幅完整可见 + 首屏至少 2 张话题卡
**signature-interaction**: 横幅自动轮播 5 秒一张,用户滑动即抢断停播;话题卡 tap 带语境进聚合页

一级页面,即 dock"发现"tab 落地页(organisms/dock.md §3.1 target=ui/discover.md)。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"发现" / 右侧搜索。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=tap→ui/search.md(搜索,`{icon-search-stroke}`); state=按下高亮

## 2. 精选横幅

页面主体第 1 区,通栏运营横幅,轮播展示编辑精选专题。

| 参数       | 值                                                                              |
| ---------- | -------------------------------------------------------------------------------- |
| 组件类型 | `image` + `text`(P0 + 现有,组合:横幅图 + 左下角标题文字)                    |
| 宽度       | match-parent − 2×`{spacing-lg}`                                                  |
| 高度       | 160px                                                                            |
| 圆角       | `{radius-lg}`                                                                    |
| 标题字号   | `{font-size-h3}` + `{font-weight-semibold}`,颜色 `{color-text-on-brand}`       |
| 页码指示   | 当前页圆点 `{color-text-on-brand}`,其余圆点 `{color-text-placeholder}`         |
| 轮播动效   | `{motion-duration-normal}` + `{motion-ease-out}`                                 |
| padding    | `{spacing-md}`                                                                   |
| intent     | 横幅是本页唯一运营位:一条专题一句话,深色渐变压底保证白字可读                |
| action     | tap=打开精选专题聚合页(action:open-topic,按需登记); state=自动轮播 5 秒一张,用户滑动后停止自动播; db=无; api=GET /api/discover/banner; long-press=无 |

### 2.1 item 字段结构

每张横幅是一个数据对象:

| 字段     | 类型   | 约束                  | 展示规则         |
| -------- | ------ | --------------------- | ---------------- |
| `id`     | string | 必填,唯一,kebab-case | 不展示,用作 key |
| `cover`  | string | 必填,URL              | 横幅背景图       |
| `title`  | string | 必填,≤10 中文字符     | 左下角标题       |
| `target` | string | 必填,`action:` 动作标识 | tap 动作目标(聚合页按需登记) |

### 2.2 默认横幅内容

| 顺序 | id            | cover       | title        | target      |
| ---- | ------------- | ----------- | ------------ | ----------- |
| 1    | banner-editor | /img/d1.jpg | 本周编辑精选 | action:open-topic |
| 2    | banner-motion | /img/d2.jpg | 动效研习社   | action:open-topic |
| 3    | banner-color  | /img/d3.jpg | 配色灵感库   | action:open-topic |

## 3. 话题卡片流

页面主体第 2 区,双列话题卡片流,按参与热度排序,滚动到底自动加载。

| 参数         | 值                                                                                |
| ------------ | ---------------------------------------------------------------------------------- |
| 组件类型 | `grid` + `card`(P1 + P2,组合:双列网格容器 + 话题卡)                       |
| 列数         | 2                                                                                  |
| 卡片背景     | `{color-surface-card}`                                                             |
| 卡片圆角     | `{radius-rounded}`                                                                 |
| 卡片间距     | `{spacing-sm}`                                                                     |
| padding      | `{spacing-sm}`                                                                     |
| 封面高度     | 120px                                                                              |
| 标题字号     | `{font-size-body}` + `{font-weight-medium}`,颜色 `{color-text-primary}`          |
| 参与数字号   | `{font-size-caption}`,颜色 `{color-brand-primary}`                                |
| 阴影         | `{shadow-card}`                                                                    |
| aria-label   | 每张卡用对应话题名,容器 aria-label="话题卡片流"                                  |
| intent       | 话题卡只留封面 + 话题名 + 参与数:封面决定点击欲,数字制造"很多人在聊"的暗示     |
| action       | tap=打开话题聚合页(action:open-topic); state=按下底色变 `{color-state-hover}`; db=无; api=GET /api/discover/topics?cursor=?; long-press=无 |

### 3.1 item 字段结构

每张话题卡是一个数据对象:

| 字段      | 类型   | 约束                  | 展示规则           |
| --------- | ------ | --------------------- | ------------------ |
| `id`      | string | 必填,唯一,kebab-case | 不展示,用作 key   |
| `cover`   | string | 必填,URL              | 卡片顶部封面图     |
| `title`   | string | 必填,≤8 中文字符      | 封面下方话题名     |
| `members` | number | 必填,≥0               | 话题名下方参与数   |
| `target`  | string | 必填,`action:` 动作标识 | tap 动作目标(聚合页按需登记) |

### 3.2 默认话题内容

| 顺序 | id             | cover       | title    | members | target      |
| ---- | -------------- | ----------- | -------- | ------- | ----------- |
| 1    | topic-aurora   | /img/t1.jpg | 极光渐变 | 12800   | action:open-topic |
| 2    | topic-grid     | /img/t2.jpg | 8px 网格 | 8600    | action:open-topic |
| 3    | topic-texture  | /img/t3.jpg | 手绘质感 | 5300    | action:open-topic |
| 4    | topic-paper    | /img/t4.jpg | 纸艺立体 | 3200    | action:open-topic |

## 4. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-state-hover}` → 暗色变体(深底上的按压叠色)
- `{color-brand-primary}` → 暗色保持色相,略降饱和度(参与数)
- `{shadow-card}` → 暗色随卡片底加深弱化

## 5. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页 / **发现(选中)** / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"发现"——本页即"发现"tab 落地页(dock §3.1 target=ui/discover.md);再次 tap"发现"回到顶部并刷新横幅与话题流
