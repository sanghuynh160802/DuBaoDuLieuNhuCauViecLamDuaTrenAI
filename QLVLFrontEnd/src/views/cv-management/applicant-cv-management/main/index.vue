<template>
  <div class="cv-main-content">
    <!-- Search Section -->
    <div class="search-section">
      <div class="search-left">
        <h1>CV của bạn</h1>
        <div class="input-search">
          <el-icon class="icon-search"><Search /></el-icon>
          <input
            type="text"
            v-model="keySearch"
            placeholder="Tìm kiếm theo vị trí, công ty..."
          />
        </div>
      </div>
    </div>

    <div class="cv-review-content">
      <!-- Loading -->
      <div v-if="loading" class="loading-state text-center text-gray-400 text-lg font-medium py-20">
        Đang tải dữ liệu...
      </div>

      <!-- CV List -->
      <template v-else-if="!selectedCV && filteredCVs.length">
        <div
          v-for="cv in paginatedCVs"
          :key="cv.id"
          :class="['cv-card', { 'cv-card-selected': selectedCV?.id === cv.id }]"
          @click="selectCV(cv)"
        >
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-lg font-semibold truncate">{{ cv.title || 'Không có tiêu đề' }}</h3>
            <span :class="['status-badge', statusClass(cv.status)]">{{ cv.status }}</span>
          </div>
          <p class="text-gray-700 truncate">{{ cv.company_name }}</p>
          <p class="text-sm text-gray-500 mt-1 truncate">
            {{ selectedJob?.Level || 'Chưa xác định' }} • {{ formatDate(cv.updated_at) }}
          </p>
        </div>
      </template>

      <!-- CV Details -->
      <template v-else-if="selectedCV">
        <button @click="selectedCV = null" class="btn-back mb-6 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon-back h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Quay lại danh sách
        </button>

        <div class="space-y-4">
          <h2 class="text-2xl font-bold">{{ selectedCV.title || 'Không có tiêu đề' }}</h2>

          <div class="text-gray-800 space-y-1">
            <p><strong>Công ty:</strong> {{ selectedCV.company_name }}</p>
            <p><strong>Vị trí ứng tuyển:</strong> {{ selectedJob?.Level || 'Không xác định' }}</p>
            <p><strong>Ngày nộp:</strong> {{ formatDate(selectedCV.submitted_at) }}</p>
            <p><strong>Cập nhật lần cuối:</strong> {{ formatDate(selectedCV.updated_at) }}</p>
            <p><strong>Trạng thái:</strong>
              <span :class="['status-badge', statusClass(selectedCV.status)]">{{ selectedCV.status }}</span>
            </p>
          </div>

          <div>
            <a
              href="#"
              @click.prevent="handleViewCV(selectedCV)"
              class="btn-link inline-flex items-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="icon-download h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linejoin="round" stroke-linecap="round" d="M12 4v16m8-8H4"/>
              </svg>
              Xem CV đã gửi
            </a>
          </div>

          <!-- Employer's message section -->
          <div v-if="selectedCV.employer_message" class="mt-6 p-4 bg-blue-50 rounded-lg">
            <h3 class="font-semibold text-lg mb-2">Tin nhắn từ nhà tuyển dụng:</h3>
            <p class="text-gray-700" v-html="formatMessage(selectedCV.employer_message)"></p>
          </div>
        </div>
      </template>

      <!-- No CV message -->
      <div v-else class="text-center text-gray-500 mt-20 text-lg">
        Không tìm thấy CV nào phù hợp.
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="filteredCVs.length"
        :page-size="pageSize"
        :current-page.sync="currentPage"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getCVsByApplicantID, getJobID } from '@/services/user.service'
import { ElNotification } from "element-plus"
import { Search } from '@element-plus/icons-vue'

export default defineComponent({
  name: 'ApplicantCVManagement',
  setup() {
    const cvs = ref<any[]>([])
    const selectedCV = ref<any | null>(null)
    const loading = ref(false)
    const keySearch = ref("")
    const currentPage = ref(1)
    const pageSize = ref(8)

    const authStore = useAuthStore()
    const userId = authStore.getUserID()

    const fetchCVs = async () => {
      loading.value = true
      try {
        const res = await getCVsByApplicantID(userId)
        cvs.value = res.data.data || []
      } catch (err) {
        ElNotification({
          title: 'Lỗi',
          message: 'Không thể tải danh sách CV. Vui lòng thử lại.',
          type: 'error',
        })
      } finally {
        loading.value = false
      }
    }

    const filteredCVs = computed(() => {
      return cvs.value.filter(cv => {
        const searchTerm = keySearch.value.toLowerCase()
        return (
          (cv.title || '').toLowerCase().includes(searchTerm) ||
          (cv.company_name || '').toLowerCase().includes(searchTerm) ||
          (cv.position || '').toLowerCase().includes(searchTerm)
        )
      })
    })

    const paginatedCVs = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredCVs.value.slice(start, end)
    })

    const handlePageChange = (page: number) => {
      currentPage.value = page
    }

    // Inside setup()
    const selectedJob = ref<any | null>(null)  // Optional: store job data if you want to reuse later

    const selectCV = async (cv: any) => {
      selectedCV.value = cv

      // ✅ Fetch job information based on job_id
      if (cv.job_id) {
        try {
          const response = await getJobID(cv.job_id)
          selectedJob.value = response.data
          console.log("📄 Job Info:", selectedJob.value)  // ✅ Log the job info
        } catch (error) {
          console.error("❌ Failed to fetch job info:", error)
        }
      }
    }

    const handleViewCV = (cv: any) => {
      if (!cv.cv_url) {
        ElNotification({
          title: 'Thông báo',
          message: 'Không tìm thấy file CV',
          type: 'info',
        })
        return
      }
      const link = getDownloadLink(cv.cv_url)
      if (link !== '#') {
        window.open(link, '_blank')
      }
    }

    const formatDate = (dateString: string) => {
      if (!dateString) return 'Không rõ'
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    }

    // Add this new method to format messages with line breaks
    const formatMessage = (message: string) => {
      if (!message) return '';
      // Convert newlines to <br> tags and escape HTML for security
      return message
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;')
        .replace(/\n/g, '<br>');
    };

    const backendHost = import.meta.env.VITE_API_URL || 'http://localhost:3009'

    const getDownloadLink = (path: string) => {
      if (!path) return '#'
      const parts = path.split("\\public\\")
      if (parts.length < 2) return '#'
      const relativePath = parts[1].replace(/\\/g, '/')
      return `${backendHost}/public/${relativePath}`
    }

    const statusClass = (status: string) => {
      switch (status?.toLowerCase()) {
        case 'approved':
        case 'accepted': return 'status-approved'
        case 'pending': return 'status-pending'
        case 'rejected': return 'status-rejected'
        case 'reviewed': return 'status-reviewed'
        default: return 'status-unknown'
      }
    }

    onMounted(() => {
      fetchCVs()
    })

    return {
      cvs,
      filteredCVs,
      paginatedCVs,
      loading,
      selectedCV,
      selectedJob,
      keySearch,
      currentPage,
      pageSize,
      selectCV,
      handleViewCV,
      getDownloadLink,
      statusClass,
      handlePageChange,
      Search,
      formatDate,
      formatMessage,
    }
  }
})
</script>

<style scoped>
/* Reuse all the same styles from the employer version */
.cv-main-content {
  background-color: #fff;
  font-family: 'Inter', sans-serif;
  padding: 1.5rem;
}

.search-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.search-left h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
}

.input-search {
  position: relative;
  display: flex;
  align-items: center;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  width: 350px;
}

.input-search input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  font-size: 0.875rem;
}

.icon-search {
  position: absolute;
  left: 1rem;
  color: #9ca3af;
}

.cv-review-content {
  flex: 1;
  overflow-y: auto;
}

/* CV Cards */
.cv-card {
  cursor: pointer;
  padding: 1.25rem 1.5rem;
  border-radius: 0.75rem;
  background-color: #f9fafb;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 0.75rem;
}

.cv-card:hover {
  background-color: #e0f2fe;
  box-shadow: 0 4px 8px rgb(0 0 0 / 0.15);
}

.cv-card-selected {
  background-color: #bae6fd;
  box-shadow: 0 0 0 3px #3b82f6;
}

/* Status badges */
.status-badge {
  font-weight: 600;
  font-size: 0.75rem;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.status-approved {
  background-color: #10b981;
  color: white;
}

.status-pending {
  background-color: #fbbf24;
  color: #92400e;
}

.status-rejected {
  background-color: #ef4444;
  color: white;
}

.status-reviewed {
  background-color: #3b82f6;
  color: white;
}

.status-unknown {
  background-color: #6b7280;
  color: white;
}

/* Buttons */
.btn-back {
  font-weight: 600;
  border-radius: 0.5rem;
  padding: 0.5rem 1.25rem;
  transition: all 0.2s ease;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  user-select: none;
  border: none;
  text-decoration: none;
}

.btn-link {
  display: inline-flex;         /* giữ chữ trên 1 dòng và dễ canh center */
  align-items: center;          /* căn dọc giữa */
  height: 30px;                 /* giảm chiều cao (tùy chỉnh theo ý bạn) */
  min-width: 160px;             /* tăng chiều rộng tối thiểu */
  padding: 0 10px;              /* padding ngang để chữ không sát viền */
  font-size: 1rem;
  white-space: nowrap;          /* ngăn xuống dòng */
  text-decoration: underline;
  color: #2563eb;
  background: none;
  border-radius: 0;
  cursor: pointer;
  user-select: none;
  font-weight: 600;
}
.btn-link:hover {
  text-decoration: none;
}

.btn-link {
  display: inline-flex !important;
  align-items: center;
  height: 30px;
  min-width: 160px;
  padding: 0 10px;
  white-space: nowrap;
}
.btn-link:hover {
  text-decoration: none;
}

.btn-back {
  color: #2563eb;
  background: transparent;
  font-size: 0.875rem;
  padding: 0.15rem 0.6rem;
  border: 1px solid #2563eb;
  user-select: none;
  border-radius: 0.5rem;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.btn-back:hover {
  background-color: #e0f2fe;
}

.icon-back {
  height: 1rem;
  width: 1rem;
}

/* Scrollbar styling */
.cv-review-content::-webkit-scrollbar {
  width: 8px;
}
.cv-review-content::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.1);
  border-radius: 4px;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

/* Responsive */
@media (max-width: 768px) {
  .search-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .input-search {
    width: 100%;
  }

  .cv-card {
    padding: 1rem;
  }
}
</style>