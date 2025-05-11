<template>
  <BaseLayout v-if="userStore.isAuthenticated && $route.name !== 'login'">
    <router-view />
  </BaseLayout>
  <router-view v-else />
</template>

<script setup lang="ts">
import { useUserStore } from './stores/user'
import { watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

watch(
  () => userStore.isAuthenticated,
  (val) => {
    if (!val && route.name !== 'login') {
      router.replace({ name: 'login' })
    }
    if (val && route.name === 'login') {
      router.replace({ name: 'home' })
    }
  },
)
</script>
