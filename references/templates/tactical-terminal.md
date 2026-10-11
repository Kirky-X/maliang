---
name: tactical-terminal
title: 战术遥测终端
source: 社区范式 industrial-brutalist-ui（外部 skill，license 未考——思想内化，本文措辞为本仓库自著）
era: 复古军工终端 / HUD 美学，2020s Web 复兴
category: design-language
status: style        # production | style | experimental
variance: 7-10          # dials VARIANCE 适配区间
motion: 1-3          # dials MOTION 适配区间
density: 7-10          # dials DENSITY 适配区间
platforms: Web（监控大屏 / 遥测仪表盘 / 军工风作品集）
verified: 2026-10-11
---
# 战术遥测终端（Tactical Telemetry & CRT Terminal）

> 密闭暗色终端世界：机密军工数据库、 legacy 主机与航空航天 HUD 的界面语言。单色白磷光 + 唯一航空红 accent + mono 全 dominance + 模拟硬件退化（扫描线/抖动/噪点）。与 [`editorial-swiss.md`](editorial-swiss.md) 同源于工业印刷传统但**互斥**：brief 偏亮色印刷纸张感 → 用 editorial-swiss；brief 明确是暗色遥测/监控/军工场景 → 用本模板。**一个项目只选一个基底，不混亮暗两套。**

## 一句话

把界面做成一台还在运行的军用 CRT 设备：数据是主角，chrome 是机械框架，一切装饰都长成硬件限制的样子。

## 色板（选一套，全站锁死）

| 角色 | 值 | 用法 |
| --- | --- | --- |
| 底色 | `#0A0A0A` / `#121212` | 熄灭的 CRT，不用纯黑 `#000` |
| 前景 | `#EAEAEA` | 白磷光，正文主色 |
| 唯一 accent | `#E61919` / `#FF2A2A` | 航空红：告警、粗结构分割线、关键数据高亮 |
| 终端绿（可选） | `#4AF626` | 仅限**一个**元素（单个状态灯或单个读数）；无明确用途就不放 |

禁：渐变、软投影、现代半透明毛玻璃。颜色只模拟物理介质或原始发光体。

## 排版双轨

| 轨 | 字族 | 参数 |
| --- | --- | --- |
| 宏排版（结构标题） | 重型无衬线（Archivo Black / Inter Black 档） | `clamp(4rem, 10vw, 15rem)` 流式巨字；字距 `-0.03em ~ -0.06em`；行高 `0.85-0.95`；全大写 |
| 微排版（数据遥测） | mono（JetBrains Mono / IBM Plex Mono 档） | `10-14px` 固定小字；字距 `0.05-0.1em` 模拟打字机；行高 `1.2-1.4`；全大写，用于全部元数据/导航/单位编号 |

反差即结构：宏排版做视觉主角，微排版做信息织体，中间几乎没有过渡档。高对比衬线只可极少量点缀，且必须做退化处理（halftone/1-bit 抖动）破坏矢量完美感——见 [`effects-degradation.md`](../dimensions/effects-degradation.md)。

## 布局工程

- **蓝图网格**：CSS Grid 锚定，元素不浮动、贴轨道与交点；`display: grid; gap: 1px` + 父子底色反差生成无 border 的数学分割线。
- **可见分格**：`1px/2px solid` 实线划分信息区，`<hr>` 横贯容器分隔操作单元。
- **双峰密度**：mono 元数据高密度簇集 与 巨字四周的大计算留白 交替，不做均匀中密度。
- **零圆角**：所有直角 90°，拒绝 `border-radius`。

## ASCII 符号系统（chrome 即语义）

- 框选：`[ DELIVERY SYSTEMS ]`、`< RE-IND >` 式 ASCII 括号做节标签
- 方向：`>>>`、`///` 做流向指示
- 交点：`+` 准星标网格交点；重复竖线段做条码带；粗横纹做警戒条
- 过程感：`REV 2.6`、`UNIT / D-01` 式短随机串模拟活动机械流程（数据必须是真占位结构，不冒充真状态，见 [`../meta/ai-tells.md`](../meta/ai-tells.md) 伪系统标记条目）
- 语义标签用 `<data>` `<samp>` `<kbd>` `<output>` `<dl>` 承载遥测内容

## 翻车点

- 绿色失控：终端绿一旦扩散到第二个元素，军工感立刻塌成赛博朋克霓虹——只留一个。
- 红色滥用：航空红是告警语义，铺开做通用强调就失去信号价值。
- 密度单峰：全程高密没有留白呼吸，或全程留白没有数据簇，都丢「设备感」。
- 纹理过量：扫描线/噪点/抖动全上且高不透明度 = 廉价 CRT 滤镜合集；退化效果各自 opacity 压低（见 [`effects-degradation.md`](../dimensions/effects-degradation.md) 的降级与性能前提）。
- 伪遥测：编造假运行状态冒充真实数据，触发 [`ai-tells.md`](../meta/ai-tells.md) §10 假产品预览/伪系统标记禁令。
