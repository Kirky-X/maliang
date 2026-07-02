# 布局模式命名词汇

> 模式词汇库。draw-md 阶段描述页面整体布局时使用的标准化命名。来源:taste-skill。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `layout-single-column`| 单列居中,最大宽度限制                            | 文章 / 博客 / 长文案                  |
| `layout-two-column`   | 主内容 + 侧边栏(左或右)                         | 文档站、博客详情、Wiki                |
| `layout-three-column` | 三列(导航 + 内容 + 辅助)                       | IDE、邮件客户端、Slack 类             |
| `layout-bento-grid`   | 不对称网格(1 大 + 多中小)                       | SaaS Dashboard、产品功能展示          |
| `layout-masonry`      | 瀑布流(列高不齐)                                | 图片社区、Pinterest 类                |
| `layout-grid-uniform` | 等大网格(N × M)                                 | 商品列表、卡片墙                      |
| `layout-full-bleed`   | 全出血(无外边距)                                | Hero、媒体、视频背景                  |
| `layout-split-screen` | 50/50 左右分屏                                    | 双 CTA、对比展示、登录页              |
| `layout-stacked`      | 全宽纵向堆叠                                      | 营销落地页、品牌叙事                  |
| `layout-canvas`       | 自由画布(拖拽 / 缩放)                           | 设计工具、白板、Figma 类              |

## 使用规则

- 单页布局模式 ≤ 2 种组合(如 `layout-full-bleed` hero + `layout-single-column` 正文)
- 触发 [`ai-tells.md`](../meta/ai-tells.md) 第 9 节"三列卡片禁令"时,改用 `layout-bento-grid`
- `layout-canvas` 仅用于创意工具,普通 SaaS 禁用
- 移动端默认 `layout-single-column`,跨端时显式标注响应式断点
- 容器宽度差异化:hero `max-w-screen-2xl`、正文 `max-w-3xl`、feature `max-w-5xl`(见 [`ai-tells.md`](../meta/ai-tells.md) 第 3 节)

## 在 draw-md 中的写法

```markdown
## Layout
- pattern: layout-stacked
- sections:
  - { name: hero, layout: layout-full-bleed }
  - { name: features, layout: layout-bento-grid, columns: 4 }
  - { name: testimonial, layout: layout-single-column, max_width: 3xl }
  - { name: pricing, layout: layout-grid-uniform, columns: 3 }
```
