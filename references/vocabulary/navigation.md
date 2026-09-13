# 导航模式命名词汇

> 模式词汇库。draw-md 阶段描述导航结构时使用的标准化命名。来源:taste-skill。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `nav-top-bar`         | 顶部水平导航栏,logo 左 + 菜单项右                | Web 默认,大多数站点                  |
| `nav-sidebar`         | 左侧垂直导航,常配折叠 / 面包屑                   | SaaS Dashboard、文档站、DevTool       |
| `nav-bottom-tab`      | 底部 tab 栏(移动端),≤ 5 项                     | 移动 App 主导航                       |
| `nav-dock`            | 浮动 dock(类 macOS),底部居中                   | 移动 App 辅助导航、PWA                |
| `nav-hamburger`       | 隐藏在 hamburger 菜单内                          | 移动端、二级导航                      |
| `nav-mega-menu`       | 顶部悬停展开大菜单(多列)                       | 电商、企业站(信息架构深)            |
| `nav-breadcrumb`      | 面包屑路径                                        | 多层级页面(详情 / 设置 / 后台)      |
| `nav-command-palette` | ⌘K 命令面板                                       | DevTool、SaaS、生产力工具             |
| `nav-floating-pill`   | 浮动药丸式导航,滚动时显隐                        | 长滚动页(单页营销 / 品牌站)         |
| `nav-stepper`         | 步进式导航(1/2/3)                                | 流程页(结账、注册、向导)            |
| `nav-floating-island` | 浮岛导航:悬浮胶囊 + 汉堡→X 形变 + 蒙版错峰揭示   | 品牌 / 创意站;移动端降级为全宽 dock(来源:taste-skill soft-skill §5.A) |
| `nav-fab`             | 悬浮操作按钮:右下角单 FAB(一屏仅一个主操作),滚动下滑出现 / 上滑收起联动,避开底部导航安全区 | 移动 App 新建/发布/写等一级操作入口                |

> 来源注:`nav-fab` 为**审计补全**(2026-09-08 组件覆盖审计):对照 Material 3 FAB(含 Extended FAB)、Ant Design FloatButton、Flutter FloatingActionButton 组件清单。

## 使用规则

- 同一站点导航模式 ≤ 2 种组合(如 `nav-top-bar` + `nav-bottom-tab` 跨端)
- 主要功能 1 tap 可达(Navigation HIGH 优先级,见 [`rules-priority.md`](../meta/rules-priority.md))
- 移动端导航项 ≤ 5 个(米勒定律,见 [`principles.md`](../meta/principles.md))
- 触发 hamburger 时,主功能不可埋深处(≤ 2 级)
- 命令面板 ⌘K 与 `nav-top-bar` 共存,不替代主导航

## 在 draw-md 中的写法

```markdown
## Navigation
- primary: nav-top-bar
- items: [Home, Products, Pricing, Docs, Login]
- mobile: nav-bottom-tab
- mobile_items: [Home, Search, Cart, Profile]
- secondary: nav-command-palette (⌘K)
```
