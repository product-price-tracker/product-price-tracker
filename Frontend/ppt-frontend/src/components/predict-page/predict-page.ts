import { Component, Prop, Vue, Ref } from 'vue-property-decorator';

import Page from '../page/index.vue';

import axios from "axios";
import PriceList from '@/classes/PriceList';
import PriceChart from '../price-chart/index.vue';

@Component({
  name: 'predict-page',
  components: {
    PriceChart,
  },
})
export default class PredictPage extends Page {
  prices: string[] = ['New', 'Amazon', 'Min Unused']
  price: string = "Min Unused";
  daysAhead: number = 14;
  asin: string = "";
  base: string = "http://localhost:5000";
  mae: number = 0;
  dataList: PriceList = new PriceList();
  predList: PriceList = new PriceList();
  isLoading: boolean = false;
  priceDefined: boolean = false;
  daysAheadList: number[] = [...Array(100).keys()].map(x=>x+1);

  onPredict() {
    // Make HTTP Request to get hist+prediction.
    this.onStartLoading();
    axios.get(this.base + '/predict', {
      params: {
        asin: this.asin,
        price: this.price.replace(/ /g,"_").toUpperCase(),
        daysAhead: this.daysAhead
      }
    }).then((response) => {
      this.dataList = new PriceList();
      this.dataList.timeList = response.data.data_times;
      this.predList = new PriceList();
      this.predList.timeList = response.data.prediction_times;
      if (this.price == "New") {
        this.dataList.newList = response.data.data_values;
        this.predList.newList = response.data.prediction_values;
      }
      if (this.price == "Amazon") {
        this.dataList.amazonList = response.data.data_values;
        this.predList.amazonList = response.data.prediction_values;
      }
      if (this.price == "Min Unused") {
        this.dataList.minUnusedList = response.data.data_values;
        this.predList.minUnusedList = response.data.prediction_values;
      }
      this.mae = response.data.mae;
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
