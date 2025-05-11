<template>
  <el-form label-width="120px" style="max-width: 400px">
    <el-form-item label="Полное имя">
      <el-input v-model="profile.full_name" placeholder="Иванов Иван Иванович" />
    </el-form-item>
    <el-form-item label="Email">
      <el-input v-model="profile.email" placeholder="Email" disabled />
    </el-form-item>
    <el-form-item label="Роль">
      <el-input v-model="profile.roleLabel" disabled />
    </el-form-item>
    <el-form-item v-if="profile.role === 'manager'" label="Отделы (менеджер)">
      <el-select v-model="profile.managedDepartments" multiple disabled>
        <el-option
          v-for="dept in profile.managedDepartments"
          :key="dept.id"
          :label="dept.name"
          :value="dept.name"
        />
      </el-select>
    </el-form-item>
    <template v-if="profile.role === 'employee'">
      <el-form-item label="Должность">
        <el-input v-model="profile.position" disabled />
      </el-form-item>
      <el-form-item label="Дата приёма">
        <el-input v-model="profile.hire_date" disabled />
      </el-form-item>
      <el-form-item label="Телефон">
        <el-input v-model="profile.phone" disabled />
      </el-form-item>
      <el-form-item label="Зарплата">
        <el-input v-model="profile.salary" disabled />
      </el-form-item>
    </template>
    <el-form-item>
      <el-button type="primary" :loading="loading" @click="onSave">Сохранить</el-button>
    </el-form-item>
  </el-form>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../../client/api'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()
const loading = ref(false)
const profile = ref({
  full_name: '',
  email: '',
  role: '',
  roleLabel: '',
  managedDepartments: [] as any[],
  position: '',
  hire_date: '',
  phone: '',
  salary: '',
})

const roleLabels: Record<string, string> = {
  employee: 'Сотрудник',
  manager: 'Менеджер',
  admin: 'Администратор',
}

onMounted(async () => {
  await userStore.fetchUser()
  if (userStore.user) {
    profile.value.full_name = userStore.user.full_name || ''
    profile.value.email = userStore.user.email || ''
    profile.value.role = userStore.user.role || ''
    profile.value.roleLabel = roleLabels[userStore.user.role] || userStore.user.role
    // Если менеджер — получить отделы, которыми управляет
    if (userStore.user.role === 'manager') {
      const { data } = await api.get('/departments')
      profile.value.managedDepartments = data.filter((d: any) => d.manager_id === userStore.user.id)
    }
    // Если сотрудник — получить инфо о сотруднике
    if (userStore.user.role === 'employee') {
      try {
        const { data } = await api.get('/employees/me')
        profile.value.position = data.position
        profile.value.hire_date = data.hire_date
        profile.value.phone = data.phone
        profile.value.salary = data.salary
      } catch {}
    }
  }
})

async function onSave() {
  loading.value = true
  try {
    await api.patch('/users/me', { full_name: profile.value.full_name })
    await userStore.fetchUser()
  } finally {
    loading.value = false
  }
}
</script>
