<template>
  <div class="cv-management-container">
    <!-- Conditionally render Header and Search only if no CV selected -->
    <header v-if="!selectedCV" class="header-section">
      <div class="header-content">
        <h1 class="title">Quản Lý CV</h1>
        <p class="subtitle">Dễ dàng quản lý và xem xét các CV ứng tuyển.</p>
      </div>
    </header>

    <section v-if="!selectedCV" class="search-and-filters">
      <div class="search-input">
        <el-icon class="icon-search"><Search /></el-icon>
        <input
          type="text"
          v-model="keySearch"
          placeholder="Tìm kiếm theo email, kỹ năng, vị trí..."
        />
      </div>
    </section>

    <section class="cv-review-content">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>Đang tải dữ liệu...</span>
      </div>

      <!-- CV List Display -->
      <template v-else-if="!selectedCV && paginatedCVs.length">
        <div class="cv-list-vertical">
          <div
            v-for="cv in paginatedCVs"
            :key="cv.id"
            :class="['cv-card', { 'cv-card-selected': selectedCV?.id === cv.id }]"
            @click="selectCV(cv)"
          >
            <div class="cv-header">
              <h3 class="cv-title">{{ cv.title }}</h3>
              <span :class="['status-badge', statusClass(cv.status)]">{{ cv.status }}</span>
            </div>
            <p class="cv-email">{{ cv.applicant_email }}</p>
            <div class="cv-details">
              <span>{{ cv.position || 'Chưa xác định' }}</span>
              <span>•</span>
              <span>{{ cv.location || 'Không rõ khu vực' }}</span>
            </div>
          </div>
        </div>
      </template>

      <!-- CV Details Display -->
      <template v-else-if="selectedCV">
        <div class="cv-details-view">
          <button @click="selectedCV = null" class="btn-back">
            <el-icon><ArrowLeft /></el-icon>
            <span>Quay lại danh sách</span>
          </button>

          <div class="cv-details-content">
            <h2 class="cv-details-title">{{ selectedCV.title }}</h2>

            <div class="cv-details-info">
              <p><strong>Ứng viên:</strong> {{ selectedCV.applicant_email }}</p>
              <p><strong>Số điện thoại:</strong> {{ selectedCV.applicant_phone || 'Chưa cung cấp' }}</p>
              <p><strong>Vị trí ứng tuyển:</strong> {{ selectedJob.Level || 'Không xác định' }}</p>
              <p><strong>Kỹ năng:</strong> {{ selectedJob.Profession || 'Chưa cập nhật' }}</p>
              <p><strong>Khu vực:</strong> {{ selectedJob.Place || 'Không rõ' }}</p>
              <p><strong>Trạng thái:</strong>
                <span :class="['status-badge', statusClass(selectedCV.status)]">{{ selectedCV.status }}</span>
              </p>
            </div>

            <div class="cv-actions">
              <a
                href="#"
                @click.prevent="handleViewCV(selectedCV)"
                class="btn-view-cv"
              >
                <el-icon><Download /></el-icon>
                <span>Xem CV</span>
              </a>
            </div>

            <div class="action-buttons">
              <el-button type="success" @click="approveCV(selectedCV)">
                <el-icon><Check /></el-icon>
                <span>Duyệt</span>
              </el-button>
              <el-button type="danger" @click="rejectCV(selectedCV)">
                <el-icon><Close /></el-icon>
                <span>Từ chối</span>
              </el-button>
              <el-button type="primary" @click="messageCandidate(selectedCV)">
                <el-icon><ChatSquare /></el-icon>
                <span>Nhắn tin</span>
              </el-button>
            </div>
          </div>
        </div>
      </template>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <el-empty description="Không có CV nào phù hợp." />
      </div>
    </section>

    <!-- Pagination Section -->
    <footer class="pagination-section">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="filteredCVs.length"
        :page-size="pageSize"
        :current-page.sync="currentPage"
        @current-change="handlePageChange"
      />
    </footer>

    <!-- Popup Message -->
    <popupMessage
      v-if="showMessagePopup"
      :candidate="messageToCandidate"
      @close-popup="showMessagePopup = false"
      @message-sent="handleMessageSent"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { getCVsByCompanyId, updateCVStatusApi, saveEmployerMessageApi, getJobID } from '@/services/user.service';
import { ElNotification, ElEmpty } from "element-plus";
import { Search, Loading, ArrowLeft, Download, Check, Close, ChatSquare } from '@element-plus/icons-vue';
import popupMessage from '@/views/popup/popupMessage.vue';

export default defineComponent({
  name: 'CVReview',
  components: { popupMessage, ElEmpty },
  setup() {
    const cvs = ref<any[]>([]);
    const selectedCV = ref<any | null>(null);
    const loading = ref(false);
    const keySearch = ref("");
    const currentPage = ref(1);
    const pageSize = ref(8);
    const showMessagePopup = ref(false);
    const messageToCandidate = ref<any>(null);
    const authStore = useAuthStore();
    const userId = authStore.getUserID();
    const selectedJob = ref(null);

    const fetchCVs = async () => {
      loading.value = true;
      try {
        const res = await getCVsByCompanyId(userId);
        cvs.value = res.data.data || [];
      } catch (err) {
        ElNotification({
          title: 'Lỗi',
          message: 'Không thể tải CVs. Vui lòng thử lại.',
          type: 'error',
        });
      } finally {
        loading.value = false;
      }
    };

    const filteredCVs = computed(() => {
      const searchTerm = keySearch.value.toLowerCase();
      return cvs.value.filter(cv =>
        (cv.title || '').toLowerCase().includes(searchTerm) ||
        cv.applicant_email.toLowerCase().includes(searchTerm) ||
        (cv.skills || []).some((s: string) => s.toLowerCase().includes(searchTerm)) ||
        (cv.position || '').toLowerCase().includes(searchTerm) ||
        (cv.location || '').toLowerCase().includes(searchTerm)
      );
    });

    const paginatedCVs = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      const end = start + pageSize.value;
      return filteredCVs.value.slice(start, end);
    });

    const handlePageChange = (page: number) => {
      currentPage.value = page;
    };

    const selectCV = async (cv: any) => {
      selectedCV.value = cv;
      if (cv?.job_id) {
        try {
          const res = await getJobID(cv.job_id);
          selectedJob.value = res.data?.data || res.data;
        } catch (error) {
          console.error('Error fetching job info:', error);
          selectedJob.value = null;
        }
      } else {
        selectedJob.value = null;
      }
    };

    const approveCV = async (cv: any) => {
      try {
        await updateCVStatusApi(cv.id, 'ACCEPTED', 'Approved by reviewer');
        ElNotification({
          title: 'Thành công',
          message: 'CV đã được duyệt thành công!',
          type: 'success',
        });
        fetchCVs();
        selectedCV.value = null;
      } catch (error: any) {
        console.error('Error approving CV:', error.response?.data || error.message);
        ElNotification({
          title: 'Lỗi',
          message: error.response?.data?.message || 'Không thể duyệt CV. Thử lại sau.',
          type: 'error',
        });
      }
    };

    const rejectCV = async (cv: any) => {
      try {
        await updateCVStatusApi(cv.id, 'REJECTED', 'Rejected by reviewer');
        ElNotification({
          title: 'Thành công',
          message: 'CV đã bị từ chối!',
          type: 'warning',
        });
        fetchCVs();
        selectedCV.value = null;
      } catch (error) {
        console.error('Error rejecting CV:', error);
        ElNotification({
          title: 'Lỗi',
          message: 'Không thể từ chối CV. Thử lại sau.',
          type: 'error',
        });
      }
    };

    const handleViewCV = async (cv: any) => {
      if (!cv) return;
      try {
        await updateCVStatusApi(cv.id, 'REVIEWED');
        cv.status = 'REVIEWED';
      } catch (error) {
        console.error('Failed to update status to REVIEWED:', error);
      }
      const link = getDownloadLink(cv.cv_url);
      if (link !== '#') {
        window.open(link, '_blank');
      }
    };

    const handleMessageSent = async (action: 'approve' | 'reject', content: string) => {
      const submissionId = messageToCandidate.value?.id;
      if (!submissionId) return;

      try {
        await saveEmployerMessageApi(submissionId, content);
        const newStatus = action === 'approve' ? 'ACCEPTED' : 'REJECTED';
        await updateCVStatusApi(submissionId, newStatus, content);

        ElNotification({
          title: 'Thành công',
          message: action === 'approve' ? 'CV đã được duyệt!' : 'CV đã bị từ chối!',
          type: action === 'approve' ? 'success' : 'warning',
        });

        await fetchCVs();
        selectedCV.value = null;
        showMessagePopup.value = false;

      } catch (error) {
        console.error('❌ Error saving message or updating status:', error);
        ElNotification({
          title: 'Lỗi',
          message: 'Không thể cập nhật trạng thái hoặc lưu tin nhắn.',
          type: 'error',
        });
      }
    };

    const messageCandidate = (cv: any) => {
      messageToCandidate.value = cv;
      showMessagePopup.value = true;
    };

    const backendHost = import.meta.env.VITE_API_URL || 'http://localhost:3009';

    const getDownloadLink = (path: string) => {
      if (!path) return '#';
      const parts = path.split("\\public\\");
      if (parts.length < 2) return '#';
      const relativePath = parts[1].replace(/\\/g, '/');
      return `${backendHost}/public/${relativePath}`;
    };

    const statusClass = (status: string) => {
      const lowerStatus = status?.toLowerCase();
      switch (lowerStatus) {
        case 'approved':
        case 'accepted': return 'status-approved';
        case 'pending': return 'status-pending';
        case 'rejected': return 'status-rejected';
        default: return 'status-unknown';
      }
    };

    onMounted(() => {
      fetchCVs();
    });

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
      approveCV,
      rejectCV,
      handleViewCV,
      messageCandidate,
      getDownloadLink,
      statusClass,
      handlePageChange,
      showMessagePopup,
      messageToCandidate,
      handleMessageSent,
      Search,
      Loading,
      ArrowLeft,
      Download,
      Check,
      Close,
      ChatSquare,
    };
  }
});
</script>

<style scoped>
.cv-management-container {
  background-color: #f5f7fa;
  min-height: 100vh;
  font-family: 'Roboto', sans-serif;
  color: #333;
  display: flex;
  flex-direction: column;
}

/* Reduced Header Styles */
.header-section {
  background-color: #3498db;
  color: white;
  padding: 1rem 2rem; /* Reduced padding */
  text-align: left;
  border-bottom: 2px solid #2980b9;
  transition: all 0.3s ease;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.header-section .title {
  font-size: 1.75rem; /* Smaller font size */
  font-weight: 700;
  margin-bottom: 0.3rem;
}

.header-section .subtitle {
  font-size: 0.9rem; /* Smaller subtitle */
  color: #ecf0f1;
  margin: 0;
}

/* Reduced Search and Filters */
.search-and-filters {
  padding: 0.75rem 2rem; /* Reduced vertical padding */
  background-color: #fff;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: flex-start; /* Align left */
  align-items: center;
}

.search-input {
  position: relative;
  width: 350px; /* Slightly narrower */
}

.search-input input {
  width: 100%;
  padding: 0.6rem 2.5rem;
  border: 1px solid #ddd;
  border-radius: 0.3rem;
  font-size: 0.9rem; /* Smaller font */
  transition: border-color 0.3s ease;
}

.search-input input:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.search-input .icon-search {
  position: absolute;
  left: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  color: #95a5a6;
}

/* CV Review Content */
.cv-review-content {
  flex: 1;
  padding: 2rem;
}

/* CV List - Vertical layout */
.cv-list-vertical {
  display: flex;
  flex-direction: column; /* Vertical stacking */
  gap: 1rem;
}

.cv-card {
  background-color: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.cv-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.cv-card-selected {
  border: 3px solid #3498db;
}

.cv-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.cv-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #34495e;
  margin: 0;
}

.cv-email {
  color: #7f8c8d;
  margin-bottom: 0.5rem;
}

.cv-details {
  font-size: 0.9rem;
  color: #95a5a6;
  display: flex;
  align-items: center;
}

.cv-details span:not(:last-child)::after {
  content: "•";
  margin: 0 0.5rem;
}

/* Status Badges */
.status-badge {
  font-size: 0.8rem;
  font-weight: 500;
  padding: 0.3rem 0.6rem;
  border-radius: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.status-approved {
  background-color: #2ecc71;
  color: white;
}

.status-pending {
  background-color: #f39c12;
  color: #fff;
}

.status-rejected {
  background-color: #e74c3c;
  color: white;
}

.status-unknown {
  background-color: #34495e;
  color: white;
}

/* CV Details View */
.cv-details-view {
  background-color: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.cv-details-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.cv-details-info {
  font-size: 1rem;
  color: #555;
  margin-bottom: 2rem;
}

.cv-details-info p {
  margin-bottom: 0.8rem;
}

.cv-actions {
  margin-bottom: 2rem;
}

.btn-view-cv {
  display: inline-flex;
  align-items: center;
  padding: 0.8rem 1.5rem;
  background-color: #3498db;
  color: white;
  border-radius: 0.3rem;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.btn-view-cv:hover {
  background-color: #2980b9;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-start;
}

/* Button Styles */
.el-button {
  font-size: 1rem;
  padding: 0.8rem 1.5rem;
  border-radius: 0.3rem;
  transition: transform 0.2s ease;
}

.el-button:hover {
  transform: translateY(-2px);
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #777;
}

.loading-state .el-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #777;
}

/* Pagination Section */
.pagination-section {
  padding: 1.5rem;
  background-color: #fff;
  border-top: 1px solid #ddd;
  display: flex;
  justify-content: center;
}

/* Back Button */
.btn-back {
  display: inline-flex;
  align-items: center;
  padding: 0.6rem 1.2rem;
  background-color: #ecf0f1;
  color: #3498db;
  border-radius: 0.3rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-back:hover {
  background-color: #d5dbdb;
}

/* Responsive */
@media (max-width: 768px) {
  .header-section {
    padding: 1rem 1.5rem;
    text-align: center;
  }

  .header-section .title {
    font-size: 1.5rem;
  }

  .search-and-filters {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    padding: 0.75rem 1.5rem;
  }

  .search-input {
    width: 100%;
  }

  /* In mobile, cv-list-vertical just stacks naturally */
  .cv-list-vertical {
    gap: 0.75rem;
  }

  .cv-details-view {
    padding: 1.5rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 0.8rem;
  }

  .el-button {
    width: 100%;
  }

  .pagination-section {
    padding: 1rem;
  }
}
</style>