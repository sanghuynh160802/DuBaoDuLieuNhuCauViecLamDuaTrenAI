<script setup lang="ts">
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"
import { ref } from "vue"
import { ILogin } from "@/types/user"
import { loginApi, getInfo } from "@/services/user.service"
import { initAuthStore } from "@/stores"
import { jwtDecode } from "jwt-decode"
import { ElNotification } from "element-plus"
import { Lock, User, ArrowRight } from "@element-plus/icons-vue"

const user = ref<ILogin>({
  email: "",
  password: "",
})
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

const submit = async () => {
  loading.value = true
  try {
    const response = await loginApi({
      email: user.value.email,
      password: user.value.password,
    })

    const data = response.data
    const { access_token, refresh_token } = data.data

    localStorage.setItem("access_token", access_token)
    localStorage.setItem("refresh_token", refresh_token)

    if (access_token) {
      const decodedToken = jwtDecode<{ role: string }>(access_token)
      const role = decodedToken.role

      initAuthStore()

      const redirectPath = role === "admin" ? "/dashboard" : "/user"
      router.push(redirectPath)

      ElNotification({
        title: "Success",
        message: "Login successful!",
        type: "success",
      })
    }
  } catch (error) {
    console.error(error)
    ElNotification({
      title: "Error",
      message: "Invalid email or password",
      type: "error",
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-background">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <div class="login-container">
      <div class="login-header">
        <h1>Welcome Back</h1>
        <p>Please enter your credentials to login</p>
      </div>

      <div class="login-form">
        <div class="form-group">
          <label>Email Address</label>
          <el-input
            v-model="user.email"
            placeholder="Enter your email"
            :prefix-icon="User"
            size="large"
            class="custom-input"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <el-input
            v-model="user.password"
            type="password"
            placeholder="Enter your password"
            :prefix-icon="Lock"
            show-password
            size="large"
            class="custom-input"
          />
        </div>

        <div class="forgot-password">
          <el-link type="info" href="/forgotpassword">Forgot Password?</el-link>
        </div>

        <el-button
          @click="submit"
          type="primary"
          size="large"
          :loading="loading"
          class="login-button"
        >
          Sign In
          <el-icon class="button-icon"><ArrowRight /></el-icon>
        </el-button>

        <div class="signup-link">
          Don't have an account?
          <el-link type="primary" href="/register">Sign up</el-link>
        </div>
      </div>

      <div class="social-login">
        <p>Or continue with</p>
        <div class="social-icons">
          <div class="social-icon google">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
          </div>
          <div class="social-icon facebook">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" fill="#1877F2"/>
            </svg>
          </div>
          <div class="social-icon linkedin">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="#0A66C2"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  height: 100%;
  min-height: calc(100vh - 56px);
  width: 100%;
  overflow: hidden;
  position: relative;
}

.login-background {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;

  .shape {
    position: absolute;
    border-radius: 50%;
    backdrop-filter: blur(5px);

    &-1 {
      width: 300px;
      height: 300px;
      top: -50px;
      left: -50px;
      background: linear-gradient(45deg, #667eea, #764ba2);
      opacity: 0.8;
    }

    &-2 {
      width: 200px;
      height: 200px;
      bottom: -30px;
      right: -30px;
      background: linear-gradient(45deg, #ff9a9e, #fad0c4);
      opacity: 0.6;
    }

    &-3 {
      width: 150px;
      height: 150px;
      bottom: 20%;
      left: 10%;
      background: linear-gradient(45deg, #a1c4fd, #c2e9fb);
      opacity: 0.4;
    }
  }
}

.login-container {
  z-index: 1;
  max-width: 450px;
  width: 90%;
  margin: 20px auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  padding: 40px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  h1 {
    font-size: 28px;
    font-weight: 700;
    color: #2c3e50;
  }

  p {
    font-size: 16px;
    color: #7f8c8d;
  }
}

.login-form {
  .form-group {
    margin-bottom: 25px;

    label {
      font-weight: 500;
      font-size: 14px;
      color: #2c3e50;
      margin-bottom: 8px;
      display: block;
    }
  }

  .custom-input {
    :deep(.el-input__wrapper) {
      padding: 12px 15px;
      border-radius: 8px;
      border: 1px solid #e0e0e0;
      transition: all 0.3s ease;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

      &:hover {
        border-color: #667eea;
      }

      &.is-focus {
        box-shadow: 0 0 0 1px #667eea inset;
      }
    }
  }
}

.forgot-password {
  text-align: right;
  margin-bottom: 25px;

  .el-link {
    font-size: 13px;
  }
}

.login-button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  margin-bottom: 25px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
  }

  .button-icon {
    margin-left: 8px;
    transition: transform 0.3s ease;
  }

  &:hover .button-icon {
    transform: translateX(3px);
  }
}

.signup-link {
  text-align: center;
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 20px;

  .el-link {
    font-weight: 600;
    margin-left: 4px;
  }
}

.social-login {
  margin-top: 20px;
  text-align: center;

  p {
    font-size: 14px;
    color: #7f8c8d;
    margin-bottom: 15px;
    position: relative;
    
    &::before,
    &::after {
      content: "";
      position: absolute;
      top: 50%;
      width: 30%;
      height: 1px;
      background: #e0e0e0;
    }
    
    &::before {
      left: 0;
    }
    
    &::after {
      right: 0;
    }
  }

  .social-icons {
    display: flex;
    justify-content: center;
    gap: 15px;

    .social-icon {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s ease;
      background: white;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

      &:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
      }

      svg {
        width: 18px;
        height: 18px;
      }

      &.facebook {
        background: #1877f2;
        
        svg {
          fill: white;
        }
      }

      &.linkedin {
        background: #0a66c2;
        
        svg {
          fill: white;
        }
      }
    }
  }
}
</style>