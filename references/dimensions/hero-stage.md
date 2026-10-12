# Hero Stage —— 首屏舞台的三层模型与兼容矩阵

> 维度层。品牌不只有"背景",而是有**首屏舞台**:背景场 + 可选主体 + 两者之间的关系(光怎么溢、影怎么落、主体是发光还是被场吸收)。只按"背景"思考会漏掉一半品牌——有的品牌不是一个渐变,是渐变上的一个发光球;有的品牌是一台相机飘在网格上;也有的品牌**没有主体本身就是决定**(如画布式知识工具:背景即主角)。本文给出一套组合模型与固定层序,供 design-md 方向阶段与 draw-md 首屏规格取用。
> 来源:hue 仓的 hero-stage.md(hero 三层模型 / 9 预设 / 兼容矩阵),2026-10 吸收;措辞自著,数值口径本地化。

---

## 1. 三层模型

每个首屏舞台由三部分组成:

```
  ┌─ 主体(可选) ─────────────┐
  │                          │
  │    ← 关系层 →            │   glow / halo / reflection / emissive / shadow-only / flat
  │                          │
  └─ 背景场 ─────────────────┘
```

- **`subject: none` 是一等选择**:舞台坍缩为纯背景——编辑向 / 知识向 / 极简品牌的本意。不要因为"感觉空"就加装饰(与 [`../meta/ai-tells.md`](../meta/ai-tells.md) §10 的装饰性十字 / 网格线禁令同源)
- 主体在场时,**关系层**决定它"长在舞台上"还是"贴上去":缺关系的 = 假贴片
- 三层各自有旋钮,默认全部取最安静值(见 §4)

## 2. 9 个命名预设

预设 = 旋钮的命名组合,作起点用,**预设名是标签不是约束**——每个字段可逐项覆盖。

| 预设 | 背景 | 主体 | 关系 | 适用 |
| ---- | ---- | ---- | ---- | ---- |
| `luminous-on-gradient` | 渐变,中心光,鲜明,bold | 发光体,居中,balanced,gradient-from-palette | glow,bleed 60 | AI / 开发工具 / 启动器,单一光物焦点 |
| `device-on-mesh` | mesh,偏心光,muted,subtle | 设备窗口,off-center-right,balanced | flat | SaaS / 事务追踪 / 产品导览 |
| `painterly-no-hero` | 手绘,painterly,ambient,muted,subtle | none | — | 编辑 / 知识 / 收藏 / 健康 |
| `grid-on-dark` | 图案(点阵 / 线阵),角落光,flat | 设备或组合,居中,balanced | shadow-only | 开发者平台 / 基建 / 文档 |
| `object-on-spotlight` | 渐变,顶光,muted,bold | 实物,居中,dominant,metallic(form 忽略——渲染为通用占位形) | shadow-only + 可选 reflection | 高端硬件 / 音频 / 工业 |
| `editorial-photo` | 照片(占位),full-bleed | none 或 photo-cutout | flat | 生活方式 / 硬件 / 时尚 |
| `shader-ambient` | 着色器,drift,subtle 默认 | none 或发光体,居中,accent | glow,bleed 30 | 生成式 / 音频 / AI / 创意工具 |
| `flat-blank` | 无或品牌调中性色,ambient | 组合,居中,accent | flat | 写作工具 / 文档 / 极简 SaaS |
| `sculptural-field` | 雕塑感(玻璃条 / 晶体簇 / 几何漂移),中心光,鲜明 | none | — | 启动器 / 开发者 AI / 创意工具——场本身即主角 |

## 3. 固定 z 轴层序

层序固定,不按需乱叠:

```
z: 0  body 背景(var(--background))
z: 1  背景介质          ← .bg-{medium}
z: 2  暗角叠层(开启时)  ← .hero-vignette
z: 3  噪点叠层(开启时)  ← .bg-grain-overlay
z: 4  关系层(glow/emissive/halo/reflection 时) ← .relation-*
z: 5  主体              ← .hero-{subject}
z:10  内容(标题 / 正文 / CTA)
```

- `flat` 与 `shadow-only` 关系**跳过 z4**;`shadow-only` 作为主体自身的 drop-shadow 存在
- 噪点是全局纹理叠层,不单属 hero
- 整栈位于 hero 容器内(`position: relative; overflow: hidden`);标题内容 `z-index: 10` 压在舞台之上

## 4. 旋钮默认取最安静值

| 旋钮 | 默认 | 升级 |
| ---- | ---- | ---- |
| `intensity` | `subtle` | `bold`(×1.4)/ `blown-out`(×1.8)是 **opt-in**,不是起点 |
| `vignette` | `off` | `subtle` / `strong` |
| `motion` | `static` | `drift` / `pulse` / `reactive`(动效还须过 [`../motion-skeletons/ROUTING.md`](../motion-skeletons/ROUTING.md) GATE 四查) |
| `saturation` | 跟随色板,不额外加饱和 | `vibrant` / `neon` 需要理由 |

**品牌自己官网看着大胆,渲染里 80% 仍读作 `subtle`**:hero 文案压在场上面,可读性不可谈判。

## 5. 主体分类(按意图,不按外形)

主体按**它物理上是什么**分类——这决定"诚实渲染"还是"诚实占位":

| subject | 是什么 | CSS 可渲染? | 物理 |
| ------- | ------ | ----------- | ---- |
| `luminous` | 发光抽象体(光球 / 圆盘 / 环 / 光环)。无质量 | ✅ 诚实渲染——光本来就没有我们假装的实体外形 | 无重力,漂浮,无地面接触,光从内部发出 |
| `object` | 具体实物产品(音箱 / 相机 / 手表 / 雕塑 / 工业造物) | ❌ **渲染为通用暖金属形占位**(竖向药丸 / 横向圆盘 / 软胶囊)。形只占住槽位,不试图再现真实产品——换真图由用户在上生产前完成 | 有重力,坐在隐含表面上;顶光,地面接触阴影 + 可选竖向反射;这些物理规则指导用户换成真图后舞台怎么配 |
| `device` | 矩形产品窗口(应用 mockup / 仪表盘框) | ✅ 诚实渲染——设备一律抽象为通用窗口,不复制具体硬件或具体产品界面 | 漂浮或落座;按平面 UI 处理 |
| `composition` | 小元素编排(插画场景 / 图标堆 / 卡组) | ✅ 诚实渲染——用选定图标族的原语搭 | 平面 2D,无物理 |
| `photo-cutout` | 真实摄影主体的替身 | ❌ 渲染为带说明的诚实地占位(同 [`../meta/visual-assets.md`](../meta/visual-assets.md) photo 口径) | n/a |
| `none` | 无主体,背景即主角 | ✅ 无需渲染 | n/a |

**规则一句话**:抽象的就诚实渲染,实物或照片就诚实占位,**永不硬画半成品 CSS 写实**。

`object` 的舞台配方(占位形也要把舞台做完整,交付时注明"占位形,上生产前换真图"):顶光(不是中心光)+ 暗角 + 地面接触阴影 + 可选竖向反射;`form` 旋钮对 object **忽略**——形永远取通用形,不按真实产品外形挑。

## 6. subject × relation 兼容矩阵

不是每个主体都能配每种关系——**尊重物理**,作者必须落在 ✅ 或 ok 格:

| | `flat` | `glow` | `halo` | `emissive` | `reflection` | `shadow-only` |
| --- | --- | --- | --- | --- | --- | --- |
| `luminous` | weak(读作贴上去) | ✅ 正典 | ✅ | ✅ | ❌(光没有地面) | ❌(与自发光矛盾) |
| `object` | ok | ❌(物体不发光) | weak | ❌ | ✅ | ✅ 正典 |
| `device` | ✅ 正典 | ok | weak | ❌ | ✅(Apple 式) | ✅ |
| `composition` | ✅ 正典 | ok | ❌ | ❌ | ❌ | ✅ |
| `photo-cutout` | ✅ 正典 | ok | ok | ❌ | ✅ | ✅ |
| `none` | ✅(关系忽略) | — | — | — | — | — |

✅ = 正典组合;ok = 允许但非默认;weak = 技术上能跑但读作贴上去 / 自相矛盾;❌ = 禁止——配方不渲染该组合。

## 7. 与 ai-tells §10 的衔接(正向替代配方)

[`../meta/ai-tells.md`](../meta/ai-tells.md) §10「hero 内 div 假产品 UI(假任务列表 / 假终端 / 假仪表盘)」是**禁令**;替代配方在本文:

- 需要"产品感"时:用 `device` 主体——抽象窗口行(几行色块 + 横条,**不复制具体产品界面**),或 `object` 占位形;不要硬造会被人当成真实截图的假 UI
- 需要"氛围感"时:调背景场介质与 intensity(默认仍取 subtle),不是往场里塞装饰零件
- 决策顺序固定:**先定主体意图(放什么)→ 再选承载它的预设/介质 → 最后补关系层**;顺序反了就会得到"先画了渐变,再想放什么"的默认产物

## 8. 与既有文档的关系

| 主题 | canonical 在哪 | 本文 |
| ---- | -------------- | ---- |
| Hero 布局模式命名与硬约束(H1-H4) | [`../vocabulary/hero.md`](../vocabulary/hero.md) | 管首屏**视觉舞台构成**(背景场 / 主体 / 关系),与布局命名正交:先选布局模式,再用本模型填舞台 |
| 素材来源、有效像素、object/photo 诚实占位 | [`../meta/visual-assets.md`](../meta/visual-assets.md) | 引用其口径,不重复 |
| 假产品 UI / 装饰零件禁令 | [`../meta/ai-tells.md`](../meta/ai-tells.md) §10 | 提供正向替代配方(§7) |
| 动效强度与 GATE | [`../meta/dials.md`](../meta/dials.md)、[`../motion-skeletons/ROUTING.md`](../motion-skeletons/ROUTING.md) | 引用其档位与四查,不另立 |
