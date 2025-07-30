<script setup lang="ts">
import { ref } from "vue"
import type { IUser, IUpdate } from "@/types/user"
import { updateInfo } from "@/services/user.service"
import { ElNotification } from "element-plus"

const props = defineProps<{
  user: IUser
}>()

const emit = defineEmits(['close', 'success'])

const userData = ref<IUpdate>({
  id: props.user.id, // Include the user ID
  name: props.user.name,
  email: props.user.email,
  age: props.user.age,
  password: "",
  avatar: props.user.avatar,
  user_type: props.user.user_type
})

const isEnterValue = ref<boolean[]>([false])
const isLoading = ref<boolean>(false)

const updateUser = async () => {
  try {
    if (!checkInput()) {
      return
    }
    
    isLoading.value = true
    
    await updateInfo(userData.value)
    ElNotification({
      title: "Success",
      message: "User updated successfully!",
      type: "success",
    })
    emit('success')
    emit('close')
  } catch (error) {
    ElNotification({
      title: "Error", 
      message: "Update failed. Please try again.",
      type: "error",
    })
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const checkInput: () => boolean = () => {
  isEnterValue.value[0] = !userData.value.name
  isEnterValue.value[1] = !userData.value.email
  return !isEnterValue.value.some((value) => value === true)
}
</script>

<template>
  <div class="popup-overlay">
    <div class="popup-content">
      <div class="popup-header">
        <h2>Update User</h2>
        <el-button 
          circle 
          icon="Close" 
          @click="emit('close')" 
          class="close-button"
        />
      </div>
      
      <div class="popup-body">
        <div class="form-group">
          <label>Full Name</label>
          <el-input 
            v-model="userData.name" 
            placeholder="Enter full name"
            class="popup-input"
          />
          <span class="error-message" v-show="isEnterValue[0]">Name is required</span>
        </div>
        
        <div class="form-group">
          <label>Age</label>
          <el-input 
            v-model="userData.age" 
            type="number" 
            placeholder="Enter age"
            class="popup-input"
          />
        </div>
        
        <div class="form-group">
          <label>Email Address</label>
          <el-input 
            v-model="userData.email" 
            type="email" 
            placeholder="Enter email"
            class="popup-input"
          />
          <span class="error-message" v-show="isEnterValue[1]">Email is required</span>
        </div>                
        
        <div class="form-group">
          <label>New Password (Leave blank to keep current)</label>
          <el-input 
            v-model="userData.password" 
            type="password" 
            placeholder="Enter new password"
            show-password
            class="popup-input"
          />
        </div>
        
        <div class="form-group">
          <label>User Type</label>
          <el-select 
            v-model="userData.user_type" 
            placeholder="Select user type"
            class="popup-input"
          >
            <el-option label="Applicant" value="APPLICANT" />
            <el-option label="Employer" value="EMPLOYER" />
          </el-select>
        </div>
      </div>
      
      <div class="popup-footer">
        <el-button @click="emit('close')">
          Cancel
        </el-button>
        <el-button 
          type="primary" 
          @click="updateUser" 
          :loading="isLoading"
        >
          Update User
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