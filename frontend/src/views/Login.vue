<template>
  <div class="login-container">
    <!-- 背景动态粒子 -->
    <div class="bg-animation">
      <span v-for="i in 20" :key="i" class="circle" :style="circleStyle(i)"></span>
    </div>

    <div class="login-box">
      <div class="login-header">
        <div class="logo-icon">
          <el-icon :size="32"><OfficeBuilding /></el-icon>
        </div>
        <h2>人事管理系统</h2>
        <p>Human Resource Management</p>
      </div>

      <el-form :model="form" :rules="rules" ref="formRef" @keyup.enter="handleLogin" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="form.username" prefix-icon="User" placeholder="请输入用户名" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" prefix-icon="Lock" type="password" placeholder="请输入密码" size="large" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" size="large" class="login-btn">
            {{ loading ? '登录中...' : '登 录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="tips">
        <el-icon><InfoFilled /></el-icon>
        默认账号: admin / admin123
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../api/auth'
import { setToken, setUser } from '../utils/auth'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

function circleStyle(i) {
  const size = Math.random() * 80 + 20
  return {
    width: size + 'px',
    height: size + 'px',
    left: Math.random() * 100 + '%',
    animationDuration: Math.random() * 15 + 10 + 's',
    animationDelay: Math.random() * 5 + 's',
    opacity: Math.random() * 0.3 + 0.05,
  }
}

async function handleLogin() {
  await formRef.value.validate()
  loading.value = true
  try {
    const res = await login(form)
    setToken(res.data.token)
    setUser(res.data.user)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0c1445 0%, #1a237e 40%, #0d47a1 100%);
  position: relative;
  overflow: hidden;
}

/* 动态背景圆圈 */
.bg-animation {
  position: absolute;
  inset: 0;
  overflow: hidden;
}
.circle {
  position: absolute;
  bottom: -150px;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.4), transparent);
  border-radius: 50%;
  animation: floatUp linear infinite;
}
@keyframes floatUp {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-120vh) rotate(720deg);
    opacity: 0;
  }
}

/* 登录卡片 */
.login-box {
  width: 420px;
  padding: 48px 40px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
  z-index: 1;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 36px;
}
.logo-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.4);
  animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 8px 24px rgba(64, 158, 255, 0.4); }
  50% { box-shadow: 0 8px 40px rgba(64, 158, 255, 0.7); }
}

.login-header h2 {
  color: #fff;
  font-size: 26px;
  margin: 0 0 8px;
  letter-spacing: 2px;
}
.login-header p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  margin: 0;
  letter-spacing: 1px;
}

/* 表单样式 */
.login-form :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  border-radius: 10px;
  transition: all 0.3s;
}
.login-form :deep(.el-input__wrapper:hover),
.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(64, 158, 255, 0.6);
  background: rgba(255, 255, 255, 0.1);
}
.login-form :deep(.el-input__inner) {
  color: #fff;
}
.login-form :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.4);
}
.login-form :deep(.el-input__prefix .el-icon) {
  color: rgba(255, 255, 255, 0.4);
}

.login-btn {
  width: 100%;
  height: 44px;
  border-radius: 10px;
  font-size: 16px;
  letter-spacing: 8px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  border: none;
  transition: all 0.3s;
}
.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(64, 158, 255, 0.5);
}

.tips {
  text-align: center;
  color: rgba(255, 255, 255, 0.35);
  font-size: 13px;
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
</style>
