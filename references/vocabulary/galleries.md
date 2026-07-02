# 画廊模式命名词汇

> 模式词汇库。图片 / 媒体集合的展示模式。来源:taste-skill。

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

## 使用规则

- 商品详情优先用 `gallery-thumbnail`(主图 + 缩略图列),不用 `gallery-carousel`
- 图片社区优先 `gallery-masonry` 或 `gallery-justified`(保留原图比例)
- 所有图片必须设 `width` + `height` 或 `aspect-ratio`(见 [`performance.md`](../meta/performance.md) CLS)
- 触发 [`ai-tells.md`](../meta/ai-tells.md) Unsplash random 占位时,改固定 ID
- `gallery-lightbox` 必须有键盘 ESC 关闭 + 左右键切换
- 单页画廊模式 1 种(避免混乱)

## 在 draw-md 中的写法

```markdown
## Gallery (product-images)
- pattern: gallery-thumbnail
- main: { image: product-1.jpg, ratio: 1:1, alt: "商品正面图" }
- thumbnails: [{ image: product-1.jpg }, { image: product-2.jpg }, { image: product-3.jpg }]
- lightbox: { enabled: true, keyboard: true }
- loading: lazy (non-first)
```
