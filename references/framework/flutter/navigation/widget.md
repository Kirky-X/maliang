# Flutter Navigation Widget 定义

## Widget 定义

Flutter 导航基于"路由栈"模型:`Navigator` 维护一个 `Route` 列表,`push` 压栈进入新页面,`pop` 出栈返回。`MaterialPageRoute` 提供 Material 风格的页面切换动画。复杂场景(深链/嵌套/Web URL)使用社区包 `go_router` 或官方 `package:go_router`。

| Widget/类 | 类 | 基类 | 用途 |
| --- | --- | --- | --- |
| `Navigator` | `Navigator` | `StatefulWidget` | 路由栈管理 |
| `Route` | `Route<T>` | - | 抽象路由(页面 + 转场) |
| `MaterialPageRoute` | `MaterialPageRoute<T>` | `PageRoute<T>` | Material 转场路由 |
| `CupertinoPageRoute` | `CupertinoPageRoute<T>` | `PageRoute<T>` | iOS 风格转场路由 |
| `NavigatorState` | `NavigatorState` | `State<Navigator>` | 状态访问(push/pop) |
| `GoRouter` | `GoRouter` | - | 声明式路由(社区包,官方维护) |
| `Router` | `Router` | `StatefulWidget` | 底层 Router 2.0 |

## 构造函数

### MaterialApp(命名路由配置)

```dart
MaterialApp(
  String title,
  ThemeMode themeMode,
  // 命名路由
  Map<String, WidgetBuilder> routes = const <String, WidgetBuilder>{},
  String? initialRoute,
  RouteFactory? onGenerateRoute,      // 动态路由生成
  RouteFactory? onUnknownRoute,       // 未知路由(404)
  GlobalKey<NavigatorState>? navigatorKey,
  ...
)
```

### Navigator.push / pushNamed

```dart
// 命名路由
Navigator.pushNamed(BuildContext context, String routeName, {Object? arguments})

// 直接构造 Route
Navigator.push<T extends Object?>(BuildContext context, Route<T> route)
```

### MaterialPageRoute

```dart
MaterialPageRoute<T>({
  required WidgetBuilder builder,
  RouteSettings? settings,        // name + arguments
  bool maintainState = true,
  bool fullscreenDialog = false,  // 全屏模态(从底部滑入)
})
```

### GoRouter(社区包)

```dart
GoRouter({
  required List<GoRoute> routes,      // 路由表
  String initialLocation = '/',
  GoRouterRedirect? redirect,         // 重定向(鉴权)
  Listenable? refreshListenable,
  ...
})

GoRoute({
  required String path,
  Widget Function(BuildContext, GoRouterState)? builder,
  List<GoRoute> routes = const [],    // 嵌套子路由
  ...
})
```

## 核心属性

### Navigator 常用方法

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `push` | `Future<T?> push<T>(Route<T>)` | 压栈,返回携带数据的 Future |
| `pop` | `void pop<T>([T? result])` | 出栈,可携带结果返回 |
| `pushNamed` | `Future<T?> pushNamed<T>(String, {Object? args})` | 命名路由压栈 |
| `pushReplacement` | `void pushReplacement<T, TO>(Route<T>, {TO? result})` | 替换栈顶 |
| `pushReplacementNamed` | 同上,命名版本 | 替换栈顶 |
| `popUntil` | `void popUntil(RoutePredicate)` | 持续出栈直到条件满足 |
| `pushAndRemoveUntil` | `Future<T?> pushAndRemoveUntil<T>(Route, RoutePredicate)` | 压栈并清栈 |
| `canPop` | `bool canPop()` | 是否可返回 |
| `maybePop` | `Future<bool> maybePop<T>([T? result])` | 可返回时返回 |
| `restorablePush` | `String restorablePush(...)` | 可恢复 push(状态恢复) |

### Route 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `settings` | `RouteSettings` | 名称 + 参数 |
| `isFirst` | `bool` | 是否栈底 |
| `isCurrent` | `bool` | 是否栈顶 |
| `willHandlePopInternally` | `bool` | 是否自行处理返回 |
| `canPop` | `bool` | 是否可 pop |

## 最小示例

```dart
import 'package:flutter/material.dart';

class NavigationSample extends StatelessWidget {
  const NavigationSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Navigation 示例')),
      body: Center(
        child: ElevatedButton(
          child: const Text('跳转到第二页'),
          onPressed: () async {
            // 命名路由跳转
            final result = await Navigator.pushNamed(context, '/second',
                arguments: '来自首页的数据');
            debugPrint('返回结果: $result');
          },
        ),
      ),
    );
  }
}

class SecondPage extends StatelessWidget {
  const SecondPage({super.key});

  @override
  Widget build(BuildContext context) {
    final args = ModalRoute.of(context)!.settings.arguments as String;
    return Scaffold(
      appBar: AppBar(title: const Text('第二页')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('收到: $args'),
            ElevatedButton(
              child: const Text('返回'),
              onPressed: () => Navigator.pop(context, '返回结果'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 命名路由配置

```dart
MaterialApp(
  initialRoute: '/',
  routes: {
    '/': (context) => const NavigationSample(),
    '/second': (context) => const SecondPage(),
  },
  // 动态路由:处理带参数的命名路由
  onGenerateRoute: (settings) {
    if (settings.name == '/detail') {
      final id = settings.arguments as int;
      return MaterialPageRoute(builder: (_) => DetailPage(id: id));
    }
    return null;
  },
)
```

## 参考链接

- Flutter 官方文档 - 导航 & 路由: https://docs.flutter.cn/ui/navigation
- Cookbook - 导航至新页面并返回: https://docs.flutter.cn/cookbook/navigation/navigation-basics
- Cookbook - 传递数据到新页面: https://docs.flutter.cn/cookbook/navigation/passing-data
- Cookbook - 从新页面返回数据: https://docs.flutter.cn/cookbook/navigation/returning-data
- Cookbook - 设置 Android App Links: https://docs.flutter.cn/cookbook/navigation/set-up-app-links
- Cookbook - 设置 iOS Universal Links: https://docs.flutter.cn/cookbook/navigation/set-up-universal-links
- Flutter 官方文档 - URL 策略(Web): https://docs.flutter.cn/ui/navigation/url-strategies
- API 参考 - Navigator: https://api.flutter.dev/flutter/widgets/Navigator-class.html
- API 参考 - MaterialPageRoute: https://api.flutter.dev/flutter/material/MaterialPageRoute-class.html
- pub.dev - go_router: https://pub.flutter-io.cn/packages/go_router
