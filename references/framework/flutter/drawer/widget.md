# Flutter Drawer Widget 定义

## Widget 定义

Flutter 通过 `Drawer`(StatelessWidget)实现侧边抽屉,常用于导航菜单。`Drawer` 通常通过 `Scaffold.drawer` / `Scaffold.endDrawer` 属性挂载,由 `Scaffold` 自动管理打开/关闭与手势支持(MD3 风格从屏幕左侧滑入)。

| Drawer 类型 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| 标准抽屉 | `Drawer` | `StatelessWidget` | 侧边导航抽屉(M3) |
| 抽屉项 | `DrawerHeader` / `UserAccountsDrawerHeader` | `StatelessWidget` | 抽屉头部(标题/用户信息) |
| 导航项 | `ListTile` / `NavigationListTile` | `StatelessWidget` | 抽屉导航项 |
| 控制器 | `ScaffoldState` | `StatefulWidget` | 通过 `openDrawer()` / `openEndDrawer()` 控制 |
| Cupertino 抽屉 | `CupertinoPageScaffold` + 自定义 | - | iOS 风格(无原生 Drawer) |

> `Scaffold` 同时支持 `drawer`(左侧)与 `endDrawer`(右侧,常用于 RTL 或筛选抽屉)。

## 构造函数

### Drawer

```dart
const Drawer({
  Key? key,
  double? width,
  Widget? child,
  String? semanticLabel,
  DrawerCallback? onDrawerChanged,
  ShapeBorder? shape,
  double? elevation,
  Color? backgroundColor,
  Color? shadowColor,
  Color? surfaceTintColor,
  Clip? clipBehavior,
})
```

### DrawerHeader

```dart
const DrawerHeader({
  Key? key,
  Widget? child,
  EdgeInsetsGeometry? margin = const EdgeInsets.only(bottom: 8.0),
  EdgeInsetsGeometry? padding = const EdgeInsets.fromLTRB(16.0, 16.0, 16.0, 8.0),
  Decoration? decoration,
  Duration duration = const Duration(milliseconds: 250),
  Curve curve = Curves.fastOutSlowIn,
})
```

### UserAccountsDrawerHeader

```dart
const UserAccountsDrawerHeader({
  Key? key,
  Widget? currentAccountAccount,
  Widget? otherAccountsPictures,
  required Widget currentAccountPicture,
  required Widget accountName,
  required Widget accountEmail,
  VoidCallback? onDetailsPressed,
  Color? decoration,
  Color? arrowColor,
})
```

> 属性与方法明细以 [properties.md](properties.md) 为唯一维护处；本文件只讲定义、构造与示例。

## 最小示例

```dart
import 'package:flutter/material.dart';

/// Drawer 最小示例:标准导航抽屉
class DrawerSample extends StatelessWidget {
  const DrawerSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Drawer 示例')),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            // 1. 抽屉头部
            const DrawerHeader(
              decoration: BoxDecoration(color: {color-primary}),
              child: Text(
                '导航菜单',
                style: TextStyle(color: {color-on-primary}, fontSize: {font-size-lg}),
              ),
            ),
            // 2. 导航项
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('首页'),
              onTap: () {
                Navigator.pop(context); // 关闭抽屉
              },
            ),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('设置'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.info),
              title: const Text('关于'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
          ],
        ),
      ),
      body: const Center(child: Text('主内容区')),
    );
  }
}
```

## 自定义样式(MD3 主题映射)

```dart
Drawer(
  width: {size-drawer},  // M3 推荐 304
  backgroundColor: {color-surface},
  elevation: {elevation-md},
  shadowColor: {color-shadow},
  surfaceTintColor: {color-primary},
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.horizontal(
      right: Radius.circular({radius-lg}),
    ),
  ),
  child: ListView(
    padding: EdgeInsets.zero,
    children: [
      // 用户信息头部
      UserAccountsDrawerHeader(
        accountName: const Text('张三'),
        accountEmail: const Text('zhangsan@example.com'),
        currentAccountPicture: const CircleAvatar(
          backgroundColor: {color-on-primary},
          child: Text('张'),
        ),
        decoration: BoxDecoration(color: {color-primary}),
      ),
      // 导航项(选中态高亮)
      ListTile(
        leading: const Icon(Icons.inbox),
        title: const Text('收件箱'),
        trailing: const Badge(label: Text('3')),
        selected: true,
        selectedTileColor: {color-primary-container},
        onTap: () {},
      ),
      ListTile(
        leading: const Icon(Icons.send),
        title: const Text('已发送'),
        onTap: () {},
      ),
    ],
  ),
)
```

> 注:示例中的 `{color-primary}`、`{size-drawer}` 等为 design token 占位符,实际运行时由主题层解析。详见 `properties.md`。

## 参考链接

- Flutter 官方文档 - 在页面上添加抽屉: https://docs.flutter.cn/cookbook/design/drawer
- Widget 目录 - Material components: https://docs.flutter.cn/ui/widgets/material
- API 参考 - Drawer: https://api.flutter.dev/flutter/material/Drawer-class.html
- API 参考 - DrawerHeader: https://api.flutter.dev/flutter/material/DrawerHeader-class.html
- API 参考 - UserAccountsDrawerHeader: https://api.flutter.dev/flutter/material/UserAccountsDrawerHeader-class.html
- API 参考 - Scaffold.drawer: https://api.flutter.dev/flutter/material/Scaffold/drawer.html
