<template>
  <el-container
    style="align-items: center; justify-content: center; display: flex; flex-direction: column"
  >
    <h1 style="font-size: 6rem; font-weight: bold">404</h1>
    <h2>Упс!</h2>
    <p>Такой страницы не существует.</p>
    <el-button style="margin-top: 20px" type="primary" @click="$router.push('/')"
      >На главную</el-button
    >
  </el-container>
</template>

<script setup lang="ts"></script>
