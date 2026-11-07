---
name: home # 页面名称(kebab-case 或简明英文/中文)
description: 首页 — 商品瀑布流 + 金刚区入口 # 一句话页面用途
background: "{surface-base}" # 页面背景,MUST 引用 token.md 的 token(非硬编码色值)
updated: 2026-06-30 # 更新时间(ISO 日期)
version: 1.0.0 # 页面版本号
mode: persuade # 可选:页面模式(persuade|operate|read|experience),判法见 references/meta/surface-modes.md
pattern: [table-sortable, form-wizard] # 可选:vocabulary 模式 slug 列表(命名对齐 references/vocabulary/ 各篇;框架代码由 draw-* 阶段映射)
platform: mobile # 可选:端型(mobile|web|ios|android|harmony|flutter)——触控阈值分端判定依据,移动端产物 SHOULD 声明
dir: ltr # 可选:书写方向(ltr|rtl)——声明 rtl 即承担逻辑属性硬门
spec_version: 1 # 可选:契约版本(当前 1;非 1 时校验器按 v1 规则检查并 WARN)
breakpoints: [375, 768, 1024] # 可选:响应式断点(升序整数,≥2 项)
---

**thesis**: <一句话:这一页要证明什么——删掉产品名后仍指向本产品才算数>
**own-world**: <一句话:本页占据的世界(物理空间/材质/光线)——能推出色彩与质感,而非品类通用词>
**first-viewport**: <一句话:首屏构图承诺——一小时后访客还能描述什么,答不上 = 未定>
**signature-interaction**: <一句话:招牌交互——指不出具体组件与触发方式 = 还没有>

<!-- 方向契约块:四字段以加粗字段名行书写,置于 frontmatter 之后、首个 ## 章节之前(检查 20 管在场);读起来像情绪 = 方向还没定 -->

<!-- 正文按从上到下、从左到右的视觉顺序组织章节:
     第一章 = 顶部导航(引用 organisms/ 导航栏组件);
     中间章节 = 页面主体各区块(每区块一章;区块原型从 references/components/INDEX.md 挑名,典型 5-7 个,不整库加载;
               组件 slug 组合按 references/framework/component-routing.md 路由表选,不凭感觉挑);
     最后一章 = 底部 dock(仅一级页面含 dock;二级页面末章为主体最后一区)。
     子组件从左到右描述,内部组件用嵌套子章节展开。 -->

## <顶部导航>(引用 organisms/nav-bar.md)

## <区块名>
<!-- 每个新增组件的参数表节前先附 4 行意图头,回答"为什么是这些值";复用既有组件(organisms / 前页已定义)可引用 DESIGN.md 或已有定义代替,不必重写 -->

意图:[这个组件为谁做什么,该什么感觉]
焦点:[本屏焦点是否在此;若不是,它如何刻意降级]
深度策略:[borders-only / subtle-shadows / layered / tint-shift 四选一,见 references/dimensions/elevation.md]
密度:[与页面 VISUAL_DENSITY 档位的关系;密集区如何控制]

| 参数        | 值                          | 说明       |
| ----------- | --------------------------- | ---------- |
| 组件类型    | `button` + `icon`(组合)     | 引用 references/framework/INDEX.md 的 56 类组件 slug,组合用 ` + ` 连接 |
| 宽度 width  | 375px(或 `match-parent`)    | 组件宽度   |
| 高度 height | 64px                        | 组件高度   |
| 字体大小    | `{font-size-md}`            | 引用 token |
| 圆角 radius | `{radius-subtle}`           | 引用 token |
| 背景颜色    | `{surface-card}`            | 引用 token |
| 字体颜色    | `{text-primary}`            | 引用 token |
| padding     | `{spacing-md} {spacing-lg}` | 引用 token |
| action      | `tap=→目标页; state=按下高亮; db=无; api=无; long-press=无` | 交互行为五元组:tap/state/db/api/long-press;action 行内 {xxx} 是 URL/JS 模板参数,非 token 引用 |
| intent      | 让"提交"在首屏无需滚动可达,故固定 44px 高 + primary 底 | 决定理由——每页 ≤3 个核心组件 SHOULD 声明,写决定不写描述 |

<!-- 多断点时表后补"响应式"说明(375 / 768 / 1024 各自差异) -->
