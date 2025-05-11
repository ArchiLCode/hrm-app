<template>
  <div v-if="!(userStore.user?.role === 'employee')">
    <el-dialog v-model="dialogVisible" title="Добавить сотрудника" width="460px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="140px">
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
          <el-select v-model="form.department_id" placeholder="Выбрать отдел" filterable>
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Должность" prop="position">
          <el-input v-model="form.position" placeholder="Должность" />
        </el-form-item>
        <el-form-item label="Принят на работу" prop="hire_date">
          <el-date-picker v-model="form.hire_date" type="date" placeholder="2025-01-01" />
        </el-form-item>
        <el-form-item label="Телефон" prop="phone">
          <el-input v-model="form.phone" placeholder="+79901001010" />
        </el-form-item>
        <el-form-item label="Зарплата" prop="salary">
          <el-input v-model="form.salary" placeholder="0" type="number" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Отменить</el-button>
        <el-button type="primary" :loading="loading" @click="onSubmit">Сохранить</el-button>
      </template>
    </el-dialog>
    <el-button type="primary" :icon="Plus" @click="dialogVisible = true"
      >Добавить сотрудника</el-button
    >
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
const form = ref({
  email: '',
  password: '',
  full_name: '',
  department_id: '',
  position: '',
  hire_date: '',
  phone: '',
  salary: undefined,
})
const departments = ref<any[]>([])

onMounted(async () => {
  try {
    const { data } = await api.get('/departments')
    departments.value = data
  } catch (e) {
    departments.value = []
  }
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
  department_id: [{ required: true, message: 'Department is required', trigger: 'blur' }],
  position: [{ required: true, message: 'Position is required', trigger: 'blur' }],
  hire_date: [{ required: true, message: 'Hire date is required', trigger: 'blur' }],
}

async function onSubmit() {
  await formRef.value.validate()
  const currentUser = userStore.user
  loading.value = true
  try {
    // 1. Создать пользователя
    const { data: user } = await api.post('/users/', {
      email: form.value.email,
      password: form.value.password,
      full_name: form.value.full_name,
      department_id: currentUser.role === 'manager' ? form.value.department_id : undefined,
    })
    // 2. Создать сотрудника
    await api.post('/employees', {
      user_id: user.id,
      department_id: form.value.department_id,
      position: form.value.position,
      hire_date: form.value.hire_date,
      phone: form.value.phone,
      salary: form.value.salary,
    })
    ElMessage.success('Employee created successfully.')
    dialogVisible.value = false
    form.value = {
      email: '',
      password: '',
      full_name: '',
      department_id: '',
      position: '',
      hire_date: '',
      phone: '',
      salary: undefined,
    }
    emit('refresh')
  } catch (e) {
    ElMessage.error('Error creating employee')
  } finally {
    loading.value = false
  }
}
</script>
