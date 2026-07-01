---
name: about
description: 关于页(二级)—— 应用信息 + 功能列表
background: "{surface-base}"
updated: 2026-06-30
version: 1.1.0
---

# 关于(about)

二级页面,位于 `setting/` 子目录(嵌套示例)。二级页面**不含 dock**(仅一级页面有 dock)。

## 1. 顶部导航

<!-- 布局组织见 ../../references/dimensions/layout.md -->

引用 [`../../organisms/nav-bar.md`](../../organisms/nav-bar.md):左侧返回 / 中间标题"关于" / 右侧无。
- nav-bar action:左=tap→history.back(返回 setting/index); 中=无; 右=无

## 2. 应用信息

页面主体第 1 区。

| 参数       | 值                       |
| ---------- | ------------------------ |
| logo 尺寸  | 72px                     |
| 应用名字号 | `{font-size-h3}`         |
| 字重       | `{font-weight-semibold}` |
| 字体颜色   | `{text-primary}`         |
| 版本字号   | `{font-size-caption}`    |
| 版本颜色   | `{text-secondary}`       |
| action     | tap=无(纯展示); state=无; db=无; api=GET /api/app/info; long-press=无 |

应用信息区展示内容:
- logo 图标(72px,居中)
- 应用名:"maliang"(或动态读取)
- 版本号:"v1.0.0(构建号 100)"(由 API 返回)

## 3. 功能列表

页面主体第 2 区,设置项行列表。

| 参数     | 值                                |
| -------- | --------------------------------- |
| 行高     | 48px                              |
| padding  | 0 `{spacing-lg}`                  |
| 字体大小 | `{font-size-body}`                |
| 字体颜色 | `{text-primary}`                  |
| 分割线   | `{border-hairline}` + `{divider}` |
| action   | tap=→对应目标页; state=按下高亮; db=无; api=无; long-press=无 |

### 3.1 item 字段结构

每个功能列表项是一个数据对象:

| 字段          | 类型    | 约束                          | 展示规则                |
| ------------- | ------- | ----------------------------- | ----------------------- |
| `id`          | string  | 必填,唯一,kebab-case          | 不展示,用作 key         |
| `label`       | string  | 必填,≤10 中文字符             | 行左侧文字              |
| `icon-left`   | token   | 选填,引用 `{icon-*}`          | 行最左侧图标(可选)      |
| `value-right` | string  | 选填                          | 行右侧文字(如版本号)    |
| `arrow`       | boolean | 选填,默认 true                | 行右侧是否显示箭头      |
| `target`      | string  | 必填,目标页或动作标识         | tap 跳转目标            |
| `external`    | boolean | 选填,默认 false               | 是否外部链接(浏览器打开)|

### 3.2 默认功能列表内容

| 顺序 | id              | label        | icon-left         | value-right | target                              | external |
| ---- | --------------- | ------------ | ----------------- | ----------- | ----------------------------------- | -------- |
| 1    | version-check   | 版本更新     | icon-version      | v1.0.0      | action:check-update                 | false    |
| 2    | user-agreement  | 用户协议     | icon-doc          |             | ui/setting/agreement.md             | false    |
| 3    | privacy-policy  | 隐私政策     | icon-shield       |             | ui/setting/privacy.md               | false    |
| 4    | about-us        | 关于我们     | icon-info         |             | ui/setting/about-us.md              | false    |
| 5    | feedback        | 意见反馈     | icon-feedback     |             | action:open-feedback                | false    |
| 6    | share-app       | 分享应用     | icon-share        |             | action:share-sheet                  | false    |
| 7    | official-site   | 官方网站     | icon-link         |             | https://maliang.example.com         | true     |

### 3.3 各项详细说明

1. **版本更新**:展示当前版本号(value-right),tap 触发 `action:check-update` → 调用 `GET /api/app/version-check` → 若有新版本弹窗提示更新
2. **用户协议**:tap 跳转到 `ui/setting/agreement.md` 二级页面,展示完整用户协议文本
3. **隐私政策**:tap 跳转到 `ui/setting/privacy.md` 二级页面,展示隐私政策文本
4. **关于我们**:tap 跳转到 `ui/setting/about-us.md` 二级页面,展示团队/公司介绍
5. **意见反馈**:tap 触发 `action:open-feedback` → 打开反馈弹窗,提交 `POST /api/feedback {content, contact}`
6. **分享应用**:tap 触发 `action:share-sheet` → 调用系统分享面板,分享内容含应用下载链接
7. **官方网站**:tap 触发 `action:open-external` → 在系统浏览器打开 `https://maliang.example.com`(external=true)
