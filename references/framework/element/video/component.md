# Video 视频组件 — Element Plus N/A 说明

> **本框架无原生 Video 组件。**

## 缺失原因

Element Plus 是 UI 组件库,视频播放属于富媒体领域,其编解码、流媒体、字幕、 DRM 等能力超出 UI 组件库职责范围。Element Plus 官方文档中不存在 Video 组件页面,视频播放交由业务层使用 HTML5 原生 `<video>` 元素或第三方播放器(如 `video.js`、`vue-video-player`)实现。

## 替代方案

- 方案 1:直接使用 HTML5 原生 `<video>` 元素,搭配 Element Plus 的容器/控件样式。
- 方案 2:封装 `<video>` 为自定义 Vue 组件,用 `<el-icon>` / `<el-button>` 实现播放控件,`<el-slider>` 作为进度条。
- 方案 3:引入第三方播放器库(如 `video.js`、`xgplayer`、`vue-video-player`)与 Element Plus 协同。

## 替代实现示例(原生 video + Element Plus 控件)

```vue
<template>
  <div class="video-wrap">
    <video ref="videoRef" :src="src" @timeupdate="onTime" />
    <div class="controls">
      <el-button :icon="playing ? VideoPause : VideoPlay" circle @click="toggle" />
      <el-slider v-model="progress" :max="100" :step="0.1" @change="onSeek" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { VideoPlay, VideoPause } from '@element-plus/icons-vue'
const src = 'https://example.com/demo.mp4'
const videoRef = ref()
const playing = ref(false)
const progress = ref(0)
const toggle = () => {
  if (playing.value) videoRef.value.pause()
  else videoRef.value.play()
  playing.value = !playing.value
}
const onTime = () => {
  const v = videoRef.value
  progress.value = (v.currentTime / v.duration) * 100
}
const onSeek = (val) => {
  const v = videoRef.value
  v.currentTime = (val / 100) * v.duration
}
</script>

<style scoped>
.video-wrap {
  border-radius: {radius-md};
  overflow: hidden;
  border: 1px solid {color-border-default};
  background-color: {color-bg-secondary};
}
video { width: 100%; display: block; }
.controls {
  display: flex; align-items: center; gap: {spacing-sm};
  padding: {spacing-sm};
}
</style>
```

## 跨框架对照

| 框架        | 实现方式                                            |
| ----------- | --------------------------------------------------- |
| ArkTS       | `Video` 组件                                        |
| Flutter     | `video_player` 插件 / `VideoPlayer` widget          |
| Element Plus| 无原生(本文件),用 `<video>` + Element Plus 控件  |

## 参考链接

- Element Plus 官方文档:无对应章节
- 相关资源:[MDN video 元素](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/video)、[video.js](https://videojs.com/)
