<template>
  <div class="quiz-view">
    <el-card class="quiz-card" v-if="!showResult">
      <template #header>
        <div class="card-header">
          <h2>人格匹配问卷</h2>
          <el-steps :active="currentStep" finish-status="success" simple>
            <el-step title="基本信息" />
            <el-step title="人格测试" />
            <el-step title="兴趣标签" />
          </el-steps>
        </div>
      </template>
      
      <!-- 步骤1: 基本信息 -->
      <div v-if="currentStep === 0" class="step-content">
        <el-form :model="form" label-position="top" :rules="basicRules" ref="basicForm">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="form.name" placeholder="请输入你的姓名" size="large" />
          </el-form-item>
          <el-form-item label="学号/编号" prop="studentId">
            <el-input v-model="form.studentId" placeholder="请输入学号或编号" size="large" />
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="form.gender" size="large">
              <el-radio-button label="男">男</el-radio-button>
              <el-radio-button label="女">女</el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 步骤2: 人格测试 -->
      <div v-if="currentStep === 1" class="step-content">
        <div class="progress-bar">
          <span>题目 {{ currentQuestionIndex + 1 }} / {{ questions.length }}</span>
          <el-progress :percentage="progressPercent" />
        </div>
        
        <div class="question-box" v-if="currentQuestion">
          <h3 class="question-text">{{ currentQuestion.text }}</h3>
          <div class="options">
            <el-radio-group v-model="answers[currentQuestion.id]" size="large">
              <el-radio-button :label="'A'">
                <div class="option-content">
                  <span class="option-label">A</span>
                  <span class="option-text">{{ currentQuestion.optionA.text }}</span>
                </div>
              </el-radio-button>
              <el-radio-button :label="'B'">
                <div class="option-content">
                  <span class="option-label">B</span>
                  <span class="option-text">{{ currentQuestion.optionB.text }}</span>
                </div>
              </el-radio-button>
            </el-radio-group>
          </div>
        </div>
        
        <div class="question-nav">
          <el-button 
            @click="prevQuestion" 
            :disabled="currentQuestionIndex === 0"
          >
            上一题
          </el-button>
          <el-button 
            type="primary" 
            @click="nextQuestion"
            :disabled="!answers[currentQuestion?.id]"
          >
            {{ currentQuestionIndex === questions.length - 1 ? '完成' : '下一题' }}
          </el-button>
        </div>
      </div>
      
      <!-- 步骤3: 兴趣标签 -->
      <div v-if="currentStep === 2" class="step-content">
        <h3>选择你的兴趣标签（多选）</h3>
        <p class="hint">选择你感兴趣的活动，这将帮助系统为你找到志同道合的伙伴</p>
        
        <div class="interests-grid">
          <el-check-tag
            v-for="interest in availableInterests"
            :key="interest"
            :checked="form.interests.includes(interest)"
            @change="toggleInterest(interest)"
            size="large"
            class="interest-tag"
          >
            {{ interest }}
          </el-check-tag>
        </div>
        
        <div class="selected-count">
          已选择 {{ form.interests.length }} 个标签
        </div>
      </div>
      
      <template #footer>
        <div class="card-footer">
          <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
          <el-button 
            v-if="currentStep < 2" 
            type="primary" 
            @click="nextStep"
            :disabled="!canProceed"
          >
            下一步
          </el-button>
          <el-button 
            v-if="currentStep === 2" 
            type="success" 
            @click="submitQuiz"
            :loading="submitting"
            :disabled="form.interests.length === 0"
          >
            提交问卷
          </el-button>
        </div>
      </template>
    </el-card>
    
    <!-- 提交成功 -->
    <el-result
      v-else
      icon="success"
      title="问卷提交成功！"
      :sub-title="`你的人格类型是：${resultPersonality}`"
    >
      <template #extra>
        <el-button type="primary" @click="viewResult">查看详细结果</el-button>
        <el-button @click="resetQuiz">再填一份</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const currentStep = ref(0)
const currentQuestionIndex = ref(0)
const questions = ref([])
const availableInterests = ref([])
const answers = ref({})
const submitting = ref(false)
const showResult = ref(false)
const resultPersonality = ref('')
const resultId = ref(null)
const basicForm = ref(null)

const form = ref({
  name: '',
  studentId: '',
  gender: '',
  interests: []
})

const basicRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  studentId: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
}

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value]
})

const progressPercent = computed(() => {
  return Math.round(((currentQuestionIndex.value + 1) / questions.value.length) * 100)
})

const canProceed = computed(() => {
  if (currentStep.value === 0) {
    return form.value.name && form.value.studentId
  }
  if (currentStep.value === 1) {
    return Object.keys(answers.value).length === questions.value.length
  }
  return true
})

const fetchQuestions = async () => {
  try {
    const { data } = await axios.get('/api/quiz/questions')
    questions.value = data.questions
  } catch (error) {
    ElMessage.error('获取问卷题目失败')
  }
}

const fetchInterests = async () => {
  try {
    const { data } = await axios.get('/api/interests')
    availableInterests.value = data.interests
  } catch (error) {
    ElMessage.error('获取兴趣标签失败')
  }
}

const toggleInterest = (interest) => {
  const index = form.value.interests.indexOf(interest)
  if (index > -1) {
    form.value.interests.splice(index, 1)
  } else {
    form.value.interests.push(interest)
  }
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
  } else {
    currentStep.value = 2
  }
}

const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const nextStep = async () => {
  if (currentStep.value === 0) {
    await basicForm.value.validate((valid) => {
      if (valid) currentStep.value++
    })
  } else {
    currentStep.value++
  }
}

const prevStep = () => {
  currentStep.value--
}

const submitQuiz = async () => {
  submitting.value = true
  try {
    const quizAnswers = Object.entries(answers.value).map(([id, answer]) => ({
      question_id: parseInt(id),
      answer
    }))
    
    const { data } = await axios.post('/api/participants', {
      name: form.value.name,
      student_id: form.value.studentId,
      gender: form.value.gender,
      quiz_answers: quizAnswers,
      interests: form.value.interests
    })
    
    resultPersonality.value = data.personality_type
    resultId.value = data.id
    showResult.value = true
    ElMessage.success('问卷提交成功！')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '提交失败')
  } finally {
    submitting.value = false
  }
}

const viewResult = () => {
  router.push(`/result/${resultId.value}`)
}

const resetQuiz = () => {
  currentStep.value = 0
  currentQuestionIndex.value = 0
  answers.value = {}
  form.value = { name: '', studentId: '', gender: '', interests: [] }
  showResult.value = false
}

onMounted(() => {
  fetchQuestions()
  fetchInterests()
})
</script>

<style scoped>
.quiz-view {
  max-width: 800px;
  margin: 0 auto;
}

.quiz-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
}

.card-header h2 {
  margin-bottom: 20px;
  color: #333;
}

.step-content {
  padding: 20px 0;
}

.progress-bar {
  margin-bottom: 30px;
}

.progress-bar span {
  color: #666;
  font-size: 14px;
}

.question-box {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
}

.question-text {
  font-size: 20px;
  color: #333;
  margin-bottom: 30px;
  line-height: 1.6;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.options :deep(.el-radio-button__inner) {
  width: 100%;
  text-align: left;
  padding: 20px;
  height: auto;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.option-label {
  width: 32px;
  height: 32px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.option-text {
  font-size: 16px;
  line-height: 1.5;
}

.question-nav {
  display: flex;
  justify-content: space-between;
}

.hint {
  color: #666;
  margin-bottom: 20px;
}

.interests-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 20px 0;
}

.interest-tag {
  padding: 10px 20px;
  font-size: 14px;
}

.interest-tag.is-checked {
  background: #667eea;
  color: white;
}

.selected-count {
  text-align: center;
  color: #667eea;
  font-weight: bold;
  margin-top: 20px;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
