# Flutter Pagination Widget 定义

> **本框架无原生 Pagination Widget。**

## 占位说明

Flutter Material Design 3 **未提供名为 `Pagination` / `Pager` 的独立 Widget**。其他框架(Ant Design `Pagination`、Element `el-pagination`)中的分页器,在 Flutter 中通过以下方式实现:

| 其他框架的 Pagination 场景 | Flutter 对应实现 |
| --- | --- |
| 简单上一页/下一页 | `Row` + `TextButton` + `Text` |
| 数字页码分页 | `Wrap` + `TextButton` / `FilledButton`(选中态) |
| 大数据分页 | `ListView.builder` + `ScrollController`(无限滚动) |
| 桌面端完整分页 | `NavigationRail` / 自定义 `Row` + `IconButton` |
| 第三方分页包 | `pagination_view` / `infinite_scroll_pagination` |

> Flutter 推荐使用"无限滚动 + 渐进加载"代替传统分页器,详见 `scroll/properties.md` 中的 `ScrollController` 监听。

## 推荐替代方案

### 1. 简单上一页/下一页 → Row + TextButton

```dart
Row(
  mainAxisAlignment: MainAxisAlignment.center,
  children: [
    TextButton(
      onPressed: _hasPrev ? () => _onPageChange(_currentPage - 1) : null,
      child: const Text('上一页'),
    ),
    Padding(
      padding: EdgeInsets.symmetric(horizontal: {spacing-md}),
      child: Text(
        '${_currentPage + 1} / $_totalPages',
        style: TextStyle(fontSize: {font-size-md}, color: {color-text-primary}),
      ),
    ),
    TextButton(
      onPressed: _hasNext ? () => _onPageChange(_currentPage + 1) : null,
      child: const Text('下一页'),
    ),
  ],
)
```

### 2. 数字页码 → Wrap + TextButton

```dart
class NumberPagination extends StatelessWidget {
  const NumberPagination({
    super.key,
    required this.currentPage,
    required this.totalPages,
    required this.onPageChanged,
  });

  final int currentPage;
  final int totalPages;
  final ValueChanged<int> onPageChanged;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: {spacing-xs},
      children: List.generate(totalPages, (i) {
        final isActive = i == currentPage;
        return SizedBox(
          width: {size-md},
          height: {size-md},
          child: isActive
              ? FilledButton(
                  onPressed: null,
                  child: Text('${i + 1}'),
                )
              : TextButton(
                  onPressed: () => onPageChanged(i),
                  child: Text('${i + 1}'),
                ),
        );
      }),
    );
  }
}
```

### 3. 无限滚动 → ListView + ScrollController

```dart
class InfiniteScrollList extends StatefulWidget {
  const InfiniteScrollList({super.key});

  @override
  State<InfiniteScrollList> createState() => _InfiniteScrollListState();
}

class _InfiniteScrollListState extends State<InfiniteScrollList> {
  final ScrollController _controller = ScrollController();
  final List<String> _items = [];
  int _page = 1;
  bool _isLoading = false;
  bool _hasMore = true;

  @override
  void initState() {
    super.initState();
    _loadMore();
    _controller.addListener(() {
      if (_controller.position.pixels >=
              _controller.position.maxScrollExtent * 0.9 &&
          !_isLoading &&
          _hasMore) {
        _loadMore();
      }
    });
  }

  Future<void> _loadMore() async {
    setState(() => _isLoading = true);
    // 模拟网络请求
    await Future.delayed(const Duration(seconds: 1));
    setState(() {
      _items.addAll(List.generate(20, (i) => 'Item ${_items.length + i}'));
      _page++;
      _isLoading = false;
      if (_page > 5) _hasMore = false; // 模拟结束
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: _controller,
      itemCount: _items.length + 1,
      itemBuilder: (_, i) {
        if (i == _items.length) {
          return _isLoading
              ? const Padding(
                  padding: EdgeInsets.all(16),
                  child: Center(child: CircularProgressIndicator()),
                )
              : const SizedBox.shrink();
        }
        return ListTile(title: Text(_items[i]));
      },
    );
  }
}
```

### 4. 第三方包 infinite_scroll_pagination

`infinite_scroll_pagination`(https://pub.flutter-io.cn/packages/infinite_scroll_pagination)提供完整分页能力:

```dart
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';

final PagingController<int, Item> _pagingController =
    PagingController(firstPageKey: 0);

@override
void initState() {
  super.initState();
  _pagingController.addPageRequestListener((pageKey) => _fetchPage(pageKey));
}

PagedListView<int, Item>(
  pagingController: _pagingController,
  builderDelegate: PagedChildBuilderDelegate<Item>(
    itemBuilder: (_, item, __) => ListTile(title: Text(item.title)),
  ),
)
```

> 注:示例中的 `{spacing-md}`、`{spacing-xs}`、`{size-md}`、`{font-size-md}`、`{color-text-primary}` 等为 design token 占位符,实际运行时由主题层解析为具体值。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- Flutter 官方文档 - 列表 & 网格: https://docs.flutter.cn/ui/layout/lists
- API 参考 - ScrollController: https://api.flutter.dev/flutter/widgets/ScrollController-class.html
- API 参考 - ListView: https://api.flutter.dev/flutter/widgets/ListView-class.html
- pub.dev - infinite_scroll_pagination: https://pub.flutter-io.cn/packages/infinite_scroll_pagination
- pub.dev - pagination_view: https://pub.flutter-io.cn/packages/pagination_view
