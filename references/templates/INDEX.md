# 模板墙 INDEX

> 模板墙总索引。选型前先读 [README.md](README.md)（schema / 治理 / 四步路由）。`dial` 列为 variance/motion/density 适配区间。

## 设计语言（design-language）

| id | 中文名 | 一句话 | dial (V/M/D) | status |
| --- | --- | --- | --- | --- |
| [apple-liquid-glass](apple-liquid-glass.md) | 液态玻璃 | 控件/导航做成悬浮光学玻璃层，折射模糊随环境与无障碍设置自适应 | 4-7 / 3-7 / 2-5 | production |
| [material-3-expressive](material-3-expressive.md) | M3 富表现力 | 大形状对比 + 弹簧物理动效 + 鲜艳色彩角色（Google 2025） | 5-8 / 5-9 / 3-7 | production |
| [fluent-2](fluent-2.md) | Fluent 2 设计系统 | 微软 token 驱动克制中性：1px 描边 + 双层软阴影 + 亚克力浮层 | 2-5 / 2-5 / 4-8 | production |
| [bento-grid](bento-grid.md) | 便当盒网格 | 不等尺寸瓷砖拼贴，一格一主题、大格叙事小格点缀 | 5-8 / 2-6 / 3-7 | production |
| [editorial-swiss](editorial-swiss.md) | 瑞士编辑排版风 | 排版即设计：栅格 + 无衬线大字 + 留白 + 1px 分割，零装饰 | 3-6 / 1-4 / 2-5 | production |
| [dark-oled](dark-oled.md) | OLED 暗色模式 | 纯黑/近黑分层 + 白字 87/60/38 三档 + 彩色降饱和（可叠加任意模板） | 2-6 / 2-6 / 3-8 | production |
| [data-dense-dashboard](data-dense-dashboard.md) | 数据密集型仪表盘 | 4/8px 网格 + KPI 卡片 + 表格明细 + 等宽数字的高密度面板 | 2-4 / 1-3 / 7-10 | production |
| [neo-brutalism](neo-brutalism.md) | 新粗野主义 | 粗黑描边 + 零模糊硬投影 + 高饱和平涂 + 超粗大字 | 7-10 / 3-7 / 3-6 | style |
| [claymorphism](claymorphism.md) | 黏土拟态 | 超大圆角 + 内外三件套阴影的软黏土立体感 | 5-8 / 3-6 / 2-5 | style |
| [glassmorphism](glassmorphism.md) | 玻璃拟态（经典磨砂） | 白色磨砂浮卡 + 彩色 blob 背景（静态贴片，≠液态玻璃的光学透镜，二选一） | 4-7 / 2-5 / 2-5 | style |
| [aurora-gradient](aurora-gradient.md) | 极光渐变 | 模糊光斑缓慢流动的氛围背景（Stripe 范式） | 4-8 / 3-7 / 1-4 | style |
| [neumorphism](neumorphism.md) | 新拟物（软 UI） | 同色凸凹浮雕软 UI（⚠ 对比度不达 WCAG AA） | 2-4 / 1-3 / 2-4 | experimental |

## 整页模式（page-pattern）

| id | 中文名 | 一句话 | dial (V/M/D) | status | 来源 |
| --- | --- | --- | --- | --- | --- |
| [editorial-split](page/editorial-split.md) | 编辑分栏型 | 左栏文字 + 大中缝留白 + 右栏图墙，杂志式左右分栏 | 4-7 / 1-4 / 2-5 | production | v05 |
| [cursor-reveal](page/cursor-reveal.md) | 叠影显影型 | 两图叠放底层压暗，鼠标 300px 光环环内显影另一张图 | 5-8 / 4-7 / 1-4 | style | v05 |
| [sliced-panels](page/sliced-panels.md) | 竖切分栏型 | 整屏竖切成条，同一时间只亮一格（flex-grow 展开） | 4-7 / 3-6 / 2-5 | style | v05 |
| [gradient-on-dark](page/gradient-on-dark.md) | 暗底流光型 | 近黑底 + 一条三色渐变只喂标题 + 5% 噪点防 banding | 5-8 / 2-5 / 1-4 | style | v05 |
| [depth-corridor](page/depth-corridor.md) | 纵深长廊型 | 作品排成一条路，透视 1500 + 滚动冲量，越远越暗 | 5-8 / 5-8 / 1-4 | style | v05 |
| [dashboard-styles](page/dashboard-styles.md) | Dashboard 风格集 | 一文件四风格（极简商务/清爽轻量/暗黑科技/高饱和撞色）+ 配色占比公式与三问自查 | 2-6 / 1-3 / 7-10 | production | v14/v08 |
| [mobile-layouts](page/mobile-layouts.md) | 移动端高级布局五式 | 图片主导/卡片节奏/大字留白/沉浸氛围/极简编辑，五套移动端设计语言 | 3-7 / 1-3 / 2-6 | production | v21 |
| [scroll-band-gallery](page/scroll-band-gallery.md) | 滚动图带六式 | 图墙收拢成带/扇/筒/环/扭/隧道六种几何形态的滚动动效骨架 | 5-8 / 5-9 / 1-4 | style | v06 |

> page-pattern 组已覆盖 Web 五风格（v05）、Dashboard 风格集（v14/v08）、移动端五式（v21）、滚动图带六式（v06）、高级布局量化对照（v03，见 vocabulary/layout.md）。

## 落地页编排与性格方向

| 文件 | 内容 |
| --- | --- |
| [landing-patterns.md](landing-patterns.md) | 落地页章节序列 + CTA 位置 + 转化优化（精选） |
| [character-directions.md](character-directions.md) | 六种性格方向卡（与产品类型正交的"感觉"轴） |

## 其他

- [variation-engine.md](variation-engine.md) — 七轴组合选型（防跨项目雷同，design-md Phase 0 必过）
- 选型提示：按平台定大方向（Apple 生态→liquid-glass；Android→m3-expressive；企业 B 端→fluent-2 / data-dense-dashboard）；风格级需先匹配品牌气质；experimental 上生产前过 WCAG AA。
