<template>
  <div class="job-crawl-container">
    <div class="header">
      <button
        :class="isCrawling && currentCrawlType === 'urls' ? 'stop-button' : 'crawl-url-button'"
        @click="toggleCrawlUrl"
        :disabled="isCrawling && currentCrawlType !== 'urls'"
      >
        {{ isCrawling && currentCrawlType === 'urls' ? "STOP CRAWLING" : "CRAWL JOB URL" }}
      </button>
      <button
        :class="isCrawling && currentCrawlType === 'info' ? 'stop-button' : 'crawl-button'"
        @click="toggleCrawlData"
        :disabled="isCrawling && currentCrawlType !== 'info'"
      >
        {{ isCrawling && currentCrawlType === 'info' ? "STOP CRAWLING" : "CRAWL JOB DATA" }}
      </button>
    </div>

    <div class="log-container">
      <pre v-if="!isCrawling || jobDataLog">
{{ jobDataLog }}
      </pre>
      <pre v-else class="loading-line">
        <span class="loading-text">LOADING</span>
        <span class="spinner-dots">
          <span class="dot dot1">.</span>
          <span class="dot dot2">.</span>
          <span class="dot dot3">.</span>
        </span>
      </pre>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from "vue";
import { crawlJobUrlsTopdev, crawlJobInfoTopdev, stopCrawling } from "@/services/user.service";

const isCrawling = ref(false);
const currentCrawlType = ref(null);
const jobDataLog = ref("");
let abortController = new AbortController();

const toggleCrawlUrl = async () => {
  if (isCrawling.value) {
    if (currentCrawlType.value === 'urls') {
      await stopCrawlingProcess();
    }
    return;
  }
  startCrawling('urls', crawlJobUrlsTopdev);
};

const toggleCrawlData = async () => {
  if (isCrawling.value) {
    if (currentCrawlType.value === 'info') {
      await stopCrawlingProcess();
    }
    return;
  }
  startCrawling('info', crawlJobInfoTopdev);
};

const startCrawling = async (type, crawlFunction) => {
  try {
    jobDataLog.value = "";
    isCrawling.value = true;
    currentCrawlType.value = type;
    abortController = new AbortController();

    const response = await crawlFunction(abortController.signal);
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (isCrawling.value) {
      const { done, value } = await reader.read();
      if (done) break;
      jobDataLog.value += decoder.decode(value);
    }
  } catch (error) {
    handleCrawlError(error);
  } finally {
    resetCrawlingState();
  }
};

const stopCrawlingProcess = async () => {
  try {
    abortController.abort();
    
    const scriptKey = currentCrawlType.value === 'urls' 
      ? 'crawl-job-urls-topdev' 
      : 'crawl-job-info-topdev';
    
    await stopCrawling(scriptKey);
    jobDataLog.value += "\nCrawl stopped by user.";
  } catch (error) {
    jobDataLog.value += `\nError stopping crawl: ${error.message}`;
  }
};

const handleCrawlError = (error) => {
  if (error.name === 'AbortError') {
    jobDataLog.value += "\nCrawl aborted by user.";
  } else {
    jobDataLog.value += `\nError during crawl: ${error.message}`;
    console.error("Crawling error:", error);
  }
};

const resetCrawlingState = () => {
  isCrawling.value = false;
  currentCrawlType.value = null;
};

onBeforeUnmount(() => {
  if (isCrawling.value) {
    abortController.abort();
  }
});
</script>

<style scoped>
.job-crawl-container {
  padding: 20px;
  background-color: #f8f8f8;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.crawl-url-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
}

.crawl-url-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.stop-button {
  background-color: #d32f2f;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
}

.crawl-button {
  background-color: #673ab7;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
}

.crawl-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.log-container {
  background-color: black;
  color: #00ff00;
  padding: 15px;
  flex: 1;
  overflow-y: auto;
  font-family: "Courier New", monospace;
  border-radius: 5px;
  max-height: 100%;
}

/* Spinner dots animation */
.spinner-dots {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  height: 100%;
  color: #00ff00;
}

.dot {
  animation: blink 1.4s infinite both;
}

.dot1 {
  animation-delay: 0s;
}

.dot2 {
  animation-delay: 0.2s;
}

.dot3 {
  animation-delay: 0.4s;
}

@keyframes blink {
  0%, 80%, 100% {
    opacity: 0;
  }
  40% {
    opacity: 1;
  }
}

.loading-line {
  display: flex;
  align-items: center;
  font-family: "Courier New", monospace;
  color: #00ff00;
}

.loading-text {
  font-weight: bold;
  font-size: 24px;
}

</style>
