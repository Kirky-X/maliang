# 菜单设计模式命名词汇

> 术语库。菜单是"把不常驻界面的命令收进按需展开的列表"的一组模式,本表标准化其形态命名与条目纪律。与按钮(buttons.md)、表单选择(forms.md)、导航(navigation.md)互补。

## 命名表

| 模式名 | 构成要素(触发/形态/语义) | 适用场景 |
| --- | --- | --- |
| `menu-dropdown` | 点击触发,展开动作/选项列表,常带勾选态与分组分隔线 | 工具栏"更多"动作、视图选项切换;≥3 项才值得做菜单,1-2 项直接用按钮/开关 |
| `menu-context` | 右键/长按触发,锚定目标对象,展示高频相关命令 | 对象级快捷操作;只放高频项,不放高级/低频项——默认藏起来的东西用户不知道存在 |
| `menu-edit` | 选区触发(右键或浮动条),展示复制/粘贴等编辑命令,按上下文裁剪 | 文本/内容选区;未选中不显示复制,无可粘贴内容不显示粘贴;正文与图注可复制,控件标签不可 |
| `menu-pulldown` | 按钮形态触发,展开后可含动作、多选、子菜单 | 与 `menu-dropdown`(互斥单选)的分界:需要放动作/多选/子菜单时用 pulldown |
| `menu-submenu` | 父项悬停/点击展开二级列表 | 同一词在 ≥3 个菜单项重复出现时收拢(Sort by Date/Score/Time → Sort by ▸);只 1 层、≤5 项 |
| `menu-toggle-item` | 单条开关项,标签随状态切换(Show Map ↔ Hide Map) | 布尔切换;语义不清时用动词式(Turn HDR On) |
| `menu-check-group` | 属性组勾选:组内标示生效项,配一条"全部清除"项 | 互斥属性集合(字体样式 Plain/Bold/Italic) |

## 使用规则

- **文案**:菜单项用动词或动词短语、title case、删冠词(View Settings,不是 View the Settings);需要用户补输入的动作标题尾加省略号(Export… 表示还会弹对话框)
- **分组 ≤ 3 组**:用分隔线分组,相关命令同组(Paste 与 Paste and Match Style 同组);破坏性项置尾并用危险色
- **不可用项处理**:常规菜单置灰禁用(让人知道有此命令);右键菜单直接隐藏不可用项(空间宝贵,复制/剪切/粘贴例外,保持置灰);全部项不可用时菜单本身仍可打开
- **子菜单纪律**:只 1 层、≤5 项;不可用时子菜单本身仍显示但项置灰;禁止用缩进排版冒充子菜单
- **右键菜单三纪律**:①只放高频相关项;②菜单项必须同时存在于主界面(右键是捷径,不是唯一入口);③分组 ≤3 组
- **图标全有或全无**:一组菜单项要么全配图标,要么全不配;找不到准确达意的图标就不放
- **与 forms.md 分界**:菜单承载命令与选项切换;字段取值(表单内选一个值)走 forms.md 的 select 连续谱
- **与 popups.md 分界**:menu 是用户主动展开;动作引发的选择分支用 action sheet(见 popups.md 浮层选型)

## 在 draw-md 中的写法

```markdown
## Menu (toolbar overflow)
- pattern: menu-pulldown
- items: [{ label: "导出…", ellipsis: true }, { label: "重命名" }, { divider: true }, { label: "删除", destructive: true }]
- groups: ≤3, labels: verb-phrase, title-case
- unavailable: dim (context: hide)
```
