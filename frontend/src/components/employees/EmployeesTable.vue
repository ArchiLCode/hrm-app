<template>
  <div>
    <AddEmployee @refresh="refresh" />
    <el-table :data="employees" v-loading="loading" style="width: 100%">
      <el-table-column prop="user_name" label="Полное имя" />
      <el-table-column prop="department_name" label="Отдел" />
      <el-table-column prop="position" label="Должность" />
      <el-table-column prop="hire_date" label="Принят на работу" />
      <el-table-column prop="phone" label="Телефон" />
      <el-table-column
        v-if="!(userStore.user?.role === 'employee')"
        prop="salary"
        label="Зарплата"
      />
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
            >Уволить</el-button
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
const employees = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = 10
const total = ref(0)
const managedDepartmentIds = ref<string[]>([])

async function fetchEmployees() {
  loading.value = true
  try {
    const { data } = await api.get('/employees', {
      params: {
        skip: (page.value - 1) * pageSize,
        limit: pageSize,
      },
    })
    // Получаем user_name и department_name для каждого сотрудника
    const userIds = [...new Set(data.map((e: any) => e.user_id))]
    const departmentIds = [...new Set(data.map((e: any) => e.department_id))]
    // Получаем пользователей
    const userMap: Record<string, string> = {}
    await Promise.all(
      (userIds as string[]).map(async (id) => {
        try {
          const { data: user } = await api.get(`/users/${id}`)
          userMap[String(id)] = user.full_name || user.email || String(id)
        } catch {
          userMap[String(id)] = String(id)
        }
      }),
    )
    // Получаем отделы
    const departmentMap: Record<string, string> = {}
    await Promise.all(
      (departmentIds as string[]).map(async (id) => {
        try {
          const { data: dept } = await api.get(`/departments/${id}`)
          departmentMap[String(id)] = dept.name || String(id)
        } catch {
          departmentMap[String(id)] = String(id)
        }
      }),
    )
    // Формируем итоговый массив
    employees.value = data.map((e: any) => ({
      ...e,
      department_name: departmentMap[String(e.department_id)] || e.department_id,
    }))
    total.value = Array.isArray(data) ? data.length : 0
  } finally {
    loading.value = false
  }
}

async function fetchManagedDepartments() {
  const user = userStore.user
  if (user && user.role === 'manager') {
    try {
      const { data } = await api.get('/departments')
      managedDepartmentIds.value = data
        .filter((d: any) => d.manager_id === user.id)
        .map((d: any) => d.id)
    } catch {
      managedDepartmentIds.value = []
    }
  } else {
    managedDepartmentIds.value = []
  }
}

function onPageChange(val: number) {
  page.value = val
  fetchEmployees()
}
function onEdit(row: any) {
  // TODO: реализовать редактирование
}
async function onDelete(row: any) {
  try {
    await api.delete(`/employees/${row.id}`)
    ElMessage.success('Сотрудник уволен')
    fetchEmployees()
  } catch (e) {
    ElMessage.error('Ошибка при удалении сотрудника')
  }
}
function refresh() {
  fetchEmployees()
}
function canEditOrDelete(row: any) {
  const user = userStore.user
  if (!user) return false
  if (user.is_superuser) return true
  if (user.role === 'manager') {
    return managedDepartmentIds.value.includes(row.department_id)
  }
  return false
}

onMounted(async () => {
  await fetchManagedDepartments()
  await fetchEmployees()
})
</script>
