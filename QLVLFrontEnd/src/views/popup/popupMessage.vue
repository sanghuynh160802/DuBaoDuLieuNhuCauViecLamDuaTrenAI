<template>
  <div class="popup-overlay" @click.self="emitClose">
    <div class="popup-container">
      <div class="popup-header">
        <h2>Send Message to Applicant</h2>
        <button class="close-btn" @click="emitClose">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="message-form">
        <div class="form-section">
          <div class="form-group full-width">
            <label for="message">Your Message*</label>
            <textarea 
              id="message" 
              v-model="messageContent" 
              rows="6" 
              required 
              placeholder="Write your message to the applicant..."
            ></textarea>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="emitClose">Cancel</button>
          <div class="decision-buttons">
            <button 
              type="button" 
              class="reject-btn"
              @click="handleReject"
            >
              Từ chối
            </button>
            <button 
              type="button" 
              class="approve-btn"
              @click="handleApprove"
            >
              Duyệt
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElNotification } from "element-plus";

const emits = defineEmits<{
  (e: "close-popup"): void;
  (e: "message-sent", type: 'approve' | 'reject', content: string): void;
}>();

const messageContent = ref("");

const emitClose = () => {
  emits("close-popup");  // <-- correct event name
};

const handleApprove = () => {
  if (!messageContent.value) {
    ElNotification({
      title: "Error",
      message: "Please enter a message",
      type: "error",
    });
    return;
  }
  
  emits("message-sent", 'approve', messageContent.value);
};

const handleReject = () => {
  if (!messageContent.value) {
    ElNotification({
      title: "Error",
      message: "Please enter a message",
      type: "error",
    });
    return;
  }
  
  emits("message-sent", 'reject', messageContent.value);
};

const handleSubmit = () => {
  // Default submit action (if needed)
  // By default we'll treat this as an approval
  handleApprove();
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
  width: 600px;
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

.message-form {
  padding: 0 25px 25px;
}

.form-section {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group.full-width {
  width: 100%;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  color: #4a5568;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: all 0.2s;
  background-color: #f8fafc;
  min-height: 150px;
  resize: vertical;
}

textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
  background-color: white;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eaeaea;
}

.cancel-btn {
  padding: 10px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #4a5568;
}

.cancel-btn:hover {
  background-color: #edf2f7;
}

.decision-buttons {
  display: flex;
  gap: 10px;
}

.approve-btn,
.reject-btn {
  padding: 10px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.approve-btn {
  background-color: #48bb78;
  color: white;
}

.approve-btn:hover {
  background-color: #38a169;
}

.reject-btn {
  background-color: #f56565;
  color: white;
}

.reject-btn:hover {
  background-color: #e53e3e;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .decision-buttons {
    width: 100%;
  }
  
  .cancel-btn,
  .approve-btn,
  .reject-btn {
    width: 100%;
  }
}
</style>