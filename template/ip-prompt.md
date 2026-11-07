# IP 形象 prompt 契约(8 维度,缺一不可)

> 填法、流程与 fallback 规则 canonical 见 [`../references/commands/ip.md`](../references/commands/ip.md);本文件是 8 维度契约与填写形态的唯一 canonical,每份 IP 形象生成请求逐字段对照,缺失任一维度即不合规,补全后再调用 API。

| 维度        | 字段 key        | 说明                                                | 示例                                    |
| ----------- | --------------- | --------------------------------------------------- | --------------------------------------- |
| 主体描述    | `subject`       | IP 形象的主体(物种/拟人化程度/性别/年龄段)         | 一只拟人化的橘猫,圆脸大眼,年龄 6-8 岁   |
| 风格        | `style`         | 与 DESIGN.md 调性一致(扁平/拟物/3D/极简/手绘)      | 极简扁平化,圆润线条,柔和过渡            |
| 构图        | `composition`   | 视角(正面/侧面/3/4 视角)+ 景别(胸像/全身)         | 3/4 视角,全身构图,居中                  |
| 光线        | `lighting`      | 光线类型(柔和/锐利/逆光/侧光)+ 方向               | 柔和顶光,轻微逆光勾勒轮廓               |
| 色彩        | `palette`       | 主色 HEX + 辅助色 HEX(必来自 DESIGN.md)            | 主色 #007DFF / 辅助色 #FFAA00            |
| 背景/交付形态 | `background`  | `scene`(背景烘进画面)或 `isolated`(单主体透明底 PNG,可直接叠放) | isolated:单主体置于完全透明背景 |
| 比例        | `aspect_ratio`  | 固定 `3:4`(对应 API 参数 `image_size=portrait_4_3`)| 3:4                                     |
| 负向提示词  | `negative`      | 需避免的元素(多余手指/文字水印/模糊/低质)         | 多余手指,文字水印,模糊,低分辨率,变形    |

- `palette` 字段的色值 **MUST 来自 DESIGN.md frontmatter 的 colors**,禁止凭空生成。
- `background` 默认 `isolated`——"放到我的网站/贴纸/叠加"类用途都是 cutout;只有明确要重新生成构图与氛围(hero 图/整幅插画)才用 `scene`。
- `aspect_ratio` 固定为 `3:4`,与 API 参数 `image_size=portrait_4_3` 严格对齐。
- 8 维度缺失任一即视为不合规 prompt,需补全后再调用 API。

## 填写形态(逐字段填充即得合规 prompt)

```text
subject: <物种/拟人化程度/性别/年龄段>
style: <与 DESIGN.md 调性一致:扁平/拟物/3D/极简/手绘 + 线条与过渡特征>
composition: <视角(正面/侧面/3/4)+ 景别(胸像/全身)+ 主体位置>
lighting: <光线类型(柔和/锐利/逆光/侧光)+ 方向;isolated 时只留中性主光>
palette: <主色 HEX / 辅助色 HEX——必来自 DESIGN.md colors>
background: <isolated(默认,单主体透明底) | scene(背景烘进画面)>
aspect_ratio: 3:4
negative: <多余手指, 文字水印, 模糊, 低分辨率, 变形, ...>
```
