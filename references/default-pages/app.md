# App 默认页面清单

> 本文件列出 App(移动端)项目的 15 个默认页面,供 `draw-md` 子命令在新项目触发"页面清单确认"步骤时引用。完整选用规则见 [index.md](./index.md)。

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
| home | 首页 | 顶部导航/金刚区/内容流/底部 dock | P0 | [app.md#home](#home) |
| discover | 发现页 | 搜索栏/分类 tab/内容流 | P1 | [app.md#discover](#discover) |
| messages | 消息中心 | 消息列表/未读标记/系统通知分组 | P1 | [app.md#messages](#messages) |
| mine | 我的 | 头像/昵称/设置入口/功能列表 | P0 | [app.md#mine](#mine) |
| login | 登录 | 账号输入/密码输入/登录按钮/第三方登录 | P0 | [app.md#login](#login) |
| signup | 注册 | 手机或邮箱/验证码/密码/协议勾选 | P1 | [app.md#signup](#signup) |
| forgot-password | 找回密码 | 账号输入/验证码/新密码 | P1 | [app.md#forgot-password](#forgot-password) |
| settings | 设置 | 分组列表/开关/退出登录 | P0 | [app.md#settings](#settings) |
| about | 关于 | 版本号/公司信息/协议链接 | P1 | [app.md#about](#about) |
| privacy | 隐私政策 | 标题/正文/更新日期 | P2 | [app.md#privacy](#privacy) |
| terms | 用户协议 | 标题/正文/更新日期 | P2 | [app.md#terms](#terms) |
| feedback | 意见反馈 | 反馈类型/内容输入/联系方式/提交 | P1 | [app.md#feedback](#feedback) |
| empty-state | 空状态 | 插图/文案/操作按钮 | P2 | [app.md#empty-state](#empty-state) |
| network-error | 网络错误 | 错误插图/重试按钮 | P2 | [app.md#network-error](#network-error) |
| not-found | 404 页 | 错误码/文案/返回首页 | P2 | [app.md#not-found](#not-found) |

---

## home

App 启动后的主入口页,聚合核心功能入口与内容流,承担分发热度。

## discover

服务于内容探索与分类检索,常见于电商、社区、资讯类 App。

## messages

统一收口系统通知、互动消息与客服会话,支持未读聚合与分组浏览。

## mine

用户个人中心,展示身份信息并聚合账户、设置与功能入口。

## login

验证已注册用户身份,支持账号密码与第三方授权登录。

## signup

引导新用户完成账号创建与协议确认,采集最小必要信息。

## forgot-password

通过验证码或邮箱链接重置登录密码。

## settings

集中管理应用偏好(通知、主题、缓存等)与账户操作(含退出登录)。

## about

展示应用版本、公司主体与法律协议入口。

## privacy

按合规要求声明用户数据收集与处理规则。

## terms

按合规要求声明服务使用条款与用户义务。

## feedback

收集用户问题反馈,支持类型选择与联系方式留存。

## empty-state

在列表为空或无搜索结果时提供插图与操作引导,缓解用户焦虑。

## network-error

在请求失败或弱网场景提供错误提示与重试入口。

## not-found

在路径或资源不存在时提供错误码与返回首页入口。

---

## 参考链接

- [draw-md 子命令](../commands/draw-md.md)
- [默认页面清单总索引](./index.md)
