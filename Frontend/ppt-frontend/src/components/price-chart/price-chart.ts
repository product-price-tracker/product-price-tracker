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
    return [];
  }

  onDraw() {
    const minPoint = Math.min(...this.priceList, ...this.predList);
    const maxPoint = Math.max(...this.priceList, ...this.predList);
    const range = maxPoint - minPoint;



    const widthPerPoint = this.canvas.width / (this.priceList.length + this.predList.length - 1);
    const heightPerPoint = this.canvas.height / range;


    const getHeight = (point: number) => (range - (point - minPoint)) * heightPerPoint;
    const ctx = this.canvas.getContext("2d")!;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    ctx.beginPath();
    ctx.strokeStyle = 'black';
    //data
    for (let i = 0; i < this.priceList.length-1; i++) {
      ctx.moveTo(i * widthPerPoint, getHeight(this.priceList[i]));
      ctx.lineTo((i+1) * widthPerPoint, getHeight(this.priceList[i+1]));
      ctx.stroke();

      ctx.moveTo(i * widthPerPoint, range * heightPerPoint)
      ctx.lineTo(i * widthPerPoint, range * heightPerPoint - 7)
      ctx.stroke();

      ctx.fillText(i.toString(), i * widthPerPoint + 5, range * heightPerPoint - 5);
    }
    //predictions
    ctx.beginPath();
    ctx.strokeStyle = "pink";
    for (let i = 0; i < this.predList.length-1; i++) {
      let startWidth = (this.priceList.length-1) * widthPerPoint;
      ctx.moveTo(startWidth+ i * widthPerPoint, getHeight(this.predList[i]));
      ctx.lineTo(startWidth+ (i+1) * widthPerPoint, getHeight(this.predList[i+1]));
      ctx.stroke();

      ctx.moveTo(startWidth+ i * widthPerPoint, range * heightPerPoint)
      ctx.lineTo(startWidth+ i * widthPerPoint, range * heightPerPoint - 7)
      ctx.stroke();

      ctx.fillText(i.toString(), startWidth + i * widthPerPoint + 5, range * heightPerPoint - 5);
    }
    ctx.beginPath();
    ctx.strokeStyle = 'black';
    const vertTicks = 5;
    const heightBetweenTicks = this.canvas.height / vertTicks
    for (let i = 0; i < vertTicks; i++) {
      ctx.moveTo(0, i * heightBetweenTicks)
      ctx.lineTo(7, i * heightBetweenTicks)
      ctx.stroke();

      ctx.fillText('$' + ((vertTicks - i) * range/vertTicks + minPoint).toString(), 5, i * heightBetweenTicks - 5);
    }
  }

  draw() {

  }

  // onClick() {
    // this.$emit('strategyClicked', this.priceHistory.newList)
  // }
}
