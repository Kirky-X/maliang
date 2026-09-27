# 生产化加固（Hardening）—— 设计只对完美数据成立 = 未完成

> 目的：设计稿与预览都用理想数据（等长标题、成功请求、单一语言、理想网络），上线后坏掉的原因几乎总在**真实数据的形状**里。本文件定义一条独立验证轴：用极端输入、真实错误、多语言、被打断的交互去攻击产物，判据可检测、可修复。交付机械判定归 [`preview-checklist.md`](../commands/preview-checklist.md) §5.16，本文件回答"怎么攻、怎么判、怎么修"。
>
> 来源：impeccable harden 思想（pbakaus/impeccable，Apache-2.0），2026-09 吸收，中文自研。

## 1. 极端输入

对每个文本容器与列表逐类喂"形状极端"的数据，渲染不破、不截断、不丢内容：

| 输入类 | 攻击什么 | 判据 |
| ------ | -------- | ---- |
| 单字符 / 空串 | 最小内容下布局塌陷、按钮收缩到不可点 | 布局保持，触控目标不缩水 |
| 超长无空格 token（URL / ID / 哈希） | 不换行长串撑破容器 | `overflow-wrap: anywhere` + flex/grid 文本子项 `min-width: 0`（见 [`mobile-floor.md`](./mobile-floor.md) M3/M4、[`ux-rules.md`](./ux-rules.md) long-token-wrapping） |
| emoji（含多码位 / ZWJ 序列） | 字号异常、截断处裁半个码位 | 截断以完整字符为界，无"豆腐块" |
| RTL 文本 | 物理属性写死的布局镜像错乱 | 见 §3 布局方向判据 |
| 千级列表 | 全量渲染卡死主线程 | 虚拟滚动或分页（对齐 preview-checklist 5.2 长列表项） |

## 2. 错误场景：分状态处置

每个请求路径必须对四类失败**各自**给出处置，禁止一个 catch-all toast 兜住全部：

| 场景 | 处置要点 |
| ---- | -------- |
| 4xx（客户端错） | 指出可修正的输入（字段旁内联提示，见 [`content-guide.md`](./content-guide.md) §4），用户改完即可重试 |
| 5xx（服务端错) | 表明是我方问题 + 重试入口 + 可用的降级路径（如查看缓存内容） |
| 超时 | 提供取消 + 重试；禁无限 spinner（对齐 [`ux-rules.md`](./ux-rules.md) progressive-loading） |
| 离线 | 检测后显式告知 + 缓存兜底或禁用写操作，禁静默失败 |

**并发双击防重**：提交请求进行中按钮进入 loading / 禁用（对齐 ux-rules loading-buttons），双击只产生一次提交；写操作建议后端幂等兜底，前端防重不是唯一防线。

## 3. 国际化：三框架判据

中文原文译英/德/俄等语言常见 **+30-40% 膨胀**：布局按最长译语实测，禁按中文长度定死容器宽高。三框架机制不同，判据分列（不互相照抄写法）：

| 判据 | Web | HarmonyOS（ArkTS） | Flutter |
| ---- | --- | ------------------ | ------- |
| 文案外置 | 文案进 i18n 资源，组件不硬编码 | 资源限定符目录（zh-CN / en-US 等）+ `$r` 引用 | Arb 文件 + intl 生成 |
| 布局方向 | CSS 逻辑属性（`margin-inline-start` / `inset-inline`）；用户生成内容包 `dir="auto"` | 跟随系统镜像方向，禁按 LTR 写死左右 | `EdgeInsetsDirectional` 等方向性 API 替代左右对称 API |
| 日期 / 数字 / 复数 | `Intl.DateTimeFormat` / `NumberFormat` / `PluralRules`，禁字符串拼接 | 系统 i18n / Intl 格式化接口 | intl 包 `DateFormat` / `NumberFormat` + 复数消息 |
| 组件内建语言 | Element Plus 组件语言走 `el-config-provider` locale | 资源系统按系统语言自动匹配 | `localizationsDelegates` + `supportedLocales` |

复数规则单列：中英"1 条 / 2 条"一套写法，俄语/阿拉伯语多复数形态必须走格式化接口的复数能力，禁 `(n === 1 ? '' : 's')` 式手写。

## 4. 被中断手势恢复

`pointercancel` 会被来电、通知中心下拉、系统边缘手势、第二根手指接管触发。判据：

- 捕获取消事件即复位：无残留的半拖状态、无卡在中间位的位置；
- **打断后再次拖拽无需刷新页面**即可正常工作；
- 与 [`../motion-skeletons/gesture-arbitration.md`](../motion-skeletons/gesture-arbitration.md) 衔接：该文件管识别与仲裁阈值，本条管取消后的状态清理。

## 5. verify 清单（设计/生成时自查）

> 本清单是**设计自查**层；交付机械判定以 preview-checklist §5.16 为准，结果按 preview.md「证据四分类」写入产物报告。

- [ ] 每个文本容器喂过最长真实内容 + 译语膨胀版（+30-40%），不溢出不截断
- [ ] 单字符 / 空串 / 纯 emoji 输入不破布局，截断以完整字符为界
- [ ] RTL 镜像下可用：方向性元素翻转、非方向性元素（媒体、时钟）不翻转
- [ ] 千级列表滚动不卡（虚拟化或分页已接）
- [ ] 每个请求路径有 4xx / 5xx / 超时 / 离线四态处置，无无限 spinner
- [ ] 提交防重：请求进行中双击只产生一次提交
- [ ] `pointercancel` 后无残留状态，再次拖拽无需刷新
- [ ] 日期 / 数字 / 复数全部走格式化接口，零字符串拼接、零 `(n===1)` 手写复数

## 与其他文档的关系

- 极端输入的修复手法与 [`mobile-floor.md`](./mobile-floor.md) M3/M4、[`ux-rules.md`](./ux-rules.md) §6 文本韧性共用一套，不另立数值
- 错误文案写法（原因 + 可执行建议）归 [`content-guide.md`](./content-guide.md) §4，本文只管"哪些状态必须有"
- 交付检查点在 [`preview-checklist.md`](../commands/preview-checklist.md) §5.16（5.0 Process 区的两项压力实测是本文件 §1/§2 的执行动作）
- 可正则判定的子集（固定宽度文本容器、物理属性硬编码）已机械化：`validate-draw-md.py` 检查 14/15（severity WARN，slug `fixed-width-text` / `physical-property` 登记于 [ux-rules.md](./ux-rules.md) §6/§12，回链见脚本 R_* 常量注释）
