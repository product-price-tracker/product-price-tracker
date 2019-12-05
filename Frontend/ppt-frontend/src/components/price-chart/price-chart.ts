import { Component, Prop, Vue, Ref, Watch } from 'vue-property-decorator';
import PriceList from '@/classes/PriceList';

@Component({
  name: 'price-chart',
  components: {
  },
})
export default class PriceChart extends Vue {
  historyLengths: string[] = ['1 Week', '2 Weeks', '1 Month', '3 Months', '1 Year', 'Max'];
  historyLength: string = '1 Month';

  @Prop()
  public priceDefined!: boolean;

  @Prop()
  public isLoading!: boolean;

  @Prop()
  public price!: string;

  @Prop()
  public mae!: number;

  @Prop()
  public priceHistory!: PriceList;

  @Prop()
  public pricePrediction!: PriceList;

  @Ref()
  public canvas!: HTMLCanvasElement;

  @Watch('priceHistory')
  onPriceHistoryChanged(value: string, oldValue: string) {
    Vue.nextTick(()=>this.onDraw());
  }
  @Watch('price')
  onPriceChanged(value: string, oldValue: string) {
    Vue.nextTick(()=>this.onDraw());
  }

  @Watch('maxHistory')
  onMaxHistoryChanged(value: string, oldValue: string) {
    Vue.nextTick(()=>this.onDraw());
  }

  get isPredicting(): boolean {
    return !(this.priceHistory === undefined || this.predList.length < 1);
  }

  get maxHistory(): number {
    if (this.historyLength == '1 Week') {
      return 7;
    }
    else if (this.historyLength == '2 Weeks') {
      return 14;
    }
    else if (this.historyLength == '1 Month') {
      return 30;
    }
    else if (this.historyLength == '3 Months') {
      return 90;
    }
    else if (this.historyLength == '1 Year') {
      return 365;
    }
    else {
      return 100000;
    }
  }

  get priceList(): number[] {
    let list: number[] = [];
    if (this.price == 'New') {
      list = this.priceHistory.newList;
    }
    else if (this.price == 'Amazon') {
      list = this.priceHistory.amazonList;
    }
    else if (this.price == 'Used') {
      list = this.priceHistory.usedList;
    }
    else if (this.price == 'Min Unused') {
      list = this.priceHistory.minUnusedList;
    }

    if (list.length > this.maxHistory) {
      list = list.slice(-this.maxHistory)
    }
    return list;
  }

  get predList(): number[] {
    if (this.pricePrediction === undefined) {
      this.pricePrediction = new PriceList();
    }
    if (this.price == 'New') {
      return this.pricePrediction.newList;
    }
    if (this.price == 'Amazon') {
      return this.pricePrediction.amazonList;
    }
    if (this.price == 'Used') {
      return this.pricePrediction.usedList;
    }
    else if (this.price == 'Min Unused') {
      return this.pricePrediction.minUnusedList;
    }
    return [];
  }

  onDraw() {
    const minPoint = Math.min(...this.priceList, ...this.predList);
    const maxPoint = Math.max(...this.priceList, ...this.predList);
    const range = maxPoint - minPoint;

    const pointsBetween: number = Math.floor((this.priceList.length + this.predList.length) / 15);

    const widthPerPoint = this.canvas.width / (this.priceList.length + this.predList.length - 1);
    const heightPerPoint = this.canvas.height / range;


    const today = new Date();


    const getHeight = (point: number) => (range - (point - minPoint)) * heightPerPoint;
    const ctx = this.canvas.getContext("2d")!;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    //border
    ctx.beginPath();
    ctx.lineWidth = 2;
    ctx.strokeStyle = "gray";
    ctx.rect(0, 0, this.canvas.width, this.canvas.height);
    ctx.stroke();


    //data
    for (let i = 0; i < this.priceList.length; i++) {

      ctx.beginPath();
      ctx.strokeStyle = 'blue';
      ctx.moveTo(i * widthPerPoint, getHeight(this.priceList[i]));
      ctx.lineTo((i+1) * widthPerPoint, getHeight(this.priceList[i+1]));
      ctx.stroke();

      ctx.beginPath();
      ctx.strokeStyle = 'black';
      if (i % pointsBetween == 0) {

        ctx.moveTo(i * widthPerPoint, range * heightPerPoint)
        ctx.lineTo(i * widthPerPoint, range * heightPerPoint - 14)
        ctx.stroke();

        let newDate = new Date();
        newDate.setDate(today.getDate() + i - (this.priceList.length));
        let dateString = newDate.getMonth()+1 + "/" + newDate.getDate() + "/" + newDate.getFullYear();
        ctx.fillText(dateString, i * widthPerPoint, range * heightPerPoint - 15);
        // ctx.fillText((-1*(this.priceList.length-1 - i)).toString(), i * widthPerPoint, range * heightPerPoint - 10);

      }
      else {
        ctx.moveTo(i * widthPerPoint, range * heightPerPoint)
        ctx.lineTo(i * widthPerPoint, range * heightPerPoint - 7)
        ctx.stroke();
      }
    }
    //predictions
    for (let i = 0; i < this.predList.length-1; i++) {
      ctx.beginPath();
      ctx.strokeStyle = "red";
      let startWidth = (this.priceList.length-1) * widthPerPoint;
      ctx.moveTo(startWidth+ i * widthPerPoint, getHeight(this.predList[i]));
      ctx.lineTo(startWidth+ (i+1) * widthPerPoint, getHeight(this.predList[i+1]));
      ctx.stroke();

      ctx.beginPath();
      ctx.strokeStyle = 'black';
      if (i % pointsBetween == 0) {

        ctx.moveTo(startWidth + i * widthPerPoint, range * heightPerPoint)
        ctx.lineTo(startWidth + i * widthPerPoint, range * heightPerPoint - 14)
        ctx.stroke();

        let newDate = new Date();
        newDate.setDate(today.getDate() + i);
        let dateString = newDate.getMonth()+1 + "/" + newDate.getDate() + "/" + newDate.getFullYear();
        ctx.fillText(dateString, startWidth + i * widthPerPoint, range * heightPerPoint - 15);
        // ctx.fillText((-1*(this.priceList.length-1 - i)).toString(), i * widthPerPoint, range * heightPerPoint - 10);

      }
      else {
        ctx.moveTo(startWidth + i * widthPerPoint, range * heightPerPoint)
        ctx.lineTo(startWidth + i * widthPerPoint, range * heightPerPoint - 7)
        ctx.stroke();
      }
    }
    ctx.beginPath();
    ctx.strokeStyle = 'black';
    const vertTicks = 5;
    const heightBetweenTicks = this.canvas.height / vertTicks
    for (let i = 0; i < vertTicks; i++) {
      ctx.moveTo(0, i * heightBetweenTicks)
      ctx.lineTo(7, i * heightBetweenTicks)
      ctx.stroke();

      ctx.fillText('$' + ((vertTicks - i) * range/vertTicks + minPoint).toFixed(2).toString(), 0, i * heightBetweenTicks - 15);
    }
  }

  draw() {

  }

  // onClick() {
    // this.$emit('strategyClicked', this.priceHistory.newList)
  // }
}
