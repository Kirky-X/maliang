<!-- 供体候选池快照(中文译本,非蒸馏供体)。
     站点分组: 通用风格模板(styleGeneral) · 站点摘要: Parallax Storytelling 是为通用界面提供的 UI 风格参照,侧重滚动驱动、叙事、分层滚动、沉浸、渐进披露。
     站点色板: —
     晋升正式供体须满足 ../README.md §5 三条件;蒸馏稿另立 ../<id>.md,与本快照并存。 -->

# Parallax Storytelling

## 1. 视觉主题与氛围

Parallax Storytelling 是为通用界面提供的 UI 风格参照,融合滚动驱动、叙事、分层滚动、沉浸、渐进披露、电影感、滚动触发。视觉方向由 transform: translateY(scroll)、position: fixed/sticky、perspective: 1px、滚动触发动画塑造。

用于品牌叙事、产品发布、案例研究、作品集、年度报告、营销活动。避免用于电子商务、仪表板、移动优先、SEO 关键、无障碍必需。

**关键特征:**
- 主色板:依故事而定,常为渐变与自然色,按区块定制色板
- 次色板:区块过渡色、深度层色、叙事情绪色
- 效果:transform: translateY(scroll)、position: fixed/sticky、perspective: 1px、滚动触发动画
- 无障碍:❌ 差(动效);性能:❌ 差;暗色模式:✓ 完整。
- 最适用于:品牌叙事、产品发布、案例研究、作品集、年度报告、营销活动
- 避免用于:电子商务、仪表板、移动优先、SEO 关键、无障碍必需

## 2. 实现要点

- 框架适配:GSAP ScrollTrigger 10/10、Locomotive Scroll 10/10
- 年代参照:2020 年代现代
- 本地预览:[打开 HTML 预览](../../refstyles/49-parallax-storytelling.html)
- 库索引:[打开 UI/UX Pro Max 首页](../../index.html)
