import { Component, Prop, Vue, Ref } from 'vue-property-decorator';

import Page from '../page/index.vue'

@Component({
  name: 'rate-page',
  components: {
  },
})
export default class RatePage extends Page {
  asin: string = "";
  priceRating: number = 0;

  get priceRatingColor() {
    return Math.log(this.priceRating);
  }

  onRate() {
    // TODO Make HTTP Request to rate price.
    this.priceRating = 1;
  }
}
