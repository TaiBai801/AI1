<template>
  <div class="app-container">
    <!-- 管理后台登录弹窗 -->
    <AdminLogin v-if="isAdminRoute && !isAdminLoggedIn" @login="handleAdminLogin" />
    
    <el-header class="app-header">
      <div class="header-content">
        <div class="logo">
          <el-icon size="28"><Connection /></el-icon>
          <span>AI联谊匹配</span>
        </div>
        <el-menu
          :default-active="$route.path"
          mode="horizontal"
          router
          class="nav-menu"
          background-color="transparent"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/quiz">开始问卷</el-menu-item>
        </el-menu>
      </div>
    </el-header>
    
    <el-main class="app-main">
      <router-view />
    </el-main>
    
    <el-footer class="app-footer">
      <p>AI联谊匹配系统 © 2024 - 基于MBTI人格理论的智能匹配</p>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import AdminLogin from './components/AdminLogin.vue'

const $route = useRoute()
const isAdminLoggedIn = ref(false)

const isAdminRoute = computed(() => {
  return $route.path === '/admin'
})

const handleAdminLogin = () => {
  isAdminLoggedIn.value = true
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  font-size: 20px;
  font-weight: bold;
}

.nav-menu {
  border-bottom: none;
}

.app-main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background: rgba(0, 0, 0, 0.2);
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  padding: 20px;
}

:deep(.el-menu--horizontal) {
  border-bottom: none;
}

:deep(.el-menu-item) {
  font-size: 16px;
}
</style>
