# 设计系统范例索引（examples/design-system/）

> 本目录是 design-md / redesign 命令的**示例产物**（每目录一份完整 DESIGN.md），供 preview 渲染比较与 draw-md 规格参照。注意 SKILL.md 的约定：examples/ 是产物示例，**不是分析目标**——用户项目中的 DESIGN.md 才是工作对象。本 INDEX 是 12 个风格目录 + 根级 Minimalism 样张的唯一清单；设计语言 token 配方的 canonical 在模板墙（[references/templates/](../../references/templates/)），范例与模板冲突时以模板为准。

| 范例 | 语言一句话 | 对应模板（token 配方 canonical） |
| --- | --- | --- |
| [DESIGN.md](DESIGN.md)（根，Minimalism） | 瑞士极简 heritage 样张，ci-gate 校验入口 | —（自著示例样张，无对应模板） |
| [brutalism](brutalism/DESIGN.md) | 高对比粗野功能主义，数据密集/工业界面 | [neo-brutalism](../../references/templates/neo-brutalism.md) |
| [cyberpunk](cyberpunk/DESIGN.md) | 暗色霓虹数据界面（青/紫/品红辉光） | —（无对应模板；勿与 tactical-terminal 混用） |
| [editorial](editorial/DESIGN.md) | 杂志级排版叙事 + 暖金强调色 | [editorial-swiss](../../references/templates/editorial-swiss.md)（编辑排版族） |
| [glassmorphism](glassmorphism/DESIGN.md) | 磨砂玻璃拟态（半透明 + backdrop blur） | [glassmorphism](../../references/templates/glassmorphism.md) |
| [heritage](heritage/DESIGN.md) | 建筑式极简编辑产品 + 新闻质感 | —（无对应模板） |
| [illustrative](illustrative/DESIGN.md) | 手绘插画 + 圆润几何的温暖叙事系 | —（无对应模板） |
| [material-design](material-design/DESIGN.md) | Google Material 语言（material 隐喻 + 阴影海拔） | [material-3-expressive](../../references/templates/material-3-expressive.md)（Material 家族） |
| [neomorphism](neomorphism/DESIGN.md) | 同色双影软浮雕 | [neumorphism](../../references/templates/neumorphism.md)（阴影配方 canonical） |
| [skeuomorphism](skeuomorphism/DESIGN.md) | 拟物材质（皮革/纸张/木纹/玻璃） | —（无对应模板） |
| [swiss-style](swiss-style/DESIGN.md) | 网格驱动 + 排版理性 + 单信号红 | [editorial-swiss](../../references/templates/editorial-swiss.md)（瑞士编辑族） |
| [y2k](y2k/DESIGN.md) | 千禧未来主义（霓虹渐变/金属玻璃/镀铬） | —（无对应模板） |

治理：范例随 skill 版本演进，过时条目不静默删除——按 [references/templates/README.md「废弃重定向」](../../references/templates/README.md) 的规则处置（frontmatter 加 `replaced-by` + 正文首行标注）。新增范例必须在本表登记，不得出现清单外孤儿目录。
