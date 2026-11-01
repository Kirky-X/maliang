<!-- 供体候选池快照(中文译本,非蒸馏供体)。
     站点分组: 设计与生产力(design) · 站点摘要: 视觉协作。明黄强调色,无限画布美学。
     站点色板: #1c1c1e, #5b76fe, #2a41b6, #00b473, #ffc6c6, #600000
     晋升正式供体须满足 ../README.md §5 三条件;蒸馏稿另立 ../<id>.md,与本快照并存。 -->

# 设计系统:Miro

## 1. 视觉主题与氛围

Miro 的网站是一个干净、以协作工具为先的平台,用宽裕留白、粉彩强调色与一款自信的几何字体传达"视觉思考"。设计以白色画布为主,配近黑文本(`#1c1c1e`)与一套辨识度高的粉彩色板——珊瑚、玫瑰、青绿、橙、黄、苔绿——每种颜色代表不同的协作语境。

排版用 Roobert PRO Medium 作主显示字族,带 OpenType 字符变体(`"blwf", "cv03", "cv04", "cv09", "cv11"`)与负字距(56px 时 -1.68px)。Noto Sans 承担正文,用它自己的样式集(`"liga" 0, "ss01", "ss04", "ss05"`)。该设计用 Framer 构建,因此有平滑动画与现代组件模式。

**关键特征:**
- 白色画布,配近黑(`#1c1c1e`)文本
- Roobert PRO Medium 带多个 OpenType 字符变体
- 粉彩强调色板:珊瑚、玫瑰、青绿、橙、黄、苔绿(浅 + 深成对)
- Blue 450(`#5b76fe`)作主交互色
- 成功绿(`#00b473`)用于正向状态
- 宽裕圆角:8px–50px 区间
- Framer 构建,平滑动效模式
- 环状阴影边框:`rgb(224,226,232) 0px 0px 0px 1px`

## 2. 色板与角色

### 主色
- **Near Black**(`#1c1c1e`):主文本
- **White**(`#ffffff`):`--tw-color-white`,主表面
- **Blue 450**(`#5b76fe`):`--tw-color-blue-450`,主交互色
- **Actionable Pressed**(`#2a41b6`):`--tw-color-actionable-pressed`

### 粉彩强调(浅/深成对)
- **Coral**:浅 `#ffc6c6` / 深 `#600000`
- **Rose**:浅 `#ffd8f4` / 深(隐含)
- **Teal**:浅 `#c3faf5` / 深 `#187574`
- **Orange**:浅 `#ffe6cd`
- **Yellow**:深 `#746019`
- **Moss**:深 `#187574`
- **Pink**(`#fde0f0`):柔和粉表面
- **Red**(`#fbd4d4`):浅红表面
- **Dark Red**(`#e3c5c5`):弱化红

### 语义色
- **Success**(`#00b473`):`--tw-color-success-accent`

### 中性
- **Slate**(`#555a6a`):次文本
- **Input Placeholder**(`#a5a8b5`):`--tw-color-input-placeholder`
- **Border**(`#c7cad5`):按钮边框
- **Ring**(`rgb(224,226,232)`):阴影当边框

## 3. 排版规则

### 字族
- **显示**:`Roobert PRO Medium`,回退:占位——`"blwf", "cv03", "cv04", "cv09", "cv11"`
- **显示变体**:`Roobert PRO SemiBold`、`Roobert PRO SemiBold Italic`、`Roobert PRO`
- **正文**:`Noto Sans`——`"liga" 0, "ss01", "ss04", "ss05"`

### 层级

| 角色 | 字体 | 字号 | 字重 | 行高 | 字距 |
|------|------|------|--------|-------------|----------------|
| 显示级 Hero | Roobert PRO Medium | 56px | 400 | 1.15 | -1.68px |
| 区块标题 | Roobert PRO Medium | 48px | 400 | 1.15 | -1.44px |
| 卡片标题 | Roobert PRO Medium | 24px | 400 | 1.15 | -0.72px |
| 副标题 | Noto Sans | 22px | 400 | 1.35 | -0.44px |
| 功能 | Roobert PRO Medium | 18px | 600 | 1.35 | normal |
| 正文 | Noto Sans | 18px | 400 | 1.45 | normal |
| 标准正文 | Noto Sans | 16px | 400–600 | 1.50 | -0.16px |
| 按钮 | Roobert PRO Medium | 17.5px | 700 | 1.29 | 0.175px |
| 说明文字 | Roobert PRO Medium | 14px | 400 | 1.71 | normal |
| 小字 | Roobert PRO Medium | 12px | 400 | 1.15 | -0.36px |
| 微型大写 | Roobert PRO | 10.5px | 400 | 0.90 | uppercase |

## 4. 组件样式

### 按钮
- 描边:透明底、`1px solid #c7cad5`、8px 圆角、7px 12px padding
- 白色圆形:50% 圆角、白底带阴影
- 蓝色主按钮(由交互色推断)

### 卡片:12px–24px 圆角、粉彩背景
### 输入框:白底、`1px solid #e9eaef`、8px 圆角、16px padding

## 5. 布局原则
- 间距:1–24px 基础刻度
- 圆角:8px(按钮)、10px–12px(卡片)、20px–24px(面板)、40px–50px(大容器)
- 环状阴影:`rgb(224,226,232) 0px 0px 0px 1px`

## 6. 深度与海拔
极简——环状阴影加粉彩表面反差

## 7. Do's and Don'ts
### Do
- 功能区块用粉彩浅/深成对
- Roobert PRO 配 OpenType 字符变体使用
- 交互元素用 Blue 450(#5b76fe)
### Don't
- 不要用重阴影
- 不要在同一区块里混用超过 2 个粉彩强调色

## 8. 响应式
断点:425px, 576px, 768px, 896px, 1024px, 1200px, 1280px, 1366px, 1700px, 1920px

## 9. Agent Prompt Guide
### 快速取色参考
- 文本:Near Black(`#1c1c1e`)
- 背景:White(`#ffffff`)
- 交互:Blue 450(`#5b76fe`)
- 成功:`#00b473`
- 边框:`#c7cad5`
### 组件提示词示例
- "做 hero:白色背景。Roobert PRO Medium 56px,行高 1.15,字距 -1.68px。蓝色 CTA(#5b76fe)。描边次级按钮(1px solid #c7cad5,8px 圆角)。"
