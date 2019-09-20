<template>
  <q-layout view="hhh lpr fff">
    <q-header elevated class="bg-teal text-black">
      <q-toolbar>
        <div v-if="signIn==='no'">
          <q-icon name="fas fa-sign-in-alt" />
        </div>
        <div v-if="signIn==='yes'">
          <q-btn
            flat
            dense
            round
            @click="leftDrawerOpen = !leftDrawerOpen"
            aria-label="SignIn"
          >
            <q-icon name="fas fa-sign-out-alt" />
          </q-btn>
        </div>

        <q-toolbar-title>
          Lassares Measurements App
        </q-toolbar-title>

        <q-btn-dropdown flat style="bg-color:teal" icon="layers" class="text-black" label="Menu Panel">
          <div class="q-pa-md">
            <div class="q-gutter-y-md" style="max-width: 450px">
              <q-tabs
                v-model="tab"
                dense
                class="text-black"
                active-color="teal"
                indicator-color="teal"
                align="justify"
                narrow-indicator
              >
                <q-tab name="layers" label="Layers" />
                <q-tab name="state" label="State" />
                <q-tab name="legend" label="Legend" />
                <q-tab name="filter" label="Filter" />
                <q-tab name="search" label="Search" />
              </q-tabs>

              <q-separator />

              <q-tab-panels v-model="tab" animated>
                <q-tab-panel name="layers">
                  <div class="text-h6">Layers</div>
                  <div class="q-pa-md q-gutter-y-sm column">
                    <q-toggle
                      :label="`Measurements Layer ${ measurementsModel }`"
                      :key="layers[1].id"
                      v-on:input="showMapPanelLayer(layers)"
                      :class="{ 'is-active': layers[1].visible }"
                      color="black"
                      false-value="Not Selected"
                      true-value="Selected"
                      v-model="measurementsModel"
                    />
                    <q-toggle
                      :label="`Powerlines Layer ${ powerlinesModel }`"
                      :key="layers[0].id"
                      v-on:input="showMapPanelLayer(layers)"
                      :class="{ 'is-active': layers[0].visible }"
                      color="black"
                      false-value="Not Selected"
                      true-value="Selected"
                      v-model="powerlinesModel"
                    />
                  </div>
                </q-tab-panel>

                <q-tab-panel name="state">
                  <div class="text-h6">State</div>
                    <table class="table is-fullwidth">
                      <tr>
                        <th>Map center</th>
                        <td>{{ center }}</td>
                      </tr>
                      <tr>
                        <th>Map zoom</th>
                        <td>{{ zoom }}</td>
                      </tr>
                      <tr>
                        <th>Map rotation</th>
                        <td>{{ rotation }}</td>
                      </tr>
                      <tr>
                        <th>Device coordinate</th>
                        <td>{{ deviceCoordinate }}</td>
                      </tr>
                      <tr>
                        <th>Selected features</th>
                        <td>{{ pid }}</td>
                      </tr>
                    </table>
                </q-tab-panel>

                <q-tab-panel name="legend">
                  <div class="text-h6">Legend</div>
                  <table class="table is-fullwidth">
                    <tr>
                      <q-expansion-item
                        group="powerlines"
                        label="Powerlines"
                        default-opened
                        header-class="text-black"
                        class="text-black"
                      >
                        <div slot="trigger">
                          <th>NYC Powerlines</th>
                        </div>
                        <q-card>
                          <q-card-section>
                            <table class="table is-fullwidth">
                              <tr>
                                <td><hr style=getNYC_PowerlinesStyle() /></td>
                                <td>Powerlines</td>
                              </tr>
                              <tr>
                                <td><b>Source</b></td>
                                <td>This data was derived from nothing.</td>
                              </tr>
                            </table>
                          </q-card-section>
                        </q-card>
                      </q-expansion-item>
                    </tr>
                    <tr>
                      <q-expansion-item
                        group="measurements"
                        label="Measurements"
                        default-opened
                        header-class="text-black"
                      >
                        <div slot="trigger">
                          <th>PFC 1 Bubbles</th>
                        </div>
                        <q-card>
                          <q-card-section>
                            <table class="table is-fullwidth">
                              <tr>
                                <td><span class="dot"></span></td>
                                <td>Test Measurments</td>
                              </tr>
                              <tr>
                                <td><b>Source</b></td>
                                <td>This data was derived from nothing.</td>
                              </tr>
                            </table>
                          </q-card-section>
                        </q-card>
                      </q-expansion-item>
                    </tr>
                  </table>
                </q-tab-panel>

                <q-tab-panel name="filter">
                  <div class="text-h6">Filter</div>
                  <table class="table is-fullwidth">
                    <tr>
                      <th>Select Start Timestamp</th>
                    </tr>
                    <tr>
                      <td>
                        <treeselect :load-options="loadFilterOptions" :options="toptions" v-model="starttimestamp"
                                    :auto-load-root-options="false" :multiple="false" placeholder="Open the menu..." />
                      </td>
                    </tr>
                    <tr>
                      <th>Select End Timestamp</th>
                    </tr>
                    <tr>
                      <td>
                        <treeselect :load-options="loadFilterOptions" :options="toptions" v-model="endtimestamp"
                                    :auto-load-root-options="false" :multiple="false" placeholder="Open the menu..." />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <q-btn color="teal" class="text-black" @click="filterMeasurements">Filter Measurements</q-btn>
                      </td>
                    </tr>
                  </table>
                </q-tab-panel>
                <q-tab-panel name="search">
                  <div class="text-h6">Search</div>
                  <table class="table is-fullwidth">
                    <tr>
                      <th>Select Start Timestamp</th>
                    </tr>
                    <tr>
                      <td>
                        <treeselect :options="searchtoptions" v-model="starttimestampx"
                                    :auto-load-root-options="false" :multiple="false" placeholder="Open the menu..." />
                      </td>
                    </tr>
                    <tr>
                      <th>Select End Timestamp</th>
                    </tr>
                    <tr>
                      <td>
                        <treeselect :options="searchtoptions" v-model="endtimestampx"
                                    :auto-load-root-options="false" :multiple="false" placeholder="Open the menu..." />
                      </td>
                    </tr>
                    <tr>
                      <th>Select Job ID</th>
                    </tr>
                    <tr>
                      <td>
                        <treeselect :options="searchjoptions" v-model="jobidsx"
                                    :auto-load-root-options="false" :multiple="false" placeholder="Open the menu..." />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <q-btn color="teal" class="text-black" @click="searchMeasurements">Search Measurements</q-btn>
                      </td>
                    </tr>
                  </table>
                </q-tab-panel>
              </q-tab-panels>
            </div>
          </div>
        </q-btn-dropdown>
      </q-toolbar>

    </q-header>

    <div v-if="signIn==='no'">

    </div>
    <div v-if="signIn==='yes'">
      <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        bordered
        content-class="teal"
      >
        <q-list>
          <q-item-label header>Measurements Data Entry</q-item-label>
          <q-item clickable tag="a" target="_blank" href="https://renci.org">
            <q-item-section avatar>
              <q-icon name="school" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Test</q-item-label>
              <q-item-label caption>test</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-drawer>
    </div>

    <!-- q-page-container :style="pageStyle" -->
    <q-page-container>
      <q-page>
        <q-page-sticky expand position="top">
          <!--// app map -->
          <vl-map v-if="mapVisible" class="map" ref="map" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
              @click="onMapClick" data-projection="EPSG:4326" @mounted="onMapMounted">
             <!--// map view aka ol.View -->
            <vl-view ref="mapView" :center.sync="center" :zoom.sync="zoom" :rotation.sync="rotation"></vl-view>

            <!--// click interactions -->
            <vl-interaction-select ref="selectInteraction" :features.sync="selectedFeatures">
              <template slot-scope="select">
                <!--// select styles -->
                <vl-style-box>
                  <vl-style-stroke color="#33201e" :width="7"></vl-style-stroke>
                  <vl-style-fill :color="[254, 178, 76, 0.7]"></vl-style-fill>
                  <vl-style-circle :radius="5">
                    <vl-style-stroke color="#9e493e" :width="7"></vl-style-stroke>
                    <vl-style-fill :color="[254, 178, 76, 0.7]"></vl-style-fill>
                  </vl-style-circle>
                </vl-style-box>
                <vl-style-box :z-index="1">
                  <vl-style-stroke color="#d43f45" :width="2"></vl-style-stroke>
                  <vl-style-circle :radius="5">
                    <vl-style-stroke color="#d43f45" :width="2"></vl-style-stroke>
                  </vl-style-circle>
                </vl-style-box>
                <!--// select styles -->

                <!--// selected feature popup -->
                <div v-if="isBox === 'no'">
                  <vl-overlay class="feature-popup" v-for="feature in select.features" :key="feature.id" :id="feature.id"
                              :position="pointOnSurface(feature.geometry)" :auto-pan="true" :auto-pan-animation="{ duration: 300 }">
                    <q-card class="feature-popup">
                      <q-card-section>
                        <q-banner inline-actions class="text-black bg-white">
                          <div class="text-h6">
                            Feature ID {{ feature.id }}
                          </div>
                          <template v-slot:action>
                            <q-btn flat round dense icon="close" @click="selectedFeatures = selectedFeatures.filter(f => f.id !== feature.id)" />
                          </template>
                      </q-banner>
                        <div v-if="pid == feature.properties['powerline']">
                          Powerline: {{ powerline }}<br>
                          Voltage: {{ feature.properties['voltage'] }}<br>
                          Service Date: {{ feature.properties['service_date'] }}
                        </div>
                        <div v-else-if="pid == feature.properties['chemical_id']">
                          Bore ID: {{ feature.properties['bore_id'] }}<br>
                          Job ID: {{ feature.properties['job_id'] }}<br>
                          Device ID: {{ feature.properties['device_id'] }}<br>
                          Chemical ID: {{ chemical_id }}<br>
                          Concentration: {{ concentration }}<br>
                          Timestamp: {{ timestamp }}
                          status: {{ feature.properties['status'] }}<br>
                          comment: {{ feature.properties['comment'] }}<br>
                        </div>
                      </q-card-section>
                    </q-card>
                  </vl-overlay>
                </div>
                <!--// selected feature popup -->

                <!--// selected feature bar plot -->
                <div v-if="isBox === 'yes'">
                  <vl-overlay class="barchart-popup" v-for="feature in select.features" :key="feature.id" :id="feature.id"
                          :position="pointOnSurface(barplotpoint)" :auto-pan="true" :auto-pan-animation="{ duration: 300 }">
                    <q-card class="barchart-popup">
                        <q-card-section>
                          <q-banner inline-actions class="text-black bg-white">
                            <b>
                              {{ pid }} concentration
                            </b>
                            <template v-slot:action>
                              <q-btn flat round dense icon="close" @click="selectedFeatures = selectedFeatures.filter(f => f.id === 0)" />
                            </template>
                          </q-banner>
                          <table class="table is-fullwidth">
                            <div v-if="pid == chemical_id">
                              <div v-if="Object.keys(selectedFeaturesBarBox).length > 0">
                                <tr>
                                  <td>x = Timestamp, y = Concentration</td>
                                </tr>
                                <tr>
                                  <td>
                                    <d3-barchart class="chart" :pdata='selectedFeaturesBarBox' :options='baroptions' />
                                  </td>
                                </tr>
                              </div>
                            </div>
                          </table>
                        </q-card-section>
                    </q-card>
                  </vl-overlay>
                </div>
                <!--// selected features bar plot -->
              </template>
            </vl-interaction-select>
            <!--// click interactions -->

            <!--// base layers -->
            <vl-layer-tile v-for="layer in baseLayers" :key="layer.name" :id="layer.name" :visible="layer.visible">
              <component :is="'vl-source-' + layer.name" v-bind="layer"></component>
            </vl-layer-tile>
            <!--// base layers -->

            <!--// other layers from config -->
            <!-- eslint-disable vue/no-use-v-if-with-v-for,vue/no-confusing-v-for-v-if -->
            <component v-for="layer in layers" :is="layer.cmp" v-if="layer.visible" :key="layer.id" v-bind="layer">
              <!--// add vl-source-* -->
              <component ref="layerSource" :is="layer.source.cmp" v-bind="layer.source">
              </component>

              <!--// add style components if provided -->
              <!--// create vl-style-box or vl-style-func -->
              <component v-if="layer.style" v-for="(style, i) in layer.style" :key="i" :is="style.cmp" v-bind="style">
              </component>
            </component>
            <!-- eslint-enable vue/no-use-v-if-with-v-for,vue/no-confusing-v-for-v-if -->
            <!--// other layers -->
          </vl-map>
          <!--// app map -->
        </q-page-sticky>
        <q-page-sticky position="bottom-right" :offset="[18, 18]">
          <q-fab icon="keyboard_arrow_up" direction="up" color="teal text-black">
            <q-fab-action color="teal" @click="onClick" icon="fas fa-object-group" class="text-black" />
          </q-fab>
        </q-page-sticky>
      </q-page>
    </q-page-container>

    <q-footer elevated class="bg-teal text-black">
      <div class="q-pa-sm">
          <q-toolbar>
            <q-btn flat round dense icon="layers">
              <q-menu transition-show="flip-right" transition-hide="flip-left">
                  <div class="q-pa-md" style="min-width: 200px">
                    <q-list link>
                      <!--
                        Rendering a <label> tag (notice tag="label")
                        so QRadios will respond to clicks on QItems to
                        change Toggle state.
                      -->
                      <q-item tag="label" v-ripple>
                        <q-item-section avatar>
                          <q-radio v-on:input="showBaseLayer" val="osm" v-model="baselayer" color="black" />
                        </q-item-section>
                        <q-item-section>
                          <q-item-label>OpenStreetMap</q-item-label>
                        </q-item-section>
                      </q-item>

                      <q-item tag="label" v-ripple>
                        <q-item-section avatar>
                          <q-radio v-on:input="showBaseLayer" val="mapbox" v-model="baselayer" color="black" />
                        </q-item-section>
                        <q-item-section>
                          <q-item-label>MapBock Satellite</q-item-label>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
              </q-menu>
            </q-btn>
            <q-toolbar-title>
              Base Layers
            </q-toolbar-title>
            <div>Built with <a href="https://quasar.dev/" target="_blank" style="color:black; text-decoration:none;">Quasar</a>,
            <a href="https://vuejs.org/" target="_blank" style="color:black; text-decoration:none;">Vue.js</a>,
            <a href="https://vuelayers.github.io" target="_blank" style="color:black; text-decoration:none;">Vuelayers</a>,
            <a href="https://openlayers.org/" target="_blank" style="color:black; text-decoration:none;">Openlayers</a>,
            <a href="https://d3js.org/" target="_blank" style="color:black; text-decoration:none;">D3.js</a>,
            <a href="https://www.openstreetmap.org" target="_blank" style="color:black; text-decoration:none;">OSM</a>,
            and <a href="https://www.mapbox.com/" target="_blank" style="color:black; text-decoration:none;">MapBox</a></div>
          </q-toolbar>
        </div>
    </q-footer>

  </q-layout>
</template>

<script>
import { openURL } from 'quasar'
import { camelCase } from 'lodash'
import { findPointOnSurface, writeGeoJsonFeature } from 'vuelayers/lib/ol-ext'
import ScaleLine from 'ol/control/ScaleLine'
import FullScreen from 'ol/control/FullScreen'
import OverviewMap from 'ol/control/OverviewMap'
import ZoomSlider from 'ol/control/ZoomSlider'
import { Style, Stroke, Fill, Circle } from 'ol/style'
import { DEVICE_PIXEL_RATIO } from 'ol/has.js'
import DragBox from 'ol/interaction/DragBox'
import { platformModifierKeyOnly } from 'ol/events/condition.js'
import d3Barchart from '../mixins/vue-d3-barchart'
import { toLonLat } from 'ol/proj.js'
import { Treeselect, LOAD_ROOT_OPTIONS } from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import axios from 'axios'

import pubhost from '../assets/pubhost.json'
import mbtoken from '../assets/mbtoken.json'
let gettoken = function () {
  return mbtoken[0].MB_KEY
}
// color values for measurements concentrations
let concentration2color = function (concentration) {
  let r = 0
  let g = 0
  let b = 0
  if (concentration < 50) {
    g = 255
    b = Math.round(5.1 * concentration)
  } else {
    b = 255
    g = Math.round(510 - 5.10 * concentration)
  }
  let h = r * 0x1 + g * 0x100 + b * 0x10000
  return '#' + ('000000' + h.toString(16)).slice(-6)
}

// sleepy time for treeselections
const sleep = d => new Promise(resolve => setTimeout(resolve, d))

// unique for job ids
const unique = (value, index, self) => {
  return self.indexOf(value) === index
}

export default {
  name: 'Lassares',
  components: {
    d3Barchart,
    Treeselect
  },
  data () {
    return {
      signIn: 'no',
      dialog: false,
      leftDrawerOpen: false,
      tab: 'layers',
      baselayer: 'osm',
      barplotpoint: undefined,
      powerlinesModel: 'Selected',
      measurementsModel: 'Selected',
      center: [-73.851271, 40.725070],
      zoom: 15,
      rotation: 0,
      searchtoptions: [],
      searchjoptions: [],
      starttimestamp: undefined,
      endtimestamp: undefined,
      starttimestampx: undefined,
      endtimestampx: undefined,
      toptions: null,
      jobids: undefined,
      jobidsx: undefined,
      joptions: null,
      pid: undefined,
      chemical_id: undefined,
      powerline: undefined,
      concentration: undefined,
      timestamp: undefined,
      storeFeatures: [],
      selectedFeatures: [],
      selectedFeaturesBarBox: [],
      isBox: undefined,
      deviceCoordinate: undefined,
      boxCoordinate: undefined,
      mapVisible: true,
      baroptions: {
        colors: ['red', 'lightgreen'],
        rules: true,
        axis: true,
        labels: true,
        padding: 0.1,
        line: true,
        points: false,
        value: false,
        gradient: {
          stroke: true
        },
        curve: {
        },
        getX: (d) => {
          return d.x
        },
        getY: (d) => {
          return d.y
        },
        autoSize: {
          w: 300,
          h: 150
        }
      },
      baseLayers: [
        {
          name: 'osm',
          title: 'OpenStreetMap',
          visible: true
        },
        {
          name: 'mapbox',
          title: 'Mapbox Satellite',
          // mapId: 'mapbox.mapbox-streets-v7',
          mapId: 'mapbox.satellite',
          accessToken: gettoken(),
          visible: false
        }
      ],
      // layers config
      layers: [
        {
          id: 'powerlines',
          title: 'Powerlines',
          cmp: 'vl-layer-vector',
          visible: true,
          source: {
            cmp: 'vl-source-vector',
            url: 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/fdr_18001_0_11/?format=json'
          },
          style: [
            {
              cmp: 'vl-style-func',
              factory: this.getPowerlinesStyle
            }
          ]
        },
        {
          id: 'measurements',
          title: 'Measurements',
          cmp: 'vl-layer-vector',
          visible: true,
          source: {
            cmp: 'vl-source-vector',
            url: this.MeasurementsURL('2019-05-12T00:00:00', '2019-12-20T17:43:30')
          },
          style: [
            {
              cmp: 'vl-style-func',
              factory: this.MeasurementsStyle
            }
          ]
        }
      ]
    }
  },
  created: function () {
    let that = this
    let turl = 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/timestamp/?format=json'
    axios.get(turl)
      .then(function (response) {
        that.searchtoptions = response.data
      })
      .catch(function (error) {
        console.log(error)
      })

    let jurl = 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/jobid/?format=json'
    axios.get(jurl)
      .then(function (response) {
        that.searchjoptions = response.data
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  watch: {
    selectedFeatures: function (features) {
      let i
      let geometries = []
      for (i = 0; i < features.length; i++) {
        let coordinates = toLonLat([features[i].geometry.coordinates[0], features[i].geometry.coordinates[1]])
        let geometry = {
          'type': 'Point',
          'coordinates': [coordinates[0], coordinates[1]]
        }
        geometries.push(geometry)
      }
      if (geometries.length > 0) {
        this.barplotpoint = geometries[0]
      }
    }
  },
  methods: {
    openURL,
    camelCase,
    pointOnSurface: findPointOnSurface,
    onClick: function () {
      alert('I clicked it!')
    },
    getPowerlinesStyle: function () {
      let canvas = document.createElement('canvas')
      let context = canvas.getContext('2d')
      let pixelRatio = DEVICE_PIXEL_RATIO

      let pattern = (function () {
        canvas.width = 8 * pixelRatio
        canvas.height = 8 * pixelRatio
        // white background
        context.fillStyle = 'rgb(22, 183, 242)'
        context.fillRect(0, 0, canvas.width, canvas.height)
        // outer circle
        context.fillStyle = 'rgb(46, 9, 46, 0.5)'
        context.beginPath()
        context.arc(4 * pixelRatio, 4 * pixelRatio, 3 * pixelRatio, 0, 2 * Math.PI)
        context.fill()
        // inner circle
        context.fillStyle = 'rgb(26, 6, 69)'
        context.beginPath()
        context.arc(4 * pixelRatio, 4 * pixelRatio, 1.5 * pixelRatio, 0, 2 * Math.PI)
        context.fill()
        return context.createPattern(canvas, 'repeat')
      }())
      return feature => {
        return [
          new Style({
            stroke: new Stroke({
              color: pattern,
              width: (this.zoom / 3.7142),
              lineCap: 'round',
              lineJoin: 'bevel'
            })
          })
        ]
      }
    },
    MeasurementsStyle: function () {
      return feature => {
        return [
          new Style({
            image: new Circle({
              radius: (this.zoom / 2.6) + (feature.get('concentration') / 2),
              fill: new Fill({ color: concentration2color(feature.get('concentration') * 4.54) }), // 'rgba(245, 111, 66, 0.7)'
              stroke: new Stroke({
                color: 'rgb(145, 7, 4, 1)',
                width: 1
              })
            })
          })
        ]
      }
    },
    onMapMounted: function (map) {
      // now ol.Map instance is ready and we can work with it directly
      this.$refs.map.$map.getControls().extend([
        new ScaleLine(),
        new FullScreen(),
        new OverviewMap({
          collapsed: false,
          collapsible: true
        }),
        new ZoomSlider()
      ])

      // a DragBox interaction used to select features by drawing boxes
      const dragBox = new DragBox({
        condition: platformModifierKeyOnly
      })

      map.$map.addInteraction(dragBox)

      dragBox.on('boxend', (event) => {
        this.boxCoordinate = event.coordinate
        // features that intersect the box are added to the collection of
        // selected features
        const extent = dragBox.getGeometry().getExtent()
        // only use source that have chemical_id
        let source
        let i
        for (i = 0; i < this.$refs.layerSource.length; i++) {
          let features = this.$refs.layerSource[i].getFeatures()
          if (features[0].values_.chemical_id) {
            source = this.$refs.layerSource[i].$source
          }
        }

        this.isBox = 'yes'

        source.forEachFeatureIntersectingExtent(extent, feature => {
          feature = writeGeoJsonFeature(feature)
          this.selectedFeatures.push(feature)
          this.selectedFeaturesBarBox.push({ x: feature.properties['timestamp'], y: feature.properties['concentration'] })
          this.chemical_id = feature.properties['chemical_id']
          this.pid = this.chemical_id
        })
      })

      // clear selection when drawing a new box and when clicking on the map
      dragBox.on('boxstart', () => {
        this.selectedFeatures = []
        this.selectedFeaturesBarBox = []
        this.isBox = 'no'
      })
    },
    // base layers
    showBaseLayer: function () {
      let layer = this.baseLayers.find(layer => layer.visible)
      if (layer != null) {
        layer.visible = false
      }

      layer = this.baseLayers.find(layer => layer.name === this.baselayer)
      if (layer != null) {
        layer.visible = true
      }
    },
    showMapPanelLayer: function (layers) {
      console.log(layers)
      let mlayer = this.layers[1]
      if (this.measurementsModel === 'Selected') {
        mlayer.visible = true
      } else if (this.measurementsModel === 'Not Selected') {
        mlayer.visible = false
      }

      let player = this.layers[0]
      if (this.powerlinesModel === 'Selected') {
        player.visible = true
      } else if (this.powerlinesModel === 'Not Selected') {
        player.visible = false
      }
    },
    onMapClick: function (event) {
      let pixel = event.pixel
      let features = this.$refs.map.$map.getFeaturesAtPixel(pixel)

      if (!features) {
        this.selectedFeaturesBarBox = []
        this.selectedFeatures = []
        this.isBox = 'no'
      } else if (features) {
        this.deviceCoordinate = event.coordinate
        let feature = features[0]
        let properties = feature.getProperties()

        if (properties['chemical_id']) {
          this.pid = properties['chemical_id']
          this.chemical_id = this.pid
          this.concentration = properties['concentration']
          this.timestamp = properties['timestamp']
          this.selectedFeaturesBarBox = []
          this.isBox = 'no'
        } else if (properties['powerline']) {
          this.pid = properties['powerline']
          this.powerline = this.pid
          this.concentration = undefined
          this.timestamp = undefined
          this.selectedFeaturesBarBox = []
          this.isBox = 'no'
        }
      }
    },
    MeasurementsURL: function (starttimestampx, endtimestampx, jobidsx) {
      if (!jobidsx) {
        return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/meas/?format=json&timestamp__gte=' + starttimestampx + '&timestamp__lte=' + endtimestampx
      } else if (jobidsx) {
        if (starttimestampx) {
          return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/meas/?format=json&timestamp__gte=' + starttimestampx + '&timestamp__lte=' + endtimestampx + '&job_id=' + jobidsx
        } else if (!starttimestampx) {
          return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/meas/?format=json&job_id=' + jobidsx
        }
      }
    },
    getFilterFields: function () {
      let startTimestamps = []
      let startJobIds = []
      let i
      let j
      for (i = 0; i < this.$refs.layerSource.length; i++) {
        let features = this.$refs.layerSource[i].getFeatures()
        if (features[0].values_.chemical_id) {
          for (j = 0; j < features.length; j++) {
            let timestamp = features[j].values_.timestamp
            startTimestamps.push(timestamp)
            let jobid = features[j].values_.job_id
            startJobIds.push(jobid)
          }
        }
      }
      return [startTimestamps.sort(), startJobIds.filter(unique).sort()]
    },
    // You can either use callback or return a Promise.
    async loadFilterOptions ({ action }) {
      if (action === LOAD_ROOT_OPTIONS) {
        await sleep(500)
        this.toptions = this.getFilterFields()[0].map(id => ({ id, label: `${id}` }))
        this.joptions = this.getFilterFields()[1].map(id => ({ id, label: `${id}` }))
      }
    },
    searchMeasurements: function () {
      // console.log(mbtoken[0].MB_KEY)
      if (this.starttimestampx && this.endtimestampx) {
        if (this.endtimestampx < this.starttimestampx) {
          this.$notification.open('You have to pick end timestep later than the start timestamp!')
        } else {
          let i
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.chemical_id) {
              // url to get data from
              let url = this.MeasurementsURL(this.starttimestampx, this.endtimestampx, this.jobidsx)
              // the that is used to deal with this scope
              var that = this
              // eye is used for i to deal with the async effects of axios
              let eye = i
              axios.get(url)
                .then(function (response) {
                  if (response.data.features.length === 0) {
                    that.$notification.open('You cannot delete all of the data. Make another type of selection')
                  } else {
                    that.layers[eye].source.url = url
                    that.$refs.layerSource[eye].removeFeatures(features)
                    that.$refs.layerSource[eye].addFeatures(response.data.features)
                  }
                })
                .catch(function (error) {
                  console.log(error)
                })
            }
          }
          this.starttimestamp = undefined
          this.endtimestamp = undefined
          this.toptions = undefined
          this.joptions = undefined
          this.storeFeatures = []
        }
      } else if (this.starttimestampx && !this.endtimestampx) {
        this.$notification.open('You have to select a end timestep!')
      } else if (!this.starttimestampx && this.endtimestampx) {
        this.$notification.open('You have to select a start timestep!')
      } else if (!this.starttimestampx && !this.endtimestampx) {
        if (!this.jobidsx) {
          this.$notification.open('You have to select something!')
        } else if (this.jobidsx) {
          let i
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.chemical_id) {
              let url = this.MeasurementsURL(this.starttimestampx, this.endtimestampx, this.jobidsx)
              this.layers[i].source.url = url
              this.$refs.layerSource[i].removeFeatures(features)
              // the that is used to deal with this scope
              var thats = this
              // eye is used for i to deal with the async effects of axios
              let eye = i
              axios.get(url)
                .then(function (response) {
                  thats.$refs.layerSource[eye].addFeatures(response.data.features)
                })
                .catch(function (error) {
                  console.log(error)
                })
            }
          }
        }
      }
    },
    // filter data only on the client side. Dependent on data available from the DRF server
    filterMeasurements: function () {
      // check to see if there are stored features, and if there are then add them
      // to the layerSource features,so all features are available for filtering.
      let i
      if (this.storeFeatures.length > 0) {
        for (i = 0; i < this.storeFeatures.length; i++) {
          let j
          for (j = 0; j < this.$refs.layerSource.length; j++) {
            let features = this.$refs.layerSource[j].getFeatures()
            if (features[0].values_.chemical_id) {
              this.$refs.layerSource[j].addFeature(this.storeFeatures[i])
            }
          }
        }
        this.storeFeatures = []
      }
      // if there are two timestamps, and if they are in order than filter
      if (this.starttimestamp && this.endtimestamp) {
        if (this.endtimestamp < this.starttimestamp) {
          this.$notification.open('You have to pick end timestep later than the start timestamp')
        } else {
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.chemical_id) {
              let j
              for (j = 0; j < features.length; j++) {
                let id = features[j].id_
                let feature = this.$refs.layerSource[i].getFeatureById(id)
                if (feature.values_.timestamp < this.starttimestamp) {
                  this.$refs.layerSource[i].removeFeature(feature)
                  this.storeFeatures.push(feature)
                } else if (feature.values_.timestamp > this.endtimestamp) {
                  this.$refs.layerSource[i].removeFeature(feature)
                  this.storeFeatures.push(feature)
                }
              }
            }
          }
        }
      // other wise tell user they have to refine their search
      } else if (this.starttimestamp && !this.endtimestamp) {
        this.$notification.open('You have to select a end timestep')
      } else if (!this.starttimestamp && this.endtimestamp) {
        this.$notification.open('You have to select a start timestep')
      }
    }
  }
}
</script>

<style lang="sass">
  .ol-control button
    color: black
    background-color: rgb(0,128,128)

  .ol-control button:hover
  .ol-control button:focus
    text-decoration: none
    background-color: rgb(0,128,128)

  a:hover
    font-weight:bold

  .Powerlines
    position: relative

    .map
      height: 100%
      width: 100%

    .map .ol-zoom
      top: 5.5em
      left: 1.5em

    .map .ol-zoomslider
      background-color: transparent
      top: 7.3em
      left: 1.5em

    .map .ol-zoom .ol-zoom-out
      margin-top: 204px

    .map .ol-touch .ol-zoom .ol-zoom-out
      margin-top: 212px

    .map .ol-touch .ol-zoomslider
      top: 2.75em

    .map .ol-zoom-in.ol-has-tooltip:hover [role=tooltip],
    .map .ol-zoom-in.ol-has-tooltip:focus [role=tooltip]
      top: 3px

    .map .ol-zoom-out.ol-has-tooltip:hover [role=tooltip],
    .map .ol-zoom-out.ol-has-tooltip:focus [role=tooltip]
      top: 232px

  .feature-popup
    position: absolute
    left: -50px
    bottom: 12px
    width: 20em
    max-width: none

    &:after, &:before
      top: 100%
      border: solid transparent
      content: ' '
      height: 0
      width: 0
      position: absolute
      pointer-events: none
    &:after
      border-top-color: white
      border-width: 10px
      left: 48px
      margin-left: -10px
    &:before
      border-top-color: #cccccc
      border-width: 11px
      left: 48px
      margin-left: -11px

    .card-content
      max-height: 20em
      overflow: auto

    .content
       word-break: break-all

  .barchart-popup
    position: absolute
    left: -50px
    bottom: 12px
    width: auto
    min-width: 27em
    max-width: 50em

    &:after, &:before
      top: 100%
      border: solid transparent
      content: ' '
      height: 0
      width: 0
      position: absolute
      pointer-events: none
    &:after
      border-top-color: white
      border-width: 10px
      left: 48px
      margin-left: -10px
    &:before
      border-top-color: #cccccc
      border-width: 11px
      left: 48px
      margin-left: -11px

    .card-content
      max-height: 20em
      overflow: auto

    .content
       word-break: break-all

  .dot
    height: 15px;
    width: 15px;
    background-color: #f56f4270;
    border-radius: 50%;
    display: inline-block

  .chart
    display: inline-block
    width: 700px
    height: 200px
    margin-top: 0em

</style>
