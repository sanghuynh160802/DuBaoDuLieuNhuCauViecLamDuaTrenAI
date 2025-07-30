<template>
  <div class="job-management-wrapper">
    <div class="job-list-header">
      <h2>Việc làm gợi ý cho bạn</h2>
    </div>

    <div class="container-listjob">
      <div v-if="listJob.length > 0" class="job-list">
        <div
          v-for="job in listJob"
          :key="job.id"
          class="card-listjob"
          @click="handleOpenPopup(job.id)"
          style="cursor: pointer;"
        >
          <div class="img-card">
            <img :src="job.Source_Picture || 'default-image.jpg'" alt="Job Image" />
          </div>
          <div class="text-card">
            <h3 class="title">{{ job.Title || "No Title" }}</h3>
            <p class="company">{{ job.Company_Name || "No Company" }}</p>
            <p class="location">{{ job.Place || "No Location" }}</p>
            <div class="details">
              <span class="salary">{{ job.Salary || "No Salary" }}</span>
              <span class="level">{{ job.Level || "No Level" }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="no-jobs">
        <p>No jobs available</p>
      </div>

      <!-- Nếu không còn dùng popup update thì comment hoặc xóa -->
      <!-- <popupUpdate v-if="isOpen" @close-popup="handleClosePopup" :idChoose="idChooseUpdate" /> -->

      <popupPost v-if="showPostPopup" @close-popup="closePostJobPopup" @job-posted="handleJobPosted" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import type { IJob, IPronvince } from "@/types/auth";
import { getJobsByUserId } from "@/services/user.service";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();

const userId = ref<string | null>(null);
const showPostPopup = ref<boolean>(false);
const listJob = ref<IJob[]>([]);
const isAdmin = ref<boolean>(false);

const handleOpenPopup = (id: string) => {
  if (!id) return;
  window.open(`/mainjob/${id}`, "_blank");
};

const openPostJobPopup = () => {
  showPostPopup.value = true;
};

const closePostJobPopup = () => {
  showPostPopup.value = false;
};

const handleJobPosted = () => {
  closePostJobPopup();
  getListJob();
};

const getListJob = async (): Promise<void> => {
  try {
    if (!userId.value) {
      console.warn("User ID not available yet.");
      return;
    }
    const res = await getJobsByUserId(userId.value);
    if (!res || !res.data) {
      throw new Error("Invalid response from the server");
    }
    const allJobs = res.data.data || res.data;
    const shuffledJobs = allJobs.sort(() => 0.5 - Math.random());
    listJob.value = shuffledJobs.slice(0, 3);
  } catch (error) {
    console.error("Error fetching jobs:", error);
  }
};

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

const handleCheckAuth = () => {
  isAdmin.value = auth.getIsAdmin();
};

onMounted(async () => {
  userId.value = auth.getUserID();
  await getProvinces();
  await getListJob();
  handleCheckAuth();
});
</script>

<style scoped>
.job-management-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 8px 20px; /* Giảm padding tổng thể */
}

.job-list-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 6px; /* Giảm margin dưới tiêu đề */
  padding: 0 20px;
}

.job-list-header h2 {
  font-size: 24px;
  color: #2d3748;
  margin: 0;
}

.container-listjob {
  max-width: 900px;
  margin: 0 auto;
  padding: 6px 10px; /* Giảm padding trong container */
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 6px; /* Giảm khoảng cách giữa các job item */
  margin-bottom: 4px; /* Giảm margin dưới danh sách */
}

.card-listjob {
  display: flex;
  align-items: center;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
  padding: 10px 18px; /* Giảm padding trong card */
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  cursor: pointer;
  position: relative;
}

.card-listjob:hover {
  box-shadow: 0 6px 16px rgb(0 0 0 / 0.15);
  transform: translateY(-3px);
}

.img-card {
  flex-shrink: 0;
  width: 90px;
  height: 90px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgb(0 0 0 / 0.1);
  margin-right: 12px; /* Giảm margin phải */
  background-color: #f0f4f8;
  display: flex;
  justify-content: center;
  align-items: center;
}

.img-card img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.text-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 3px; /* Giảm khoảng cách giữa các dòng text */
}

.title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.company {
  font-size: 0.95rem;
  font-weight: 600;
  color: #4a4a4a;
  margin: 0;
}

.location {
  font-size: 0.85rem;
  color: #777;
  margin: 0;
}

.details {
  margin-top: 3px; /* Giảm margin trên */
  font-size: 0.9rem;
  color: #222;
  display: flex;
  gap: 6px; /* Giảm gap giữa salary và level */
  align-items: center;
}

.salary {
  color: #2a8bf2;
  font-weight: 600;
}

.level {
  color: #555;
  font-style: italic;
}

.no-jobs {
  text-align: center;
  color: #888;
  font-size: 1.1rem;
  padding: 10px 0; /* Giảm padding */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px; /* Giảm gap */
  margin-bottom: 0;
}
</style>