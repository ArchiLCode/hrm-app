<template>
  <el-container>
    <el-main>
      <h2>Управление отпусками</h2>
      <LeaveRequestsTable :user="user" :role="role" />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const user = computed(() => userStore.user)
const role = computed(() => userStore.user?.role)
</script>
