---
name: mobile-layouts
title: 移动端高级布局五式
category: page-pattern
status: production
source: 视频研究 v21「5 种高级审美移动端网页」（WITH DESIGN INTENT 五模式帧转写）
era: 2026
verified: 2026-09-07
variance: "3-7"
motion: "1-3"
density: "2-6"
platforms: 移动端
---
# 移动端高级布局五式（Mobile Layouts）

## 一句话定位
同一块移动端画布换五种设计语言（图片主导/卡片节奏/大字留白/沉浸氛围/极简编辑）——生成前先选式再产出，替代 AI 默认的"紫渐变 hero + Welcome Back + 四宫格统计卡"。

## 视觉特征（token 级参数）
- 反面基准（AI 默认输出，v21 定性"总是差点意思"）：紫蓝渐变 + 问候语 + 四宫格 + 折线图，无设计意图
- 五式共同点：显式押中一项并做到极端——主次、节奏、字号比、氛围、色相数

### 式一：图片主导型（Image First）
- 首屏一张大图卡当主角：282×458、占屏高 54%；其余内容往两边收，主次一下就出来
- 适用：旅行/电商/作品等要视觉冲击的内容页。案例：Norway 山湖大图卡 + Explore New

### 式二：卡片节奏型（Card Rhythm）
- 大小卡交替 + 不等宽；顺序：大图 → 卡片 → 一排小标签 → 列表；"一路等宽"是反例
- 宽窄交替让手指划过去也有节奏。适用：阅读/资讯/杂志类长滚动流。案例：ISSUE 013 阅读流（42% 进度环）

### 式三：大字留白型（Big Type · Big Space）
- 超大标题 + 大面积留白：标题 33 / 正文 10.5（约 3.1 倍）；一屏只讲一件事
- 适用：情绪记录/单任务工具首屏。案例："今天，是什么颜色的?"（开心/平静/低落表情格）

### 式四：沉浸氛围型（Immersive）
- 背景不一定是纯色：铺一层图 + 模糊 + 透明（图底 + 玻璃卡）；先有氛围，再放内容，页面才有空气
- 适用：协作/数据看板等暗色沉浸场景。案例：NOVA 星桥攻坚台（79% Team Performance 玻璃卡）

### 式五：极简编辑型（Editorial Minimal）
- 一个色 + 细线 + 间距：整页只 1 个色相（案例全页 83 处同色相）；一个红只给三处——刻度、按钮、当前页
- 层级交给字号，设计感来自细节。适用：计时器/极简工具。案例：Pomo Focus 25:00 刻度环 + 红色"开始专注"

## 结构骨架
1. 选式：内容有主图 → 式一/式二；单件事 → 式三；暗色工具 → 式四；计时/编辑类 → 式五
2. 首屏只放一个主角（大图卡/超大标题/氛围层），次级内容两边收或下沉
3. 长滚动流按"大图 → 卡 → 小标签 → 列表"排节奏；重点色全页 ≤2-3 处
4. 式五的做法可单独抽用：任何页面都能"收敛到 1 个色相 + 重点色 3 处"

## 适用场景 / 慎用场景
- 适用：移动端 H5、小程序、App 内嵌页、移动端作品页
- 慎用：信息密集的移动后台（用式二承载，勿用式三/式五的留白挤掉数据）

## AI 常见翻车点（反模式）
1. 首屏拿一堆等大小图凑数（无主次）——正确：一张 282×458 主图卡占屏高 54%
2. 列表一路等宽等高，滚动无节奏
3. 一屏塞多件事，重点淹没；标题与正文只差一档字号（应约 3.1 倍）
4. 强调色到处都是；紫渐变 + 问候语开场（默认模板脸）

## CSS 关键实现（≤15 行）
```css
.hero-img { width: 282px; height: 458px; border-radius: 24px; object-fit: cover; } /* 占屏高 54% */
.rhythm > * + * { margin-top: 12px; }
.rhythm .wide { width: 100%; } .rhythm .half { width: 62%; } /* 宽窄交替，忌一路等宽 */
.display { font-size: 33px; line-height: 1.2; } .body { font-size: 10.5px; } /* 约 3.1 倍字比 */
.glass { background: rgba(255,255,255,.12); backdrop-filter: blur(18px); border-radius: 20px; }
.page { --ink: oklch(.55 .12 30); color: var(--ink); } /* 全页 1 个色相 */
.accent { color: var(--ink); } /* 红只给刻度/按钮/当前页三处 */
```

## 来源链接
- temp/video-analysis/v21.md（五式参数标注帧转写）
- 相关：temp/video-analysis/v03.md（App 布局量化对照 STAGGER/SCALE/ASYMMETRY/OVERLAP/WHITESPACE，见 references/vocabulary/layout.md）
