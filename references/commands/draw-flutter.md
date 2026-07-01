# draw-flutter 子命令 —— 将逻辑 UI 转换为 Flutter(Dart)实现

> 本文件是 `draw-flutter` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 输入 = `draw-md` 产出的页面级 UI markdown(`examples/ui-markdown/` 下),输出 = Flutter Dart 框架实现代码。
> 组件映射参考 [`framework/flutter/`](../framework/flutter/) 下的组件文档。

---

## 流程概览(三段式)

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  1. 输入解析      │ -> │  2. 组件映射      │ -> │  3. 产出校验      │
│  读取 draw-md 产出 │    │  查 framework 文档 │    │  Flutter API + token │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## 1. 输入解析

读取 `draw-md` 产出的页面 markdown(位于 `examples/ui-markdown/ui/` 下):

1. **解析 frontmatter** — 提取 `name`、`description`、`background`、`updated`、`version`
2. **解析 token.md** — 读取 `examples/ui-markdown/token.md`,建立 token 名→硬值映射表(颜色/字体/间距/圆角)
3. **解析布局章节** — 按"顶部导航 → 主体区块 → 底部 dock"顺序,逐章提取组件类型(按钮/文本/列表/...)与参数表

**⚑ 输入解析确认检查点**:确认已解析出页面布局章节 + 组件参数表 + token 引用清单(逻辑组件 → Flutter Widget 预映射),再进入组件映射阶段。

---

## 2. 组件映射

逐组件查 [`framework/flutter/`](../framework/flutter/) 文档,将逻辑组件映射为 Flutter Widget:

### 组件映射表

| 逻辑组件(draw-md) | Flutter Widget | 框架文档 |
| ------------------- | -------------- | -------- |
| button | `ElevatedButton` / `TextButton` / `OutlinedButton` / `FilledButton` | [widget.md](../framework/flutter/button/widget.md) + [properties.md](../framework/flutter/button/properties.md) |
| text | `Text` / `RichText` / `Text.rich` | [widget.md](../framework/flutter/text/widget.md) + [properties.md](../framework/flutter/text/properties.md) |
| list | `ListView` / `ListView.builder` / `ListTile` | [widget.md](../framework/flutter/list/widget.md) + [properties.md](../framework/flutter/list/properties.md) |
| image | `Image` / `Image.asset` / `Image.network` | [widget.md](../framework/flutter/image/widget.md) + [properties.md](../framework/flutter/image/properties.md) |
| input | `TextField` / `TextFormField` | [widget.md](../framework/flutter/input/widget.md) + [properties.md](../framework/flutter/input/properties.md) |
| navigation bar | `AppBar` / `BottomNavigationBar` | (参考 organisms/) |

### Token 映射规则

| draw-md token 引用 | Flutter 实现 |
| ------------------- | ------------ |
| `{color-primary}` | `Color(0xFF...)` 或 `Theme.of(context).colorScheme.primary` |
| `{font-size-md}` | `FontSize(16)` 或 `Theme.of(context).textTheme.bodyMedium?.fontSize` |
| `{spacing-md}` | `SizedBox(width: 16)` / `EdgeInsets.all(16)` |
| `{radius-md}` | `BorderRadius.circular(8)` |

> 优先使用 `ThemeData` 集中管理 token,若无主题系统则降级为硬值(从 token.md 解析)。

### 映射步骤

1. 识别组件类型 — 从参数表的组件名推断(如"按钮"→ElevatedButton/TextButton)
2. 查框架文档 — 读 `framework/flutter/<component>/widget.md` 获取 Widget 定义,读 `properties.md` 获取属性表
3. 填充属性 — 将 draw-md 参数表的值(token 引用)映射为 Flutter Widget 属性
4. 生成代码 — 产出 `StatelessWidget` 或 `StatefulWidget`,含 `build()` 方法

**⚑ Flutter 代码生成确认检查点**:确认每个组件都已映射到 Flutter Widget,所有 token 引用点已用 {token-name} 格式标注(无裸值),再进入产出校验。

---

## 3. 产出校验

生成 Flutter Dart 代码后,执行自检:

- [ ] 所有 Widget 使用正确的 Flutter Material 3 语法(`StatelessWidget` / `StatefulWidget` / `build()`)
- [ ] 颜色值已从 token 映射为 `Color()` 或 `ThemeData`,无 `{token-name}` 占位符残留
- [ ] 布局结构符合 draw-md 章节顺序(顶部导航 → 主体 → 底部 dock)
- [ ] Widget 属性与 `framework/flutter/` 文档一致(无杜撰 API)
- [ ] 产出文件含注释标注来源(`// 由 draw-flutter 从 <page>.md 生成`)
- [ ] import 语句完整(`package:flutter/material.dart` 等)

**⚑ 校验通过确认检查点**:确认无裸值、无悬空 token、组件映射完整,Flutter Dart 代码方可交付使用。

---

## 产出物

- 一个页面 → 一个 Dart 文件(`class <PageName>Page extends StatelessWidget/StatefulWidget`)
- 跨页面复用组件 → 单独 Widget 文件(被各页面 import)
- 文件命名:`<page_name>_page.dart`(如 `home_page.dart`、`setting_about_page.dart`)

---

## 约束汇总(硬性)

- [ ] 输入必须是 draw-md 产出(含 frontmatter + 参数表 + token 引用),MUST NOT 直接从 DESIGN.md 跳过 draw-md
- [ ] 组件映射 MUST 查 `framework/flutter/` 文档,MUST NOT 凭记忆杜撰 Flutter Widget API
- [ ] Token 引用 MUST 解析为具体值(`Color()` 或 `ThemeData`),MUST NOT 在产出代码中残留 `{token-name}` 占位符
- [ ] 产出代码 MUST 可通过 `dart analyze`(语法正确、import 完整、类型安全)

---

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
| -------- | -------- | ---------- |
| DESIGN.md 缺失关键 token(如无 color.text) | 列出缺失 token 清单,询问用户补全 | 用 `{color-text-primary}` 等标准命名占位,标注"假设值,需 DESIGN.md 确认" |
| UI markdown 缺少 token 引用(裸值) | 提示具体偏差(哪些值未引用 token) | 用 DESIGN.md 中的 token 替换裸值,标注"自动补全,需确认" |
| 组件无对应 Flutter Widget 文档(framework/flutter/ 无对应类型) | 在 index.md 索引表查最接近类型 | 用基础 Widget(Text/ElevatedButton/ListView)组合实现,标注"组合方案" |
| Flutter 代码编译报错(Widget 嵌套/类型错误) | 提示具体编译错误及修复方向 | 引导用户简化 UI markdown(移除复杂组件)后重试 |
