<template>
  <div id="app" class="ui container">
    <h1 class="ui dividing header">Weaviate 查詢應用程式</h1>

    <div class="ui grid">
      <div class="eight wide column">
        <div class="ui segment">
          <ConnectionSettings @schema-loaded="handleSchemaLoaded" />
        </div>
      </div>
      <div class="eight wide column" v-if="schemaLoaded">
        <div class="ui segment">
          <ModifyObject />
        </div>
      </div>
    </div>

    <div class="ui segment" v-if="schemaLoaded">
      <QueryForm :weaviateSchema="weaviateSchema" @query-executed="handleQueryExecuted" />
    </div>

    <div class="ui segment" v-if="searchResults.length > 0">
      <SearchResults :results="searchResults" />
    </div>
  </div>
</template>

<script>
import ConnectionSettings from './components/ConnectionSettings.vue';
import QueryForm from './components/QueryForm.vue';
import SearchResults from './components/SearchResults.vue';
import ModifyObject from './components/ModifyObject.vue';

export default {
  name: 'App',
  components: {
    ConnectionSettings,
    QueryForm,
    SearchResults,
    ModifyObject,
  },
  data() {
    return {
      weaviateSchema: null,
      schemaLoaded: false,
      searchResults: [],
    };
  },
  methods: {
    handleSchemaLoaded(schema) {
      this.weaviateSchema = schema;
      this.schemaLoaded = true;
      this.searchResults = []; // Clear previous results on new connection
    },
    handleQueryExecuted(results) {
      this.searchResults = results;
    },
  },
};
</script>

<style>
#app {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
