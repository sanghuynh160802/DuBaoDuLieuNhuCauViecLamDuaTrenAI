<template>
  <div class="skills-management-container">
    <div class="header-bar">
      <h2>User Skills</h2>
      <el-button class="btn-create" @click="showCreatePopup = true" type="primary">
        Thêm kỹ năng
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="userSkills"
      stripe
      style="width: 100%"
      :empty-text="loading ? 'Đang tải...' : 'Không có kỹ năng nào'"
    >
      <el-table-column prop="skill" label="Kỹ năng" min-width="180" />
      <el-table-column prop="level" label="Trình độ" min-width="120" />
      <el-table-column prop="experience" label="Kinh nghiệm" min-width="150" />
      <el-table-column prop="work_way" label="Hình thức làm việc" min-width="150" />
      <el-table-column prop="city" label="Thành phố" min-width="120" />
    </el-table>

    <!-- Popup User Skill Component -->
    <popup-user-skill
      v-if="showCreatePopup"
      @close="onPopupClose"
      @saved="onPopupSaved"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getUserSkillsByUserId } from '@/services/user.service'
import PopupUserSkill from '@/views/popup/popupUserSkill.vue'

const userSkills = ref<Array<any>>([])
const loading = ref(false)
const showCreatePopup = ref(false)

const authStore = useAuthStore()
const userId = ref<string | null>(null)

const fetchUserSkills = async () => {
  if (!userId.value) {
    console.warn('[Debug] No userId available, skipping fetchUserSkills')
    return
  }
  loading.value = true
  try {
    console.log('[Debug] Fetching skills for userId:', userId.value)
    const response = await getUserSkillsByUserId(userId.value)
    userSkills.value = response.data || []
    console.log(`[Debug] User skills fetched: ${userSkills.value.length} items`)
  } catch (error) {
    console.error('Failed to fetch user skills:', error)
  } finally {
    loading.value = false
  }
}

// Watch for user ID changes to refetch skills
watch(
  () => authStore.getUserID(),
  (newUserId) => {
    userId.value = newUserId
    console.log('[Debug] User ID updated:', userId.value)
    if (userId.value) {
      fetchUserSkills()
    } else {
      userSkills.value = []
    }
  },
  { immediate: true }
)

const onPopupClose = () => {
  showCreatePopup.value = false;
};

const onPopupSaved = () => {
  showCreatePopup.value = false
  fetchUserSkills()
}

onMounted(() => {
  userId.value = authStore.getUserID()
  console.log('[Debug] Mounted: userId =', userId.value)
  if (userId.value) {
    fetchUserSkills()
  }
})
</script>

<style scoped lang="scss">
.skills-management-container {
  padding: 24px;
  background-color: #f5f7fa; /* light background */

  .header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-weight: 700;
      font-size: 24px;
      color: #003366; /* dark blue header color */
    }

    .btn-create {
      font-weight: 600;
      font-size: 14px;
      padding: 10px 20px;
      border-radius: 8px;
      background: linear-gradient(135deg, #00f0ff, #007cf0, #6a00ff);
      color: white;
      border: none;
      cursor: pointer;
      transition: background-position 0.3s ease;

      &:hover {
        background-position: right center;
      }
    }
  }

  /* Table overrides if needed */
  ::v-deep .el-table {
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
  }
}
</style>