# 媒体播放器模式命名词汇

> 术语库。视频/音频播放器的状态与适配模式命名。与页面加载(states.md)、滚动行为(scroll.md)互补:那里管页面级加载与滚动,这里管播放语境专属的加载时机、续播与画面适配。

## 命名表

| 模式名 | 构成要素(形态/阈值) | 适用场景 |
| --- | --- | --- |
| `player-loading-screen` | 纯黑底 + 居中 spinner,无周边内容 | 视频加载超过 2 秒才显示;够播即起播,剩余缓冲后台续载——2 秒内不出加载屏,防闪变 |
| `player-autoresume` | 自动从上次退出时间点续播,不弹"是否继续"询问 | 回访续看;能续播就静默续,退出播放落在内容详情页并留续播入口 |
| `player-aspect-fill` | 裁切充满容器 | 宽幅视频(2:1 至 2.40:1)的默认适配 |
| `player-aspect-fit` | 完整适配 + 黑边 | 标准比例(4:3、16:9)的默认适配;宽高比决定默认模式,用户可手动切换 |
| `player-overlay-delay` | 交互浮层(答题/打卡)出现时延迟 ≥0.5s 才暂停媒体,并给明确的"关闭浮层继续播放"出口 | 教育视频中途测验、打卡类浮层;浮层关闭立即续播 |
| `player-chrome-autohide` | 全屏播放时控制 chrome(控制面板/进度条)无操作自动隐藏 | 沉浸播放场景:全屏 chrome 约 2s 无操作隐藏,播放控制面板约 3s;点击/上滑恢复 |
| `player-ambient-sync` | 播放联动氛围:频谱律动、封面呼吸、环境反光与流动高光随播放同步;暂停时所有环境动效同步收住(玻璃 / 拟态质感均适用,静态光晕配方见 [pro-motion.md](pro-motion.md) `media-ambient-glow`) | 音乐 / 视频播放页 |
| `player-eq-mode-link` | 音效模式按钮与低/中/高滑块双向联动:点模式即切滑块参数并滚到新值,拖滑块实时回显数值与进度 | 播放器音效设置(联动控件纪律同 [`states.md`](states.md) 联动家族) |
| `player-skip-controls` | 长内容(播客/听书/长视频)配快进快退,档位 10/15/30s 可配 | 直播内容无进度语义,进度条置灰;不支持的播控功能置灰而非隐藏 |

## 使用规则

- **2 秒阈值**:加载屏是"慢"的信号,不是默认开场;网络快的首帧直出
- **续播免确认**:自动续播 + 时间点精确到上次退出位置;询问式续播("从 12:34 继续吗?")只用于源质量变化等真有歧义的场景
- **宽高比决定默认**:fill 与 fit 是适配策略不是用户偏好;默认由内容比例定,切换入口常驻
- **浮层不抢画面**:一切中途浮层必须可一键关闭并自动续播;浮层出现到暂停的 ≥0.5s 延迟让用户看清是画面在让位
- **与 states.md 分工**:播放器内的加载走 `player-loading-screen`;页面级加载状态仍走 states.md
- **氛围动效随播放态生灭**:频谱 / 呼吸 / 反光只在播放态运行,暂停同步收住;`prefers-reduced-motion` 一律静态封面与静态光晕

## 在 draw-md 中的写法

```markdown
## MediaPlayer (video-detail)
- loading: { pattern: player-loading-screen, threshold: 2s }
- resume: player-autoresume
- fit: { default: player-aspect-fit, wide: player-aspect-fill, switchable: true }
- overlays: { pause-delay: 0.5s, dismiss-resumes: true }
```
