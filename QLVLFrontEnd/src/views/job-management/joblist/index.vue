<template>
  <div class="job-management-container">
    <div class="header-section">
      <div class="search-section">
        <h1>Job Listings</h1>
        <div class="search-box">
          <el-icon class="search-icon"><Search /></el-icon>
          <input
            type="text"
            v-model="keySearch"
            placeholder="Search jobs..."
          />
        </div>
      </div>
      <button class="create-button" @click="openPostJobPopup">
        <el-icon><Plus /></el-icon>
        <span>Post Job</span>
      </button>
    </div>

    <div class="table-container">
      <table class="job-table">
        <thead>
          <tr>
            <th class="image-header">Image</th>
            <th class="title-header">Title</th>
            <th class="company-header">Company</th>
            <th class="location-header">Location</th>
            <th class="salary-header">Salary</th>
            <th class="level-header">Level</th>
            <th class="action-header">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in paginatedJobs" :key="job.id" class="job-row" @click="handleOpenPopup(job.id)">
            <td class="image-cell">
              <img :src="job.Source_Picture || defaultImage" class="job-image" />
            </td>
            <td class="title-cell">{{ job.Title || "No Title" }}</td>
            <td class="company-cell">{{ job.Company_Name || "No Company" }}</td>
            <td class="location-cell">{{ job.Place || "No Location" }}</td>
            <td class="salary-cell">{{ job.Salary || "Not Specified" }}</td>
            <td class="level-cell">{{ job.Level || "Not Specified" }}</td>
            <td class="action-cell">
              <button class="edit-button" @click.stop="handleOpenPopup(job.id)">Edit</button>
            </td>
          </tr>
          <tr v-if="listJob.length === 0">
            <td colspan="7" class="no-jobs">
              No jobs available
              <button class="post-job-button" @click="openPostJobPopup">
                <el-icon><Plus /></el-icon>
                Post Your First Job
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination-section" v-if="listJob.length > 0">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="filteredJobs.length"
        :page-size="pageSize"
        :current-page.sync="currentPage"
        @current-change="handlePageChange"
      />
    </div>

    <popupUpdate v-if="isOpen" @close-popup="handleClosePopup" @job-updated="handleJobUpdated" :idChoose="idChooseUpdate" />
    <popupPost v-if="showPostPopup" @close-popup="closePostJobPopup" @job-posted="handleJobPosted" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import axios from "axios";
import type { IJob, IPronvince } from "@/types/auth";
import { getJobAll, fetchJobsForUser } from "@/services/user.service";
import { useAuthStore } from "@/stores/auth";
import popupUpdate from "@/views/popup/popupUpdate.vue";
import popupPost from "@/views/popup/popupPost.vue";
import { ElNotification } from "element-plus";

const auth = useAuthStore();
const isOpen = ref<boolean>(false);
const showPostPopup = ref<boolean>(false);
const idChooseUpdate = ref<string>("");
const listJob = ref<IJob[]>([]);
const isAdmin = ref<boolean>(false);
const defaultImage = "default-image.jpg";

// Pagination
const keySearch = ref<string>("");
const pageSize = ref(10);
const currentPage = ref(1);

// Filter and paginate jobs
const filteredJobs = computed(() => {
  return listJob.value.filter(job =>
    (job.Title && job.Title.toLowerCase().includes(keySearch.value.toLowerCase())) ||
    (job.Company_Name && job.Company_Name.toLowerCase().includes(keySearch.value.toLowerCase())) ||
    (job.Place && job.Place.toLowerCase().includes(keySearch.value.toLowerCase()))
  );
});

const paginatedJobs = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredJobs.value.slice(start, start + pageSize.value);
});

// Open and close popups
const handleOpenPopup = (id: string) => {
  isOpen.value = true;
  idChooseUpdate.value = id;
};

const handleClosePopup = () => {
  isOpen.value = false;
  idChooseUpdate.value = "";
};

const openPostJobPopup = () => {
  showPostPopup.value = true;
};

const closePostJobPopup = () => {
  showPostPopup.value = false;
};

const handleJobPosted = () => {
  closePostJobPopup();
  fetchData(); // Refresh the job list after posting
};

const handleJobUpdated = (updatedJob: any) => { // Update type to 'any' for now
  try {
    const index = listJob.value.findIndex(job => job.id === idChooseUpdate.value);
    if (index !== -1) {
      // Update the specific job in the list
      listJob.value[index] = { ...listJob.value[index], ...updatedJob };
    }
    ElNotification({
      title: "Success",
      message: "Job updated successfully!",
      type: "success",
    });
  } catch (error) {
    console.error("Error updating job list:", error);
    ElNotification({
      title: "Error",
      message: "Failed to update job list",
      type: "error",
    });
  } finally {
    handleClosePopup();
  }
};

// Fetch provinces
const provinces = ref<IPronvince[]>([]);
const getProvinces = async () => {
  try {
    const response = await axios.get("https://provinces.open-api.vn/api/");
    provinces.value = response.data;
    provinces.value.unshift({ code: 0, name: "" });
  } catch (error) {
    console.error("Error fetching provinces:", error);
  }
};

// Fetch jobs based on admin status
const fetchData = async () => {
  try {
    if (auth.getIsAdmin()) {
      const res = await getJobAll();
      if (!res || !res.data) {
        throw new Error("Invalid response from the server");
      }
      listJob.value = res.data.data || res.data;
    } else {
      const userId = auth.getUserID();
      if (userId) {
        const jobs = await fetchJobsForUser(userId);
        listJob.value = jobs;
      } else {
        console.warn("User ID not found.");
        listJob.value = []; // Or handle the case where user ID is not available
      }
    }
  } catch (error) {
    console.error("Error fetching jobs:", error);
    listJob.value = []; // Ensure listJob is empty in case of error
  }
};

const handleCheckAuth = () => {
  isAdmin.value = auth.getIsAdmin();
};

const handlePageChange = (page: number) => {
  currentPage.value = page;
};

onMounted(async () => {
  await getProvinces();
  handleCheckAuth();
  fetchData();
});

// Watch for changes in isAdmin or userID
watch(
  () => [auth.getIsAdmin(), auth.getUserID()],
  ([newIsAdmin, newUserID]) => {
    isAdmin.value = newIsAdmin;
    if (!newIsAdmin && !newUserID) {
      console.warn("User ID not found.");
      listJob.value = [];
    }
    fetchData();
  },
  { immediate: false } // Execute on mount
);
</script>

<style lang="scss" scoped>
.job-management-container {
  padding: 20px;
  background-color: #f8f9fa;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-section {
  display: flex;
  align-items: center;
  gap: 20px;

  h1 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
  }
}

.search-box {
  position: relative;
  width: 300px;

  .search-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #7d7d7d;
  }

  input {
    width: 100%;
    padding: 10px 15px 10px 40px;
    border: 1px solid #dcdfe6;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.3s;

    &:focus {
      border-color: #409eff;
      outline: none;
      box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
    }
  }
}

.create-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;

  &:hover {
    background-color: #3e8e41;
    transform: translateY(-2px);
  }
}

.table-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.job-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

th {
  padding: 12px 8px;
  text-align: left;
  font-weight: 600;
  color: #606266;
  background-color: #f5f7fa;
  white-space: nowrap;
}

.image-header {
  width: 80px;
  padding-left: 12px;
}

.title-header {
  width: 200px;
}

.company-header {
  width: 180px;
}

.location-header {
  width: 150px;
}

.salary-header {
  width: 120px;
}

.level-header {
  width: 120px;
}

.action-header {
  width: 100px;
  padding-right: 12px;
}

.job-row {
  border-bottom: 1px solid #ebeef5;
  transition: background-color 0.3s;
  cursor: pointer;

  &:hover {
    background-color: #f5f7fa;
  }

  &:last-child {
    border-bottom: none;
  }

  td {
    padding: 12px 8px;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
}

.image-cell {
  width: 80px;
  padding: 8px 4px 8px 12px !important;
  text-align: center;

  .job-image {
    width: 60px;
    height: 60px;
    border-radius: 4px;
    object-fit: cover;
  }
}

.title-cell {
  width: 200px;
  font-weight: 500;
}

.company-cell {
  width: 180px;
}

.location-cell {
  width: 150px;
}

.salary-cell {
  width: 120px;
  color: #2a8bf2;
  font-weight: 500;
}

.level-cell {
  width: 120px;
}

.action-cell {
  width: 100px;
  padding: 8px 12px 8px 4px !important;
  text-align: center;

  .edit-button {
    background-color: #2a8bf2;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
      background-color: #1666c1;
    }
  }
}

.no-jobs {
  text-align: center;
  padding: 40px 0;
  color: #888;

  .post-job-button {
    margin-top: 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 0.9rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }
}

.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .search-section {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .search-box {
    width: 100%;
  }

  .create-button {
    width: 100%;
    justify-content: center;
  }
}
</style>