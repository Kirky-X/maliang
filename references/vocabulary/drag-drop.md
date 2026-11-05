# 拖放模式命名词汇

> 术语库。拖放是"按住-移动-放下"的直接操纵模式,本表标准化其触发阈值、语义与成败反馈命名。动效实现(排序重排/弹簧)见 [`../motion-skeletons/spring-reorder.md`](../motion-skeletons/spring-reorder.md);行内排序实例见 [`tables.md`](tables.md)。

## 命名表

| 模式名 | 构成要素(阈值/反馈) | 适用场景 |
| --- | --- | --- |
| `drag-lift-threshold` | 按住位移约 4px(3pt)后才出现拖影并进入拖动态 | 区分点击与拖拽;阈值内松手 = 点击,不触发拖放 |
| `drop-affordance` | 目的地可接受时才显示插入点/高亮,悬停即显、移开即消;不可接受时显示禁止符;文件夹类目标四态状态机:靠近即提前张开(预判)→悬停保持张开等待→放入夹口合上计数 +1→移出取消不触发(动效参数挂 [pro-motion.md](pro-motion.md) `drop-target-attract`) | 一切拖放目标;接受性反馈是拖放的核心语言 |
| `drop-move-copy` | 同容器放下 = 移动;跨容器放下 = 复制;跨应用恒为复制 | 默认语义;偏离默认(如跨容器移动)需显式修饰键并在拖影上标注 |
| `drop-fail-revert` | 放置失败:拖影弹回源位置;不可恢复的丢弃用放大淡出"蒸发"且先确认 | 排序失败回弹;删除到回收站类可蒸发,直接销毁必须确认 |
| `drop-arc-archive` | 归档吸入:文件沿弧线飞向目标缩小淡出,目标抬起接住、计数 +1;误放入的文件可沿原路弧线恢复(撤销) | 文件归档 / 拖放整理(成功路径与撤销;失败回弹见 `drop-fail-revert`) |
| `drag-autoscroll` | 拖到容器边缘时自动滚动,继续暴露更远目标 | 长列表/画布内拖放 |
| `drop-keep-selection` | 放置后保留源选中态,供连续操作(再拖/再删) | 批量整理场景 |
| `drag-split-snap` | 分屏比例把手:拖动横向把手两栏内容实时重排,松手吸附最近预设比例档 | 上下分屏 / 双栏工作区(离散档吸附同 [pro-motion.md](pro-motion.md) `picker-snap-level`) |

## 使用规则

- **阈值先行**:没有 `drag-lift-threshold` 的拖放会吃掉点击;点击与拖拽必须靠阈值分流
- **接受性先行**:目的地不显示接受反馈 = 用户默认这里不能放;禁止"放了才知道不行"
- **move/copy 语义可预期**:同容器移动/跨容器复制是用户心智默认;改默认必须给修饰键方案(Ctrl/Option 切换)并在拖影上可视化当前语义
- **不可撤销先确认**:放置导致数据不可恢复地丢弃时,先确认再执行;可撤销的失败走 `drop-fail-revert`
- **触屏侧发起细则**:长按浮起(带触觉反馈)后移动 >10px 才算发起拖拽,阈值内松手保留选中态;大对象拖影等比缩小防遮挡自身(排序场景除外——需原位对齐);多选拖拽聚拢成一摞并标数量角标;放置失败的双动画:目标在可见范围则归位原处,跨容器/不可见则原地放大淡出
- **框选/拖拽热区二分**:容器列表中对象本体(图标/标题区)=拖拽热区,行间与右侧空白=框选热区;框选内容类对象出现选框,文本类不出选框走原生文本选中(I-beam 指针)
- **滑动操作必须留可见启示**:chevron/标签/首次提示任选其一,禁纯隐形手势动作——发现不了的手势等于没有
- **键盘替代**:拖放排序必须提供键盘等价操作(上移/下移命令),无障碍口径见 [`../meta/accessibility.md`](../meta/accessibility.md)
- **触屏适配**:小目标的拖放把手(hit)独立于点击目标;把手不放大控件本身(口径同 [`../meta/ux-rules.md`](../meta/ux-rules.md) 触控条目)

## 在 draw-md 中的写法

```markdown
## DragDrop (board-kanban)
- threshold: { pattern: drag-lift-threshold, distance: 4px }
- semantics: { same-container: move, cross-container: move }   # 偏离默认需注明
- feedback: [drop-affordance, drop-fail-revert]
- extras: [drag-autoscroll, drop-keep-selection]
- keyboard-alternative: move-up / move-down commands
```
