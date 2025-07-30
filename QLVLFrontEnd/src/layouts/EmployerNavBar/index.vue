<!--
<script setup lang="ts">
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"


    const router = useRouter()
    const goToDashBoard: () => void = () => {
        router.push("/dashboard")
    }
    const goToJob: () => void = () => {
        router.push("/mainjob")
    }
    const goToUser: () => void = () => {
        router.push("/user")
    }
</script>
<template>
    <div class="container-navbar-left">
        <div class="ava-nav-left">
            <img src="../../images/logodashboard.png" alt="Logo">
        </div>
        <div class="list-dashboard">    
            <div class="dashboard" @click="goToJob()">
                    <span class="icon"><el-icon><Operation /></el-icon></span>
                    <a >Thông tin việc làm</a>
            </div>
            <div class="dashboard" @click="goToUser()">
                    <span class="icon"><el-icon><Odometer /></el-icon></span>
                    <a >Thông tin tài khoản</a>
            </div>
            <div v-if="useAuthStore().getIsAdmin()" class="dashboard" @click="goToDashBoard()">
                    <span class="icon"><el-icon><User /></el-icon></span>
                    <a >Quản lí người dùng</a>
            </div>
        </div>  
    </div>
</template>
<style lang="scss" scoped>
.container-navbar-left {
    max-width: 250px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #e0e0e0; 
    align-items: center;
    gap: 20px;
    padding: 15px;
}
.ava-nav-left img {
    max-width: 200px;
    max-height: 200px;
}
.container-navbar-left a {
  text-decoration: none;
  font-size: 14px;
  color: gray;
}
.dashboard .icon {
    text-align: center;
    padding-right: 10px;
}
.dashboard .icon:hover {
    cursor: pointer;
}
.dashboard {
    padding: 20px;
    cursor: pointer;
}
.dashboard:hover {
    background-color: #e0e0e0;
}

</style>
-->




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
        <div class="submenu-item" @click="goTo('/post')">
          <span class="icon"><el-icon><Document /></el-icon></span>
          <span>Post</span>
        </div>
        <div class="submenu-item" @click="goTo('/cv-management')">
          <span class="icon"><el-icon><Document /></el-icon></span>
          <span>CV Management</span>
        </div>
      </div>

      <!-- AI Career Connect -->
      <div class="menu-item">
        <span class="icon"><el-icon><Link /></el-icon></span>
        <span class="title">AI Career Connect</span>
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
  transition: background 0.3s;
}

.submenu-item:hover {
  background-color: #e9ecef;
}
</style>
