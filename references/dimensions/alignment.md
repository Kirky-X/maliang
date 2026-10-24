# 对齐规范

> 规范层。值型 token 管「每个元素长什么样」(色/字/距/角,单元素属性,可 grep);本文件管「元素相对彼此站在哪」——对齐轴、同排等高、混排基线、光学修正、凸起与越界关系。布局容器选型见 [layout.md](./layout.md)(用什么容器),间距数值见 [spacing.md](./spacing.md)(离多远);本文件补的是两者之间的**相对位置**维度。机械判据由 [`../../scripts/preview-lint.js`](../../scripts/preview-lint.js) 的 `siblingRowMisalign` / `siblingUnequalSize` 承担,交付门禁为 [`../meta/numbered-gates.md`](../meta/numbered-gates.md) G44/G45。
>

## 值型 vs 关系型(为什么需要本文件)

| | 值型约束 | 关系型约束 |
| --- | --- | --- |
| 管什么 | 单元素的属性(色值/字号/间距/圆角) | 元素与元素/元素与容器的相对位置 |
| 怎么判 | token 引用 + 字面量 grep,静态可判 | 兄弟/父子几何比较,需渲染后量测 |
| 典型漏网 | 硬编码 `#FF0000`(G04 拦) | 四列统计卡图标顶差 12px(此前无人拦) |

值全对但排歪,是关系型错误——静态扫描对它失明,必须渲染后量测。

## 对齐轴

- **同容器内同类元素共享对齐轴**:同排卡片的左缘/顶缘、同列表图标的左缘、混排行内文字的基线,各自成轴。
- **同排同类元素的轴偏差 ≤ 2px**(亚像素 + 抗锯齿容差;超过即肉眼可辨)。
- 同一区块的**对齐轴 ≤ 3 条**——刻意错位(如 STAGGER 双列瀑布)须在方向契约或构建盖章里声明,未声明的错位即缺陷(轴数口径见 [`../vocabulary/layout.md`](../vocabulary/layout.md) STAGGER 行)。
- 跨页同构组件(nav-bar/dock 等 organisms)的对齐轴跨页恒定,见下文「跨页一致」。

## 同排等高与行槽

- **同排等高**:同一 flex 行内的同构卡片/控件渲染高必须相等。flex 默认 `align-items: stretch` 已保证;出现高差说明有元素逃逸(`align-self` 覆盖/固定高度/内容溢出),即缺陷(探针 `siblingUnequalSize`)。grid 同排等高同此要求,但探针对 grid 高度不查(bento 行跨度豁免,防误报),由 G44 人工截图核对。
- **行槽(slot)**:同构卡片内部的第 k 行(图标/数值/副文案)须跨卡对齐——**图标必须定框**(固定宽高的容器),禁止「图标内容天然高度」直接决定行位;图标高 32px 与 20px 混排时,下方所有行全部错位,这是统计卡错位的第一根因(探针 `siblingRowMisalign`)。
- **等分宽**:同排声明了 `flex-grow > 0` 的元素渲染宽必须相等;不等即某元素被内容撑破或配了固定宽。
- **与 ai-tells 三列等高禁令的边界**:[`../meta/ai-tells.md`](../meta/ai-tells.md) §1 禁的是「三列**同构凑数卡片**(icon+标题+描述 ×3)」的版式套路;本节管的是**同排控件/表单项/统计卡的几何一致**。等高本身不是罪——同构元素等高是纪律,无意图的参差才是缺陷。
- **与 G16 的边界**:G16 管**同一元素跨状态**几何恒定(输入框聚焦不抖动)与相邻 input/button 高度取同一**档位**;本节/G44 管**同排同构元素之间**的渲染几何一致——一个是状态轴,一个是兄弟轴,双命中时同向不冲突。

## 混排基线

- 一行内大小字号混排(数值+单位、大数字+标签)用 `align-items: baseline`(Web)/ `CrossAxisAlignment.baseline`(Flutter)——规则条目为 [`../meta/ux-rules.md`](../meta/ux-rules.md) `baseline-align-mixed`,自本文件归口。
- 数据数字用 tabular-nums(`ux-rules` `number-tabular`),防刷新跳动破坏基线。
- checkbox/radio 与文字同行的负 margin 修正、图标+文字按钮的单侧 padding 修正等**光学修正**清单见 [`../meta/polish-craft.md`](../meta/polish-craft.md) §六——几何居中 ≠ 视觉居中。

## 凸起与越界关系

越出容器边缘的凸起元素(dock 中心主操作按钮/FAB/骑缝头像)必须同时声明**三要素**,缺一即 G45:

| 要素 | 判据 |
| --- | --- |
| 凸起量 | 落 spacing token 档,且 ≤ 按钮高的 50%——超过即与相邻项基线断裂 |
| 锚定轴 | 声明水平/垂直锚定(如 dock 水平中轴),偏差 ≤ 2px |
| 相邻基线关系 | 凸起不得改变相邻元素的行位;两侧元素的图标顶/文字基线与其余同排项保持同一水平线 |

canonical 示例:[`../../examples/ui-markdown/organisms/dock.md`](../../examples/ui-markdown/organisms/dock.md) 中心凸起位。无规格的「大概齐」偏移不允许——偏移量没有依据,就没有上限。

## 跨页一致

- organisms 复用组件的几何(高度/圆角/对齐轴)**跨页恒定**:引用即承诺同构( [`../commands/draw-md.md`](../commands/draw-md.md) 的 organisms 引用规则)。导航栏首页 64px、内页 56px 这类漂移是缺陷,不是变化。
- 单页内一致( [`border.md`](border.md) / [`radius.md`](radius.md) 的「同一视图」条款)是**下限**;跨页一致是对 organisms 的要求。

## 机械判据与门禁

| 检查 | 手段 | 门禁 |
| --- | --- | --- |
| 同排行位错位 | 探针 `siblingRowMisalign`(结构相同兄弟逐行比顶缘,容差 2px) | G44 |
| 同排等高/等分宽破坏 | 探针 `siblingUnequalSize`(flex 行 stretch 语义 / flexGrow 等分) | G44 |
| 凸起无依据/越界 | 人工对账三要素 + 渲染实测凸起量 | G45 |

探针**只报不拦**,命中后按 [`../commands/preview.md`](../commands/preview.md) 处置三档处理;门禁 G44/G45 在 preview 交付时逐条过。

## 与其他文档的关系

| 文档 | 分工 |
| --- | --- |
| [layout.md](./layout.md) | 容器选型(Row/Column/Flex/Grid/Relative),管「用什么装」 |
| [spacing.md](./spacing.md) | 间距数值与六角色合同,管「离多远」;其「网格」节的 4 列基准网格与 8px 纵向基线是本文件对齐轴的数值基础 |
| [radius.md](./radius.md) | 嵌套圆角 `inner = outer − 间距` 是另一种父子几何关系,归彼处 |
| [`../meta/ux-rules.md`](../meta/ux-rules.md) | `baseline-align-mixed` / `number-tabular` 规则条目 |
| [`../meta/polish-craft.md`](../meta/polish-craft.md) | §六光学修正清单(经验数值跨端通用) |
| [`../meta/numbered-gates.md`](../meta/numbered-gates.md) | G44(同排错位)/G45(凸起无依据)交付否决 |
