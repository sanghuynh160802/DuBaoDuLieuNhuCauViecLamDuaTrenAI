<script setup lang="ts">
import { ref } from "vue"
import { ISignUp } from "@/types/user"
import { registerApi } from "@/services/user.service"
import { ElNotification } from "element-plus"

const emit = defineEmits(['close', 'success'])

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
const isLoading = ref<boolean>(false)

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
        isLoading.value = true
        
        await registerApi(user.value)
        ElNotification({
            title: "Success",
            message: "Account created successfully!",
            type: "success",
        })
        emit('success')
        emit('close')
    } catch (error) {
        ElNotification({
            title: "Error", 
            message: "Registration failed. Please try again.",
            type: "error",
        })
        console.error(error)
    } finally {
        isLoading.value = false
    }
}

const checkInput: () => boolean = () => {
    isEnterValue.value[0] = !user.value.email
    isEnterValue.value[1] = !user.value.name
    isEnterValue.value[2] = !user.value.password
    isEnterValue.value[3] = !rePassword.value
    return !isEnterValue.value.some((value) => value === true)
}

const resetForm = () => {
    user.value = {
        email: "",
        name: "",
        password: "",
        avatar: "",
        age: null,
        user_type: "APPLICANT"
    }
    rePassword.value = ""
    isEmployer.value = false
    isMatchPassword.value = false
    isEnterValue.value = [false]
}
</script>

<template>
    <div class="popup-overlay">
        <div class="popup-content">
            <div class="popup-header">
                <h2>Create New User</h2>
                <el-button 
                    circle 
                    icon="Close" 
                    @click="() => { resetForm(); emit('close'); }" 
                    class="close-button"
                />
            </div>
            
            <div class="popup-body">
                <div class="form-group">
                    <label>Full Name</label>
                    <el-input 
                        v-model="user.name" 
                        placeholder="Enter full name"
                        class="popup-input"
                    />
                    <span class="error-message" v-show="isEnterValue[1]">Name is required</span>
                </div>
                
                <div class="form-group">
                    <label>Age (Optional)</label>
                    <el-input 
                        v-model="user.age" 
                        type="number" 
                        placeholder="Enter age"
                        class="popup-input"
                    />
                </div>
                
                <div class="form-group">
                    <label>Email Address</label>
                    <el-input 
                        v-model="user.email" 
                        type="email" 
                        placeholder="Enter email"
                        class="popup-input"
                    />
                    <span class="error-message" v-show="isEnterValue[0]">Email is required</span>
                </div>                
                
                <div class="form-group">
                    <label>Password</label>
                    <el-input 
                        v-model="user.password" 
                        type="password" 
                        placeholder="Create password"
                        show-password
                        class="popup-input"
                    />
                    <span class="error-message" v-show="isEnterValue[2]">Password is required</span>
                </div>
                
                <div class="form-group">
                    <label>Confirm Password</label>
                    <el-input 
                        v-model="rePassword" 
                        type="password" 
                        placeholder="Confirm password"
                        show-password
                        class="popup-input"
                    />
                    <span class="error-message" v-show="isEnterValue[3]">Please confirm password</span>
                </div>
                
                <div class="employer-option">
                    <el-checkbox v-model="isEmployer" size="large" class="employer-checkbox">
                        <span class="employer-label">This user is an Employer</span>
                    </el-checkbox>
                </div>
                
                <span class="error-message" v-show="isMatchPassword">Passwords don't match</span>
            </div>
            
            <div class="popup-footer">
                <el-button @click="() => { resetForm(); emit('close'); }">
                    Cancel
                </el-button>
                <el-button 
                    type="primary" 
                    @click="signUp" 
                    :loading="isLoading"
                >
                    Create User
                </el-button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.popup-content {
    background-color: white;
    border-radius: 8px;
    width: 450px;
    max-width: 90%;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid #eee;
}

.popup-header h2 {
    margin: 0;
    font-size: 1.25rem;
    color: #333;
}

.close-button {
    border: none;
    background: transparent;
    font-size: 1rem;
}

.popup-body {
    padding: 20px;
}

.form-group {
    margin-bottom: 16px;
}

.form-group label {
    display: block;
    margin-bottom: 6px;
    font-size: 0.875rem;
    color: #666;
}

.popup-input {
    width: 100%;
}

.employer-option {
    margin: 16px 0;
}

.employer-label {
    font-size: 0.875rem;
}

.error-message {
    color: #f56c6c;
    font-size: 0.75rem;
    margin-top: 4px;
    display: block;
}

.popup-footer {
    display: flex;
    justify-content: flex-end;
    padding: 12px 20px;
    border-top: 1px solid #eee;
    gap: 10px;
}
</style>