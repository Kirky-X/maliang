# 撤销重做模式命名词汇

> 术语库。撤销是"命令级历史回退"的一组模式,与页面状态的删除防护(states.md `state-destructive-undo` 三段式)互补:那个管"破坏性动作的前置确认+撤销 toast+焦点恢复",本篇管命令历史的可预期性与可见性。两者共用同一 undo toast 载体,不得实现两套。

## 命名表

| 模式名 | 构成要素(触发/反馈) | 适用场景 |
| --- | --- | --- |
| `undo-named` | 撤销/重做入口标注具体操作名("撤销重命名"而非泛"撤销") | 一切可撤销操作;命名让用户确认撤的就是刚才那步 |
| `undo-visible` | 撤销生效后滚动到位并高亮受影响对象 | 目标已不在视野内时;防止用户误以为无效而连按 |
| `undo-batch` | 相关的连续微调合并为一个撤销单元;支持回到打开/保存点 | 拖拽排序、连续改色等高频微操作;批量回退省去 N 次单步 |
| `undo-unbounded` | 自上个逻辑节点起不限撤销次数 | 编辑器/文档/画布类;人为限制次数是任意惩罚 |

## 使用规则

- **可预期**:撤销菜单/按钮永远标注结果名;泛"撤销"只允许在无上下文空间时退化使用
- **可见**:撤销/重做后受影响内容必须在视野内(自动滚动+高亮);用户不应靠猜测验证撤销是否生效
- **合并粒度 = 用户心智动作**:一次"拖动卡片到顶部"是 1 个撤销单元,不管内部改了几处数据;跨逻辑动作不合并
- **不限次数**:从最近保存点/会话起点起所有命令可撤;重做栈在撤销后新动作进入时才清空
- **与 destructive-undo 分工**:删除类破坏动作走 states.md 三段防护(前置确认→undo toast→焦点恢复);普通命令错误直接 `undo-named` 回退,不弹确认
- **键盘惯例**:Ctrl/Cmd+Z 撤销、Shift+Ctrl/Cmd+Z 重做;redo 的修饰键角色见 [`../meta/ux-rules.md`](../meta/ux-rules.md) 键盘条目

## 在 draw-md 中的写法

```markdown
## Undo
- patterns: [undo-named, undo-visible, undo-batch]
- scope: session-since-last-save
- shortcut: { undo: mod+z, redo: shift+mod+z }
- destructive-actions: route-through state-destructive-undo
```
