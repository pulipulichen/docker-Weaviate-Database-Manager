<template>
  <div class="ui form">
    <h3 class="ui header">修改單一物件屬性</h3>
    <div class="field">
      <label>Weaviate 實例 URL</label>
      <input type="text" v-model="weaviateUrl" placeholder="例如: http://localhost:8080" />
    </div>
    <div class="field">
      <label>Class 名稱</label>
      <input type="text" v-model="className" placeholder="例如: Article" />
    </div>
    <div class="field">
      <label>物件 ID (UUID)</label>
      <input type="text" v-model="objectId" placeholder="例如: a1b2c3d4-e5f6-7890-1234-567890abcdef" />
    </div>
    <div class="field">
      <label>屬性名稱</label>
      <input type="text" v-model="propertyName" placeholder="例如: title" />
    </div>
    <div class="field">
      <label>新值 (New Value)</label>
      <textarea rows="3" v-model="newValue" placeholder="輸入新值，JSON 物件/陣列請使用有效 JSON 格式"></textarea>
      <small>對於物件或陣列，請輸入有效的 JSON 字串。</small>
    </div>
    <button class="ui primary button" :class="{ loading: modifying }" @click="modifyObjectProperty">
      修改物件屬性
    </button>
    <div v-if="modifyStatus === 'success'" class="ui positive message">
      <div class="header">修改成功</div>
      <p>{{ modifyMessage }}</p>
    </div>
    <div v-if="modifyStatus === 'error'" class="ui negative message">
      <div class="header">修改失敗</div>
      <p>{{ modifyMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ModifyObject',
  data() {
    return {
      weaviateUrl: 'http://localhost:8080', // Default, can be updated by user
      className: '',
      objectId: '',
      propertyName: '',
      newValue: '',
      modifying: false,
      modifyStatus: null, // 'success' or 'error'
      modifyMessage: '',
    };
  },
  methods: {
    async modifyObjectProperty() {
      this.modifying = true;
      this.modifyStatus = null;
      this.modifyMessage = '';

      let parsedValue = this.newValue;
      try {
        // Attempt to parse as JSON if it looks like an object or array
        if ((this.newValue.startsWith('{') && this.newValue.endsWith('}')) ||
            (this.newValue.startsWith('[') && this.newValue.endsWith(']'))) {
          parsedValue = JSON.parse(this.newValue);
        }
      } catch (e) {
        this.modifyStatus = 'error';
        this.modifyMessage = '新值 JSON 格式錯誤: ' + e.message;
        this.modifying = false;
        return;
      }

      try {
        const payload = {
          weaviate_url: this.weaviateUrl,
          className: this.className,
          id: this.objectId,
          propertyName: this.propertyName,
          value: parsedValue,
        };

        const response = await axios.patch('/api/object', payload);
        this.modifyStatus = 'success';
        this.modifyMessage = response.data.message || '物件屬性修改成功。';
      } catch (error) {
        console.error('Error modifying object property:', error);
        this.modifyStatus = 'error';
        this.modifyMessage = error.response?.data?.detail || error.message;
      } finally {
        this.modifying = false;
      }
    },
  },
};
</script>

<style scoped>
/* Add component-specific styles here if needed */
</style>
