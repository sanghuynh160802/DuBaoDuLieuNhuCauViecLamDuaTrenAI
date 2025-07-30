<template>
  <div class="popup-overlay">
    <div class="popup-container">
      <h2>Update Job</h2>
      <div class="form-grid">
        <!-- Row 1 -->
        <div class="input-group">
          <label for="title">Title</label>
          <input id="title" type="text" v-model="updateJobS.Title" />
        </div>
        <div class="input-group">
          <label for="company">Company</label>
          <input id="company" type="text" v-model="updateJobS.Company_Name" />
        </div>

        <!-- Row 2 - Modified to include Place next to City -->
        <div class="input-group">
          <label for="city">City</label>
          <input id="city" type="text" v-model="updateJobS.City" />
        </div>
        <div class="input-group">
          <label for="place">Place</label>
          <input id="place" type="text" v-model="updateJobS.Place" />
        </div>

        <!-- Row 3 - Modified to include Skills next to Level -->
        <div class="input-group">
          <label for="level">Level</label>
          <input id="level" type="text" v-model="updateJobS.Level" />
        </div>
        <div class="input-group">
          <label for="skills">Skills</label>
          <input id="skills" type="text" v-model="updateJobS.Skills" />
        </div>

        <!-- Row 4 -->
        <div class="input-group">
          <label for="profession">Profession</label>
          <input id="profession" type="text" v-model="updateJobS.Profession" />
        </div>
        <div class="input-group">
          <label for="work_way">Work Way</label>
          <input id="work_way" type="text" v-model="updateJobS.Work_Way" />
        </div>

        <!-- Row 5 -->
        <div class="input-group">
          <label for="number_recruitment">Number Recruitment</label>
          <input id="number_recruitment" type="number" v-model="updateJobS.Number_Recruitment" />
        </div>
        <div class="input-group">
          <label for="experience">Experience</label>
          <input id="experience" type="text" v-model="updateJobS.Experience" />
        </div>

        <!-- Row 6 -->
        <div class="input-group">
          <label for="education">Education</label>
          <input id="education" type="text" v-model="updateJobS.Education" />
        </div>
        <div class="input-group">
          <label for="probation_time">Probation Time</label>
          <input id="probation_time" type="text" v-model="updateJobS.Probation_Time" />
        </div>

        <!-- Row 7 -->
        <div class="input-group">
          <label for="salary">Salary</label>
          <input id="salary" type="text" v-model="updateJobS.Salary" />
        </div>
        <div class="input-group">
          <label for="deadline">Deadline</label>
          <input id="deadline" type="date" v-model="updateJobS.Deadline" />
        </div>

        <!-- Row 8 - Added Source_Picture and Job_URL -->
        <div class="input-group">
          <label for="source_picture">Image URL</label>
          <input id="source_picture" type="text" v-model="updateJobS.Source_Picture" placeholder="https://example.com/image.jpg" />
        </div>
        <div class="input-group">
          <label for="job_url">Job URL</label>
          <input id="job_url" type="text" v-model="updateJobS.Job_URL" placeholder="https://example.com/job" />
        </div>

        <!-- Full width fields -->
        <div class="input-group full-width">
          <label for="description">Description</label>
          <textarea id="description" v-model="updateJobS.Description"></textarea>
        </div>

        <div class="input-group full-width">
          <label for="requirement">Requirement</label>
          <textarea id="requirement" v-model="updateJobS.Requirement"></textarea>
        </div>

        <div class="input-group full-width">
          <label for="right">Right</label>
          <textarea id="right" v-model="updateJobS.Right"></textarea>
        </div>
      </div>

      <div class="button-popup">
        <button @click="handleUpdate">Update</button>
        <button @click="emits('close-popup')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, watch } from "vue";
import type { IJob, IJobUpdate } from "@/types/auth";
import { useRoute, useRouter } from "vue-router";
import { getJobID, updateJob } from "@/services/user.service";
import { ElNotification } from "element-plus";

const emits = defineEmits<{
  (e: "close-popup"): void;
  (e: "job-updated", job: IJobUpdate): void;
}>();
const props = defineProps<{
  idChoose: string
}>()

const jobUpdate = ref<IJobUpdate>();

onBeforeMount(async () => {
  await getJobtoUpdate();
});

const updateJobS = ref<IJobUpdate>({
  Title: '',
  Company_Name: '',
  Place: '',
  Salary: '',
  Level: '',
  City: '',
  Profession: '',
  Work_Way: '',
  Number_Recruitment: 0,
  Experience: '',
  Education: '',
  Description: '',
  Requirement: '',
  Right: '',
  Skills: '',
  Probation_Time: '',
  Deadline: '',
  Source_Picture: '',  // Added field
  Job_URL: ''         // Added field
});

watch(jobUpdate, (newValue) => {
  if (newValue) {
    updateJobS.value = {
      Title: newValue.Title || '',
      Company_Name: newValue.Company_Name || '',
      Place: newValue.Place || '',
      Salary: newValue.Salary || '',
      Level: newValue.Level || '',
      City: newValue.City || '',
      Profession: newValue.Profession || '',
      Work_Way: newValue.Work_Way || '',
      Number_Recruitment: newValue.Number_Recruitment || 0,
      Experience: newValue.Experience || '',
      Education: newValue.Education || '',
      Description: newValue.Description || '',
      Requirement: newValue.Requirement || '',
      Right: newValue.Right || '',
      Skills: newValue.Skills || '',
      Probation_Time: newValue.Probation_Time || '',
      Deadline: newValue.Deadline || '',
      Source_Picture: newValue.Source_Picture || '',  // Added field
      Job_URL: newValue.Job_URL || ''               // Added field
    };
  }
});

const getJobtoUpdate = async (): Promise<void> => {
  try {
    const res = await getJobID(props.idChoose);
    jobUpdate.value = res.data;
  } catch (error) {
    console.log("error", error);
  }
};

const handleUpdate = async (): Promise<void> => {
  try {
    if (jobUpdate.value) {
      await updateJob(props.idChoose, updateJobS.value);
      emits('job-updated', updateJobS.value);
      emits('close-popup');
    }
  } catch (error) {
    console.log("Error updating job", error);
    ElNotification({
      title: "Error",
      message: "Update Failed!",
      type: "error",
    });
  }
};
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-container {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
}

.popup-container h2 {
  padding-bottom: 20px;
  text-align: center;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 10px;
}

.input-group.full-width {
  grid-column: span 2;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

input[type="text"],
input[type="number"],
input[type="date"],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  font-family: inherit;
}

textarea {
  min-height: 80px;
  resize: vertical;
}

.button-popup {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
}

button {
  padding: 10px 25px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #0056b3;
}

button:last-child {
  background-color: #6c757d;
}

button:last-child:hover {
  background-color: #5a6268;
}

@media (max-width: 850px) {
  .popup-container {
    width: 90%;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .input-group.full-width {
    grid-column: span 1;
  }
}
</style>