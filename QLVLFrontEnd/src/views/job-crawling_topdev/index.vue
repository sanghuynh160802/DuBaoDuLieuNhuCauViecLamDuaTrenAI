<script setup lang="ts">
import NavBar from "../../layouts/NavBar/index.vue"
import JobCrawlingMain from "./main/index.vue"
</script>

<template>
  <div class="container-dashboard">
    <NavBar />
    <div class="container-list-user">
      <JobCrawlingMain />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container-dashboard {
  width: 100%;
  height: 100vh; /* Use viewport height */
  background: white;
  display: flex;
  overflow: hidden; /* Prevent any scrollbar from appearing */
}

.container-list-user {
  margin-left: 50px;
  flex: 1; /* Allow it to grow and take remaining space */
  padding: 20px; /* Optional: spacing inside */
  overflow: hidden; /* Prevent scrolling on this container */
}
</style>