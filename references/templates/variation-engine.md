# 组合式变化引擎（Variation Engine）

> 目的：防止"同档位跨项目雷同"。dials 解决强度档位，本引擎解决**同档位下的方向差异**——每个项目从 7 根轴各选 1 并整页 commit，不同项目的轴组合必须不同。来源：taste-skill image-to-code §12 + impeccable new-work §3-4 反同质化协议，2026-09 吸收。

## 使用时机

`design-md` Phase 0 的 Design Read 之后、方向确认之前。产出一行"组合声明"（可写进 DESIGN.md frontmatter 或决策记录）：

```
组合 = Pristine Light × technical grid × editorial serif+sans × asymmetric split × bento rhythm × [marquee, layered-crop, product-stack, quote-wall] × [float-up, fade-through]
```

## 七轴选项

### 1. Theme Paradigm（选 1）
1. Pristine Light Mode（纯净浅色）
2. Deep Dark Mode（深邃暗色）
3. Bold Studio Solid（大胆纯色块面）
4. Quiet Premium Neutral（安静高级中性）

### 2. Background Character（选 1）
1. subtle technical grid / dotted field（细微技术网格/点阵）
2. pure solid field with soft ambient gradient depth（纯色 + 柔和环境渐变景深）
3. full-bleed cinematic imagery（全出血影像）
4. tactile textured surface feel（触感材质表面）

### 3. Typography Character（选 1）
1. clean grotesk（干净无衬线）
2. refined grotesk（精致无衬线）
3. expressive display（表现力展示体）
4. compressed statement typography（压缩标语体）
5. editorial serif + sans（编辑衬线 + 无衬线混排）
6. Swiss rational hierarchy（瑞士理性层级）

### 4. Hero Architecture（选 1）
1. cinematic centered minimalist（电影式居中极简）
2. asymmetric split hero（非对称分栏）
3. floating polaroid scatter（悬浮拍立得散布）
4. inline typography behemoth（行内巨字）
5. editorial offset composition（编辑错位构图）
6. massive image-first hero with restrained text（巨图先行 + 克制文字）

### 5. Section System（选 1）
1. modular bento rhythm（模块化 bento 韵律）
2. alternating editorial blocks（交替编辑块）
3. poster-like stacked storytelling（海报式堆叠叙事）
4. gallery-led cadence（画廊主导节奏）
5. Swiss grid discipline（瑞士栅格纪律）
6. asymmetric premium marketing flow（非对称高级营销流）

### 6. Signature Component Set（11 选 4，唯一组合）
diagonal staggered square masonry ／ 3D cascading card deck ／ hover-accordion slice layout ／ pristine gapless bento grid ／ infinite brand marquee strip ／ turning polaroid arc ／ vertical rhythm lines ／ off-grid editorial layout ／ product UI panel stack ／ split testimonial quote wall ／ layered image crop frames

### 7. Motion-Implied Language（6 选 2）
scrubbing text reveal ／ pinned narrative section ／ staggered float-up ／ parallax image drift ／ smooth accordion expansion ／ cinematic fade-through

## 强制规则

1. **整页 commit**：组合选定后全页贯彻，禁止中途换轴、禁止混搭成"四不像"。
2. **组合去重**：与项目最近一次产出（或同品类参考项目）逐轴对比，≥5 轴相同即须重选。
3. **反品类默认**：列出该品类最惯用的 2-3 个组合并显式拒绝，除非 brief 明确要求；"能从品类猜出你的组合 = 自检失败"。
4. **与模板墙联动**：选定组合后到 [`INDEX.md`](INDEX.md) 找 category/dials 匹配的模板做具象化参照；模板是配方可参考，轴组合是身份须保持。
5. **挑战者捐赠**（可选强化）：让另一方向作为"挑战者"先行构思 5 分钟，verdict 三档（win/competitive/declined）；即使 declined，也必须从挑战者身上指认一项纪律反哺选定方向——"捐赠纪律，绝不搬运外衣"。
