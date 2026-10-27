---
name: about-us
description: 关于我们页(二级)—— 团队介绍 + 联系方式
background: "{color-surface-base}"
components: [navigation, image, text, list, button, icon]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
---

# 关于我们(about-us)

**thesis**: 一屏讲清团队是谁、在做什么、怎么联系上——三个信息组封顶
**own-world**: 图文名片页——通栏封面图压顶,一段介绍文字,末尾三行联系方式;列表只此一组,不再分组
**first-viewport**: 封面图 + 介绍段落 + 联系方式首行(邮箱)首屏可见
**signature-interaction**: 邮箱行 tap 唤起系统邮件客户端(mailto),官网行 external=true 走系统浏览器新开——本页仅有的两个出站动作,其余行纯展示

二级页面,位于 `setting/` 子目录(嵌套示例)。二级页面**不含 dock**(仅一级页面有 dock)。

## 1. 顶部导航

引用 [`../../organisms/nav-bar.md`](../../organisms/nav-bar.md)(组件类型:`navigation`):左侧返回 / 中间标题"关于我们" / 右侧无。
- nav-bar action:左=tap→history.back(返回上一页,通常为 setting/about); 中=无; 右=无

## 2. 团队介绍

页面主体第 1 区,通栏封面图 + 介绍段落,组合展示。

| 参数       | 值                                                          |
| ---------- | ----------------------------------------------------------- |
| 组件类型 | `image` + `text`(P0 + 现有组件,组合:团队封面图 + 介绍段落文本) |
| 图片资源   | /img/about-team.jpg                                         |
| 宽度       | match-parent                                                |
| 高度       | 160px                                                       |
| 圆角       | `{radius-lg}`                                               |
| 字号       | `{font-size-body}`                                          |
| 字重       | `{font-weight-regular}`                                     |
| 行高       | `{line-height-relaxed}`                                     |
| 字体颜色   | `{color-text-primary}`                                      |
| padding    | `{spacing-lg}`                                              |
| action     | tap=无(纯展示); state=无; db=无; api=无; long-press=无 |

介绍段落文案:

maliang 是一个把设计规范变成可用界面的前端设计工具,由 4 人小团队利用业余时间开发。我们相信好的设计系统应该可读、可校验、可交付——本应用内每个页面样张都附带可机械校验的设计契约,这也是团队名字的由来:良工不示人以朴。

## 3. 联系方式

页面主体第 2 区,可点击行列表,行内含左侧图标与右侧文案。

| 参数       | 值                                                          |
| ---------- | ----------------------------------------------------------- |
| 组件类型 | `list` + `button` + `icon`(现有 + 现有 + P1,组合:行列表容器 + 可点击行 + 左侧图标) |
| 行高       | 48px(满足 44px 触控下限)                                   |
| padding    | 0 `{spacing-lg}`                                            |
| 字体大小   | `{font-size-body}`                                          |
| 字体颜色   | `{color-text-primary}`                                      |
| 次要文字颜色 | `{color-text-secondary}`(行右侧 value 文案)               |
| 分割线     | `{border-hairline}` + `{color-divider}`                     |
| aria-label | 每行用对应 label 字段值(如"发送邮件"/"打开官网"),容器 aria-label="联系方式列表" |
| action     | tap=打开对应渠道(见 §3.2); state=按下高亮; db=无; api=无; long-press=无 |

### 3.1 item 字段结构

每个联系方式项是一个数据对象:

| 字段        | 类型    | 约束                       | 展示规则                    |
| ----------- | ------- | -------------------------- | --------------------------- |
| `id`        | string  | 必填,唯一,kebab-case      | 不展示,用作 key            |
| `label`     | string  | 必填,≤10 中文字符          | 行左侧文字                  |
| `icon-left` | token   | 必填,引用 `{icon-*}`       | 行左侧图标                  |
| `value`     | string  | 选填                        | 行右侧文案(邮箱地址/域名) |
| `channel`   | string  | 必填,mailto 或 browser     | tap 打开方式                |
| `contact`   | string  | 必填                        | 邮箱地址或网址(非页面跳转,不进导航图) |
| `external`  | boolean | 选填,默认 false            | 是否离开应用(浏览器打开)  |

### 3.2 默认联系方式内容

| 顺序 | id              | label | icon-left        | value                        | channel | contact                                 | external |
| ---- | --------------- | ----- | ---------------- | ---------------------------- | ------- | --------------------------------------- | -------- |
| 1    | contact-email   | 邮箱  | {icon-feedback}  | support@maliang.example.com  | mailto  | support@maliang.example.com             | false    |
| 2    | contact-site    | 官网  | {icon-link}      | maliang.example.com          | browser | https://maliang.example.com             | true     |
| 3    | contact-service | 客服  | {icon-service}   | 工作日 10:00-18:00           | browser | https://maliang.example.com/support     | true     |

### 3.3 各行详细说明

1. **邮箱**:tap 以 mailto 方式唤起系统邮件客户端,收件人预填 `support@maliang.example.com`,不离开应用发起网络请求
2. **官网**:tap 触发 `action:open-external` → 在系统浏览器打开 `https://maliang.example.com`(external=true)
3. **客服**:tap 触发 `action:open-external` → 在系统浏览器打开支持页 `https://maliang.example.com/support`(external=true)

## 4. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)
- `{color-divider}` → 暗色变体(低对比分割线)
