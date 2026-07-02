# Hero 模式命名词汇

> 模式词汇库。为 draw-md 阶段的 Hero 区域提供标准化命名,避免 LLM 用泛化词(如 "顶部大图")描述,产出可直接对应代码的模式名。来源:taste-skill。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `hero-centered`       | 居中文案 + CTA,无图或背景图淡出                  | 营销首页、SaaS 主页、产品发布         |
| `hero-split`          | 左文案 + 右视觉(图 / 视频 / 产品截图)          | 产品页、功能介绍、电商首页            |
| `hero-fullscreen`     | 全屏图 / 视频 + 浮层文字                          | 品牌站、作品集、影视媒体              |
| `hero-kenburns`       | 全屏图 + Ken Burns 缓慢缩放                       | 品牌、影视、摄影集                    |
| `hero-parallax`       | 多层视差,滚动时背景 / 中景 / 前景速率不同        | 品牌叙事、产品发布                    |
| `hero-canvas`         | WebGL / Canvas 动态背景(粒子 / 流体)            | 科技品牌、3D 交互、创意工具           |
| `hero-illustration`   | 插画为主,文字辅助                                | 健康 / 教育 / 冥想类 App              |
| `hero-card-stack`     | 卡片堆叠 + 滚动揭示(配合 sticky-stack 骨架)     | 产品功能介绍、案例展示                |
| `hero-video-loop`     | 短视频循环 + 文字浮层                             | 消费品、产品演示、IP 落地页           |
| `hero-text-only`      | 纯文字 + 排版,无图                               | 设计师作品集、极简品牌、文档站        |

## 使用规则

- draw-md 输出时,Hero 章节必须标注一个模式名,不接受"顶部"等泛化描述
- 模式名与 [`motion-skeletons/`](../motion-skeletons/) 联动:`hero-parallax` 必须配 sticky-stack 或 scroll-reveal-stagger
- 同一站点跨页 Hero 模式 ≤ 2 种(避免混乱)
- 触发 [`ai-tells.md`](../meta/ai-tells.md) 第 1 节"紫蓝粉渐变背景"的,改用 `hero-text-only` 或 `hero-split`

## 在 draw-md 中的写法

```markdown
## Hero
- pattern: hero-split
- left: { headline, subhead, cta-primary, cta-secondary }
- right: { image: product-screenshot.png, ratio: 4:3 }
- motion: scroll-reveal-stagger (Level 5)
```
