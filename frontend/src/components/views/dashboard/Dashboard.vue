<template>

  <div class="dashboard">
    <h1>
      Dashboard
    </h1>
    <div class="searchBar">
      <search-bar @search-term-changed="applySearch" class="left"/>
    </div>
    <DashboardTable :search-term="searchTerm" class="dashboard-table" :current-sorting="sortColumn"/>
  </div>
</template>

<script lang="ts">
import Tip from "../../basic/Tip.vue";
import {defineComponent} from "vue";
import DashboardTable from "./components/DashboardTable.vue";
import SearchBar from "./components/SearchBar.vue";
import {DashboardSortColumn} from "./components/DashboardSortColumn";

export default defineComponent({
  name: "Dashboard",
  components: {SearchBar, DashboardTable, Tip},
  data() {
    return {
      searchTerm: "",
      sortColumn: DashboardSortColumn.DATE
    }
  },
  methods: {
    applySearch(searchTerm: string) {
      this.searchTerm = searchTerm;
    },
  },
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}

.dashboard-table {
  margin-top: 2vh;
  height: max-content;
  margin-bottom: 12vh;
}

.searchBar {
  width: 80vw;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr;
  grid-template-areas: "searchBar sortOption";

}
.left {
  text-align: left;
}


</style>