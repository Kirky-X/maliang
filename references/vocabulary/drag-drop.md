# 拖放模式命名词汇

> 术语库。拖放是"按住-移动-放下"的直接操纵模式,本表标准化其触发阈值、语义与成败反馈命名。动效实现(排序重排/弹簧)见 [`../motion-skeletons/spring-reorder.md`](../motion-skeletons/spring-reorder.md);行内排序实例见 [`tables.md`](tables.md)。

## 命名表

| 模式名 | 构成要素(阈值/反馈) | 适用场景 |
| --- | --- | --- |
| `drag-lift-threshold` | 按住位移约 4px(3pt)后才出现拖影并进入拖动态 | 区分点击与拖拽;阈值内松手 = 点击,不触发拖放 |
| `drop-affordance` | 目的地可接受时才显示插入点/高亮,悬停即显、移开即消;不可接受时显示禁止符 | 一切拖放目标;接受性反馈是拖放的核心语言 |
| `drop-move-copy` | 同容器放下 = 移动;跨容器放下 = 复制;跨应用恒为复制 | 默认语义;偏离默认(如跨容器移动)需显式修饰键并在拖影上标注 |
| `drop-fail-revert` | 放置失败:拖影弹回源位置;不可恢复的丢弃用放大淡出"蒸发"且先确认 | 排序失败回弹;删除到回收站类可蒸发,直接销毁必须确认 |
| `drag-autoscroll` | 拖到容器边缘时自动滚动,继续暴露更远目标 | 长列表/画布内拖放 |
| `drop-keep-selection` | 放置后保留源选中态,供连续操作(再拖/再删) | 批量整理场景 |

## 使用规则

- **阈值先行**:没有 `drag-lift-threshold` 的拖放会吃掉点击;点击与拖拽必须靠阈值分流
- **接受性先行**:目的地不显示接受反馈 = 用户默认这里不能放;禁止"放了才知道不行"
- **move/copy 语义可预期**:同容器移动/跨容器复制是用户心智默认;改默认必须给修饰键方案(Ctrl/Option 切换)并在拖影上可视化当前语义
- **不可撤销先确认**:放置导致数据不可恢复地丢弃时,先确认再执行;可撤销的失败走 `drop-fail-revert`
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
