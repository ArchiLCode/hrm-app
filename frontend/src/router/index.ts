import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminView from '../views/AdminView.vue'
import SettingsView from '../views/SettingsView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import EmployeesView from '../views/EmployeesView.vue'
import LoginView from '../views/LoginView.vue'
import DepartmentsView from '../views/DepartmentsView.vue'
import LeaveRequestsView from '../views/LeaveRequestsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    { path: '/admin', name: 'admin', component: AdminView },
    { path: '/settings', name: 'settings', component: SettingsView },
    { path: '/employees', name: 'employees', component: EmployeesView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/departments', name: 'departments', component: DepartmentsView },
    { path: '/leaves', name: 'leaves', component: LeaveRequestsView },
    { path: '/:pathMatch(.*)*', name: 'notfound', component: NotFoundView },
  ],
})

router.beforeEach((to, from, next) => {
  const isAuth = localStorage.getItem('access_token')
  if (to.path === '/') {
    if (isAuth) {
      next()
    } else {
      next({ name: 'login' })
    }
    return
  }
  if (!isAuth && to.name !== 'login') {
    next({ name: 'login' })
  } else if (isAuth && to.name === 'login') {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
