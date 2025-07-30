<template>
  <div class="popup-wrapper">
    <div class="overlay"></div>
    <div class="popup-content">
      <div class="loader" v-if="isLoading"></div>
      <div>
        <h2>Ứng tuyển vào vị trí {{ jobTitle }} tại {{ companyName }}</h2>
      </div>
      <div class="box-input">
        <label for="username">Họ và tên *</label>
        <input
          type="text"
          id="username"
          readonly
          :value="authStore.getUserName()"
        />

        <label for="email">Email *</label>
        <input
          type="text"
          id="email"
          readonly
          :value="authStore.getEmail()"
        />

        <label for="phoneNumber">Phone Number *</label>
        <input
          v-model="phoneNumber"
          type="text"
          id="phoneNumber"
          placeholder="Enter phone number..."
        />
      </div>
      <div class="upload-cv-section">
      <label for="cvFile">📎 Tải lên CV có sẵn *</label>
      <input
        type="file"
        id="cvFile"
        accept=".pdf,.doc,.docx"
        @change="handleFileUpload"
      />
      <p class="file-info">Hỗ trợ định dạng: PDF, DOC, DOCX • Dung lượng tối đa: 5MB</p>
      <div v-if="fileError" class="error-msg">{{ fileError }}</div>
      </div>
      <div class="box-button">
            <button @click="handleSendMail">Send Mail</button>
            <button @click="emits('closePopup')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted } from "vue";
import { useAuthStore } from "../../stores/auth";
import { ISendMail } from "@/types/user";
import { ElNotification } from "element-plus"
import { sendMailApi, getUserIdByName } from "@/services/user.service"

const phoneNumber = ref("");
const selectedFile = ref<File | null>(null);
const fileError = ref("");

const fetchedUserId = ref<number | null>(null); // store fetched company_id

const props = defineProps<{
  companyName: string;
  jobTitle: string;
  jobId: string;
  userId: number | string;
  email: string;
}>();

onMounted(async () => {
  console.log('Received in PopUp:', props.companyName, props.jobTitle, props.jobId, props.userId, props.email);
  try {
    const companyId = await getUserIdByName(props.companyName);
    fetchedUserId.value = companyId;
    console.log("Fetched Company ID:", companyId);
  } catch (err) {
    console.error("Error fetching company ID:", err);
  }
});
const authStore = useAuthStore();
const userId = authStore.getUserID();

const emits = defineEmits<{
  (e: "closePopup"): void;
}>();
const sendMail = ref<ISendMail>({
    mailTo: "",
    link: window.location.href
})
const isLoading = ref<boolean>(false)
const handleFileUpload = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0] || null;
  fileError.value = "";

  if (file) {
    const validTypes = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!validTypes.includes(file.type)) {
      fileError.value = "Định dạng không hợp lệ.";
      selectedFile.value = null;
    } else if (file.size > 5 * 1024 * 1024) {
      fileError.value = "Kích thước file vượt quá 5MB.";
      selectedFile.value = null;
    } else {
      selectedFile.value = file;
    }
  }
};

const handleSendMail = async () => {
  if (!selectedFile.value) {
    fileError.value = "Vui lòng tải lên CV hợp lệ.";
    return;
  }

  isLoading.value = true;
  try {
    const reader = new FileReader();
    reader.readAsDataURL(selectedFile.value);
    reader.onload = async () => {
      const base64Content = (reader.result as string).split(",")[1]; // Remove data:*/*;base64,

      const payload = {
        applicant_id: props.userId || authStore.getUserID(),
        company_id: fetchedUserId.value,
        job_id: props.jobId,
        applicant_email: props.email || authStore.getEmail(),
        applicant_phone: phoneNumber.value,
        title: props.jobTitle,
        company_name: props.companyName,
        cv_content_base64: base64Content,
        cv_filename: selectedFile.value?.name,         // <-- Add this
        cv_mimetype: selectedFile.value?.type           // <-- Add this
      };

      await sendMailApi(payload);
      ElNotification({
        title: "Success",
        message: "Send mail successfully!",
        type: "success",
      });
      emits("closePopup");
    };
  } catch (error) {
    console.error(error);
    ElNotification({
      title: "Error",
      message: "Send mail failed!",
      type: "error",
    });
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 9001;
}

.popup-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9002; /* Đảm bảo popup luôn ở trên cùng */
}

.popup-content {
  position: relative;
  width: 500px;
  max-height: 90vh; /* Allow it to grow but not exceed the viewport */
  background-color: #fff;
  z-index: 9003;
  border-radius: 24px;
  padding: 20px;
  overflow-y: auto; /* Allow scrolling if content exceeds */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Pushes buttons to bottom */
}
.popup-content h2 {
  padding-bottom: 20px;
}
.box-input input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}

.box-input input[readonly] {
  background-color: #f9f9f9;
  cursor: not-allowed;
  opacity: 0.7;
}
.box-input label {
  font-size: 14px;
  margin-bottom: 10px;
}
.box-button button {
    padding: 10px 20px;
    background-color: #2563eb;
    border-radius: 16px;
    outline: none;
    border: none;
    cursor: pointer;
    color: white;
  }
  .box-button button:hover {
    background-color: #07379e;
  }
  .box-button {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    padding-top: 20px;
}
.loader {
    position: absolute;
    top: 45%;
    left: 45%;
    border: 8px solid #f3f3f3;
    border-top: 8px solid #3498db; 
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    
}
.upload-cv-section {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
}

.upload-cv-section label {
  font-weight: bold;
  margin-bottom: 8px;
}

.upload-cv-section input[type="file"] {
  padding: 10px;
  border-radius: 5px;
  border: 1px dashed #ccc;
  background-color: #fafafa;
}

.file-info {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

.error-msg {
  color: red;
  font-size: 13px;
  margin-top: 5px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
