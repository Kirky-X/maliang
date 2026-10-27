---
name: category
description: 分类(一级)—— 左侧分类导航 + 右侧内容网格
background: "{color-surface-base}"
components: [navigation, list, grid, card]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 分类(category)

**thesis**: 左栏定类,右栏看图——选类与浏览两栏各司其职,一屏完成
**own-world**: 左栏 96px 列表贴灰底,右栏白卡两列网格,选中分类只用品牌色竖条标注
**first-viewport**: 左栏至少 6 个分类可读,右栏首屏至少 4 张内容卡
**signature-interaction**: 点左栏分类,右栏网格整组淡入刷新({motion-duration-fast},可跳过)

一级页面,自首页金刚区"分类"进入(ui/home.md §3.2)。

## 1. 顶部导航

引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)(组件类型:`navigation`):左侧无(一级页隐藏返回) / 中间标题"分类" / 右侧无。
- nav-bar action:左=无(一级页面无返回); 中=无; 右=无(本页无顶部操作)

## 2. 分类导航(左侧)

页面主体左栏,一/二级分类列表。

| 参数       | 值                                                                                              |
| ---------- | ----------------------------------------------------------------------------------------------- |
| 组件类型 | `list`(现有组件,组合:左侧分类列)                                                      |
| 栏宽       | 96px(约 25% 屏宽)                                                                             |
| 行高       | 44px                                                                                            |
| 选中态     | 行首 2px `{color-brand-primary}` 竖条 + 文字 `{color-text-primary}` + `{font-weight-semibold}` + 底色 `{color-surface-card}` |
| 未选中态   | 文字 `{color-text-secondary}`,底色透明                                                          |
| 字体大小   | `{font-size-body}`                                                                              |
| aria-label | 容器 aria-label="分类导航",每行用分类名(如"插画")                                            |
| intent     | 左栏只承担"选类",不放图标不放徽标,把宽度让给右栏内容                                            |
| action     | tap=切换选中分类并刷新右侧网格; state=竖条 + 加粗 + 白底; db=UPDATE user_settings SET last_category=?; api=GET /api/categories; long-press=无 |

### 2.1 分类 item 字段结构

每个分类项是一个数据对象:

| 字段          | 类型    | 约束                            | 展示规则             |
| ------------- | ------- | ------------------------------- | -------------------- |
| `id`          | string  | 必填,唯一,kebab-case           | 不展示,用作 key     |
| `label`       | string  | 必填,≤4 中文字符               | 行内分类名           |
| `sort-order`  | number  | 必填,≥1                        | 左栏排列顺序         |
| `item-count`  | number  | 选填,≥0                        | 行尾作品数(可选)    |
| `is-selected` | boolean | 选填,默认 false                | 当前选中分类         |

### 2.2 默认分类内容

| 顺序 | id            | label   | item-count |
| ---- | ------------- | ------- | ---------- |
| 1    | recommend     | 推荐    |            |
| 2    | illustration  | 插画    | 1284       |
| 3    | photography   | 摄影    | 962        |
| 4    | three-d       | 三维    | 517        |
| 5    | ui-design     | UI 设计 | 733        |
| 6    | typeface      | 字体    | 286        |

## 3. 内容网格(右侧)

页面主体右栏,当前分类的两列内容网格。

| 参数       | 值                                                                            |
| ---------- | ----------------------------------------------------------------------------- |
| 组件类型 | `grid` + `card`(P0 + P2,组合:两列内容网格 + 封面卡)                  |
| 列数       | 2                                                                             |
| 卡片背景   | `{color-surface-card}`                                                        |
| 卡片圆角   | `{radius-rounded}`                                                            |
| 卡片间距   | `{spacing-sm}`                                                                |
| padding    | `{spacing-sm}`                                                                |
| 标题字号   | `{font-size-caption}`,颜色 `{color-text-primary}`                           |
| intent     | 网格卡只保留封面 + 标题一行,细节留给详情页,保证首屏 4 卡                      |
| action     | tap=打开分类条目详情(action:open-category-item,按需登记); state=按下底色变 `{color-state-hover}`; db=无; api=GET /api/categories/{category-id}/items?cursor=?; long-press=无 |

### 3.1 网格卡 item 字段结构

每张网格卡是一个数据对象:

| 字段     | 类型   | 约束                  | 展示规则         |
| -------- | ------ | --------------------- | ---------------- |
| `id`     | string | 必填,唯一,kebab-case | 不展示,用作 key |
| `cover`  | string | 必填,URL             | 卡片封面图       |
| `title`  | string | 必填,≤12 字符        | 封面下方标题     |
| `target` | string | 必填,`action:` 动作标识 | tap 动作目标(详情页按需登记) |

## 4. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-surface-card}` → 暗色变体(深卡片,选中分类与网格卡)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-brand-primary}` → 暗色保持色相,略降饱和度(选中竖条)
- `{color-state-hover}` → 暗色变体(深底上的按压叠色)

## 5. 底部 dock

引用 [`../organisms/dock.md`](../organisms/dock.md)(组件类型:`navigation`):首页(选中) / 发现 / 消息 / 我的。
- dock action:tap=切换至 dock.md §3.1 target 声明的一级页面; state=切换选中态+全局 tab 索引; db=UPDATE user_settings SET last_tab=?; api=无; long-press=无
- 本页选中项说明:选中"首页"——本页自首页金刚区进入,归属首页动线,选中态维持首页;tap"首页"返回 ui/home.md
