# 登录注册模式命名词汇

> 术语库。认证页面(登录/注册/验证/找回)的模式化命名。来源:Authgear(login-signup-ux-guide)、Microsoft Learn(passkey design guidelines)、WorkOS Blog(ux-best-practices-for-mfa)、GOV.UK Design System(components/password-input)。抓取验证日期:verified 2026-09-08。

## 命名表

| 模式名                  | 视觉/行为特征                                                                   | 适用场景                                   |
| ----------------------- | -------------------------------------------------------------------------------- | ------------------------------------------- |
| `auth-password`         | 邮箱/用户名 + 密码框 + 登录按钮;"忘记密码"紧贴密码框下方                          | 通用登录(Authgear)                        |
| `auth-social`           | 第三方登录按钮组:2-3 个主供应商,遵守各家品牌规范,配"或"分隔线与隐私 microcopy     | C 端注册登录(Authgear:主方法置顶,其余收起) |
| `auth-combined-entry`   | 合并入口:输入邮箱一次,系统自动判定登录或注册                                      | 首页登录注册一体(Microsoft/Authgear 均推荐) |
| `auth-toggle-mode`      | 登录/注册分页时,底部固定切换文案,如"新用户?创建账号"                             | 分离式双页(Authgear)                      |
| `auth-magic-link`       | 输邮箱 → 发登录链接 →"查收邮件"确认态(重发/换邮箱);过期链接一键重发且预填邮箱     | 低摩擦登录(Authgear)                      |
| `auth-otp`              | 手机号/邮箱收验证码登录:自动填充 + 满位自动提交,失败给重发倒计时                   | 移动优先产品(Authgear/WorkOS)             |
| `auth-mfa`              | 二步验证:密码后独立 MFA 屏,说明为何需要;主方法默认选中 +"尝试其他方式"切换        | 已开启二步验证的账号(WorkOS)              |
| `auth-passkey`          | passkey 登录:用户名框 `autocomplete="webauthn"` 自动填充优先,配专用按钮与降级路径  | 现代账号体系(Microsoft Learn:autofill 成功率最高) |
| `auth-sso`              | 企业 IdP 单点登录入口(SAML/OIDC),常以"使用 XX 继续"按钮呈现                        | B2B/企业产品                               |
| `auth-passwordless`     | 无密码总模式:passkey/OTP/magic link 组合,首次配教育文案,始终留密码降级路径         | 全面去密码的账号体系(Authgear)            |
| `auth-split-brand`      | 左品牌区(logo/价值主张/插画)+ 右表单区分栏                                        | SaaS 登录页、营销型站点                    |
| `auth-guest-checkout`   | 游客结算:跳过注册直接购买,只收最小信息,事后引导绑定账号                            | 电商结账(Authgear:渐进补全画像)          |

## 使用规则

- 分工同 [forms.md](forms.md):[`ux-rules.md`](../meta/ux-rules.md) 管 Do/Don't 可核对规则,本表只管**模式命名与选型**;表单字段级模式复用 forms.md
- 登录/注册按钮与社交按钮命名见 [buttons.md](buttons.md);错误与二次确认浮层见 [popups.md](popups.md);左品牌右表单的分栏结构见 [layout.md](layout.md);提交等待态见 [states.md](states.md)
- 登录失败不得暴露"用户名或密码哪个错",并清空密码框(GOV.UK password-input);密码框复用 forms.md 的 `input-password-reveal`,不加二次确认框
- 每种认证模式必须自带降级路径(passkey→密码、OTP→换方法、magic link→重发),不许死胡同(Authgear"don't dead-end users")
- 凭据输入框务必设 `autocomplete="username"/"current-password"/"new-password"`,且允许粘贴(Authgear:禁粘贴伤密码管理器用户)
- 验证码屏用 forms.md 的 `input-otp` 分格模式;MFA 招募给多方法选择,QR 码外必须给文本密钥(WorkOS)

## 在 draw-md 中的写法

```markdown
## Page (auth-login)
- pattern: auth-split-brand > auth-password + auth-social
- left: { brand: { logo, tagline } }
- form: { pattern: form-basic, fields: [email, password(input-password-reveal)] }
- extras: { forgot: text-link, social: [google, apple], divider: "或" }
- fallback: [auth-magic-link, auth-otp]
```

```markdown
## Step (auth-mfa)
- pattern: auth-mfa
- methods: [totp, sms, backup-code]
- otp_input: { pattern: input-otp, length: 6, autosubmit: true, autocomplete: one-time-code }
- switch: { label: 尝试其他方式, type: text-link }
```
