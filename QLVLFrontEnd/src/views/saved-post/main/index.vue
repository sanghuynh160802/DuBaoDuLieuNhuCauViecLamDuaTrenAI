<template>
  <div class="saved-posts-wrapper">
    <div class="header">
      <h2>Bài đăng đã lưu</h2>
    </div>

    <div class="container-listjob">
      <!-- Add loading state -->
      <div v-if="isLoading" class="loading-state">
        <p>Đang tải bài đăng đã lưu...</p>
      </div>

      <!-- Display jobs if available -->
      <div v-else-if="savedJobs.length > 0" class="job-list">
        <div
          v-for="job in savedJobs"
          :key="job.id"
          class="card-listjob"
          @click="openJobDetail(job.id)"
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

      <!-- Display message if no jobs -->
      <div v-else class="no-jobs">
        <p>Bạn chưa lưu bài đăng nào.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getSavedPostsByUserId, getJobID } from '@/services/user.service'
import type { IJob } from '@/types/auth'

const authStore = useAuthStore()
const savedJobs = ref<IJob[]>([])
const isLoading = ref(true)

const fetchSavedJobs = async () => {
  console.group('Fetching Saved Jobs')
  isLoading.value = true
  
  try {
    const userId = authStore.getUserID()
    console.log('User ID:', userId)
    
    if (!userId) {
      console.warn('No user ID found')
      savedJobs.value = []
      return
    }
    
    // Get saved post IDs
    console.log('Fetching saved post IDs...')
    const savedPostsRes = await getSavedPostsByUserId(userId)
    console.log('Saved posts response:', savedPostsRes)
    
    if (!savedPostsRes?.data || !Array.isArray(savedPostsRes.data)) {
      console.warn('Invalid saved posts response')
      savedJobs.value = []
      return
    }

    const savedPostIds = savedPostsRes.data.map(item => String(item.post_id))
    console.log('Saved post IDs:', savedPostIds)

    if (savedPostIds.length === 0) {
      console.log('No saved posts found')
      savedJobs.value = []
      return
    }

    // Call API one by one and collect results
    console.log('Fetching job details for each saved post ID...')
    const jobDetailsPromises = savedPostIds.map(id => getJobID(id).then(res => res.data).catch(() => null))
    const jobDetailsArray = await Promise.all(jobDetailsPromises)

    // Filter out nulls and normalize results to array
    const jobsArray = jobDetailsArray.flatMap(jobData => {
      if (!jobData) return []
      // If jobData is an array, return as is, else wrap into array
      return Array.isArray(jobData) ? jobData : [jobData]
    })

    if (jobsArray.length === 0) {
      console.warn('No valid job details fetched')
      savedJobs.value = []
      return
    }

    // Create map for quick lookup
    const jobsMap = new Map(jobsArray.map(job => [String(job.id), job]))
    console.log('Jobs map:', jobsMap)

    // Map savedPostIds to jobs keeping order
    const processedJobs = savedPostIds
      .map(id => jobsMap.get(id))
      .filter(job => job !== undefined) as IJob[]

    console.log('Processed jobs:', processedJobs)
    savedJobs.value = processedJobs

  } catch (error) {
    console.error('Error fetching saved jobs:', error)
    savedJobs.value = []
  } finally {
    isLoading.value = false
    console.log('Final saved jobs:', savedJobs.value)
    console.log('Number of saved jobs:', savedJobs.value.length)
    console.groupEnd()
  }
}

// Initial fetch
onMounted(() => {
  console.log('Component mounted')
  fetchSavedJobs()
})

// Watch for auth changes
watch(() => authStore.getUserID(), (newVal) => {
  console.log('User ID changed:', newVal)
  fetchSavedJobs()
})

const openJobDetail = (id: string) => {
  console.log('Opening job detail:', id)
  if (!id) return
  window.open(`/mainjob/${id}`, '_blank')
}
</script>

<style scoped>
.saved-posts-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

.header {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.header h2 {
  font-size: 24px;
  color: #2d3748;
  margin: 0;
  font-weight: 700;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.container-listjob {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px 10px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
  min-height: 300px;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-listjob {
  display: flex;
  align-items: center;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
  padding: 20px 25px;
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
  margin-right: 20px;
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
  gap: 6px;
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
}

.location {
  font-size: 0.85rem;
  color: #777;
}

.details {
  margin-top: 6px;
  font-size: 0.9rem;
  color: #222;
  display: flex;
  gap: 10px;
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

.no-jobs, .loading-state {
  text-align: center;
  color: #888;
  font-size: 1.1rem;
  padding: 50px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}
</style>