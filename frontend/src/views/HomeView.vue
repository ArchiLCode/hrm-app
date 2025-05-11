<template>
  <el-container>
    <el-main>
      <h2 style="text-align: center">
        Добро пожаловать, {{ userStore.getUser?.full_name || 'User' }}!
      </h2>
      <el-card style="margin: 0 auto; margin-top: 20px; width: 360px">
        <p>
          Этот сервис предназначен для управления персоналом, отделами, отпусками в компании.
          Система поддерживает роли сотрудников, менеджеров и администраторов, автоматизирует
          процессы подачи и согласования заявок на отпуск.
        </p>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
</script>
