# 画廊模式命名词汇

> 模式词汇库。图片 / 媒体集合的展示模式。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `gallery-grid`        | 等比方格(N × M)                                | 摄影集、作品集、商品图墙              |
| `gallery-masonry`     | 瀑布流(列高不齐)                                | Pinterest 类、图片社区                |
| `gallery-carousel`    | 轮播(自动 + 手动)                               | 商品详情图、首页 banner、推荐位       |
| `gallery-slider`      | 单图滑块(无缩略图)                              | Hero、案例展示                        |
| `gallery-lightbox`    | 点击放大全屏查看                                  | 摄影集、商品详情                      |
| `gallery-thumbnail`   | 缩略图列 + 主图切换                               | 商品详情、作品集详情                  |
| `gallery-filmstrip`   | 横向滚动胶片条                                    | 影视集、视频缩略图、媒体库            |
| `gallery-justified`   | 行高一致,图宽自适应(Justified Gallery)         | 婚礼摄影、旅行图集                    |
| `gallery-mosaic`      | 拼贴(大小图组合)                                | 案例展示、IP 展示                     |
| `gallery-split`       | 主图 + 列表(可切换)                             | 商品详情、相册管理                    |
| `gallery-coverflow` | 封面流:居中卡正视,两侧按离心距离后仰变暗,切换整排转动 | 专辑/媒体封面选择 |
| `gallery-css3d-film-ring` | 零依赖 CSS 3D 胶片环:环形排布可拖转,点选单格抬起 | 品牌展示、怀旧媒体墙(与 `gallery-filmstrip` 互见:彼条平面横向胶片条,本条 3D 环) |
| `gallery-carousel-magnet` | 轮播磁吸:停正中吸附,中央放大、两侧缩小变暗 | 商品/内容轮播(与 [scroll.md](scroll.md) `scroll-center-focus` 互见:彼条通用中心聚焦原理,本条轮播磁吸落位) |
| `gallery-carousel-peek-snap` | 露角吸附轮播:横滑露邻卡一角提示可滑,松手自动对齐完整卡片(吸附+统一间距) | 移动端卡片轮播(吸附机制见 [scroll.md](scroll.md) `scroll-snap`) |
| `gallery-intro-drop-fan` | 开场三段:照片逐张落下堆叠→数张收拢成扇形→标题面板升起 | 相册/摄影集开场 |
| `gallery-shared-element-expand` | 原位放大共享元素:缩略图/列表图从原位同比放大成详情,文字随后进入,返回收回原位,焦点不跳;撕口票根是变体细节 | 图库/商品图→详情(与 [cards.md](cards.md) `shared-element-card-transition` 互见:彼条卡片容器转场机制,本条图片原位放大家族;与 `gallery-lightbox` 互见:彼条全屏跳切,本条连续过渡) |
| `gallery-reflow-filter` | 图片主角网格留白:点分类平滑退出自动重排,关闭详情归原位 | 摄影/作品集分类浏览 |
| `gallery-whitespace-showcase` | 大留白横向摄影:切作品主图说明同步过渡,滑杆实时调明暗 | 摄影作品展示页 |
| `gallery-fan-stair-scroll` | 扇形转台阶:彩色扇形卡片抓视线,滚动后变台阶式排列,按钮驱动依次换位 | 营销/活动页(与 [cards.md](cards.md) `card-fan-stack-swipe` 互见:彼条滑动换组,本条滚动/按钮改排列) |

## 使用规则

- 商品详情优先用 `gallery-thumbnail`(主图 + 缩略图列),不用 `gallery-carousel`
- 图片社区优先 `gallery-masonry` 或 `gallery-justified`(保留原图比例)
- 所有图片必须设 `width` + `height` 或 `aspect-ratio`(见 [`performance.md`](../meta/performance.md) CLS)
- 触发 [`ai-tells.md`](../meta/ai-tells.md) Unsplash random 占位时,改固定 ID
- `gallery-lightbox` 必须有键盘 ESC 关闭 + 左右键切换
- 单页画廊模式 1 种(避免混乱)
- 分页圆点只表扁平有序页(不表层级);≤10 个,再多难以一瞥计数(改网格/缩略图索引);自定义指示图 ≤2 种
- **页码指示三型判据**:数量少用圆点;数量多用"当前/总数"数字型(圆点数不清就别硬数);用户无需感知总数时仅用切换箭头

## 在 draw-md 中的写法

```markdown
## Gallery (product-images)
- pattern: gallery-thumbnail
- main: { image: product-1.jpg, ratio: 1:1, alt: "商品正面图" }
- thumbnails: [{ image: product-1.jpg }, { image: product-2.jpg }, { image: product-3.jpg }]
- lightbox: { enabled: true, keyboard: true }
- loading: lazy (non-first)
```
