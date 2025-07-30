<template>
  <div class="user-management-container">
    <div class="header-section">
      <div class="search-section">
        <h1>User Management</h1>
        <div class="search-box">
          <el-icon class="search-icon"><Search /></el-icon>
          <input
            type="text"
            v-model="keySearch"
            placeholder="Search users..."
          />
        </div>
      </div>
      <button class="create-button" @click="showCreatePopup = true">
        <el-icon><Plus /></el-icon>
        <span>Create User</span>
      </button>
    </div>

    <div class="table-container">
      <table class="user-table">
        <thead>
          <tr>
            <th class="avatar-header">Avatar</th>
            <th class="name-header">Name</th>
            <th class="email-header">Email</th>
            <th class="date-header">Created</th>
            <th class="date-header">Updated</th>
            <th class="action-header"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id" class="user-row">
            <td class="avatar-cell">
              <img :src="user.avatar || defaultAvatar" class="avatar-image" />
            </td>
            <td class="name-cell">{{ user.name }}</td>
            <td class="email-cell">{{ user.email }}</td>
            <td class="date-cell">{{ formatDate(user.created_at) }}</td>
            <td class="date-cell">{{ formatDate(user.updated_at) }}</td>
            <td class="action-cell">
              <button class="edit-button" @click="openUpdatePopup(user)">✎</button>
              <button class="delete-button" @click="$emit('delete', user.id)">×</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination-section">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="listUser.length"
        :page-size="pageSize"
        :current-page.sync="currentPage"
        @current-change="handlePageChange"
      />
    </div>

    <!-- Create User Popup -->
    <popup-create-user 
      v-if="showCreatePopup" 
      @close="showCreatePopup = false"
      @success="handleUserCreated"
    />
    <!-- Update User Popup -->
    <popup-update-user
      v-if="showUpdatePopup && selectedUser"
      :user="selectedUser"
      @close="showUpdatePopup = false"
      @success="handleUserUpdated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onBeforeMount } from "vue";
import { getInfoAll } from "@/services/user.service";
import type { IUser } from "@/types/user";
import PopupCreateUser from "@/views/popup/popupCreateUser.vue";
import PopupUpdateUser from "@/views/popup/popupUpdateUser.vue";

const defaultAvatar = "http://www.gravatar.com/avatar/?d=mp";

const listUser = ref<Array<IUser>>([]);
const showCreatePopup = ref(false);
const showUpdatePopup = ref(false);
const selectedUser = ref<IUser | null>(null);

const getListUser = async (): Promise<void> => {
  try {
    const res = await getInfoAll();
    listUser.value = res.data;
  } catch (error) {
    console.error("Error loading users:", error);
  }
};

const handleUserCreated = () => {
  // Refresh the user list when a new user is created
  getListUser();
};

const handleUserUpdated = () => {
  getListUser();
};

const openUpdatePopup = (user: IUser) => {
  selectedUser.value = user;
  showUpdatePopup.value = true;
};

onBeforeMount(() => {
  getListUser();
});

const formatDate = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

const keySearch = ref<string>("");
const pageSize = ref(10);
const currentPage = ref(1);

const filteredUsers = computed(() => {
  const filtered = listUser.value.filter(
    (user) =>
      user.email.toLowerCase().includes(keySearch.value.toLowerCase()) ||
      user.name.toLowerCase().includes(keySearch.value.toLowerCase()) ||
      (user.created_at && user.created_at.toLowerCase().includes(keySearch.value.toLowerCase())) ||
      (user.updated_at && user.updated_at.toLowerCase().includes(keySearch.value.toLowerCase()))
  );
  const start = (currentPage.value - 1) * pageSize.value;
  return filtered.slice(start, start + pageSize.value);
});

const handlePageChange = (page: number) => {
  currentPage.value = page;
};
</script>

<style lang="scss" scoped>
.user-management-container {
  padding: 20px;
  background-color: #f8f9fa;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-section {
  display: flex;
  align-items: center;
  gap: 20px;

  h1 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
  }
}

.search-box {
  position: relative;
  width: 300px;

  .search-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #7d7d7d;
  }

  input {
    width: 100%;
    padding: 10px 15px 10px 40px;
    border: 1px solid #dcdfe6;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.3s;

    &:focus {
      border-color: #409eff;
      outline: none;
      box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
    }
  }
}

.create-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;

  &:hover {
    background-color: #66b1ff;
  }
}

.table-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

th {
  padding: 12px 8px;
  text-align: left;
  font-weight: 600;
  color: #606266;
  background-color: #f5f7fa;
  white-space: nowrap;
}

.avatar-header {
  width: 44px;  /* Tight fit for avatar */
  padding-left: 12px;
}

.name-header {
  width: 180px;
}

.email-header {
  width: 250px;
}

.date-header {
  width: 90px;   /* Reduced width for date columns */
  min-width: 90px;
}

.action-header {
  width: 80px;   /* Adjusted for two buttons */
  min-width: 80px;
  padding-right: 12px;
}

.user-row {
  border-bottom: 1px solid #ebeef5;
  transition: background-color 0.3s;

  &:hover {
    background-color: #f5f7fa;
  }

  &:last-child {
    border-bottom: none;
  }

  td {
    padding: 12px 8px;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
}

.avatar-cell {
  width: 44px;
  padding: 8px 4px 8px 12px !important;
  text-align: center;

  .avatar-image {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
  }
}

.name-cell {
  width: 180px;
}

.email-cell {
  width: 250px;
}

.date-cell {
  width: 90px;
  min-width: 90px;
  font-size: 0.85em;  /* Slightly smaller font */
  color: #666;
}

.action-cell {
  width: 80px;
  min-width: 80px;
  padding: 8px 12px 8px 4px !important;
  text-align: center;
  display: flex;
  gap: 4px;
  justify-content: center;

  .edit-button {
    background-color: #409eff;
    color: white;
    border: none;
    border-radius: 4px;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.2s;

    &:hover {
      background-color: #66b1ff;
    }
  }

  .delete-button {
    background-color: #ff4d4f;
    color: white;
    border: none;
    border-radius: 4px;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.2s;

    &:hover {
      background-color: #d9363e;
    }
  }
}

.pagination-section {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .search-section {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .search-box {
    width: 100%;
  }

  .create-button {
    width: 100%;
    justify-content: center;
  }
}
</style>