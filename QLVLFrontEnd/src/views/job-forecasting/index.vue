<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import NavBar from "@/layouts/NavBar/index.vue";
import EmployerNavBar from "@/layouts/EmployerNavBar/index.vue";
import ApplicantNavBar from "@/layouts/ApplicantNavBar/index.vue";
import JobChart from "./jobchart/index.vue";
import { useAuthStore } from "@/stores/auth";
import { getInfo } from "@/services/user.service";
import { ILogin } from "@/types/user";

const auth = useAuthStore();
const dataInfo = ref<ILogin>();

onBeforeMount(async () => {
  try {
    const res = await getInfo();
    dataInfo.value = res["data"];

    if (dataInfo.value?.user_type) {
      auth.setUserType(dataInfo.value.user_type);
    }
  } catch (error) {
    console.error("Failed to fetch user info:", error);
  }
});
</script>

<template>
  <div class="container-forecast">
    <NavBar v-if="auth.getIsAdmin()" />
    <ApplicantNavBar v-else-if="auth.getUserType() === 'APPLICANT'" />
    <EmployerNavBar v-else-if="auth.getUserType() === 'EMPLOYER'" />

    <div class="container-chart">
      <JobChart />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container-forecast {
  width: 100%;
  height: 100%;
  background: white;
  display: flex;
  overflow-x: hidden;
}

.container-chart {
  margin-left: 50px;
  padding: 20px;
  flex: 1;
}
</style>
