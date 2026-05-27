import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { title: '数据看板' } },
      { path: 'employees', name: 'EmployeeList', component: () => import('../views/employee/EmployeeList.vue'), meta: { title: '员工管理' } },
      { path: 'departments', name: 'DepartmentList', component: () => import('../views/department/DepartmentList.vue'), meta: { title: '部门管理' } },
      { path: 'attendances', name: 'AttendanceList', component: () => import('../views/attendance/AttendanceList.vue'), meta: { title: '考勤管理' } },
      { path: 'salaries', name: 'SalaryList', component: () => import('../views/salary/SalaryList.vue'), meta: { title: '薪资管理' } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
