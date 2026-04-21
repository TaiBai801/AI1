<template>
  <div class="admin-view">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 概览统计 -->
      <el-tab-pane label="概览统计" name="overview">
        <div class="stats-grid">
          <el-card class="stat-card">
            <div class="stat-icon" style="background: #667eea;">
              <el-icon size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats?.total_participants || 0 }}</div>
              <div class="stat-label">总报名人数</div>
            </div>
          </el-card>
          
          <el-card class="stat-card">
            <div class="stat-icon" style="background: #764ba2;">
              <el-icon size="32"><Connection /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats?.matched || 0 }}</div>
              <div class="stat-label">已匹配人数</div>
            </div>
          </el-card>
          
          <el-card class="stat-card">
            <div class="stat-icon" style="background: #f093fb;">
              <el-icon size="32"><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats?.match_rate || 0 }}%</div>
              <div class="stat-label">匹配率</div>
            </div>
          </el-card>
        </div>
        
        <!-- 人格类型分布 -->
        <el-card class="distribution-card">
          <template #header>
            <span>人格类型分布</span>
          </template>
          <div class="personality-distribution">
            <div 
              v-for="(count, type) in stats?.personality_distribution" 
              :key="type"
              class="personality-item"
            >
              <span class="type-name">{{ type }}</span>
              <el-progress 
                :percentage="Math.round((count / stats?.total_participants) * 100)" 
                :stroke-width="20"
                :text-inside="true"
              />
              <span class="type-count">{{ count }}人</span>
            </div>
          </div>
        </el-card>
      </el-tab-pane>
      
      <!-- 参与者管理 -->
      <el-tab-pane label="参与者管理" name="participants">
        <div class="toolbar">
          <el-button type="danger" @click="confirmReset" :disabled="!hasMatches">
            <el-icon><RefreshLeft /></el-icon>
            重置匹配
          </el-button>
          <el-button type="primary" @click="fetchParticipants">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
        
        <el-table :data="participants" stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="姓名" width="100" />
          <el-table-column prop="student_id" label="学号" width="120" />
          <el-table-column prop="gender" label="性别" width="80" />
          <el-table-column prop="personality_type" label="人格类型" width="100">
            <template #default="{ row }">
              <el-tag type="primary" effect="dark">{{ row.personality_type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="interests" label="兴趣标签">
            <template #default="{ row }">
              <el-tag 
                v-for="interest in row.interests.slice(0, 3)" 
                :key="interest"
                size="small"
                effect="plain"
                style="margin-right: 5px;"
              >
                {{ interest }}
              </el-tag>
              <span v-if="row.interests.length > 3">+{{ row.interests.length - 3 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="is_matched" label="匹配状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_matched ? 'success' : 'info'">
                {{ row.is_matched ? '已匹配' : '未匹配' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button size="small" @click="viewDetail(row)">详情</el-button>
              <el-button size="small" type="danger" @click="deleteParticipant(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <!-- 匹配管理 -->
      <el-tab-pane label="匹配管理" name="matching">
        <div class="matching-controls">
          <el-form inline>
            <el-form-item label="匹配模式">
              <el-radio-group v-model="matchMode">
                <el-radio-button label="similar">同好匹配</el-radio-button>
                <el-radio-button label="complementary">互补匹配</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="runMatching" :loading="matchingRunning">
                <el-icon><Magic /></el-icon>
                开始AI匹配
              </el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-divider />
        
        <h4>匹配结果 ({{ matchResults.length }}对)</h4>
        <el-empty v-if="matchResults.length === 0" description="暂无匹配结果" />
        
        <div v-else class="match-results">
          <el-card 
            v-for="(match, index) in matchResults" 
            :key="index"
            class="match-card"
          >
            <div class="match-pair">
              <div class="person-info">
                <el-avatar :size="50" :style="{ background: getAvatarColor(match.person_a.personality_type) }">
                  {{ match.person_a.name[0] }}
                </el-avatar>
                <div class="person-detail">
                  <div class="person-name">{{ match.person_a.name }}</div>
                  <el-tag size="small" type="primary">{{ match.person_a.personality_type }}</el-tag>
                </div>
              </div>
              
              <div class="match-center">
                <el-icon size="32" color="#667eea"><Connection /></el-icon>
                <div class="match-score">{{ match.match_score }}分</div>
              </div>
              
              <div class="person-info">
                <el-avatar :size="50" :style="{ background: getAvatarColor(match.person_b.personality_type) }">
                  {{ match.person_b.name[0] }}
                </el-avatar>
                <div class="person-detail">
                  <div class="person-name">{{ match.person_b.name }}</div>
                  <el-tag size="small" type="primary">{{ match.person_b.personality_type }}</el-tag>
                </div>
              </div>
            </div>
            
            <div class="match-reason" v-if="match.match_reason">
              <el-icon><InfoFilled /></el-icon>
              {{ match.match_reason }}
            </div>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const activeTab = ref('overview')
const stats = ref(null)
const participants = ref([])
const matchResults = ref([])
const matchMode = ref('similar')
const matchingRunning = ref(false)

const hasMatches = computed(() => matchResults.value.length > 0)

const fetchStats = async () => {
  try {
    const { data } = await axios.get('/api/stats')
    stats.value = data
  } catch (error) {
    console.error('获取统计失败:', error)
  }
}

const fetchParticipants = async () => {
  try {
    const { data } = await axios.get('/api/participants')
    participants.value = data.participants
  } catch (error) {
    ElMessage.error('获取参与者列表失败')
  }
}

const fetchMatchResults = async () => {
  try {
    const { data } = await axios.get('/api/matching/results')
    matchResults.value = data.results
  } catch (error) {
    console.error('获取匹配结果失败:', error)
  }
}

const runMatching = async () => {
  matchingRunning.value = true
  try {
    const { data } = await axios.post('/api/matching/run', { mode: matchMode.value })
    matchResults.value = data.matches
    ElMessage.success(`匹配完成！成功匹配 ${data.total_matched} 人`)
    fetchStats()
    fetchParticipants()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '匹配失败')
  } finally {
    matchingRunning.value = false
  }
}

const confirmReset = () => {
  ElMessageBox.confirm(
    '确定要重置所有匹配结果吗？此操作不可恢复！',
    '确认重置',
    { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
  ).then(() => {
    resetMatching()
  })
}

const resetMatching = async () => {
  try {
    await axios.post('/api/matching/reset')
    ElMessage.success('匹配结果已重置')
    fetchStats()
    fetchParticipants()
    fetchMatchResults()
  } catch (error) {
    ElMessage.error('重置失败')
  }
}

const viewDetail = (row) => {
  router.push(`/result/${row.id}`)
}

const deleteParticipant = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除 ${row.name} 吗？`, '确认删除', { type: 'warning' })
    await axios.delete(`/api/participants/${row.id}`)
    ElMessage.success('删除成功')
    fetchParticipants()
    fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const getAvatarColor = (type) => {
  const colors = {
    'ISTJ': '#FF6B6B', 'ISFJ': '#4ECDC4', 'INFJ': '#45B7D1', 'INTJ': '#96CEB4',
    'ISTP': '#FFEAA7', 'ISFP': '#DDA0DD', 'INFP': '#98D8C8', 'INTP': '#F7DC6F',
    'ESTP': '#BB8FCE', 'ESFP': '#85C1E9', 'ENFP': '#F8C471', 'ENTP': '#82E0AA',
    'ESTJ': '#F1948A', 'ESFJ': '#85C1E9', 'ENFJ': '#F7DC6F', 'ENTJ': '#BB8FCE'
  }
  return colors[type] || '#667eea'
}

onMounted(() => {
  fetchStats()
  fetchParticipants()
  fetchMatchResults()
})
</script>

<style scoped>
.admin-view {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 15px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.distribution-card {
  margin-top: 20px;
}

.personality-distribution {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.personality-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.type-name {
  width: 60px;
  font-weight: bold;
  color: #667eea;
}

.type-count {
  width: 50px;
  text-align: right;
  color: #666;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.matching-controls {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.match-results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.match-card {
  background: #f9f9f9;
}

.match-pair {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.person-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.person-detail {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.person-name {
  font-weight: bold;
  color: #333;
}

.match-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.match-score {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
}

.match-reason {
  margin-top: 15px;
  padding: 10px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  color: #666;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
