<template>
  <div class="result-view">
    <el-card v-if="participant" class="result-card">
      <template #header>
        <div class="result-header">
          <h2>你的人格分析报告</h2>
        </div>
      </template>
      
      <div class="personality-section">
        <div class="type-badge">{{ participant.personality_type }}</div>
        <h3 class="type-title">{{ description.title }}</h3>
        <p class="type-traits">
          <el-tag v-for="trait in description.traits" :key="trait" type="primary" effect="dark">
            {{ trait }}
          </el-tag>
        </p>
      </div>
      
      <el-divider />
      
      <div class="dimensions-section">
        <h4>人格维度分析</h4>
        <div class="dimension-bars">
          <div class="dimension-item">
            <div class="dimension-labels">
              <span :class="{ active: dimensionScores['E_I'] >= 0 }">外向 E</span>
              <span :class="{ active: dimensionScores['E_I'] < 0 }">内向 I</span>
            </div>
            <el-progress 
              :percentage="Math.abs(dimensionScores['E_I'] * 100)" 
              :color="dimensionScores['E_I'] >= 0 ? '#667eea' : '#764ba2'"
            />
          </div>
          
          <div class="dimension-item">
            <div class="dimension-labels">
              <span :class="{ active: dimensionScores['S_N'] >= 0 }">实感 S</span>
              <span :class="{ active: dimensionScores['S_N'] < 0 }">直觉 N</span>
            </div>
            <el-progress 
              :percentage="Math.abs(dimensionScores['S_N'] * 100)" 
              :color="dimensionScores['S_N'] >= 0 ? '#667eea' : '#764ba2'"
            />
          </div>
          
          <div class="dimension-item">
            <div class="dimension-labels">
              <span :class="{ active: dimensionScores['T_F'] >= 0 }">思考 T</span>
              <span :class="{ active: dimensionScores['T_F'] < 0 }">情感 F</span>
            </div>
            <el-progress 
              :percentage="Math.abs(dimensionScores['T_F'] * 100)" 
              :color="dimensionScores['T_F'] >= 0 ? '#667eea' : '#764ba2'"
            />
          </div>
          
          <div class="dimension-item">
            <div class="dimension-labels">
              <span :class="{ active: dimensionScores['J_P'] >= 0 }">判断 J</span>
              <span :class="{ active: dimensionScores['J_P'] < 0 }">感知 P</span>
            </div>
            <el-progress 
              :percentage="Math.abs(dimensionScores['J_P'] * 100)" 
              :color="dimensionScores['J_P'] >= 0 ? '#667eea' : '#764ba2'"
            />
          </div>
        </div>
      </div>
      
      <el-divider />
      
      <div class="interests-section">
        <h4>你的兴趣标签</h4>
        <div class="interests-list">
          <el-tag 
            v-for="interest in participant.interests" 
            :key="interest"
            type="success"
            effect="plain"
            size="large"
          >
            {{ interest }}
          </el-tag>
        </div>
      </div>
      
      <el-divider />
      
      <div class="match-section" v-if="participant.is_matched">
        <h4>匹配结果</h4>
        <el-alert
          title="匹配成功！"
          type="success"
          :description="`匹配分数: ${participant.match_score}分`"
          show-icon
        />
      </div>
      
      <div class="match-section" v-else>
        <h4>匹配状态</h4>
        <el-alert
          title="等待匹配中..."
          type="info"
          description="管理员将在活动开始前统一进行匹配"
          show-icon
        />
      </div>
      
      <template #footer>
        <div class="result-footer">
          <el-button @click="$router.push('/')">返回首页</el-button>
          <el-button type="primary" @click="$router.push('/admin')">查看所有结果</el-button>
        </div>
      </template>
    </el-card>
    
    <el-skeleton v-else :rows="10" animated />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const route = useRoute()
const participant = ref(null)
const description = ref({})
const dimensionScores = ref({})

const fetchResult = async () => {
  try {
    const { data } = await axios.get(`/api/participants/${route.params.id}`)
    participant.value = data
    description.value = data.description
    dimensionScores.value = data.dimension_scores
  } catch (error) {
    ElMessage.error('获取结果失败')
  }
}

onMounted(fetchResult)
</script>

<style scoped>
.result-view {
  max-width: 700px;
  margin: 0 auto;
}

.result-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
}

.result-header h2 {
  text-align: center;
  color: #333;
}

.personality-section {
  text-align: center;
  padding: 20px 0;
}

.type-badge {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 32px;
  font-weight: bold;
  margin: 0 auto 20px;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.type-title {
  color: #333;
  margin-bottom: 15px;
}

.type-traits {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.dimensions-section h4,
.interests-section h4,
.match-section h4 {
  color: #333;
  margin-bottom: 20px;
}

.dimension-bars {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dimension-item {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
}

.dimension-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-weight: bold;
  color: #999;
}

.dimension-labels span.active {
  color: #667eea;
}

.interests-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.result-footer {
  display: flex;
  justify-content: center;
  gap: 15px;
}
</style>
