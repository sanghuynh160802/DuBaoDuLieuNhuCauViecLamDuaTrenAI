<template>
  <div class="job-card-container">
    <div class="job-card" @click="toJobDetail(job?.id)">
      <div class="company-logo">
        <img :src="job.Source_Picture" alt="Company Logo" />
      </div>
      
      <div class="job-info">
        <div class="job-header">
          <h3 class="job-title">{{ job?.Title || "No Title" }}</h3>
          <div class="save-icon" @click.stop="toggleSaveJob">
            <el-icon :class="{ saved: isSaved }"><Star /></el-icon>
          </div>
        </div>
        
        <p class="company-name">{{ job?.Company_Name || "No Company" }}</p>
        
        <div class="job-meta">
          <span class="salary">{{ job?.Salary || "Thỏa thuận" }}</span>
          <span class="separator" v-if="job.Salary && (job.Level || job.Place)">•</span>
          <span class="job-level" v-if="job.Level">{{ job.Level }}</span>
        </div>
        
        <div class="job-meta location-workway">
          <span class="job-location" v-if="job.Place">
            <el-icon><Location /></el-icon>
            {{ job.Place }}
          </span>
          <span class="job-type" v-if="job.Work_Way">
            <el-icon><OfficeBuilding /></el-icon>
            {{ job.Work_Way }}
          </span>
        </div>
        
        <hr class="divider" />
        
        <div class="job-tags" v-if="job.Profession">
          <span 
            class="job-tag" 
            v-for="tag in job.Profession.split(',')" 
            :key="tag.trim()"
          >
            {{ tag.trim() }}
          </span>
        </div>
        
        <div class="posted-time">
          {{ formatPostedTime(job?.Time) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Star, Location, OfficeBuilding } from '@element-plus/icons-vue'
import { savePost, deleteSavedPostByPostId, getSavedPostsByUserId } from '@/services/user.service'
import { useAuthStore } from '@/stores/auth'
import { ref, onMounted, computed } from 'vue'

const props = defineProps({
  job: {
    type: Object,
    required: true,
  }
})

const router = useRouter()
const authStore = useAuthStore()

// Lưu danh sách post_id đã lưu
const savedPostIds = ref<string[]>([])

// isSaved là computed dựa trên savedPostIds và props.job.id
const isSaved = computed(() => {
  if (!props.job || !props.job.id) return false
  // So sánh string để tránh sai lệch kiểu
  return savedPostIds.value.includes(String(props.job.id))
})

// Lấy danh sách saved posts khi component mounted
onMounted(async () => {
  await fetchSavedPosts()
})

const fetchSavedPosts = async () => {
  try {
    const userId = authStore.getUserID()
    if (!userId) {
      savedPostIds.value = []
      return
    }
    const response = await getSavedPostsByUserId(userId)
    if (response.data && Array.isArray(response.data)) {
      console.log("Saved Post IDs:", response.data.map(post => post.post_id))
      savedPostIds.value = response.data.map(post => String(post.post_id))
    } else {
      savedPostIds.value = []
    }
  } catch (error) {
    console.error('Error fetching saved posts:', error)
    savedPostIds.value = []
  }
}

const toggleSaveJob = async () => {
  try {
    const userId = authStore.getUserID()
    if (!userId) return

    if (!props.job || !props.job.id) return

    if (isSaved.value) {
      // Unsave
      await deleteSavedPostByPostId(props.job.id)
      savedPostIds.value = savedPostIds.value.filter(id => id !== String(props.job.id))
    } else {
      // Save
      await savePost({
        user_id: userId,
        post_id: props.job.id
      })
      savedPostIds.value.push(String(props.job.id))
    }
  } catch (error) {
    console.error('Error toggling save:', error)
  }
}

const toJobDetail = (id: string) => {
  if (!id) return
  router.push(`/mainjob/${id}`)
}

const formatPostedTime = (time: string) => {
  if (!time) return 'Không rõ thời gian'
  return `Đăng ${time}`
}
</script>

<style scoped>
.job-card-container {
  padding: 4px 12px;
  max-width: 1100px;
  margin: 0 auto;
}

.job-card {
  display: flex;
  gap: 24px;
  background-color: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 6px rgb(0 0 0 / 0.08);
  padding: 12px 20px;
  cursor: pointer;
  transition: box-shadow 0.25s ease, background-color 0.25s ease, transform 0.2s ease;
  border: 1px solid #e7e7e7;
  width: 100%;
  box-sizing: border-box;
  min-height: 80px;
}

.job-card:hover {
  background-color: #e8f0fe;
  box-shadow: 0 8px 20px rgb(0 0 0 / 0.14);
  transform: translateY(-3px);
}

.company-logo {
  flex-shrink: 0;
  width: 86px;
  height: 86px;
  border-radius: 12px;
  background-color: #f9fafb;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.company-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.job-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4px;
}

.job-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1.2;
  max-width: calc(100% - 32px);
  overflow-wrap: break-word;
}

.save-icon {
  color: #9ca3af;
  cursor: pointer;
  font-size: 24px;
  transition: all 0.2s ease;
}
.save-icon:hover {
  color: #2563eb;
}
.save-icon .saved {
  color: #f59e0b;
  font-weight: bold;
}

.company-name {
  font-size: 15px;
  color: #4b5563;
  margin: 2px 0 8px 0;
}

.job-meta {
  font-size: 14px;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 4px;
}

.salary {
  color: #dc2626;
  font-weight: 600;
}

.job-level {
  white-space: nowrap;
}

.location-workway {
  margin-bottom: 8px;
}

.job-location,
.job-type {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #4b5563;
  font-size: 14px;
}

.el-icon {
  font-size: 16px;
  color: #6b7280;
}

.divider {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 0 0 8px 0;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.job-tag {
  font-size: 12px;
  color: #2563eb;
  background-color: #dbeafe;
  border: 1px solid #93c5fd;
  padding: 4px 10px;
  border-radius: 8px;
  user-select: none;
  white-space: nowrap;
}

.posted-time {
  font-size: 12px;
  color: #6b7280;
  text-align: right;
  margin-top: auto;
  align-self: flex-end;
}

/* Responsive */
@media (max-width: 768px) {
  .job-card {
    flex-direction: column;
    padding: 10px 14px;
  }
  .company-logo {
    width: 64px;
    height: 64px;
  }
  .job-title {
    font-size: 16px;
  }
  .company-name {
    font-size: 13px;
  }
  .job-meta,
  .job-location,
  .job-type {
    font-size: 13px;
  }
  .job-tag {
    font-size: 11px;
    padding: 4px 8px;
  }
  .posted-time {
    font-size: 11px;
  }
}
</style>