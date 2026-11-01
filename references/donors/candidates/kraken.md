<!-- 供体候选池快照(中文译本,非蒸馏供体;原文见「原始出处」)。
     站点分组: 金融与加密(finance) · 站点摘要: 加密交易平台。紫色强调的暗色 UI、数据密集的仪表板
     站点色板: #101114, #7132f5, #5741d8, #686b82, #9497a9, #dedee5
     晋升正式供体须满足 ../README.md §5 三条件;蒸馏稿另立 ../<id>.md,与本快照并存。 -->

# 设计系统:Kraken

## 1. 视觉主题与氛围

Kraken 的网站是一个干净、可信赖的加密交易所,用紫色作为统辖性的品牌色。设计运行在白色背景上,由 Kraken Purple(`#7132f5`、`#5741d8`、`#5b1ecf`)造出鲜明、专业的加密身份。自有字体 Kraken-Brand 以粗体(700)字重与负字距处理显示级标题,Kraken-Product(回退 IBM Plex Sans)则充当 UI 的主力字体。

**关键特征:**
- Kraken Purple(`#7132f5`)作主品牌,配深色变体(`#5741d8`、`#5b1ecf`)
- Kraken-Brand(显示)+ Kraken-Product(UI)双字体系统
- 近黑(`#101114`)文字配冷蓝灰中性色阶
- 12px 圆角按钮(圆但不做药丸)
- 微妙阴影(`rgba(0,0,0,0.03) 0px 4px 24px`)——耳语级
- 绿色强调(`#149e61`)用于正向/成功态

## 2. 色板与角色

### 主色
- **Kraken Purple**(`#7132f5`):主 CTA、品牌强调、链接
- **Purple Dark**(`#5741d8`):按钮边框、描边变体
- **Purple Deep**(`#5b1ecf`):最深的紫
- **Purple Subtle**(`rgba(133,91,251,0.16)`):16% 的紫——微妙的按钮背景
- **Near Black**(`#101114`):主文本

### 中性色阶
- **Cool Gray**(`#686b82`):主中性色,边框用 24% 不透明度
- **Silver Blue**(`#9497a9`):次文本、弱化元素
- **White**(`#ffffff`):主表面
- **Border Gray**(`#dedee5`):分割线边框

### 语义
- **Green**(`#149e61`):成功/正向,徽章用 16% 不透明度
- **Green Dark**(`#026b3f`):徽章文字

## 3. 排版规则

### 字族
- **显示**:`Kraken-Brand`,回退:`IBM Plex Sans, Helvetica, Arial`
- **UI / 正文**:`Kraken-Product`,回退:`Helvetica Neue, Helvetica, Arial`

### 层级

| 角色 | 字体 | 字号 | 字重 | 行高 | 字距 |
|------|------|------|--------|-------------|----------------|
| 显示 Hero | Kraken-Brand | 48px | 700 | 1.17 | -1px |
| 区块标题 | Kraken-Brand | 36px | 700 | 1.22 | -0.5px |
| 子标题 | Kraken-Brand | 28px | 700 | 1.29 | -0.5px |
| 功能标题 | Kraken-Product | 22px | 600 | 1.20 | normal |
| 正文 | Kraken-Product | 16px | 400 | 1.38 | normal |
| 正文中等 | Kraken-Product | 16px | 500 | 1.38 | normal |
| 按钮 | Kraken-Product | 16px | 500–600 | 1.38 | normal |
| 说明文字 | Kraken-Product | 14px | 400–700 | 1.43–1.71 | normal |
| 小号 | Kraken-Product | 12px | 400–500 | 1.33 | normal |
| 微字 | Kraken-Product | 7px | 500 | 1.00 | uppercase |

## 4. 组件样式

### 按钮

**主紫色**
- 背景:`#7132f5`
- 文字:`#ffffff`
- padding:13px 16px
- 圆角:12px

**紫色描边**
- 背景:`#ffffff`
- 文字:`#5741d8`
- 边框:`1px solid #5741d8`
- 圆角:12px

**紫色弱化**
- 背景:`rgba(133,91,251,0.16)`
- 文字:`#7132f5`
- padding:8px
- 圆角:12px

**白色按钮**
- 背景:`#ffffff`
- 文字:`#101114`
- 圆角:10px
- 阴影:`rgba(0,0,0,0.03) 0px 4px 24px`

**次级灰**
- 背景:`rgba(148,151,169,0.08)`
- 文字:`#101114`
- 圆角:12px

### 徽章
- 成功:`rgba(20,158,97,0.16)` 底、`#026b3f` 文字、6px 圆角
- 中性:`rgba(104,107,130,0.12)` 底、`#484b5e` 文字、8px 圆角

## 5. 布局原则

### 间距:1px, 2px, 3px, 4px, 5px, 6px, 8px, 10px, 12px, 13px, 15px, 16px, 20px, 24px, 25px
### 圆角:3px, 6px, 8px, 10px, 12px, 16px, 9999px, 50%

## 6. 深度与海拔
- 微妙:`rgba(0,0,0,0.03) 0px 4px 24px`
- 微:`rgba(16,24,40,0.04) 0px 1px 4px`

## 7. Do's and Don'ts

### Do
- CTA 与链接用 Kraken Purple(#7132f5)
- 所有按钮统一 12px 圆角
- 标题用 Kraken-Brand,正文用 Kraken-Product

### Don't
- 不用药丸按钮——12px 是按钮圆角的上限
- 不用定义色阶之外的紫色

## 8. 响应式
断点:375px, 425px, 640px, 768px, 1024px, 1280px, 1536px

## 9. Agent Prompt Guide

### 快速取色参考
- 品牌:Kraken Purple(`#7132f5`)
- 深色变体:`#5741d8`
- 文本:Near Black(`#101114`)
- 次文本:`#9497a9`
- 背景:White(`#ffffff`)

### 组件提示词示例
- "创建 hero:白色背景。Kraken-Brand 48px 字重 700,字距 -1px。紫色 CTA(#7132f5,12px 圆角,13px 16px padding)。"
