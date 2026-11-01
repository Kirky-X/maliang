# UX 规则库 —— 规则 ID + Do/Don't 可核对条目

> 规范层。本文是"规则 ID + Do/Don't"的**可核对条目库**:每条规则有稳定 slug、一句话规则、Do/Don't、适用端与严重级,供设计/实现/验证三阶段按 slug 引用与核对。基础精选 40 条;§11 浏览器原生面主题化 5 条§12 国际化与方向 1 条为 2026-09 整合审查增补(W2-05 harden 可正则子集配套登记,中文自研),§6 增补 fixed-width-text 1 条(同批)与 cancellable-state-transitions 1 条(2026-10 自 accessibility §8 收敛),§13 层级与动作 5 条,§14 包容性 5 条、§15 键盘与指针 7 条、§5 触控目标增补 3 条为 2026-11 增补(中文自研),§3/§4/§6/§13/§15 再增 5 条为 2026-11 二批(中文自研),§16 页面框架 7 条为 2026-11 三批(实证蒸馏),全库共 80 条。
> 与脚本的关系:`scripts/validate.py draw-md` 现有 23 项检查中 4 项回链本表 slug(aria-label → aria-labels;touch-target → touch-target-44 / web-target-size-24;fixed-width-text → fixed-width-text;physical-property → physical-property,回链见脚本 R_* 常量行内注释),其余 19 项为结构/token 契约项、无本表对应;演进目标:ERROR 级规则逐步机械化进脚本,新检查注释须回链 slug。脚本通过 ≠ 规则全对,脚本未覆盖的部分以本文 Do/Don't 为准。

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
| redundant-entry     | 同流程已填信息自动复用        | 自动填充先前值或提供选择            | 强制重输同一地址/账号       | 全端 | WARN     |

## 3. 反馈与状态

| slug                 | 一句话规则                    | Do(怎么做)                            | Don't(别怎么做)         | 端   | Severity |
| -------------------- | ----------------------------- | -------------------------------------- | ------------------------ | ---- | -------- |
| loading-buttons      | 异步提交期间按钮进入 loading 态 | 禁用 + spinner/进度,防重复提交          | 处理中仍可连点           | 全端 | WARN     |
| empty-states         | 空状态给消息与下一步动作        | 说明为何为空 + 主行动按钮               | 空白屏或干巴巴"暂无数据"  | 全端 | WARN     |
| toast-accessibility  | toast 不抢焦点且会消失          | aria-live="polite" 通报,3-5s 自动消失   | 抢焦点、永不消失的 toast | 全端 | WARN     |
| transition-duration-floor | 转场有时长下限,禁单帧硬切 | 全屏页面转场 ≥200ms 平滑过渡;转场过程不得插入 loading/加载态(缓存视图直接呈现) | 转场闪帧、路由切换闪 loading | 全端 | WARN     |
| disabled-states      | 禁用态可视且语义可辨            | 降透明度 + cursor 变化 + disabled 语义属性 | 禁用与可用外观无差别     | 全端 | ADVISORY |

## 4. 导航

| slug              | 一句话规则               | Do(怎么做)                        | Don't(别怎么做)       | 端           | Severity |
| ----------------- | ------------------------ | ---------------------------------- | ---------------------- | ------------ | -------- |
| nav-state-active  | 导航标明当前位置          | 当前项颜色/字重/指示条高亮          | 无当前态,用户迷路       | 全端         | WARN     |
| back-behavior     | 返回可预期并保留状态      | 返回恢复滚动位置/筛选/输入          | 静默重置导航栈跳首页    | 全端         | WARN     |
| modal-escape      | 模态必须提供明确退出途径  | 关闭按钮 + Esc/物理返回 + 点遮罩    | 仅靠隐藏手势或无退出    | 全端         | ERROR    |
| bottom-nav-limit  | 底部导航 ≤ 5 项且图标带文字 | 图标 + 短标签,超量收进"更多"        | 塞 6+ 项或纯图标导航    | ArkTS/Flutter | ADVISORY |
| no-dead-links     | 占位链接要么接真目标要么视觉禁用 | `#` 占位 href 换成真路由;确实未实现时用 `action:` 动作标识(draw-md 约定)或加视觉禁用态,不保留可点但无处去的链接 | 留 `href="#"` 的死链接充数;明知未实现还渲染成正常可点态 | 全端 | WARN     |
| back-no-interception | 退出/返回不拦截 | 一键返回目标页;确需拦截仅限未保存数据一类真损失,且只拦一次并给明确理由 | beforeunload 滥用、history 劫持、二次弹框确认"确定离开吗" | Web  | WARN     |

## 5. 触控目标

| slug               | 一句话规则                            | Do(怎么做)                   | Don't(别怎么做)              | 端            | Severity |
| ------------------ | ------------------------------------- | ----------------------------- | ----------------------------- | -------------- | -------- |
| touch-target-44    | 原生移动端(iOS/Android/鸿蒙)触控目标 ≥ 44pt/48dp/44vp(平台规范);Web 口径见 web-target-size-24 | 视觉不足时扩展热区至达标       | 热区跟重视觉尺寸一起缩水      | iOS/Android/鸿蒙 | ERROR    |
| web-target-size-24 | Web 指针目标 ≥ 24×24 CSS px(WCAG 2.2 2.5.8 AA),推荐 44px;原生分层口径见 touch-target-44 | 不足时间距等效豁免并记录原因   | 拿原生 44pt/48dp 混充 Web 达标 | Web            | ERROR    |
| touch-spacing      | 相邻触控目标间距 ≥ 8px                 | 密集列表加间隔或收拢行动       | 可点击元素紧贴排列            | 全端           | WARN     |
| hit-area-padding   | 热区内边距:带边框控件 ≈12px、无边框控件 ≈24px | 视觉尺寸外的透明热区扩边,防误触;过小显得必须精准瞄准,过大指针难移出 | 相邻热区留缝(条栏按钮热区不连续,高亮会在缝隙闪烁) | 全端           | ADVISORY |
| touch-press-visible | 触摸按压反馈必须可见                  | 反馈效果(辉光/提亮)避开指腹遮挡区或足够大,透过手指也能看到 | 反馈只在指腹正下方 1:1 区域(被手指盖住看不见) | iOS/Android/鸿蒙 | WARN     |
| target-scale-not-control | 放大热区而非控件本身            | 小/密集控件提供触摸时临时放大的可操作变体,抬指后保留片刻再收起 | 为达标把控件视觉尺寸放大,破坏布局密度 | 全端           | WARN     |

## 6. 文本韧性

| slug                        | 一句话规则                    | Do(怎么做)                                        | Don't(别怎么做)                | 端   | Severity |
| --------------------------- | ----------------------------- | -------------------------------------------------- | ------------------------------- | ---- | -------- |
| heading-line-balance        | 标题换行平衡仅作渐进增强       | `text-wrap: balance` 失效时自然换行仍可读           | 承诺精确末行,全局不间断空格/硬 br | Web  | ADVISORY |
| long-token-wrapping         | 长 token(URL/ID/哈希)必须可断行 | `overflow-wrap: anywhere` + flex/grid 文本子项可收缩 | 对正文 prose 用 `word-break: break-all` | Web  | WARN     |
| chip-collection-reflow      | chip 集合先换行再缩短          | 允许换行;`+n` 折叠必须是可点开的披露               | 全塞一行裁切,`+n` 只是藏值      | 全端 | WARN     |
| number-tabular              | 数据数字用等宽数字             | 表格数字/价格/计时用 tabular-nums 防列宽抖动        | 比例数字导致整列微跳            | 全端 | ADVISORY |
| truncation-strategy         | 截断必须留全文路径,且按字段分型 | 识别型字段(人名/标题)换行不截断;次要元数据尾部省略号;差异在后半段的(文件名/UUID/长域名)中段省略号保头尾;卡片预览 line-clamp;**数字/金额/日期永不截断**;任何截断配 tooltip/展开的全文路径,键盘可达 | 一刀切尾部省略号;只认 hover 出 tooltip;截断金额与日期 | 全端 | WARN     |
| fixed-width-text            | 文本容器禁固定宽度             | min-width / max-width / match-parent / flex 弹性,留换行与缩放余量 | 给 text 组件写死 `width: Npx`(超长词/emoji/RTL 溢出截断);登记:2026-09 整合审查(validate-draw-md 检查 14 回链) | 全端 | WARN     |
| cancellable-state-transitions | 动画可被打断且终态正确        | 快速状态切换取消/替换前序微交互,直接设置终态语义并清理副作用   | 依赖 animationend/transitionend 保证状态正确(被打断即坏);登记:2026-10 自 accessibility.md §8 收敛 | 全端 | WARN     |
| hyphenation-split   | 西文断词按文本长度二分         | 短文本(弹窗/标语/按钮)禁音节断行保整词;长文窄栏可音节断行,但行末 ≥3 字符、行首 ≥2 字符,连字符行数受限 | 短文案被拆成音节;长文行末 1-2 字符孤段 | 全端 | ADVISORY |

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
| progressive-loading | 等待反馈按 Doherty 分档给足 | <100ms 不给指示器;400ms-3s 给指示器;3s+ 给进度而非裸 spinner;布局已知时骨架优于 spinner(保空间语境);分档 canonical 见 [ux-laws.md](./ux-laws.md) Doherty 专节 | 长时间裸 spinner 或冻结无反馈;≤400ms 的快操作也闪指示器(指示器本身即干扰) | 全端 | WARN |
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
| readable-font-size   | 移动端正文 ≥ 16px          | 16px 起步,支持系统字号缩放       | 12-14px 小字(触发 iOS 聚焦缩放;输入控件聚焦放大的平台根因与修法见 mobile-floor M7)   | 全端           | ERROR    |
| horizontal-scroll    | 移动端禁止页面级横向滚动    | 内容自适应视口,宽表局部横滚      | 全页被撑出横向滚动条              | Web            | ERROR    |
| safe-area-awareness  | 主要操作避开刘海/手势条/边缘 | 用安全区 padding 包住导航与主按钮 | 底部按钮被手势条遮挡              | ArkTS/Flutter  | WARN     |
| viewport-units       | 移动端全屏高度用 dvh        | min-h-dvh 或兼容浏览器 chrome    | `100vh` 被地址栏裁切              | Web            | WARN     |

## 11. 浏览器原生面主题化

> 浏览器渲染的原生面(选区、光标、滚动条、焦点环、下划线)也是**设计面**:不做主题化时,它们以浏览器默认形态突兀在品牌界面里。全部为 Web 项;**Harmony/Flutter n/a**——原生组件体系无此面,主题化走各自平台机制(见 [`../commands/draw-harmony.md`](../commands/draw-harmony.md) / [`../commands/draw-flutter.md`](../commands/draw-flutter.md))。等宽数字已在 §6 number-tabular,此处不重复。

| slug              | 一句话规则                    | Do(怎么做)                                        | Don't(别怎么做)                | 端   | Severity |
| ----------------- | ----------------------------- | -------------------------------------------------- | ------------------------------- | ---- | -------- |
| selection-style   | 文本选区颜色是设计面           | `::selection` 配主题前景/背景对(从 token 派生)      | 依赖浏览器默认蓝选区             | Web  | ADVISORY |
| caret-color       | 输入光标与文本色同源           | `caret-color` 从主题 token 派生,暗色下可见          | 暗色界面留默认黑光标不可见       | Web  | ADVISORY |
| scrollbar-theme   | 滚动条随主题着色               | `scrollbar-color`(或 `::-webkit-scrollbar`)与界面主题一致 | 暗色界面闪默认白滚动条     | Web  | ADVISORY |
| focus-ring-token  | 焦点环颜色从主题派生           | 焦点环用主题色且满足对比度(可见性要求见 focus-states) | 默认蓝焦点环与品牌色打架       | Web  | ADVISORY |
| underline-offset  | 链接下划线光学对位             | `text-underline-offset` + `text-decoration-thickness` 调至不压字形 | 默认下划线穿过降部 | Web  | ADVISORY |

## 12. 国际化与方向


| slug               | 一句话规则                    | Do(怎么做)                                        | Don't(别怎么做)                | 端   | Severity |
| ------------------ | ----------------------------- | -------------------------------------------------- | ------------------------------- | ---- | -------- |
| physical-property  | 布局方向用逻辑属性             | margin/padding/border 用 `-inline-start/end`,text-align 用 `start/end` | 物理属性硬编码 left/right(或 text-align: left/right)且无 ltr-only 标注 | Web  | WARN     |

## 13. 层级与动作


| slug                   | 一句话规则                              | Do(怎么做)                                                                 | Don't(别怎么做)                          | 端   | Severity |
| ---------------------- | ---------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------- | ---- | -------- |
| primary-solid-unique   | 每页唯一实心主按钮;破坏性操作三级化     | Primary 实心高对比,通常每页恰一个;Secondary 用描边或低对比底;Tertiary 样式同链接;破坏性动作在页面层用次级/三级样式,红色实心主按钮只放进确认框(那里它才是真主操作) | 按语义而非层级配样式;「删除」直接大红按钮摆页面;一页多个实心主按钮互抢焦点 | 全端 | WARN     |
| label-fold-into-value  | label 是最后手段,能折进 value 就折     | 值自明格式(`$19.99`、邮箱地址)不配 label;确需 label 时折进值(「仅剩 12 件」,不是「库存: 12」)或排为显著次级内容;规格表式页面(用户扫的就是 label)才反向强调 label | `label: value` 平铺,给所有数据同等权重(数据库导出感) | 全端 | WARN     |
| weight-contrast-balance| 重量与对比互偿:加重量修低对比,降对比修超重 | 实心图标压过旁边文字 → 降图标对比(更柔的色);1px 边框柔色太隐、加深又太凶 → 保柔色加粗到 2px | 用同一种预算硬扛(只加深 / 只加粗)把另一维推过头 | 全端 | ADVISORY |
| baseline-align-mixed   | 一行混排字号对齐用 baseline             | 一行内大小字号混排用 `align-items: baseline`(Web)/ `CrossAxisAlignment.baseline`(Flutter),大数字与单位/标签底对齐 | 垂直居中对齐混排行,字面看起来各飘各的      | 全端 | ADVISORY |
| layout-explains        | 删掉不必要的次要标签与描述,让布局本身传达(Avoid unnecessary secondary labels and descriptions — let the layout do the explaining) | 层级靠尺度差/重量差/留白差/分组表达,先试「不加任何说明能不能不言自明」;说明文字只在删掉后会误读或误操作时保留(单位/法律/风险类);同组卡片用版式差异区分身份,说明只留一份且放在唯一需要处 | 每个标题上挂一行全大写小标签(eyebrow)充当层级;卡片下配「这是 XX 卡片」式自我描述行;标签与描述双份说同一件事;用说明行补版式没做出来的分组 | 全端 | WARN     |
| info-depth-3           | 单页面主要信息层级 ≤3 级      | 超过 3 级先合并/折叠(渐进披露)再谈排版                     | 4 层以上的嵌套分组硬排(人因实验:层级 >3 视觉复杂度显著上升) | 全端 | ADVISORY |

## 16. 页面框架

> 数据密集屏另见 [`app-screen-floor.md`](./app-screen-floor.md) 实测地板;本节管所有页面的**框架完整性**——空带、失衡、无边界是模板稿最常见的水印。

| slug                   | 一句话规则                                        | Do(怎么做)                                                                 | Don't(别怎么做)                          | 端   | Severity |
| ---------------------- | -------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------- | ---- | -------- |
| margin-pair            | 页面左右外边距是一对等值,全页复用                  | 16-32px 一档贯穿所有断点,逐宽度校验左右相等                                 | 各节 margin 各拍各的;左右不等               | 全端 | WARN     |
| half-width-needs-mate  | 文本占半宽时,另一半必须有内容                      | 图/第二列/列表/图元补位;实在无内容就收窄文本                                 | 半屏文本 + 半屏空白带                       | 全端 | WARN     |
| no-void-band           | >半屏的连续空白带禁止                              | "留白"必须有 closer 才成立(图本身/图跨洞/字跨洞/四角装裱),每页至多一次刻意 rest | 无 closer 的大空洞;节距拉到 250px+ 凑高度   | 全端 | WARN     |
| named-sections         | 每节有可命名的标题或明确的构成角色                | 逐节自检:这一节叫什么名字?答不出=没有存在理由                              | 无标题、无角色、纯装饰凑数节                | 全端 | ADVISORY |
| h1-says-what           | 首屏 h1 说出这是什么                               | h1 = 产品/页面是什么 + 给谁;副标补一行 how                                 | 抽象口号式大标题,看完不知道页面是什么       | 全端 | WARN     |
| anchor-lines           | 全页竖向锚线(左缘对齐轴)2-3 条                     | 数一遍左缘 x 位置:2-3 条=有决策,6 条=逐个摆放                              | 每节各起一个左缘,页边参差                   | 全端 | ADVISORY |
| section-rhythm         | 节间距 > 节内间距,节距 120-240(手机 72-112)        | 节与节的开合感明显;同页节距一致                                             | 节距与行距拉不开;节距忽大忽小               | 全端 | WARN     |

## 14. 包容性

| slug                   | 一句话规则                                        | Do(怎么做)                                                                 | Don't(别怎么做)                          | 端   | Severity |
| ---------------------- | -------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------- | ---- | -------- |
| inclusive-language     | 文案避开俚语/习语/有压迫渊源的短语                 | 用直白中性表达("遗留" 而非带歧视渊源的旧词);幽默谨慎,翻译后语义会漂移        | 未定义术语、圈内黑话、依赖文化语境的比喻     | 全端 | WARN     |
| gender-neutral         | 文案与人形图形性别中性;表单性别项给自填出口         | 表单需性别时给 nonbinary / self-identify / 不愿透露选项;人形图标用无性别人形 | 默认二元性别单选;人形图标暗示性别角色       | 全端 | WARN     |
| stereotype-check       | 以普遍人类经历替代特定文化/能力经历                 | 安全问题用"你最喜欢的活动"这类普适项,而非依赖车/房/教育经历的项;插图场景覆盖多元人群 | 场景/角色固化刻板印象(性别/种族/年龄/能力)  | 全端 | ADVISORY |
| people-first-disability | 残障表述用"人"优先语言,残障是光谱                 | "视障用户";交互设计考虑永久/临时/情境性残障(单手抱娃=情境性)                 | 把用户按能力二分("健全/残障");用缺陷定义人  | 全端 | ADVISORY |
| cultural-color-semantic | 色彩语义随目标 locale 校验                         | 面向新市场时核对颜色的文化含义(红在部分文化表喜庆非危险)                      | 假设语义色(红=危险/绿=成功)全球通用         | 全端 | ADVISORY |

## 15. 键盘与指针

| slug                   | 一句话规则                                        | Do(怎么做)                                                                 | Don't(别怎么做)                          | 端   | Severity |
| ---------------------- | -------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------- | ---- | -------- |
| keyboard-standard-shortcuts | 尊重标准快捷键语义,Esc=取消当前操作       | 仅为高频专属命令新增快捷键,组合键数 ≤3;Ctrl/Cmd+Z 撤销、Ctrl/Cmd+F 查找等标准语义不挪用 | 给标准快捷键重绑异义;堆砌快捷键降低可学性;给低频功能配快捷键   | Web/桌面 | WARN     |
| keyboard-modifier-roles | 修饰键分层:Ctl/Cmd 主命令、Shift 补充/反向、Alt 低频 | Shift-Tab 反向移动、Shift+Cmd+Z 重做;多修饰键按 Control→Alt→Shift→Command 顺序书写 | 给双字符键的上位字符再加 Shift;Alt 承载高频命令 | Web/桌面 | ADVISORY |
| input-compose-stability | 组合输入(IME/手写/语音)期间文本字段保持静止       | 候选窗/转写进行中不移动字段、不缩放、不自动滚动已转写文本                    | 输入中途重排布局或滚走落笔位置              | 全端 | WARN     |
| cursor-semantics       | cursor 跟随内容语义映射                           | 文本 I-beam、链接 pointer、拖拽 grab/grabbing、禁用 not-allowed、缩放 zoom-in/out、方向调整 resize-* | 全站默认 cursor 或漏设可点元素的 pointer    | Web  | ADVISORY |
| hover-delay-tiered     | hover 反馈延迟按用途分三档                        | 细微/邀请型即时显示;快速交互型(面板展开)短延迟;附加信息型(tooltip)更长延迟 | 所有 hover 一刀切零延迟(误扫即触发)或统一长延迟 | Web  | ADVISORY |
| hover-style-by-element | hover 效果按元素类型三选一                        | 组内控件=高亮;独立控件=lift(缩放+投影+高光,阴影不脱离缩放);大元素=自定义;表格行不用缩放 | 对所有元素套同一种 lift;只用阴影不缩放      | Web  | ADVISORY |
| no-gesture-hijack      | 不劫持浏览器原生手势                              | 双指滚动/捏合缩放/历史导航滑动保持系统行为;自定义手势只加在非冲突区          | preventDefault 掉捏合缩放或右键菜单且无替代  | Web  | WARN     |
| tap-lift-commit        | 点击抬手才生效,抬起前可反悔                       | 按下仅反馈、抬起且在热区内才提交;抬起前移出热区即取消——天然容错;"按下即生效"仅限可轻易撤销的场景 | 高压操作用按下触发(无反悔机会);按下即生效无撤销路径 | 全端 | WARN     |

## 与其他文档的关系

- WCAG 2.2 增量准则与韧性文本细则的展开版见 [`accessibility.md`](./accessibility.md) 第 7/8 节;触控目标分层口径(原生 44pt/48dp/44vp、Web 最低 24px/推荐 44px)与其 §5 强制项、§6 预检项、§7 target-size-minimum 一致
- 对比度阈值与 prefers-* 强制支持的完整规范见 [`accessibility.md`](./accessibility.md),本文 color-contrast 等条目是其规则出处
- 复用阶梯与结构性 hack 禁令见 [`framework/INDEX.md`](../framework/INDEX.md)
- `scripts/validate.py draw-md` 各检查项在脚本 R_* 常量行内注释标注本文 slug 回链:aria-label → aria-labels、touch-target → touch-target-44 / web-target-size-24,其余 11 项为结构/token 契约项注明"无 ux-rules 对应";新增脚本检查时先在本文登记规则条目
- §11 浏览器原生面主题化的交付检查点在 [`preview-checklist.md`](../commands/preview-checklist.md) 5.11「原生面锁」三条(Web 项;Harmony/Flutter n/a)
- overscroll 双层模型 / 键盘属性分派 / user-select 控件-内容二分的完整口径见 [`web-interface-guidelines.md`](./web-interface-guidelines.md)(input-type-keyboard 是其表单侧对齐条目)
- §8 等待反馈三条的时长分档与降级阶梯 canonical 见 [`ux-laws.md`](./ux-laws.md) Doherty 专节(六级映射 + 五级阶梯);§13 层级与动作的用户感知症状对照表见 [`visual-symptoms.md`](./visual-symptoms.md)(按危害排序)
