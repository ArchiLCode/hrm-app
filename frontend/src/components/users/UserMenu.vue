<template>
  <el-dropdown>
    <span class="el-dropdown-link">
      <el-icon><i class="el-icon-user"></i></el-icon>
      <span>{{ userName }}</span>
      <el-icon><i class="el-icon-arrow-down"></i></el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item @click="goToSettings">Настройки</el-dropdown-item>
        <el-dropdown-item divided @click="logout">Выйти</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, computed } from 'vue'
import { useUserStore } from '../../stores/user'

const router = useRouter()
const userStore = useUserStore()

const userName = computed(() => userStore.user?.full_name || 'Admin')

onMounted(async () => {
  await userStore.fetchUser()
})

function goToSettings() {
  router.push('/settings')
}
function logout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.el-dropdown-link {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}
</style>
