import { defineStore } from 'pinia'
import api from '../client/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as any,
    isAuthenticated: false,
  }),
  getters: {
    getUser: (state) => state.user,
    getIsAuthenticated: (state) => state.isAuthenticated,
  },
  actions: {
    async fetchUser() {
      try {
        const { data } = await api.get('/users/me')
        this.user = data
        this.isAuthenticated = true
      } catch {
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('access_token')
      }
    },
    async login(email: string, password: string) {
      const params = new URLSearchParams()
      params.append('username', email)
      params.append('password', password)
      const { data } = await api.post('/login/access-token', params)
      localStorage.setItem('access_token', data.access_token)
      await this.fetchUser()
    },
    logout() {
      localStorage.removeItem('access_token')
      this.user = null
      this.isAuthenticated = false
    },
    async init() {
      const token = localStorage.getItem('access_token')
      if (token) {
        await this.fetchUser()
      }
    },
  },
})
