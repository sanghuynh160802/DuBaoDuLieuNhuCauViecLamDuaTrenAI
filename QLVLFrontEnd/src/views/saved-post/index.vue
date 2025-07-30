<template>
  <div class="saved-post-page">
    <!-- Applicant Navbar on the left -->
    <ApplicantNavBar class="sidebar" />

    <!-- Saved Post main content on the right -->
    <SavedPostMain class="main-content" />
  </div>
</template>

<script setup lang="ts">
import ApplicantNavBar from '@/layouts/ApplicantNavBar/index.vue'
import SavedPostMain from '@/views/saved-post/main/index.vue'
</script>

<style scoped>
.saved-post-page {
  display: flex;
  flex-direction: row; /* horizontal layout */
  min-height: 100vh;
  height: 100vh; /* full viewport height */
  overflow: hidden;
}

/* Set fixed width for the sidebar (ApplicantNavBar) */
.sidebar {
  width: 250px; /* adjust as needed */
  flex-shrink: 0; /* prevent shrinking */
  border-right: 1px solid #e0e0e0; /* optional separator */
  overflow-y: auto; /* scroll if content overflows */
}

/* SavedPostMain takes remaining space */
.main-content {
  flex-grow: 1;
  overflow-y: auto; /* scroll if content overflows */
  padding: 20px; /* optional padding */
  background-color: #f9f9f9; /* optional bg */
}
</style>