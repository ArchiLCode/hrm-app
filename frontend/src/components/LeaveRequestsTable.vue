<template>
  <div>
    <el-row justify="space-between" align="middle" class="mb-4">
      <el-col style="margin: 10px 0"><h3>Заявки на отпуск/больничный</h3></el-col>
      <el-col v-if="role === 'employee'">
        <el-button type="primary" @click="showRequestDialog = true">Подать заявку</el-button>
      </el-col>
      <el-col v-if="role === 'manager' || role === 'admin'">
        <el-button type="success" @click="showAssignDialog = true">Назначить отпуск</el-button>
      </el-col>
    </el-row>
    <el-table :data="leaveRequests" style="width: 100%" v-loading="loading">
      <el-table-column
        prop="employee.user.full_name"
        label="Сотрудник"
        v-if="role !== 'employee'"
      />
      <el-table-column prop="leave_type" label="Тип" />
      <el-table-column prop="start_date" label="Начало" />
      <el-table-column prop="end_date" label="Конец" />
      <el-table-column prop="status" label="Статус" />
      <el-table-column prop="created_at" label="Создана" />
      <el-table-column width="160" v-if="role === 'manager' || role === 'admin'" label="Действия">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'pending' && role === 'manager'"
            size="small"
            type="success"
            @click="approve(row)"
            >Одобрить</el-button
          >
          <el-button
            v-if="row.status === 'pending' && role === 'manager'"
            size="small"
            type="danger"
            @click="reject(row)"
            >Отклонить</el-button
          >
          <el-button size="small" :icon="Edit" @click="openEditDialog(row)"></el-button>
          <el-button size="small" type="danger" @click="deleteLeave(row)">Удалить</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Диалог подачи заявки -->
    <el-dialog v-model="showRequestDialog" title="Подать заявку" width="400px">
      <el-form :model="requestForm">
        <el-form-item label="Тип">
          <el-select v-model="requestForm.leave_type" placeholder="Выберите тип">
            <el-option label="Отпуск" value="vacation" />
            <el-option label="Больничный" value="sick_leave" />
          </el-select>
        </el-form-item>
        <el-form-item label="Начало">
          <el-date-picker v-model="requestForm.start_date" type="date" />
        </el-form-item>
        <el-form-item label="Конец">
          <el-date-picker v-model="requestForm.end_date" type="date" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRequestDialog = false">Отмена</el-button>
        <el-button type="primary" @click="submitRequest">Отправить</el-button>
      </template>
    </el-dialog>

    <!-- Диалог назначения отпуска -->
    <el-dialog v-model="showAssignDialog" title="Назначить отпуск" width="400px">
      <el-form :model="assignForm">
        <el-form-item label="Сотрудник">
          <el-select v-model="assignForm.employee_id" filterable placeholder="Выберите сотрудника">
            <el-option
              v-for="emp in employees"
              :key="emp.id"
              :label="emp.user?.full_name"
              :value="emp.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Тип">
          <el-select v-model="assignForm.leave_type" placeholder="Выберите тип">
            <el-option label="Отпуск" value="vacation" />
            <el-option label="Больничный" value="sick_leave" />
          </el-select>
        </el-form-item>
        <el-form-item label="Начало">
          <el-date-picker v-model="assignForm.start_date" type="date" />
        </el-form-item>
        <el-form-item label="Конец">
          <el-date-picker v-model="assignForm.end_date" type="date" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAssignDialog = false">Отмена</el-button>
        <el-button type="primary" @click="assignLeave()">Назначить</el-button>
      </template>
    </el-dialog>

    <!-- Диалог редактирования отпуска -->
    <el-dialog v-model="showEditDialog" title="Редактировать отпуск" width="400px">
      <el-form :model="editForm">
        <el-form-item label="Сотрудник">
          <el-select
            v-model="editForm.employee_id"
            filterable
            placeholder="Выберите сотрудника"
            :disabled="true"
          >
            <el-option
              v-for="emp in employees"
              :key="emp.id"
              :label="emp.user?.full_name"
              :value="emp.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Тип">
          <el-select v-model="editForm.leave_type" placeholder="Выберите тип">
            <el-option label="Отпуск" value="vacation" />
            <el-option label="Больничный" value="sick_leave" />
          </el-select>
        </el-form-item>
        <el-form-item label="Начало">
          <el-date-picker v-model="editForm.start_date" type="date" />
        </el-form-item>
        <el-form-item label="Конец">
          <el-date-picker v-model="editForm.end_date" type="date" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">Отмена</el-button>
        <el-button type="primary" @click="saveEdit">Сохранить</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import api from '../client/api'
import { Edit } from '@element-plus/icons-vue'

const props = defineProps<{ user: any; role: string }>()

const leaveRequests = ref([])
const loading = ref(false)
const showRequestDialog = ref(false)
const showAssignDialog = ref(false)
const showEditDialog = ref(false)
const requestForm = ref({ leave_type: '', start_date: '', end_date: '' })
const assignForm = ref({ employee_id: '', leave_type: '', start_date: '', end_date: '' })
const editForm = ref({ id: '', employee_id: '', leave_type: '', start_date: '', end_date: '' })
// КОСТЫЛЬ: Явно указываем тип employees как any[] для устранения TS2339
const employees = ref<any[]>([])

async function fetchLeaveRequests() {
  loading.value = true
  try {
    const { data } = await api.get('/leaverequests')
    leaveRequests.value = data
  } finally {
    loading.value = false
  }
}

async function fetchEmployees() {
  if (props.role === 'admin') {
    const { data } = await api.get('/employees')
    employees.value = data.filter((e: any) => e.is_active)
  } else if (props.role === 'manager') {
    // Получить только сотрудников отделов менеджера
    const { data } = await api.get('/employees')
    employees.value = data.filter(
      (e: any) => e.is_active && e.department.manager_id === props.user.id,
    )
  }
}

async function submitRequest() {
  try {
    const payload = {
      ...requestForm.value,
      start_date: requestForm.value.start_date ? requestForm.value.start_date.slice(0, 10) : '',
      end_date: requestForm.value.end_date ? requestForm.value.end_date.slice(0, 10) : '',
    }
    await api.post('/leaverequests', payload)
    showRequestDialog.value = false
    requestForm.value = { leave_type: '', start_date: '', end_date: '' }
    fetchLeaveRequests()
  } catch (e) {}
}

async function assignLeave() {
  try {
    const toDateString = (val: any) => {
      if (!val) return ''
      if (typeof val === 'string') return val.slice(0, 10)
      if (val instanceof Date) return val.toISOString().slice(0, 10)
      return String(val).slice(0, 10)
    }
    const payload = {
      ...assignForm.value,
      start_date: toDateString(assignForm.value.start_date),
      end_date: toDateString(assignForm.value.end_date),
    }

    await api.post('/leaverequests/assign', payload)
    showAssignDialog.value = false
    assignForm.value = { employee_id: '', leave_type: '', start_date: '', end_date: '' }
    fetchLeaveRequests()
  } catch (e) {}
}

function openEditDialog(row: any) {
  editForm.value = {
    id: row.id,
    employee_id: row.employee_id,
    leave_type: row.leave_type,
    start_date: row.start_date,
    end_date: row.end_date,
  }
  showEditDialog.value = true
}

async function saveEdit() {
  try {
    const payload = {
      leave_type: editForm.value.leave_type,
      start_date: editForm.value.start_date ? editForm.value.start_date.slice(0, 10) : '',
      end_date: editForm.value.end_date ? editForm.value.end_date.slice(0, 10) : '',
    }
    await api.patch(`/leaverequests/${editForm.value.id}`, payload)
    showEditDialog.value = false
    fetchLeaveRequests()
  } catch (e) {}
}

async function deleteLeave(row: any) {
  try {
    await api.delete(`/leaverequests/${row.id}`)
    fetchLeaveRequests()
  } catch (e) {}
}

async function approve(row: any) {
  await api.patch(`/leaverequests/${row.id}`, { status: 'approved' })
  fetchLeaveRequests()
}
async function reject(row: any) {
  await api.patch(`/leaverequests/${row.id}`, { status: 'rejected' })
  fetchLeaveRequests()
}

onMounted(() => {
  fetchLeaveRequests()
  fetchEmployees()
})
watch(
  () => props.role,
  () => fetchEmployees(),
)
</script>
