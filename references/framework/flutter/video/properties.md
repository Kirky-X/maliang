# Flutter Video 属性列表与默认值

本文档汇总 `video_player` 插件的完整属性、方法与默认值。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## VideoPlayer 构造参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `controller` | `VideoPlayerController` | 必填 | 控制器实例 |
| `aspectRatio` | `double?` | `null`(取视频原生比例) | 强制宽高比 |

## VideoPlayerController.networkUrl 参数

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `url` | `Uri` | 必填 | 视频 URL |
| `httpHeaders` | `Map<String, String>` | `{}` | HTTP 请求头(鉴权用) |
| `closedCaptionFile` | `Future<ClosedCaptionFile>?` | `null` | 字幕文件 |
| `formatHint` | `VideoFormat?` | `null` | 格式提示(优化探测) |

## VideoFormat 取值

| 取值 | 说明 |
| --- | --- |
| `VideoFormat.ss` | Smooth Streaming |
| `VideoFormat.hls` | HTTP Live Streaming(.m3u8) |
| `VideoFormat.dash` | Dynamic Adaptive Streaming |
| `VideoFormat.other` | 其他(MP4/WebM 等) |

> 提供 `formatHint` 可跳过格式探测,缩短初始化时间;不确定时省略。

## VideoPlayerValue 状态属性

`controller.value` 返回 `VideoPlayerValue`,核心字段:

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `isInitialized` | `bool` | 是否完成初始化 |
| `isPlaying` | `bool` | 是否播放中 |
| `isLooping` | `bool` | 是否循环播放 |
| `isBuffering` | `bool` | 是否缓冲中 |
| `position` | `Duration` | 当前播放位置 |
| `duration` | `Duration` | 视频总时长 |
| `size` | `Size` | 视频尺寸(宽 × 高) |
| `aspectRatio` | `double` | 宽高比(`size.width / size.height`) |
| `playbackSpeed` | `double` | 播放倍速(默认 `1.0`) |
| `volume` | `double` | 音量(0.0-1.0) |
| `errorDescription` | `String?` | 错误描述(`null` 表示无错误) |
| `caption` | `Caption` | 当前字幕 |

## VideoPlayerController 方法

### 生命周期

| 方法 | 返回 | 说明 |
| --- | --- | --- |
| `initialize()` | `Future<void>` | 初始化(加载视频元数据) |
| `dispose()` | `void` | 释放资源(必填) |
| `play()` | `Future<void>` | 开始播放 |
| `pause()` | `Future<void>` | 暂停 |
| `seekTo(Duration)` | `Future<void>` | 跳转到指定位置 |
| `setLooping(bool)` | `Future<void>` | 设置循环 |
| `setVolume(double)` | `Future<void>` | 设置音量(0.0-1.0) |
| `setPlaybackSpeed(double)` | `Future<void>` | 设置播放倍速(0.25-2.0) |
| `setMixWithOthers(bool)` | `Future<void>` | 是否与其他音频混播 |

### 监听

| 方法 | 说明 |
| --- | --- |
| `addListener(VoidCallback)` | 监听状态变化(每次 `value` 更新触发) |
| `removeListener(VoidCallback)` | 移除监听 |
| `value` | 获取当前 `VideoPlayerValue` |

## VideoProgressIndicator 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `controller` | `VideoPlayerController` | 必填 | 控制器 |
| `allowScrubbing` | `bool` | `false` | 是否允许拖动跳转 |
| `colors` | `VideoProgressColors` | 见下表 | 颜色配置 |
| `padding` | `EdgeInsets` | `EdgeInsets.only(top: 5.0)` | 内边距 |

## VideoProgressColors 默认值

| 属性名 | 默认值 | 说明 |
| --- | --- | --- |
| `playedColor` | `{color-primary}` | 已播放部分颜色 |
| `bufferedColor` | `Color.fromRGBO(50, 50, 50, 0.7)` | 缓冲部分颜色 |
| `backgroundColor` | `{color-bg-tertiary}` | 背景颜色 |

## 完整示例

```dart
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

class VideoFullSample extends StatefulWidget {
  const VideoFullSample({super.key});

  @override
  State<VideoFullSample> createState() => _VideoFullSampleState();
}

class _VideoFullSampleState extends State<VideoFullSample> {
  late VideoPlayerController _controller;
  bool _initialized = false;
  double _playbackSpeed = 1.0;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.networkUrl(
      Uri.parse('https://example.com/sample.mp4'),
      httpHeaders: const {'Authorization': 'Bearer xxx'},
      formatHint: VideoFormat.other,
    )..initialize().then((_) {
      if (mounted) {
        setState(() => _initialized = true);
        _controller.addListener(_onVideoUpdate);
      }
    }).catchError((e) {
      debugPrint('视频初始化失败: $e');
    });
  }

  void _onVideoUpdate() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    _controller.removeListener(_onVideoUpdate);
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!_initialized) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (_controller.value.hasError) {
      return Scaffold(
        body: Center(
          child: Text(
            '视频加载失败: ${_controller.value.errorDescription}',
            style: TextStyle(color: {color-error}),
          ),
        ),
      );
    }

    final value = _controller.value;
    return Scaffold(
      appBar: AppBar(title: const Text('Video 完整示例')),
      body: Column(
        children: [
          AspectRatio(
            aspectRatio: value.aspectRatio,
            child: VideoPlayer(_controller),
          ),
          Padding(
            padding: const EdgeInsets.all({spacing-sm}),
            child: Column(
              children: [
                // 进度条
                VideoProgressIndicator(
                  _controller,
                  allowScrubbing: true,
                  colors: const VideoProgressColors(
                    playedColor: {color-primary},
                    bufferedColor: {color-bg-secondary},
                    backgroundColor: {color-bg-tertiary},
                  ),
                ),
                Row(
                  children: [
                    // 播放/暂停
                    IconButton(
                      icon: Icon(
                        value.isPlaying ? Icons.pause : Icons.play_arrow,
                        color: {color-on-surface},
                      ),
                      onPressed: () {
                        value.isPlaying
                            ? _controller.pause()
                            : _controller.play();
                      },
                    ),
                    // 时间显示
                    Text(
                      '${_formatDuration(value.position)} / ${_formatDuration(value.duration)}',
                      style: const TextStyle(fontSize: {font-size-sm}),
                    ),
                    const Spacer(),
                    // 倍速切换
                    DropdownButton<double>(
                      value: _playbackSpeed,
                      items: const [
                        DropdownMenuItem(value: 0.5, child: Text('0.5x')),
                        DropdownMenuItem(value: 1.0, child: Text('1.0x')),
                        DropdownMenuItem(value: 1.5, child: Text('1.5x')),
                        DropdownMenuItem(value: 2.0, child: Text('2.0x')),
                      ],
                      onChanged: (v) {
                        if (v != null) {
                          _controller.setPlaybackSpeed(v);
                          setState(() => _playbackSpeed = v);
                        }
                      },
                    ),
                    // 音量
                    IconButton(
                      icon: Icon(
                        value.volume > 0 ? Icons.volume_up : Icons.volume_off,
                        color: {color-on-surface},
                      ),
                      onPressed: () {
                        _controller.setVolume(value.volume > 0 ? 0 : 1);
                      },
                    ),
                  ],
                ),
                // 缓冲指示
                if (value.isBuffering)
                  LinearProgressIndicator(
                    color: {color-primary},
                    backgroundColor: {color-bg-secondary},
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _formatDuration(Duration d) {
    final m = d.inMinutes.remainder(60).toString().padLeft(2, '0');
    final s = d.inSeconds.remainder(60).toString().padLeft(2, '0');
    return '$m:$s';
  }
}
```

## 注意事项

- **务必调用 `dispose()`**:`VideoPlayerController` 持有原生资源(编解码器、纹理),未释放会持续占用内存与 GPU。
- `initialize()` 是异步操作,UI 应等待 `isInitialized == true` 后再渲染 `VideoPlayer`;未初始化时渲染会抛 `UnimplementedError`。
- `addListener` 触发频率高(每帧播放进度更新都会触发),回调中**不要做重计算**,使用 `setState` 时务必先检查 `mounted`。
- iOS 模拟器不支持硬解码,视频会显示黑屏但音频正常;真机测试正常。
- Web 平台需要服务端配置 CORS 头(`Access-Control-Allow-Origin`),否则 `networkUrl` 加载失败且无明确错误提示。
- 后台进入前台时,`isPlaying` 状态可能与实际不符;应在 `WidgetsBindingObserver.didChangeAppLifecycleState` 中显式 `pause()` 或 `play()`。
- `setPlaybackSpeed` 的有效范围是 0.25-2.0,超出范围会被平台忽略(无错误抛出)。
