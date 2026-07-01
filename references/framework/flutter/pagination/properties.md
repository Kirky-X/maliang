# Flutter Pagination 属性列表与默认值

> **本框架无原生 Pagination Widget,以下为替代方案的属性汇总。**

## 占位说明

Flutter 不存在 `Pagination` 类。本文档汇总替代实现(`TextButton` + `FilledButton` + `ScrollController` + 第三方包)的关键属性,供设计 token 映射参考。

## 替代方案 1:TextButton / FilledButton(页码按钮)

详见 `button/properties.md`。核心属性:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `onPressed` | `VoidCallback?` | 必填 | 点击回调(`null` 禁用) |
| `child` | `Widget` | 必填 | 按钮内容(页码文字) |
| `style` | `ButtonStyle?` | `null` | 样式 |

### FilledButton 选中态样式

| 属性名 | 类型 | 默认值(MD3) | 说明 |
| --- | --- | --- | --- |
| `backgroundColor` | `MaterialStateProperty<Color?>?` | `{color-primary}` | 选中页码背景 |
| `foregroundColor` | `MaterialStateProperty<Color?>?` | `{color-on-primary}` | 选中页码文字 |
| `minimumSize` | `MaterialStateProperty<Size?>?` | `Size(40, 40)` | 最小尺寸 |

## 替代方案 2:IconButton(上/下一页)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `onPressed` | `VoidCallback?` | 必填 | 点击回调 |
| `icon` | `Widget` | 必填 | 图标(常用 `Icons.chevron_left` / `Icons.chevron_right`) |
| `iconSize` | `double` | `24.0` | 图标尺寸 |
| `color` | `Color?` | `null` | 图标色 |
| `disabledColor` | `Color?` | `null` | 禁用态色 |
| `tooltip` | `String?` | `null` | tooltip |
| `style` | `ButtonStyle?` | `null` | 样式(M3) |

## 替代方案 3:ScrollController(无限滚动)

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `initialScrollOffset` | `double` | `0.0` | 初始滚动位置 |
| `keepScrollOffset` | `bool` | `true` | 是否保持滚动位置 |
| `debugLabel` | `String?` | `null` | 调试标签 |
| `onAttach` | `ValueChanged<ScrollPosition>?` | `null` | 附加位置时回调 |
| `onDetach` | `ValueChanged<ScrollPosition>?` | `null` | 分离位置时回调 |

### ScrollController 方法

| 方法 | 说明 |
| --- | --- |
| `addListener(VoidCallback)` | 添加监听器 |
| `removeListener(VoidCallback)` | 移除监听器 |
| `jumpTo(double)` | 跳转到指定位置(无动画) |
| `animateTo(double, duration, curve)` | 带动画跳转 |
| `position` | 当前 `ScrollPosition`(可读取 `pixels` / `maxScrollExtent`) |

### 监听接近底部触发加载

```dart
_controller.addListener(() {
  final pos = _controller.position;
  if (pos.pixels >= pos.maxScrollExtent * 0.9 && !_isLoading && _hasMore) {
    _loadMore();
  }
});
```

## 替代方案 4:infinite_scroll_pagination 包

`infinite_scroll_pagination`(https://pub.flutter-io.cn/packages/infinite_scroll_pagination)提供:

### PagingController 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `firstPageKey` | `K` | 必填 | 首页 key |
| `invisibleItemsThreshold` | `int?` | `null` | 触发加载的剩余项数 |

### PagingController 方法

| 方法 | 说明 |
| --- | --- |
| `addPageRequestListener(listener)` | 添加分页请求监听 |
| `appendPage(List<Item>, nextKey)` | 追加一页 |
| `appendLastPage(List<Item>)` | 追加最后一页(无 nextKey) |
| `error = Object` | 触发错误状态 |
| `refresh()` | 重置并重新加载首页 |

### PagedListView 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `pagingController` | `PagingController<K, T>` | 必填 | 分页控制器 |
| `builderDelegate` | `PagedChildBuilderDelegate<T>` | 必填 | 构建器委托 |
| `padding` | `EdgeInsets?` | `null` | 内边距 |
| `shrinkWrap` | `bool` | `false` | 是否按内容收缩 |

## 设计 token 映射建议

| 场景 | 推荐 token |
| --- | --- |
| 选中页码背景 | `{color-primary}` |
| 选中页码文字 | `{color-on-primary}` |
| 未选中页码文字 | `{color-text-primary}` |
| 禁用态文字 | `{color-on-surface}` 38% |
| 页码尺寸 | `{size-md}`(40×40) |
| 页码间距 | `{spacing-xs}` |
| 上/下一页图标 | `{color-text-secondary}` / `{icon-size-sm}` |

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- Flutter 官方文档 - 列表 & 网格: https://docs.flutter.cn/ui/layout/lists
- API 参考 - ScrollController: https://api.flutter.dev/flutter/widgets/ScrollController-class.html
- API 参考 - ListView: https://api.flutter.dev/flutter/widgets/ListView-class.html
- API 参考 - IconButton: https://api.flutter.dev/flutter/material/IconButton-class.html
- pub.dev - infinite_scroll_pagination: https://pub.flutter-io.cn/packages/infinite_scroll_pagination
