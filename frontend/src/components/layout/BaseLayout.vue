<template>
  <el-container style="min-height: 100vh; width: 960px">
    <el-header class="navbar">
      <Navbar />
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import Navbar from './Navbar.vue'
</script>

<style scoped>
.navbar {
  background: #fff;
  border-bottom: 1px solid #ebeef5;
  padding: 0;
}
</style>
