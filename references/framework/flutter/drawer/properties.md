# Flutter Drawer 属性列表与默认值

本文档汇总 `Drawer` / `DrawerHeader` / `UserAccountsDrawerHeader` 与 `Scaffold` 抽屉相关的完整属性、默认值与回调。所有颜色默认值以 design token 形式给出,不在文档中硬编码。

## Drawer 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget?` | `null` | 抽屉内容 |
| `width` | `double?` | `null`(M3 默认 304.0) | 宽度 |
| `semanticLabel` | `String?` | `null`(默认 'Navigation menu') | 无障碍标签 |
| `onDrawerChanged` | `DrawerCallback?` | `null` | 打开/关闭状态回调 |
| `shape` | `ShapeBorder?` | `null`(M3 默认右侧 16dp 圆角) | 形状 |
| `elevation` | `double?` | `null`(M3 默认 1.0) | 阴影高度 |
| `backgroundColor` | `Color?` | `null`(取主题 `{color-surface}`) | 背景色 |
| `shadowColor` | `Color?` | `null`(取主题 `{color-shadow}`) | 阴影色 |
| `surfaceTintColor` | `Color?` | `null`(取主题 `{color-primary}`) | 表面染色(M3) |
| `clipBehavior` | `Clip?` | `Clip.hardEdge` | 裁剪行为 |

## DrawerHeader 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `child` | `Widget?` | `null` | 头部内容 |
| `margin` | `EdgeInsetsGeometry?` | `EdgeInsets.only(bottom: 8.0)` | 外边距 |
| `padding` | `EdgeInsetsGeometry?` | `EdgeInsets.fromLTRB(16.0, 16.0, 16.0, 8.0)` | 内边距 |
| `decoration` | `Decoration?` | `null`(默认主题色背景) | 装饰 |
| `duration` | `Duration` | `Duration(milliseconds: 250)` | 动画时长 |
| `curve` | `Curve` | `Curves.fastOutSlowIn` | 动画曲线 |

## UserAccountsDrawerHeader 完整属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `currentAccountPicture` | `Widget` | 必填 | 当前账号头像 |
| `otherAccountsPictures` | `Widget?` | `null` | 其他账号头像(右上角) |
| `accountName` | `Widget` | 必填 | 账号名 |
| `accountEmail` | `Widget` | 必填 | 账号邮箱 |
| `onDetailsPressed` | `VoidCallback?` | `null` | 详情切换回调(显示下拉箭头) |
| `decoration` | `Color?` | `null`(取主题) | 装饰色 |
| `arrowColor` | `Color?` | `null`(取主题) | 箭头颜色 |

## Scaffold 抽屉相关属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `drawer` | `Widget?` | `null` | 左侧抽屉 |
| `endDrawer` | `Widget?` | `null` | 右侧抽屉 |
| `drawerEdgeDragWidth` | `double?` | `null`(默认全宽) | 边缘拖拽触发宽度 |
| `drawerEnableOpenDragGesture` | `bool` | `true` | 是否允许拖拽打开左侧抽屉 |
| `endDrawerEnableOpenDragGesture` | `bool` | `true` | 是否允许拖拽打开右侧抽屉 |
| `onDrawerChanged` | `DrawerCallback?` | `null` | 左侧抽屉状态变化 |
| `onEndDrawerChanged` | `DrawerCallback?` | `null` | 右侧抽屉状态变化 |
| `drawerScrimColor` | `Color?` | `null`(默认 `Colors.black54`) | 抽屉遮罩色 |

## ScaffoldState 抽屉方法

| 方法 | 说明 |
| --- | --- |
| `openDrawer()` | 打开左侧抽屉 |
| `openEndDrawer()` | 打开右侧抽屉 |
| `closeDrawer()` | 关闭左侧抽屉(M3 新增) |
| `closeEndDrawer()` | 关闭右侧抽屉(M3 新增) |
| `isDrawerOpen` | `bool` 左侧抽屉是否打开 |
| `isEndDrawerOpen` | `bool` 右侧抽屉是否打开 |

## DrawerCallback 签名

```dart
typedef DrawerCallback = void Function(bool isOpened);
```

## NavigationDrawer(M3 替代版)

Flutter 3.x 引入 `NavigationDrawer`(M3 标准),与 `Drawer` 区别:

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `List<Widget>` | 必填 | 导航项列表 |
| `selectedIndex` | `int?` | `null` | 当前选中项索引 |
| `onDestinationSelected` | `ValueChanged<int>?` | `null` | 选择回调 |
| `backgroundColor` | `Color?` | `null`(取主题) | 背景色 |
| `elevation` | `double?` | `null`(M3 默认 1.0) | 阴影高度 |
| `shadowColor` | `Color?` | `null` | 阴影色 |
| `surfaceTintColor` | `Color?` | `null` | 表面染色 |
| `indicatorColor` | `Color?` | `null`(取主题 `{color-secondary-container}`) | 选中指示器颜色 |
| `indicatorShape` | `ShapeBorder?` | `null`(M3 全圆角) | 选中指示器形状 |
| `tilePadding` | `EdgeInsetsGeometry?` | `EdgeInsets.symmetric(horizontal: 12)` | 项内边距 |
| `extended` | `bool` | `false` | 是否展开(常驻) |

## NavigationDrawerDestination 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `icon` | `Widget` | 必填 | 图标 |
| `selectedIcon` | `Widget?` | `null`(默认 icon) | 选中态图标 |
| `label` | `Widget` | 必填 | 标签 |
| `backgroundColor` | `Color?` | `null` | 背景色 |

## 完整示例

```dart
import 'package:flutter/material.dart';

class DrawerFullSample extends StatefulWidget {
  const DrawerFullSample({super.key});

  @override
  State<DrawerFullSample> createState() => _DrawerFullSampleState();
}

class _DrawerFullSampleState extends State<DrawerFullSample> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drawer 完整示例'),
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () => Scaffold.of(context).openDrawer(),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: () => Scaffold.of(context).openEndDrawer(),
          ),
        ],
      ),
      drawer: Drawer(
        width: {size-drawer},
        backgroundColor: {color-surface},
        elevation: {elevation-md},
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.horizontal(
            right: Radius.circular({radius-lg}),
          ),
        ),
        onDrawerChanged: (isOpen) {
          debugPrint('抽屉 ${isOpen ? "打开" : "关闭"}');
        },
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            // 1. 用户信息头部
            UserAccountsDrawerHeader(
              accountName: const Text('张三'),
              accountEmail: const Text('zhangsan@example.com'),
              currentAccountPicture: CircleAvatar(
                backgroundColor: {color-on-primary},
                child: const Text('张', style: TextStyle(fontSize: {font-size-lg})),
              ),
              otherAccountsPictures: const [
                CircleAvatar(child: Text('L')),
              ],
              decoration: BoxDecoration(color: {color-primary}),
              onDetailsPressed: () {
                debugPrint('切换账号');
              },
            ),
            // 2. 导航项(选中态高亮)
            ListTile(
              leading: const Icon(Icons.inbox),
              title: const Text('收件箱'),
              trailing: const Badge(label: Text('3')),
              selected: _selectedIndex == 0,
              selectedTileColor: {color-primary-container},
              onTap: () {
                setState(() => _selectedIndex = 0);
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.send),
              title: const Text('已发送'),
              selected: _selectedIndex == 1,
              selectedTileColor: {color-primary-container},
              onTap: () {
                setState(() => _selectedIndex = 1);
                Navigator.pop(context);
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('设置'),
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              leading: const Icon(Icons.logout),
              title: const Text('退出登录'),
              onTap: () => Navigator.pop(context),
            ),
          ],
        ),
      ),
      endDrawer: Drawer(
        child: ListView(
          padding: const EdgeInsets.all({spacing-md}),
          children: const [
            Text('筛选', style: TextStyle(fontSize: {font-size-lg})),
            ListTile(title: Text('全部')),
            ListTile(title: Text('未读')),
            ListTile(title: Text('已读')),
          ],
        ),
      ),
      body: Center(child: Text('当前页: $_selectedIndex')),
    );
  }
}
```

## 注意事项

- `Drawer` 内容应为可滚动 Widget(`ListView` / `CustomScrollView`),否则内容过长会溢出。
- 点击导航项后**必须调用 `Navigator.pop(context)`** 关闭抽屉,否则抽屉不会自动关闭。
- `Scaffold.of(context).openDrawer()` 在 `AppBar` 的 `leading` 中调用时,需用 `Builder` 包裹以获取正确的 `context`(避免 `Scaffold` 还未构建完成)。
- `drawerEdgeDragWidth` 默认为全宽,可能导致水平 `ListView` 滑动冲突;**显式设置为边缘 32-48px** 可解决。
- M3 推荐使用 `NavigationDrawer` + `NavigationDrawerDestination`(声明式 API),而非命令式的 `Drawer` + `ListTile`;两者可同时存在,但同一 `Scaffold` 不应同时使用。
- `UserAccountsDrawerHeader` 已较老,优先使用自定义 `DrawerHeader` 或 `Container` 实现用户信息头部。
- iOS 风格不推荐使用 `Drawer`;iOS HIG 推荐使用 `CupertinoTabScaffold` + 底部 Tab,或 `CupertinoPageScaffold` + 自定义滑出。
- `endDrawer` 在 RTL 布局下会自动镜像到左侧;若需固定方向,使用 `Directionality` 包裹。
