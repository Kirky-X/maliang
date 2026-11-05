# 卡片模式命名词汇

> 模式词汇库。卡片是 UI 中最通用的容器组件,本表标准化其变体命名。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `card-basic`          | 标题 + 描述,无图                                 | 功能介绍、简单列表                    |
| `card-media-top`      | 顶部图 + 下方文案                                 | 博客文章、商品卡、案例展示            |
| `card-media-left`     | 左图 + 右文(水平)                              | 列表项、搜索结果、商品列表            |
| `card-media-bg`       | 背景图 + 浮层文字                                 | 类目入口、IP 展示、活动卡             |
| `card-action`         | 含 CTA 按钮                                       | 商品卡(加购)、服务卡(预约)         |
| `card-collapsible`    | 可折叠(点击展开)                                | FAQ、设置项、详情展开                 |
| `card-glass`          | 玻璃质感(见 [`glass-effect.md`](../dimensions/glass-effect.md)) | 浮动 dock、模态浮层 |
| `card-shadowed`       | 强阴影悬浮                                        | Tooltip 卡、下拉菜单                  |
| `card-bordered`       | 仅 border 无阴影                                  | 列表项、表格行替代                    |
| `card-tinted`         | 浅色背景 tint(非白)                             | 高亮项、选中态、分组                  |
| `card-skeleton`       | 加载占位骨架                                      | Loading 状态(见 [`principles.md`](../meta/principles.md) 第 14 定律) |
| `card-empty`          | 空状态卡(插画 + 文案 + CTA)                     | 空列表(见 [`principles.md`](../meta/principles.md) 第 14 定律) |
| `card-double-bezel`   | 双层嵌套容器:外壳 `bg-*/5` + ring 发丝边 + `p-1.5` + 大圆角,内核独立底色 + 内高光 + 同心圆角 `calc(外圆角 - 0.375rem)` | 高级感工艺卡、设置组、统计卡 |
| `card-tilt-depth`     | 卡片层深 tilt:0.4 / 1.0 / 1.6 三档层深,hover 视差(层移/旋转参数详见 [buttons.md](buttons.md)) | 精品内容卡、作品集、封面卡 |
| `card-stat`           | 数值卡:大数值 + 标签 + delta 涨跌,数字用等宽数字(tabular-nums) | KPI 概览、仪表盘指标卡(样式基准见 [data-dense-dashboard](../templates/data-dense-dashboard.md) 模板) |
| `card-swipe-verdict`  | 左右甩卡判定:顶层卡跟手平移+随位移旋转(±15° 上限),右拖浮绿色判定章/左拖浮红色否定章,过阈值(120px)松手沿拖向加速甩出,下一张 0.95→1 补位;不足弹回中间(与 [buttons.md](buttons.md) `card-stack-pull` 互见:彼条纵向抽卡;与 [pro-motion.md](pro-motion.md) `card-swipe-deck` 互见:彼条卡组循环切换,本条二选一判定即终结) | 匹配、选片、二选一评审卡堆 |
| `swipe-row-delete`    | 行级左滑删除:行跟手左移露出删除钮,松手按阈值分流——过线(80px)吸附停在露钮位、不足弹回、过半宽直接删除(该行滑出淡出+高度收 0+下行平滑补位,约 300ms ease-out);删除有去向,禁止整块瞬间消失 | 消息/条目列表行 |
| `card-disintegrate`   | 碎沙消散删除:确认删除后元素按像素拆成小粒子(约 1500 粒,各保留原位置颜色),从一侧依次散开似风扫过(约 0.8s,装饰类长动效须可跳过/reduced-motion 直达删除终态) | 聊天气泡、内容销毁(与 `swipe-row-delete` 互见:彼条滑出+补位"有去向",本条原地消散强情绪,仅低频高情绪场景) |
| `card-fan-stack-swipe` | 扇形叠滑动切换:一组照片按序展开成扇形,左右滑动换组时整组用弹簧重新摆位,标题同步替换,分页指示点当前项拉长 | 相册分组浏览(与 [buttons.md](buttons.md) `card-stack-pull` 互见:彼条单张纵向抽卡,本条整组扇形横向换组) |
| `swipe-triage` | 滑动分拣:相似项排成一叠,当前张跟手平移,超阈值沿手势方向飞出对应一种处置(左丢右留);下一张从缩小压暗状态弹簧放大浮上瞬时接替 | 照片整理/邮件/待办批量分流(与 `swipe-row-delete` 互见:彼条删单行,本条连叠分拣双处置) |
| `card-press-tilt-follow` | 按压跟手倾斜:按压点在哪侧卡片向哪侧下沉倾斜,按住平移跟手,松手弹回 | 大图卡/可视化卡按压反馈(与 `card-tilt-depth` 互见:彼条 hover 视差层深,本条按压跟手倾斜) |
| `card-flip-3d` | 3D 翻面:绕竖轴带透视翻面,backface 隐藏背面镜像,翻到一半微微抬起落下带回弹,柔和高光随指针变化;变体:绕横轴垂直翻(与 [`buttons.md`](buttons.md) `card-flip-3d` 互见:彼条为该模式的 CSS 配方行,本条为交互定义) | 卡片正反面(摘要/详情)、集换卡(与 `card-tilt-depth` 互见:彼条倾斜不换面,本条翻面换内容面) |
| `card-longpress-lift-menu` | 长按浮起:长按把卡片"拿起来"(抬起放大),整页虚化,弹出菜单滑动选择 | 移动端卡片快捷操作(长按浮起家族 canonical;桌面端改 hover/右键菜单) |
| `card-expand-fullpage` | 整卡铺满:点击放大圆角贴合屏幕,封面延续为详情头图,新增内容错层入场,关闭复原 | 列表卡→详情(与 `shared-element-card-transition` 互见:彼条共享元素映射对应位,本条整卡放大铺满) |
| `stacked-cards-peel` | 纵深逐层展开:纵深堆叠卡片按不同位移逐层下移展开,收起带弹性叠回 | 堆叠内容就地展开(与 `card-fan-stack-swipe` 互见:彼条扇形叠滑动换组,本条纵深逐层展开;与 [buttons.md](buttons.md) `card-stack-pull` 互见:彼条纵向抽卡) |
| `staged-card-swap-arc` | 圆弧卡组换卡三阶段:选中卡转到中央,换卡分转侧→换内容→转回正面三步走 | 人物/物品弧形选择卡组 |
| `card-peel-curl` | 卷纸揭面:按角卷纸揭背面,弯曲阴影跟手同步,松手回弹 | 贺卡/票据/翻页隐喻(与 `card-flip-3d` 互见:彼条刚体绕轴翻面,本条柔性卷曲) |
| `glass-weather-card` | 玻璃数据卡:玻璃卡上温度/文字/趋势曲线/背景色随数据连续变化,玻璃透出后方柔色而前景信息清晰 | 天气/环境监测卡(质感配方见 [`glass-effect.md`](../dimensions/glass-effect.md);与 `card-glass` 互见:彼条静态质感,本条数据连续过渡) |
| `shared-element-card-transition` | 共享元素转场(container transform):卡片与详情间连续过渡位置/尺寸/圆角,核心信息移到详情对应位,禁整体缩放文字 | 列表卡→详情无缝转场(与 `card-expand-fullpage` 互见:彼条整卡铺满;图片原位放大家族见 [galleries.md](galleries.md) `gallery-shared-element-expand`) |

## 使用规则

- 同一页面卡片变体 ≤ 3 种(避免混乱)
- 卡片间距统一(用 spacing-md 或 spacing-lg,不混用)
- 卡片圆角按 [`radius.md`](../dimensions/radius.md) 分档,容器 > 控件
- 触发 [`ai-tells.md`](../meta/ai-tells.md) "全场 rounded-2xl" 时,差异化圆角
- 等高三列卡片网格禁用(见 [`ai-tells.md`](../meta/ai-tells.md) 第 9 节),改 bento 或非对称
- 信息密度平衡:太疏的卡显得多余,太密失去一瞥价值——一瞥给要点,细看有增量;卡片尺寸升级=信息层级加深,禁止把小卡内容原样拉伸填大卡
- 卡片描述动词开头("查看当前用量…"),禁"本卡片展示…"式自我介绍
- **刷新动效按变化幅度选型**:微元素(按钮/图标)直接变化;数字翻转/滚动(见 number-motion);整卡大面积内容换版用渐隐渐现;周期轮换用带方向的推移补位——变化多小配多小的动效,禁小变化配大动作

## 在 draw-md 中的写法

```markdown
## Card (product-card)
- pattern: card-media-top
- media: { image: product.jpg, ratio: 4:3 }
- title: { typography: font-size-title-md, max_lines: 2 }
- meta: { typography: font-size-label-sm, color: color-text-secondary }
- price: { typography: font-size-display-md, color: color-brand }
- action: { type: button-primary, label: "加入购物车" }
- states: [default, hover-lift, pressed-scale]
```
