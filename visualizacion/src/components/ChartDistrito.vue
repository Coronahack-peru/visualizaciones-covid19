<template>
  <div class="row justify-content-center">

    <div class="col-12">
      <div class="row mb-3 text-center justify-content-center">

        <div class="col">
          <b-form-group label="Categorias">
            <b-form-checkbox-group
              id="radio-group-1"
              v-model="campoActivo"
              :options="campos"
              value-field="name"
              text-field="label"
              name="radio-options"
            ></b-form-checkbox-group>
          </b-form-group>
        </div>

      </div>
    </div>

    <div class="col-12">
      <div class="chart-container">
        <highcharts :options="chartOptions"></highcharts>
      </div>
    </div>

  </div>
</template>

<script>
  import { Chart } from 'highcharts-vue'
  import sortBy from 'lodash/sortBy'
  import filter from 'lodash/filter'
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
        campoActivo: ['nPositivos', 'nFallecidos', 'infectadosPCP', 'muertesPCP', 'tasa_fatalidad'],
        campos: [
        {
          'name':'nPositivos',
          'label':'Nro. positivos',
        }, 
        {
          'name':'nFallecidos',
          'label':'Nro. Fallecidos',
        }, 
        {
          'name':'infectadosPCP',
          'label':'Nro. infectados PCP',
        }, 
        {
          'name':'muertesPCP',
          'label':'Nro. muertes PCP',
        }, 
        {
          'name':'tasa_fatalidad',
          'label':'Tasa fatalidad',
        }, 
      ],
      grupo_etario: [
        {
          "grupo": "1",
          "name": "0 - 19 años",
          "color": "#fbb4ae"
        },
        {
          "grupo": "2",
          "name": "20 - 44 años",
          "color": "#b3cde3"
        },
        {
          "grupo": "3",
          "name": "45 - 64 años",
          "color": "#ccebc5"
        },
        {
          "grupo": "4",
          "name": "65 - 69 años",
          "color": "#decbe4"
        },
        {
          "grupo": "5",
          "name": "más de 70 años",
          "color": "#fed9a6"
        },
      ]
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
          xAxis: {        
            categories: this.campoActivo
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
          series: this.categories_series
        }

      },
      categories_series() {

        let data = map(groupBy(this.dataset, 'grupo_etario'), (item, value) => {
          
          const data_values = map(this.campoActivo, campo => sum(map(item, campo)) )
          
          const grupo = filter(this.grupo_etario,['name', value])

          return {
            type: "column",
            name: value,
            data: data_values,
            color: grupo.color
          }
        })

        

        return data
      }
    }
  }

</script>

<style lang="scss">
  .chart-container {
    max-width: 720px;
    margin: 0 auto;
  }
</style>