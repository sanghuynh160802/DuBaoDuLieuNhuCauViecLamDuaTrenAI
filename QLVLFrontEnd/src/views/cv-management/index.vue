<template>
  <div class="container">
    <!-- EmployerNavBar on the left side -->
    <EmployerNavBar />

    <!-- Main content -->
    <main class="main-content">
      <Main 
        :filters="filters"
        :cvs="cvs"
        :selectedCV="selectedCV"
        @updateCVs="updateCVs"
      />
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import Main from './main/index.vue'
import EmployerNavBar from '@/layouts/EmployerNavBar/index.vue'  // Import EmployerNavBar

export default defineComponent({
  name: 'CVManagement',
  components: { Main, EmployerNavBar },  // Register EmployerNavBar
  setup() {
    const filters = ref({
      skill: '',
      experience: '',
      position: '',
      location: '',
    })

    const cvs = ref<any[]>([])
    const selectedCV = ref(null)

    const updateCVs = (newCvs: any[]) => {
      cvs.value = newCvs
    }

    return {
      filters,
      cvs,
      selectedCV,
      updateCVs
    }
  }
})
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  background-color: #f9fafb;
  max-width: 1250px;
  padding: 1.5rem;
}
</style>