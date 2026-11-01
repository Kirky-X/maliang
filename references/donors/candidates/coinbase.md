<!-- 供体候选池快照(中文译本,非蒸馏供体;原文见「原始出处」)。
     站点分组: 金融与加密(finance) · 站点摘要: 加密交易所。干净的蓝色识别、侧重信任、机构感
     站点色板: #0a0b0d, #0052ff, #578bfa, #eef0f3, #282b31, #5b616e
     晋升正式供体须满足 ../README.md §5 三条件;蒸馏稿另立 ../<id>.md,与本快照并存。 -->

# 设计系统:Coinbase

## 1. 视觉主题与氛围

Coinbase 的网站是一个干净、可信赖的加密平台,用蓝白二值色板传达金融可靠性。设计把 Coinbase Blue(`#0052ff`)——一种深而饱和的蓝——当作唯一的品牌强调色,置于白色与近黑表面之上。自有字族包含 CoinbaseDisplay(主视觉标题)、CoinbaseSans(UI 文本)、CoinbaseText(正文阅读)、CoinbaseIcons(图标)——一套完整的四字体系统。

按钮系统用独特的 56px 圆角做药丸形 CTA,悬浮态过渡到更浅的蓝(`#578bfa`)。设计在白色内容区与暗色(`#0a0b0d`、`#282b31`)功能区之间交替,形成专业、金融级的界面。

**关键特征:**
- Coinbase Blue(`#0052ff`)作为唯一品牌强调色
- 四字体自有字族:Display、Sans、Text、Icons
- 56px 圆角药丸按钮,悬浮过渡到蓝
- 近黑(`#0a0b0d`)暗区 + 白色亮区
- 显示级标题行高 1.00 —— 极紧
- 冷灰次级表面(`#eef0f3`),带蓝调
- 部分按钮文案用 `text-transform: lowercase` —— 少见

## 2. 色板与角色

### 主色
- **Coinbase Blue**(`#0052ff`):主品牌、链接、CTA 边框
- **Pure White**(`#ffffff`):主亮面
- **Near Black**(`#0a0b0d`):文本、暗区背景
- **Cool Gray Surface**(`#eef0f3`):次级按钮背景

### 交互
- **Hover Blue**(`#578bfa`):按钮悬浮背景
- **Link Blue**(`#0667d0`):次级链接色
- **Muted Blue**(`#5b616e`):边框色,20% 不透明度

### 表面
- **Dark Card**(`#282b31`):暗色按钮 / 卡片背景
- **Light Surface**(`rgba(247,247,247,0.88)`):微妙表面

## 3. 排版规则

### 字族
- **Display**:`CoinbaseDisplay` —— 主视觉标题
- **UI / Sans**:`CoinbaseSans` —— 按钮、标题、导航
- **正文**:`CoinbaseText` —— 阅读文本
- **图标**:`CoinbaseIcons` —— 图标字体

### 层级

| 角色 | 字体 | 字号 | 字重 | 行高 | 备注 |
|------|------|------|--------|-------------|-------|
| 显示级主标 | CoinbaseDisplay | 80px | 400 | 1.00(紧) | 最大冲击力 |
| 显示级次标 | CoinbaseDisplay | 64px | 400 | 1.00 | 副主标 |
| 显示级三级 | CoinbaseDisplay | 52px | 400 | 1.00 | 第三档 |
| 区块标题 | CoinbaseSans | 36px | 400 | 1.11(紧) | 功能区 |
| 卡片标题 | CoinbaseSans | 32px | 400 | 1.13 | 卡片标题 |
| 功能标题 | CoinbaseSans | 18px | 600 | 1.33 | 功能强调 |
| 正文粗 | CoinbaseSans | 16px | 700 | 1.50 | 强正文 |
| 正文半粗 | CoinbaseSans | 16px | 600 | 1.25 | 按钮、导航 |
| 正文 | CoinbaseText | 18px | 400 | 1.56 | 标准阅读 |
| 小号正文 | CoinbaseText | 16px | 400 | 1.50 | 次级阅读 |
| 按钮 | CoinbaseSans | 16px | 600 | 1.20 | +0.16px 字距 |
| 说明文字 | CoinbaseSans | 14px | 600–700 | 1.50 | 元数据 |
| 小号 | CoinbaseSans | 13px | 600 | 1.23 | 标签 |

## 4. 组件样式

### 按钮

**主药丸(56px 圆角)**
- 背景:`#eef0f3` 或 `#282b31`
- 圆角:56px
- 边框:`1px solid`,与背景同色
- 悬浮:`#578bfa`(浅蓝)
- 焦点:`2px solid black` 描边

**全药丸(100000px 圆角)**
- 用于最大药丸形状

**蓝边框**
- 边框:`1px solid #0052ff`
- 背景:透明

### 卡片与容器
- 圆角:8px–40px 区间
- 边框:`1px solid rgba(91,97,110,0.2)`

## 5. 布局原则

### 间距系统
- 基数:8px
- 刻度:1px, 3px, 4px, 5px, 6px, 8px, 10px, 12px, 15px, 16px, 20px, 24px, 25px, 32px, 48px

### 圆角刻度
- 小(4px–8px):文章链接、小卡片
- 标准(12px–16px):卡片、菜单
- 大(24px–32px):功能容器
- XL(40px):大按钮 / 容器
- 药丸(56px):主 CTA
- 全(100000px):最大药丸

## 6. 深度与海拔

极简阴影系统 —— 深度来自暗 / 亮区块之间的色彩对比。

## 7. Do's and Don'ts

### Do
- 主交互元素用 Coinbase Blue(#0052ff)
- 所有 CTA 按钮都用 56px 圆角
- CoinbaseDisplay 只用于主视觉标题
- 暗区(#0a0b0d)与白区交替

### Don't
- 不把蓝色做装饰 —— 它只做功能
- CTA 不用尖角 —— 最少 56px

## 8. 响应式

断点:400px, 576px, 640px, 768px, 896px, 1280px, 1440px, 1600px

## 9. Agent Prompt Guide

### 快速取色参考
- 品牌:Coinbase Blue(`#0052ff`)
- 背景:白(`#ffffff`)
- 暗表面:`#0a0b0d`
- 次级表面:`#eef0f3`
- 悬浮:`#578bfa`
- 文本:`#0a0b0d`

### 组件提示词示例
- "创建 hero:白色背景。CoinbaseDisplay 80px,行高 1.00。药丸 CTA(#eef0f3,56px 圆角)。悬浮:#578bfa。"
- "搭建暗区:#0a0b0d 背景。CoinbaseDisplay 64px 白字。蓝色强调链接(#0052ff)。"
