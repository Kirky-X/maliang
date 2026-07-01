---
name: token
description: 产物层全局硬 token 表 —— 颜色/字体/图标/间距/圆角/分割线的具体值,所有 UI 页面 markdown 引用此处
updated: 2026-06-30
version: 1.1.0
---

# token.md —— 全局硬 token 表(产物层)

> 所有页面 markdown 的 frontmatter 与组件参数表 **MUST 引用本文件的 token**,禁止硬编码色值字面量。
> token 命名遵循规范层 [`token.md`](../../../references/meta/token.md) 的规则(kebab-case、层级、语义)。
> **格式约定**:颜色 token 给 HEX + RGBA 双格式;尺寸类 token(字号/图标/间距/圆角/分割线粗细)给具体像素值(无 RGBA 语义)。
> 默认浅色模式;暗色模式见文末。

## 1. 颜色(colors)

> HEX 列含色块预览(`<span style="background:...">`),支持 markdown 内联 HTML 渲染器(GitHub / VSCode 预览)。

| token                | HEX                                                                    | RGBA                | 用途                 |
| --------------------- | ---------------------------------------------------------------------- | ------------------- | -------------------- |
| color-brand-primary   | #5B7CFA <span style="background:#5B7CFA;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(91,124,250,1)  | 品牌主色 / 主 CTA    |
| color-brand-secondary | #8B5CF6 <span style="background:#8B5CF6;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(139,92,246,1)  | 品牌次色 / 辅助强调  |
| color-accent          | #FF6B6B <span style="background:#FF6B6B;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(255,107,107,1) | 强调色(每屏至多一处) |
| color-surface-base    | #F7F8FA <span style="background:#F7F8FA;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(247,248,250,1) | 页面背景             |
| color-surface-card    | #FFFFFF <span style="background:#FFFFFF;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(255,255,255,1) | 卡片背景             |
| color-surface-elevated| #FFFFFF <span style="background:#FFFFFF;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(255,255,255,1) | 悬浮卡片 / 弹层背景  |
| color-text-primary    | #1A1D21 <span style="background:#1A1D21;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(26,29,33,1)    | 主要文字(标题/正文)  |
| color-text-secondary  | #6B7280 <span style="background:#6B7280;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(107,114,128,1) | 次要文字(说明/时间)  |
| color-text-placeholder| #9CA3AF <span style="background:#9CA3AF;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(156,163,175,1) | 占位符 / 辅助提示    |
| color-text-disabled   | #C0C4CC <span style="background:#C0C4CC;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(192,196,204,1) | 禁用文字             |
| color-text-on-brand   | #FFFFFF <span style="background:#FFFFFF;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(255,255,255,1) | 品牌色背景上的文字   |
| color-border-base     | #E5E7EB <span style="background:#E5E7EB;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(229,231,235,1) | 标准边框             |
| color-divider         | #F0F1F3 <span style="background:#F0F1F3;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(240,241,243,1) | 分割线               |
| color-danger          | #EF4444 <span style="background:#EF4444;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(239,68,68,1)   | 危险 / 错误 / 删除   |
| color-success         | #10B981 <span style="background:#10B981;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(16,185,129,1)  | 成功 / 已完成        |
| color-warning         | #F59E0B <span style="background:#F59E0B;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(245,158,11,1)  | 警告 / 提示          |
| color-link            | #3B82F6 <span style="background:#3B82F6;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>     | rgba(59,130,246,1)  | 链接文字             |
| color-overlay         | #00000080 <span style="background:#00000080;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span> | rgba(0,0,0,0.5)     | 遮罩层(弹窗背景)     |

## 2. 字体(typography)

字族:`"PingFang SC", "SF Pro Text", -apple-system, BlinkMacSystemFont, sans-serif`(中英文统一)。

| token                | 值   | 用途              |
| -------------------- | ---- | ----------------- |
| font-size-h1         | 24px | 页面主标题        |
| font-size-h2         | 18px | 区块标题          |
| font-size-h3         | 16px | 小标题 / 卡片标题 |
| font-size-body       | 14px | 正文(移动端基准)  |
| font-size-caption    | 12px | 辅助文字 / 标签   |
| font-size-mini       | 10px | 角标 / 极辅助     |
| font-weight-regular  | 400  | 正文默认          |
| font-weight-medium   | 500  | 小标题 / 强调正文 |
| font-weight-semibold | 600  | 卡片标题 / 按钮   |
| font-weight-bold     | 700  | 页面主标题        |
| line-height-tight    | 1.2  | 标题              |
| line-height-base     | 1.5  | 正文              |
| line-height-relaxed  | 1.6  | 长文本阅读        |

## 3. 图标(icon)

| token             | 值    | 用途                 |
| ----------------- | ----- | -------------------- |
| icon-size-sm      | 16px  | 辅助 / 提示图标      |
| icon-size-md      | 20px  | 列表 / 行内图标      |
| icon-size-lg      | 24px  | 导航 / 标签栏图标    |
| icon-size-xl      | 32px  | 空状态 / 大图标      |
| icon-stroke       | 1.5px | 线性图标描边粗细     |
| icon-touch-target | 44px  | 可点击热区(费茨定律) |

### 3.1 图标内容 token

> 命名约定:`{icon-<name>-<style>}`,其中 `<name>` 是图标语义名(kebab-case),`<style>` 是 `filled`(填充)或 `stroke`(线性)。本表只列默认 App 端 dock + 首页用到的图标,业务图标按需扩展并补充到此表。

| token                       | 用途                             | 风格   |
| -------------------------- | -------------------------------- | ------ |
| icon-search-filled         | 搜索图标(填充,搜索栏右侧)     | filled |
| icon-search-stroke         | 搜索图标(线性)                 | stroke |
| icon-home-filled           | 首页 tab(填充,选中态)         | filled |
| icon-home-stroke           | 首页 tab(线性,未选中态)       | stroke |
| icon-discover-filled       | 发现 tab(填充,选中态)         | filled |
| icon-discover-stroke       | 发现 tab(线性,未选中态)       | stroke |
| icon-messages-filled       | 消息 tab(填充,选中态)         | filled |
| icon-messages-stroke       | 消息 tab(线性,未选中态)       | stroke |
| icon-mine-filled           | 我的 tab(填充,选中态)         | filled |
| icon-mine-stroke           | 我的 tab(线性,未选中态)       | stroke |
| icon-back                  | 返回箭头(线性,导航栏左上)     | stroke |
| icon-feed                  | 内容流图标(首页内容流)         | stroke |
| icon-rank                  | 排行榜图标(金刚区入口)         | stroke |
| icon-category              | 分类图标(金刚区入口)           | stroke |

**约束**:页面 markdown 引用图标 token 时 MUST 使用本表的命名,不得自创。新增图标 token 需在「新增组件流程」对应的 token 维护流程中补充到此表。

## 4. 间距(spacing)

以 2px 为基准,所有值为 2 的倍数。

| token       | 值   | 用途                    |
| ----------- | ---- | ----------------------- |
| spacing-xs  | 4px  | 图标内 / 紧凑组内       |
| spacing-sm  | 8px  | 相关元素组内            |
| spacing-md  | 14px | 模块内边距 / 卡片内边距 |
| spacing-lg  | 20px | 页面边距(安全区)        |
| spacing-xl  | 24px | 模块间距                |
| spacing-2xl | 32px | 宽松区块间距            |
| spacing-3xl | 48px | 大分区 / 章节间距       |

## 5. 圆角(radius)

| token          | 值     | 用途                       |
| -------------- | ------ | -------------------------- |
| radius-sharp   | 0px    | 直角(图片 / 严谨数据表)    |
| radius-subtle  | 4px    | 小控件(标签 / chip / 输入) |
| radius-rounded | 8px    | 卡片 / 容器(主流)          |
| radius-lg      | 12px   | 大卡片                     |
| radius-xl      | 16px   | 弹窗 / 模态                |
| radius-full    | 9999px | 胶囊(按钮 / 头像 / 开关)   |

## 6. 分割线 / 边框(border)

| token           | 值    | 用途                  |
| --------------- | ----- | --------------------- |
| border-hairline | 0.5px | 极细分隔(iOS 风格)    |
| border-thin     | 1px   | 标准分割线 / 卡片边框 |
| border-medium   | 2px   | 强调 / 选中态边框     |
| border-thick    | 4px   | 容器边界 / 分隔栏     |

分割线颜色用 `{color-divider}`;标准边框用 `{color-border-base}`(见颜色表)。**慎用分割线**,分组优先用间距 > 底色 > 分割线。

---

## 暗色模式(参考)

暗色模式独立调色(非简单反色),关键 token 对应值:

| token              | HEX(暗)                                                                   | RGBA(暗)               |
| ------------------ | ------------------------------------------------------------------------- | ---------------------- |
| color-surface-base | #141413 <span style="background:#141413;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>   | rgba(20,20,19,1)       |
| color-surface-card | #1F1F1E <span style="background:#1F1F1E;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>   | rgba(31,31,30,1)       |
| color-text-primary | #F5F4ED <span style="background:#F5F4ED;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>   | rgba(245,244,237,1)    |
| color-text-secondary | #A8A29E <span style="background:#A8A29E;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span>   | rgba(168,162,158,1)    |
| color-border-base  | #FFFFFF14 <span style="background:#FFFFFF14;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span> | rgba(255,255,255,0.08) |
| color-divider      | #FFFFFF0F <span style="background:#FFFFFF0F;display:inline-block;width:1.5em;height:1em;vertical-align:middle;border:1px solid #ccc">　</span> | rgba(255,255,255,0.06) |

品牌色 / 功能色(color-brand-primary、color-danger、color-success、color-warning、color-link)暗色模式下保持色相、略降饱和度以适配深底。字号 / 间距 / 圆角 / 分割线粗细暗色模式不变。
