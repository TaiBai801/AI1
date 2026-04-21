<template>
  <div class="home-view">
    <div class="hero-section">
      <h1 class="title">
        <el-icon size="48"><Magic /></el-icon>
        AI智能联谊匹配
      </h1>
      <p class="subtitle">基于MBTI人格理论，找到最契合的TA</p>
      
      <div class="features">
        <div class="feature-card">
          <el-icon size="40" color="#667eea"><DocumentChecked /></el-icon>
          <h3>科学问卷</h3>
          <p>20道精心设计的人格测试题</p>
        </div>
        <div class="feature-card">
          <el-icon size="40" color="#764ba2"><UserFilled /></el-icon>
          <h3>人格分析</h3>
          <p>16种MBTI人格类型精准分类</p>
        </div>
        <div class="feature-card">
          <el-icon size="40" color="#f093fb"><Connection /></el-icon>
          <h3>智能匹配</h3>
          <p>AI算法实现最优两两配对</p>
        </div>
      </div>
      
      <div class="actions">
        <el-button type="primary" size="large" @click="$router.push('/quiz')">
          <el-icon><Edit /></el-icon>
          开始问卷
        </el-button>
        <el-button size="large" @click="$router.push('/admin')">
          <el-icon><Setting /></el-icon>
          管理后台
        </el-button>
      </div>
      
      <div class="stats-section" v-if="stats">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-number">{{ stats.total_participants }}</div>
              <div class="stat-label">已报名</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-number">{{ stats.matched }}</div>
              <div class="stat-label">已匹配</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-number">{{ stats.match_rate }}%</div>
              <div class="stat-label">匹配率</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
    
    <div class="how-it-works">
      <h2>如何进行匹配？</h2>
      <el-steps :active="4" simple>
        <el-step title="填写问卷" icon="Edit" />
        <el-step title="人格分析" icon="DataAnalysis" />
        <el-step title="AI匹配" icon="Cpu" />
        <el-step title="查看结果" icon="View" />
      </el-steps>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = ref(null)

const fetchStats = async () => {
  try {
    const { data } = await axios.get('/api/stats')
    stats.value = data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(fetchStats)
</script>

<style scoped>
.home-view {
  color: white;
}

.hero-section {
  text-align: center;
  padding: 40px 0;
}

.title {
  font-size: 48px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 50px;
}

.features {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 50px;
  flex-wrap: wrap;
}

.feature-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  width: 250px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  margin: 15px 0 10px;
  font-size: 20px;
}

.feature-card p {
  opacity: 0.8;
  font-size: 14px;
}

.actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 50px;
}

.actions .el-button {
  padding: 15px 40px;
  font-size: 18px;
  border-radius: 30px;
}

.stats-section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  max-width: 600px;
  margin: 0 auto;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #ffd04b;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
  margin-top: 5px;
}

.how-it-works {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 40px;
  margin-top: 40px;
}

.how-it-works h2 {
  text-align: center;
  margin-bottom: 30px;
}

:deep(.el-step__title) {
  color: white;
  font-size: 14px;
}

:deep(.el-step__icon) {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

:deep(.el-step__line) {
  background: rgba(255, 255, 255, 0.3);
}
</style>
