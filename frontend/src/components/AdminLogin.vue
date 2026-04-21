<template>
  <div class="login-overlay">
    <el-card class="login-card">
      <template #header>
        <h3>管理后台登录</h3>
      </template>
      <el-form @submit.prevent="handleLogin">
        <el-form-item>
          <el-input
            v-model="password"
            type="password"
            placeholder="请输入管理密码"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button type="primary" size="large" @click="handleLogin" style="width: 100%">
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const password = ref('')
const emit = defineEmits(['login'])

const handleLogin = () => {
  if (password.value === 'qsxcyy33') {
    emit('login')
  } else {
    ElMessage.error('密码错误')
    password.value = ''
  }
}
</script>

<style scoped>
.login-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.login-card {
  width: 350px;
}

.login-card h3 {
  text-align: center;
  margin: 0;
}
</style>
