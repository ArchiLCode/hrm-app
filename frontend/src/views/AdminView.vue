<template>
  <el-container>
    <el-main>
      <template v-if="currentUser?.is_superuser">
        <h2>Админ-панель</h2>
        <AddManager />
      </template>
      <el-alert
        v-else
        title="Доступ запрещен"
        type="error"
        description="У вас нет прав для просмотра этой страницы"
        show-icon
        :closable="false"
      />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const currentUser = userStore.user
</script>
