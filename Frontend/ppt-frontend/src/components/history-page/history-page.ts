import { Component, Prop, Vue, Ref } from 'vue-property-decorator';

import Page from '../page/index.vue';

import axios from "axios";
import PriceList from '@/classes/PriceList';
import PriceChart from '../price-chart/index.vue';

@Component({
  name: 'history-page',
  components: {
    PriceChart,
  },
})
export default class HistoryPage extends Page {
  prices: string[] = ['New', 'Amazon', 'Used']
  price: string = "New";
  asin: string = "";
  base: string = "http://localhost:5000";
  priceList: PriceList = new PriceList();
  isLoading: boolean = false;
  priceDefined: boolean = false;

  onGetHistory() {
    // Make HTTP Request to get hist.
    this.onStartLoading();
    axios.get(this.base + '/price-data', {
      params: {asin: this.asin}
    }).then((response) => {
      this.priceList = new PriceList(response.data.data);
      this.onStopLoading();
    })
  }

  onStartLoading() {
    this.isLoading = true;
    this.priceDefined = false;
  }

  onStopLoading() {
    this.isLoading = false;
    this.priceDefined = true;
  }
}
