<template>
  <div class="ui form">
    <h3 class="ui header">查詢設定</h3>

    <div class="field">
      <label>Class 選擇</label>
      <select class="ui dropdown" v-model="selectedClass" @change="handleClassChange">
        <option value="">請選擇一個 Class</option>
        <option v-for="cls in classNames" :key="cls" :value="cls">{{ cls }}</option>
      </select>
    </div>

    <div v-if="selectedClass" class="field">
      <label>屬性欄位選擇</label>
      <div class="ui grid">
        <div class="four wide column" v-for="prop in classProperties" :key="prop.name">
          <div class="ui checkbox">
            <input type="checkbox" v-model="selectedProperties" :value="prop.name" />
            <label>{{ prop.name }} ({{ prop.dataType.join(', ') }})</label>
          </div>
        </div>
      </div>
    </div>

    <div class="inline fields">
      <label>查詢類型</label>
      <div class="field">
        <div class="ui radio checkbox">
          <input type="radio" name="queryType" value="vector" v-model="queryType" />
          <label>向量相似性查詢 (Vector Search)</label>
        </div>
      </div>
      <div class="field">
        <div class="ui radio checkbox">
          <input type="radio" name="queryType" value="keyword" v-model="queryType" />
          <label>關鍵字查詢 (Keyword Search)</label>
        </div>
      </div>
      <div class="field">
        <div class="ui radio checkbox">
          <input type="radio" name="queryType" value="hybrid" v-model="queryType" />
          <label>混合式查詢 (Hybrid Search)</label>
        </div>
      </div>
    </div>

    <div class="field" v-if="queryType === 'vector' || queryType === 'hybrid'">
      <label>嵌入模型名稱 (選填)</label>
      <input type="text" v-model="embeddingModel" placeholder="例如: text-embedding-ada-002" />
    </div>

    <div class="field">
      <label>查詢文字 / 關鍵字</label>
      <textarea rows="3" v-model="queryText"></textarea>
    </div>

    <div class="field" v-if="queryType === 'hybrid'">
      <label>混合式查詢 Alpha 參數: {{ alpha.toFixed(1) }}</label>
      <input type="range" min="0" max="1" step="0.1" v-model.number="alpha" />
    </div>

    <div class="field">
      <label>篩選條件 (JSON 格式)</label>
      <textarea rows="5" v-model="filterJson" placeholder='例如: {"path": ["propertyName"], "operator": "Equal", "valueText": "someValue"}'></textarea>
      <small>支援運算子: Equal, NotEqual, LessThan, LessThanEqual, GreaterThan, GreaterThanEqual, ContainsAny, ContainsAll, And, Or</small>
    </div>

    <div class="two fields">
      <div class="field">
        <label>限制數量 (Limit)</label>
        <input type="number" v-model.number="limit" min="1" />
      </div>
      <div class="field">
        <label>偏移量 (Offset)</label>
        <input type="number" v-model.number="offset" min="0" />
      </div>
    </div>

    <button class="ui primary button" :class="{ loading: querying }" @click="executeQuery">
      執行查詢
    </button>
    <div v-if="queryError" class="ui negative message">
      <div class="header">查詢失敗</div>
      <p>{{ queryError }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'QueryForm',
  props: {
    weaviateSchema: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      selectedClass: '',
      classProperties: [],
      selectedProperties: [],
      queryType: 'vector', // Default query type
      embeddingModel: '',
      queryText: '',
      alpha: 0.5,
      filterJson: '',
      limit: 10,
      offset: 0,
      querying: false,
      queryError: null,
    };
  },
  computed: {
    classNames() {
      return this.weaviateSchema.classes ? this.weaviateSchema.classes.map(cls => cls.class) : [];
    },
  },
  watch: {
    weaviateSchema: {
      immediate: true,
      handler(newSchema) {
        if (newSchema && newSchema.classes && newSchema.classes.length > 0) {
          this.checkUrlClassParam();
        }
      },
    },
  },
  methods: {
    checkUrlClassParam() {
      const urlParams = new URLSearchParams(window.location.search);
      const classFromParam = urlParams.get('class');
      if (classFromParam && this.classNames.includes(classFromParam)) {
        this.selectedClass = classFromParam;
        this.loadClassProperties();
      } else if (this.classNames.length > 0) {
        // Optionally select the first class if no param or invalid param
        // this.selectedClass = this.classNames[0];
        // this.loadClassProperties();
      }
    },
    handleClassChange() {
      this.loadClassProperties();
      this.saveSelectedProperties(); // Save current state before loading new
    },
    loadClassProperties() {
      const selectedClassObj = this.weaviateSchema.classes.find(
        cls => cls.class === this.selectedClass
      );
      if (selectedClassObj) {
        this.classProperties = selectedClassObj.properties || [];
        this.loadSelectedProperties(); // Load saved properties for this class
      } else {
        this.classProperties = [];
        this.selectedProperties = [];
      }
    },
    loadSelectedProperties() {
      const savedProps = localStorage.getItem(`weaviate_props_${this.selectedClass}`);
      if (savedProps) {
        this.selectedProperties = JSON.parse(savedProps);
      } else {
        // Default: select all properties if no saved state
        this.selectedProperties = this.classProperties.map(prop => prop.name);
      }
    },
    saveSelectedProperties() {
      localStorage.setItem(`weaviate_props_${this.selectedClass}`, JSON.stringify(this.selectedProperties));
    },
    async executeQuery() {
      this.querying = true;
      this.queryError = null;
      this.saveSelectedProperties(); // Save current property selection before query

      try {
        let filter = null;
        if (this.filterJson) {
          try {
            filter = JSON.parse(this.filterJson);
          } catch (e) {
            this.queryError = '篩選條件 JSON 格式錯誤: ' + e.message;
            return;
          }
        }

        const payload = {
          weaviate_url: this.$parent.weaviateUrl, // Access Weaviate URL from parent (App.vue or ConnectionSettings)
          className: this.selectedClass,
          queryText: this.queryText,
          queryType: this.queryType,
          alpha: this.queryType === 'hybrid' ? this.alpha : undefined,
          embeddingModel: (this.queryType === 'vector' || this.queryType === 'hybrid') ? this.embeddingModel : undefined,
          filter: filter,
          limit: this.limit,
          offset: this.offset,
          properties: this.selectedProperties,
        };

        const response = await axios.post('/api/query', payload);
        this.$emit('query-executed', response.data);
      } catch (error) {
        console.error('Error executing query:', error);
        this.queryError = error.response?.data?.detail || error.message;
        this.$emit('query-executed', []); // Emit empty array on error
      } finally {
        this.querying = false;
      }
    },
  },
};
</script>

<style scoped>
.ui.grid {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
