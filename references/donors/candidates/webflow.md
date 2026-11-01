<!-- 供体候选池快照(中文译本,非蒸馏供体)。
     站点分组: 设计与生产力(design) · 站点摘要: 可视化网站搭建器。蓝色强调、精致的营销站审美
     站点色板: #080808, #146ef5, #3b89ff, #7a3dff, #ed52cb, #00d722
     晋升正式供体须满足 ../README.md §5 三条件;蒸馏稿另立 ../<id>.md,与本快照并存。 -->

# 设计系统:Webflow

## 1. 视觉主题与氛围

Webflow 的网站是一个视觉丰富、工具导向的平台,用干净的白表面、签名 Webflow 蓝(`#146ef5`)与丰富的次级色板(紫、粉、绿、橙、黄、红)传达"无代码设计"。自建 WF Visual Sans Variable 字体造出自信、精确的排版体系,显示级用 600 字重,正文用 500。

**关键特征:**
- 白画布配近黑(`#080808`)文字
- Webflow 蓝(`#146ef5`)作主品牌色与交互色
- WF Visual Sans Variable——自建可变字体,字重 500–600
- 丰富次级色板:紫 `#7a3dff`、粉 `#ed52cb`、绿 `#00d722`、橙 `#ff6b00`、黄 `#ffae13`、红 `#ee1d36`
- 保守的 4px–8px 圆角——锐利,不圆
- 多层阴影栈(5 层级联阴影)
- 全大写标签:10px–15px,字重 500–600,宽字距(0.6px–1.5px)
- 按钮 hover 时 translate(6px)

## 2. 色板与角色

### 主色
- **近黑**(`#080808`):主文本
- **Webflow 蓝**(`#146ef5`):`--_color---primary--webflow-blue`,主 CTA 与链接
- **蓝 400**(`#3b89ff`):`--_color---primary--blue-400`,更浅的交互蓝
- **蓝 300**(`#006acc`):`--_color---blue-300`,更深的蓝变体
- **按钮 hover 蓝**(`#0055d4`):`--mkto-embed-color-button-hover`

### 次级强调
- **紫**(`#7a3dff`):`--_color---secondary--purple`
- **粉**(`#ed52cb`):`--_color---secondary--pink`
- **绿**(`#00d722`):`--_color---secondary--green`
- **橙**(`#ff6b00`):`--_color---secondary--orange`
- **黄**(`#ffae13`):`--_color---secondary--yellow`
- **红**(`#ee1d36`):`--_color---secondary--red`

### 中性色
- **灰 800**(`#222222`):暗色次级文本
- **灰 700**(`#363636`):中段文本
- **灰 300**(`#ababab`):哑色文本、占位
- **中灰**(`#5a5a5a`):链接文字
- **边框灰**(`#d8d8d8`):边框、分隔线
- **边框 hover**(`#898989`):hover 边框

### 阴影
- **5 层级联**:`rgba(0,0,0,0) 0px 84px 24px, rgba(0,0,0,0.01) 0px 54px 22px, rgba(0,0,0,0.04) 0px 30px 18px, rgba(0,0,0,0.08) 0px 13px 13px, rgba(0,0,0,0.09) 0px 3px 7px`

## 3. 排版规则

### 字体:`WF Visual Sans Variable`,回退:`Arial`

| 角色 | 字号 | 字重 | 行高 | 字距 | 备注 |
|------|------|--------|-------------|----------------|-------|
| 显示 Hero | 80px | 600 | 1.04 | -0.8px | |
| 区块标题 | 56px | 600 | 1.04 | normal | |
| 子标题 | 32px | 500 | 1.30 | normal | |
| Feature 标题 | 24px | 500–600 | 1.30 | normal | |
| 正文 | 20px | 400–500 | 1.40–1.50 | normal | |
| 正文标准 | 16px | 400–500 | 1.60 | -0.16px | |
| 按钮 | 16px | 500 | 1.60 | -0.16px | |
| 全大写标签 | 15px | 500 | 1.30 | 1.5px | uppercase |
| 说明 | 14px | 400–500 | 1.40–1.60 | normal | |
| 徽章大写 | 12.8px | 550 | 1.20 | normal | uppercase |
| 微型大写 | 10px | 500–600 | 1.30 | 1px | uppercase |
| 代码:Inconsolata(配套等宽字体)

## 4. 组件样式

### 按钮
- 透明:文字 `#080808`,hover 时 translate(6px)
- 白色圆形:50% 圆角,白底
- 蓝色徽章:`#146ef5` 底,4px 圆角,字重 550

### 卡片:`1px solid #d8d8d8`,4px–8px 圆角
### 徽章:蓝调背景 10% 不透明度,4px 圆角

## 5. 布局
- 间距:分数刻度(1px, 2.4px, 3.2px, 4px, 5.6px, 6px, 7.2px, 8px, 9.6px, 12px, 16px, 24px)
- 圆角:2px, 4px, 8px, 50%——保守、锐利
- 断点:479px, 768px, 992px

## 6. 深度:5 层级联阴影系统

## 7. Do's and Don'ts
- Do: 用 WF Visual Sans Variable,字重 500–600。CTA 用蓝色(#146ef5)。4px 圆角。hover 用 translate(6px)。
- Don't: 功能元素圆角超过 8px。主 CTA 上用次级色。

## 8. 响应式:479px, 768px, 992px

## 9. Agent Prompt Guide
- 文本:近黑(`#080808`)
- CTA:Webflow 蓝(`#146ef5`)
- 背景:白(`#ffffff`)
- 边框:`#d8d8d8`
- 次级:紫 `#7a3dff`、粉 `#ed52cb`、绿 `#00d722`
