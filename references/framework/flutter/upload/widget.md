# Flutter Upload Widget 定义

> **本组件为 maliang 组合方案,Flutter 无原生 Upload Widget。** 通过生态标准 picker 包(`image_picker` / `file_picker`)+ `List` 文件列表 + `LinearProgressIndicator` 进度组合实现上传。

## 缺失原因

Flutter Material 未提供统一 Upload 控件;平台文件/媒体选取依赖宿主能力,由 pub.dev 验证过的 picker 包承担。

## 替代方案(组合结构)

| 角色 | Flutter 实现 |
| --- | --- |
| 触发器 | `FilledButton` / `OutlinedButton` / `IconButton` |
| 图片选取 | `image_picker` 包(`ImagePicker().pickImage / pickMultiImage`) |
| 文件选取 | `file_picker` 包(`FilePicker.platform.pickFiles`) |
| 文件列表 | `ListView` + `ListTile`(缩略图 + 文件名 + 状态) |
| 进度/状态 | `LinearProgressIndicator` + 状态文本(上传中/成功/失败重试) |

## 核心 API

```dart
import 'package:image_picker/image_picker.dart';
import 'package:file_picker/file_picker.dart';

// 单图 / 多图
final picker = ImagePicker();
final XFile? photo = await picker.pickImage(source: ImageSource.gallery, maxWidth: 1920);
final List<XFile> images = await picker.pickMultiImage(limit: 9);

// 任意文件
final result = await FilePicker.platform.pickFiles(
  type: FileType.custom,
  allowedExtensions: ['pdf', 'doc', 'docx'],
  withData: false,
);
// result?.files: List<PlatformFile>(name / size / path)
```

## 最小示例

```dart
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

/// Upload 最小示例:多图选择 + 上传队列
class UploadSample extends StatefulWidget {
  const UploadSample({super.key});

  @override
  State<UploadSample> createState() => _UploadSampleState();
}

class _UploadSampleState extends State<UploadSample> {
  final List<XFile> _files = [];
  final ImagePicker _picker = ImagePicker();

  Future<void> _pick() async {
    final images = await _picker.pickMultiImage(limit: 9);
    if (images != null) setState(() => _files.addAll(images));
    // 逐个进入上传队列,进度驱动 LinearProgressIndicator
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Upload 示例')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all({spacing-md}),
            child: FilledButton.icon(
              onPressed: _pick,
              icon: const Icon(Icons.upload),
              label: const Text('选择图片'),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: _files.length,
              itemBuilder: (_, i) => ListTile(
                leading: const Icon(Icons.image),
                title: Text(_files[i].name),
                subtitle: const LinearProgressIndicator(value: 0.4),
                trailing: Text('40%',
                    style: Theme.of(context).textTheme.bodySmall),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

## 参考链接

- pub.dev - image_picker: https://pub.dev/packages/image_picker
- pub.dev - file_picker: https://pub.dev/packages/file_picker
- Flutter 官方文档 - ListTile: https://api.flutter.dev/flutter/material/ListTile-class.html
