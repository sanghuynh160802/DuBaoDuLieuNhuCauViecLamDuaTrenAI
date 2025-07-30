<template>
  <div class="main-container">
    <div class="carousel">
      <el-carousel indicator-position="outside">
        <el-carousel-item v-for="item in listImages" :key="item">
          <h3 text="2xl" justify="center"><img :src="item" alt="" /></h3>
        </el-carousel-item>
      </el-carousel>
    </div>

    <div class="container-box-search">
      <p class="suggest-label">Gợi ý cho bạn:</p>
      
      <div 
        class="list-search" 
        v-for="(item, index) in listSearchItems" 
        :key="index"
        @click="handleSearchClick(item.label)"
        style="cursor:pointer;"
      >
        <img :src="item.img" alt="" />
        <div class="text-block">
          <p class="label">{{ item.label }}</p>
        </div>
      </div>
    </div>

    <!-- Search bar container -->
    <div class="container-search">
      <el-input
        v-model="keySearch"
        placeholder="Tìm kiếm cơ hội việc làm"
        prefix-icon="el-icon-search"
        clearable
        class="input-search"
      />
      <el-select
        v-model="selectedJobTitle"
        placeholder="Lọc theo nghề nghiệp"
        clearable
        class="input-search-select"
      >
        <el-option
          v-for="(item, index) in listJobTitle"
          :key="index"
          :value="item"
          :label="item"
        />
      </el-select>
      <el-select
        v-model="selectedProvince"
        placeholder="Lọc theo tỉnh thành"
        clearable
        class="input-search-select"
      >
        <el-option
          v-for="item in provinces"
          :key="item.code"
          :value="item.name"
          :label="item.name"
        />
      </el-select>

      <button 
        class="button-search" 
        @click="getJobFilterkey(
          keySearch,
          selectedJobTitle,
          selectedProvince,
          selectedLevel,
          selectedWorkWay,
          selectedEducation,
          selectedExperience,
          selectedSalary // thêm
        )"
      >
        <el-icon><Search /></el-icon>
        <span>Tìm <br />kiếm</span>
      </button>

      <button class="button-advanced">Lọc nâng cao</button>
    </div>

    <!-- Filter bar -->
    <div class="filter-bar">
      <div class="tag urgent">⚡ Tuyển gấp</div>

      <el-select
        v-model="selectedLevel"
        placeholder="Cấp bậc"
        clearable
        class="filter-select"
      >
        <el-option
          v-for="(level, index) in levels"
          :key="index"
          :label="level"
          :value="level"
        />
      </el-select>
      <el-select
        v-model="selectedWorkWay"
        placeholder="Hình thức làm việc"
        clearable
        class="filter-select"
      >
        <el-option
          v-for="(way, index) in workWays"
          :key="index"
          :label="way"
          :value="way"
        />
      </el-select>
      <el-select placeholder="Mức lương" clearable class="filter-select" v-model="selectedSalary">
        <el-option
          v-for="salary in salaryOptions"
          :key="salary.value"
          :label="salary.label"
          :value="salary.value"
        />
      </el-select>
      <el-select
        v-model="selectedEducation"
        placeholder="Trình độ"
        clearable
        class="filter-select"
      >
        <el-option
          v-for="(education, index) in educationLevels"
          :key="index"
          :label="education"
          :value="education"
        />
      </el-select>
      <el-select
        v-model="selectedExperience"
        placeholder="Kinh nghiệm"
        clearable
        class="filter-select"
      >
        <el-option
          v-for="(exp, index) in experienceLevels"
          :key="index"
          :label="exp"
          :value="exp"
        />
      </el-select>

      <div class="filter-actions">
        <button class="clear-filters" @click="clearAllFilters">Xóa chọn</button>
        <button class="close-filters">Đóng</button>
      </div>
    </div>

    <div class="job-list-child">
      <div class="left-column">
        <div v-for="(job, index) in filteredJobs" :key="index">
          <JobList :job="job" />
        </div>
      </div>
      <div class="right-column">
        <div class="list-img-left">
          <img src="src/images/left-img-1.webp" alt="anh" />
          <img src="src/images/left-img-2.webp" alt="anh" />
          <img src="src/images/left-img-3.webp" alt="anh" />
          <img src="src/images/img-left-4.webp" alt="anh" />
          <img src="src/images/img-left-5.jpg" alt="anh" />
          <img src="src/images/left-img-6.webp" alt="anh" />
        </div>
      </div>
    </div>

    <div class="pagination">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="totalSearchedAndFilteredJobs"
        :page-size="pageSize"
        :current-page.sync="currentPage"
        @current-change="handlePageChange"
      />
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
// Your existing script remains unchanged
import { ref, onBeforeMount, computed, watch } from "vue";
import axios from "axios";
import type { IJob, IPronvince } from "@/types/auth";
import { getJobAll, getJobFilter, getProfessions, getAllLevels, getAllWorkWays, getAllEducation, getAllExperiences } from "@/services/user.service";
import JobList from "../joblist/index.vue";
import Footer from "../../footer/index.vue";
import { Search } from '@element-plus/icons-vue';

onBeforeMount(async () => {
  await getProvinces();
  await getListJob();
  await fetchJobTitles();
  await fetchLevels();
  await fetchWorkWays(); 
  await fetchEducationLevels();
  await fetchExperienceLevels();
  await applyFiltersFromStorage();
});

const listImages = [
  "src/images/carousel-1.webp",
  "src/images/carousel-2.webp",
  "src/images/carousel-3.webp",
  "src/images/carousel-4.webp",
];

const listSearchItems = [
  { img: "src/images/img-1.webp", label: "Java" },
  { img: "src/images/img-2.webp", label: "SQL" },
  { img: "src/images/img-3.webp", label: ".NET" },
  { img: "src/images/img-4.webp", label: "Manager" },
  { img: "src/images/img-5.webp", label: "NodeJS" },
  { img: "src/images/img-1.webp", label: "Python" },
  { img: "src/images/img-2.webp", label: "PHP" },
  { img: "src/images/img-3.webp", label: "Analyst" },
];

const salaryOptions = [
  { label: 'Từ 3.000.000 đ', value: 3000000 },
  { label: 'Từ 5.000.000 đ', value: 5000000 },
  { label: 'Từ 7.000.000 đ', value: 7000000 },
  { label: 'Từ 10.000.000 đ', value: 10000000 },
  { label: 'Từ 15.000.000 đ', value: 15000000 },
  { label: 'Từ 20.000.000 đ', value: 20000000 },
  { label: 'Từ 30.000.000 đ', value: 30000000 },
  { label: 'Từ 40.000.000 đ', value: 40000000 },
  { label: 'Từ 50.000.000 đ', value: 50000000 },
  { label: 'Từ 60.000.000 đ', value: 60000000 },
  { label: 'Từ 70.000.000 đ', value: 70000000 },
];

const selectedSalary = ref(null);

const provinces = ref<Array<IPronvince>>([]);
const keySearch = ref("");
const selectedProvince = ref("");
const selectedJobTitle = ref("");

const removePrefix = (keyword: string) => {
  return keyword.replace('Tỉnh ', '').replace('Thành phố ', '');
};

const getJobFilterkey = async (
  key1: string,
  key2: string,
  key3: string,
  level: string,
  workWay: string,
  education: string,
  experience: string,
  salary: number | null
): Promise<void> => {
  try {
    const res = await getJobFilter(
      key1.toLowerCase(),
      key2.toLowerCase(),
      removePrefix(key3),
      level.toLowerCase(),
      workWay.toLowerCase(),
      education.toLowerCase(),
      experience.toLowerCase(),
      salary
    );
    listJob.value = res.data.data;
  } catch (error) {
    console.log("error", error);
  }
};

const applyFiltersFromStorage = async () => {
  const savedKeySearch = localStorage.getItem('keySearch') || ""
  const savedJobTitle = localStorage.getItem('selectedJobTitle') || ""
  const savedProvince = localStorage.getItem('selectedProvince') || ""
  const savedLevel = localStorage.getItem('selectedLevel') || ""
  const savedWorkWay = localStorage.getItem('selectedWorkWay') || ""
  const savedEducation = localStorage.getItem('selectedEducation') || ""
  const savedExperience = localStorage.getItem('selectedExperience') || ""
  const savedSalary = localStorage.getItem('selectedSalary') ? Number(localStorage.getItem('selectedSalary')) : null

  keySearch.value = savedKeySearch
  selectedJobTitle.value = savedJobTitle
  selectedProvince.value = savedProvince
  selectedLevel.value = savedLevel
  selectedWorkWay.value = savedWorkWay
  selectedEducation.value = savedEducation
  selectedExperience.value = savedExperience
  selectedSalary.value = savedSalary

  await getJobFilterkey(
    savedKeySearch,
    savedJobTitle,
    savedProvince,
    savedLevel,
    savedWorkWay,
    savedEducation,
    savedExperience,
    savedSalary
  )
}

watch(selectedJobTitle, (newVal) => {
  localStorage.setItem('selectedJobTitle', newVal || '')
})

watch(keySearch, (val) => {
  localStorage.setItem('keySearch', val || '')
})

const selectedLevel = ref("");
const selectedWorkWay = ref("");    // ✅ Bound to el-select
const selectedEducation = ref("");
const selectedExperience = ref("");

onBeforeMount(() => {
  selectedJobTitle.value = localStorage.getItem('selectedJobTitle') || "";
  selectedProvince.value = localStorage.getItem('selectedProvince') || "";
  selectedLevel.value = localStorage.getItem('selectedLevel') || "";
  selectedWorkWay.value = localStorage.getItem('selectedWorkWay') || "";
  selectedEducation.value = localStorage.getItem('selectedEducation') || "";
  selectedExperience.value = localStorage.getItem('selectedExperience') || "";
  selectedSalary.value = localStorage.getItem('selectedSalary') ? Number(localStorage.getItem('selectedSalary')) : null;
});

watch(selectedJobTitle, (val) => localStorage.setItem('selectedJobTitle', val || ""));
watch(selectedProvince, (val) => localStorage.setItem('selectedProvince', val || ""));
watch(selectedLevel, (val) => localStorage.setItem('selectedLevel', val || ""));
watch(selectedWorkWay, (val) => localStorage.setItem('selectedWorkWay', val || ""));
watch(selectedEducation, (val) => localStorage.setItem('selectedEducation', val || ""));
watch(selectedExperience, (val) => localStorage.setItem('selectedExperience', val || ""));
watch(selectedSalary, (val) => {
  if(val === null) localStorage.removeItem('selectedSalary');
  else localStorage.setItem('selectedSalary', String(val));
});

const clearAllFilters = () => {
  keySearch.value = "";
  selectedJobTitle.value = "";
  selectedProvince.value = "";
  selectedLevel.value = "";
  selectedWorkWay.value = "";
  selectedEducation.value = "";
  selectedExperience.value = "";
  selectedSalary.value = null;

  localStorage.removeItem('selectedJobTitle');
  localStorage.removeItem('selectedProvince');
  localStorage.removeItem('selectedLevel');
  localStorage.removeItem('selectedWorkWay');
  localStorage.removeItem('selectedEducation');
  localStorage.removeItem('selectedExperience');
  localStorage.removeItem('selectedSalary');

  getJobFilterkey("", "", "", "", "", "", "", null);
  getListJob();
};

const getProvinces = async () => {
  try {
    const response = await axios.get("https://provinces.open-api.vn/api/");
    const cleanedProvinces = response.data.map((province: IPronvince) => ({
      ...province,
      name: province.name.replace('Tỉnh ', '').replace('Thành phố ', '')
    }));

    const priorityCities = ['Hà Nội', 'Hồ Chí Minh', 'Đà Nẵng'];
    const prioritized = cleanedProvinces.filter(p => priorityCities.includes(p.name));
    const others = cleanedProvinces
      .filter(p => !priorityCities.includes(p.name))
      .sort((a, b) => a.name.localeCompare(b.name));

    provinces.value = [{ code: 0, name: '' }, ...prioritized, ...others];
  } catch (error) {
    console.error("Error fetching provinces:", error);
  }
};

const listJob = ref<Array<IJob>>([]);
const getListJob = async (): Promise<void> => {
  try {
    const res = await getJobAll();
    listJob.value = res.data;
  } catch (error) {
    console.log("error", error);
  }
};

const listJobTitle = ref<string[]>([]);
const fetchJobTitles = async () => {
  try {
    const professions = await getProfessions();
    listJobTitle.value = professions
      .map((item: { Profession: string }) => item.Profession)
      .filter((title) => !!title);
  } catch (error) {
    console.error("Error loading job titles:", error);
  }
};

const levels = ref<string[]>([]);
const fetchLevels = async () => {
  try {
    const response = await getAllLevels();
    levels.value = response;
  } catch (error) {
    console.error("Error loading levels:", error);
  }
};

const workWays = ref<string[]>([]); // ✅ Holds options
const fetchWorkWays = async () => {
  try {
    const response = await getAllWorkWays();
    workWays.value = response;
  } catch (error) {
    console.error("Error loading work ways:", error);
  }
};

const educationLevels = ref<string[]>([]);

const fetchEducationLevels = async () => {
  try {
    const response = await getAllEducation();
    educationLevels.value = response;
  } catch (error) {
    console.error("Error loading education levels:", error);
  }
};

const experienceLevels = ref<string[]>([]);

const fetchExperienceLevels = async () => {
  try {
    const response = await getAllExperiences();
    experienceLevels.value = response;
    console.log("✅ Loaded experience levels:", response);
  } catch (error) {
    console.error("❌ Error fetching experiences:", error);
  }
};

const pageSize = ref(10);
const currentPage = ref(1);

const totalSearchedAndFilteredJobs = computed(() => {
  return listJob.value.length;
});

const filteredJobs = computed(() => {
  if (!Array.isArray(listJob.value)) return [];
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return listJob.value.slice(start, end);
});

const handlePageChange = (page: number) => {
  currentPage.value = page;
};

const handleSearchClick = (label: string) => {
  keySearch.value = label; // gán từ khóa tìm kiếm
  // Gọi lại hàm tìm kiếm với các filter hiện tại, truyền keySearch mới
  getJobFilterkey(
    label,
    selectedJobTitle.value,
    selectedProvince.value,
    selectedLevel.value,
    selectedWorkWay.value,
    selectedEducation.value,
    selectedExperience.value,
    selectedSalary.value
  );
};
</script>

<style scoped>
.main-container {
  margin: 0;
  position: relative;
  overflow-x: hidden;
  padding-top: 20px;
}

.container-box-search {
  display: flex;
  align-items: center;
  background-color: #fff;
  height: 100px;
  max-width: 1200px;
  margin: 0 auto 30px;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(160, 159, 102, 0.32);
  padding: 10px 30px;
  gap: 20px;
  overflow-x: auto;
  white-space: nowrap;
}

.suggest-label {
  font-weight: 600;
  font-size: 16px;
  color: #444;
  margin-right: 20px;
  flex-shrink: 0;
}

.list-search {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  gap: 6px;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.list-search:hover {
  transform: translateY(-2px);
}

.list-search img {
  width: 35px;
  height: 35px;
  object-fit: contain;
}

.text-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1.2;
}

.text-row-2 {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.text-row-2 p {
  font-size: 16px;
  font-weight: 700;
  color: #3b91ee;
  margin: 0;
  line-height: 1;
}

.text-row-2 span {
  color: #a7a6a9;
  font-size: 12px;
  line-height: 1;
}

.label {
  font-size: 13px;
  margin: 0;
  color: #444;
  text-align: center;
}

.container-search {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px 30px;
  background-color: #483aa0;
  border-radius: 10px;
  max-width: 1200px;
  margin: 0 auto 8px;
  box-sizing: border-box;
  box-shadow: none;
  position: relative;
  z-index: 100;
}

/* Reduced width of search input */
.input-search {
  width: 450px; /* or any smaller value */
}
.input-search::v-deep(.el-select .el-input__inner) {
  width: 320px;
  height: 44px;
  background-color: white !important;
  border-radius: 6px !important;
  border: none !important;
  padding-left: 40px !important;
  font-size: 14px;
  color: #444;
  box-shadow: none !important;
}

/* Search icon */
.input-search::v-deep(.el-select .el-input__inner) {
  color: #999;
  font-size: 18px;
  left: 14px;
}

/* Enlarged width and height of the two selects next to search input */
.input-search-select {
  width: 200px; /* wider than default */
}

.input-search::v-deep(.el-input__inner),
.input-search-select::v-deep(.el-input__inner) {
  height: 44px;
  background-color: white !important;
  border-radius: 6px !important;
  border: none !important;
  padding-left: 40px !important;
  font-size: 14px;
  color: #444;
  box-shadow: none !important;
}

/* Buttons */
.button-search {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #198cff;
  border: none;
  border-radius: 6px;
  padding: 0 20px;
  height: 44px;
  color: white;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 3px 8px rgba(25, 140, 255, 0.5);
  transition: background-color 0.3s ease;
  white-space: nowrap;
}

.button-search:hover {
  background-color: #0f6ec7;
}

.button-search el-icon {
  font-size: 18px;
  color: white;
}

/* Advanced button */
.button-advanced {
  background-color: #5c3dbb;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  font-size: 14px;
  padding: 0 20px;
  height: 44px;
  cursor: pointer;
  box-shadow: 0 3px 8px rgba(92, 61, 187, 0.5);
  transition: background-color 0.3s ease;
  white-space: nowrap;
}

.button-advanced:hover {
  background-color: #472c96;
}

/* Filter bar */
.filter-bar {
  max-width: 1200px;
  margin: 0 auto 40px;
  background: white;
  border-radius: 10px;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-sizing: border-box;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  flex-wrap: wrap;
}

/* Urgent tag */
.tag.urgent {
  background-color: #fff4db;
  color: #b17400;
  border: 1px solid #ffd37f;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}

/* Filter selects */
.filter-select {
  width: 150px;
}

.filter-select::v-deep(.el-select .el-input__inner) {
  border-radius: 6px !important;
  height: 36px;
  font-size: 13px;
  padding-left: 10px !important;
}

/* Filter actions */
.filter-actions {
  margin-left: auto;
  display: flex;
  gap: 12px;
}

.clear-filters,
.close-filters {
  border: none;
  background: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  padding: 4px 8px;
  white-space: nowrap;
  transition: color 0.3s ease;
}

.clear-filters {
  color: #1e40af;
}

.clear-filters:hover {
  text-decoration: underline;
}

.close-filters {
  color: #6b21a8;
}

.close-filters:hover {
  text-decoration: underline;
}

/* Job list layout */
.job-list-child {
  margin-left: 80px;
  margin-top: 0;
  display: flex;
  justify-content: space-between;
  gap: 80px;
}

.left-column {
  width: 60%; /* Adjust the percentage as needed */
  padding: 0 15px;
}

.right-column {
  width: 40%; /* Adjust the percentage as needed */
  padding: 0 15px;
}

.list-img-left img {
  width: 400px;
  height: 300px;
  margin-top: 15px;
  border-radius: 16px;
  transition: transform 1s ease-in-out;
  cursor: pointer;
}

.list-img-left img:hover {
  transform: scale(1.05);
  box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
}

/* Pagination */
.pagination {
  margin: 40px 0;
  display: flex;
  justify-content: center;
}

.carousel {
  height: 24vh; /* 24% of the viewport height */
  max-width: 1200px;
  margin: 0 auto 30px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.carousel :deep(.el-carousel) {
  height: 100%;
}

.carousel :deep(.el-carousel__container) {
  height: 100%;
}

.carousel :deep(.el-carousel-item) {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* ensures the image fills without distortion */
  border-radius: 10px;
}

</style>