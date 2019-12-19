import Vue from 'vue'
import VueRouter from 'vue-router'

import AuthService from '../auth/AuthService'

import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css'

import VueGeolocation from 'vue-browser-geolocation'

import routes from './routes'

Vue.use(VueRouter)

Vue.use(VueLayers, {
  // global data projection, see https://vuelayers.github.io/#/quickstart?id=global-data-projection
  // dataProjection: 'EPSG:4326',
})

Vue.use(VueGeolocation)

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  // console.log('routing ', from, AuthService.authenticated())
  if (to.meta.requiresAuth) {
    if (!AuthService.authenticated()) {
      next('/')
    }
  }
  next()
})

export default router
