<template>
  <el-radio-group v-model="theme" @change="changeTheme">
    <el-radio label="system">Системная</el-radio>
    <el-radio label="light">Светлая тема</el-radio>
    <el-radio label="dark">Тёмная тема</el-radio>
  </el-radio-group>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
const theme = ref(localStorage.getItem('theme') || 'system')

function applyTheme(value: string) {
  const html = document.documentElement
  if (value === 'dark') {
    html.setAttribute('data-theme', 'dark')
  } else if (value === 'light') {
    html.setAttribute('data-theme', 'light')
  } else {
    // system
    html.removeAttribute('data-theme')
  }
}

function changeTheme(val: string) {
  localStorage.setItem('theme', val)
  applyTheme(val)
}

onMounted(() => {
  applyTheme(theme.value)
})
</script>
<style>
:root {
  --el-bg-color: #fff;
  --el-text-color-primary: #222;
  --el-menu-bg-color: #fff;
  --el-menu-text-color: #222;
}
[data-theme='dark'] {
  --el-bg-color: #181818;
  --el-text-color-primary: #fff;
  --el-menu-bg-color: #232323;
  --el-menu-text-color: #fff;
  background: #181818;
  color-scheme: dark;
}
[data-theme='light'] {
  --el-bg-color: #fff;
  --el-text-color-primary: #222;
  --el-menu-bg-color: #fff;
  --el-menu-text-color: #222;
  background: #fff;
  color-scheme: light;
}
body,
html {
  background: var(--el-bg-color);
  color: var(--el-text-color-primary);
}
.el-menu {
  background-color: var(--el-menu-bg-color) !important;
  color: var(--el-menu-text-color) !important;
}
.el-menu .el-menu-item {
  color: var(--el-menu-text-color) !important;
}
</style>
