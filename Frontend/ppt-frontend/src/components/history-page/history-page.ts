import { Component, Prop, Vue, Ref } from 'vue-property-decorator';

import Page from '../page/index.vue';

import axios from "axios";

@Component({
  name: 'history-page',
  components: {
  },
})
export default class HistoryPage extends Page {
  asin: string = "";
  base: string = "http://localhost:5000";
  priceList: PriceList = {};

  onHistory() {
    // TODO Make HTTP Request to rate price.
    axios.get(this.base + '/price-data', {
      params: {asin: this.asin}
    }).then((response) => {
      this.priceRating = response.data
    })
  }
}
