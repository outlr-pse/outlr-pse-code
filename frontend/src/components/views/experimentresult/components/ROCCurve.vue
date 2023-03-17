<template>
  <Line :data="data" :options="options"/>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import {Experiment} from "../../../../models/experiment/Experiment";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import {Line} from 'vue-chartjs'
import {ButtonType} from "../../../basic/button/ButtonType";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

export default defineComponent({
  name: "ROCCurve",
  components: {Line},
  props: {
    experiment: {
      type: Experiment,
      required: true
    }
  },
  data() {
    const experimentResult = this.experiment.experimentResult;
    return {
      data: {
        labels: experimentResult ? experimentResult.fpr : [],
        datasets: [
          {
            label: 'ROC Curve',
            data: experimentResult ? experimentResult.tpr : [],
            backgroundColor: 'rgb(32,32,32)',
            borderColor: 'rgb(146,95,240)',
            borderWidth: 2
          }
        ]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            type: 'linear',
          },
          x: {
            beginAtZero: true,
            type: 'linear',
          }
        },
        aspectRatio: 1,
        pointRadius: 0,
        events: [],
      }
    }
  }
})
</script>

<style scoped>

</style>