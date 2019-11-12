import { Component, Prop, Vue, Ref } from 'vue-property-decorator';

import Page from '../page/index.vue'

@Component({
  name: 'predict-page',
  components: {
  },
})
export default class PredictPage extends Page {
  asin: string = "";
  price: string = "";
  prices: string[] = ["NEW", "AMAZON"];
  history: number[] = [];
  prediction: number[] = [];

  onSelectAsin() {
    // TODO Make HTTP Request to get valid prices for ASIN.
    this.prices = ["NEW", "AMAZON"];
  }

  onPredict() {
    // TODO Make HTTP Request to get historical price and predict future price.
    this.history = [];
    this.prediction = [];
  }
}
