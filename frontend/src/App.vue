<template>
  <div class="min-h-screen grid-bg relative overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-br from-dark-bg via-dark-bg/90 to-dark-bg pointer-events-none"></div>
    
    <div class="absolute top-0 left-0 w-96 h-96 bg-neon-blue/10 rounded-full blur-3xl animate-pulse-slow"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 bg-neon-purple/10 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 1.5s;"></div>
    
    <div class="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
      <header class="text-center mb-12">
        <div class="inline-flex items-center gap-3 mb-4">
          <div class="w-3 h-3 rounded-full bg-neon-blue animate-pulse"></div>
          <span class="text-neon-blue text-sm tracking-widest uppercase">Avatar Generator</span>
          <div class="w-3 h-3 rounded-full bg-neon-purple animate-pulse" style="animation-delay: 0.5s;"></div>
        </div>
        <h1 class="text-5xl md:text-6xl font-black mb-4">
          <span class="bg-gradient-to-r from-neon-blue via-neon-purple to-neon-pink bg-clip-text text-transparent">
            头像生成器
          </span>
        </h1>
        <p class="text-gray-400 text-lg max-w-2xl mx-auto">
          选择你的性格标签与风格偏好，让智能系统为你生成独一无二的专属头像
        </p>
      </header>

      <div class="grid lg:grid-cols-2 gap-8">
        <div class="space-y-8">
          <div class="glass-card rounded-2xl p-6">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-10 h-10 rounded-lg bg-neon-blue/20 flex items-center justify-center">
                <svg class="w-5 h-5 text-neon-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                </svg>
              </div>
              <div>
                <h2 class="text-xl font-bold text-white">性格标签</h2>
                <p class="text-sm text-gray-400">选择最能代表你的性格特质（可选多个）</p>
              </div>
            </div>
            <div class="flex flex-wrap gap-3">
              <button
                v-for="tag in personalityTags"
                :key="tag.id"
                @click="togglePersonalityTag(tag.id)"
                :class="['tag-button', { 'tag-button-selected': selectedPersonality.includes(tag.id) }]"
              >
                {{ tag.label }}
              </button>
            </div>
            <div class="mt-4 flex items-center gap-2 text-sm text-gray-500">
              <span>已选择: </span>
              <span class="text-neon-blue">{{ selectedPersonality.length }}</span>
              <span> 个标签</span>
            </div>
          </div>

          <div class="glass-card rounded-2xl p-6">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-10 h-10 rounded-lg bg-neon-purple/20 flex items-center justify-center">
                <svg class="w-5 h-5 text-neon-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
                </svg>
              </div>
              <div>
                <h2 class="text-xl font-bold text-white">风格标签</h2>
                <p class="text-sm text-gray-400">选择你喜欢的视觉风格（可选多个）</p>
              </div>
            </div>
            <div class="flex flex-wrap gap-3">
              <button
                v-for="tag in styleTags"
                :key="tag.id"
                @click="toggleStyleTag(tag.id)"
                :class="['tag-button', { 'tag-button-selected': selectedStyle.includes(tag.id) }]"
              >
                {{ tag.label }}
              </button>
            </div>
            <div class="mt-4 flex items-center gap-2 text-sm text-gray-500">
              <span>已选择: </span>
              <span class="text-neon-purple">{{ selectedStyle.length }}</span>
              <span> 个标签</span>
            </div>
          </div>

          <button
            @click="generateAvatar"
            :disabled="isGenerating || canGenerate"
            class="primary-button w-full flex items-center justify-center gap-3"
          >
            <template v-if="isGenerating">
              <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>正在生成中... {{ progress }}%</span>
            </template>
            <template v-else>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              <span>生成头像</span>
            </template>
          </button>

          <div v-if="errorMessage" class="glass-card rounded-xl p-4 border border-red-500/50 bg-red-500/10">
            <div class="flex items-center gap-3">
              <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="text-red-400 text-sm">{{ errorMessage }}</p>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="glass-card rounded-2xl p-6">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-neon-pink/20 flex items-center justify-center">
                  <svg class="w-5 h-5 text-neon-pink" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <h2 class="text-xl font-bold text-white">预览区</h2>
                  <p class="text-sm text-gray-400">生成后的头像将显示在这里</p>
                </div>
              </div>
              <div v-if="generatedImage" class="flex gap-2">
                <button
                  @click="showPreview = true"
                  class="px-4 py-2 rounded-lg bg-dark-card border border-dark-border text-gray-300 text-sm hover:border-neon-blue hover:text-neon-blue transition-all"
                >
                  预览
                </button>
                <button
                  @click="downloadImage"
                  class="px-4 py-2 rounded-lg bg-dark-card border border-dark-border text-gray-300 text-sm hover:border-neon-blue hover:text-neon-blue transition-all"
                >
                  下载
                </button>
              </div>
            </div>

            <div class="relative aspect-square rounded-xl overflow-hidden bg-dark-card border-2 border-dark-border">
              <div v-if="!generatedImage && !isGenerating" class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="w-24 h-24 rounded-full bg-dark-border flex items-center justify-center mb-4">
                  <svg class="w-12 h-12 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <p class="text-gray-500 text-center">选择标签后点击生成</p>
                <p class="text-gray-600 text-sm text-center mt-2">你的专属头像即将诞生</p>
              </div>

              <div v-if="isGenerating" class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="relative w-32 h-32 mb-6">
                  <div class="absolute inset-0 rounded-full border-4 border-dark-border"></div>
                  <div class="absolute inset-0 rounded-full border-4 border-transparent border-t-neon-blue animate-spin"></div>
                  <div class="absolute inset-4 rounded-full border-4 border-transparent border-t-neon-purple animate-spin" style="animation-direction: reverse; animation-duration: 1.5s;"></div>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-2xl font-bold text-white">{{ progress }}%</span>
                  </div>
                </div>
                <p class="text-gray-400">正在渲染你的专属头像...</p>
                <p class="text-gray-600 text-sm mt-2">AI 正在根据你的选择进行创作</p>
              </div>

              <img
                v-if="generatedImage"
                :src="generatedImage"
                alt="Generated Avatar"
                class="w-full h-full object-cover animate-float"
              />
            </div>
          </div>

          <div class="glass-card rounded-2xl p-6">
            <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-neon-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              使用提示
            </h3>
            <ul class="space-y-3">
              <li class="flex items-start gap-3 text-sm text-gray-400">
                <div class="w-6 h-6 rounded-full bg-neon-blue/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span class="text-neon-blue text-xs font-bold">1</span>
                </div>
                <span>选择至少一个性格标签和一个风格标签</span>
              </li>
              <li class="flex items-start gap-3 text-sm text-gray-400">
                <div class="w-6 h-6 rounded-full bg-neon-purple/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span class="text-neon-purple text-xs font-bold">2</span>
                </div>
                <span>点击"生成头像"按钮开始创作</span>
              </li>
              <li class="flex items-start gap-3 text-sm text-gray-400">
                <div class="w-6 h-6 rounded-full bg-neon-pink/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span class="text-neon-pink text-xs font-bold">3</span>
                </div>
                <span>生成完成后可预览并下载高清图片</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <footer class="mt-16 text-center">
        <div class="flex items-center justify-center gap-2 text-gray-600 text-sm">
          <div class="w-2 h-2 rounded-full bg-neon-blue animate-pulse"></div>
          <span>Powered by 通义万象</span>
          <div class="w-2 h-2 rounded-full bg-neon-purple animate-pulse" style="animation-delay: 0.3s;"></div>
        </div>
      </footer>
    </div>

    <div v-if="showPreview && generatedImage" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="showPreview = false"></div>
      <div class="relative max-w-3xl max-h-[90vh]">
        <button
          @click="showPreview = false"
          class="absolute -top-12 right-0 text-white hover:text-neon-blue transition-colors"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
        <img
          :src="generatedImage"
          alt="Preview"
          class="max-w-full max-h-[80vh] rounded-xl shadow-2xl"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const personalityTags = ref([])
const styleTags = ref([])
const selectedPersonality = ref([])
const selectedStyle = ref([])
const isGenerating = ref(false)
const generatedImage = ref(null)
const progress = ref(0)
const errorMessage = ref(null)
const showPreview = ref(false)

const canGenerate = computed(() => {
  return selectedPersonality.value.length === 0 || selectedStyle.value.length === 0
})

const togglePersonalityTag = (id) => {
  const index = selectedPersonality.value.indexOf(id)
  if (index > -1) {
    selectedPersonality.value.splice(index, 1)
  } else {
    selectedPersonality.value.push(id)
  }
}

const toggleStyleTag = (id) => {
  const index = selectedStyle.value.indexOf(id)
  if (index > -1) {
    selectedStyle.value.splice(index, 1)
  } else {
    selectedStyle.value.push(id)
  }
}

const fetchTags = async () => {
  try {
    const [personalityRes, styleRes] = await Promise.all([
      axios.get('/api/tags/personality'),
      axios.get('/api/tags/style'),
    ])
    personalityTags.value = personalityRes.data
    styleTags.value = styleRes.data
  } catch (error) {
    console.error('获取标签失败:', error)
    errorMessage.value = '获取标签数据失败，请刷新页面重试'
  }
}

const generateAvatar = async () => {
  if (canGenerate.value) return

  isGenerating.value = true
  errorMessage.value = null
  generatedImage.value = null
  progress.value = 0

  try {
    const response = await axios.post('/api/generate', {
      personality_tags: selectedPersonality.value,
      style_tags: selectedStyle.value,
    })

    const taskId = response.data.task_id
    
    let pollCount = 0
    const maxPolls = 60

    const pollTask = async () => {
      if (pollCount >= maxPolls) {
        errorMessage.value = '生成超时，请重试'
        isGenerating.value = false
        return
      }

      pollCount++
      progress.value = Math.min(Math.floor((pollCount / maxPolls) * 100), 95)

      try {
        const taskRes = await axios.get(`/api/task/${taskId}`)
        const status = taskRes.data.status

        if (status === 'succeeded') {
          generatedImage.value = taskRes.data.image_url
          progress.value = 100
          isGenerating.value = false
        } else if (status === 'failed') {
          errorMessage.value = taskRes.data.error || '生成失败，请重试'
          isGenerating.value = false
        } else {
          setTimeout(pollTask, 2000)
        }
      } catch (error) {
        setTimeout(pollTask, 2000)
      }
    }

    setTimeout(pollTask, 2000)

  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '生成失败，请重试'
    isGenerating.value = false
  }
}

const downloadImage = async () => {
  if (!generatedImage.value) return

  try {
    const response = await axios.get(generatedImage.value, {
      responseType: 'blob',
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `avatar-${Date.now()}.png`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    window.open(generatedImage.value, '_blank')
  }
}

onMounted(() => {
  fetchTags()
})
</script>
