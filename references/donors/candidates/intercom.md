<!-- 供体候选池快照(中文译本,非蒸馏供体)。
     站点分组: 设计与生产力(design) · 站点摘要: 客户消息。友好的蓝色色板,对话式 UI 模式
     站点色板: #faf9f6, #111111, #ffffff, #ff5600, #dedbd6, #7b7b78
     晋升正式供体须满足 ../README.md §5 三条件;蒸馏稿另立 ../<id>.md,与本快照并存。 -->

# 设计系统:Intercom

## 1. 视觉主题与氛围

Intercom 的网站是一个温暖、自信的客户服务平台,用干净、编辑式的设计语言传达"AI 优先的 helpdesk"。页面运行在暖调米白画布(`#faf9f6`)上,配近黑(`#111111`)文字,营造亲密、杂志般的阅读体验。签名色 Fin Orange(`#ff5600`)——以 Intercom 的 AI agent 命名——是温暖中性色板上唯一的鲜艳强调。

排版用 Saans——一款自定义几何无衬线字体,配激进的负字距(80px 下 -2.4px,24px 下 -0.48px),所有标题字号统一 1.00 行高。这形成极度压缩、广告牌般的大标题,感觉像被工程化过、精确。Serrif 提供编辑场景用的衬线搭档,SaansMono 处理代码与大写技术标签。MediumLL 与 LLMedium 出现在特定 UI 语境,构成一个丰富的五字体生态。

Intercom 的辨识点在异常锐利的几何——按钮 4px 圆角形成近矩形的交互元素,感觉工业、精确,与温暖的表面色形成对比。按钮 hover 态用 `scale(1.1)` 放大,制造物理性的"生长"交互。边框系统用暖燕麦色调(`#dedbd6`)与基于 oklab 的不透明度值,做精细的颜色管理。

**关键特征:**
- 暖调米白画布(`#faf9f6`)配燕麦色边框(`#dedbd6`)
- Saans 字体配极端负字距(80px 下 -2.4px)与 1.00 行高
- Fin Orange(`#ff5600`)作唯一品牌强调
- 锐利 4px 圆角——近矩形的按钮与元素
- hover scale(1.1) 配激活 scale(0.85)——物理性按钮交互
- SaansMono 大写标签配宽字距(0.6px–1.2px)
- 丰富的多色报表色板(蓝、绿、红、粉、青柠、橙)
- oklab 色值做精细的不透明度管理

## 2. 色板与角色

### 主色
- **Off Black**(`#111111`):`--color-off-black`,主文本、按钮背景
- **Pure White**(`#ffffff`):`--wsc-color-content-primary`,主表面
- **Warm Cream**(`#faf9f6`):按钮背景、卡片表面
- **Fin Orange**(`#ff5600`):`--color-fin`,主品牌强调
- **Report Orange**(`#fe4c02`):`--color-report-orange`,数据可视化

### 报表色板
- **Report Blue**(`#65b5ff`):`--color-report-blue`
- **Report Green**(`#0bdf50`):`--color-report-green`
- **Report Red**(`#c41c1c`):`--color-report-red`
- **Report Pink**(`#ff2067`):`--color-report-pink`
- **Report Lime**(`#b3e01c`):`--color-report-lime-300`
- **Green**(`#00da00`):`--color-green`
- **Deep Blue**(`#0007cb`):深蓝强调

### 中性色阶(暖调)
- **Black 80**(`#313130`):`--wsc-color-black-80`,深中性
- **Black 60**(`#626260`):`--wsc-color-black-60`,中中性
- **Black 50**(`#7b7b78`):`--wsc-color-black-50`,弱化文本
- **Content Tertiary**(`#9c9fa5`):`--wsc-color-content-tertiary`
- **Oat Border**(`#dedbd6`):暖色边框
- **Warm Sand**(`#d3cec6`):浅暖中性

## 3. 排版规则

### 字族
- **主字族**:`Saans`,回退:`Saans Fallback, ui-sans-serif, system-ui`
- **衬线**:`Serrif`,回退:`Serrif Fallback, ui-serif, Georgia`
- **等宽**:`SaansMono`,回退:`SaansMono Fallback, ui-monospace`
- **UI**:`MediumLL` / `LLMedium`,回退:`system-ui, -apple-system`

### 层级

| 角色 | 字体 | 字号 | 字重 | 行高 | 字距 |
|------|------|------|--------|-------------|----------------|
| 显示级 hero | Saans | 80px | 400 | 1.00(紧) | -2.4px |
| 区块标题 | Saans | 54px | 400 | 1.00 | -1.6px |
| 子标题 | Saans | 40px | 400 | 1.00 | -1.2px |
| 卡片标题 | Saans | 32px | 400 | 1.00 | -0.96px |
| 特性标题 | Saans | 24px | 400 | 1.00 | -0.48px |
| 正文强调 | Saans | 20px | 400 | 0.95 | -0.2px |
| 导航 / UI | Saans | 18px | 400 | 1.00 | normal |
| 正文 | Saans | 16px | 400 | 1.50 | normal |
| 细体正文 | Saans | 14px | 300 | 1.40 | normal |
| 按钮 | Saans | 16px / 14px | 400 | 1.50 / 1.43 | normal |
| 加粗按钮 | LLMedium | 16px | 700 | 1.20 | 0.16px |
| 衬线正文 | Serrif | 16px | 300 | 1.40 | -0.16px |
| 等宽标签 | SaansMono | 12px | 400–500 | 1.00–1.30 | 0.6px–1.2px uppercase |

## 4. 组件样式

### 按钮

**深色主按钮**
- 背景:`#111111`
- 文字:`#ffffff`
- padding:0px 14px
- 圆角:4px
- hover:白底、深色文字、scale(1.1)
- 激活:绿底(`#2c6415`)、scale(0.85)

**描边按钮**
- 背景:透明
- 文字:`#111111`
- 边框:`1px solid #111111`
- 圆角:4px
- hover/激活缩放行为相同

**暖色卡片按钮**
- 背景:`#faf9f6`
- 文字:`#111111`
- padding:16px
- 边框:`1px solid oklab(... / 0.1)`

### 卡片与容器
- 背景:`#faf9f6`(暖米白)
- 边框:`1px solid #dedbd6`(暖燕麦)
- 圆角:8px
- 无可见阴影

### 导航
- 链接用 Saans 16px
- 白底近黑文字
- 小号 4px–6px 圆角按钮
- AI 特性用橙色 Fin 强调

## 5. 布局原则

### 间距:8px, 10px, 12px, 14px, 16px, 20px, 24px, 32px, 40px, 48px, 60px, 64px, 80px, 96px
### 圆角:4px(按钮)、6px(导航项)、8px(卡片、容器)

## 6. 深度与海拔
阴影极简。深度靠暖色边框与表面浅调表达。

## 7. Do's and Don'ts

### Do
- Saans 配 1.00 行高,所有标题用负字距
- 按钮用 4px 圆角——锐利几何就是身份
- Fin Orange(#ff5600)只用于 AI/品牌强调
- 按钮 hover 用 scale(1.1)
- 用暖中性色(#faf9f6、#dedbd6)

### Don't
- 不要把按钮圆角做到 4px 以上
- 不要装饰性地使用 Fin Orange
- 不要用冷灰边框——永远用暖燕麦色调
- 不要在标题上跳过负字距

## 8. 响应式
断点:425px, 530px, 600px, 640px, 768px, 896px

## 9. Agent Prompt Guide

### 快速取色参考
- 文字:Off Black(`#111111`)
- 背景:Warm Cream(`#faf9f6`)
- 强调:Fin Orange(`#ff5600`)
- 边框:Oat(`#dedbd6`)
- 弱化:`#7b7b78`

### 组件提示词示例
- "做 hero:暖米白(#faf9f6)背景。Saans 80px 字重 400,行高 1.00,字距 -2.4px,#111111。深色按钮(#111111,4px 圆角)。hover:scale(1.1),白色背景。"
