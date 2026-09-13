# Upload 上传

> Element Plus 上传组件 `<el-upload>`,覆盖"触发器 + 文件列表 + 进度 + 失败重试"完整模式,支持头像、拖拽、照片墙等形态。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-upload> <el-upload--picture-card> <el-upload-dragger>
```

`<el-upload>` 为容器,`action` 指定上传地址;`#trigger` / `#tip` 插槽定义触发器与提示;`<el-upload-dragger>` 提供拖拽区域。

## 基本用法

```vue
<template>
  <el-upload
    action="https://api.example.com/upload"
    :on-success="onSuccess"
    :on-error="onError"
  >
    <el-button type="primary">点击上传</el-button>
    <template #tip>
      <div class="el-upload__tip">单个不超过 10MB 的 jpg/png 文件</div>
    </template>
  </el-upload>
</template>

<script setup>
const onSuccess = (res) => console.log('成功', res)
const onError = () => console.log('失败,可重试')
</script>
```

## 使用场景

### 场景 1:头像上传(单图 + 回显)

`limit: 1` 限一张;`on-exceed` 提示替换;`show-file-list` 关闭默认列表。

```vue
<template>
  <el-upload
    class="avatar-uploader"
    action="https://api.example.com/upload"
    :show-file-list="false"
    :on-success="handleSuccess"
    :before-upload="beforeUpload"
  >
    <el-image v-if="avatarUrl" :src="avatarUrl" class="avatar" fit="cover" />
    <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
  </el-upload>
</template>

<script setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
const avatarUrl = ref('')
const beforeUpload = (file) => {
  const ok = file.type.startsWith('image/') && file.size / 1024 / 1024 < 2
  if (!ok) ElMessage.error('仅支持 2MB 内图片')
  return ok
}
const handleSuccess = (res) => (avatarUrl.value = res.url)
</script>

<style scoped>
.avatar { width: 72px; height: 72px; border-radius: {radius-full}; }
</style>
```

### 场景 2:照片墙(多图 + 进度)

`list-type="picture-card"` 照片墙;`:on-progress` 驱动每项进度。

```vue
<template>
  <el-upload
    v-model:file-list="fileList"
    action="https://api.example.com/upload"
    list-type="picture-card"
    :limit="9"
    :on-exceed="() => ElMessage.warning('最多 9 张')"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>
</template>

<script setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
const fileList = ref([])
</script>
```

### 场景 3:拖拽上传

`<el-upload-dragger>` 包裹拖拽区,适合后台大文件/附件场景。

```vue
<template>
  <el-upload drag action="https://api.example.com/upload" multiple>
    <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
    <div class="el-upload__text">拖拽文件到此处,或<em>点击选择</em></div>
  </el-upload>
</template>

<script setup>
import { UploadFilled } from '@element-plus/icons-vue'
</script>
```

## 参考链接

- Element Plus 官方文档 - Upload 上传: https://element-plus.org/zh-CN/component/upload
