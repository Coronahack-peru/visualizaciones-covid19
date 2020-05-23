<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        Componente
      </div>
    </div>    
    <div class="row">
      <div class="col-12">
        <formulario />
      </div>
    </div>    
  </div>
</template>

<script>
  import BootstrapVue from 'bootstrap-vue'
  import "vue-select/dist/vue-select.css"
  import Vue from 'vue'
  import Vuex from 'vuex'

  //impotar componentes

  import Formulario from './components/formulario'


  Vue.use(BootstrapVue)
  Vue.use(Vuex)


  export default {
    name: "App",
    components: {
      Formulario
    },
    computed: {
      dataset () {
        return require('./data/dataset.json')
      },
    }
  }
</script>

<style lang="scss">
  @import '../node_modules/bootstrap/scss/bootstrap';
  @import '../node_modules/bootstrap-vue/src/index.scss';
</style>