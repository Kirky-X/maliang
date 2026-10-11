# 对话与消息组件命名词汇

> 模式词汇库。IM / 客服 / AI 助手等对话界面的组件级模式命名:气泡生命周期、流式输出、输入态、语音输入、滚动锚点、引用来源。来源:外部对标(NN/g《10 Guidelines for Designing AI Chatbots》、Setproduct《Designing AI chat interfaces》、Kommunicate《AI Agent UI》、The Front Kit,2026-10);与 [`popups.md`](popups.md)(浮层选型)、[`micro-interactions.md`](micro-interactions.md)(时长预算)、[`../templates/page/ai-console.md`](../templates/page/ai-console.md)(Agent 工作台整页模式——纯聊天不适用该模板,走本篇)互补。

## 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `chat-bubble-lifecycle` | 气泡生命周期:消息从输入框位置飞入列表位,长按弹操作排(复制 / 引用 / 撤回);发送失败原地标红可点击重发 | 所有对话界面的消息进出 |
| `chat-stream-typewriter` | 流式输出:逐 chunk 追加 + 块光标,可跳过直达终稿;AI 自报身份与能力边界 | AI 助手回复(流式口径与 [ai-console.md](../templates/page/ai-console.md) 一致) |
| `chat-typing-indicator` | 输入中指示:对方气泡位三点呼吸;超 10s 未出内容降级为「仍在输入」文案 | 双人 IM、客服会话 |
| `chat-stop-regenerate` | 停止与重生成:生成中主钮变「停止」,完成后唤起「重新生成」;重生成保留旧答案可对比 | AI 对话的连续生成控制 |
| `chat-swipe-reply` | 滑动引用回复:气泡水平滑出引用轨,松手进输入框带引用头 | IM 消息回复(桌面为右键等价) |
| `chat-voice-input` | 按住说话:按住出实时波形,上滑进取消区,松手发送;转写中显示占位骨架 | 语音消息、语音输入 |
| `chat-scroll-anchor` | 新消息锚点:贴底时自动跟随新消息;上滚后钉住 + 「回到底部」徽标(带未读数) | 所有滚动对话流 |
| `chat-citation-chip` | 引用角标:AI 回答尾部来源 chip(N 条),点击展开来源卡可跳转 | AI 回答的可信度与溯源 |

## 使用规则

- 进出场 ≤ 400ms(浮层档);气泡从输入框长出(`card-pop-origin` 语义,挂 [pro-motion.md](pro-motion.md)),禁屏幕中心凭空淡入
- `chat-stream-typewriter`:≤ 1 chunk/帧、带块光标、可跳过(点击或 Esc 直达终稿),沿 [ai-console.md](../templates/page/ai-console.md) 既有口径;流式中禁改写历史消息
- AI 透明度:AI 必须自报身份与能力边界(NN/g);失败必须给重试路径,禁静默失败(见 [`../meta/principles.md`](../meta/principles.md) 失败显性化)
- `chat-stop-regenerate`:停止后已生成部分保留,禁整段丢弃;重生成时旧答案折叠可展开对比
- `chat-voice-input`:按住 < 400ms 视为误触回落(挂 [buttons.md](buttons.md) `press-peek` 长按判定);上滑超阈值进取消区松手不发送;波形只动 transform
- `chat-scroll-anchor`:用户上滚超过 1 屏才钉住;「回到底部」徽标带未读数(`num-badge` 语义,挂 [number-motion.md](number-motion.md));点击回底后恢复自动跟随
- 键盘弹起:列表锚定到当前气泡,输入框随键盘上移不遮内容;系统返回键 / Esc 收键盘
- 无障碍:消息列表 `aria-live="polite"` 播报新消息(见 [`accessibility.md`](../meta/accessibility.md));流式可跳过即等价 reduced-motion 降级

## 在 draw-md 中的写法

```markdown
## Chat (support-session)
- pattern: chat-bubble-lifecycle + chat-scroll-anchor
- bubble: origin-input, failed: retry-inline, anchor: bottom-follow

## Chat (ai-assistant)
- pattern: chat-stream-typewriter + chat-stop-regenerate + chat-citation-chip
- stream: 1-chunk-per-frame, skippable: true, identity: ai-disclosed

## Input (voice-bar)
- pattern: chat-voice-input
- hold: 400ms, cancel: slide-up, waveform: transform-only
```
