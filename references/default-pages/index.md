# 默认页面清单总索引

> 本文件是 `references/default-pages/` 的入口,为 `draw-md` 子命令提供 App/Web 两端的默认页面清单与选用规则。

---

## 总索引

### App 端(15 页,详见 [app.md](./app.md))

| 页面 slug | 描述 | 优先级 |
| --------- | ---- | ------ |
| home | 首页 | P0 |
| discover | 发现页 | P1 |
| messages | 消息中心 | P1 |
| mine | 我的 | P0 |
| login | 登录 | P0 |
| signup | 注册 | P1 |
| forgot-password | 找回密码 | P1 |
| settings | 设置 | P0 |
| about | 关于 | P1 |
| privacy | 隐私政策 | P2 |
| terms | 用户协议 | P2 |
| feedback | 意见反馈 | P1 |
| empty-state | 空状态 | P2 |
| network-error | 网络错误 | P2 |
| not-found | 404 页 | P2 |

### Web 端(15 页,详见 [web.md](./web.md))

| 页面 slug | 描述 | 优先级 |
| --------- | ---- | ------ |
| home | 首页 | P0 |
| about | 关于 | P1 |
| contact | 联系我们 | P1 |
| login | 登录 | P0 |
| signup | 注册 | P1 |
| forgot-password | 找回密码 | P1 |
| verify-email | 邮箱验证 | P1 |
| dashboard | 仪表盘 | P0 |
| settings | 设置 | P0 |
| profile | 个人资料 | P1 |
| not-found | 404 页 | P2 |
| server-error | 500 页 | P2 |
| forbidden | 403 页 | P2 |
| privacy | 隐私政策 | P2 |
| terms | 服务条款 | P2 |

---

## 选用规则

### P0 必备

新项目 MUST 产出全部 P0 页面:

- **App 端(4 页)**:home / mine / login / settings
- **Web 端(4 页)**:home / login / dashboard / settings

P0 不得删减,用户裁剪仅限 P1/P2。

### P1 按业务选

根据产品形态选配,常见组合:

- 电商/内容类 App:discover / messages
- 社区/工具类 App:feedback / about
- SaaS Web 后台:verify-email / profile
- 官网型 Web:about / contact

### P2 可选

错误页/协议页等,按合规与容错需求选配,建议至少保留 `not-found`。

---

## 与 draw-md 关联说明

- `draw-md` 子命令在新项目触发"页面清单确认"步骤时引用本索引(触发条件与步骤行为见 [draw-md.md](../commands/draw-md.md))。
- `draw-md` 产出的页面文件名(`examples/ui-markdown/ui/<slug>.md`)SHALL 与本清单 slug 对齐(如 `home.md`、`forgot-password.md`)。
- 用户可裁剪 P1/P2 但不得删减 P0。

---

## 端型选用指引

| 项目端型 | 引用清单 | 说明 |
| -------- | -------- | ---- |
| App 端(移动) | [app.md](./app.md) | 移动端 15 页清单 |
| Web 后台/官网 | [web.md](./web.md) | Web 端 15 页清单 |
| 跨端(移动+Web) | app.md + web.md | 两端清单各自适用,共享 design token 保证视觉一致(呼应 `framework/index.md` 框架选型指南的"需要同时支持移动+Web"行) |

---

## 示例链接列说明

当前 app.md / web.md 主表格的"示例链接"列指向各文档内锚点(`app.md#<slug>` / `web.md#<slug>`)。

---

## 参考链接

- [draw-md 子命令](../commands/draw-md.md)
- [框架资源总览](../framework/index.md)
