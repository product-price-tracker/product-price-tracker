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
  prices: string[] = ['New', 'Amazon', 'Min Unused'];
  predictors: string[] = ['Statistical', 'Machine Learning'];
  predictor: string = "Machine Learning";
  price: string = "Min Unused";
  daysAhead: number = 14;
  asin: string = "";
  base: string = "http://localhost:5000";
  mse: number = 0;
  dataList: PriceList = new PriceList();
  predList: PriceList = new PriceList();
  lowerCiList: PriceList = new PriceList();
  upperCiList: PriceList = new PriceList();
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
        daysAhead: this.daysAhead,
        predictor: this.predictor
      }
    }).then((response) => {
      this.dataList = new PriceList();
      this.dataList.timeList = response.data.data_times;
      this.predList = new PriceList();
      this.predList.timeList = response.data.prediction_times;
      this.lowerCiList = new PriceList();
      this.lowerCiList.timeList = response.data.prediction_times;
      this.upperCiList = new PriceList();
      this.upperCiList.timeList = response.data.prediction_times;
      if (this.price == "New") {
        this.dataList.newList = response.data.data_values;
        this.predList.newList = response.data.prediction_values;
        this.lowerCiList.newList = response.data.lower_ci;
        this.upperCiList.newList = response.data.upper_ci;
      }
      if (this.price == "Amazon") {
        this.dataList.amazonList = response.data.data_values;
        this.predList.amazonList = response.data.prediction_values;
        this.lowerCiList.amazonList = response.data.lower_ci;
        this.upperCiList.amazonList = response.data.upper_ci;
      }
      if (this.price == "Min Unused") {
        this.dataList.minUnusedList = response.data.data_values;
        this.predList.minUnusedList = response.data.prediction_values;
        this.lowerCiList.minUnusedList = response.data.lower_ci;
        this.upperCiList.minUnusedList = response.data.upper_ci;
      }
      this.mse = response.data.mse;
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
