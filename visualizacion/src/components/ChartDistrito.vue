<template>
  <div class="row justify-content-center">
    <div class="col-12 text-center">
      <h2>Resultados en {{ departamento }} por grupo de edad</h2>
    </div>
    <div class="col-12">
      <highcharts :options="chartOptions"></highcharts>
    </div>
    <div class="col-12">
      <div class="row mb-3 text-center justify-content-center">

        <div class="col">
          <input class="form-check-input" type="radio" name="var_dataset" group="var_dataset" id="nPositivos" value="nPositivos" checked @click="change_data">
          <label class="form-check-label" for="nPositivos">
            Nro positivos
          </label>
        </div>

        <div class="col">
          <input class="form-check-input" type="radio" name="var_dataset"  group="var_dataset" id="nFallecidos" value="nFallecidos" @click="change_data">
          <label class="form-check-label" for="nFallecidos" >
            Nro. Fallecidos
          </label>
        </div>

        <div class="col">
          <input class="form-check-input" type="radio" name="var_dataset" id="infectadosPCP" value="infectadosPCP"  group="var_dataset" @click="change_data">
          <label class="form-check-label" for="infectadosPCP">
            Nro. infectados PCP
          </label>
        </div>

        <div class="col">
          <input class="form-check-input" type="radio" name="var_dataset" id="nFallecidos" value="nFallecidos" group="var_dataset" @click="change_data">
          <label class="form-check-label" for="muertesPCP">
            Nro. muertes PCP
          </label>
        </div>

        <div class="col">
          <input class="form-check-input" type="radio" name="var_dataset" id="tasa_fatalidad" value="tasa_fatalidad" group="var_dataset" @click="change_data">
          <label class="form-check-label" for="tasa_fatalidad">
           Tasa fatalidad
          </label>
        </div>

      </div>
        
    </div>
  </div>
</template>

<script>
  import { Chart } from 'highcharts-vue'
  import sortBy from 'lodash/sortBy'
  import map from 'lodash/map'
  import sum from 'lodash/sum'
  import groupBy from 'lodash/groupBy'
  import uniq from 'lodash/uniq'
  import moment from 'moment'

  export default {
    name: "ChartDistrito",
    components: {
      highcharts: Chart
    },
    props: {
      dataset: Array,
      departamento: String
    },
    data() {
      return {
        categories: [],
        campo: 'nPositivos'
      }
    },
    methods: {
      change_data(e) {
        console.log(e.target.value)
        this.campo = e.target.value
      }
    },
    computed: {
      comprasDiarias() {
        let data = sortBy(this.dataset, 'name')
        return data
      },
      chartOptions() {
        return {
          title: {
              text: ''
          },
          subtitle: {
              text: ''
          },
          tooltip: {
            pointFormat: '{series.name}: <b>{point.y}',
            shared: true
          },
          xAxis: {        
            categories: this.categories_data
          },
          yAxis: {
            title: {
              text: 'Número de infectados'
            },
            min: 0
          },
          legend: {
            enabled: false
          },
          series: [{
            type: "column",
            name: 'Positivos',
            data: this.categories_series,
            color: "#1c70b7"
          }]
        }

      },
      categories_data() {

        let grupos = map(groupBy(this.dataset, 'grupo_etario'), (item, value) => {
          return value
        })

        return grupos
      },
      categories_series() {

        let grupos = map(groupBy(this.dataset, 'grupo_etario'), (item, value) => {
          
          if(map(item, this.campo))
            return (sum(map(item, this.campo)))
        })

        return grupos
      }
    }
  }

</script>