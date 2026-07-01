# i18n API(国际化)

> 本文件列出国际化相关 API:`<el-config-provider>` 属性与语言包结构。用法见 [component.md](./component.md)。

## el-config-provider 属性(Props)

| 属性名           | 类型                                      | 默认值    | 说明                                |
| ---------------- | ----------------------------------------- | --------- | ----------------------------------- |
| `locale`         | `Language`                                | 中文(zh) | 语言包,来自 `@element-plus/locale` |
| `size`           | `'large' \| 'default' \| 'small'`         | `'default'` | 全局组件尺寸                     |
| `z-index`        | `number`                                  | `2000`    | 全局起始 z-index                    |
| `namespace`      | `string`                                  | `'el'`    | CSS 类名前缀                        |
| `button`         | `{ autoInsertSpace?: boolean }`           | —         | Button 全局配置                     |
| `message`        | `{ max?: number }`                        | —         | Message 全局配置                    |
| `experimental-features` | `object`                           | —         | 实验特性开关                        |
| `empty-values`   | `unknown[]`                               | —         | 视为空的值列表(2.7+)              |
| `value-on-clear`| `unknown`                                 | —         | 清空时的回填值                       |

## el-config-provider 事件 / 方法 / 插槽

- 无对外事件、无方法。
- 插槽:`default`(被包裹的子树)。

## 语言包结构(Language)

语言包是一个对象,按组件分组翻译文案。关键字段:

| 字段           | 归属组件                         |
| -------------- | -------------------------------- |
| `el.pagination`| 分页(`prev`/`next`/`total` 等)|
| `el.datepicker`| 日期选择器(月份/星期/按钮)    |
| `el.select`    | Select(loading/placeholder)    |
| `el.cascader`  | 级联选择器                       |
| `el.table`     | 表格(空数据/筛选)             |
| `el.popconfirm`| 气泡确认框                       |
| `el.upload`    | 上传(提示文案)               |

## 语言包引入方式

```js
// ESM
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'
import ja from 'element-plus/es/locale/lang/ja'

// 全局注册(app 入口)
// app.use(ElementPlus, { locale: zhCn })
```

## 自定义语言包

可对官方语言包做局部覆盖:

```js
import en from 'element-plus/es/locale/lang/en'
const customEn = {
  ...en,
  el: {
    ...en.el,
    pagination: { ...en.el.pagination, total: 'Total {total}' },
  },
}
```

> 完整语言包列表见 https://element-plus.org/zh-CN/guide/i18n.html
