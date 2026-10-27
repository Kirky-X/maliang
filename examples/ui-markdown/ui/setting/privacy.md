---
name: privacy
description: 隐私政策页(二级)—— 数据处理规则纯阅读,mode=read
background: "{color-surface-base}"
components: [navigation, text]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
mode: read
---

# 隐私政策(privacy)

**thesis**: 五分钟读完全部数据处理规则——收什么、怎么用、跟谁共享、用户能删什么
**own-world**: 纯阅读版式——引言与生效日期用次要色弱化,条款正文用主色,零交互元素,阅读节奏放宽一档
**first-viewport**: 导航标题"隐私政策" + 生效日期引言 + 第 1 条(信息收集)主题句首屏可见
**signature-interaction**: 本页零交互,以排版可读性为招牌——条款分节间距取 `{spacing-xl}`(32px)放宽节奏,正文行高 `{line-height-relaxed}`(1.6),容器宽度 match-parent 不定宽,辅助说明降为 `{color-text-secondary}` 分层

二级页面,位于 `setting/` 子目录,frontmatter 声明 `mode: read`(纯展示页,全页无 tap 动作)。二级页面**不含 dock**(仅一级页面有 dock)。

## 1. 顶部导航

引用 [`../../organisms/nav-bar.md`](../../organisms/nav-bar.md)(组件类型:`navigation`):左侧返回 / 中间标题"隐私政策" / 右侧无。
- nav-bar action:左=tap→history.back(返回上一页,通常为 setting/about); 中=无; 右=无

## 2. 政策正文

页面主体第 1 区,也是唯一内容区。分"引言 + 编号条款"两段排版,长文本容器宽度用 match-parent。

| 参数       | 值                              |
| ---------- | ------------------------------- |
| 组件类型 | `text`(现有组件,长文本阅读区) |
| 宽度       | match-parent                    |
| 字号       | `{font-size-body}`              |
| 字重       | `{font-weight-regular}`         |
| 行高       | `{line-height-relaxed}`         |
| 字体颜色   | `{color-text-primary}`          |
| 辅助说明颜色 | `{color-text-secondary}`(引言与生效日期) |
| 条款间距   | `{spacing-xl}`                  |
| padding    | `{spacing-lg}`                  |
| action     | tap=无(纯展示); state=无; db=无; api=无; long-press=无 |

### 2.1 引言

本政策说明 maliang 开发团队如何收集、使用、存储与保护用户个人信息,自 2026-10-27 起生效。政策变更时在本页公告重大事项,涉及扩大收集范围须重新取得用户同意。

### 2.2 条款正文(示例条款)

1. **信息收集**:仅在注册、配置同步与改进体验所必需时收集邮箱、设备型号与系统版本,不收集通讯录、定位、剪贴板等与功能无关的信息。
2. **信息使用**:收集的信息仅用于账号识别、配置同步与崩溃分析,不用于广告画像,不进行自动化决策。
3. **本地存储与缓存**:创作内容与设计配置优先保存在设备本地;清除缓存或卸载应用即删除全部本地数据。
4. **第三方共享**:除云托管与崩溃上报两类必需服务商外,不向任何第三方共享个人信息;服务商清单与数据范围在本节公示。
5. **用户权利**:用户可随时在设置内查询、导出、更正或删除个人信息,或注销账号;相关请求在 15 个工作日内响应。
6. **未成年人保护**:若发现未满 14 周岁儿童在监护人未同意的情况下提供个人信息,团队将主动删除并通知监护人。

## 3. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-text-primary}` → 暗色变体(浅文字)
- `{color-text-secondary}` → 暗色变体(浅次要文字)

行高 / 字号 / 间距为尺寸类 token,暗色模式不变。
