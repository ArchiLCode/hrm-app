<template>
  <div v-if="!(userStore.user?.role === 'employee')">
    <el-dialog v-model="dialogVisible" title="Добавить отдел" width="400px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="Название" prop="name">
          <el-input v-model="form.name" placeholder="Название" />
        </el-form-item>
        <el-form-item label="Описание" prop="description">
          <el-input v-model="form.description" placeholder="Описание" />
        </el-form-item>
        <el-form-item label="Менеджер" prop="manager_id">
          <el-select v-model="form.manager_id" placeholder="Выбрать менеджера">
            <el-option
              v-for="manager in managers"
              :key="manager.id"
              :label="manager.full_name || manager.email"
              :value="manager.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Отменить</el-button>
        <el-button type="primary" :loading="loading" @click="onSubmit">Создать</el-button>
      </template>
    </el-dialog>
    <el-button type="primary" :icon="Plus" @click="dialogVisible = true">Добавить отдел</el-button>
  </div>
</template>
<script setup lang="ts">
import { ref, defineEmits, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import api from '../../client/api'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()
const emit = defineEmits(['refresh'])
const dialogVisible = ref(false)
const loading = ref(false)
const formRef = ref()
const managers = ref<any[]>([])
const form = ref({
  name: '',
  description: '',
  manager_id: '',
})
const rules = {
  name: [{ required: true, message: 'Name is required', trigger: 'blur' }],
  manager_id: [{ required: true, message: 'Manager is required', trigger: 'blur' }],
}

async function onSubmit() {
  await formRef.value.validate()
  loading.value = true
  try {
    await api.post('/departments', {
      name: form.value.name,
      description: form.value.description,
      manager_id: form.value.manager_id,
    })
    ElMessage.success('Отдел успешно создан!')
    dialogVisible.value = false
    form.value = { name: '', description: '', manager_id: '' }
    emit('refresh')
  } catch (e) {
    ElMessage.error('Ошибка при создании отдела.')
  } finally {
    loading.value = false
  }
}

async function loadManagers() {
  try {
    const { data } = await api.get('/users/managers')
    managers.value = data.data
  } catch (e) {
    ElMessage.error('Ошибка при загрузке менеджеров.')
  }
}

onMounted(async () => {
  await loadManagers()
})
</script>
