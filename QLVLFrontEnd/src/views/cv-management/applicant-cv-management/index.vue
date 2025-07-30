<template>
  <div class="cv-management-container">
    <!-- Applicant Navigation Bar -->
    <ApplicantNavBar />

    <!-- Main CV Management Component -->
    <div class="cv-management-content">
      <ApplicantCVMain />
    </div>
  </div>
</template>

<script setup lang="ts">
import ApplicantNavBar from "@/layouts/ApplicantNavBar/index.vue";
import ApplicantCVMain from "./main/index.vue";
</script>

<style scoped>
.cv-management-container {
  display: grid;
  grid-template-columns: 250px auto;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.cv-management-content {
  padding: 20px;
}
</style>