# 区段原型库（Components Index）

> 区段级编码原型：50 个原型，覆盖一页的全部区段类型。**从索引挑名、只加载选中的那几个。**编号消歧**:本库 H1–H9 指代 hero 区段原型;`vocabulary/hero.md` 与 `dimensions/hero-stage.md` 中的 H1–H4 指 Hero 硬约束条目——两套编号语境不同,引用时以文件为准**——典型一次构建需要 5-7 个文件：1 个 hero + 1 个区段头 + 1-2 个主体区段 + 1 个 CTA + 1 个页脚 + 1 个导航；不整库加载。
>
> 分工：[templates/](../templates/README.md) 选整页语言，本库选「每个区段长成什么」；元素级外观（按钮/卡片/表单的样式细节）仍在 [vocabulary/](../vocabulary/)。每个原型的「变体旋钮」供 [variation-engine.md](../templates/variation-engine.md) 盖章扩 knob 引用——选原型时逐旋钮取值并写进盖章。

## Hero（首屏，9 个）

| id | 原型 | 一句话形状 |
| --- | --- | --- |
| H1 | [跑马灯宣言](h1-marquee.md) | 一句 display 大字撑满首屏，无副标题无 CTA |
| H2 | [左右双联](h2-split-diptych.md) | 左文案右实证，6/6 或 7/5 分栏 |
| H3 | [引言主导](h3-quote-led.md) | 带署名的拉引言做首屏主角 |
| H4 | [数字主导](h4-stat-led.md) | 一个巨型数字 + 一行限定语 |
| H5 | [书信开场](h5-letter-hero.md) | 第一人称「致读者」式开场，首屏无按钮 |
| H6 | [摄影满版](h6-photographic-fold.md) | 一张满版真图占满视口，说明字落角 |
| H7 | [演示视频裁边](h7-demo-video-clipped-by-viewport-edge.md) | 左标题右视频，视频右缘 10-20% 刻意溢出被裁 |
| H8 | [模型分栏](h8-mockup-split-browser-framed.md) | 左标题右浏览器框模型，倾斜 1-3° |
| H9 | [手绘插画主角](h9-custom-illustration-centerpiece.md) | 一件自建 SVG/CSS 插画做首屏主视觉 |

## 区段头（5 个）

| id | 原型 | 一句话形状 |
| --- | --- | --- |
| S1 | [左栏编号](s1-left-margin-numbered.md) | 窄左栏放「01 — 标签」，宽右栏放标题与内容 |
| S2 | [悬置标题](s2-hanging.md) | 标题浮在负空间里，无边无线 |
| S3 | [粘性钉住](s3-sticky-pinned.md) | 标题钉在视口内，内容从底下滚过 |
| S4 | [行内不断章](s4-inline-no-break.md) | 小型大写短语嵌在正文流里，不断章 |
| S5 | [底部锚定](s5-bottom-anchored.md) | 标签放在区段内容下方，反转层级 |

## 主体区段（6 个）

| id | 原型 | 一句话形状 |
| --- | --- | --- |
| F1 | [Bento 网格](f1-bento-grid.md) | 8-15 块混合跨度的非对称瓦片 |
| F2 | [粘性滚动栈](f2-sticky-scroll-stack.md) | 左栏钉住，右栏滚动换图 |
| F3 | [规格表](f3-tabular-spec-sheet.md) | 每行一特性，发丝线分行，表格数字 |
| F4 | [步骤序列](f4-step-sequence.md) | 编号阶段（1.0→2.0→3.0）纵向流动 |
| F5 | [标注截图](f5-annotated-screenshot.md) | 产品截图居中，箭头/短标签指向细节 |
| F6 | [商品卡网格](f6-product-card-grid.md) | 每卡一商品：图·名·价·一个微动作 |

## CTA / 行动（4 个）

| id | 原型 | 一句话形状 |
| --- | --- | --- |
| C1 | [描边 chip](c1-outlined-chip.md) | 透明底描边按钮 + 排版动词 |
| C2 | [行内表单即 CTA](c2-inline-form-as-cta.md) | CTA 本身就是邮箱输入 + 提交 |
| C3 | [排版链接](c3-typographic-link.md) | 一个词 + 一个箭头 + 1px 下划线 |
| C4 | [粘性底栏](c4-sticky-bottom-bar.md) | 钉在视口底部的横条：CTA + 一句安心话 |

## 证言 / 证明（4 个）

| id | 原型 | 一句话形状 |
| --- | --- | --- |
| T1 | [边注拉引言](t1-pull-quote-with-marginalia.md) | 引言占宽栏，署名与来源浮在窄边栏 |
| T2 | [发丝线 logo 墙](t2-logo-wall-hairline.md) | 单色客户 logo 一排，发丝线分隔，无卡片 |
| T3 | [独占巨引](t3-single-huge-quote.md) | 一句引言放大约占整节，署名收成小字行 |
| T4 | [编号数据条](t4-numbered-stat-strip.md) | 3-5 个互补指标横排一条 |

## 页脚（8 个）

| id | 原型 | 一句话形状 |
| --- | --- | --- |
| Ft1 | [报头式](ft1-mast-headed.md) | 字标 + 标语锚定一条横带，少量链接 |
| Ft2 | [单行内联](ft2-inline-rule-single-line.md) | 一行版权·地址·许可，上压发丝线 |
| Ft3 | [索引式分类列](ft3-index-style-category-list.md) | 3-4 短列，小型大写类目头，各挂 4-6 链接 |
| Ft4 | [密集版权页](ft4-dense-typographic.md) | 一大块 mono 小字：版本·构建·许可·地址 |
| Ft5 | [宣言句](ft5-statement.md) | 一句 display 大字收尾，元信息压在下面 |
| Ft6 | [书信落款](ft6-letter-close.md) | 「此致——工作室」式落款，可带附言 |
| Ft7 | [订阅优先](ft7-newsletter-first.md) | 订阅表单是页脚主角，其余收成 12px 小字 |
| Ft8 | [跑马灯滚动](ft8-marquee-scroll.md) | 标语·分隔符无限横滚一行 |

## 导航（14 个）

| id | 原型 | 一句话形状 |
| --- | --- | --- |
| N1 | [字标双链](n1-wordmark-2-links.md) | 左字标右两条文字链的极简顶栏 |
| N1b | [SaaS 三段标准栏](n1b-saas-three-section.md) | 字标左·中簇 4-6 链接·登录+实心 CTA 右 |
| N2 | [浮动角标](n2-floating-chip.md) | 钉在角落的小 chip：字标 + 单一动作 |
| N3 | [侧栏轨](n3-side-rail.md) | 左缘细竖条：旋转字标 + 区段圆点指示 |
| N4 | [藏于 ⌘K](n4-hidden-behind-k.md) | 无可见导航，⌘K 命令面板即全部 |
| N5 | [浮动药丸](n5-floating-pill.md) | 明显脱离页缘的圆角药丸，模糊底衬 |
| N6 | [报纸报头](n6-newspaper-masthead.md) | 居中大字标 + 期号行 + 双线 |
| N7 | [粗野厚板](n7-brutal-slab.md) | 2px 实线下边、全大写、密集无圆角 |
| N8 | [终端命令](n8-terminal-command.md) | 导航排成 CLI 提示行，链接即命令旗标 |
| N9 | [贴边极简](n9-edge-aligned-minimal.md) | 字标贴左 CTA 贴右，中间大片空 |
| N10 | [滚动形变浮窗](n10-floating-on-scroll-morph.md) | 顶栏过阈值后形变为浮动药丸（单 DOM 双态） |
| N11 | [巨型菜单](n11-mega-menu.md) | 触发器开全宽多列面板，页底压暗纱 |
| N12 | [公告条 + 收回](n12-banner-retract.md) | 彩色公告条叠在真导航上，下滚收回 |
| N13 | [行内 ⌘K 搜索药丸](n13-inline-cmdk-pill.md) | 栏内可见搜索药丸 + ⌘K 聚光灯弹层 |

## 总则（横切规则，全原型生效）

1. **同页不重样**：同一页内任意两个区段不得用同一原型（F1 Bento 可与 C2 表单、T2 logo 墙相邻搭配，不可两块 Bento）。
2. **跨产出轮换**：同一会话连续构建中，导航与页脚原型**连续两次相同即违规**。写导航/页脚标记前先声明一行：「上一构建导航/页脚：X。本构建：Y，因为 Z」。题材默认款不能连用，要有意识地在「也可」列里轮换（如 N1a 是最被滥用的 AI 指纹，只有页面真只有 2 个目的地时才用；Ft3 只给真正的枢纽/文档根，其余默认 Ft1/Ft2/Ft4-Ft8）。
3. **同原型必换旋钮**：复用同一原型时，逐旋钮至少换一个值并在盖章中声明全部旋钮值——**同一组旋钮值跨产出照抄 = 与照抄原型同款**（上一次 Bento 是 `tiles=6, spans=irregular, accent=corner-only`，下一次至少变一个）。
4. **两个折叠断点**：<60rem（约 960px）是**布局**断点——多栏塌单栏、倾斜/裁边效果撤除、粘性栏解除；<40rem（约 640px）是**排版**断点——display 字号降一档、边栏标签转行内、标注合并。窄屏下原型必须仍是它自己：层级、气质、节奏不变，只是堆叠成单列。
5. **44px 命中区**：<40rem 一切可点目标 ≥ 44×44px（WCAG AA），不得更小。
6. **页缘净空**：页面容器 `padding-inline: clamp(1rem, 4vw, 1.5rem)` 起步，内容不贴屏缘。
7. **滚动动画**：<40rem 禁用一切滚动驱动动画（移动端滚动有自己的物理，多层动画互相打架）。
8. **图片加载**：首屏以下一律 `loading="lazy"`；LCP 元素任何视口下都禁 lazy。
9. **自动播放视频**：尊重 `navigator.connection.saveData`（`data-saver` 置位时换 poster 图）。

## 选型步骤

1. 判断该区段的角色（hero / 区段头 / 主体 / CTA / 证言 / 页脚 / 导航）。
2. 扫该类目下的原型，取「何时用」命中 brief 的那一个。
3. 同页查重：没有两个区段共用一个原型。
4. 整页模板（[templates/](../templates/README.md)）若已指定默认原型则沿用；未指定时**有意轮换**，不落默认套路。
5. 每原型逐旋钮取值，连同原型 id 写入构建盖章（见 [variation-engine.md](../templates/variation-engine.md)）。

来源：hallmark components cookbook 改写，2026-10 吸收（索引与总则含旋钮总表、路由表与移动端折叠表三张横切表）。
