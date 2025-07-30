<template>
  <div class="popup-overlay" @click.self="emitClose">
    <div class="popup-container">
      <div class="popup-header">
        <h2>Post a New Job</h2>
        <button class="close-btn" @click="emitClose">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="handlePost" class="job-form">
        <div class="form-section">
          <h3 class="section-title">Basic Information</h3>
          <div class="form-row">
            <div class="form-group full-width">
              <label for="title">Job Title*</label>
              <input id="title" type="text" v-model="job.Title" required placeholder="e.g. Senior Frontend Developer" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="profession">Profession</label>
              <input id="profession" type="text" v-model="job.Profession" placeholder="e.g. Software Development" />
            </div>
            <div class="form-group">
              <label for="level">Level</label>
              <select id="level" v-model="job.Level">
                <option value="">Select level</option>
                <option value="Intern">Intern</option>
                <option value="Junior">Junior</option>
                <option value="Mid-level">Mid-level</option>
                <option value="Senior">Senior</option>
                <option value="Lead">Lead</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3 class="section-title">Job Details</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="place">Location*</label>
              <input id="place" type="text" v-model="job.Place" required placeholder="e.g. Ho Chi Minh City" />
            </div>
            <div class="form-group">
              <label for="workway">Work Type</label>
              <select id="workway" v-model="job.Work_Way">
                <option value="">Select type</option>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Remote">Remote</option>
                <option value="Hybrid">Hybrid</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="salary">Salary Range</label>
              <input id="salary" type="text" v-model="job.Salary" placeholder="e.g. $1,500 - $2,500" />
            </div>
            <div class="form-group">
              <label for="numrecruit">Open Positions</label>
              <input id="numrecruit" type="number" v-model="job.Number_Recruitment" min="1" placeholder="e.g. 3" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="experience">Experience</label>
              <select id="experience" v-model="job.Experience">
                <option value="">Select experience</option>
                <option value="No experience">No experience</option>
                <option value="1-2 years">1-2 years</option>
                <option value="3-5 years">3-5 years</option>
                <option value="5+ years">5+ years</option>
              </select>
            </div>
            <div class="form-group">
              <label for="education">Education</label>
              <select id="education" v-model="job.Education">
                <option value="">Select education</option>
                <option value="High School">High School</option>
                <option value="Bachelor's Degree">Bachelor's Degree</option>
                <option value="Master's Degree">Master's Degree</option>
                <option value="PhD">PhD</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3 class="section-title">Additional Information</h3>
          <div class="form-group full-width">
            <label for="description">Job Description*</label>
            <textarea id="description" v-model="job.Description" rows="4" required placeholder="Describe the job responsibilities..."></textarea>
          </div>

          <div class="form-group full-width">
            <label for="requirement">Requirements</label>
            <textarea id="requirement" v-model="job.Requirement" rows="4" placeholder="List the required skills and qualifications..."></textarea>
          </div>

          <div class="form-group full-width">
            <label for="right">Rights</label>
            <textarea id="right" v-model="job.Right" rows="4" placeholder="List the rights that employees receive..."></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="deadline">Application Deadline</label>
              <input id="deadline" type="date" v-model="job.Deadline" />
            </div>
            <div class="form-group">
              <label for="probation">Probation Period</label>
              <select id="probation" v-model="job.Probation_Time">
                <option value="">Select period</option>
                <option value="1 month">1 month</option>
                <option value="2 months">2 months</option>
                <option value="3 months">3 months</option>
                <option value="6 months">6 months</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="emitClose">Cancel</button>
          <button type="submit" class="submit-btn">Post Job</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElNotification } from "element-plus";
import { createJob } from "@/services/user.service"; // Import your API call

const emits = defineEmits<{
  (e: "close-popup"): void;
  (e: "job-posted"): void;
}>();

const job = ref({
  Title: "",
  Age: null as number | null,
  Sexual: "",
  Probation_Time: "",
  Work_Way: "",
  Profession: "",
  Place: "",
  Number_Recruitment: null as number | null,
  Experience: "",
  Level: "",
  Salary: "",
  Education: "",
  Description: "",
  Requirement: "",
  Right: "",
  Deadline: ""
});

const emitClose = () => {
  emits("close-popup");
};

const handlePost = async () => {
  try {
    // Call createJob API with job data
    const response = await createJob(job.value);

    ElNotification({
      title: "Success",
      message: "Job posted successfully!",
      type: "success",
    });

    emits("job-posted");
    emitClose();
  } catch (error) {
    console.error("Failed to post job:", error);
    ElNotification({
      title: "Error",
      message: "Failed to post job!",
      type: "error",
    });
  }
};
</script>

<style scoped>
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
  width: 800px;
  max-width: 95vw;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
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

.job-form {
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
}

input[type="text"],
input[type="number"],
input[type="date"],
select,
textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: all 0.2s;
  background-color: #f8fafc;
}

input[type="text"]:focus,
input[type="number"]:focus,
input[type="date"]:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
  background-color: white;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 1em;
}

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