<template>
  <div class="container">  
    <div class="row mb-5 text-center">
      <div class="col-12">
        <div class="logo"><img src="./images/logo.png" /></div>
        <h1>Corona-Zona</h1>
        <p>Situacion del Covid-19 en mi distrito y barrio</p>
      </div>
    </div>
    <div class="row mb-5 justify-content-center">
      <div class="col-12 col-md-4">
        <form class="row">
          <div class="col-6">
            <div class="form-group">
              <label for="exampleFormControlSelect1">Departamento</label>
              <select class="form-control" id="departamentoList" @change="seleccionarMapa">
                <option v-for="region in regiones" :value="region">{{ region }}</option>
              </select>
            </div>
          </div>
          
          <div class="col-6">
            <div class="form-group">
              <label for="edadReader">Edad</label>
              <input type="number" class="form-control" id="edadReader">
            </div>
          </div>
        </form>
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
  import groupBy from 'lodash/groupBy'
  import sum from 'lodash/sum'


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
    methods: {
      seleccionarMapa(e) {
        this.departamento = e.target.value
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