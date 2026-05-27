<template>
  <div class="layout">
    <aside class="aside">
      <div class="logo">
        <div class="logo-icon">
          <el-icon :size="20"><OfficeBuilding /></el-icon>
        </div>
        <span>HR 管理系统</span>
      </div>

      <nav class="nav">
        <div
          v-for="item in menuItems"
          :key="item.path"
          class="nav-item"
          :class="{ active: route.path === item.path }"
          @click="router.push(item.path)"
        >
          <el-icon :size="18"><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </div>
      </nav>

      <div class="aside-footer">
        <div class="user-info">
          <div class="avatar">{{ user?.username?.[0]?.toUpperCase() }}</div>
          <div class="user-detail">
            <div class="user-name">{{ user?.username }}</div>
            <div class="user-role">{{ user?.role === 'admin' ? '管理员' : '员工' }}</div>
          </div>
          <el-icon class="logout-btn" @click="handleLogout" title="退出登录"><SwitchButton /></el-icon>
        </div>
      </div>
    </aside>

    <div class="right">
      <header class="header">
        <div class="header-left">
          <span class="header-title">{{ route.meta.title }}</span>
        </div>
        <div class="header-right">
          <span class="time">{{ currentTime }}</span>
        </div>
      </header>
      <main class="main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { removeToken, removeUser, getUser } from '../utils/auth'

const route = useRoute()
const router = useRouter()
const user = computed(() => getUser())
const currentTime = ref('')

const menuItems = [
  { path: '/dashboard', label: '数据看板', icon: 'DataLine' },
  { path: '/employees', label: '员工管理', icon: 'User' },
  { path: '/departments', label: '部门管理', icon: 'OfficeBuilding' },
  { path: '/attendances', label: '考勤管理', icon: 'Clock' },
  { path: '/salaries', label: '薪资管理', icon: 'Money' },
]

let timer = null
function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  })
}
onMounted(() => { updateTime(); timer = setInterval(updateTime, 1000) })
onUnmounted(() => clearInterval(timer))

function handleLogout() {
  ElMessageBox.confirm('确定退出登录？', '提示', { type: 'warning' }).then(() => {
    removeToken(); removeUser(); router.push('/login')
  }).catch(() => {})
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.aside {
  width: 220px;
  background: linear-gradient(180deg, #0c1445 0%, #1a237e 100%);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 1px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.logo-icon {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
}

.nav {
  flex: 1;
  padding: 12px 10px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px;
  height: 44px;
  color: rgba(255, 255, 255, 0.6);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s;
  margin-bottom: 4px;
  font-size: 14px;
}
.nav-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}
.nav-item.active {
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.3), rgba(103, 194, 58, 0.2));
  color: #fff;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.2);
}

.aside-footer {
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.user-info {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 12px; border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
}
.avatar {
  width: 32px; height: 32px; border-radius: 8px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: bold;
}
.user-detail { flex: 1; }
.user-name { color: #fff; font-size: 13px; font-weight: 500; }
.user-role { color: rgba(255, 255, 255, 0.4); font-size: 11px; }
.logout-btn { color: rgba(255, 255, 255, 0.4); cursor: pointer; }
.logout-btn:hover { color: #f56c6c; }

.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: 56px;
  display: flex; align-items: center; justify-content: space-between;
  background: #fff; border-bottom: 1px solid #f0f0f0;
  padding: 0 24px; flex-shrink: 0;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.header-title { font-size: 17px; font-weight: 600; color: #1a1a1a; }
.header-right { display: flex; align-items: center; gap: 16px; }
.time { color: #999; font-size: 13px; }

.main {
  flex: 1;
  background: #f5f7fa;
  overflow-y: auto;
  padding: 0;
}
</style>
