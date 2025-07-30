<template>
  <div class="container">
    <NavBar v-if="auth.getIsAdmin()" />
    <ApplicantNavBar v-if="auth.getUserType() === 'APPLICANT'" />
    <EmployerNavBar v-else-if="auth.getUserType() === 'EMPLOYER'" />
    <div class="container-right">
      <div class="nav-user">
        <div class="text-nav-user">
          Xin chào, <b>{{ dataInfo?.name }}</b>
        </div>
      </div>
      <div class="box-infor">
        <div class="infor">
          <div class="infor-register" @click="handleClickInfor">
            <div v-if="isArrowUp">
              <el-icon><ArrowDown /></el-icon>
            </div>
            <div v-if="!isArrowUp">
              <el-icon><ArrowUp /></el-icon>
            </div>
            <div><span>Thông tin đăng ký</span></div>
            <router-link to="/resetpassword" class="forgot-password-link">
              Quên mật khẩu ?
            </router-link>
          </div>
          <div class="arrowupdown" v-if="isArrowUp">
            <div class="email">
              <label>Email</label>
              <div class="input-email">
                <input type="text" v-model="updateI.email" />
                <div class="icon-input">
                  <el-icon><CircleCheckFilled /></el-icon>
                </div>
              </div>
            </div>
            <div class="button-edit">
              <button @click="showPasswordDialog('email')">
                <el-icon><EditPen /></el-icon>
                <span>Cập nhật email</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="container-box-private">
        <div class="box-infor-private">
          <h3>Thông tin cá nhân</h3>
          <div class="box-image">
            <img src="http://www.gravatar.com/avatar/?d=mp" alt="avatar" />
          </div>
          <div class="border"></div>
          <div class="flex-input">
            <div class="name">
              <label>Họ và tên</label>
              <input v-model="updateI.name" type="text" />
            </div>
            <div class="age">
              <label>Tuổi</label>
              <input type="text" v-model="updateI.age" />
            </div>
          </div>
          <div class="button-edit-infor">
            <button @click="showPasswordDialog('info')">
              <el-icon><Edit /></el-icon><span> Cập nhật </span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Password Verification Dialog -->
    <el-dialog
      v-model="passwordDialogVisible"
      title="Xác nhận mật khẩu"
      width="30%"
      :before-close="handleClose"
    >
      <el-form :model="passwordForm" label-width="120px">
        <el-form-item label="Mật khẩu" required>
          <el-input
            v-model="passwordForm.password"
            type="password"
            show-password
            placeholder="Nhập mật khẩu của bạn"
          />
        </el-form-item>
      </el-form>
      <span class="error-message" v-if="passwordError">{{ passwordError }}</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="passwordDialogVisible = false">Hủy</el-button>
          <el-button type="primary" @click="verifyPassword">
            Xác nhận
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { useAuthStore } from "../../stores/auth";
import NavBar from "../../layouts/NavBar/index.vue"
import EmployerNavBar from "../../layouts/EmployerNavBar/index.vue";
import ApplicantNavBar from "../../layouts/ApplicantNavBar/index.vue";
import { ref, onBeforeMount, watch } from "vue";
import { updateInfo, getInfo, getUserById, loginApi } from "@/services/user.service";
import { IUpdate, ILogin } from "@/types/user";
import { ElNotification, ElMessage } from "element-plus";
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const isArrowUp = ref(false);
const dataInfo = ref<ILogin>();
const passwordDialogVisible = ref(false);
const passwordForm = ref({
  password: ""
});
const passwordError = ref("");
const updateType = ref<"email" | "info">("info");

// Password verification and update functions
const showPasswordDialog = (type: "email" | "info") => {
  updateType.value = type;
  passwordDialogVisible.value = true;
  passwordForm.value.password = "";
  passwordError.value = "";
};

const verifyPassword = async () => {
  try {
    const userId = auth.getUserID();
    if (!userId) {
      passwordError.value = "Không tìm thấy thông tin người dùng";
      return;
    }

    const userData = await getUserById(userId);
    const storedPassword = userData.data.password; // Assuming password is returned from API
    
    if (passwordForm.value.password !== storedPassword) {
      passwordError.value = "Mật khẩu không chính xác";
      return;
    }

    passwordError.value = "";
    passwordDialogVisible.value = false;
    
    // Proceed with the update after successful verification
    await handleUpdate();
  } catch (error) {
    console.error("Error verifying password:", error);
    passwordError.value = "Đã xảy ra lỗi khi xác minh mật khẩu";
  }
};

const handleClose = (done: () => void) => {
  passwordForm.value.password = "";
  passwordError.value = "";
  done();
};

// Existing functions
onBeforeMount(async () => {
  await handleGetInfo();
  console.log("Is Admin:", auth.getIsAdmin())
});

watch(dataInfo, (newValue) => {
  if (newValue) {
    updateI.value = {
      name: newValue.name || "",
      age: newValue.age || 0,
      avatar: newValue.avatar || "",
      email: newValue.email || "",
    };
    if (newValue.user_type) {
      auth.setUserType(newValue.user_type);
    }
  }
});

const userType = ref<string | undefined>();
const handleGetInfo = async () => {
  try {
    const res = await getInfo();
    dataInfo.value = res["data"];
    if (dataInfo.value?.user_type) {
      auth.setUserType(dataInfo.value.user_type);
    }
    console.log("User Type:", auth.getUserType());
  } catch (error) {
    console.log(error);
  }
};

const updateI = ref<IUpdate>({
  name: dataInfo.value?.name,
  age: dataInfo.value?.age,
  avatar: dataInfo.value?.avatar,
  email: dataInfo.value?.email,
});

const handleClickInfor = () => {
  isArrowUp.value = !isArrowUp.value;
};

const handleUpdate = async () => {
  try {
    await updateInfo(updateI.value);

    // Sau khi cập nhật, gọi lại login để lấy token mới
    const { data } = await loginApi({
      email: updateI.value.email,
      password: passwordForm.value.password
    });
    localStorage.setItem("access_token", data.data.access_token);
    ElNotification({
      title: "Thành công",
      message: "Cập nhật thông tin thành công!",
      type: "success",
    });
    await handleGetInfo(); // Refresh user data
  } catch (error) {
    ElNotification({
      title: "Lỗi",
      message: "Cập nhật thông tin thất bại!",
      type: "error",
    });
    console.error(error);
  }
};
</script>

<style scoped>
.container {
  display: grid;
  grid-template-columns: 250px auto;
  overflow-x: hidden;
  padding-top: 20px;
}
.nav-user {
  width: 100%;
  height: 50px;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 0;
  box-shadow: 2px 2px 2px 0px rgb(0, 0, 0, 0.2);
}
.text-nav-user {
  padding-left: 30px;
}
.box-infor {
  width: 100%;
  padding: 0 30px;
}
.infor {
  transition: all 0.5s ease-in-out;
}
.infor-register {
  width: 100%;
  height: 50px;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  padding: 0;
  box-shadow: 2px 2px 2px 2px rgb(0, 0, 0, 0.2);
  padding-left: 30px;
  cursor: pointer;
  justify-content: space-between; /* Added to distribute space */
}
.infor-register span {
  margin-left: 5px;
}
.arrowupdown {
  gap: 50px;
  width: 100%;
  height: 100px;
  background-color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
  box-shadow: 2px 2px 2px 2px rgb(0, 0, 0, 0.2);
  padding-left: 30px;
}
.email {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 20px;
  gap: 20px;
}
.email label {
  font-size: 14px;
}
.email input {
  padding: 5px;
  outline: none;
  width: 350px;
}
.input-email {
    position: relative;

}
.icon-input {
  position: absolute;
  top: 20%;
  left: 80%;
  color: #3a91ee;
  z-index: 1;
}
.button-edit {
  margin-right: 100px;
}
.button-edit button {
  padding: 7px 20px;
  background-color: #f1ecf6;
  border: none;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}
.button-edit button:hover {
  background-color: #afa8e0;
}
.container-box-private {
  width: 100%;
  padding: 0 30px;
}
.box-infor-private {
  width: 100%;
  height: auto;
  background-color: #ffffff;
  box-shadow: 2px 2px 2px 2px rgb(0, 0, 0, 0.2);
  padding-left: 30px;
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  padding-right: 30px;
  padding-bottom: 50px;
}
.box-image img {
  border-radius: 50%;
}
.border {
  width: 100%;
  padding: 5px;
  border-bottom: 1px solid black;
}
.flex-input {
  display: flex;
  gap: 60px;
}
.flex-input input {
  padding: 5px;
  position: relative;
  outline: none;
  width: 450px;
}
.flex-input label {
  padding-right: 15px;
  font-weight: 700;
  font-size: 14px;
}
.name {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.age {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.button-edit-infor button {
  padding: 7px 20px;
  background-color: #f1ecf6;
  border: none;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  margin-left: auto;
  margin-right: 80px;
}
.button-edit-infor button:hover {
  background-color: #afa8e0;
}
.error-message {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 10px;
  display: block;
}

/* Added styles for the link */
.forgot-password-link {
  color: #3a91ee; /* Link color */
  text-decoration: none; /* Remove underline */
  font-size: 14px; /* Adjust font size */
  transition: color 0.3s ease; /* Smooth transition for hover effect */
  margin-right: 30px; /* Keep some space from the right border */
}

.forgot-password-link:hover {
  color: #2766a1; /* Darker color on hover */
}
</style>