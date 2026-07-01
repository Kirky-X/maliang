# Video API — Element Plus N/A(替代方案)

> 本组件为 N/A,见 [component.md](./component.md) 替代方案说明。本文件列出 HTML5 原生 `<video>` 元素的属性与事件,作为视频实现的 API 参考。

## `<video>` 属性(原生)

| 属性名        | 类型      | 默认值 | 说明                          |
| ------------- | --------- | ------ | ----------------------------- |
| `src`         | `string`  | —      | 视频地址                      |
| `poster`      | `string`  | —      | 封面图                        |
| `autoplay`    | `boolean` | `false`| 自动播放(受浏览器策略限制) |
| `loop`        | `boolean` | `false`| 循环播放                      |
| `muted`       | `boolean` | `false`| 静音                          |
| `controls`    | `boolean` | `false`| 显示原生控件                  |
| `preload`     | `'auto' \| 'metadata' \| 'none'` | `'metadata'` | 预加载策略 |
| `width`       | `number`  | —      | 宽度                          |
| `height`      | `number`  | —      | 高度                          |
| `playsinline` | `boolean` | `false`| iOS 内联播放(避免全屏)     |

## `<video>` 事件(原生)

| 事件名         | 触发时机                       |
| -------------- | ------------------------------ |
| `loadstart`    | 开始加载                       |
| `loadedmetadata` | 元数据加载完成               |
| `canplay`      | 可开始播放                     |
| `play`         | 播放开始                       |
| `pause`        | 暂停                           |
| `ended`        | 播放结束                       |
| `timeupdate`   | 播放位置改变                   |
| `progress`     | 加载进度更新                   |
| `error`        | 加载/播放错误                  |
| `volumechange` | 音量改变                       |

## HTMLMediaElement 方法(常用)

| 方法        | 签名             | 说明                |
| ----------- | ---------------- | ------------------- |
| `play`      | `() => Promise`  | 播放                |
| `pause`     | `() => void`     | 暂停                |
| `load`      | `() => void`     | 重新加载            |
| `canPlayType` | `(type: string) => string` | 判断是否支持某格式 |

## 与 Element Plus 协同建议

| 视频控件     | Element Plus 替代组件                 |
| ------------ | ------------------------------------- |
| 播放/暂停    | `<el-button :icon>`                   |
| 进度条       | `<el-slider>`                         |
| 音量         | `<el-slider>` + `<el-icon>`           |
| 全屏         | `<el-button>` + Fullscreen API        |
| 加载态       | `<el-skeleton>` / `v-loading`         |

> 以上为原生 API,Element Plus 不额外封装,业务层可基于此自定义视频组件。
