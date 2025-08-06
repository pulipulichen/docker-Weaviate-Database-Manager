<template>
  <div class="ui form">
    <h3 class="ui header">Weaviate 連線設定</h3>
    <div class="field">
      <label>Weaviate 實例 URL</label>
      <div class="ui action input">
        <input type="text" v-model="weaviateUrl" placeholder="例如: http://localhost:8080" />
        <button class="ui primary button" :class="{ loading: connecting }" @click="connectToWeaviate">
          連線並載入 Schema
        </button>
      </div>
    </div>
    <div v-if="connectionError" class="ui negative message">
      <div class="header">連線失敗</div>
      <p>{{ connectionError }}</p>
    </div>
    <div v-if="schemaLoaded" class="ui positive message">
      <div class="header">連線成功</div>
      <p>已成功連線到 Weaviate 並載入 Schema。</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ConnectionSettings',
  data() {
    return {
      weaviateUrl: '',
      connecting: false,
      connectionError: null,
      schemaLoaded: false,
    };
  },
  mounted() {
    // Check for WEAVIATE_URL environment variable (passed via Nginx/Docker-compose)
    // In a real Vue app, this would typically be accessed via a global variable set by Vite/Webpack
    // For this setup, we'll assume it's available on window._env_ or similar, or directly from the URL param
    // For simplicity, we'll use a placeholder for now and rely on manual input or URL param later.
    // The spec mentions "前端啟動時，應檢查是否存在名為 WEAVIATE_URL 的環境變數。如果存在，則自動將其值填充到 URL 輸入框中，並嘗試自動連線。"
    // This implies a build-time or runtime injection. For now, we'll simulate it.
    const urlParams = new URLSearchParams(window.location.search);
    const weaviateUrlFromParam = urlParams.get('weaviate_url');
    if (weaviateUrlFromParam) {
      this.weaviateUrl = weaviateUrlFromParam;
      this.connectToWeaviate();
    } else if (process.env.VUE_APP_WEAVIATE_URL) { // Example for Vite/Vue CLI env var
      this.weaviateUrl = process.env.VUE_APP_WEAVIATE_URL;
      this.connectToWeaviate();
    } else if (window.WEAVIATE_URL) { // Example for Nginx injected env var
      this.weaviateUrl = window.WEAVIATE_URL;
      this.connectToWeaviate();
    } else {
      // Default to localhost if nothing else is found
      this.weaviateUrl = 'http://localhost:8080';
    }
  },
  methods: {
    async connectToWeaviate() {
      this.connecting = true;
      this.connectionError = null;
      this.schemaLoaded = false;
      try {
        const response = await axios.get(`/api/schema?weaviate_url=${this.weaviateUrl}`);
        this.$emit('schema-loaded', response.data);
        this.schemaLoaded = true;
      } catch (error) {
        console.error('Error connecting to Weaviate:', error);
        this.connectionError = error.response?.data?.detail || error.message;
      } finally {
        this.connecting = false;
      }
    },
  },
};
</script>

<style scoped>
/* Add component-specific styles here if needed */
</style>
