import { Component, Prop, Vue, Ref } from 'vue-property-decorator';

import Page from '../page/index.vue';

import axios from "axios";


@Component({
  name: 'rate-page',
  components: {
  },
})
export default class RatePage extends Page {
  asin: string = "";
  priceRating: number = 0.0;
  base: string = "http://localhost:5000";

  underMax: number = 0.75;
  slightlyUnderMax: number = 0.9;
  fairMax: number = 1.1;
  slightlyOverMax: number = 1.5;

  get priceRatingColor(): string {
    let colorWeight = 1.0/(1+Math.pow(Math.E, -(this.priceRating-1)*4));
    let r = colorWeight;
    let g = 1-r;
    let str = "color: rgb(" + Math.floor(r*256) + "," + Math.floor(g*256) + ", 0);";
    return str;
  }

  get priceRatingDesc(): string {
    if (this.priceRating < this.underMax) {
      return "Underpriced"
    }
    else if (this.priceRating < this.slightlyUnderMax) {
      return "Slightly Underpriced"
    }
    else if (this.priceRating < this.fairMax) {
      return "Fairly Priced"
    }
    else if (this.priceRating < this.slightlyOverMax) {
      return "Slightly Overpriced"
    }
    else {
      return "Overpriced"
    }
  }

  onRate() {
    // Make HTTP Request to rate price.
    axios.get(this.base + '/rate', {
      params: {asin: this.asin}
    }).then((response) => {
      this.priceRating = response.data
    })
  }
}
