<template>
  <el-row justify="center" align="middle" style="height: 100vh">
    <el-col style="width: 480px">
      <el-card>
        <h2 style="text-align: center; margin-bottom: 30px">Авторизация</h2>
        <el-form
          :model="form"
          :rules="rules"
          ref="formRef"
          label-width="90px"
          style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 10px;
          "
          @submit.prevent="onLogin"
        >
          <el-form-item label="Email" prop="email">
            <el-input v-model="form.email" placeholder="Email" />
          </el-form-item>
          <el-form-item label="Пароль" prop="password">
            <el-input v-model="form.password" type="password" placeholder="Пароль" />
          </el-form-item>
          <el-form-item label-width="0" style="width: 140px">
            <el-button type="primary" :loading="loading" @click="onLogin" style="width: 100%"
              >Войти</el-button
            >
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)
const form = ref({
  email: '',
  password: '',
})
const rules = {
  email: [
    { required: true, message: 'Email is required', trigger: 'blur' },
    { type: 'email', message: 'Invalid email', trigger: 'blur' },
  ],
  password: [
    { required: true, message: 'Password is required', trigger: 'blur' },
    { min: 6, message: 'Min 6 characters', trigger: 'blur' },
  ],
}

async function onLogin() {
  await formRef.value.validate()
  loading.value = true
  try {
    await userStore.login(form.value.email, form.value.password)
    await userStore.fetchUser()
    ElMessage.success('Успешная авторизация!')
    router.replace('/')
  } catch (e) {
    ElMessage.error('Неверные данные.')
  } finally {
    loading.value = false
  }
}
</script>
