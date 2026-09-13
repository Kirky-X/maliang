# 数据表格模式命名词汇

> 术语库。表格是数据密集页面的核心容器:先按数据量级(行数/列数)与操作需求(排序/筛选/批量/编辑)选模式,再谈样式。来源:IBM Carbon Design System(carbondesignsystem.com)、Ant Design(ant.design)、Red Hat PatternFly(patternfly.org)、Material Design 3(m3.material.io)。抓取核验日期(verified):2026-09-08。

## 命名表

| 模式名                  | 视觉特征                                             | 适用场景                              | 禁用场景/阈值                                        |
| ----------------------- | ---------------------------------------------------- | ------------------------------------- | ---------------------------------------------------- |
| `table-basic`           | 表头行 + 数据行,无附加交互(表头行是必备底座)     | 静态结构化展示                        | <3 行改列表;>200 行必配排序或分页                    |
| `table-dense`           | 行高取小档收窄,表头与数据行同档不混用               | 后台密集数据页,同屏多行               | ≤20 行不必加密;行内需双行内容时禁用最小档            |
| `table-sortable`        | 列头排序三态(未排/升/降),图标只在排序列显示        | 需按列重排的 ≤200 行本地数据          | 图标常亮全列 = 噪声;服务端大数据改默认排序+筛选      |
| `table-filterable`      | 工具栏承载复杂筛选,列头下拉筛选(菜单/树两种模式)  | 多维过滤(状态/日期/分类)            | 单一字段过滤用搜索即可,勿堆筛选器                    |
| `table-selectable`      | 行首选择框(多选/单选),全选框三态,选中出批量操作栏 | 批量操作(导出/删除/审批)            | 无批量动作不建选择列;批量模式下行内单行动作须禁用    |
| `table-expandable`      | 行展开露出补充详情,展开图标固定行首                 | 补充信息或慢加载数据收进行内          | 内容撑满一屏改详情页/侧栏;"展开全部"不默认提供       |
| `table-sticky-header`   | 滚动时表头吸顶                                      | >20 行长列表滚动浏览                  | <一屏的短表吸顶无意义                                |
| `table-sticky-column`   | 首列(行标识)吸左,宽表横向滚动时常驻               | ≥6 列宽表                             | 无横向滚动禁用;首尾同固注意遮挡                      |
| `table-grouped`         | 分组行聚合可折叠,子行缩进成树                       | 按维度(地区/部门/品类)聚合          | 层级 >3 层改树组件;无聚合语义不硬分组                |
| `table-paginated`       | 底部分页(简单翻页/每页条数+跳页),上方加分隔      | 20-200 行稳定数据集                   | <20 行不配分页;分页控件只放底部                      |
| `table-infinite-scroll` | 滚动到底自动追加行                                  | 流式数据(动态/日志)、探索式浏览     | 任务型需定位具体行的场景;必须给"到底"提示           |
| `table-virtualized`     | 只渲染可视区行,滚动按需挂载                         | >1000 行大数据量平铺                  | <500 行无需虚拟化;虚拟化时行高必须恒定               |
| `table-card-reflow`     | 窄屏每行降级为卡片,字段名-值成对展示               | 移动端宽表降级                        | 移动端禁页面级横滚;字段多时优先局部横滚              |
| `table-inline-edit`     | 单元格/行内点击进入编辑态就地保存                   | 少量字段就地修改(配置表/清单)      | 大面积录入改表单;只读展示勿留编辑入口                |
| `table-summary-row`     | 尾部合计/小计行                                     | 财务/统计的合计                       | 无可加总语义的列禁用                                  |
| `table-zebra`           | 隔行底色辅助横向扫读                                 | 宽表多列对照                          | <6 行或已用 hover 态时二选一,勿叠加                  |
| `table-descriptions`    | 键值对详情:两列 label/value 成组分节,只读摘要        | 详情页字段摘要(订单/资产/配置;与 [data-dense-dashboard](../templates/data-dense-dashboard.md) 模板呼应) | 需排序/筛选/多行对比仍用数据表;可编辑字段改表单      |

> 来源注:`table-descriptions` 为**审计补全**(2026-09-08 组件覆盖审计):对照 Ant Design Descriptions、IBM Carbon structured list 组件清单(Material 3 无原生对应)。

## 使用规则

- 分工:图表选型在 [charts.md](charts.md),搜索与筛选交互在 [search.md](search.md),本文只管表格结构;图表的无障碍 fallback 数据表遵循 ux-rules.md 的 data-table 条目
- 行高分档同表一档:Carbon 五档行高中表头必须与数据行同高,不混用;仅行内双行内容才允许最大档
- 排序图标只在当前排序列显示,未排序列 hover 时浮现(Carbon 三态);行 hover 态恒开辅助扫读,与斑马纹按需二选一
- 数字列右对齐并用等宽数字,排版细节见 [typography.md](typography.md);列头 1-2 个词,截断必须留 tooltip 全文路径
- 选中行后批量操作栏接管工具栏,行内溢出菜单在批量模式下禁用(Carbon);批量按钮与筛选片的撤销反馈动效见 [buttons.md](buttons.md)
- 慢数据用骨架屏替代 spinner(Carbon);空表给空态与下一步动作(ux-rules empty-data-state),表格不要嵌套表格、不塞进滚动文本容器(M3)
- 移动端禁止页面级横向滚动(ux-rules horizontal-scroll):宽表要么局部横滚,要么 `table-card-reflow`;触控行高 ≥48dp(M3)
- 筛选交互细节(分面/chip/抽屉)见 [search.md](search.md);本表 `table-filterable` 只定结构位

## 在 draw-md 中的写法

```markdown
## Table (orders-main)
- pattern: table-sortable + table-selectable
- rows: { count: 120, render: paginated, page_size: 20 }
- columns: [order_no(text), status(tag), amount(number, align: right, tabular_nums: true)]
- batch_actions: [export, delete]
- states: [hover, loading-skeleton, empty]
```
