# 搜索与筛选模式命名词汇

> 术语库。搜索的目标是"少打字、快收敛",筛选的目标是"收窄数据集且状态可撤销":建议、高亮、撤销三条线都要可预期。来源:NN/g(nngroup.com)、Red Hat PatternFly(patternfly.org)、IBM Carbon Design System(carbondesignsystem.com)、Ant Design(ant.design)。抓取核验日期(verified):2026-09-08。

## 命名表

| 模式名                     | 视觉特征                                          | 适用场景                                  | 禁用场景/阈值                                        |
| -------------------------- | ------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------- |
| `search-bar`               | 常驻搜索框,占工具栏左侧并延展到右侧动作前        | 表格工具栏、列表页头部(Carbon open search) | 搜索非主任务时降级为图标入口                        |
| `search-on-demand`         | 默认收起为图标按钮,点击才展开输入框              | 工具栏动作多、空间紧(Carbon active search) | 搜索是主任务时不许收起                              |
| `search-autocomplete`      | 输入时下拉补全建议,逐键更新                      | 已知词检索、商品/文档查找                 | 每条建议必须有有效结果;移动端只做纯文本建议          |
| `search-scope`             | 建议下挂分类范围,缩进且视觉区分                  | 电商/多类目站内搜索(NN/g scoped)        | 类目含义不清禁用;防建议列表过载                      |
| `search-instant`           | 边输边出结果,无需回车                            | 小而快的结果集(通讯录/设置项)          | 慢源或大结果集须回车提交,防半途渲染                  |
| `search-faceted`           | 多维分面筛选(分类/状态/区间)由工具栏或侧栏承载 | 多属性数据集收敛(PatternFly toolbar)    | 单维度用搜索;分面 >5 组折叠                          |
| `filter-chip`              | 已选筛选落成可逐个撤销的片,"清除全部"常驻       | 激活筛选的可见化(移动端尤其必要)        | 只显示数量不显示值 = 藏状态                          |
| `filter-drawer`            | 筛选项收进抽屉,呼出按钮带已选计数                | 移动端筛选项多(≥3 组)                  | 抽屉容器与手势遵循 popups.md;桌面端少用              |
| `filter-sidebar`           | 左侧栏分面常驻可见,改选即时生效                  | 桌面端大结果集(商品/文档库)            | 筛选维度 ≤2 时工具栏足够                             |
| `search-command`           | 快捷键唤起命令面板,搜动作/页面/对象三合一        | 后台工具、开发者向产品                    | 消费者内容站慎用;必须有可发现入口                    |
| `search-results-highlight` | 结果与建议中加粗/缩进区分用户已输入片段          | 全部搜索结果与建议列表(NN/g 文本样式)   | 补全式高亮补全段,包含式高亮用户输入,勿混用          |
| `search-empty-query`       | 聚焦未输入时给快捷入口(最近/热门/历史)          | 首页搜索、高频复访场景                    | 无历史数据只给热门,勿留空面板                        |
| `search-no-result`         | 无结果页:说明原因 + 建议改词/清除筛选出口        | 所有搜索必须覆盖的终态                    | 纯"无结果"空屏禁用;筛选叠加时优先给"清除筛选"      |
| `filter-range-slider`      | 单/双滑块区间筛选:价格、日期等连续区间,拖动实时联动结果计数 | 价格带、时间范围等数值区间收敛          | 离散少档位改 chip/复选;双滑块须键盘可微调,读数不被拇指遮挡 |

> 来源注:`filter-range-slider` 为**审计补全**(2026-09-08 组件覆盖审计):对照 Ant Design Slider、IBM Carbon Slider、Material 3 Slider 组件清单;framework `slider` 类提供控件层支撑。

## 使用规则

- 分工:表格结构模式在 [tables.md](tables.md),图表选型在 [charts.md](charts.md);表格工具栏里的搜索与筛选是本表模式在 tables.md 工具栏规则下的实例
- 建议不是装饰:用户仅约 23% 的场景选中建议,其价值在减少打字、防错、减轻记忆负担(NN/g)——空结果或劣质结果的建议比没有更糟
- 高亮规则固定:建议为"补全式"高亮补全字符,建议"包含"用户输入时高亮用户输入;用字重/斜体/缩进区分,禁止只靠颜色(ux-rules color-not-only)
- 筛选可见化:激活筛选必须以 chip 展示值并可逐个撤销,"清除全部"常驻(PatternFly);chip 增删与撤销的反馈动效见 [buttons.md](buttons.md)
- 空间不够时筛选收进 toggle 折叠面板或抽屉,容器与退场手势遵循 [popups.md](popups.md);折叠面板展开后跨过断点不自动收起(PatternFly 警告)
- 结果计数常驻"1 - 20 of 37"口径(PatternFly),翻页/筛选后总数与加载态可见;清空筛选必须能回到全量数据集
- 筛选与搜索状态可返回:返回键恢复筛选/输入(ux-rules back-behavior);行内筛选面板支持面板内搜索(Ant Design filterSearch)
- 移动端建议只做纯文本,富建议(图片/类目卡)留在桌面端(NN/g);范围型建议缩进置于推荐查询之下
- `search-command` 的快捷键必须配可见入口(占位符文案或按钮),纯隐藏快捷键 = 不可发现;面板内选中项与输入保持键盘可达
- `search-no-result` 三要素:说清原因 + 下一步(改词建议/热门内容/清除筛选)+ 搜索框保持可用,对齐 ux-rules empty-states

## 在 draw-md 中的写法

```markdown
## Search (list-toolbar-search)
- pattern: search-bar + filter-chip
- input: { placeholder: "搜索订单号/客户名", autocomplete: on, highlight: typed }
- filters: [status(multi), date(range), owner(multi)]
- chips: { clear_all: always, collapse: +n }
- states: [empty-query: recent+hot, no-result: guide]
```
