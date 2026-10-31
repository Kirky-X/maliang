# 候选池索引（Candidates）—— 上游原文快照总目录

> **provenance**：原始出处 [样张源](https://样张源) DESIGNS 索引；上游 [/设计样张集](https://github.com//设计样张集)，许可 MIT。站点条目上游路径为 `design-md/<slug>/DESIGN.md`，风格模板条目为 `extra/uiuxskillProMax/generated/<n>-<name>/DESIGN.md`。快照日期 2026-10-25，共 112 条 / 9 组。
> 每条原文存档为同目录 `<slug>.md`，文件头有完整 provenance 注释（原始出处 / 上游路径 / 许可证 / 分组 / 站点摘要 / 站点色板 / 快照日期）。

## 本目录的定位

本目录是**候选池原文快照**，与蒸馏供体层（[../README.md](../README.md)）分工如下：

- 蒸馏供体层**只收逐家晋升的条目**：把原文蒸馏为 9 节带实测值的结构、过核验时效与查重后，另立 `../<id>.md`，与本快照**并存不互替**（各快照文件头同注）。
- **晋升三条件**（canonical 见 [../README.md](../README.md) §5）：① 与首批气质轴不重复（暗 / 亮 / 工具 / 内容至少一轴不同）② 9 节能写到具体值 ③ 与既有供体查重；不做"整库平移"，逐家按需收录。
- 已晋升并存档的：`linear.app` / `raycast` / `stripe` / `vercel` 四条，行内注明对应蒸馏供体。

## 抓取失败未入库

无：fetch-manifest 112/112 全部 ok，merge-manifest written 112 / skipped 0；designs.json、快照目录、两份清单四方 slug 集合一致（2026-10-31 编目时核验）。

## 分组总览

| 分组 | 条数 |
| ---- | ---- |
| AI 与机器学习 | 12 |
| 开发工具与平台 | 14 |
| 基础设施与云 | 6 |
| 设计与生产力 | 10 |
| 金融与加密 | 4 |
| 企业与消费 | 8 |
| 通用风格模板 | 40 |
| 落地页风格模板 | 8 |
| 分析仪表板模板 | 10 |
| 合计 | 112 |

> 色板列取 provenance 站点色板的前 3 个 hex；15 条风格模板上游未提取色板，以 — 标记。

---

## AI 与机器学习（ai · 12 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `claude` | Claude | 羊皮纸暖底，衬线 500 单字重标题，陶土橙单点强调，灰阶全带黄棕底 | `#141413` `#c96442` `#d97757` | [claude.md](claude.md) |
| `cohere` | Cohere | 纯白画布冷灰描边，签名 22px 大圆角卡片，数据面板密度高 | `#000000` `#212121` `#17171c` | [cohere.md](cohere.md) |
| `elevenlabs` | ElevenLabs | 暖白画布配 300 细字重大标题，暗色影院块承载音频波形 | `#ffffff` `#f5f5f5` `#000000` | [elevenlabs.md](elevenlabs.md) |
| `minimax` | Minimax | 白底为主多彩产品卡，DM Sans / Outfit / Poppins 多字体分角色 | `#1456f0` `#3daeff` `#ea5ec1` | [minimax.md](minimax.md) |
| `mistral.ai` | Mistral AI | 琥珀色全谱从奶油到焦橙，82px 大字配负字距 | `#fa520f` `#fb6424` `#ff8105` | [mistral.ai.md](mistral.ai.md) |
| `ollama` | Ollama | 纯白底零彩色全灰阶，SF Pro Rounded 圆体标题 | `#000000` `#262626` `#090909` | [ollama.md](ollama.md) |
| `opencode.ai` | OpenCode AI | 全站单用 Berkeley Mono 等宽，暖红棕近黑画布 | `#201d1d` `#fdfcfc` `#9a9898` | [opencode.ai.md](opencode.ai.md) |
| `replicate` | Replicate | 橙红洋红爆炸渐变 hero，128px 特重展示字 | `#202020` `#ea2804` `#dd4425` | [replicate.md](replicate.md) |
| `runwayml` | RunwayML | 全幅影像当界面，单一字体走到底，纯黑画布 | `#000000` `#030303` `#1a1a1a` | [runwayml.md](runwayml.md) |
| `together.ai` | Together AI | 白底配粉蓝薰衣草柔和渐变，深午夜蓝承载研究暗区 | `#ef2cc1` `#fc4c02` `#010120` | [together.ai.md](together.ai.md) |
| `x.ai` | xAI | 深灰蓝与纯白二值对比无中间灰，GeistMono 320px 细字重当展示字 | `#f8f8f8` `#ffffff` `#1f2228` | [x.ai.md](x.ai.md) |

## 开发工具与平台（dev · 14 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `cursor` | Cursor | 自制 Gothic 压缩大字负字距，正文衬线带花体替换 | `#26251e` `#f2f1ed` `#e6e5e0` | [cursor.md](cursor.md) |
| `expo` | Expo | 冷白画廊式留白，严格黑白单色配蓝灰正文 | `#000000` `#1c2024` `#0d74ce` | [expo.md](expo.md) |
| `linear.app` | Linear | 暗色原生精密工程：近黑画布 + 单色强调 + 签名字重 510。已有蒸馏供体 [../linear.md](../linear.md)，本条为原文快照 | `#f7f8f8` `#ffffff` `#f3f4f5` | [linear.app.md](linear.app.md) |
| `lovable` | Lovable | 暖奶油画布，人文气质展示字配编辑式字距 | `#f7f4ed` `#1c1c1c` `#fcfbf8` | [lovable.md](lovable.md) |
| `mintlify` | Mintlify | Inter 展示级紧字距，Geist Mono 大写小号当技术标签 | `#0d0d0d` `#ffffff` `#fafafa` | [mintlify.md](mintlify.md) |
| `posthog` | PostHog | 鼠尾草橄榄绿替代常规蓝调，IBM Plex 700/800 粗标题配 1.5 宽行距 | `#4d4f46` `#23251d` `#f54e00` | [posthog.md](posthog.md) |
| `raycast` | Raycast | 桌面原生暗色：蓝调近黑 + inset 高光阴影 + 正字距正文。已有蒸馏供体 [../raycast.md](../raycast.md)，本条为原文快照 | `#07080a` `#101111` `#1b1c1e` | [raycast.md](raycast.md) |
| `resend` | Resend | 纯黑画廊式暗场，衬线主视觉配三字体层级 | `#000000` `#f0f0f0` `#ffffff` | [resend.md](resend.md) |
| `sentry` | Sentry | 紫黑画布，暖紫谱系深浅分段 | `#1f1633` `#150f23` `#362d59` | [sentry.md](sentry.md) |
| `supabase` | Supabase | 近黑画布，祖母绿限次点缀作身份标记 | `#3ecf8e` `#00c573` `#0f0f0f` | [supabase.md](supabase.md) |
| `superhuman` | Superhuman | 深紫渐变 hero，可变字体 460/540 非标字重档 | `#1b1938` `#cbb7fb` `#292827` | [superhuman.md](superhuman.md) |
| `vercel` | Vercel | 工程静默：纯白画廊 + shadow-as-border + 压缩大字。已有蒸馏供体 [../vercel.md](../vercel.md)，本条为原文快照 | `#171717` `#ffffff` `#fafafa` | [vercel.md](vercel.md) |
| `warp` | Warp | 暖土调近黑画布，奶白正文替代纯白 | `#0e0e0d` `#161615` `#faf9f6` | [warp.md](warp.md) |
| `zapier` | Zapier | 暖奶油画布红棕黑正文，插画驱动 | `#201515` `#fffefb` `#fffdf9` | [zapier.md](zapier.md) |

## 基础设施与云（infra · 6 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `clickhouse` | ClickHouse | 纯黑画布配荧光黄绿，Inter 900 黑重 96px 大字 | `#faff69` `#166534` `#14572f` | [clickhouse.md](clickhouse.md) |
| `composio` | Composio | 漆黑画布近隐白描边，几何无衬线正文配等宽技术标签 | `#ffffff` `#0007cd` `#000000` | [composio.md](composio.md) |
| `hashicorp` | HashiCorp | 白暗双模，白色文档区与深灰蓝产品区交替 | `#000000` `#15181e` `#0d0e12` | [hashicorp.md](hashicorp.md) |
| `mongodb` | MongoDB | 森绿黑画布，荧光绿单点品牌色 | `#001e2b` `#00ed64` `#00684a` | [mongodb.md](mongodb.md) |
| `sanity` | Sanity | 近黑为默认身份而非暗色模式，极端负字距展示字 | `#f7f7f7` `#ffffff` `#f0f0f0` | [sanity.md](sanity.md) |
| `stripe` | Stripe | 金融精致：细字重大标题 + 蓝调染色阴影 + 表格数字。已有蒸馏供体 [../stripe.md](../stripe.md)，本条为原文快照 | `#533afd` `#4434d4` `#2e2b8c` | [stripe.md](stripe.md) |

## 设计与生产力（design · 10 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `airtable` | Airtable | 白底深海军蓝正文，单一蓝承担 CTA 与链接 | `#181d26` `#1b61c9` `#e0e2e6` | [airtable.md](airtable.md) |
| `cal` | Cal.com | 品牌零彩色全灰阶，几何展示字极紧默认字距 | `#242424` `#111111` `#898989` | [cal.md](cal.md) |
| `clay` | Clay | 暖奶油底燕麦描边，具名糖果色板 matcha / ube 等 | `#faf9f7` `#000000` `#ffffff` | [clay.md](clay.md) |
| `figma` | Figma | 黑白界面铬，彩色只存在于产品内容，320/450 非标字重档 | `#000000` `#ffffff` `#0acf83` | [figma.md](figma.md) |
| `framer` | Framer | 纯黑虚空画布，110px 展示字配极端负字距 | `#000000` `#ffffff` `#0099ff` | [framer.md](framer.md) |
| `intercom` | Intercom | 暖米白底燕麦描边，80px 大字负字距配 1.0 行高 | `#faf9f6` `#111111` `#ffffff` | [intercom.md](intercom.md) |
| `miro` | Miro | 白底近黑正文，亮黄点缀，字体带多字符变体 | `#1c1c1e` `#5b76fe` `#2a41b6` | [miro.md](miro.md) |
| `notion` | Notion | 暖极简，灰阶全带黄棕底，64px 标题负字距 | `#000000` `#ffffff` `#f6f5f4` | [notion.md](notion.md) |
| `pinterest` | Pinterest | 暖白底橄榄沙色中性系，正红唯一强调色 | `#ffffff` `#211922` `#e60023` | [pinterest.md](pinterest.md) |
| `webflow` | Webflow | 白底近黑正文，蓝同时承担品牌与交互色 | `#080808` `#146ef5` `#3b89ff` | [webflow.md](webflow.md) |

## 金融与加密（finance · 4 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `coinbase` | Coinbase | 单一品牌蓝定调，四字体专有家族分工 | `#0a0b0d` `#0052ff` `#578bfa` | [coinbase.md](coinbase.md) |
| `kraken` | Kraken | 品牌紫谱系，暗底数据密集仪表板 | `#101114` `#7132f5` `#5741d8` | [kraken.md](kraken.md) |
| `revolut` | Revolut | 500 字重 136px 广告牌大字，黑白二值配语义 token 体系 | `#ffffff` `#191c1f` `#f4f4f4` | [revolut.md](revolut.md) |
| `wise` | Wise | 900 字重 0.85 行高广告牌标题，青柠绿配深绿正文 | `#ffffff` `#0e0f0c` `#9fe870` | [wise.md](wise.md) |

## 企业与消费（enterprise · 8 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `airbnb` | Airbnb | 纯白画布珊瑚红单点，圆头可变字体 | `#ffffff` `#222222` `#ff385c` | [airbnb.md](airbnb.md) |
| `apple` | Apple | SF Pro 光学字号自适应，黑与浅灰分段交替 | `#1d1d1f` `#ffffff` `#000000` | [apple.md](apple.md) |
| `bmw` | BMW | 300 细字重全大写展示，蓝仅用于交互件 | `#ffffff` `#262626` `#1c69d4` | [bmw.md](bmw.md) |
| `ibm` | IBM | 300 细字重展示配等宽技术字，小字号恒定微字距 | `#ffffff` `#f4f4f4` `#e8e8e8` | [ibm.md](ibm.md) |
| `nvidia` | NVIDIA | 黑底主导，品牌绿只做描边与下划线等强调件 | `#76b900` `#bff230` `#000000` | [nvidia.md](nvidia.md) |
| `spacex` | SpaceX | 纯黑画布全幅影像，工业血统 D-DIN 字体 | `#000000` `#f0f0fa` `#ff4444` | [spacex.md](spacex.md) |
| `spotify` | Spotify | 沉浸近黑底，品牌绿只做功能不装饰 | `#121212` `#181818` `#1f1f1f` | [spotify.md](spotify.md) |
| `uber` | Uber | 纯黑白零中间调，双字体家族分工 | `#000000` `#ffffff` `#e2e2e2` | [uber.md](uber.md) |

## 通用风格模板（styleGeneral · 40 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `minimalism` | Minimalism & Swiss Style | 黑白单色加米灰中性，大留白网格秩序 | `#000000` `#ffffff` `#808080` | [minimalism.md](minimalism.md) |
| `neumorphism` | Neumorphism | 软粉彩底，同色凸凹浮雕阴影 | `#e8e8e8` `#ffffff` `#d1d1d1` | [neumorphism.md](neumorphism.md) |
| `glassmorphism` | Glassmorphism | 半透白磨砂层叠，鲜艳底色透出模糊 | `#667eea` `#764ba2` `#f093fb` | [glassmorphism.md](glassmorphism.md) |
| `brutalism` | Brutalism | 红蓝黄黑原色硬撞，裸文本高对比零修饰 | `#ff0000` `#0000ff` `#ffff00` | [brutalism.md](brutalism.md) |
| `3d-hyperrealism` | 3D & Hyperrealism | 深海军蓝酒红金多档渐变，拟真光影厚阴影 | `#ffd700` `#ffa500` `#667eea` | [05-3d-hyperrealism.md](3d-hyperrealism.md) |
| `vibrant-block` | Vibrant & Block-based | 霓虹原色几何色块拼贴，高饱和分区 | `#39ff14` `#bf00ff` `#ff1493` | [vibrant-block.md](vibrant-block.md) |
| `dark-mode-oled` | Dark Mode (OLED) | 纯黑 OLED 底，午夜蓝分域配霓虹强调 | `#000000` `#121212` `#39ff14` | [dark-mode-oled.md](dark-mode-oled.md) |
| `accessible` | Accessible & Ethical | WCAG AA/AAA 对比底，色彩永不单独编码 | `#0066cc` `#000000` `#ffffff` | [accessible.md](accessible.md) |
| `claymorphism` | Claymorphism | 蜜桃婴儿蓝薄荷粉彩，黏土软 3D 厚圆角 | `#fef3f2` `#f0f9ff` `#ffffff` | [claymorphism.md](claymorphism.md) |
| `aurora-ui` | Aurora UI | 蓝紫粉青极光渐变融合，网格渐变发光 | `#667eea` `#764ba2` `#f093fb` | [10-aurora-ui.md](aurora-ui.md) |
| `retro-futurism` | Retro-Futurism | 深黑底霓虹蓝粉青，CRT 扫描线加金属银 | `#1a1a2e` `#0080ff` `#ff006e` | [11-retro-futurism.md](retro-futurism.md) |
| `flat-design` | Flat Design | 4-6 色高饱和实色，零阴影零拟物 | `#3498db` `#e74c3c` `#f39c12` | [12-flat-design.md](flat-design.md) |
| `skeuomorphism` | Skeuomorphism | 木纹皮革金属材质，8-12 档渐变拟真 | `#c8c8c8` `#a0a0a0` `#f5f5f5` | [13-skeuomorphism.md](skeuomorphism.md) |
| `liquid-glass` | Liquid Glass | 彩虹虹彩流质渐变，红青色差流动变形 | `#667eea` `#764ba2` `#f093fb` | [14-liquid-glass.md](liquid-glass.md) |
| `motion-driven` | Motion-Driven | 高对比强调色承载动效，绿红语义状态色 | `#22c55e` `#ef4444` | [15-motion-driven.md](motion-driven.md) |
| `micro-interactions` | Micro-interactions | 10-20% 细微色移做反馈，中性底配状态点 | `#3b82f6` `#22c55e` `#ef4444` | [16-micro-interactions.md](micro-interactions.md) |
| `inclusive-design` | Inclusive Design | WCAG AAA 7:1 对比，红绿不单独编码，纹样辅助 | `#0066cc` `#003366` `#2563eb` | [17-inclusive-design.md](inclusive-design.md) |
| `zero-interface` | Zero Interface | 软白暖米底，可见界面元素降到近零 | `#fafafa` `#e5e5e5` `#f5f1e8` | [18-zero-interface.md](zero-interface.md) |
| `soft-ui-evolution` | Soft UI Evolution | 高对比粉彩，软 UI 投影的可及性迭代 | `#e0f2fe` `#f0f9ff` `#ecfeff` | [19-soft-ui-evolution.md](soft-ui-evolution.md) |
| `neubrutalism` | Neubrutalism | 黄红蓝原色块黑粗描边硬投影，零渐变 | `#fff8e7` `#ff6b6b` `#4ecdc4` | [38-neubrutalism.md](neubrutalism.md) |
| `bento-box` | Bento Box Grid | 中性底加品牌色，不对称模块瓷砖拼格 | `#ffffff` `#f5f5f5` | [39-bento-box.md](bento-box.md) |
| `y2k-revival` | Y2K Aesthetic | 荧光粉青铬银金属，气泡光泽虹彩 | `#ff00ff` `#00ffff` `#ffff00` | [40-y2k-revival.md](y2k-revival.md) |
| `cyberpunk` | Cyberpunk UI | 深黑底矩阵绿品红青霓虹，扫描线加故障色 | `#ff00ff` `#00ffff` `#ffff00` | [41-cyberpunk.md](cyberpunk.md) |
| `organic-biophilic` | Organic Biophilic | 森林绿大地棕米色自然系，有机圆角形 | `#f5f1e8` `#e0d8c8` `#5d6b4d` | [42-organic-biophilic.md](organic-biophilic.md) |
| `ai-native` | AI-Native UI | 中性底配 AI 紫单强调，会话流状态点 | `#667eea` `#764ba2` `#6366f1` | [43-ai-native.md](ai-native.md) |
| `memphis-revival` | Memphis Design | 粉黄青几何撞色，波普纹样填充 | `#fff5e6` `#ffe66d` `#ff6b6b` | [44-memphis-revival.md](memphis-revival.md) |
| `vaporwave` | Vaporwave | 粉青薄荷紫日落渐变，VHS 故障质感 | `#ff71ce` `#c0c0c0` `#01cdfe` | [45-vaporwave.md](vaporwave.md) |
| `dimensional-layering` | Dimensional Layering | 中性底配 sm 至 xl 阴影阶梯，层叠表达深度 | `#ffffff` `#f5f5f5` `#e0e0e0` | [46-dimensional-layering.md](dimensional-layering.md) |
| `exaggerated-minimalism` | Exaggerated Minimalism | 黑白加单一艳色，超大字号排印做主角 | `#000000` `#ffffff` | [47-exaggerated-minimalism.md](exaggerated-minimalism.md) |
| `kinetic-typography` | Kinetic Typography | 文字动效主导，高对比底渐变字填充 | — | [48-kinetic-typography.md](kinetic-typography.md) |
| `parallax-storytelling` | Parallax Storytelling | 滚动分层叙事，分段专属色板与深度层色 | — | [49-parallax-storytelling.md](parallax-storytelling.md) |
| `swiss-modernism` | Swiss Modernism 2.0 | 黑白灰网格系统，Helvetica 血统单点缀色 | `#000000` `#ffffff` `#f5f5f5` | [50-swiss-modernism.md](swiss-modernism.md) |
| `hud-scifi` | HUD / Sci-Fi FUI | 霓虹青全息蓝警报红，网格线加透明黑 HUD | `#00ffff` `#0080ff` `#ff0000` | [51-hud-scifi.md](hud-scifi.md) |
| `pixel-art` | Pixel Art | NES 调色板低饱和，抖动着色像素块 | `#0f380f` `#9bbc0f` `#306230` | [52-pixel-art.md](pixel-art.md) |
| `bento-grids` | Bento Grids | 米白底 Apple 式模块卡配柔影 | `#f5f5f7` `#ffffff` `#1d1d1f` | [53-bento-grids.md](bento-grids.md) |
| `neubrutalism-v2` | Neubrutalism | 爆黄亮红黑主色，薰衣草薄荷辅助，粗野扁平 | `#fffbf0` `#ff6b6b` `#a388ee` | [54-neubrutalism-v2.md](neubrutalism-v2.md) |
| `spatial-ui` | Spatial UI (VisionOS) | 白磨砂玻璃层配深投影，空间深度视觉 | `#ffffff` | [55-spatial-ui.md](spatial-ui.md) |
| `e-ink-paper` | E-Ink / Paper | 纸白墨黑高对比，荧光黄笔刷点缀，哑光纸感 | `#1a1a1a` `#f5f1eb` `#fdfbf7` | [56-e-ink-paper.md](e-ink-paper.md) |
| `gen-z-chaos` | Gen Z Chaos / Maximalism | 品红绿黄蓝硬撞色，贴纸拼贴噪点满铺 | `#ff6b6b` `#4ecdc4` `#ffe66d` | [57-gen-z-chaos.md](gen-z-chaos.md) |
| `biomimetic-organic` | Biomimetic / Organic 2.0 | 细胞粉叶绿素绿生物荧光蓝，深海底色 | `#001e3c` `#00ff41` `#ff9999` | [58-biomimetic-organic.md](biomimetic-organic.md) |

## 落地页风格模板（styleLanding · 8 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `hero-centric` | Hero-Centric Design | 大幅 hero 配高对比 CTA，品牌主色定调 | — | [20-hero-centric.md](hero-centric.md) |
| `conversion-optimized` | Conversion-Optimized | 表单聚焦单 CTA，白底高对比加限时紧迫色 | — | [21-conversion-optimized.md](conversion-optimized.md) |
| `feature-rich` | Feature-Rich Showcase | 功能卡网格铺陈，绿红蓝紫按语义分色 | — | [22-feature-rich.md](feature-rich.md) |
| `minimal-direct` | Minimal & Direct | 单栏黑白灰，强调色只留给 CTA | — | [23-minimal-direct.md](minimal-direct.md) |
| `social-proof` | Social Proof-Focused | 信任蓝配成功绿，浅灰 logo 墙与证言高亮 | — | [24-social-proof.md](social-proof.md) |
| `interactive-demo` | Interactive Product Demo | 内嵌产品演示，界面同源色加编号步骤色阶 | — | [25-interactive-demo.md](interactive-demo.md) |
| `trust-authority` | Trust & Authority | 专业蓝灰底，金银徽章色做资质背书 | — | [26-trust-authority.md](trust-authority.md) |
| `storytelling` | Storytelling-Driven | 叙事分段换色，每段独立情绪色板与过渡渐变 | — | [27-storytelling.md](storytelling.md) |

## 分析仪表板模板（styleAnalytics · 10 条）

| slug | 名称 | 气质一句话 | 签名色板（前 3 个 hex） | 文件 |
| ---- | ---- | ---------- | ------------------------ | ---- |
| `data-dense-dashboard` | Data-Dense Dashboard | 浅灰底高密度网格，红绿蓝数据语义色，最小内边距 | `#f5f5f5` `#333333` `#22c55e` | [28-data-dense-dashboard.md](data-dense-dashboard.md) |
| `heatmap-density` | Heat Map & Heatmap Style | 蓝到红热度梯度尺，白黄中点双向发散 | `#1e293b` `#1e3a5f` `#0369a1` | [29-heatmap-density.md](heatmap-density.md) |
| `executive-summary` | Executive Dashboard | 大号 KPI 数字主导，蓝灰专业底红色警报 | — | [30-executive-summary.md](executive-summary.md) |
| `real-time-monitoring` | Real-Time Monitoring | 红橙绿警报三色加蓝色刷新动效，状态灯主导 | `#ff0000` `#ffa500` `#22c55e` | [31-real-time-monitoring.md](real-time-monitoring.md) |
| `drill-down-analytics` | Drill-Down Analytics | 层级深度分色，面包屑与下钻路径指示 | — | [32-drill-down-analytics.md](drill-down-analytics.md) |
| `comparative-analytics` | Comparative Analysis Dashboard | 蓝对橙紫对比双系，绿红增量指标 | — | [33-comparative-analytics.md](comparative-analytics.md) |
| `predictive-analytics` | Predictive Analytics | 预测线独立用色，置信区间明暗分层 | `#3b82f6` `#a855f7` | [34-predictive-analytics.md](predictive-analytics.md) |
| `user-behavior-analytics` | User Behavior Analytics | 漏斗阶段分色：高参与绿、流失红、转化蓝，灰流向箭头 | — | [35-user-behavior-analytics.md](user-behavior-analytics.md) |
| `financial-analytics` | Financial Dashboard | 盈绿亏红加信任深蓝，预算偏差橙红 | `#334155` `#10b981` `#22c55e` | [36-financial-analytics.md](financial-analytics.md) |
| `sales-intelligence` | Sales Intelligence Dashboard | 赢单绿输单红进行蓝加配额金，管道阶段分色 | — | [37-sales-intelligence.md](sales-intelligence.md) |
