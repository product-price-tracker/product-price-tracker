import { Component, Prop, Vue, Ref } from 'vue-property-decorator';

@Component({
  name: 'toolbar',
  components: {
  },
})
export default class Toolbar extends Vue {
  newPage(index: number) {
    this.$emit('newPage', index);
  }
}
