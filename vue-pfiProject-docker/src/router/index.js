import Vue from 'vue'
import Router from 'vue-router'
import nycPowerlines from '@/components/NYC_Powerlines'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'NYC_Powerlines',
      component: nycPowerlines,
    },
  ],
})
