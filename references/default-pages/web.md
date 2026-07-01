# Web 默认页面清单

> 本文件列出 Web 端(后台/官网)项目的 15 个默认页面,供 `draw-md` 子命令在新项目触发"页面清单确认"步骤时引用。完整选用规则见 [index.md](./index.md)。

---

## 列结构说明

主表格统一采用 5 列结构:

| 列名 | 含义 |
| ---- | ---- |
| 页面 slug | kebab-case 页面标识,与 `examples/ui-markdown/ui/<slug>.md` 产物文件名对齐(如 `home` → `ui/home.md`,`forgot-password` → `ui/forgot-password.md`) |
| 描述 | 一句话页面用途(≤20 字) |
| 必备元素 | 该页 MUST 含的核心区块/组件,用 `/` 分隔 |
| 优先级 | P0(必备)/ P1(按业务选)/ P2(可选) |
| 示例链接 | 指向本文档内锚点(后续可扩展为 `examples/ui-markdown/ui/_defaults/` 模板链接) |

---

## 默认页面清单(15 个)

| 页面 slug | 描述 | 必备元素 | 优先级 | 示例链接 |
| --------- | ---- | -------- | ------ | -------- |
| home | 首页 | 顶部导航/Hero/功能区/页脚 | P0 | [web.md#home](#home) |
| about | 关于 | 公司介绍/团队/历史 | P1 | [web.md#about](#about) |
| contact | 联系我们 | 联系表单/地址/电话/地图 | P1 | [web.md#contact](#contact) |
| login | 登录 | 账号/密码/登录按钮/记住我 | P0 | [web.md#login](#login) |
| signup | 注册 | 邮箱/密码/确认密码/协议 | P1 | [web.md#signup](#signup) |
| forgot-password | 找回密码 | 邮箱/验证码/新密码 | P1 | [web.md#forgot-password](#forgot-password) |
| verify-email | 邮箱验证 | 验证码输入/重发倒计时 | P1 | [web.md#verify-email](#verify-email) |
| dashboard | 仪表盘 | 侧边栏/数据卡片/图表/顶栏 | P0 | [web.md#dashboard](#dashboard) |
| settings | 设置 | 分组表单/保存按钮 | P0 | [web.md#settings](#settings) |
| profile | 个人资料 | 头像/信息表单/保存 | P1 | [web.md#profile](#profile) |
| not-found | 404 页 | 错误码/文案/返回首页 | P2 | [web.md#not-found](#not-found) |
| server-error | 500 页 | 错误码/文案/联系支持 | P2 | [web.md#server-error](#server-error) |
| forbidden | 403 页 | 错误码/文案/登录入口 | P2 | [web.md#forbidden](#forbidden) |
| privacy | 隐私政策 | 标题/正文/更新日期 | P2 | [web.md#privacy](#privacy) |
| terms | 服务条款 | 标题/正文/更新日期 | P2 | [web.md#terms](#terms) |

---

## home

Web 站点首页,承载品牌传达、核心功能入口与转化引导。

## about

介绍公司背景、团队与演进历程,建立访问者信任。

## contact

提供联系表单、地址电话与地图,便于用户触达与商务沟通。

## login

验证用户身份进入受控区域,支持记住登录态与会话保持。

## signup

引导新用户注册,采集邮箱/密码并完成协议确认。

## forgot-password

通过邮箱验证码重置账户密码。

## verify-email

注册后或敏感操作触发的邮箱所有权验证,支持重发倒计时。

## dashboard

后台系统主工作台,聚合关键数据指标、图表与快捷操作。

## settings

集中管理账户与系统偏好,支持分组表单与统一保存。

## profile

编辑当前用户个人资料,含头像与基础信息维护。

## not-found

路径不存在时的友好提示,提供返回首页入口。

## server-error

服务异常时的提示页,引导用户联系支持或稍后重试。

## forbidden

无权限访问时的提示页,提供登录入口或申请权限引导。

## privacy

按合规要求声明用户数据收集与处理规则。

## terms

按合规要求声明服务条款与用户义务。

---

## 参考链接

- [draw-md 子命令](../commands/draw-md.md)
- [默认页面清单总索引](./index.md)
