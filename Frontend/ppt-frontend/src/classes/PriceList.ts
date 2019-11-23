import PricePoint from './PricePoint';

export default class PriceList {
  newList: number[];
  amazonList: number[];
  usedList: number[];
  timeList: number[];

  constructor(priceList: PricePoint[]|null = null) {
    if (priceList == null) {
      this.newList = [];
      this.amazonList = [];
      this.usedList = [];
      this.timeList = [];
    }
    else {
      this.newList = priceList.map(pricePoint => pricePoint.NEW);
      this.amazonList = priceList.map(pricePoint => pricePoint.AMAZON);
      this.usedList = priceList.map(pricePoint => pricePoint.USED);
      this.timeList = priceList.map(pricePoint => pricePoint.Time);
      // this.newList = [0, 1, 2, 3, 4, 5, 3, 1, 2, 3];
      // this.amazonList = [0, 1, 2, 3, 4, 5, 3, 1, 2, 3];
      // this.salesList = [0, 1, 2, 3, 4, 5, 3, 1, 2, 3];
      // this.timeList = [0, 1, 2, 3, 4, 5, 3, 1, 2, 3];
    }
  }
}
