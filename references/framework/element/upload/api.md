# Upload API

> `<el-upload>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-upload 属性(Props)

| 属性名            | 类型                                        | 默认值              | 说明                                  |
| ----------------- | ------------------------------------------- | ------------------- | ------------------------------------- |
| `action`          | `string`                                    | 必填(或用 http-request) | 上传地址                       |
| `headers`         | `Record<string, any>`                       | —                   | 请求头(如鉴权 token)              |
| `multiple`        | `boolean`                                   | `false`             | 是否多选                              |
| `data`            | `Record<string, any>`                       | —                   | 附带的额外表单字段                    |
| `name`            | `string`                                    | `'file'`            | 文件字段名                            |
| `with-credentials`| `boolean`                                   | `false`             | 是否携带 cookie                       |
| `show-file-list`  | `boolean`                                   | `true`              | 是否显示文件列表                      |
| `drag`            | `boolean`                                   | `false`             | 是否启用拖拽(或用 el-upload-dragger) |
| `accept`          | `string`                                    | —                   | 接受的文件类型(MIME)               |
| `list-type`       | `'text' \| 'picture' \| 'picture-card'`     | `'text'`            | 列表形态                              |
| `auto-upload`     | `boolean`                                   | `true`              | 选文件后是否立即上传                  |
| `limit`           | `number`                                    | —                   | 最大允许上传数                        |
| `file-list` / `v-model:file-list` | `UploadUserFile[]`          | —                   | 文件列表(受控)                     |
| `disabled`        | `boolean`                                   | `false`             | 是否禁用                              |
| `http-request`    | `(options) => void`                         | —                   | 自定义上传实现(直传 OSS 等)        |

## UploadFile 关键字段

| 字段       | 类型                | 说明                                      |
| ---------- | ------------------- | ----------------------------------------- |
| `name`     | `string`            | 文件名                                    |
| `url`      | `string`            | 文件地址(已上传/本地预览)              |
| `status`   | `'ready' \| 'uploading' \| 'success' \| 'fail'` | 四态状态 |
| `percentage` | `number`          | 上传进度(0-100,uploading 时)          |
| `uid`      | `number`            | 唯一标识                                  |

## 事件(Events)

| 事件名        | 回调签名                                        | 说明                       |
| ------------- | ----------------------------------------------- | -------------------------- |
| `change`      | `(uploadFile, uploadFiles) => void`             | 任一状态变化               |
| `success`     | `(response, uploadFile, uploadFiles) => void`   | 单个上传成功               |
| `error`       | `(error, uploadFile, uploadFiles) => void`      | 上传失败(保留重试)      |
| `progress`    | `(evt, uploadFile, uploadFiles) => void`        | 进度变化                   |
| `exceed`      | `(files, uploadFiles) => void`                  | 超出 limit                 |
| `before-upload` | `(rawFile) => void \| Promise \| boolean`     | 上传前校验,返回 false 中止 |
| `before-remove` / `remove` | `(uploadFile, uploadFiles) => ...` | 移除前/移除                |
| `preview`     | `(uploadFile) => void`                          | 点击列表预览               |

## 方法 / 插槽

- `submit()` / `clearFiles()` / `abort()` / `handleStart()`:`ref` 实例方法(`auto-upload: false` 时手动 `submit()`)。
- 插槽:`default`(触发器)、`trigger`(与 default 区分)、`tip`(提示文案)、`file`(自定义列表项)、`append`。

## 关键规格要点

- **四态**:ready / uploading(percentage 进度)/ success / fail(fail 项保留"重新上传"入口)。
- **校验链路**:数量用 `limit` + `on-exceed`;类型/大小用 `before-upload` 拦截并给出明确错误提示(防错原则)。
- **无障碍**:触发器为原生 button 语义;文件列表项提供移除按钮的 `aria-label`;进度变化建议 `aria-live="polite"` 播报关键节点(成功/失败)。
- **尺寸**:picture-card 默认 148 × 148;头像上传参考 72 × 72 + `{radius-full}`。
