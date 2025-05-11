<template>
  <el-container>
    <el-main>
      <h2>Настройки</h2>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="Мой профиль" name="profile">
          <UserProfile />
        </el-tab-pane>
        <el-tab-pane label="Внешний вид" name="appearance">
          <UserAppearance />
        </el-tab-pane>
        <el-tab-pane label="Опасная зона" name="danger">
          <UserDanger />
        </el-tab-pane>
      </el-tabs>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const activeTab = ref('profile')
</script>
