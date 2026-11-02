# 工作区布局 —— maliang 产物的统一目录契约

> 规范层。定义 maliang 在**用户项目**里全部产物的落点:单根 `.maliang/`,交付产物与运行时状态同住一个家,按文件类分别决定入仓。2026-11-03 单根化(第三代布局);此前各命令文档书写的根 `DESIGN.md` + `design/`(第二代)与 `examples/`(第一代)产物路径,用户项目一律按本表映射为 `.maliang/`(本仓范例链接除外,见下)。

## 一个家,两类提交策略

| 类 | 位置 | 入仓 | 为什么 |
| --- | --- | --- | --- |
| 交付产物 | `.maliang/DESIGN.md` + `.maliang/{ui-markdown,preview,critique,ip,ip-handbook}/` | 是 | 页面规格/预览/评审快照要跨会话比对(ui-graph 哈希基线、critique 趋势),必须随仓提交 |
| 运行时状态 | `.maliang/` 下的运行态文件(逐条见 gitignore 建议) | 否(项目 gitignore) | receipts 会话收据「上一会话永不复用」、feedback 账本、build-log 是本地状态 |

单根裁决(2026-11-03,用户令):全部产物统一进 `.maliang/`,含 DESIGN.md。点目录是工具私有命名空间,协作者与工具默认识别其归属;代价是 DESIGN.md 不再位于仓库根(google/design.md 生态按根路径发现的约定随之失效,已知情裁决)。`.maliang/` 默认**提交**,仅运行态文件逐条 gitignore——不要整目录 ignore,否则交付产物会被静默排除出仓。

项目 `.gitignore` 建议:

```gitignore
.maliang/receipts/
.maliang/feedback/
.maliang/build-log.json
.maliang/preflight.json
.maliang/source-fingerprints.json
.maliang/progress.md
.maliang/direction-approved.md
```

## 用户项目布局(canonical)

```
<项目根>/
└── .maliang/            # maliang 产物统一目录(单根)
    ├── DESIGN.md        # 设计契约
    ├── facts.md         # design-md 事实核查台账(入仓)
    ├── ui-markdown/     # draw-md 产物:token.md + organisms/ + ui/*.md
    │                    #   + ui-graph 产出的 JSON 基线(清单以 ui-graph 命令文档为准)
    ├── preview/         # preview 产物:preview_<page>_<device>.html + 取证 report.json / shots/
    ├── critique/        # critique 产物:评分快照 <date>_<page>.md + a11y-walkthrough.md
    ├── ip/              # ip 产物:IP PNG / fallback prompt 文档(不覆盖旧产物)
    ├── ip-handbook/     # ip-handbook 产物:<project>/ 8 模块
    ├── direction-approved.md  # explore 方向门禁文件(运行态,gitignore)
    └── (运行态文件)      # receipts/ feedback/ build-log.json preflight.json
                         #   source-fingerprints.json progress.md
```

生成代码(draw-harmony / draw-flutter / draw-element)落用户项目自身源码目录,不在 `.maliang/` 下。

## 与本仓范例的映射

本仓(skill 仓)的开发夹具树 `examples/` 是第一代布局的历史实例(ci-gate 与 tests 指向,**不重命名**)。文档中指向本仓范例的**链接**(如 [`../../examples/ui-markdown/token.md`](../../examples/ui-markdown/token.md)、[`../../examples/design-system/heritage/DESIGN.md`](../../examples/design-system/heritage/DESIGN.md))均指本仓实例;用户项目按上表落 `.maliang/`。

## 存量项目兼容与迁移

- **旧路径识别兼容(三代候选)**:按 `.maliang/ui-markdown/` → `design/ui-markdown/` → `examples/ui-markdown/` 顺序取第一个存在的目录(preview、DESIGN.md 同理:`.maliang/DESIGN.md` → 根 `DESIGN.md`);命中旧代时按存量项目处理,并在交付说明里提示一次迁移(`git mv design/ui-markdown .maliang/ui-markdown` 等);用户拒绝则沿用旧路径并在 decisions 账本记录;
- 新项目一律 canonical 布局;receipts 初始化时已提示按上节把运行态文件逐条加入项目 `.gitignore`。

## 与其他文档的分工

- 判阶产物信号(theory-router §1)按本表路径取证据;审计收据(receipts)落 `.maliang/`,绑定对象是 `.maliang/` 下产物;
- 各命令文档的「产出落在 .maliang/…」表述以本表为 canonical 总图,单命令目录结构细节(如 ui-markdown/ 内部树)仍见各命令文档。
