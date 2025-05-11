<template>
  <div>
    <AddDepartment @refresh="refresh" />
    <el-table :data="departments" v-loading="loading" style="width: 100%">
      <el-table-column prop="name" label="Название" />
      <el-table-column prop="description" label="Описание" />
      <el-table-column label="Менеджер">
        <template #default="scope">
          {{ getManagerName(scope.row.manager_id) }}
        </template>
      </el-table-column>
      <el-table-column label="Действия" width="160">
        <template #default="scope">
          <el-button
            size="small"
            :icon="Edit"
            @click="onEdit(scope.row)"
            v-if="canEditOrDelete(scope.row)"
          ></el-button>
          <el-button
            size="small"
            type="danger"
            @click="onDelete(scope.row)"
            v-if="canEditOrDelete(scope.row)"
            >Удалить</el-button
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
import api from '../../client/api'
import { Edit } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()

const departments = ref([])
const managers = ref<Manager[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 10
const total = ref(0)

interface Manager {
  id: string
  full_name?: string
  email: string
}

async function fetchManagers() {
  try {
    const { data } = await api.get('/users/managers')
    managers.value = data.data || []
  } catch (e) {
    ElMessage.error('Ошибка загрузки менеджеров')
  }
}

function getManagerName(managerId: string) {
  const manager = managers.value.find((m) => m.id === managerId)
  return manager ? manager.full_name || manager.email : managerId
}

async function fetchDepartments() {
  loading.value = true
  try {
    const { data } = await api.get('/departments', {
      params: {
        skip: (page.value - 1) * pageSize,
        limit: pageSize,
      },
    })
    departments.value = data
    total.value = Array.isArray(data) ? data.length : 0
  } catch (e) {
    ElMessage.error('Ошибка загрузки отделов.')
  } finally {
    loading.value = false
  }
}

function onPageChange(val: number) {
  page.value = val
  fetchDepartments()
}
function onEdit(row: any) {
  // TODO: реализовать редактирование
}
function canEditOrDelete(row: any) {
  const user = userStore.user
  if (!user) return false
  if (user.is_superuser) return true
  if (user.role === 'manager') {
    return row.manager_id === user.id
  }
  return false
}
async function onDelete(row: any) {
  try {
    await api.delete(`/departments/${row.id}`)
    ElMessage.success('Отдел удалён')
    fetchDepartments()
  } catch (e) {
    ElMessage.error('Ошибка при удалении отдела')
  }
}
function refresh() {
  fetchDepartments()
}

onMounted(async () => {
  await fetchManagers()
  await fetchDepartments()
})
</script>
