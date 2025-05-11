<template>
  <div>
    <el-dialog v-model="dialogVisible" title="Add User" width="400px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="Full Name" prop="full_name">
          <el-input v-model="form.full_name" placeholder="Full Name" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="form.email" placeholder="Email" />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="form.password" type="password" placeholder="Password" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" :loading="loading" @click="onSubmit">Save</el-button>
      </template>
    </el-dialog>
    <el-button type="primary" icon="el-icon-plus" @click="dialogVisible = true">Add User</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
// import { UsersService } from '@/client/sdk.gen'
const dialogVisible = ref(false)
const loading = ref(false)
const formRef = ref()
const form = ref({
  full_name: '',
  email: '',
  password: '',
})
const rules = {
  full_name: [
    { required: true, message: 'Full Name is required', trigger: 'blur' },
    { min: 1, max: 255, message: '1-255 characters', trigger: 'blur' },
  ],
  email: [
    { required: true, message: 'Email is required', trigger: 'blur' },
    { type: 'email', message: 'Invalid email', trigger: 'blur' },
  ],
  password: [
    { required: true, message: 'Password is required', trigger: 'blur' },
    { min: 6, message: 'Min 6 characters', trigger: 'blur' },
  ],
}
async function onSubmit() {
  // await formRef.value.validate()
  loading.value = true
  try {
    // await UsersService.createUser({ requestBody: form.value })
    ElMessage.success('User created successfully.')
    dialogVisible.value = false
    form.value.full_name = ''
    form.value.email = ''
    form.value.password = ''
    // emit('refresh')
  } catch (e) {
    ElMessage.error('Error creating user')
  } finally {
    loading.value = false
  }
}
</script>
