# Token 溯源 —— 让每个 token 都能回答「它为什么存在」

> 规范层。DESIGN.md 最常见的病是 token 只有值没有来由:改它没人知道能不能改,评审只能靠「看着顺眼」争论,跨会话后新做的会话根本看不出某值是深思熟虑还是随手填的。本文给 token 加一条**反向索引**——每个 token 值指回产生它的那条设计决策的 id。
>
> 决策 id 的字段定义与 `decisions` 账本写法见 [`spec-schema.md`](spec-schema.md);本文只管溯源约定与违规判据。机制来源:oh-my-design 的 derivation chain(工作顺序「先立原则 → 写决策表 → 决策落 token 并反向引用」,MIT,2026-09 吸收,中文自研)。

---

## 1. 为什么需要

没有溯源的 token 有三种典型死法:

| 死法                 | 表现                                                             | 代价                                       |
| -------------------- | ---------------------------------------------------------------- | ------------------------------------------ |
| **即兴值**           | 同一个语义在两个页面取了两个值,都能画通,没人知道哪个是有意的   | 视觉漂移在评审时无法定性,只能返工         |
| **装饰性 token**     | token 存在是因为「设计系统应该有这一项」,不是任何取舍的结果     | 删它没人敢,留着没人用,规模只增不减         |
| **决策蒸发**         | 决策当初写在会话里没落盘,值留下了,理由没了                     | 半年后没人敢动这个值,改版成本永久升高     |

溯源把「值」和「取舍」绑在一起:有 id 的 token 是决定,没 id 的 token 是待解释的意外。

---

## 2. 决策 id 编号规则

```
D-P<原则序号>-<决策序号>
```

- `P<原则序号>` 指向 DESIGN.md `## Overview` 里声明的立场/原则(P1 / P2 / P3,2–3 条为宜,写多于 3 条说明原则没分清层)
- `<决策序号>` 在该原则下从 1 递增,只增不复用:决策被推翻后 id 保留在账本里标 `status: superseded`,**不复用编号**
- 原则号不可重排。P1 被推翻后新原则接 P4,不占 P1

**一个决策可覆盖一族 token**,这是正常写法:

```yaml
# D-P1-2 覆盖:中性色阶承担 99% 视觉负载,强调色只出现在交互点
secondary: "#9D9D9D" # D-P1-2
neutral: "#F5F5F5" # D-P1-2
surface: "#FFFFFF" # D-P1-2
tertiary: "#2563EB" # D-P1-1
```

**但一族必须同源**。把「蓝色 CTA」和「8px 网格」塞进同一条决策(靠一句万能理由)等于没溯源——判断标准:能说清「改这个值会连带推翻哪条取舍」,说清不了就拆成两条。

---

## 3. 溯源写法

溯源写在 **YAML 行尾注释**,位于值之后:

```yaml
colors:
  primary: "#212121" # D-P1-1
  tertiary: "#2563EB" # D-P1-1
typography:
  body-md:
    fontSize: 16px # D-P3-1
    lineHeight: 1.6 # D-P3-1
```

> ⚠️ **颜色值必须加引号**。YAML 里 `#` 只有在前置空白或行首时才起注释作用,`primary: #212121` 会被解析成空值而不是注释加颜色。加引号(`"#212121"`)是溯源能生效的前提,也是 `spec-schema.md` 颜色 token 节本就要求的写法。

行尾注释也可写原因短句,便于单点 review,但**不替代** id:

```yaml
  tertiary: "#2563EB" # D-P1-1 全屏至多一处,稀缺即信号
```

### 逃逸口:`no-decision`

不是所有 token 都有本地决策。以下两类用 `no-decision:` 显式声明,而不是随手编一个 id:

| 写法                        | 适用                                                          |
| --------------------------- | ------------------------------------------------------------- |
| `# no-decision: <继承来源>` | 继承品牌规范 / 上游设计系统 / 参考物的既定值,本项目不重新裁决 |
| `# no-decision: <提取来源>` | 1A 流程从既有代码/截图提取的原值,尚未重新裁决               |

`no-decision` 是**待办标记**,不是免责金牌:一个 DESIGN.md 里 `no-decision` 占比过高(> 1/3 的 token 键)说明这次没做定义阶段,应回 Phase 0 重走,而不是把 `no-decision` 铺满当通过。

**弃权出口(canonical 短语,与 `no-decision` 同族)**:提取型输入(1A 从既有代码 / 截图提取)可能整节没有本地决策可溯——此时**诚实的弃权与写满同等合格**:

| canonical 短语(逐字) | 读法 | 用在哪 |
| -------------------- | ---- | ------ |
| `insufficient evidence` | 证据不足 → 该项按 **pass** 读 | 溯源与计数型硬门(如 Do's and Don'ts ≥ 4-6 条)对提取型输入允许弃权 |
| `material sufficient` | 材料足够(无开放问题) | 开放问题节 |
| `no open questions` | 同上的等价写法 | 开放问题节 |

弃权必须写明**缺什么材料才能结束弃权**;弃权只对提取型输入成立,生成型任务(greenfield design-md)不得用它替代溯源——能溯源就必须溯源。机械检查把 canonical 短语读作 pass。来源:anydesign(#37),2026-10 吸收。

**置信标记通道(提取型输入)**:溯源行尾注释同时承载**提取置信三档**——✅ 直接看到(代码 / computed style 原值)/ ⚠️ 有据推断(像素采样、视觉识别)/ ❓ 公开推测:

```yaml
tertiary: "#2563EB" # D-P1-1 ✅
secondary: "#9D9D9D" # no-decision: 提取来源 ⚠️
```

- 标记写在 id 或 `no-decision` **之后**,不替代 id;标记语义与交付末尾 Confidence map 表(Layer | Confidence | Why)由 [`../commands/design-md.md`](../commands/design-md.md) 的 1A / 1C 提取路径定义;
- 「只报观察到的数量」同理:看到 1 个按钮变体写「1 variant observed」,不写「primary, secondary, tertiary」;
- 与证据四分类是**不同轴**:置信标记回答「凭什么相信这个值」,证据四分类回答「凭什么断言已解决」——两者互补,不互相替代。来源:anydesign(#36),2026-10 吸收。

---

## 4. 三类违规

三类都按**硬性失败**处理,不是 warning。

| 编号 | 违规         | 判据                                                                     | 修法                                                                     |
| ---- | ------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| V1   | **悬空溯源** | token 注释的 id 在 `decisions[]` 中查不到                                | 补写这条决策(决策 / 理由 / 日期),或改注释指向正确 id;查不到来源的 token 不得留 |
| V2   | **孤儿 token** | `colors` / `typography` / `rounded` / `spacing` / `components` 的顶层键既无 id 也无 `no-decision` | 归到一条决策下;确实无依据的写 `no-decision:` 显式声明                   |
| V3   | **空原则**   | `## Overview` 声明的某条原则,没有任何 token 的注释指向它                 | 该原则要么落到至少一个 token 上,要么从 Overview 删掉——只写在散文里不改任何值的原则是装饰 |

V3 判定时**只数 token**,不看散文。理由写在正文但没落成值 = 没落成。

---

## 5. 判定与留痕

### 覆盖范围

溯源核对覆盖 front matter 五个块的**顶层键**:`colors` / `typography` / `rounded` / `spacing` / `components`。`typography` 内部字段(`fontSize` / `lineHeight` / …)与 `components` 内部属性属实现细节,不要求逐字段溯源,顶层键有 id 即可。

### 机械判定(validate-design-md.py)

**V1–V3 由 [`../../scripts/validate-design-md.py`](../../scripts/validate-design-md.py) 机械判定,人工仅复核脚本标 `unconfirmed` 的项**。脚本做四处交叉,缺哪一环就落在哪一类违规:

1. 每个顶层键有 id 或 `no-decision` —— 缺 = V2(孤儿 token);
2. 注释里的 id 在 `decisions[]` 可查 —— 查不到 = V1(悬空溯源);
3. `## Overview` 每条原则至少被一个 token 引用 —— 零引用 = V3(空原则,只数 token 不看散文);
4. `no-decision` 占比(> 1/3 提示回 Phase 0 重走)。

另加 **DESIGN.md → token.md 派生一致性**:token.md 里的 token 能追回 DESIGN.md(反向孤儿)。典型盲区——跨文件命名漂移(页面用了 `--border-vis` 类错名而检查仍全绿)——由此兜住。脚本退出码与 validate-draw-md.py 同三态语义(0 看了没问题 / 1 看了有问题 / 2 没能检查,canonical 见 [`../../scripts/EXIT-CODES.md`](../../scripts/EXIT-CODES.md));未测量不得记为通过。

脚本覆盖不到的残余形态才留给人工判断;人工复核结论逐项写出,与脚本输出摘要一并进判定记录。

### 判定记录(缺证据 = 未判定)

每次 design-md 交付、以及改过 token 的 redesign 交付,产物报告须留下三行核对结果(附 validate-design-md.py 输出摘要),格式固定:

```
溯源核对(YYYY-MM-DD):
  决策 N 条 / token 顶层键 M 个 / no-decision K 个
  V1 悬空:0 · V2 孤儿:0 · V3 空原则:0
  孤儿清单(应为空,非空则逐条列 key):—
```

**没有这三行就不许写「溯源已覆盖」**——机械判定也要留痕:三行记录(含脚本输出摘要与 unconfirmed 复核结论)是 [`numbered-gates.md`](numbered-gates.md) A 组 G01–G03 的判定记录,无记录视为未判定。

---

## 6. 回流规则:新值从哪来

build 阶段(draw-md / draw-*)出现 DESIGN.md 里没有的视觉值时,**不许就地即兴**:

1. 即兴值 = 孤儿 token(V2),是缺陷不是灵活性
2. 回 design-md:先补一条决策(拿到 id),再把值写进 DESIGN.md,再回下游
3. 用户明确说「这个值临时调一下、不进系统」时,在 ui-markdown 该行标 `<!-- no-decision: 临时调参,不入系统 -->` 并在报告列出,不算 V2

跳过第 1–2 步直接写进产物的,即使数值好看,也在 draw-* 交付门被拦(见 [`numbered-gates.md`](numbered-gates.md) A 组)。

---

## 7. 与既有文档的关系

| 主题               | canonical 在哪                                    | 本文                              |
| ------------------ | ------------------------------------------------- | --------------------------------- |
| 决策字段 / 账本结构 | [`spec-schema.md`](spec-schema.md) `decisions` 块 | 只管 id 编号与 token 反向引用     |
| token 命名与层级   | [`token.md`](token.md)                            | 只管溯源标记,不碰命名             |
| DESIGN.md 模板     | [`../commands/design-md.md`](../commands/design-md.md) | 只管模板里溯源注释落在哪      |
| 交付门禁           | [`numbered-gates.md`](numbered-gates.md) A 组      | 提供判据,门禁在那边执行          |
| 跨会话决策记忆     | `decisions` 账本(迭代段回写)                      | 账本记「为什么是这样」,溯源记「谁指的路」 |
