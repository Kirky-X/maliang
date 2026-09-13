# 表单模式命名词汇

> 术语库。表单与输入控件的模式化命名,统一"结构 + 校验时机 + 反馈位置"的选型语言。来源:GOV.UK Design System(components/error-summary、components/password-input、patterns/validation)、W3C WAI ARIA APG(patterns/combobox)、WorkOS Blog(ux-best-practices-for-mfa)、Authgear(login-signup-ux-guide)。抓取验证日期:verified 2026-09-08。

## 命名表

| 模式名                     | 视觉/行为特征                                                              | 适用场景                                            |
| -------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------- |
| `form-basic`               | 单列纵向,标签在上、输入在下,一个主提交按钮                                  | 通用信息采集(GOV.UK text-input 口径)                |
| `form-inline`              | 单行水平排布,回车即提交,无独立错误摘要区                                    | 搜索框、订阅条、快捷筛选                             |
| `form-wizard`              | 多步分步,步骤指示器,每步只问一件事,步内校验后前进                           | 注册引导、复杂开户、结账流程                         |
| `form-section`             | 长表单分组:组标题 + 描述,可配锚点导航                                       | 设置页、长问卷、详情编辑                             |
| `field-group`              | 输入组:前缀/后缀图标、单位或内嵌按钮                                        | 金额带单位、网址带协议、搜索框内嵌按钮               |
| `input-otp`                | 验证码分格,`type="text" + inputmode="numeric" + autocomplete="one-time-code"`,满位自动提交 | 短信/邮箱验证码(WorkOS:禁用 type=number 防丢前导零) |
| `input-masked`             | 格式掩码自动分隔,宽容空格/连字符/标点等杂字符                               | 电话、卡号、邮编(GOV.UK validation:忽略杂字符)     |
| `input-password-reveal`    | Show/Hide 明文切换,提交时还原为密文类型                                     | 注册/登录密码框(GOV.UK password-input)             |
| `input-password-strength`  | 实时强度计 + 要求清单逐项勾选                                               | 注册设置密码(Authgear"strength meters")            |
| `select-searchable`        | combobox:输入框 + 折叠弹层列表,可输入过滤,键盘上下键 + Enter 选择            | 选项 > 10 的选择器:国家、城市、标签(W3C APG)       |
| `input-character-count`    | 实时字数计数,接近/超限即提示                                                | 有上限的简介、留言(GOV.UK character count)         |
| `validate-on-submit`       | 提交时统一校验,失败整页回显并保留已填值                                     | 默认校验时机(GOV.UK 明确"勿在移出字段时校验")      |
| `validate-on-blur`         | 失焦即时标记单个字段错误                                                    | 格式类字段的即时增益;与 GOV.UK 口径冲突时按业务取舍(对照 [`ux-rules.md`](../meta/ux-rules.md) inline-validation) |
| `validate-inline`          | 错误文案显示在对应字段下方,aria-describedby 关联                            | 所有字段的行内反馈(GOV.UK error-message)           |
| `error-summary`            | 页面顶部汇总面板:标题 + 逐条错误链接回字段,自动聚焦 + role="alert",仅 1 条错误也要显示 | 服务端校验失败回显(GOV.UK error-summary)           |
| `form-autosave`            | 草稿自动保存/离开保留已填值,失败回显不重输                                  | 长表单、多步向导(GOV.UK:保留用户已填答案)         |
| `field-checkbox-group`     | 多选字段组:竖排列表 / 横排胶囊两种排布,勾选即时计数,可配最少/最多选中数校验           | 标签多选、兴趣/权限勾选、批量筛选条件(表格行首多选见 [`tables.md`](tables.md) `table-selectable`) |
| `select-basic`             | 常规下拉:点开弹层单选,无输入过滤,选中即收起                                   | 3-10 项短列表选择(分类/状态/时段);与 `select-searchable` 构成选项量级连续谱:<3 项用 radio 组,>10 项用 `select-searchable` |
| `upload-click` / `upload-drag` | 点击按钮选文件 / 拖拽区上传(拖入即高亮);文件类型与大小前置校验,上传中显进度、失败可重试;两变体共享"触发器 + 文件列表 + 进度 + 失败重试"结构 | 头像、附件、凭证、商品图上传                 |
| `field-date`               | 日期/时间选择字段:点按唤起选择器录入,与展示型日历(framework `calendar` 类)是录入/浏览两个交互域 | 预订、筛选区间、排期等日期/时间录入              |

> 来源注:`field-checkbox-group`、`select-basic`、`upload-click`/`upload-drag`、`field-date` 4 行为**审计补全**(2026-09-08 组件覆盖审计):对照 Ant Design(Checkbox/Select/Upload/DatePicker)、IBM Carbon(Checkbox/Dropdown/FileUploader/DatePicker)、Material 3(Selection controls/Menu/Date picker)组件清单;非 GOV.UK/W3C 原始来源。

## 使用规则

- 分工:[`ux-rules.md`](../meta/ux-rules.md) 管 Do/Don't 可核对规则(inline-validation、error-summary 等 slug),本表只管**模式命名与选型**,规则争议回链 ux-rules
- 校验时机首选 `validate-on-submit` + `error-summary` 成对出现(GOV.UK:摘要措辞须与行内错误完全一致);`validate-on-blur` 只用于强度计、字数上限等即时增益字段
- 表单按钮(主提交/次级取消)命名见 [buttons.md](buttons.md);错误确认与危险操作浮层见 [popups.md](popups.md)
- 表单容器、分栏与分组布局见 [layout.md](layout.md);提交等待/成功/禁用态命名见 [states.md](states.md)
- 密码字段配 `input-password-reveal`,不再加二次确认密码框(GOV.UK:show/hide 已替代 confirm 框);禁止 maxlength 截断
- 服务端校验永远保留:客户端校验只是增强,用户可绕过且 JS 可能失败(GOV.UK validation)

## 在 draw-md 中的写法

```markdown
## Form (checkout-address)
- pattern: form-section + validate-on-submit + error-summary
- fields:
  - { name: email, type: email, label: 邮箱, required: true }
  - { name: phone, pattern: input-masked, inputmode: tel }
  - { name: city, pattern: select-searchable, source: regions }
- submit: { type: button-primary, label: 提交, loading: states/loading }
- error: { summary: { focus: true, link_to_field: true }, inline: below-field }
```
