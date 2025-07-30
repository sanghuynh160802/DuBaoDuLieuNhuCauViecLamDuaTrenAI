<template>
  <div class="skills-management-layout">
    <SideBar />
    <MainComponent />
  </div>
</template>

<script>
import MainComponent from './main/index.vue';
import SideBar from '@/layouts/ApplicantNavBar/index.vue';

export default {
  components: {
    MainComponent,
    SideBar
  }
};
</script>

<style scoped>
.skills-management-layout {
  display: flex;           /* Arrange children horizontally */
  width: 100%;
  min-height: 100vh;       /* Full viewport height */
  background-color: #f8f9fa; /* Optional: light background */
}

/* Sidebar styles */
.skills-management-layout > *:first-child {
  width: 250px;            /* Fixed width for sidebar */
  min-width: 250px;
  background-color: white; /* Match sidebar background */
  border-right: 1px solid #ddd; /* subtle separator */
  overflow-y: auto;        /* Scroll if content overflows */
}

/* Main content styles */
.skills-management-layout > *:last-child {
  flex-grow: 1;            /* Fill remaining horizontal space */
  padding: 20px;           /* Existing padding */
  padding-top: 40px;       /* Add extra top padding to push down */
  overflow-y: auto;        /* Scroll if content overflows vertically */
  background-color: white; /* Main content background */
}
</style>