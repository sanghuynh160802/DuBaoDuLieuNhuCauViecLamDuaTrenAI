<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();

const goTo = (path: string) => {
  router.push(path);
};
</script>

<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <img src="../../images/logodashboard.png" alt="Logo" />
    </div>

    <div class="menu">
      <!-- Dashboard -->
      <div class="menu-item">
        <span class="icon"><el-icon><Odometer /></el-icon></span>
        <span class="title">Dashboard</span>
      </div>

      <!-- Management Section -->
      <div class="menu-item">
        <span class="icon"><el-icon><Setting /></el-icon></span>
        <span class="title">Management</span>
      </div>
      <div class="submenu">
        <div class="submenu-item" @click="goTo('/user')">
          <span class="icon"><el-icon><User /></el-icon></span>
          <span>User</span>
        </div>
        <div class="submenu-item" @click="goTo('/skill-management')">
          <span class="icon"><el-icon><User /></el-icon></span>
          <span>Skills</span>
        </div>
        <div class="submenu-item" @click="goTo('/applicant-cv-management')">
          <span class="icon"><el-icon><Document /></el-icon></span>
          <span>CV Management</span>
        </div>
        <div class="submenu-item" @click="goTo('/saved-post')">
          <span class="icon"><el-icon><Star /></el-icon></span>
          <span>Saved Post</span>
        </div>
      </div>

      <!-- AI Career Connect -->
      <div class="menu-item">
        <span class="icon"><el-icon><Link /></el-icon></span>
        <span class="title">Job Forecasting</span>
      </div>
      <div class="submenu">
        <div class="submenu-item" @click="goTo('/job-opportunity')">
          <span class="icon"><el-icon><Briefcase /></el-icon></span>
          <span>Job Opportunity</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #f8f9fa;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  padding: 15px;
}

.sidebar-header img {
  max-width: 180px;
  margin-bottom: 20px;
}

.menu {
  width: 100%;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  transition: background 0.3s;
}

.menu-item:hover {
  background-color: #e0e0e0;
}

.icon {
  margin-right: 10px;
}

.submenu {
  padding-left: 30px;
}

.submenu-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  font-size: 14px;
  color: #555;
  cursor: pointer;
  transition: all 0.3s;
}

.submenu-item:hover {
  background-color: #e9ecef;
  color: #333;
}

/* Add some visual hierarchy */
.submenu-item:not(:last-child) {
  margin-bottom: 2px;
}

/* Active state for menu items */
.submenu-item.router-link-active {
  background-color: #e0e0e0;
  color: #333;
  font-weight: 500;
}
</style>