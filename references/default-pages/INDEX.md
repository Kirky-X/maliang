# 默认页面清单总索引

> 本文件是 `references/default-pages/` 的入口,为 `draw-md` 子命令提供 App/Web 两端的默认页面清单与选用规则。

---

## 总索引

App/Web 各 15 页的页面 slug、描述、优先级与示例链接**以平台文件为唯一源**,本文件不复述(防三处同步漂移;平台文件同时承载「列结构说明」五列定义):

- App 端(15 页):[app.md](./app.md)
- Web 端(15 页):[web.md](./web.md)

下方「页面 × 支撑资产映射」是本文件独有的资产路由视角,予以保留。

---

## 页面 × 支撑资产映射(30 页)

> 每个页面类型的三层落点:首选 [vocabulary](../vocabulary/) 模式 → [模板墙](../templates/INDEX.md) 条目 → [framework](../framework/INDEX.md) 组件类(该列均为 framework 索引表中的组件类型 slug)。标注"缺口"的是暂无现成支撑、建议后续补充的资产。本表只覆盖 30 个默认页;非默认页面按区块逐个选型,判据见 [framework/component-routing.md](../framework/component-routing.md)。

### App 端(15 页)

| 页面 | vocabulary 模式支撑 | 模板墙条目 | framework 组件类 |
| ---- | ------------------- | ---------- | ---------------- |
| home | [hero](../vocabulary/hero.md)、[galleries](../vocabulary/galleries.md)、[navigation](../vocabulary/navigation.md)(nav-bottom-tab/nav-dock) | [mobile-layouts](../templates/page/mobile-layouts.md)、[landing-patterns](../templates/landing-patterns.md) | navigation, grid, image, list, carousel, fab |
| discover | [search](../vocabulary/search.md)(search-bar/filter-chip)、[scroll](../vocabulary/scroll.md)(scroll-infinite/scroll-pull-refresh)、[galleries](../vocabulary/galleries.md) | [mobile-layouts](../templates/page/mobile-layouts.md) | input, tabs, grid, carousel, tag |
| messages | [popups](../vocabulary/popups.md)(popup-sheet 等弹层会话)、[states](../vocabulary/states.md)(空态/未读聚合);会话流(chat)模式缺口,建议后续补 chat 词汇 | 无专项(可借 [mobile-layouts](../templates/page/mobile-layouts.md) 卡片节奏) | notification, message, list, badge, avatar, tabs |
| mine | [cards](../vocabulary/cards.md)(card-media-left/card-action 功能入口卡) | 无专项 | avatar, card, list, badge, switch |
| login | [auth](../vocabulary/auth.md)(auth-split-brand/auth-password/auth-social)、[forms](../vocabulary/forms.md)(validate-on-submit) | 无专项(设计语言任选) | input, button, checkbox, icon |
| signup | [auth](../vocabulary/auth.md)(auth-toggle-mode/auth-otp)、[forms](../vocabulary/forms.md)(input-otp/form-basic) | 无 | form, input, checkbox, button |
| forgot-password | [forms](../vocabulary/forms.md)(input-otp/error-summary)、[auth](../vocabulary/auth.md) | 无 | form, input, button, message |
| settings | [forms](../vocabulary/forms.md)(form-section);设置分组/子入口模式为弱支撑 | 无 | list, switch, select, slider, theme, popconfirm |
| about | [typography](../vocabulary/typography.md)、[layout](../vocabulary/layout.md)(弱支撑) | [editorial-swiss](../templates/editorial-swiss.md) | text, image, list, divider |
| privacy / terms | [typography](../vocabulary/typography.md)(弱支撑);法务长文页结构模式缺口,建议后续补 legal-doc 模式 | [editorial-swiss](../templates/editorial-swiss.md) | text, divider |
| feedback | [forms](../vocabulary/forms.md)(field-group/input-character-count) | 无 | form, input, radio, upload, button |
| empty-state | [states](../vocabulary/states.md)(state-empty-first-use/no-results/clear-filters/starter) | 无 | image, button, text |
| network-error | [states](../vocabulary/states.md)(state-error-network/state-offline) | 无 | button, image, message |
| not-found | [states](../vocabulary/states.md)(state-error-crash 近似);404 专属出口(搜索/回首页)模式缺口 | 无 | button, image |

### Web 端(15 页)

| 页面 | vocabulary 模式支撑 | 模板墙条目 | framework 组件类 |
| ---- | ------------------- | ---------- | ---------------- |
| home | [hero](../vocabulary/hero.md)、[galleries](../vocabulary/galleries.md)、[navigation](../vocabulary/navigation.md) | [landing-patterns](../templates/landing-patterns.md)、[editorial-split](../templates/page/editorial-split.md) | navigation, grid, image, button, carousel |
| about | [typography](../vocabulary/typography.md)(type-editorial)、[layout](../vocabulary/layout.md)(layout-two-column) | [editorial-swiss](../templates/editorial-swiss.md)、[editorial-split](../templates/page/editorial-split.md) | text, image, grid, timeline |
| contact | [forms](../vocabulary/forms.md)(form-basic/field-group/error-summary) | 无 | form, input, select, button |
| login | [auth](../vocabulary/auth.md)、[forms](../vocabulary/forms.md) | 无专项(设计语言任选) | input, button, checkbox, card |
| signup | [auth](../vocabulary/auth.md)(auth-otp)、[forms](../vocabulary/forms.md)(input-otp) | 无 | form, input, checkbox, button |
| forgot-password | [forms](../vocabulary/forms.md)(input-otp/error-summary) | 无 | form, input, button |
| verify-email | [forms](../vocabulary/forms.md)(input-otp/field-group)、[auth](../vocabulary/auth.md)(auth-otp/auth-magic-link);验证成功/链接过期页面状态暂缺专属模式,暂借 [states](../vocabulary/states.md) 的 state-error-crash 语义 | 无 | input, form, button, message |
| dashboard | [charts](../vocabulary/charts.md)、[tables](../vocabulary/tables.md)(table-sortable/table-paginated);chart 组件类缺口(framework 索引表无 chart 类),建议后续补 chart 组件类 | [data-dense-dashboard](../templates/data-dense-dashboard.md)、[dashboard-styles](../templates/page/dashboard-styles.md) | statistic, table, card, tabs, menu, skeleton |
| settings | [forms](../vocabulary/forms.md)(form-section/form-autosave) | 无 | form, input, select, switch, radio, upload |
| profile | [cards](../vocabulary/cards.md)(card-media-bg 头像区)、[forms](../vocabulary/forms.md)(field-group/input-masked) | 无 | avatar, upload, form, input, card |
| not-found | [states](../vocabulary/states.md)(state-error-crash 近似) | 无 | button, image |
| server-error | [states](../vocabulary/states.md)(state-error-crash:错误插画 + 重试/返回,覆盖 5xx 语义;无 5xx 专属模式) | 无 | button, image, message |
| forbidden | [states](../vocabulary/states.md)(state-error-permission:权限说明 + 申请入口) | 无 | button, image |
| privacy / terms | [typography](../vocabulary/typography.md)(弱支撑);法务长文页结构模式缺口,建议后续补 legal-doc 模式 | [editorial-swiss](../templates/editorial-swiss.md) | text, divider |

---

## 选用规则

### P0 必备

新项目 MUST 产出全部 P0 页面:

- **App 端(4 页)**:home / mine / login / settings
- **Web 端(4 页)**:home / login / dashboard / settings

P0 不得删减,用户裁剪仅限 P1/P2。

### P1 按业务选

按产品形态查下表选配(页面 slug 花名册以 [app.md](./app.md) / [web.md](./web.md) 为唯一源,本表只做「形态 → 选配」判据):

| 产品形态 | App P1 选配 | Web P1 选配 |
| -------- | ----------- | ----------- |
| 电商 / 交易 | discover, messages | contact, verify-email |
| 内容 / 社区 | discover, about | about, contact |
| 效率工具 | feedback, about | profile, contact |
| SaaS / 后台 | feedback | profile, verify-email |
| 社交 / 通讯 | messages, feedback | profile, verify-email |
| 通用底座(任何形态必配) | signup, forgot-password | signup, forgot-password |

- **未列形态**:按「用户产生内容的页面优先于管理功能页面」就近判,选择写入页面产出清单并注明假设。
- P1 全不适用时可仅出通用底座行,不凑满;P1 全部可裁,裁剪不影响 P0 义务。

### P2 可选

错误页/协议页等,按合规与容错需求选配,建议至少保留 `not-found`。

---

## 与 draw-md 关联说明

- `draw-md` 子命令在新项目触发"页面清单确认"步骤时引用本索引(触发条件与步骤行为见 [draw-md.md](../commands/draw-md.md))。
- `draw-md` 产出的页面文件名(`.maliang/ui-markdown/ui/<slug>.md`)SHALL 与本清单 slug 对齐(如 `home.md`、`forgot-password.md`)。
- 用户可裁剪 P1/P2 但不得删减 P0。

---

## 端型选用指引

| 项目端型 | 引用清单 | 说明 |
| -------- | -------- | ---- |
| App 端(移动) | [app.md](./app.md) | 移动端 15 页清单 |
| Web 后台/官网 | [web.md](./web.md) | Web 端 15 页清单 |
| 跨端(移动+Web) | app.md + web.md | 两端清单各自适用,共享 design token 保证视觉一致(呼应 `framework/INDEX.md` 框架选型指南的"需要同时支持移动+Web"行) |

---

## 示例链接列说明

当前 app.md / web.md 主表格的"示例链接"列指向各文档内锚点(`app.md#<slug>` / `web.md#<slug>`)。

---

## 参考链接

- [draw-md 子命令](../commands/draw-md.md)
- [框架资源总览](../framework/INDEX.md)
