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

## 跨次构建记忆（Build Log + Stamp）

> 规则 2 的"与最近一次产出对比"以前无可执行的读取路径，只能靠叙述。本节让"Don't Repeat"真正可执行：**PROJECT 内一致性**由 DESIGN.md 锁定（第 7 页必须像第 1 页），**跨次差异**由构建日志驱动（第 7 次构建必须不同于第 6 次）——两个目标相反，禁止共用一份文件。来源：Adapted from finesse-ui divergence §4（MIT），2026-09 吸收，轴替换为本引擎七轴。

### 构建日志 `.maliang/build-log.json`

项目根目录。JSON 数组，**新条目在前**，最多保留 **20** 条：

```json
[
  {
    "date": "2026-09-22",
    "page": "acme-launch",
    "mode": "Experience",
    "axes": {
      "theme": "Deep Dark Mode",
      "background": "tactile textured surface",
      "typography": "editorial serif+sans",
      "hero": "massive image-first",
      "section": "gallery-led cadence",
      "signature": "layered-crop + quote-wall + bento + marquee",
      "motion": "pinned narrative + scrubbing reveal"
    },
    "dials": { "variance": 7, "motion": 6, "density": 3 },
    "brief": "工业键盘发布页"
  }
]
```

首次写入时创建 `.maliang/` 目录，并把 `.maliang/` 加入项目 `.gitignore`。

### 盖章 Stamp —— 无日志时的回退

页面 CSS 的第一个非空行（或内联 `<style>` 顶部）写入同一组坐标：

```css
/* maliang · mode=Experience · A=deep-dark · B=tactile-texture · C=editorial-serif
 * D=image-first · E=gallery-led · F=crop+quote+bento+marquee · G=pinned+scrub · V7M6D3 */
```

日志是主记忆（本机连续构建快），盖章是回退（随代码走：新 clone、协作者、被单独拷走的 HTML 都能读）。**两者分工成立的前提是盖章被提交而日志被 ignore**——丢掉任何一个，项目都会静默退回无记忆状态。无 `build-log.json` 时，grep 目标代码里的 `/* maliang ·` 反推一条记录。

### 接线表（两端都是强制的）

| 时机 | 动作 |
| --- | --- |
| design-md Phase 0（Design Read 之前） | 读 `.maliang/build-log.json`；无则 grep `/* maliang ·` 盖章反推；都无 = 首次构建，无约束 |
| Phase 0 组合声明（旁边） | **把轮换说出来**——用一句话陈述新组合与最近一条在哪几根轴上不同，写进决策记录 |
| design-md 收尾（自检通过后） | 数组头部 prepend 一条、裁到 20 条；把盖章写进 CSS 首行 |

### 阈值

沿用强制规则 2：新组合与日志最近一条**逐轴对比，≥5 轴相同即须重选**（等价于差异 ≥3 轴才放行）。补全历史页（dials 从未被记录）时只写七轴、省略 dials 数值——**编造的 dial 比缺席更糟**，下一次构建会把它当真值去轮换。
