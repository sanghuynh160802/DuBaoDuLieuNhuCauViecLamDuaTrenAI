<script setup lang="ts">
import { onBeforeMount, ref, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { getInfo } from "@/services/user.service";
import { ILogin } from "@/types/user";

// Import all navbars
import NavBar from "@/layouts/NavBar/index.vue";
import EmployerNavBar from "@/layouts/EmployerNavBar/index.vue";
import ApplicantNavBar from "@/layouts/ApplicantNavBar/index.vue";

// Import main component
import JobList from "./joblist/index.vue";

const auth = useAuthStore();
const dataInfo = ref<ILogin>();

onBeforeMount(async () => {
  await handleGetInfo();
  console.log("Is Admin:", auth.getIsAdmin());
  console.log("User Type:", auth.getUserType());
});

const handleGetInfo = async () => {
  try {
    const res = await getInfo();
    dataInfo.value = res["data"];
    if (dataInfo.value?.user_type) {
      auth.setUserType(dataInfo.value.user_type);
    }
  } catch (error) {
    console.error("Failed to get user info:", error);
  }
};
</script>

<template>
  <div class="container-job-management">
    <!-- Conditionally render navbar -->
    <NavBar v-if="auth.getIsAdmin()" />
    <ApplicantNavBar v-else-if="auth.getUserType() === 'APPLICANT'" />
    <EmployerNavBar v-else-if="auth.getUserType() === 'EMPLOYER'" />
    
    <div class="container-job-list">
      <JobList />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container-job-management {
  width: 100%;
  height: 100%;
  background: white;
  display: flex;
  overflow-x: hidden;
}

.container-job-list {
  margin-left: 50px;
  padding: 20px;
  flex: 1;
}
</style>
