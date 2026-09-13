# Flutter Upload 属性列表与默认值

本文档汇总上传组合方案的核心 API:image_picker / file_picker 常用参数与文件列表/进度的 Widget 属性。所有颜色默认值以 design token 形式给出。

## ImagePicker 常用参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `source` | `ImageSource` | 必填 | `gallery` 相册 / `camera` 相机 |
| `maxWidth` / `maxHeight` | `double?` | `null`(原图) | 压缩上限,上传场景建议设 1920 |
| `imageQuality` | `int?` | `null`(100) | JPEG 压缩质量(0-100) |
| `limit`(pickMultiImage) | `int?` | `null` | 最多选取张数 |

## FilePicker.pickFiles 常用参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `type` | `FileType` | `FileType.any` | any/media/image/video/audio/custom |
| `allowedExtensions` | `List<String>?` | `null` | `type: FileType.custom` 时必填(如 `['pdf']`) |
| `allowMultiple` | `bool` | `false` | 是否多选 |
| `withData` | `bool` | `false` | 是否载入字节流(大文件建议 `false` 用 path) |
| `maxSize` | `int?` | `null` | 单文件上限(KB) |

## PlatformFile 关键字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `name` | `String` | 文件名 |
| `size` | `int` | 字节数 |
| `path` | `String?` | 本地路径(`withData: false` 时的取数来源) |

## 文件列表项(ListTile)建议属性

| 属性 | 建议值 | 说明 |
| --- | --- | --- |
| `leading` | `Image.file` 缩略图或 `Icon` | 56 × 56 以内,`{radius-sm}` 圆角 |
| `title` | 文件名,单行截断 | `maxLines: 1` + `overflow: ellipsis` |
| `subtitle` | `LinearProgressIndicator(value: p)` | p ∈ [0,1];`null` 表示不确定进度 |
| `trailing` | 状态文本 / 重试 IconButton | 失败态用 `{color-error}` + 重试入口 |

## 四态语义

| 状态 | 视觉 | 交互 |
| --- | --- | --- |
| 等待 | subtitle 显示"等待中" | 可取消 |
| 上传中 | `LinearProgressIndicator(value: p)` | 可取消 |
| 成功 | trailing `Icon(Icons.check_circle, color: {color-success})` | — |
| 失败 | trailing"失败" + 重试按钮,`{color-error}` | 保留文件可重试 |

## 完整示例

```dart
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

class UploadQueueSample extends StatefulWidget {
  const UploadQueueSample({super.key});

  @override
  State<UploadQueueSample> createState() => _UploadQueueSampleState();
}

class _Item {
  _Item(this.name, {this.progress = 0, this.failed = false});
  final String name;
  double progress;
  bool failed;
}

class _UploadQueueSampleState extends State<UploadQueueSample> {
  final List<_Item> _items = [];

  Future<void> _pick() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'doc', 'docx'],
      allowMultiple: true,
    );
    if (result != null) {
      setState(() {
        _items.addAll(result.files.map((f) => _Item(f.name)));
      });
      // 逐个上传:成功 progress=1,失败 failed=true
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('附件上传')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all({spacing-md}),
            child: OutlinedButton.icon(
              onPressed: _pick,
              icon: const Icon(Icons.attach_file),
              label: const Text('选择文件(≤ 10MB)'),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: _items.length,
              itemBuilder: (_, i) {
                final f = _items[i];
                return ListTile(
                  leading: const Icon(Icons.description),
                  title: Text(f.name, maxLines: 1, overflow: TextOverflow.ellipsis),
                  subtitle: f.failed
                      ? const Text('上传失败',
                          style: TextStyle(color: {color-error}))
                      : LinearProgressIndicator(value: f.progress),
                  trailing: f.failed
                      ? IconButton(
                          icon: const Icon(Icons.refresh),
                          tooltip: '重试',
                          onPressed: () => setState(() {
                            f.failed = false;
                            f.progress = 0;
                          }),
                        )
                      : Text('${(f.progress * 100).round()}%',
                          style: Theme.of(context).textTheme.bodySmall),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- **picker 包为平台通道实现**,需 iOS Info.plist 相册权限描述(NSPhotoLibraryUsageDescription)与 Android 存储权限声明。
- 上传场景图片先压缩(`maxWidth` / `imageQuality`),避免原图直传流量浪费。
- `withData: false` 大文件用 `path` 流式读取;`withData: true` 会把字节载入内存,大附件慎用。
- 触控目标:触发器与重试按钮热区 ≥44/48(MaterialTapTargetSize.padded)。
- 无障碍:ListTile 自带语义;进度对读屏用户用 `Semantics(label: '上传中 40%')` 播报。
