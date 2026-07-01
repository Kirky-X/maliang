# Flutter Card 属性列表与默认值

本文档汇总 `Card` 及其 M3 变体(`Card.filled` / `Card.outlined`)的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## Card 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget?` | `null` | 卡片内容 |
| `color` | `Color?` | `null`(取主题 `{color-surface}`) | 背景色 |
| `shadowColor` | `Color?` | `null`(取主题 `{color-shadow}`) | 阴影色 |
| `surfaceTintColor` | `Color?` | `null`(取主题 `{color-primary}`) | 表面染色(M3 elevation tint) |
| `elevation` | `double?` | `null`(M3 默认 1.0) | 阴影高度 |
| `shape` | `ShapeBorder?` | `null`(M3 默认 12dp 圆角矩形) | 形状 |
| `borderOnForeground` | `bool` | `true` | 边框是否在前台 |
| `margin` | `EdgeInsetsGeometry?` | `null`(默认 `EdgeInsets.all(4)`) | 外边距 |
| `clipBehavior` | `Clip?` | `Clip.none` | 裁剪行为 |
| `semanticContainer` | `bool` | `true` | 是否为语义容器 |

## Card.filled 属性差异

| 属性 | 差异 |
| --- | --- |
| `elevation` | 固定为 `0.0`(忽略传入值) |
| `color` | 默认取 `{color-surface-variant}`(更高对比度) |
| 其他 | 与 `Card` 相同 |

## Card.outlined 属性差异

| 属性 | 差异 |
| --- | --- |
| `elevation` | 固定为 `0.0`(忽略传入值) |
| `shape` | 默认带 1px `{color-outline-variant}` 边框 |
| `surfaceTintColor` | 默认 `Colors.transparent`(无 tint) |
| 其他 | 与 `Card` 相同 |

## ShapeBorder 子类(常用)

| 子类 | 用途 |
| --- | --- |
| `RoundedRectangleBorder(borderRadius, side)` | 圆角矩形(默认) |
| `StadiumBorder()` | 全圆角(胶囊形) |
| `BeveledRectangleBorder(borderRadius, side)` | 斜角矩形 |
| `ContinuousRectangleBorder(borderRadius, side)` | 连续圆角(更平滑) |
| `CircleBorder()` | 圆形 |

## Clip 取值

| 取值 | 说明 |
| --- | --- |
| `Clip.none` | 不裁剪(默认) |
| `Clip.hardEdge` | 硬边裁剪(性能优) |
| `Clip.antiAlias` | 抗锯齿裁剪(图像推荐) |
| `Clip.antiAliasWithSaveLayer` | 抗锯齿 + SaveLayer(最耗性能,慎用) |

## M3 elevation 默认值

| 变体 | 默认 elevation |
| --- | --- |
| `Card`(标准) | `1.0` |
| `Card.filled` | `0.0` |
| `Card.outlined` | `0.0` |

## M3 surfaceTintColor 与 elevation 关系

启用 `surfaceTintColor`(M3 elevation tint)时,卡片背景色随 elevation 渐变:

| elevation | surfaceTintColor 应用比例 |
| --- | --- |
| 0 | 0%(纯 surface 色) |
| 1 | ~5% |
| 3 | ~10% |
| 6 | ~12% |
| 12 | ~14% |

> `surfaceTintColor: Colors.transparent` 可禁用 M3 elevation tint,使用纯背景色。

## CardTheme 主题级配置

通过 `ThemeData.cardTheme` 注入主题级样式:

```dart
ThemeData(
  cardTheme: CardTheme(
    color: {color-surface},
    shadowColor: {color-shadow},
    surfaceTintColor: {color-primary},
    elevation: {elevation-sm},
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular({radius-md}),
    ),
    margin: const EdgeInsets.all({spacing-sm}),
    clipBehavior: Clip.antiAlias,
  ),
)
```

## 事件回调

`Card` 本身无事件回调;通过 `InkWell` / `GestureDetector` 包裹实现交互:

| 包裹方式 | 水波纹效果 | 点击区域 |
| --- | --- | --- |
| `InkWell` | 有(Material 风格) | 全部子节点 |
| `GestureDetector` | 无 | 全部子节点 |
| `InkResponse` | 有(可定制) | 可指定 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class CardFullSample extends StatelessWidget {
  const CardFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Card 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 媒体卡片(图片 + 文字)
          Card(
            clipBehavior: Clip.antiAlias,
            elevation: {elevation-md},
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular({radius-lg}),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Image.network(
                  'https://example.com/cover.jpg',
                  height: {size-lg},
                  width: double.infinity,
                  fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) => Container(
                    height: {size-lg},
                    color: {color-bg-secondary},
                    alignment: Alignment.center,
                    child: const Icon(Icons.broken_image),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all({spacing-md}),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '媒体卡片标题',
                        style: TextStyle(
                          fontSize: {font-size-lg},
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const SizedBox(height: {spacing-xs}),
                      Text(
                        '副标题描述',
                        style: TextStyle(color: {color-text-secondary}),
                      ),
                      const SizedBox(height: {spacing-sm}),
                      Row(
                        children: [
                          Icon(Icons.access_time, size: {icon-size-sm},
                              color: {color-text-secondary}),
                          const SizedBox(width: {spacing-xs}),
                          Text(
                            '2 小时前',
                            style: TextStyle(
                              color: {color-text-secondary},
                              fontSize: {font-size-sm},
                            ),
                          ),
                          const Spacer(),
                          TextButton(onPressed: () {}, child: const Text('阅读')),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          // 2. 可点击卡片(InkWell)
          Card(
            clipBehavior: Clip.antiAlias,
            child: InkWell(
              onTap: () => debugPrint('点击卡片'),
              onLongPress: () => debugPrint('长按卡片'),
              child: const ListTile(
                leading: Icon(Icons.notifications),
                title: Text('可点击卡片'),
                subtitle: Text('点击或长按触发'),
                trailing: Icon(Icons.chevron_right),
              ),
            ),
          ),
          // 3. 三种变体对比
          Row(
            children: [
              Expanded(
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all({spacing-sm}),
                    child: const Text('标准\n(elevation 1)'),
                  ),
                ),
              ),
              Expanded(
                child: Card.filled(
                  child: Padding(
                    padding: const EdgeInsets.all({spacing-sm}),
                    child: const Text('填充\n(elevation 0)'),
                  ),
                ),
              ),
              Expanded(
                child: Card.outlined(
                  child: Padding(
                    padding: const EdgeInsets.all({spacing-sm}),
                    child: const Text('描边\n(elevation 0)'),
                  ),
                ),
              ),
            ],
          ),
          // 4. 列表卡片(多个 ListTile)
          Card(
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.person),
                  title: const Text('张三'),
                  subtitle: const Text('设计师'),
                  trailing: IconButton(
                    icon: const Icon(Icons.more_vert),
                    onPressed: () {},
                  ),
                ),
                const Divider(height: 1),
                ListTile(
                  leading: const Icon(Icons.person),
                  title: const Text('李四'),
                  subtitle: const Text('工程师'),
                ),
                const Divider(height: 1),
                ListTile(
                  leading: const Icon(Icons.person),
                  title: const Text('王五'),
                  subtitle: const Text('产品经理'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

## 注意事项

- `Card` 默认 `elevation: 1.0`(M3);过高的 elevation 会让卡片"漂浮",M3 推荐 0-3 范围。
- `clipBehavior: Clip.antiAlias` 让圆角裁剪生效,**带图片或 InkWell 的卡片必填**,否则圆角处不裁剪。
- `surfaceTintColor` 是 M3 elevation tint,与 `color` 共同决定背景;`color` 是基底色,`surfaceTintColor` 按 elevation 比例叠加。
- `Card` 本身无点击事件,必须用 `InkWell` 包裹 `child`;**直接用 `GestureDetector` 会丢失水波纹效果**。
- `InkWell` 的水波纹需要 `Material` 祖先;`Card` 内部已含 `Material`,因此 `InkWell` 直接作为 `Card.child` 即可。
- `margin` 是外边距,`padding` 由 `child` 内部控制;`Card` 自身无 `padding` 属性。
- `Card.filled` 与 `Card.outlined` 是 M3 新增(Flutter 3.0+),旧版本需用 `Card(elevation: 0)` 或 `Card(shape: ...)` 模拟。
