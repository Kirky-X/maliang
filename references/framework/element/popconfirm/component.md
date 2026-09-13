# Popconfirm 气泡确认框

> Element Plus 气泡确认组件 `<el-popconfirm>`,点击触发二次确认(确认/取消双按钮),用于删除、注销、退款等破坏性操作的轻量确认。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-popconfirm>
```

`title` 为确认问题;`confirm-button-text` / `cancel-button-text` 自定义按钮文案;`confirm-button-type` 表达危险色;`#reference` 插槽放触发元素。

## 基本用法

```vue
<template>
  <el-popconfirm
    title="确认删除该地址?"
    confirm-button-text="删除"
    cancel-button-text="取消"
    confirm-button-type="danger"
    @confirm="onDelete"
    @cancel="onCancel"
  >
    <template #reference>
      <el-button type="danger" plain>删除</el-button>
    </template>
  </el-popconfirm>
</template>

<script setup>
import { ElMessage } from 'element-plus'
const onDelete = () => ElMessage.success('已删除')
const onCancel = () => {}
</script>
```

## 使用场景

### 场景 1:表格行删除(危险色 + 明确宾语)

```vue
<template>
  <el-popconfirm
    :title="`确认删除\"${row.name}\"?`"
    confirm-button-text="删除"
    cancel-button-text="取消"
    confirm-button-type="danger"
    confirm-button-icon="Delete"
    width="220"
    @confirm="del(row.id)"
  >
    <template #reference>
      <el-button link type="danger">删除</el-button>
    </template>
  </el-popconfirm>
</template>

<script setup>
import { ElMessage } from 'element-plus'
const del = (id) => ElMessage.success(`已删除 ${id}`)
</script>
```

### 场景 2:退款确认(带副文案 + 非危险默认)

`hide-icon` 去图标;副文案经 `#reference` 外的 `title` + 自定义内容表达;普通提交用 primary 而非 danger。

```vue
<template>
  <el-popconfirm
    title="确认申请退款 ¥128.00?退款将在 1-3 个工作日原路退回"
    confirm-button-text="确认申请"
    cancel-button-text="再想想"
    confirm-button-type="primary"
    hide-icon
    width="260"
    @confirm="refund"
  >
    <template #reference>
      <el-button>申请退款</el-button>
    </template>
  </el-popconfirm>
</template>

<script setup>
import { ElMessage } from 'element-plus'
const refund = () => ElMessage.success('退款申请已提交')
</script>
```

### 场景 3:不可逆操作升级 elMessageBox

后果严重的操作不用气泡,升级为确认弹窗(`ElMessageBox.confirm`):

```vue
<template>
  <el-button type="danger" @click="cancelAccount">注销账户</el-button>
</template>

<script setup>
import { ElMessageBox, ElMessage } from 'element-plus'
const cancelAccount = async () => {
  await ElMessageBox.confirm(
    '注销后所有数据将被清空且无法恢复',
    '确认注销账户?',
    { confirmButtonText: '确认注销', cancelButtonText: '取消', type: 'warning' }
  )
  ElMessage.success('已提交注销申请')
}
</script>
```

## 参考链接

- Element Plus 官方文档 - Popconfirm 气泡确认框: https://element-plus.org/zh-CN/component/popconfirm
- MessageBox 弹框: https://element-plus.org/zh-CN/component/message-box
