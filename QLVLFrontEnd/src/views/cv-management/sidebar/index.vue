<template>
  <div class="p-6 space-y-8">
    <div>
      <h3 class="text-xl font-bold mb-4">🔎 Bộ lọc ứng viên</h3>

      <div class="space-y-4">
        <div class="space-y-1">
          <label class="text-sm font-medium">Kỹ năng</label>
          <input v-model="localFilter.skill" type="text" placeholder="VD: Java, React..." class="filter-input" />
        </div>

        <div class="space-y-1">
          <label class="text-sm font-medium">Kinh nghiệm</label>
          <input v-model="localFilter.experience" type="text" placeholder="VD: 2 năm, 5 năm..." class="filter-input" />
        </div>

        <div class="space-y-1">
          <label class="text-sm font-medium">Vị trí</label>
          <input v-model="localFilter.position" type="text" placeholder="VD: Lập trình viên" class="filter-input" />
        </div>

        <div class="space-y-1">
          <label class="text-sm font-medium">Khu vực</label>
          <input v-model="localFilter.location" type="text" placeholder="VD: Hà Nội, TP.HCM" class="filter-input" />
        </div>

        <div class="flex gap-2 mt-4">
          <button class="btn-primary w-1/2" @click="applyFilter">Áp dụng</button>
          <button class="btn-secondary w-1/2" @click="resetFilter">Xóa lọc</button>
        </div>
      </div>
    </div>

    <div class="space-y-3">
      <div v-if="cvs.length === 0" class="text-center text-gray-400 text-sm">
        Không có ứng viên phù hợp.
      </div>
      <div
        v-else
        v-for="cv in cvs"
        :key="cv.id"
        class="cv-card"
        :class="{ 'bg-blue-50': selectedCV?.id === cv.id }"
        @click="$emit('selectCV', cv)"
      >
        <div class="flex justify-between items-center">
          <h4 class="font-semibold truncate w-2/3">{{ cv.title }}</h4>
          <span v-if="cv.status === 'Approved'" class="badge">⭐</span>
        </div>
        <div class="text-xs text-gray-500 truncate">{{ cv.position || 'Chưa rõ vị trí' }} • {{ cv.location || 'Không rõ khu vực' }}</div>
        <p class="text-sm text-gray-600 truncate">{{ cv.applicant_email }}</p>
        <p class="text-xs text-gray-400">{{ formatDate(cv.submitted_at) }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'Sidebar',
  props: {
    cvs: {
      type: Array,
      default: () => []
    },
    selectedCV: {
      type: Object,
      default: null
    }
  },
  emits: ['selectCV', 'updateFilter'],
  setup(_, { emit }) {
    const localFilter = ref({
      skill: '',
      experience: '',
      location: '',
      position: ''
    })

    const applyFilter = () => {
      emit('updateFilter', { ...localFilter.value })
    }

    const resetFilter = () => {
      localFilter.value = { skill: '', experience: '', location: '', position: '' }
      emit('updateFilter', { ...localFilter.value })
    }

    const formatDate = (dateStr: string) => {
      return new Date(dateStr).toLocaleDateString('vi-VN')
    }

    return {
      localFilter,
      applyFilter,
      resetFilter,
      formatDate
    }
  }
})
</script>

<style scoped>
/* Input styling */
.filter-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: #f9fafb;
}

/* Buttons */
.btn-primary {
  background: #3b82f6;
  color: white;
  font-weight: 600;
  padding: 10px;
  border-radius: 8px;
  transition: 0.2s;
}
.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
  font-weight: 600;
  padding: 10px;
  border-radius: 8px;
  transition: 0.2s;
}
.btn-secondary:hover {
  background: #d1d5db;
}

/* CV Card */
.cv-card {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px;
  background: white;
  cursor: pointer;
  transition: background 0.2s;
}
.cv-card:hover {
  background: #f0f9ff;
}

/* Badge */
.badge {
  background-color: #fde68a;
  color: #92400e;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: bold;
}
</style>
