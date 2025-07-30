<template>
  <div class="nav-container">
    <div class="nav-container__body">
      <div class="logo-job" role="img" aria-label="ITF DUT Job Search Logo">
        <svg
          viewBox="0 0 160 180"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="xMidYMid meet"
        >
          <!-- Red circle with white ITF -->
          <circle cx="30" cy="30" r="25" fill="#C1272D" />
          <text
            x="30"
            y="38"
            text-anchor="middle"
            font-family="Arial, sans-serif"
            font-size="24"
            font-weight="bold"
            fill="white"
          >
            ITF
          </text>

          <!-- DUT text to the right -->
          <text
            x="70"
            y="42"
            font-family="Arial, sans-serif"
            font-size="28"
            font-weight="bold"
            fill="white"
          >
            DUT
          </text>

          <!-- JOB text with magnifying glass as O -->
          <text
            x="10"
            y="110"
            font-family="Arial, sans-serif"
            font-size="72"
            font-weight="bold"
            fill="white"
          >
            J
          </text>

          <!-- Magnifying glass circle for O -->
          <circle cx="75" cy="70" r="35" fill="none" stroke="white" stroke-width="10" />
          <!-- Magnifying glass handle -->
          <rect
            x="95"
            y="95"
            width="15"
            height="40"
            rx="7"
            ry="7"
            fill="white"
            transform="rotate(-45 102 115)"
          />

          <!-- B letter -->
          <text
            x="115"
            y="110"
            font-family="Arial, sans-serif"
            font-size="72"
            font-weight="bold"
            fill="white"
          >
            B
          </text>

          <!-- Sang text below -->
          <text
            x="50"
            y="150"
            font-family="Arial, sans-serif"
            font-size="24"
            fill="white"
          >
            Sang
          </text>
        </svg>
      </div>

      <!-- Nav Menu Items -->
      <div class="nav-menu">
        <a class="nav-menu__item" @click="goToJob()">Tìm việc làm</a>
        <a class="nav-menu__item" @click="goToTrends()">Xu hướng việc làm</a>
      </div>

      <div class="nav-container__body__action" v-if="!authStore.getIsLoggedIn()">
        <el-button type="primary" @click="goToLogin">Login</el-button>
      </div>
      <div class="nav-container__body__info" v-else>
        <div class="avatar-flex" @click="goToUser()">
          <img :src="authStore.getAvatar()" alt="avatar" />
          <p>{{ authStore.getUserName() }}</p>
        </div>
        <div class="dropdown">
          <button class="dropbtn">
            Menu
            <el-icon><CaretBottom /></el-icon>
          </button>
          <div class="dropdown-content">
            <a @click="goToJob()">Việc làm</a>
            <a @click="goToUser()">Tài khoản</a>
            <a @click="logout()">Đăng xuất</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "../stores/auth"

defineProps<{}>()
const router = useRouter()
const authStore = useAuthStore()

const goToLogin = () => {
  router.push("/login")
}
const goToJob = () => {
  router.push("/mainjob")
}
const goToUser = () => {
  router.push("/user")
}
const goToRegister = () => {
  router.push("/register")
}
const goToTrends = () => {
  router.push("/job-forecasting")
}

const logout = async () => {
  try {
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    authStore.setAuthStore({
      user: {
        email: "",
        password: "",
      },
      isLoggedIn: false,
      isAdmin: false,
    })
    router.push("/login")
  } catch (error) {
    console.error(error)
  }
}
</script>

<style lang="scss" scoped>
.nav-container {
  z-index: 999;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 72px;
  display: flex;
  justify-content: center;
  border-bottom: 1px solid #004080;
  background-color: #003366;

  &__body {
    width: 100%;
    max-width: 1440px;
    padding: 0 20px;
    display: flex;
    align-items: center;
    gap: 40px;
  }
}

.logo-job {
  height: 72px;
  width: auto;
  display: flex;
  align-items: center;
  flex-shrink: 0;

  svg {
    height: 100%;
    width: auto;
    display: block;
  }
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-right: auto; /* Pushes everything after it to the right */

  &__item {
    font-size: 14px;
    font-weight: 500;
    color: white;
    text-decoration: none;
    cursor: pointer;
    position: relative;
    padding: 8px 0;

    &:hover {
      color: #00F0FF;
    }

    &::after {
      content: "";
      position: absolute;
      left: 0;
      bottom: -4px;
      width: 100%;
      height: 2px;
      background-color: #00F0FF;
      transform: scaleX(0);
      transition: transform 0.3s ease;
      transform-origin: right;
    }

    &:hover::after {
      transform: scaleX(1);
      transform-origin: left;
    }
  }
}

.nav-container__body__action {
  display: flex;
  gap: 12px;

  .el-button {
    font-weight: bold;
    font-size: 14px;
    padding: 10px 18px;
    border-radius: 8px;
    min-width: 120px;
    height: 42px;
    text-transform: none;
    transition: all 0.25s ease-in-out;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }

  .el-button--primary {
    background: linear-gradient(135deg, #00F0FF, #007CF0, #6A00FF);
    border: none;
    color: white;
    background-size: 200% auto;

    &:hover {
      background-position: right center;
      transform: scale(1.05);
    }

    &:active {
      transform: scale(0.97);
    }
  }

  .el-button--plain {
    background-color: #ffffff;
    border: 2px solid #00C2FF;
    color: #007CF0;

    &:hover {
      background-color: #e6f7ff;
      color: #005ecb;
      border-color: #009ee3;
      transform: scale(1.03);
    }

    &:active {
      transform: scale(0.97);
    }
  }
}

.nav-container__body__info {
  display: flex;
  align-items: center;
  gap: 5px;

  img {
    width: 30px;
    height: 30px;
    border-radius: 50%;
  }

  p {
    font-size: 12px;
    color: white;
  }
}

.avatar-flex {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 12px 5px;
  cursor: pointer;

  &:hover {
    background-color: rgba(255 255 255 / 0.1);
  }
}

.dropbtn {
  background-color: transparent;
  color: white;
  padding: 16px;
  font-size: 12px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;

  &:hover {
    background-color: rgba(255 255 255 / 0.1);
  }
}

.dropdown {
  position: relative;
  display: inline-block;
  font-size: 12px;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: white;
  top: 100%;
  left: 0;
  min-width: 120px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  z-index: 1000000;
  padding: 5px 0;

  a {
    color: black;
    padding: 10px 16px;
    text-decoration: none;
    display: block;
    font-size: 14px;

    &:hover {
      background-color: #f0f0f0;
    }
  }
}

.dropdown:hover .dropdown-content {
  display: block;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .nav-container__body {
    gap: 20px;
    padding: 0 10px;
  }
  
  .nav-menu {
    gap: 12px;
  }
  
  .logo-job svg {
    width: 120px; /* Adjust logo size on smaller screens */
  }
}
</style>