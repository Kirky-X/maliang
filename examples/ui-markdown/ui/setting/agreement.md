---
name: agreement
description: 用户协议页(二级)—— 编号条款纯阅读,mode=read
background: "{color-surface-base}"
components: [navigation, text]
platform: mobile
dir: ltr
spec_version: 1
updated: 2026-10-27
version: 1.0.0
mode: read
---

# 用户协议(agreement)

**thesis**: 两屏滚动读完协议骨架——生效日期、六条主条款、争议出口,一个不少
**own-world**: 纯阅读版式——单列正文无任何可点元素,条款用"编号 + 主题句"分节,阅读节奏即全部体验
**first-viewport**: 导航标题"用户协议" + 生效日期引言段 + 第 1 条主题句首屏可见
**signature-interaction**: 本页零交互,以排版可读性为招牌——正文行高取 `{line-height-relaxed}`(1.6),容器宽度 match-parent 不定宽,条款间距 `{spacing-lg}`(24px),字号固定 `{font-size-body}` 不做缩放

二级页面,位于 `setting/` 子目录,frontmatter 声明 `mode: read`(纯展示页,全页无 tap 动作)。二级页面**不含 dock**(仅一级页面有 dock)。

## 1. 顶部导航

引用 [`../../organisms/nav-bar.md`](../../organisms/nav-bar.md)(组件类型:`navigation`):左侧返回 / 中间标题"用户协议" / 右侧无。
- nav-bar action:左=tap→history.back(返回上一页,通常为 setting/about); 中=无; 右=无

## 2. 协议正文

页面主体第 1 区,也是唯一内容区。分"引言 + 编号条款"两段排版,长文本容器宽度用 match-parent。

| 参数       | 值                              |
| ---------- | ------------------------------- |
| 组件类型 | `text`(现有组件,长文本阅读区) |
| 宽度       | match-parent                    |
| 字号       | `{font-size-body}`              |
| 字重       | `{font-weight-regular}`         |
| 行高       | `{line-height-relaxed}`         |
| 字体颜色   | `{color-text-primary}`          |
| 条款间距   | `{spacing-lg}`                  |
| padding    | `{spacing-lg}`                  |
| action     | tap=无(纯展示); state=无; db=无; api=无; long-press=无 |

### 2.1 引言

本协议是用户与 maliang 开发团队之间关于使用本应用的约定,自 2026-10-27 起生效。协议更新时在本页公告,并在设置页推送变更提示;继续使用即视为接受更新后的协议。

### 2.2 条款正文(示例条款)

1. **账号与使用**:用户注册与登录需提供有效邮箱,账号不得出借或转让;利用本应用从事违法活动的,团队有权中止服务。
2. **内容归属**:用户在本应用创作的草稿与配置归用户所有;应用本身的代码、界面设计与文档归团队所有,未经授权不得复制或分发。
3. **隐私与数据**:个人信息的收集与处理遵循《隐私政策》(ui/setting/privacy.md);用户注销账号时,云端数据在 15 个工作日内删除。
4. **服务变更与中止**:团队可迭代功能或调整服务范围,重大变更提前 7 天在应用内公告;不可抗力导致的服务中断不视为违约。
5. **免责声明**:因用户设备故障、网络中断或第三方服务变更导致的损失,团队在法律允许范围内不承担责任。
6. **争议解决**:因本协议产生的争议应先友好协商;协商不成的,提交团队所在地有管辖权的人民法院诉讼解决。

## 3. 暗色模式

本页暗色模式覆盖以下 token(暗色取值见 token.md 暗色章节):

- `{color-surface-base}` → 暗色变体(深底)
- `{color-text-primary}` → 暗色变体(浅文字)

行高 / 字号 / 间距为尺寸类 token,暗色模式不变。
