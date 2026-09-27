# UX 规则库 —— 规则 ID + Do/Don't 可核对条目

> 规范层。本文是"规则 ID + Do/Don't"的**可核对条目库**:每条规则有稳定 slug、一句话规则、Do/Don't、适用端与严重级,供设计/实现/验证三阶段按 slug 引用与核对。来源:ui-ux-pro-max-skill(`ux-guidelines.csv` 119 条 + `quick-reference.md` 稳定 ID)精选 40 条;精选日期 2026-09-07。§11 浏览器原生面主题化 5 条为 2026-09 吸收增补(impeccable 思想,Apache-2.0,中文自研);§12 国际化与方向 1 条为 2026-09 整合审查增补(W2-05 harden 可正则子集配套登记,中文自研),§6 增补 fixed-width-text 1 条(同批),全库共 47 条。
> 与脚本的关系:`scripts/validate-draw-md.py` 现有 15 项检查中 4 项回链本表 slug(aria-label → aria-labels;touch-target → touch-target-44 / web-target-size-24;fixed-width-text → fixed-width-text;physical-property → physical-property,回链见脚本 R_* 常量行内注释),其余 11 项为结构/token 契约项、无本表对应;演进目标:ERROR 级规则逐步机械化进脚本,新检查注释须回链 slug。脚本通过 ≠ 规则全对,脚本未覆盖的部分以本文 Do/Don't 为准。

## 严重级定义

| Severity  | 含义                           | 处置                   |
| --------- | ------------------------------ | ---------------------- |
| ERROR     | 可访问性硬伤/功能损坏,交付即失败 | 阻断交付,必须修复       |
| WARN      | 生产高频翻车,显著伤害体验       | 默认修复,豁免需写明理由 |
| ADVISORY  | 打磨项,做对加分                 | 建议遵循,不阻断         |

## 1. 可访问性

| slug              | 一句话规则                          | Do(怎么做)                                  | Don't(别怎么做)            | 端       | Severity |
| ----------------- | ----------------------------------- | -------------------------------------------- | --------------------------- | -------- | -------- |
| color-contrast    | 正文与背景对比度 ≥ 4.5:1(大字 3:1)  | 每个 colors.* 与背景配对过 AA,lint/preview 实算 | 低对比灰字,浅灰 placeholder 凑数 | 全端     | ERROR    |
| color-not-only    | 颜色不单独传达信息                   | 错误/成功/警告附图标或文字辅助                 | 仅红/绿区分对错             | 全端     | ERROR    |
| focus-states      | 每个交互控件有可见焦点环             | Tab 可达 + 2-4px 焦点环(含模态内控件)          | `outline: none` 不补替代    | 全端     | ERROR    |
| aria-labels       | 无文字的图标按钮必须有无障碍名        | aria-label / semanticLabel / accessibilityLabel | 纯图标按钮无可访问名        | 全端     | ERROR    |
| heading-hierarchy | 标题层级顺序递进不跳级               | h1→h6 顺序使用,层级即文档大纲                  | 跳级,或拿标题标签当字号样式  | Web      | WARN     |

## 2. 表单

| slug                | 一句话规则                   | Do(怎么做)                        | Don't(别怎么做)           | 端   | Severity |
| ------------------- | ---------------------------- | ---------------------------------- | -------------------------- | ---- | -------- |
| form-labels         | 每个输入框有可见 label        | label for 关联或包裹输入框          | placeholder 当唯一标签      | 全端 | ERROR    |
| input-type-keyboard | 语义输入类型唤起正确键盘      | email/tel/number/url 语义 type;inputmode 分派(numeric→验证码、decimal→金额);用户名/验证码加 autocapitalize=none + autocorrect=off;enterkeyhint 匹配动作语义(go/search/send/next/done)   | 一律 text 再靠用户手改,或键盘属性缺配   | 全端 | WARN     |
| inline-validation   | 校验在失焦后触发             | blur 后标记错误,提交前留纠错机会;GOV.UK 反对失焦校验,强监管/政府类表单改为提交时统一校验(双模式取舍见 [../vocabulary/forms.md](../vocabulary/forms.md)) | 每键报错                     | 全端 | WARN     |
| redundant-entry     | 同流程已填信息自动复用        | 自动填充先前值或提供选择            | 强制重输同一地址/账号       | 全端 | WARN     |

## 3. 反馈与状态

| slug                 | 一句话规则                    | Do(怎么做)                            | Don't(别怎么做)         | 端   | Severity |
| -------------------- | ----------------------------- | -------------------------------------- | ------------------------ | ---- | -------- |
| loading-buttons      | 异步提交期间按钮进入 loading 态 | 禁用 + spinner/进度,防重复提交          | 处理中仍可连点           | 全端 | WARN     |
| empty-states         | 空状态给消息与下一步动作        | 说明为何为空 + 主行动按钮               | 空白屏或干巴巴"暂无数据"  | 全端 | WARN     |
| toast-accessibility  | toast 不抢焦点且会消失          | aria-live="polite" 通报,3-5s 自动消失   | 抢焦点、永不消失的 toast | 全端 | WARN     |
| disabled-states      | 禁用态可视且语义可辨            | 降透明度 + cursor 变化 + disabled 语义属性 | 禁用与可用外观无差别     | 全端 | ADVISORY |

## 4. 导航

| slug              | 一句话规则               | Do(怎么做)                        | Don't(别怎么做)       | 端           | Severity |
| ----------------- | ------------------------ | ---------------------------------- | ---------------------- | ------------ | -------- |
| nav-state-active  | 导航标明当前位置          | 当前项颜色/字重/指示条高亮          | 无当前态,用户迷路       | 全端         | WARN     |
| back-behavior     | 返回可预期并保留状态      | 返回恢复滚动位置/筛选/输入          | 静默重置导航栈跳首页    | 全端         | WARN     |
| modal-escape      | 模态必须提供明确退出途径  | 关闭按钮 + Esc/物理返回 + 点遮罩    | 仅靠隐藏手势或无退出    | 全端         | ERROR    |
| bottom-nav-limit  | 底部导航 ≤ 5 项且图标带文字 | 图标 + 短标签,超量收进"更多"        | 塞 6+ 项或纯图标导航    | ArkTS/Flutter | ADVISORY |

## 5. 触控目标

| slug               | 一句话规则                            | Do(怎么做)                   | Don't(别怎么做)              | 端            | Severity |
| ------------------ | ------------------------------------- | ----------------------------- | ----------------------------- | -------------- | -------- |
| touch-target-44    | 原生移动端(iOS/Android/鸿蒙)触控目标 ≥ 44pt/48dp/44vp(平台规范);Web 口径见 web-target-size-24 | 视觉不足时扩展热区至达标       | 热区跟重视觉尺寸一起缩水      | iOS/Android/鸿蒙 | ERROR    |
| web-target-size-24 | Web 指针目标 ≥ 24×24 CSS px(WCAG 2.2 2.5.8 AA),推荐 44px;原生分层口径见 touch-target-44 | 不足时间距等效豁免并记录原因   | 拿原生 44pt/48dp 混充 Web 达标 | Web            | ERROR    |
| touch-spacing      | 相邻触控目标间距 ≥ 8px                 | 密集列表加间隔或收拢行动       | 可点击元素紧贴排列            | 全端           | WARN     |

## 6. 文本韧性

| slug                        | 一句话规则                    | Do(怎么做)                                        | Don't(别怎么做)                | 端   | Severity |
| --------------------------- | ----------------------------- | -------------------------------------------------- | ------------------------------- | ---- | -------- |
| heading-line-balance        | 标题换行平衡仅作渐进增强       | `text-wrap: balance` 失效时自然换行仍可读           | 承诺精确末行,全局不间断空格/硬 br | Web  | ADVISORY |
| long-token-wrapping         | 长 token(URL/ID/哈希)必须可断行 | `overflow-wrap: anywhere` + flex/grid 文本子项可收缩 | 对正文 prose 用 `word-break: break-all` | Web  | WARN     |
| chip-collection-reflow      | chip 集合先换行再缩短          | 允许换行;`+n` 折叠必须是可点开的披露               | 全塞一行裁切,`+n` 只是藏值      | 全端 | WARN     |
| number-tabular              | 数据数字用等宽数字             | 表格数字/价格/计时用 tabular-nums 防列宽抖动        | 比例数字导致整列微跳            | 全端 | ADVISORY |
| truncation-strategy         | 截断必须留全文路径             | ellipsis + tooltip/展开,键盘可达                   | 只在 hover 出 tooltip           | 全端 | WARN     |
| fixed-width-text            | 文本容器禁固定宽度             | min-width / max-width / match-parent / flex 弹性,留换行与缩放余量 | 给 text 组件写死 `width: Npx`(超长词/emoji/RTL 溢出截断);登记:2026-09 整合审查(validate-draw-md 检查 14 回链) | 全端 | WARN     |

## 7. 错误处理

| slug              | 一句话规则                     | Do(怎么做)                              | Don't(别怎么做)              | 端   | Severity |
| ----------------- | ------------------------------ | ---------------------------------------- | ----------------------------- | ---- | -------- |
| error-summary     | 提交失败聚焦顶部错误摘要        | 摘要可聚焦,逐条链回对应字段,保留行内错误  | 只给视觉摘要不聚焦            | Web  | WARN     |
| error-placement   | 错误显示在对应字段旁            | 字段下方具体错误 + aria-describedby 关联  | 仅顶部笼统一句,不指明字段     | 全端 | ERROR    |
| error-clarity     | 错误说清原因与修复方式          | "原因 + 怎么办"(如"密码需 ≥ 8 位,含字母") | 只说"输入无效"                | 全端 | WARN     |
| aria-live-errors  | 表单错误向读屏通报              | role="alert" 或 aria-live 区域           | 纯视觉错误指示                | Web  | ERROR    |

## 8. 性能感知

| slug                | 一句话规则                    | Do(怎么做)                        | Don't(别怎么做)           | 端   | Severity |
| ------------------- | ----------------------------- | ---------------------------------- | -------------------------- | ---- | -------- |
| progressive-loading | > 1s 的等待用骨架屏/占位       | 骨架或 shimmer 保布局稳定          | 长时间裸 spinner 或冻结无反馈 | 全端 | WARN     |
| content-jumping     | 异步内容预留空间              | 声明宽高/aspect-ratio,占位高度稳定 | 内容插入把页面往下顶(CLS)   | Web  | WARN     |
| tap-feedback-speed  | 点击 100ms 内给出视觉反馈      | 按压态即时高亮/涟漪                | 点击后无任何响应感         | 全端 | WARN     |

## 9. 数据展示

| slug              | 一句话规则               | Do(怎么做)                 | Don't(别怎么做)     | 端   | Severity |
| ----------------- | ------------------------ | --------------------------- | --------------------- | ---- | -------- |
| data-table        | 图表提供数据表替代        | 附表格或文本摘要供读屏      | 图表是唯一信息载体    | Web  | WARN     |
| pattern-texture   | 图表不只靠颜色区分类别    | 叠加纹理/形状/直接标注      | 仅用红绿系列区分序列  | 全端 | WARN     |
| empty-data-state  | 无数据给空态而非空白图    | "暂无数据"+引导,加载中给骨架 | 空白坐标系或破图      | 全端 | WARN     |
| no-pie-overuse    | 饼图分类 ≤ 5             | > 5 类换横向条形图          | 用 10+ 扇区的饼图     | 全端 | ADVISORY |

## 10. 移动端适配

| slug                 | 一句话规则                 | Do(怎么做)                      | Don't(别怎么做)                  | 端            | Severity |
| -------------------- | -------------------------- | -------------------------------- | --------------------------------- | -------------- | -------- |
| readable-font-size   | 移动端正文 ≥ 16px          | 16px 起步,支持系统字号缩放       | 12-14px 小字(触发 iOS 聚焦缩放)   | 全端           | ERROR    |
| horizontal-scroll    | 移动端禁止页面级横向滚动    | 内容自适应视口,宽表局部横滚      | 全页被撑出横向滚动条              | Web            | ERROR    |
| safe-area-awareness  | 主要操作避开刘海/手势条/边缘 | 用安全区 padding 包住导航与主按钮 | 底部按钮被手势条遮挡              | ArkTS/Flutter  | WARN     |
| viewport-units       | 移动端全屏高度用 dvh        | min-h-dvh 或兼容浏览器 chrome    | `100vh` 被地址栏裁切              | Web            | WARN     |

## 11. 浏览器原生面主题化

> 来源:impeccable 思想(pbakaus/impeccable,Apache-2.0),2026-09 吸收(W3-10),中文自研。
> 浏览器渲染的原生面(选区、光标、滚动条、焦点环、下划线)也是**设计面**:不做主题化时,它们以浏览器默认形态突兀在品牌界面里。全部为 Web 项;**Harmony/Flutter n/a**——原生组件体系无此面,主题化走各自平台机制(见 [`../commands/draw-harmony.md`](../commands/draw-harmony.md) / [`../commands/draw-flutter.md`](../commands/draw-flutter.md))。等宽数字已在 §6 number-tabular,此处不重复。

| slug              | 一句话规则                    | Do(怎么做)                                        | Don't(别怎么做)                | 端   | Severity |
| ----------------- | ----------------------------- | -------------------------------------------------- | ------------------------------- | ---- | -------- |
| selection-style   | 文本选区颜色是设计面           | `::selection` 配主题前景/背景对(从 token 派生)      | 依赖浏览器默认蓝选区             | Web  | ADVISORY |
| caret-color       | 输入光标与文本色同源           | `caret-color` 从主题 token 派生,暗色下可见          | 暗色界面留默认黑光标不可见       | Web  | ADVISORY |
| scrollbar-theme   | 滚动条随主题着色               | `scrollbar-color`(或 `::-webkit-scrollbar`)与界面主题一致 | 暗色界面闪默认白滚动条     | Web  | ADVISORY |
| focus-ring-token  | 焦点环颜色从主题派生           | 焦点环用主题色且满足对比度(可见性要求见 focus-states) | 默认蓝焦点环与品牌色打架       | Web  | ADVISORY |
| underline-offset  | 链接下划线光学对位             | `text-underline-offset` + `text-decoration-thickness` 调至不压字形 | 默认下划线穿过降部 | Web  | ADVISORY |

## 12. 国际化与方向

> 来源:2026-09 整合审查增补(W2-05 harden 可正则子集配套登记,中文自研),validate-draw-md.py 检查 15 回链本节 slug。物理方向属性(left/right)不随书写方向翻转,RTL 语境下布局不镜像;逻辑属性(start/end / -inline-*)一次编写双向成立。行内 `ltr-only` 标注为显式豁免(确与方向无关时使用)。HarmonyOS / Flutter 有各自的方向镜像机制,本条 CSS 属性名仅 Web 端可核对。

| slug               | 一句话规则                    | Do(怎么做)                                        | Don't(别怎么做)                | 端   | Severity |
| ------------------ | ----------------------------- | -------------------------------------------------- | ------------------------------- | ---- | -------- |
| physical-property  | 布局方向用逻辑属性             | margin/padding/border 用 `-inline-start/end`,text-align 用 `start/end` | 物理属性硬编码 left/right(或 text-align: left/right)且无 ltr-only 标注 | Web  | WARN     |

## 与其他文档的关系

- WCAG 2.2 增量准则与韧性文本细则的展开版见 [`accessibility.md`](./accessibility.md) 第 7/8 节;触控目标分层口径(原生 44pt/48dp/44vp、Web 最低 24px/推荐 44px)与其 §5 强制项、§6 预检项、§7 target-size-minimum 一致
- 对比度阈值与 prefers-* 强制支持的完整规范见 [`accessibility.md`](./accessibility.md),本文 color-contrast 等条目是其规则出处
- 复用阶梯与结构性 hack 禁令见 [`framework/index.md`](../framework/index.md)
- `scripts/validate-draw-md.py` 各检查项在脚本 R_* 常量行内注释标注本文 slug 回链:aria-label → aria-labels、touch-target → touch-target-44 / web-target-size-24,其余 11 项为结构/token 契约项注明"无 ux-rules 对应";新增脚本检查时先在本文登记规则条目
- §11 浏览器原生面主题化的交付检查点在 [`preview-checklist.md`](../commands/preview-checklist.md) 5.11「原生面锁」三条(Web 项;Harmony/Flutter n/a)
- overscroll 双层模型 / 键盘属性分派 / user-select 控件-内容二分的完整口径见 [`web-interface-guidelines.md`](./web-interface-guidelines.md)(input-type-keyboard 是其表单侧对齐条目)
