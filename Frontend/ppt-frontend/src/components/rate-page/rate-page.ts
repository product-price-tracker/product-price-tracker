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
  priceRating: number = 0;
  base: string = "http://localhost:5000";

  get priceRatingColor() {
    return Math.log(this.priceRating);
  }

  onRate() {
    // TODO Make HTTP Request to rate price.
    axios.get(this.base + '/rate', {
      params: {asin: this.asin}
    }).then((response) => {
      this.priceRating = response.data
    })
  }
}
