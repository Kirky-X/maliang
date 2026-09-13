# FAB API

> FAB 组合方案(Element Plus)的规格参数与实现约定。用法见 [component.md](./component.md)。

## 组合方案规格参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `icon` | `Component` | — | 内容图标(`Plus` / `Edit` 等) |
| `label`(扩展 FAB) | `string` | — | 胶囊文案("写邮件""发布") |
| `position.right / bottom` | `px` | `24` / `48` | 定位(有 dock 时上移避让) |
| `size` | `number` | `56`(圆形) / `48`(胶囊高) | 触控尺寸 |
| `z-index` | token | `{z-index-modal}` | 悬浮层级 |
| `aria-label` | `string` | 必填 | 动作语义(如"新建笔记") |
| `scroll-behavior` | `up-show \| down-show \| always` | `up-show` | 滚动联动策略 |

## el-button 关键属性(FAB 本体)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `circle` | `boolean` | `false` | 圆形(标准 FAB) |
| `size` | `'large' \| 'default' \| 'small'` | `'large'` | 尺寸(large 40px,外层补到 56px) |
| `type` | `'primary' \| ...` | — | 建议 `primary` 承载一级动作 |
| `aria-label` / `aria-disabled` | `string` / `boolean` | — | 无障碍语义(图标按钮必填) |

## 与相邻组件的分工

| 维度 | FAB(本类) | `el-backtop` | 页面主按钮 |
| ---- | ----------- | ------------ | ---------- |
| 语义 | 一级动作入口(新建/发布) | 回到顶部 | 表单提交/区块 CTA |
| 位置 | 右下悬浮 | 右下(滚动后出现) | 内容流内 |
| 数量 | 每页 0-1 个 | 至多 1 个 | 不限 |

## 关键规格要点

- **单 FAB 原则**:每页最多 1 个,承载唯一一级操作;多动作收进点击菜单或底部 sheet。
- **滚动联动**:上滑显示、下滑收起(或反向,按页面任务选),过渡 200ms;列表顶部时必显示。
- **避让**:有底部 dock 上移(dock 高 + 24px);有侧栏右移(侧栏宽 + 24px);不遮内容关键操作。
- **层级**:`z-index` 用 `{z-index-*}` token,低于 dialog/popover。
- **无障碍**:`aria-label` 必填;焦点可见(focus-visible ring);禁用态用 `aria-disabled` + 视觉灰。
