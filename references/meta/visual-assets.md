# 视觉资产策略 —— 图片 / Logo / 截图的优先级瀑布

> 规范层。定义页面图片资产的四级优先级与硬禁令。"极简站也需要 2-3 张真图"——纯文字排版页面是 AI 产出 uninspired 的头号信号之一。来源：taste-skill §4.8/§9.E，2026-09 吸收。

## 图片来源四级优先级（从上到下取，级级降级须留痕）

| 级 | 来源 | 适用 | 注意 |
| --- | --- | --- | --- |
| 1 | **图像生成工具**（ip 子命令 / text_to_image API） | 有明确情绪与主题要求的场合 | prompt 写主题不写"abstract tech background" |
| 2 | **带语义 seed 的 picsum**（`https://picsum.photos/seed/<语义词>/<w>/<h>`） | 快速原型、占位 | seed 用语义词（`seed/forest-lab/800/600`），禁 `?random` |
| 3 | **真实来源图**（用户素材 / 官方 asset / 已授权图库） | 品牌页、证言、Logo 墙 | 记录来源；禁止热链未授权 CDN |
| 4 | **显式占位槽**：输出 `<img>` 槽 + 尺寸/比例/内容说明，并告知用户"待替换" | 无法安全取图时 | 禁止静默留空或用灰色 div 顶替 |

## 硬禁令

1. **禁止 div 拼假截图**——用嵌套 div/渐变/文字模拟"产品截图"是头号 AI 破绽。要么用真实截图素材，要么出占位槽 + 说明。
2. **禁止 `?random` 随机图**——每次渲染都换图，preview 不可复现。
3. **Logo 墙必须真 SVG**：优先 Simple Icons / devicon 官方源；虚构品牌则配自造 SVG 字标（几何标记即可，禁止文字假装 logo）。
4. **LOGO-ONLY 规则**：Logo 墙下方禁止配"Trusted by 1000+ teams"式品类说明文字凑数。

## 数量基线

| 页面模式（surface-modes） | 真图基线 |
| --- | --- |
| Experience / Persuade | ≥ 2-3 张（首屏至少 1 张主视觉） |
| Operate | 0-1 张（图标即可，不强求） |
| Read | 0-2 张（配图须承载信息） |

## 空态插画策略

> 落地 [`vocabulary/states.md`](../vocabulary/states.md) 的空态模式引用；取图来源仍走上文四级优先级。

- **首用空态**（states.md 的 `state-empty-first-use` / `state-empty-starter`）：可用插画或示例数据传达"这里将出现什么"，插画承载正向情绪引导。
- **无结果空态**（`state-empty-no-results` / `state-empty-clear-filters`）：优先**文字 + 筛选调整建议**，而非插画——用户要的是出路不是装饰；确需配图时从简。
- **错误态**（`state-error-*` / `state-offline`）：**禁装饰插画**；仅允许功能性示意（断网/锁形图标），重心放在重试动作与已保留数据。

## 与其他规范联动

- [`ai-tells.md`](ai-tells.md) §5（Unsplash ?random 占位）执行本文件优先级 2/4 的替代方案。
- [`vocabulary/galleries.md`](../vocabulary/galleries.md)：所有图片必须设 `width`+`height` 或 `aspect-ratio`（CLS，见 performance.md）。
- preview 自检项：页面真图 ≥ 基线，或存在显式占位槽与替换说明。
