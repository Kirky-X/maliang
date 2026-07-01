# Flutter Video Widget 定义

## Widget 定义

Flutter 官方通过 `video_player` 插件提供视频播放能力,核心 Widget 为 `VideoPlayer`(StatefulWidget),配合 `VideoPlayerController` 管理播放状态。Flutter SDK 自身未内置视频 Widget,需引入 `video_player` 包。高级封装可使用 `chewie`(基于 `video_player` 的 Material 风格播放器 UI)。

| Video 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 基础播放器 | `VideoPlayer` | `StatefulWidget` | 渲染视频画面,无控制 UI |
| 网络视频 | `VideoPlayerController.networkUrl` | `VideoPlayerController` | 播放网络 URL 视频 |
| 资源视频 | `VideoPlayerController.asset` | `VideoPlayerController` | 播放 assets 资源 |
| 文件视频 | `VideoPlayerController.file` | `VideoPlayerController` | 播放本地文件 |
| 高级封装 | `Chewie`(第三方) | `StatelessWidget` | 带播放/暂停/进度条 UI |

> `VideoPlayer` 本身仅渲染画面,业务层需自行实现控制 UI(播放/暂停/进度/全屏)。

## 构造函数

### VideoPlayer

```dart
const VideoPlayer(VideoPlayerController controller, {
  Key? key,
  double aspectRatio,
})
```

### VideoPlayerController.networkUrl

```dart
VideoPlayerController.networkUrl(
  Uri url, {
  httpHeaders = const <String, String>{},
  Future<ClosedCaptionFile>? closedCaptionFile,
  VideoFormat? formatHint,
})
```

### VideoPlayerController.asset

```dart
VideoPlayerController.asset(
  String dataSource, {
  String? package,
  Future<ClosedCaptionFile>? closedCaptionFile,
})
```

### VideoPlayerController.file

```dart
VideoPlayerController.file(File file, {Future<ClosedCaptionFile>? closedCaptionFile})
```

## 核心属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `controller` | `VideoPlayerController` | 控制器,管理播放状态 |
| `aspectRatio` | `double?` | 宽高比(如 16/9);`null` 时按视频原生比例 |
| `closedCaptionFile` | `Future<ClosedCaptionFile>?` | 字幕文件 |
| `formatHint` | `VideoFormat?` | 格式提示(优化探测) |

## 最小示例

```dart
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

/// Video 最小示例:网络视频播放 + 基础控制
class VideoSample extends StatefulWidget {
  const VideoSample({super.key});

  @override
  State<VideoSample> createState() => _VideoSampleState();
}

class _VideoSampleState extends State<VideoSample> {
  late VideoPlayerController _controller;
  bool _initialized = false;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.networkUrl(
      Uri.parse('https://example.com/sample.mp4'),
    )..initialize().then((_) {
      setState(() => _initialized = true);
      _controller.setLooping(true);
      _controller.play();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Video 示例')),
      body: Center(
        child: _initialized
            ? Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  AspectRatio(
                    aspectRatio: _controller.value.aspectRatio,
                    child: VideoPlayer(_controller),
                  ),
                  Padding(
                    padding: const EdgeInsets.all({spacing-sm}),
                    child: Row(
                      children: [
                        IconButton(
                          icon: Icon(
                            _controller.value.isPlaying
                                ? Icons.pause
                                : Icons.play_arrow,
                          ),
                          onPressed: () {
                            setState(() {
                              _controller.value.isPlaying
                                  ? _controller.pause()
                                  : _controller.play();
                            });
                          },
                        ),
                        Expanded(
                          child: VideoProgressIndicator(
                            _controller,
                            allowScrubbing: true,
                            colors: const VideoProgressColors(
                              playedColor: {color-primary},
                              bufferedColor: {color-bg-secondary},
                              backgroundColor: {color-bg-tertiary},
                            ),
                          ),
                        ),
                        Text(
                          '${_controller.value.position.inSeconds}s',
                          style: const TextStyle(fontSize: {font-size-sm}),
                        ),
                      ],
                    ),
                  ),
                ],
              )
            : const CircularProgressIndicator(),
      ),
    );
  }
}
```

## 自定义控制 UI(MD3 主题映射)

```dart
Container(
  padding: const EdgeInsets.all({spacing-sm}),
  decoration: BoxDecoration(
    color: {color-surface},
    borderRadius: BorderRadius.circular({radius-md}),
  ),
  child: Row(
    children: [
      Icon(
        Icons.play_arrow,
        color: {color-on-surface},
        size: {icon-size-md},
      ),
      Expanded(
        child: Slider(
          value: _controller.value.position.inMilliseconds.toDouble(),
          min: 0,
          max: _controller.value.duration.inMilliseconds.toDouble(),
          activeColor: {color-primary},
          inactiveColor: {color-bg-secondary},
          onChanged: (v) {
            _controller.seekTo(Duration(milliseconds: v.toInt()));
          },
        ),
      ),
    ],
  ),
)
```

> 注:示例中的 `{color-primary}`、`{spacing-sm}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - 播放及暂停视频: https://docs.flutter.cn/cookbook/plugins/play-video
- pub.dev - video_player: https://pub.flutter-io.cn/packages/video_player
- pub.dev - chewie: https://pub.flutter-io.cn/packages/chewie
- API 参考 - VideoPlayer: https://pub.dev/documentation/video_player/latest/video_player/VideoPlayer-class.html
