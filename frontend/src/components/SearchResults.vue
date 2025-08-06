<template>
  <div class="ui segment">
    <h3 class="ui header">查詢結果</h3>
    <div v-if="results.length === 0" class="ui info message">
      <div class="header">沒有找到符合條件的結果。</div>
      <p>請調整您的查詢條件後再試一次。</p>
    </div>
    <div v-else class="ui fluid container" style="overflow-x: auto;">
      <table class="ui celled table">
        <thead>
          <tr>
            <th v-for="header in tableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in results" :key="item._additional?.id || index">
            <td v-for="header in tableHeaders" :key="header">
              {{ formatValue(item[header] || item._additional[header.replace('_additional.', '')]) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchResults',
  props: {
    results: {
      type: Array,
      required: true,
    },
  },
  computed: {
    tableHeaders() {
      if (this.results.length === 0) return [];
      // Get all unique keys from the first item, including _additional properties
      const firstItem = this.results[0];
      const keys = new Set();
      for (const key in firstItem) {
        if (key === '_additional') {
          for (const additionalKey in firstItem._additional) {
            keys.add(`_additional.${additionalKey}`);
          }
        } else {
          keys.add(key);
        }
      }
      // Sort headers to put _additional.id, distance, score first
      const sortedHeaders = Array.from(keys).sort((a, b) => {
        const order = ['_additional.id', '_additional.distance', '_additional.score'];
        const indexA = order.indexOf(a);
        const indexB = order.indexOf(b);

        if (indexA !== -1 && indexB !== -1) return indexA - indexB;
        if (indexA !== -1) return -1;
        if (indexB !== -1) return 1;
        return a.localeCompare(b);
      });
      return sortedHeaders;
    },
  },
  methods: {
    formatValue(value) {
      if (typeof value === 'object' && value !== null) {
        try {
          return JSON.stringify(value, null, 2);
        } catch (e) {
          return String(value);
        }
      }
      return value;
    },
  },
};
</script>

<style scoped>
/* Add component-specific styles here if needed */
</style>
