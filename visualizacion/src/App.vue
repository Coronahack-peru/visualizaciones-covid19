<template>
  <div class="container">  
    <div class="row mb-1 text-center pt-3 pb-3">
      <div class="col-12">
        <div class="logo"><img src="./images/logo.png" /></div>
        <h1>Corona-Zona</h1>
        <p>Situacion del Covid-19 en mi distrito y barrio</p>
      </div>
    </div>
    <div class="row mb-5 justify-content-center">
      <div class="col-12 col-md-4 text-center">
        <div class="form-group">
            <p><strong>Conoce los los casos de covid-19 positivos y fallecidos por grupo etario en: </strong></p>
            <b-form-select v-model="departamento" :options="regiones" size="sm" class="mt-3"></b-form-select>
        </div>
      </div>
    </div>
    <div class="row mb-5 justify-content-center">
      <div class="col-12">
        <chart-distrito :departamento="departamento" :dataset="grupos_edades"></chart-distrito>
      </div>
    </div>   
    <!-- <div class="row mb-5 justify-content-center">
      <div class="col-9">
        <mapa-contagio :departamento="departamento"></mapa-contagio>
      </div>
    </div>     -->
     
  </div>
</template>

<script>
  import BootstrapVue from 'bootstrap-vue'
  import "vue-select/dist/vue-select.css"
  import Vue from 'vue'
  import Vuex from 'vuex'

  //impotar componentes

  //import Formulario from './components/formulario'
  //import MapaContagio from './components/MapaContagio'
  import ChartDistrito from './components/ChartDistrito'
  import map from 'lodash/map'
  import uniq from 'lodash/uniq'
  import orderBy from 'lodash/orderBy'
  import filter from 'lodash/filter'

  Vue.use(BootstrapVue)
  Vue.use(Vuex)


  export default {
    name: "App",
    components: {
      //MapaContagio,
      ChartDistrito
    },
    data() {
      return {
        departamento: "AMAZONAS"
      }
    },
    computed: {
      dataset () {
        return require('./data/dataset.json')
      },
      regiones () {
        return orderBy(uniq(map(this.dataset, 'departamento')))
      },
      grupos_edades () {

        let departamento_data = filter(this.dataset, item => item.departamento == this.departamento)

        return departamento_data
      }
    }
  }
</script>

<style lang="scss">
  @import '../node_modules/bootstrap/scss/bootstrap';
  @import '../node_modules/bootstrap-vue/src/index.scss';

  .logo {
    max-width: 128px;
    margin: 0 auto;

    img {
      width: 100%;
    }
  }
</style>