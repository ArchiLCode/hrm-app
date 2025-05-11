<template>
  <div>
    <el-table :data="users" v-loading="loading" style="width: 100%">
      <el-table-column prop="id" label="ID" width="180" />
      <el-table-column prop="full_name" label="Full Name" />
      <el-table-column prop="email" label="Email" />
      <el-table-column prop="role" label="Role" />
      <el-table-column prop="status" label="Status" />
      <el-table-column label="Actions" width="160">
        <template #default="scope">
          <el-button size="small" @click="onEdit(scope.row)" v-if="canEditOrDelete(scope.row)"
            >Edit</el-button
          >
          <el-button
            size="small"
            type="danger"
            @click="onDelete(scope.row)"
            v-if="canEditOrDelete(scope.row)"
            >Delete</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-if="total > pageSize"
      :current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="prev, pager, next"
      @current-change="onPageChange"
      style="margin-top: 16px; text-align: right"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../../stores/user'
import api from '../../client/api'
// import { UsersService } from '@/client/sdk.gen'
const userStore = useUserStore()
const users = ref<
  Array<{
    id: number
    full_name: string
    email: string
    role: string
    status: string
  }>
>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 5
const total = ref(0)
async function fetchUsers() {
  loading.value = true
  try {
    // const res = await UsersService.readUsers({ skip: (page.value - 1) * pageSize, limit: pageSize })
    // users.value = res.data
    // total.value = res.count
    // DEMO MOCK:
    users.value = Array.from({ length: 3 }, (_, i) => ({
      id: i + 1 + (page.value - 1) * pageSize,
      full_name: `User ${i + 1 + (page.value - 1) * pageSize}`,
      email: `user${i + 1 + (page.value - 1) * pageSize}@mail.com`,
      role: i === 0 ? 'Superuser' : 'User',
      status: i % 2 === 0 ? 'Active' : 'Inactive',
    }))
    total.value = 12
  } finally {
    loading.value = false
  }
}
function onPageChange(val: number) {
  page.value = val
  fetchUsers()
}
function onEdit(row: any) {
  // TODO: реализовать редактирование
}
async function onDelete(row: any) {
  try {
    await api.delete(`/users/${row.id}`)
    ElMessage.success('Пользователь удалён')
    fetchUsers()
  } catch (e) {
    ElMessage.error('Ошибка при удалении пользователя')
  }
}
function canEditOrDelete(row: any) {
  const user = userStore.user
  if (!user) return false
  return user.role === 'admin'
}
onMounted(fetchUsers)
</script>
