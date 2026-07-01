# Video 组件 API 文档

> ArkTS 视频播放组件 `Video`,支持本地/网络视频播放、控件显示、循环、静音等。

## 组件定义

`Video` 组件内置播放控制器,通过 `VideoController` 控制播放/暂停/跳转。

## 构造函数

```arkts
Video(value: {
  src?: string | Resource      // 视频源
  currentProgressRate?: number // 播放倍速
  previewUri?: string | Resource // 封面图
  controller?: VideoController
})
```

## 核心属性表

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| src | string \| Resource | 视频源(本地/网络 URL) |
| muted | boolean | 是否静音 |
| autoPlay | boolean | 是否自动播放 |
| controls | boolean | 是否显示默认控制条 |
| objectFit | ImageFit | 填充模式 |
| loop | boolean | 是否循环 |
| showSpeed | boolean | 是否显示倍速选择 |
| showFullscreen | boolean | 是否显示全屏按钮 |

## VideoController 方法

| 方法 | 说明 |
| --- | --- |
| start() | 开始播放 |
| pause() | 暂停 |
| stop() | 停止 |
| setCurrentTime(t) | 跳转(ms) |
| requestFullscreen() | 进入全屏 |
| exitFullscreen() | 退出全屏 |

## 事件回调

| 事件 | 说明 |
| --- | --- |
| onStart | 开始播放 |
| onPause | 暂停 |
| onFinish | 播放完成 |
| onError | 错误 |
| onUpdate | 进度更新 |
| onFullscreenChange | 全屏状态变化 |

## 最小示例

```arkts
@Entry
@Component
struct VideoDemo {
  private controller: VideoController = new VideoController()
  build() {
    Video({
      src: $r('app.media.intro'),
      controller: this.controller,
      previewUri: $r('app.media.cover')
    })
      .width('100%').height(200)
      .controls(true)
      .autoPlay(false)
      .borderRadius({radius-md})
  }
}
```

## 关联组件

- [`image`](../image/component.md) — 封面图
- [`progress`](../progress/component.md) — 自定义播放进度条

## 参考链接

- ArkTS 官方文档 - 视频播放 (Video): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-video-player
