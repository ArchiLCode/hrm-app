<template>
  <div class="navbar-content">
    <router-link to="/">
      <img src="../../assets/logo.png" alt="Logo" class="logo" />
    </router-link>
    <el-menu
      mode="horizontal"
      :default-active="$route.path"
      class="navbar-menu"
      router
      style="flex: 1; min-width: 0; max-width: 700px; justify-content: flex-start"
      :ellipsis="false"
    >
      <el-menu-item index="/">Главная</el-menu-item>
      <el-menu-item v-if="userStore.user && userStore.user.is_superuser" index="/admin"
        >Админ-панель</el-menu-item
      >
      <el-menu-item index="/employees">Персонал</el-menu-item>
      <el-menu-item index="/departments">Отделы</el-menu-item>
      <el-menu-item index="/leaves">Отпуска</el-menu-item>
    </el-menu>
    <div class="navbar-right">
      <UserMenu />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '../../stores/user'
const userStore = useUserStore()
</script>

<style scoped>
.navbar-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
  padding: 0 24px;
  min-width: 0;
}
.logo {
  height: 40px;
}
.navbar-menu {
  flex: 1;
  margin: 0 32px;
  background: transparent;
  border-bottom: none;
  min-width: 0;
  max-width: 700px;
  justify-content: space-between;
}
.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
