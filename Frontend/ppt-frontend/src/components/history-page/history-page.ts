import { Component, Prop, Vue, Ref } from 'vue-property-decorator';

import Page from '../page/index.vue'

@Component({
  name: 'history-page',
  components: {
  },
})
export default class HistoryPage extends Page {
  asin: string = "";
}
