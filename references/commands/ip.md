# ip 子命令 —— 从 DESIGN.md 调性生成 IP 形象

> 本文件是 `ip` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 输入 = 项目根目录的 [`DESIGN.md`](./design-md.md) 产出物(YAML frontmatter 含 colors/typography/keywords + 正文风格描述)。
> 输出 = **IP 形象 PNG 图片** 或 **结构化 prompt 文档(API 不可用时 fallback)**,落在 `examples/ip/` 下。
> 这是 [`design-md`](./design-md.md) 的**下游**:design-md 产出 DESIGN.md 定义品牌调性,ip 基于调性生成与品牌一致的 IP 形象,不修改 DESIGN.md。
> 调用通道 = `text_to_image` API,agent 运行时通过 WebFetch / run_mcp 工具发起 HTTP 请求。

---

> **CHECKPOINT 与无人值守**:无人值守时按 [`SKILL.md`](../../SKILL.md)「无人值守与 CHECKPOINT 降级」节的默认取值表执行,不逐点阻塞;自选决定与理由写入交付说明。

## 产物层目录结构

所有 ip 产出落在 `examples/ip/`:

```
examples/ip/
├── <project-name>-ip.png                    # IP 形象图片(API 可用,3:4 比例)
├── <project-name>-ip-<YYYYMMDD-HHMMSS>.png  # 重画/多轮产出:新路径,不覆盖上一版
└── <project-name>-ip-prompt.md              # 结构化 prompt 文档(API 不可用 fallback)
```

- `<project-name>` 取自项目根目录名(kebab-case),与 DESIGN.md 所在项目对齐。
- 正常路径:仅产出 `-ip.png`;**重画或批量产出一律新路径**(时间戳/序号后缀),不静默覆盖旧产物。
- Fallback 路径:仅产出 `-ip-prompt.md`,文档内含完整 8 维 prompt + 生成参数(CFG/步数/种子),供人工或外部工具离线生成。

---

## IP 形象 prompt 契约(8 维度齐全)

每份 IP 形象生成请求 MUST 含以下 8 个维度,缺一不可:

| 维度        | 字段 key        | 说明                                                | 示例                                    |
| ----------- | --------------- | --------------------------------------------------- | --------------------------------------- |
| 主体描述    | `subject`       | IP 形象的主体(物种/拟人化程度/性别/年龄段)         | 一只拟人化的橘猫,圆脸大眼,年龄 6-8 岁   |
| 风格        | `style`         | 与 DESIGN.md 调性一致(扁平/拟物/3D/极简/手绘)      | 极简扁平化,圆润线条,柔和过渡            |
| 构图        | `composition`   | 视角(正面/侧面/3/4 视角)+ 景别(胸像/全身)         | 3/4 视角,全身构图,居中                  |
| 光线        | `lighting`      | 光线类型(柔和/锐利/逆光/侧光)+ 方向               | 柔和顶光,轻微逆光勾勒轮廓               |
| 色彩        | `palette`       | 主色 HEX + 辅助色 HEX(必来自 DESIGN.md)            | 主色 #007DFF / 辅助色 #FFAA00            |
| 背景/交付形态 | `background`  | `scene`(背景烘进画面)或 `isolated`(单主体透明底 PNG,可直接叠放) | isolated:单主体置于完全透明背景 |
| 比例        | `aspect_ratio`  | 固定 `3:4`(对应 API 参数 `image_size=portrait_4_3`)| 3:4                                     |
| 负向提示词  | `negative`      | 需避免的元素(多余手指/文字水印/模糊/低质)         | 多余手指,文字水印,模糊,低分辨率,变形    |

- `palette` 字段的色值 **MUST 来自 DESIGN.md frontmatter 的 colors**,禁止凭空生成。
- `background` 默认 `isolated`——"放到我的网站/贴纸/叠加"类用途都是 cutout;只有明确要重新生成构图与氛围(hero 图/整幅插画)才用 `scene`。
- `aspect_ratio` 固定为 `3:4`,与 API 参数 `image_size=portrait_4_3` 严格对齐。
- 8 维度缺失任一即视为不合规 prompt,需补全后再调用 API。

### 交付形态与透明底防御(background 维度展开)

> 来源:anydesign element-copy(asset 交付形态),2026-10 吸收。

**isolated 提示词的两类失败模式,按防御写法写**:

1. **提示词里写「透明背景」不可靠(prose transparency is unreliable)**——多数模型照常画背景。可靠路径是 **API 参数**(gpt-image:`background:"transparent"`);Midjourney 无真 alpha;SD/Flux 视管线而定,不能按散文承诺。
2. **氛围词会召唤回背景与投射**:world/atmosphere 词("环境填充""夜景氛围""xxx 色光")会让模型把整个氛围画出来;风格词库暗示世界观时还会加塞其他角色与道具。

因此 isolated 写法三条:**隔离指令前置**(「单主体置于完全透明背景:只有一个 X,画面里没有别的——没有场景、没有其他角色、没有道具、没有地面、没有落地阴影」);**剥掉所有 world/atmosphere 词**(光线只留中性的"柔和摄影棚主光");**AVOID 块以「no background of any kind」收尾**。

**chroma-key 兜底**(透明仍失败时):让主体站在调色板**之外**的纯色 chroma 背景上(如纯 `#00FF00`,注明「完全均匀、无渐变、无暗角」),后期按容差抠成 alpha。

**透明校验**:PNG 扩展名、RGBA 模式、画入的棋盘格都**不能证明透明**——须程序识别真 alpha 像素,并检查背景是否完整移除、主体有无误删、细线是否残留色边。

---

## 流程

0. **读取 DESIGN.md 提取调性** —— 读取项目根目录的 `DESIGN.md`,解析 YAML frontmatter,提取以下字段:
   - `colors`:主色(primary)、辅助色(secondary)的 HEX 值
   - `typography`:字体族(font-family,如 HarmonyOS Sans / Inter / Roboto)
   - `keywords` / `description`:情感基调关键词(如"专业/温暖/科技感/可信赖")

   **🔴 CHECKPOINT · DESIGN.md 提取**:确认 DESIGN.md 存在且 frontmatter 解析成功,再进入下一步。若 DESIGN.md 缺失,走「失败模式与 fallback」表中的对应策略。

1. **提取调性关键词** —— 将 DESIGN.md frontmatter 字段归并为 4 元调性向量:
   - **主色 HEX** — 取 `colors.primary`(缺失时默认 `#007DFF`)
   - **辅助色 HEX** — 取 `colors.secondary`(缺失时默认 `#FFAA00`)
   - **字体风格** — 取 `typography.font-family`(缺失时默认 `HarmonyOS Sans`)
   - **情感基调** — 取 `keywords` 与 `description` 合并去重(缺失时默认 `专业可信赖`)

   缺失字段使用上述合理默认值,但在最终 prompt 文档中 MUST 标注 "(default)" 后缀以示来源。

2. **构造 IP 形象 prompt(8 维度)** —— 基于调性向量构造完整 prompt:
   - `subject`:从用户输入或 DESIGN.md `description` 推断主体(如"一只拟人化的猫")
   - `style`:与 DESIGN.md 调性一致(情感基调=温暖 → 圆润线条;科技感 → 几何线条)
   - `composition`:默认 `3/4 视角,全身构图,居中`
   - `lighting`:默认 `柔和顶光,轻微逆光勾勒轮廓`(科技感可改 `锐利侧光`)
   - `palette`:主色 + 辅助色 HEX(必来自步骤 1)
   - `background`:默认 `isolated`(单主体透明底);需要整体氛围构图时用 `scene`;透明底走 API 参数,不靠提示词承诺(防御写法见契约节)
   - `aspect_ratio`:固定 `3:4`
   - `negative`:默认 `多余手指,文字水印,模糊,低分辨率,变形,过度复杂背景`;isolated 时以 `no background of any kind` 收尾

   **🔴 CHECKPOINT · 8 维度齐全**:确认 8 个维度全部填写,`palette` 来自 DESIGN.md,`background` 形态已判定,再进入 API 调用。

3. **调用 text_to_image API** —— 将 8 维 prompt 拼接为单行字符串(用逗号分隔),URL 编码后调用:
   ```
   https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=<url-encoded>&image_size=portrait_4_3
   ```
   - agent 运行时通过 `WebFetch` / `run_mcp` 工具发起 HTTP GET。
   - 返回的图片二进制落地为 `examples/ip/<project-name>-ip.png`。**落盘与自检三条**:
     - **新路径不覆盖**:目标路径已存在时改用带时间戳/序号的新路径(`<project-name>-ip-<YYYYMMDD-HHMMSS>.png`),不静默覆盖旧产物
     - **实际打开图片核对**:生成后打开图片检查主体 / 风格 / 配色与 DESIGN.md 调性一致,记录待修正项——只验"文件存在且非空"不算自检
     - **记录生成档案**:模型 / 提示词 / 真实尺寸 / 待修正项写进产物说明或 prompt 文档;对结果不满意的重画算**新的生成**,不伪装成网络重试
   - 若项目名未知,取 `DESIGN.md` 所在目录名(kebab-case)。

   **🔴 CHECKPOINT · 图片落地**:确认 PNG 已写入**新路径**、已实际打开核对、生成档案已记录,再交付。若 API 返回错误或超时,走步骤 4 fallback。

4. **Fallback 结构化 prompt 文档**(API 不可用时) —— 当步骤 3 API 调用失败(网络错误 / 鉴权失败 / 超时 / 返回非图片),产出 markdown 文档 `examples/ip/<project-name>-ip-prompt.md`,内容含:
   - **正向提示词**(8 维度完整拼接,中英双语)+ **散文版**(同一内容一段话,gpt-image / DALL-E 类模型更吃散文),hex 一个不漏
   - **负向提示词**
   - **逐模型适配注记**:gpt-image / DALL-E 用散文版原样;Midjourney 压缩为逗号短语 + `--ar 3:4`(`--style raw`),**无真 alpha**,透明底走纯色 chroma + 后期抠图;SD / Flux 按结构化字段转逗号标签,AVOID 块移入 negative prompt 字段
   - **生成参数建议**:
     - CFG scale:7-8
     - 采样步数:30-50
     - 种子建议:随机或固定(如 42)
     - 采样器:DPM++ 2M Karras 或 Euler a
     - 图片尺寸:2048×2732(3:4 比例,2K 高清)
   - **调性来源声明**:列出引用的 DESIGN.md 字段与默认值

   **🔴 CHECKPOINT · Fallback 完成**:确认 prompt 文档含完整 8 维 + 散文版 + 逐模型适配注记 + 生成参数,交付给用户人工或外部工具离线生成。

---

## 约束汇总(硬性)

- [ ] prompt MUST 含 8 维度齐全(subject/style/composition/lighting/palette/background/aspect_ratio/negative)
- [ ] `palette` 主色与辅助色 HEX MUST 来自 DESIGN.md frontmatter `colors`
- [ ] `aspect_ratio` 固定 `3:4`,对应 API 参数 `image_size=portrait_4_3`
- [ ] 调性(色彩/字体/情感)MUST 来自 DESIGN.md,禁止凭空生成
- [ ] 缺失字段使用默认值时 MUST 在 prompt 文档中标注 "(default)"
- [ ] API 可用路径产出 PNG,API 不可用路径产出 prompt markdown,二选一
- [ ] 产出物落在 `examples/ip/` 目录;重画/多轮产出 MUST 落新路径(时间戳/序号),不覆盖旧产物
- [ ] 生成后 MUST 实际打开图片核对并记录生成档案(模型/提示词/真实尺寸/待修正项),只验"文件非空"不算自检
- [ ] cutout 用途(贴纸/叠加/网站素材)MUST 走 `isolated` 形态;提示词写「透明」不构成证明,须程序校验真 alpha,失败按 chroma-key 兜底并如实标注

---

## 失败模式与 fallback

| 触发条件                                   | 一线修复                                              | 仍失败兜底                                                |
| ------------------------------------------ | ----------------------------------------------------- | --------------------------------------------------------- |
| DESIGN.md 缺失(项目根目录无该文件)        | 提示用户先执行 [`design-md`](./design-md.md) 生成     | 用全默认调性(主色 #007DFF / 辅助 #FFAA00 / 情感"专业可信赖"),并在产出物顶部明确标注"调性来源:default,非 DESIGN.md" |
| DESIGN.md frontmatter 缺失 colors 字段     | 列出缺失字段,询问用户补全 DESIGN.md                  | 用默认主色 #007DFF + 辅助 #FFAA00,在 prompt 文档标注 "(default)" |
| DESIGN.md frontmatter 缺失 typography      | 同上                                                  | 用默认字体 HarmonyOS Sans,标注 "(default)"                |
| text_to_image API 返回错误(4xx/5xx)        | 重试 1 次,确认 URL 编码正确                           | 走步骤 4 fallback 产出 prompt markdown                    |
| API 返回非图片内容(如 JSON 错误)          | 检查响应 Content-Type,确认 endpoint                   | 走步骤 4 fallback 产出 prompt markdown                    |
| API 超时(>30s 无响应)                     | 重试 1 次,延时至 60s                                  | 走步骤 4 fallback 产出 prompt markdown                    |
| 8 维 prompt 不全(缺 background / 负向提示词等) | 列出缺失维度,补全后再调用                             | 拒绝调用 API,提示用户补全 prompt                          |
| 目标路径已有旧产物                          | 改用带时间戳/序号的新路径重生成                       | 同上;禁止覆盖旧产物,禁止为省事复用旧图                   |
| isolated 透明底失败(生成图仍带背景)        | 走 API 参数 `background:"transparent"`;仍失败改 chroma-key 后台生成后抠图 | 如实标注「底色需后期处理」,不冒称透明 PNG                 |
| 项目名无法推断                             | 取 `DESIGN.md` 所在目录名(kebab-case)                | 用 `default-ip` 作为文件名,提示用户重命名                 |

---

## 禁止事项(反例)

- **禁止凭空生成调性**(如自创主色 #FF0000、自创情感"年轻活力"):IP 形象必须与 DESIGN.md 调性一致,脱离调性会导致品牌割裂。MUST 从 DESIGN.md frontmatter 提取,缺失字段用默认值并标注。
- **禁止跳过 DESIGN.md 直接构造 prompt**:跳过会让 IP 形象脱离项目设计系统。MUST 先执行步骤 0 读取 DESIGN.md,即使全用默认值也要在产出物中声明调性来源。
- **禁止 8 维 prompt 缺维**(如只写 subject + style):缺维会让 API 输出不可控。MUST 8 维度齐全,缺一即拒绝调用 API。
- **禁止用非 3:4 比例**(如 16:9 / 1:1):IP 形象统一比例便于后续手册延展。MUST `image_size=portrait_4_3`,固定 3:4。
- **禁止 API 失败时静默无产出**:API 不可用时必须走步骤 4 fallback 产出 prompt markdown,严禁只报错不交付。MUST 二选一产出(PNG 或 prompt md)。
- **禁止为复制第三方 logo / 吉祥物 / 角色设计出 prompt**:第三方品牌识别性美术(logo、吉祥物、角色设计)不得作为 prompt 复制目标——只描述「共享风格词汇的原创主体」(原创角色、共享风格与调色板),并在 prompt 文档注明原创声明。与 [`../meta/visual-assets.md`](../meta/visual-assets.md)「禁止生成人像冒充真实背书」同源口径。
