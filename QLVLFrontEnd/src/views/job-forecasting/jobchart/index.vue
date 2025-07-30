<template>
  <div class="chart-container">
    <!-- Filters Row -->
    <div class="filters-row">
      <!-- City Filter Dropdown (moved to first position) -->
      <div class="filter-container">
        <label for="city-filter">Select City:</label>
        <select id="city-filter" v-model="selectedCity" @change="onCityChange">
          <option v-for="city in cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
      </div>

      <!-- Industry Filter Dropdown (now in second position) -->
      <div class="filter-container">
        <label for="industry-filter">Select Industry:</label>
        <select id="industry-filter" v-model="selectedIndustry" @change="onIndustryChange">
          <option v-for="industry in industries" :key="industry" :value="industry">
            {{ industry }}
          </option>
        </select>
      </div>

      <!-- Job Filter Dropdown (now in third position) -->
      <div class="filter-container">
        <label for="job-filter">Select Job:</label>
        <select id="job-filter" v-model="selectedJob" @change="onJobChange">
          <option v-for="job in topJobs" :key="job.job" :value="job.job">
            {{ job.job }}
          </option>
        </select>
      </div>

      <!-- Month-Year Picker -->
      <div class="filter-container">
        <label for="month-year-picker">Select Month & Year:</label>
        <DatePicker
          v-model:value="selectedMonthYear"
          type="month"
          format="YYYY-MM"
          value-type="format"
          placeholder="Select Month & Year"
        />
      </div>

      <!-- Step Filter Dropdown -->
      <div class="filter-container">
        <label for="step-filter">Select Step (1-36):</label>
        <select id="step-filter" v-model="selectedStep">
          <option v-for="step in steps" :key="step" :value="step">
            {{ step }}
          </option>
        </select>
      </div>

      <!-- Buttons Container -->
      <div class="filter-container buttons-wrapper">
        <label>&nbsp;</label>
        <div class="buttons-container">
          <button
            class="predict-btn"
            @click="predict"
            :disabled="loading"
            aria-busy="loading"
          >
            <span v-if="loading" class="spinner"></span>
            <span v-else>PREDICT</span>
          </button>
          <button class="reset-btn" @click="resetFilters" :disabled="loading">
            RESET
          </button>
        </div>
      </div>
    </div>

    <!-- Chart with loading overlay -->
    <div class="chart-wrapper" :class="{ loading: loading }">
      <LineChart
        v-if="chartData"
        :chart-data="chartData"
        :chart-options="chartOptions"
      />
      <div v-if="loading" class="chart-loading-overlay">
        <div class="spinner large"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import DatePicker from "vue-datepicker-next";
import "vue-datepicker-next/index.css";
import { LineChart } from "vue-chart-3";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  LineController,
} from "chart.js";
import { getTopJobs, getCities, getJobPredictions, getIndustryFields } from "../../../services/user.service";

ChartJS.register(
  LineController,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
);

const chartData = ref(null);
const loading = ref(false);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: true },
    title: { display: true, text: "Job Trends Over Time" },
  },
  scales: {
    x: { title: { display: true, text: "Time (Months)" } },
    y: { title: { display: true, text: "Job Count" } },
  },
};

const topJobs = ref([]);
const selectedJob = ref("");
const cities = ref([]);
const selectedCity = ref("");
const industries = ref([]);
const selectedIndustry = ref("");
const selectedMonthYear = ref("2023-01");
const steps = ref([...Array(36).keys()].map((i) => i + 1));
const selectedStep = ref(1);
const isPredicted = ref(false);

const fetchTopJobs = async () => {
  try {
    const response = await getTopJobs();
    topJobs.value = response.data;
    if (topJobs.value.length > 0) {
      selectedJob.value = topJobs.value[0].job;
      if (!isPredicted.value) fetchJobTrends();
    }
  } catch (error) {
    console.error("Failed to fetch top jobs:", error);
  }
};

const fetchCities = async () => {
  try {
    const response = await getCities();
    cities.value = response.data;
    if (cities.value.length > 0) {
      selectedCity.value = cities.value[0];
      if (!isPredicted.value) fetchCityTrends();
    }
  } catch (error) {
    console.error("Failed to fetch cities:", error);
  }
};

const fetchIndustries = async () => {
  try {
    const response = await getIndustryFields();
    industries.value = response;
    if (industries.value.length > 0) {
      selectedIndustry.value = industries.value[0];
    }
  } catch (error) {
    console.error("Failed to fetch industries:", error);
  }
};

const fetchJobTrends = async () => {
  if (!selectedJob.value) return;
  const fakeData = [
    { time: "2023-01", job_counting: 120 },
    { time: "2023-02", job_counting: 150 },
    { time: "2023-03", job_counting: 130 },
    { time: "2023-04", job_counting: 180 },
    { time: "2023-05", job_counting: 210 },
    { time: "2023-06", job_counting: 250 },
    { time: "2023-07", job_counting: 230 },
    { time: "2023-08", job_counting: 270 },
    { time: "2023-09", job_counting: 290 },
    { time: "2023-10", job_counting: 310 },
  ];
  chartData.value = {
    labels: fakeData.map((d) => d.time),
    datasets: [
      {
        label: `Job Count for ${selectedJob.value}`,
        data: fakeData.map((d) => d.job_counting),
        borderColor: "#3498db",
        backgroundColor: "rgba(52, 152, 219, 0.2)",
        fill: true,
      },
    ],
  };
};

const fetchCityTrends = async () => {
  if (!selectedCity.value) return;
  const fakeData = [
    { time: "2023-01", job_counting: 80 },
    { time: "2023-02", job_counting: 90 },
    { time: "2023-03", job_counting: 85 },
    { time: "2023-04", job_counting: 100 },
    { time: "2023-05", job_counting: 110 },
    { time: "2023-06", job_counting: 120 },
    { time: "2023-07", job_counting: 115 },
    { time: "2023-08", job_counting: 130 },
    { time: "2023-09", job_counting: 140 },
    { time: "2023-10", job_counting: 150 },
  ];
  chartData.value = {
    labels: fakeData.map((d) => d.time),
    datasets: [
      {
        label: `Job Count for ${selectedCity.value}`,
        data: fakeData.map((d) => d.job_counting),
        borderColor: "#2ecc71",
        backgroundColor: "rgba(46, 204, 113, 0.2)",
        fill: true,
      },
    ],
  };
};

const onJobChange = () => {
  if (!isPredicted.value) fetchJobTrends();
};

const onCityChange = () => {
  if (!isPredicted.value) fetchCityTrends();
};

const onIndustryChange = () => {
  // Add your industry change logic here
};

const predict = async () => {
  loading.value = true;
  try {
    const time = selectedMonthYear.value;
    const response = await getJobPredictions(
      selectedCity.value,
      selectedJob.value,
      time,
      selectedStep.value
    );
    if (response && response.predictions) {
      const labels = Array.from({ length: selectedStep.value }, (_, i) => {
        const date = new Date(`${time}-01`);
        date.setMonth(date.getMonth() + i);
        return date.toISOString().slice(0, 7);
      });
      chartData.value = {
        labels,
        datasets: [
          {
            label: `Predicted Job Count for ${selectedJob.value} in ${selectedCity.value}`,
            data: response.predictions,
            borderColor: "#e74c3c",
            backgroundColor: "rgba(231, 76, 60, 0.2)",
            fill: true,
          },
        ],
      };
      isPredicted.value = true;
    }
  } catch (error) {
    console.error("Failed to fetch predictions:", error);
  } finally {
    loading.value = false;
  }
};

const resetFilters = () => {
  if (topJobs.value.length > 0) selectedJob.value = topJobs.value[0].job;
  if (cities.value.length > 0) selectedCity.value = cities.value[0];
  if (industries.value.length > 0) selectedIndustry.value = industries.value[0];
  selectedMonthYear.value = "2023-01";
  selectedStep.value = 1;
  isPredicted.value = false;
  fetchJobTrends();
  fetchCityTrends();
};

onMounted(() => {
  fetchTopJobs();
  fetchCities();
  fetchIndustries();
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 1350px;
  height: 600px;
  margin: auto;
  padding-top: 30px;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.filters-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px; /* Reduced gap to fit more filters */
  margin-bottom: 30px;
  align-items: flex-end;
  padding: 0 20px;
}

.filter-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 200px; /* Set a fixed width */
  flex: none; /* Prevent containers from growing and shrinking */
}

.buttons-wrapper {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
}

.buttons-container {
  display: flex;
  gap: 10px;
}

.predict-btn,
.reset-btn {
  padding: 10px 20px; /* Slightly reduced padding */
  font-size: 14px; /* Slightly smaller font */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  height: auto;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap; /* Prevent button text from wrapping */
}

.predict-btn {
  background-color: #3498db;
  color: white;
}

.reset-btn {
  background-color: #e74c3c;
  color: white;
}

.predict-btn:hover,
.reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.predict-btn:active,
.reset-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.predict-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.filter-container label {
  font-size: 14px; /* Slightly smaller font */
  font-weight: 600;
  color: #444;
  white-space: nowrap; /* Prevent label text from wrapping */
}

.filter-container select,
.filter-container :deep(.mx-input) {
  padding: 10px 12px; /* Slightly reduced padding */
  font-size: 14px; /* Slightly smaller font */
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  height: 40px; /* Reduced height */
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  width: 100%; /* Ensure full width */
}

.filter-container select:focus,
.filter-container :deep(.mx-input:focus) {
  border-color: #66b3ff;
  box-shadow: 0 0 0 3px rgba(102, 179, 255, 0.25);
}

/* Chart wrapper for loading overlay */
.chart-wrapper {
  position: relative;
  height: 480px;
}

/* Overlay when loading */
.chart-loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  border-radius: 12px;
}

/* Spinner styles */
.spinner,
.spinner.large {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
}

.spinner.large {
  width: 48px;
  height: 48px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .filter-container {
    width: 200px; /* Adjust for smaller screens */
  }
}

@media (max-width: 992px) {
  .filter-container {
    width: 180px; /* Further adjust for smaller screens */
  }
}

@media (max-width: 768px) {
  .filters-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-container {
    width: 100%;
  }
  
  .buttons-container {
    justify-content: flex-start;
  }
}
</style>