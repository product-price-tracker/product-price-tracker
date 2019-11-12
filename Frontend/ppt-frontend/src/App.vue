<template>
  <div id="app">
    <toolbar @newPage="onNewPage" style="margin-bottom: 2rem;"/>
    <home-page v-if="currentPage==0"/>
    <predict-page v-if="currentPage==1"/>
    <history-page v-if="currentPage==2"/>
    <rate-page v-if="currentPage==3"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Toolbar from './components/toolbar/index.vue';
import HomePage from './components/home-page/index.vue';
import PredictPage from './components/predict-page/index.vue';
import HistoryPage from './components/history-page/index.vue';
import RatePage from './components/rate-page/index.vue';

@Component({
  components: {
    Toolbar,
    HomePage,
    PredictPage,
    HistoryPage,
    RatePage
  },
})
export default class App extends Vue {
  currentPage: number = 0;

  onNewPage(index: number) {
    this.currentPage = index;
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
