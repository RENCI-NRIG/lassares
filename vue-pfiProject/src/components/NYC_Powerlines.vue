<template xmlns:>
  <div id="app" :class="[$options.name]">
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
              <template slot-scope="popup">
                <section class="card">
                  <header class="card-header">
                    <p class="card-header-title">
                      Feature ID {{ feature.id }}
                    </p>
                    <a class="card-header-icon" title="Close"
                       @click="selectedFeatures = selectedFeatures.filter(f => f.id !== feature.id)">
                      <b-icon icon="close"></b-icon>
                    </a>
                  </header>
                  <div class="card-content">
                    <div class="content">
                      <div v-if="pid == feature.properties['powerline']">
                        Powerline: {{ powerline }}</br>
                        Voltage: {{ feature.properties['voltage'] }}</br>
                        Service Date: {{ feature.properties['service_date'] }}
                      </div>
                      <div v-else-if="pid == feature.properties['chemical_id']">
                        Bore ID: {{ feature.properties['bore_id'] }}</br>
                        Job ID: {{ feature.properties['job_id'] }}</br>
                        Device ID: {{ feature.properties['device_id'] }}</br>
                        Chemical ID: {{ chemical_id }}</br>
                        Concentration: {{ concentration }}</br>
                        Timestamp: {{ timestamp }}
                        status: {{ feature.properties['status'] }}</br>
                        comment: {{ feature.properties['comment'] }}</br>

                      </div>
                      </p>
                    </div>
                  </div>
                </section>
              </template>
            </vl-overlay>
          </div>
          <!--// selected popup -->
        </template>
      </vl-interaction-select>
      <!--// click interactions -->

      <!--// base layers -->
      <vl-layer-tile v-for="layer in baseLayers" :key="layer.name" :id="layer.name" :visible="layer.visible">
        <component :is="'vl-source-' + layer.name" v-bind="layer"></component>
      </vl-layer-tile>
      <!--// base layers -->

      <!--// other layers from config -->
      <component v-for="layer in layers" :is="layer.cmp" v-if="layer.visible" :key="layer.id" v-bind="layer">
        <!--// add vl-source-* -->
        <component ref="layerSource" :is="layer.source.cmp" v-bind="layer.source">
        </component>

        <!--// add style components if provided -->
        <!--// create vl-style-box or vl-style-func -->
        <component v-if="layer.style" v-for="(style, i) in layer.style" :key="i" :is="style.cmp" v-bind="style">
        </component>
        <!--// style -->
      </component>
      <!--// other layers -->

    </vl-map>
    <!--// app map -->

    <!--// menu panel, controls -->
    <div class="menu-panel">
      <b-collapse class="panel box is-paddingless" :open.sync="panelOpen">
        <div slot="trigger" class="panel-heading">
          <div class="columns">
            <div class="column is-11">
              <strong>Menu panel</strong>
            </div>
            <div class="column">
              <b-icon :icon="panelOpen ? 'chevron-up' : 'chevron-down'" size="is-small"></b-icon>
            </div>
          </div>
        </div>
        <p class="panel-tabs">
          <a @click="showMapPanelTab('layers')" :class="mapPanelTabClasses('layers')">Layers</a>
          <a @click="showMapPanelTab('state')" :class="mapPanelTabClasses('state')">State</a>
          <a @click="showMapPanelTab('legend')" :class="mapPanelTabClasses('legend')">Legend</a>
          <a @click="showMapPanelTab('filter')" :class="mapPanelTabClasses('filter')">Filter</a>
          <a @click="showMapPanelTab('search')" :class="mapPanelTabClasses('search')">Search</a>
        </p>

        <!-- <div class="panel-block" v-for="layer in layers" :key="layer.id" @click="showMapPanelLayer" 
          :class="{ 'is-active': layer.visible }" v-show="mapPanel.tab === 'layers'"> -->
        <div class="panel-block" v-for="layer in layers"  :key="layer.id" @click="showMapPanelLayer(layer)"
          :class="{ 'is-active': layer.visible }" v-show="mapPanel.tab === 'layers'">
          <b-switch :key="layer.id" v-model="layer.visible">
            {{ layer.title }}
          </b-switch>
        </div>

        <div class="panel-block" v-show="mapPanel.tab === 'state'">
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
        </div>

        <div class="panel-block" v-show="mapPanel.tab === 'legend'">
          <table class="table is-fullwidth">
            <tr>
              <b-collapse :open="true">
                <div slot="trigger">
                   <th>NYC Powerlines</th>
                </div>
                <div class="content">
                  <table class="table is-fullwidth">
                    <tr>
                      <td><hr style=getNYC_PowerlinesStyle() /></td>
                      <td>Powerlines</td>
                    </tr>
                    <tr>
                      <td><b>Source</b></td>
                      <td>This data was derived from nothing.
                      </td>
                    </tr>
                  </table>
                </div>
              </b-collapse>
            </tr>
            <tr>
              <b-collapse :open="true">
                <div slot="trigger">
                   <th>PFC 1 Bubbles</th>
                </div>
                <div class="content">
                  <table class="table is-fullwidth">
                    <tr>
                      <td><span class="dot"></span></td>
                      <td>Test Measurments</td>
                    </tr>
                    <tr>
                      <td><b>Source</b></td>
                      <td>This data was derived from nothing.
                      </td>
                    </tr>
                  </table>
                </div>
              </b-collapse>
            </tr>
          </table>
        </div>

        <div class="panel-block" v-show="mapPanel.tab === 'filter'">
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
                <b-button @click="filterMeasurements">Filter Measurements</b-button>
              </td>
            </tr>
          </table>
        </div>

        <div class="panel-block" v-show="mapPanel.tab === 'search'">
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
                <b-button @click="searchMeasurements">Search Measurements</b-button>
              </td>
            </tr>
          </table>
        </div>
      </b-collapse>
    </div>
    <!--// menu panel, controls -->

    <!--// bar panel, controls -->
    <div class="bar-panel">
      <b-collapse class="panel box is-paddingless" :open.sync="barpanelOpen">
        <div slot="trigger" class="panel-heading">
          <div class="columns">
            <div class="column is-11">
              <strong>bar chart panel</strong>
            </div>
            <div class="column">
              <b-icon :icon="barpanelOpen ? 'chevron-up' : 'chevron-down'" size="is-small"></b-icon>
            </div>
          </div>
        </div>

        <div class="panel-block">
          <table class="table is-fullwidth">
            <div v-if="pid == chemical_id">
              <div v-if="Object.keys(selectedFeaturesBarBox).length > 0">
                <tr>
                  <th>{{ pid }} Concentration</th>
                </tr>
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
        </div>
      </b-collapse>
    </div>
    <!--// bar panel, controls -->

    <!--// base layers switch -->
    <div class="base-layers-panel">
      <div class="buttons has-addons">
        <button class="button is-light" v-for="layer in baseLayers"
                :key="layer.name" :class="{ 'is-info': layer.visible }"
                @click="showBaseLayer(layer.name)">
          {{ layer.title }}
        </button>
        <button class="button is-light" @click="mapVisible = !mapVisible">
          {{ mapVisible ? 'Hide map' : 'Show map' }}
        </button>
      </div>
    </div>
    <!--// base layers -->
  </div>
</template>

<script>
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
  import d3Barchart from '@/mixins/vue-d3-barchart'
  import { Treeselect, LOAD_ROOT_OPTIONS } from '@riophae/vue-treeselect'
  import '@riophae/vue-treeselect/dist/vue-treeselect.css'
  import axios from 'axios'
  
  // import mbtoken from '@/assets/mbtoken.json'
  // const mbtoken = require('@/assets/mbtoken.json')
  let gettoken = function () {
    return 'sk.eyJ1IjoiY29kZWZvcmFtZXJpY2EiLCJhIjoiY2ptd3F1d2Q4MDJ4djNxcjJ6NDltNzhnayJ9.4wsfBXJpT4y9L4tahnag9g'
  }
  // color values for measurement concentrations
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

  // Async reload treeselections
  /* const simulateAsyncOperation = fn => {
    setTimeout(fn, 2000)
  } */
  // sleepy time for treeselections
  const sleep = d => new Promise(resolve => setTimeout(resolve, d))

  // unique for job ids
  const unique = (value, index, self) => {
    return self.indexOf(value) === index
  }

  export default {
    name: 'nycPowerlines',
    components: {
      d3Barchart,
      Treeselect,
    },
    data () {
      return {
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
        selectedFeaturesBarClick: [],
        selectedFeaturesBarBox: [],
        isBox: undefined,
        deviceCoordinate: undefined,
        mapPanel: {
          tab: 'layers',
        },
        panelOpen: true,
        barpanelOpen: true,
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
            stroke: true,
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
            w: 200,
            h: 150,
          },
        },
        baseLayers: [
          {
            name: 'osm',
            title: 'OpenStreetMap',
            visible: true,
          },
          {
            name: 'mapbox',
            title: 'Mapbox Satellite',
            // mapId: 'mapbox.mapbox-streets-v7',
            mapId: 'mapbox.satellite',
            accessToken: gettoken(),
            visible: false,
          },
        ],
        // layers config
        layers: [
          {
            id: 'nyc_powerlines',
            title: 'NYC Powerlines',
            cmp: 'vl-layer-vector',
            visible: true,
            source: {
              cmp: 'vl-source-vector',
              url: 'https://127.0.0.1:443/drf/api/fdr_18001_0_11/?format=json',
            },
            style: [
              {
                cmp: 'vl-style-func',
                factory: this.getNYC_PowerlinesStyle,
              },
            ],
          },
          {
            id: 'measurements',
            title: 'Test Measurements',
            cmp: 'vl-layer-vector',
            visible: true,
            source: {
              cmp: 'vl-source-vector',
              url: this.MeasurementsURL('2019-05-12T00:00:00', '2019-12-20T17:43:30'),
            },
            style: [
              {
                cmp: 'vl-style-func',
                factory: this.MeasurementsStyle,
              },
            ],
          },
        ],
      }
    },
    created: function () {
      let that = this
      let turl = 'https://127.0.0.1:443/drf/api/timestamp/?format=json'
      axios.get(turl)
        .then(function (response) {
          that.searchtoptions = response.data
        })
        .catch(function (error) {
          console.log(error)
        })

      let jurl = 'https://127.0.0.1:443/drf/api/jobid/?format=json'
      axios.get(jurl)
        .then(function (response) {
          that.searchjoptions = response.data
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    methods: {
      camelCase,
      pointOnSurface: findPointOnSurface,
      getNYC_PowerlinesStyle () {
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
                lineJoin: 'bevel',
              }),
            }),
          ]
        }
      },
      MeasurementsStyle () {
        return feature => {
          return [
            new Style({
              image: new Circle({
                radius: (this.zoom / 2.6) + (feature.get('concentration') / 2),
                fill: new Fill({ color: concentration2color(feature.get('concentration') * 4.54) }), // 'rgba(245, 111, 66, 0.7)'
                stroke: new Stroke({
                  color: 'rgb(145, 7, 4, 1)',
                  width: 1,
                }),
              }),
            }),
          ]
        }
      },
      onMapMounted (map) {
        // now ol.Map instance is ready and we can work with it directly
        this.$refs.map.$map.getControls().extend([
          new ScaleLine(),
          new FullScreen(),
          new OverviewMap({
            collapsed: false,
            collapsible: true,
          }),
          new ZoomSlider(),
        ])

        // a DragBox interaction used to select features by drawing boxes
        const dragBox = new DragBox({
          condition: platformModifierKeyOnly,
        })

        map.$map.addInteraction(dragBox)

        dragBox.on('boxend', () => {
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

          this.selectedFeaturesBarClick = []
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
      showBaseLayer (name) {
        let layer = this.baseLayers.find(layer => layer.visible)
        if (layer != null) {
          layer.visible = false
        }

        layer = this.baseLayers.find(layer => layer.name === name)
        if (layer != null) {
          layer.visible = true
        }
      },
      // map panel
      mapPanelTabClasses (tab) {
        return {
          'is-active': this.mapPanel.tab === tab,
        }
      },
      showMapPanelLayer (layer) {
        layer.visible = !layer.visible
      },
      showMapPanelTab (tab) {
        this.mapPanel.tab = tab
      },
      onMapClick (event) {
        let pixel = event.pixel
        let features = this.$refs.map.$map.getFeaturesAtPixel(pixel)

        if (!features) {
          this.selectedFeaturesBarClick = []
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
            this.selectedFeaturesBarClick.push({ x: this.timestamp, y: this.concentration })
            this.selectedFeaturesBarBox = []
            this.isBox = 'no'
          } else if (properties['powerline']) {
            this.pid = properties['powerline']
            this.powerline = this.pid
            this.concentration = undefined
            this.timestamp = undefined
            this.selectedFeaturesBarClick = []
            this.selectedFeaturesBarBox = []
            this.isBox = 'no'
          }
        }
      },
      getFilterFields () {
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
      MeasurementsURL (starttimestampx, endtimestampx, jobidsx) {
        if (!jobidsx) {
          return 'https://127.0.0.1:443/drf/api/meas/?format=json&timestamp__gte=' + starttimestampx + '&timestamp__lte=' + endtimestampx
        } else if (jobidsx) {
          if (starttimestampx) {
            return 'https://127.0.0.1:443/drf/api/meas/?format=json&timestamp__gte=' + starttimestampx + '&timestamp__lte=' + endtimestampx + '&job_id=' + jobidsx
          } else if (!starttimestampx) {
            return 'https://127.0.0.1:443/drf/api/meas/?format=json&job_id=' + jobidsx
          }
        }
      },
      searchMeasurements () {
        // console.log(mbtoken)
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
      filterMeasurements () {
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
      },
    },
  }
</script>

<style lang="sass">
  @import ~bulma/sass/utilities/_all

  html, body, #app
    width: 100%
    height: 100%
    margin: 0
    padding: 0

  .nycPowerlines
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

    .menu-panel
      padding: 0

      .panel-heading
        box-shadow: 0 .25em .5em transparentize($dark, 0.8)

      .panel-content
        background: $white
        box-shadow: 0 .25em .5em transparentize($dark, 0.8)

      .panel-block
        &.draw-panel
          .buttons
            .button
              display: block
              flex: 1 1 100%

      +tablet()
        position: absolute
        top: 0
        right: 0
        max-height: 50px
        width: 22em

    .bar-panel
      padding: 0

      .panel-heading
        box-shadow: 0 .25em .5em transparentize($dark, 0.8)

      .panel-content
        background: $white
        box-shadow: 0 .25em .5em transparentize($dark, 0.8)

      .panel-block
        &.draw-panel
          .buttons
            .button
              display: block
              flex: 1 1 100%

      +tablet()
        position: absolute
        top: 0
        left: 0
        max-height: 50px
        width: 38em

    .base-layers-panel
      position: absolute
      left: 50%
      bottom: 20px
      transform: translateX(-50%)

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
