<template>
  <div>
    <el-dialog v-model="dialogVisible" title="Добавить менеджера" width="400px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="Email" prop="email">
          <el-input v-model="form.email" placeholder="Email" />
        </el-form-item>
        <el-form-item label="Пароль" prop="password">
          <el-input v-model="form.password" type="password" placeholder="Пароль" />
        </el-form-item>
        <el-form-item label="Полное имя" prop="full_name">
          <el-input v-model="form.full_name" placeholder="Иванов Иван Иванович" />
        </el-form-item>
        <el-form-item label="Отдел" prop="department_id">
          <el-input v-model="form.department_id" placeholder="Отдел (необязательно)" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Отменить</el-button>
        <el-button type="primary" :loading="loading" @click="onSubmit">Сохранить</el-button>
      </template>
    </el-dialog>
    <el-button type="primary" :icon="Plus" @click="dialogVisible = true"
      >Добавить менеджера</el-button
    >
  </div>
</template>
<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import api from '../../client/api'

const emit = defineEmits(['refresh'])
const dialogVisible = ref(false)
const loading = ref(false)
const formRef = ref()
const form = ref({
  email: '',
  password: '',
  full_name: '',
  department_id: '',
})
const rules = {
  email: [
    { required: true, message: 'Email is required', trigger: 'blur' },
    { type: 'email', message: 'Invalid email', trigger: 'blur' },
  ],
  password: [
    { required: true, message: 'Password is required', trigger: 'blur' },
    { min: 6, message: 'Min 6 characters', trigger: 'blur' },
  ],
  full_name: [{ required: true, message: 'Full Name is required', trigger: 'blur' }],
  department_id: [], // Optional field
}

async function onSubmit() {
  await formRef.value.validate()
  loading.value = true
  try {
    // 1. Создать пользователя с ролью manager
    const { data: user } = await api.post('/users/', {
      email: form.value.email,
      password: form.value.password,
      full_name: form.value.full_name,
      is_active: true,
      is_superuser: false,
      role: 'manager',
    })
    // 2. (опционально) создать сотрудника
    // await api.post('/employees', { user_id: user.id, department_id: form.value.department_id, position: 'Manager', hire_date: new Date().toISOString().slice(0, 10) })    // 3. Назначить менеджера отделу (если указан)
    if (form.value.department_id) {
      await api.patch(`/departments/${form.value.department_id}`, { manager_id: user.id })
      ElMessage.success('Manager created and assigned to department.')
    } else {
      ElMessage.success('Manager created successfully.')
    }
    dialogVisible.value = false
    form.value = { email: '', password: '', full_name: '', department_id: '' }
    emit('refresh')
  } catch (e) {
    ElMessage.error('Error creating manager')
  } finally {
    loading.value = false
  }
}
</script>
