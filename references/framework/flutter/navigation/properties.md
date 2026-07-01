# Flutter Navigation 属性列表与默认值

本文档汇总 `Navigator` / `MaterialPageRoute` / `GoRouter` 的属性、方法与回调。颜色/尺寸默认值以 design token 形式给出。

## Navigator 静态方法

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `push` | `Future<T?> push<T>(BuildContext, Route<T>)` | 压入新路由 |
| `pushNamed` | `Future<T?> pushNamed<T>(BuildContext, String, {Object? arguments})` | 命名路由压入 |
| `pushReplacement` | `Future<T?> pushReplacement<T, TO>(BuildContext, Route<T>, {TO? result})` | 替换栈顶 |
| `pushReplacementNamed` | `Future<T?> pushReplacementNamed<T, TO>(BuildContext, String, {Object? arguments, TO? result})` | 命名替换 |
| `pop` | `void pop<T>(BuildContext, [T? result])` | 弹出栈顶(可带结果) |
| `popAndPushNamed` | `Future<T?> popAndPushNamed<T, TO>(BuildContext, String, {Object? arguments, TO? result})` | 弹出后压入命名 |
| `popUntil` | `void popUntil(BuildContext, RoutePredicate)` | 弹出直到谓词为真 |
| `pushAndRemoveUntil` | `Future<T?> pushAndRemoveUntil<T>(BuildContext, Route<T>, RoutePredicate)` | 压入并清理栈 |
| `pushNamedAndRemoveUntil` | `Future<T?> pushNamedAndRemoveUntil<T>(BuildContext, String, RoutePredicate, {Object? arguments})` | 命名压入并清理 |
| `removeRoute` | `void removeRoute(BuildContext, Route)` | 移除指定路由 |
| `removeRouteBelow` | `void removeRouteBelow(BuildContext, Route)` | 移除指定路由下方路由 |
| `replace` | `void replace<T>(BuildContext, {Route oldRoute, Route newRoute})` | 替换指定路由 |
| `replaceRouteBelow` | `void replaceRouteBelow<T>(BuildContext, {Route anchorRoute, Route newRoute})` | 替换锚点下方 |
| `canPop` | `bool canPop(BuildContext)` | 是否可返回 |
| `maybePop` | `Future<bool> maybePop<T>(BuildContext, [T? result])` | 可返回时返回 |
| `restorablePush` | `String restorablePush(BuildContext, RestorableRouteBuilder<T>, {Object? arguments})` | 可恢复压入 |

## NavigatorState 实例方法(通过 `Navigator.of(context)`)

| 方法 | 说明 |
| --- | --- |
| `push(route)` | 压入路由 |
| `pop([result])` | 弹出栈顶 |
| `pushNamed(name, {arguments})` | 命名压入 |
| `popUntil(predicate)` | 弹出直到条件 |
| `canPop()` | 是否可返回 |
| `maybePop([result])` | 可返回时返回 |

## MaterialPageRoute 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `builder` | `WidgetBuilder` | 必填 | 页面构建函数 |
| `settings` | `RouteSettings` | `RouteSettings()` | 路由名 + 参数 |
| `maintainState` | `bool` | `true` | 是否在栈中保持状态 |
| `fullscreenDialog` | `bool` | `false` | 全屏模态(从底部滑入) |
| `allowSnapshotting` | `bool` | `true` | 是否允许快照 |

## RouteSettings 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `name` | `String?` | `null` | 路由名 |
| `arguments` | `Object?` | `null` | 传递参数 |

## GoRouter 配置属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `routes` | `List<RouteBase>` | 必填 | 路由表 |
| `initialLocation` | `String` | `'/'` | 初始位置 |
| `redirect` | `GoRouterRedirect?` | `null` | 全局重定向(鉴权) |
| `refreshListenable` | `Listenable?` | `null` | 监听刷新(登录态变化) |
| `errorBuilder` | `GoRouterWidgetBuilder?` | `null` | 错误页构建 |
| `navigatorKey` | `GlobalKey<NavigatorState>?` | `null` | 根 navigator key |
| `debugLogDiagnostics` | `bool` | `false` | 调试日志 |

## GoRoute 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `path` | `String` | 必填 | 路径(如 '/user/:id') |
| `name` | `String?` | `null` | 路由名(可命名跳转) |
| `builder` | `GoRouterWidgetBuilder?` | `null` | 页面构建 |
| `pageBuilder` | `GoRouterPageBuilder?` | `null` | 自定义转场(Page) |
| `redirect` | `GoRouterRedirect?` | `null` | 局部重定向 |
| `routes` | `List<RouteBase>` | `const []` | 嵌套子路由 |

## 完整示例

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class NavigationFullSample extends StatelessWidget {
  const NavigationFullSample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Navigation 完整示例')),
      body: ListView(
        padding: const EdgeInsets.all({spacing-md}),
        children: [
          // 1. 命名路由 + 传参
          ElevatedButton(
            child: const Text('命名路由(带参)'),
            onPressed: () => Navigator.pushNamed(
              context, '/detail', arguments: {'id': 42},
            ),
          ),
          // 2. 直接构造 Route
          ElevatedButton(
            child: const Text('直接构造 Route'),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const DetailPage(id: 1),
                  fullscreenDialog: true, // 从底部滑入
                  settings: const RouteSettings(name: '/detail'),
                ),
              );
            },
          ),
          // 3. 返回到指定页面(popUntil)
          ElevatedButton(
            child: const Text('返回到首页'),
            onPressed: () => Navigator.popUntil(
              context, (route) => route.isFirst,
            ),
          ),
          // 4. GoRouter 声明式跳转
          ElevatedButton(
            child: const Text('GoRouter 跳转'),
            onPressed: () => context.go('/user/123'),
          ),
          // 5. GoRouter push
          ElevatedButton(
            child: const Text('GoRouter push'),
            onPressed: () => context.push('/user/456'),
          ),
        ],
      ),
    );
  }
}

class DetailPage extends StatelessWidget {
  final int id;
  const DetailPage({super.key, required this.id});

  @override
  Widget build(BuildContext context) {
    // 命名路由取参数
    final args = ModalRoute.of(context)?.settings.arguments;
    return Scaffold(
      appBar: AppBar(title: Text('详情 #$id')),
      body: Center(child: Text('参数: $args')),
    );
  }
}

// GoRouter 配置
final _router = GoRouter(
  initialLocation: '/',
  redirect: (context, state) {
    // 鉴权:未登录跳登录页
    final loggedIn = false; // 替换为实际登录态
    if (!loggedIn && state.matchedLocation != '/login') return '/login';
    return null;
  },
  routes: [
    GoRoute(path: '/', builder: (_, __) => const NavigationFullSample()),
    GoRoute(
      path: '/user/:id',
      builder: (_, state) =>
          DetailPage(id: int.parse(state.pathParameters['id']!)),
    ),
    GoRoute(path: '/login', builder: (_, __) => const Scaffold(body: Center(child: Text('登录')))),
  ],
);
```

## 注意事项

- `Navigator.pop` 传给上一个页面的返回值通过 `push` 返回的 `Future` 获取
- `popUntil` 的谓词 `(route) => route.isFirst` 用于返回栈底;`(route) => route.settings.name == '/home'` 按名匹配
- `fullscreenDialog: true` 让页面从底部滑入(适用于创建/编辑场景)
- iOS 上 `CupertinoPageRoute` 提供原生平移转场(支持左滑返回),iOS 项目建议用 Cupertino 路由
- Web 平台 `Navigator.push` 不会更新浏览器 URL;需要 URL 同步请用 `go_router`
- 嵌套 `Navigator` 用于分栈管理(如底部 Tab 各自独立栈)
- 深链与 Universal Links 配置见 cookbook 链接
