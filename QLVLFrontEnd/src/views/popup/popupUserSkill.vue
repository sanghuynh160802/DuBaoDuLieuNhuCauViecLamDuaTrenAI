<template>
  <div class="popup-overlay" @click.self="emitClose">
    <div class="popup-container">
      <div class="popup-header">
        <h2>Add New Skill</h2>
        <button class="close-btn" @click="emitClose">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="skill-form">
        <div class="form-section">
          <h3 class="section-title">Skill Information</h3>
          <div class="form-row">
            <div class="form-group full-width">
              <label for="skill">Skill Name*</label>
              <input
                id="skill"
                type="text"
                v-model="skillData.skill"
                required
                placeholder="e.g. JavaScript, Python, UI/UX Design"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="level">Proficiency Level</label>
              <el-select
                id="level"
                v-model="skillData.level"
                placeholder="Select level"
                clearable
                :popper-class="'custom-el-select-dropdown'"
              >
                <el-option
                  v-for="level in levels"
                  :key="level"
                  :label="level"
                  :value="level"
                />
              </el-select>
            </div>
            <div class="form-group">
              <label for="experience">Experience</label>
              <el-select
                id="experience"
                v-model="skillData.experience"
                placeholder="Select experience"
                clearable
                :popper-class="'custom-el-select-dropdown'"
              >
                <el-option
                  v-for="exp in experienceLevels"
                  :key="exp"
                  :label="exp"
                  :value="exp"
                />
              </el-select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3 class="section-title">Work Details</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="workway">Work Type</label>
              <el-select
                id="workway"
                v-model="skillData.work_way"
                placeholder="Select type"
                clearable
                :popper-class="'custom-el-select-dropdown'"
              >
                <el-option
                  v-for="workway in workWays"
                  :key="workway"
                  :label="workway"
                  :value="workway"
                />
              </el-select>
            </div>
            <div class="form-group">
              <label for="city">Location</label>
              <el-select
                id="city"
                v-model="skillData.city"
                placeholder="Select location"
                clearable
                :popper-class="'custom-el-select-dropdown'"
              >
                <el-option
                  v-for="province in provinces"
                  :key="province.code"
                  :label="province.name"
                  :value="province.name"
                />
              </el-select>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="emitClose">Cancel</button>
          <button type="submit" class="submit-btn">Add Skill</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import { ElNotification } from "element-plus";
import { createUserSkill, getAllLevels, getAllWorkWays, getAllExperiences } from "@/services/user.service";
import axios from "axios";
import { useAuthStore } from '@/stores/auth'; // Import auth store

const authStore = useAuthStore();
const props = defineProps<{
  userId: string;
}>();

const emits = defineEmits<{
  (e: "close"): void;
  (e: "skill-added"): void;
}>();

const skillData = ref({
  user_id: authStore.getUserID(), // Get user ID from auth store instead of props
  level: "",
  skill: "",
  experience: "",
  work_way: "",
  city: ""
});

// Reactive arrays for selects
const levels = ref<string[]>([]);
const workWays = ref<string[]>([]);
const experienceLevels = ref<string[]>([]);
const provinces = ref<Array<{ code: number; name: string }>>([]);

// Fetch provinces with priority cities and proper sorting
const getProvinces = async () => {
  try {
    const response = await axios.get("https://provinces.open-api.vn/api/");
    const cleanedProvinces = response.data.map((province: { code: number; name: string }) => ({
      ...province,
      name: province.name.replace('Tỉnh ', '').replace('Thành phố ', '')
    }));

    const priorityCities = ['Hà Nội', 'Hồ Chí Minh', 'Đà Nẵng'];
    const prioritized = cleanedProvinces.filter(p => priorityCities.includes(p.name));
    const others = cleanedProvinces
      .filter(p => !priorityCities.includes(p.name))
      .sort((a, b) => a.name.localeCompare(b.name));

    provinces.value = [...prioritized, ...others];
  } catch (error) {
    console.error("Error fetching provinces:", error);
  }
};

// Fetch all dropdown data before component mounts
onBeforeMount(async () => {
  try {
    levels.value = await getAllLevels();
    workWays.value = await getAllWorkWays();
    experienceLevels.value = await getAllExperiences();
    await getProvinces();
    
    // Ensure user_id is set
    skillData.value.user_id = authStore.getUserID();
  } catch (error) {
    console.error("Error loading dropdown data:", error);
  }
});

const emitClose = () => {
  emits("close");
};

const handleSubmit = async () => {
  try {
    // Validate required fields
    if (!skillData.value.skill) {
      ElNotification({
        title: "Error",
        message: "Skill name is required",
        type: "error",
      });
      return;
    }

    // Ensure user_id is set
    if (!skillData.value.user_id) {
      skillData.value.user_id = authStore.getUserID();
    }

    // Create payload object
    const payload = {
      user_id: skillData.value.user_id,
      level: skillData.value.level,
      skill: skillData.value.skill,
      experience: skillData.value.experience,
      work_way: skillData.value.work_way,
      city: skillData.value.city
    };

    // Call the createUserSkill service
    const response = await createUserSkill(payload);

    if (response.data) {
      ElNotification({
        title: "Success",
        message: "Skill added successfully!",
        type: "success",
      });

      emits("skill-added");
      emitClose();
      
      // Reset form
      skillData.value = {
        user_id: authStore.getUserID(), // Reset with current user ID
        level: "",
        skill: "",
        experience: "",
        work_way: "",
        city: ""
      };
    }
  } catch (error) {
    console.error("Error adding skill:", error);
    let errorMessage = "Failed to add skill. Please try again.";
    
    if (error.response && error.response.data && error.response.data.message) {
      errorMessage = error.response.data.message;
    }

    ElNotification({
      title: "Error",
      message: errorMessage,
      type: "error",
    });
  }
};
</script>

<style scoped>
/* Reuse base styles, then enhance for el-select */

.popup-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-container {
  background-color: #fff;
  border-radius: 12px;
  width: 600px;
  max-width: 95vw;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  padding-bottom: 20px; /* extra padding for dropdown space */
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #eaeaea;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.popup-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2d3748;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #718096;
  cursor: pointer;
  padding: 5px;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #2d3748;
}

.skill-form {
  padding: 0 25px 25px;
}

.form-section {
  margin-bottom: 25px;
}

.section-title {
  font-size: 1.1rem;
  color: #2d3748;
  margin: 20px 0 15px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f2f5;
  font-weight: 700;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
  margin-bottom: 10px;
}

.form-group.full-width {
  flex: 0 0 100%;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  color: #4a5568;
  user-select: none;
}

/* Input styling */
input[type="text"] {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: all 0.2s;
  background-color: #f8fafc;
}

input[type="text"]:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
  background-color: white;
}

/* Element Plus el-select base styling override */
.el-select {
  width: 100%;
  font-size: 0.95rem;
}

.el-select .el-input__inner {
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background-color: #f8fafc;
  padding-left: 12px;
  transition: all 0.2s;
  height: 38px; /* consistent height */
  font-weight: 400;
  color: #2d3748;
}

.el-select .el-input__inner:hover {
  border-color: #a0aec0;
}

.el-select.is-focus .el-input__inner {
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
  background-color: white;
}

/* Dropdown panel custom styling */
.custom-el-select-dropdown {
  border-radius: 8px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  font-size: 0.95rem !important;
  color: #2d3748 !important;
}

/* Dropdown option hover and selected */
.el-select-dropdown__item:hover {
  background-color: #ebf8ff !important;
  color: #3182ce !important;
}

.el-select-dropdown__item.selected {
  background-color: #4299e1 !important;
  color: white !important;
  font-weight: 600 !important;
}

/* Scrollbar styling for dropdown */
.el-select-dropdown__wrap::-webkit-scrollbar {
  width: 6px;
}

.el-select-dropdown__wrap::-webkit-scrollbar-thumb {
  background-color: rgba(66, 153, 225, 0.5);
  border-radius: 3px;
}

.el-select-dropdown__wrap::-webkit-scrollbar-track {
  background-color: transparent;
}

/* Form actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
  padding-top: 15px;
  border-top: 1px solid #eaeaea;
}

.cancel-btn,
.submit-btn {
  padding: 10px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 100px;
}

.cancel-btn {
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #4a5568;
}

.cancel-btn:hover {
  background-color: #edf2f7;
}

.submit-btn {
  background-color: #4299e1;
  border: none;
  color: white;
}

.submit-btn:hover {
  background-color: #3182ce;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 15px;
  }

  .popup-container {
    width: 95vw;
  }
}
</style>