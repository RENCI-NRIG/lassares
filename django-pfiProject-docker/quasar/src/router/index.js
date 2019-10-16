import Vue from 'vue'
import VueRouter from 'vue-router'

import AuthService from '../auth/AuthService'

import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css'

import routes from './routes'

Vue.use(VueRouter)

Vue.use(VueLayers, {
  // global data projection, see https://vuelayers.github.io/#/quickstart?id=global-data-projection
  // dataProjection: 'EPSG:4326',
})

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation
 */

// export default function (/* { store, ssrContext } */) {
//  const Router = new VueRouter({
//    scrollBehavior: () => ({ x: 0, y: 0 }),
//    routes,

//     Leave these as is and change from quasar.conf.js instead!
//     quasar.conf.js -> build -> vueRouterMode
//     quasar.conf.js -> build -> publicPath
//    mode: process.env.VUE_ROUTER_MODE,
//    base: process.env.VUE_ROUTER_BASE
//  })

//  return Router
// }

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

export function authGuard (to, from, next) {
  if (!AuthService.authenticated()) {
    next('/')
  }
  next()
}

export default router
