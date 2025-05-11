<template>
  <div>
    <el-alert title="Внимание! Это действие нельзя отменить!" type="error" show-icon> </el-alert
    ><el-button
      style="margin-top: 10px"
      type="danger"
      :loading="loading"
      @click="dialogVisible = true"
      >Удалить аккаунт</el-button
    >
    <el-dialog
      v-model="dialogVisible"
      title="Подтверждение"
      width="350px"
      :close-on-click-modal="false"
    >
      <span>Вы уверены, что хотите удалить свой аккаунт?</span>
      <template #footer>
        <el-button @click="dialogVisible = false">Отмена</el-button>
        <el-button type="danger" :loading="loading" @click="onDelete">Удалить</el-button>
      </template>
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import api from '../../client/api'
import { useUserStore } from '../../stores/user'
import { useRouter } from 'vue-router'

const loading = ref(false)
const dialogVisible = ref(false)
const router = useRouter()
const userStore = useUserStore()

async function onDelete() {
  loading.value = true
  try {
    await api.delete('/users/me')
    userStore.logout()
    router.push('/login')
  } finally {
    loading.value = false
    dialogVisible.value = false
  }
}
</script>
