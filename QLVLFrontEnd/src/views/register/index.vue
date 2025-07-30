<script setup lang="ts">
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"
import { ref } from "vue"
import { ISignUp } from "@/types/user"
import { registerApi } from "@/services/user.service"
import { ElNotification } from "element-plus"

const auth = useAuthStore()
const router = useRouter()

const user = ref<ISignUp>({
    email: "",
    name: "",
    password: "",
    avatar: "",
    age: null,
    user_type: "APPLICANT" // Default user_type
})

const isEnterValue = ref<boolean[]>([false])
const isMatchPassword = ref<boolean>(false)
const rePassword = ref<string>("")
const isEmployer = ref<boolean>(false)

const signUp = async () => {
    try {
        if (!checkInput()) {
            return
        }
        if (rePassword.value != user.value.password) {
            isMatchPassword.value = true
            return
        }
        isMatchPassword.value = false
        
        user.value.user_type = isEmployer.value ? "EMPLOYER" : "APPLICANT"
        
        await registerApi(user.value)
        ElNotification({
            title: "Success",
            message: "Account created successfully!",
            type: "success",
        })
        router.push("/login")
    } catch (error) {
        ElNotification({
            title: "Error", 
            message: "Registration failed. Please try again.",
            type: "error",
        })
        console.error(error)
    }
}

const checkInput: () => boolean = () => {
    isEnterValue.value[0] = !user.value.email
    isEnterValue.value[1] = !user.value.name
    isEnterValue.value[2] = !user.value.password
    isEnterValue.value[3] = !rePassword.value
    return !isEnterValue.value.some((value) => value === true)
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <h1>Join Us</h1>
                <p>Create your account to get started</p>
            </div>
            
            <div class="auth-form">
                <div class="form-group">
                    <label>Full Name</label>
                    <el-input 
                        v-model="user.name" 
                        placeholder="Enter your full name"
                        class="modern-input"
                    />
                    <span class="error-message" v-show="isEnterValue[1]">Name is required</span>
                </div>
                
                <div class="form-group">
                    <label>Age (Optional)</label>
                    <el-input 
                        v-model="user.age" 
                        type="number" 
                        placeholder="Enter your age"
                        class="modern-input"
                    />
                </div>
                <div class="form-group">
                    <label>Email Address</label>
                    <el-input 
                        v-model="user.email" 
                        type="email" 
                        placeholder="Enter your email"
                        class="modern-input"
                    />
                    <span class="error-message" v-show="isEnterValue[0]">Email is required</span>
                </div>                
                <div class="form-group">
                    <label>Password</label>
                    <el-input 
                        v-model="user.password" 
                        type="password" 
                        placeholder="Create a password"
                        show-password
                        class="modern-input"
                    />
                    <span class="error-message" v-show="isEnterValue[2]">Password is required</span>
                </div>
                
                <div class="form-group">
                    <label>Confirm Password</label>
                    <el-input 
                        v-model="rePassword" 
                        type="password" 
                        placeholder="Confirm your password"
                        show-password
                        class="modern-input"
                    />
                    <span class="error-message" v-show="isEnterValue[3]">Please confirm password</span>
                </div>
                
                <div class="employer-option">
                    <div class="employer-toggle">
                        <el-checkbox v-model="isEmployer" size="large" class="employer-checkbox">
                            <span class="employer-label">I'm an Employer (Nhà tuyển dụng)</span>
                        </el-checkbox>
                    </div>
                </div>
                
                <span class="error-message" v-show="isMatchPassword">Passwords don't match</span>
                
                <button @click="signUp" class="auth-button">
                    Create Account
                </button>
                
                <div class="auth-footer">
                    <span>Already have an account?</span>
                    <el-link type="primary" href="/login">Sign In</el-link>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #f6f9fc 0%, #e8f0fe 100%);
    padding: 2rem;
}

.auth-card {
    width: 100%;
    max-width: 480px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeIn 0.5s ease-out;
    
    &:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
}

.auth-header {
    padding: 2.5rem 2rem 1.5rem;
    text-align: center;
    background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
    color: white;
    
    h1 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    p {
        font-size: 0.95rem;
        opacity: 0.9;
    }
}

.auth-form {
    padding: 2rem;
    
    .form-group {
        margin-bottom: 1.5rem;
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            font-weight: 500;
            color: #4a5568;
        }
    }
}

.employer-option {
    margin: 1.5rem 0;
    padding: 1rem;
    background-color: #f8fafc;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    
    .employer-toggle {
        display: flex;
        align-items: center;
    }
    
    .employer-checkbox {
        :deep(.el-checkbox__label) {
            font-size: 1rem;
            font-weight: 500;
            color: #4a5568;
        }
        
        :deep(.el-checkbox__inner) {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 1px solid #cbd5e0;
            
            &::after {
                height: 10px;
                left: 6px;
                top: 2px;
                width: 5px;
            }
        }
    }
    
    .employer-label {
        margin-left: 10px;
    }
}

.modern-input {
    :deep(.el-input__wrapper) {
        border-radius: 8px;
        padding: 0.8rem 1rem;
        box-shadow: 0 0 0 1px #e2e8f0 inset;
        transition: all 0.3s ease;
        
        &:hover {
            box-shadow: 0 0 0 1px #cbd5e0 inset;
        }
        
        &:focus-within {
            box-shadow: 0 0 0 2px #4361ee inset;
        }
    }
}

.error-message {
    display: block;
    margin-top: 0.5rem;
    font-size: 0.8rem;
    color: #e53e3e;
    animation: shake 0.5s;
}

.auth-button {
    width: 100%;
    padding: 1rem;
    background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    
    &:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(67, 97, 238, 0.2);
    }
    
    &:active {
        transform: translateY(0);
    }
}

.auth-footer {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 0.9rem;
    color: #718096;
    
    span {
        margin-right: 0.5rem;
    }
    
    .el-link {
        font-size: 0.9rem;
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-5px); }
    40%, 80% { transform: translateX(5px); }
}

@media (max-width: 640px) {
    .auth-container {
        padding: 1rem;
    }
    
    .auth-card {
        border-radius: 12px;
    }
    
    .auth-header {
        padding: 1.5rem 1rem;
    }
    
    .auth-form {
        padding: 1.5rem;
    }
    
    .employer-option {
        padding: 0.8rem;
    }
}
</style>