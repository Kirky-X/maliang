# 工作区布局 —— maliang 产物的统一目录契约

> 规范层。定义 maliang 在**用户项目**里全部产物的落点:交付物入可见目录,运行时状态入点目录。2026-10-25 建立;此前各命令文档书写的 `examples/` 产物路径,用户项目一律按本表映射为 `design/`(本仓范例链接除外,见下)。

## 两类文件,两个家

| 类 | 目录 | 入仓 | 为什么 |
| --- | --- | --- | --- |
| 交付产物 | 根 `DESIGN.md` + `design/` | 是 | 页面规格/预览/评审快照要跨会话比对(ui-graph 哈希基线、critique 趋势),必须随仓提交 |
| 运行时状态 | `.maliang/` | 否(项目 gitignore) | receipts 会话收据「上一会话永不复用」、feedback 账本、build-log 是本地状态 |

点目录惯例上是工具私有状态:协作者不看、部分工具忽略点目录——**交付物禁入点目录**,这是交付物不并入 `.maliang/` 的原因。

## 用户项目布局(canonical)

```
<项目根>/
├── DESIGN.md            # 设计契约,留根:google/design.md 生态按仓库根路径发现(agent-first)
├── design/              # maliang 交付产物统一目录
│   ├── ui-markdown/     # draw-md 产物:token.md + organisms/ + ui/*.md
│   │                    #   + ui-graph 产出的 JSON 基线(清单以 ui-graph 命令文档为准)
│   ├── preview/         # preview 产物:preview_<page>_<device>.html + 取证 report.json / shots/
│   ├── critique/        # critique 产物:评分快照 <date>_<page>.md + a11y-walkthrough.md
│   ├── ip/              # ip 产物:IP PNG / fallback prompt 文档(不覆盖旧产物)
│   └── ip-handbook/     # ip-handbook 产物:<project>/ 8 模块
└── .maliang/            # 运行时状态(项目 .gitignore 加 .maliang/)
    ├── receipts/        # 测量收据 <session>.jsonl
    ├── feedback/        # 反馈账本
    └── build-log.json   # 跨次构建记忆(轮换/盖章)
```

生成代码(draw-harmony / draw-flutter / draw-element)落用户项目自身源码目录,不在 `design/` 下。

## 与本仓范例的映射

本仓(skill 仓)的开发夹具树 `examples/` 是同一布局的历史实例(ci-gate 与 tests 指向,**不重命名**)。文档中指向本仓范例的**链接**(如 [`../../examples/ui-markdown/token.md`](../../examples/ui-markdown/token.md)、[`../../examples/design-system/heritage/DESIGN.md`](../../examples/design-system/heritage/DESIGN.md))均指本仓实例;用户项目按上表落 `design/`。

## 存量项目兼容与迁移

- **旧路径识别兼容**:发现 `examples/ui-markdown/` 存在而 `design/ui-markdown/` 不存在时,按存量项目处理(读旧路径),并在交付说明里提示一次迁移(`git mv examples/ui-markdown design/ui-markdown` 等);用户拒绝则沿用旧路径并在 decisions 账本记录;
- 新项目一律 canonical 布局;receipts 初始化时已提示把 `.maliang/` 加入项目 `.gitignore`。

## 与其他文档的分工

- 判阶产物信号(theory-router §1)按本表路径取证据;审计收据(receipts)落 `.maliang/`,绑定对象是 `design/` 下产物;
- 各命令文档的「产出落在 design/…」表述以本表为 canonical 总图,单命令目录结构细节(如 ui-markdown/ 内部树)仍见各命令文档。
