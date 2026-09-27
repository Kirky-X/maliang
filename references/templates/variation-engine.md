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

## 单次发散会话伪分歧自检

> 作用域不同的**第二套轴**：上文七轴管**跨项目防雷同**（选型枚举，项目级、写入 DESIGN.md），本节五轴管**单次发散会话内的运行时自检**（方案级、不落 DESIGN.md）——多方案 prototype、方向探索时启用，两套轴禁止混用。来源：prototype skill 伪分歧判据，2026-09 吸收；并反哺强制规则 5 的挑战者捐赠——挑战者脑内构思同样过本自检，防止挑战者只是选定方向的换色版。

- **构建前声明分歧轴**：每个变体动手前，一句话说出它在五根轴——layout / density / personality / motion / interaction model——中的哪根上发散；说不出的变体不配进列表。
- **方向词命名**：变体用方向词命名（"安静""编辑感""致密""游戏感"），禁止 Option A/B/C——名字讲不出方向，说明方向不存在。
- **同向即替换**：两个候选若只差强调色或文案，它们是同一个方向；把其中一个换成真正的替代（换布局、换交互模型、换动效叙事）。
- **完成判据**：每个变体有名有轴，且 no two variants share an axis position——任一变体单独拿出来都是可独立发布的答案。
- **收敛则砍并明说**：构建中若两个变体收敛了，砍掉一个并显式告知；"两个真不同的方向"胜过"凑满三个"。
- **发散不降 craft bar**：每个变体单独满足完整 craft 标准（入场 ease-out、UI 动效 ≤400ms、只动 transform/opacity、处理 reduced-motion）；粗糙的变体不会拓宽探索面，只会输在执行并浪费一次方向采样。

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
