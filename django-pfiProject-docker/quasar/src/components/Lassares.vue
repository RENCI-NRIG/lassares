<template>
  <q-layout view="lhr lpr lfr">
    <!--// Left Drawer, check to see if authenticated -->
    <div v-if="!authenticated">
      <!-- If not authenticated do nothing -->
    </div>
    <div v-else-if="authenticated">
      <!-- If authenticated show drawer -->
      <q-drawer v-model="leftDrawerOpen" show-if-above bordered content-class="teal">
        <!-- // measurement-list -->
        <q-card class="q-pa-md" style="max-width: 300px">
          <q-btn label="View List of Measurements" type="viewlist" color="teal" class="text-black">
            <q-popup-proxy class="measurement-popup" transition-show="flip-up" transition-hide="flip-down">
              <measurement-list></measurement-list>
            </q-popup-proxy>
          </q-btn>
        </q-card>
        <!-- // measurement-list -->
        <q-space />
        <q-separator />
        <q-space />
        <!--// measurement-create -->
        <div class="q-pa-md" style="max-width: 300px">
          <q-card>
            <div class="q-pa-md" style="max-width: 300px">
              <div class="text-subtitle2">Input Measurement Data</div>

              <q-form class="q-gutter-md">
                <q-input color="teal" filled v-model="measurement.properties.bore_id" type="number" id="bore_id" label="Bore ID *" hint="ID of the bore hole" lazy-rules
                  :rules="[ val => val !== null && val !== '' || 'Please type id', val => val > 0 && val < 1000 || 'Please type a correct id' ]"/>

                <q-input color="teal" filled v-model="measurement.properties.job_id" type="number" id="job_id" label="Job ID *" hint="ID of the job" lazy-rules
                  :rules="[ val => val !== null && val !== '' || 'Please type id', val => val > 0 && val < 1000 || 'Please type a correct id' ]"/>

                <q-input color="teal" filled v-model="measurement.properties.device_id" id="device_id" label="Device ID *" hint="ID of the device" lazy-rules
                  :rules="[ val => val && val.length > 0 || 'Please type something']"/>

                <q-input color="teal" filled v-model="measurement.properties.chemical_id" id="chemical_id" label="Chemical ID *" hint="ID of chemical" lazy-rules
                  :rules="[ val => val && val.length > 0 || 'Please type something']"/>

                <q-input color="teal" filled v-model="measurement.properties.concentration" id="concentration" type="number" label="Concentration *" hint="Concentration of chemical" lazy-rules
                  :rules="[ val => val !== null && val !== '' || 'Please type concentration', val => val > 0 && val < 30 || 'Please type correct chemical concentration' ]"/>

                <q-input color="teal" filled v-model="measurement.properties.comment" id="comment" label="Comment *" hint="Comment" lazy-rules
                  :rules="[ val => val && val.length > 0 || 'Please type something']"/>

                <!-- // date selection -->
                <q-input color="teal" filled v-model="measurement.properties.date" id="date" label="Date *" hint="Date of measurement">
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
                        <q-date v-model="measurement.properties.date" mask="YYYY-MM-DD" color="teal" text-color="black">
                          <div class="row items-right justify-end q-gutter-sm">
                            <q-btn icon="close" color="teal" flat v-close-popup />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <!-- // date selection -->

                <!-- // time selection -->
                <q-input color="teal" filled v-model="measurement.properties.time" id="time" label="Time *" hint="Time of measurement" mask="fulltime" :rules="['fulltime']">
                  <template v-slot:append>
                    <q-icon name="access_time" class="cursor-pointer">
                      <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
                        <q-time now-btn v-model="measurement.properties.time" mask="HH:mm:ss" with-seconds format24h color="teal" text-color="black">
                          <div class="row items-right justify-end q-gutter-sm">
                            <q-btn icon="close" color="teal" flat v-close-popup />
                          </div>
                        </q-time>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <!-- // time selection -->

                <!-- // longitude selection -->
                <q-input color="teal" filled v-model="longitude" id="longitude" label="Longitude *" hint="Longitude of the bore hole">
                  <template v-slot:append>
                    <q-icon name="fas fa-globe-americas" class="cursor-pointer">
                      <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
                        <q-card color="white">
                          <q-banner inline-actions>
                            <div class="text-subtitle2">
                              Select Method
                            </div>
                            <template align="right" v-slot:action>
                              <q-btn flat round dense icon="close" color="teal" v-close-popup />
                            </template>
                          </q-banner>
                          <q-card-section>
                            <q-btn label="Current Location" color="teal" class="text-black" @click="currentLocation" v-close-popup>
                            </q-btn>
                          </q-card-section>
                          <q-separator />
                          <q-card-section>
                            <q-btn label="Select Map Location" type="Point" color="teal" class="text-black" @click="drawType = 'point'">
                            </q-btn><br />
                             <q-btn label="Enter Map Selection" color="teal" class="text-black" @click="selectLocation" v-close-popup>
                            </q-btn>
                          </q-card-section>
                        </q-card>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <!-- // longitude selection -->

                <!-- // latitude selection -->
                <q-input color="teal" filled v-model="latitude" id="latitude" label="Latitude *" hint="Latitude of the bore hole">
                  <template v-slot:append>
                    <q-icon name="fas fa-globe-americas" class="cursor-pointer">
                      <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
                        <q-card color="white">
                          <q-banner inline-actions>
                            <div class="text-subtitle2">
                              Select Method
                            </div>
                            <template align="right" v-slot:action>
                              <q-btn flat round dense icon="close" color="teal" v-close-popup />
                            </template>
                          </q-banner>
                          <q-card-section>
                            <q-btn label="Current Location" color="teal" class="text-black" @click="currentLocation" v-close-popup>
                            </q-btn>
                          </q-card-section>
                          <q-separator />
                          <q-card-section>
                            <q-btn label="Select Map Location" type="Point" color="teal" class="text-black" @click="drawType = 'point'">
                            </q-btn><br />
                             <q-btn label="Enter Map Selection" color="teal" class="text-black" @click="selectLocation" v-close-popup>
                            </q-btn>
                          </q-card-section>
                        </q-card>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <!-- // latitude selection -->

                <!-- // submit, update, and reset -->
                <div>
                  <q-btn label="Submit" type="submit" color="teal" class="text-black" v-if="!this.measurement.id" @click="createMeasurement()" >
                    <span v-if="creating">Creating... Please wait </span>
                  </q-btn>
                  <q-btn label="Ubdate" type="submit" color="teal" class="text-black" v-if="this.measurement.id" @click="updateMeasurement()" >
                    <span v-if="updating">Updating... Please wait </span>
                  </q-btn>
                  <q-btn label="Reset" type="reset" color="teal" flat class="q-ml-sm" @click="onReset()" />
                </div>
                <!-- // submit, update, and reset -->
              </q-form>
            </div>
          </q-card>
        </div>
        <!--// /measurement-create -->
        <q-space />
        <q-separator />
        <q-space />
        <!-- // upload-file -->
        <q-card class="q-pa-md" style="max-width: 300px">
          <q-uploader label="Upload json data file" color="teal" text-color="black" flat bordered style="max-width: 250px"
            ref="uploader"
            accept=".json"
            :factory="uploadFile"
          />
        </q-card>
        <!-- // upload-file -->
      </q-drawer>
    </div>

    <!--// right side drawer -->
    <q-drawer side="right" v-model="rightDrawerOpen" show-if-above bordered content-class="teal">
      <q-list bordered class="rounded-borders">
        <!-- // baselayers -->
        <q-expansion-item default-opened expand-separator icon="list" label="Base Layers">
          <div class="q-pa-md" style="min-width: 200px">
            <q-list link>
              <!--//
                Rendering a <label> tag (notice tag="label")
                so QRadios will respond to clicks on QItems to
                change Toggle state.
              -->
              <q-item tag="label" v-ripple>
                <q-item-section avatar>
                  <q-radio v-on:input="showBaseLayer" val="osm" v-model="baselayer" color="teal" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>OpenStreetMap</q-item-label>
                </q-item-section>
              </q-item>

              <q-item tag="label" v-ripple>
                <q-item-section avatar>
                  <q-radio v-on:input="showBaseLayer" val="mapbox" v-model="baselayer" color="teal" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>MapBox Satellite</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </q-expansion-item>
        <!-- // baselayers -->

        <!-- // measurement, and powerlines layer -->
        <q-expansion-item default-opened expand-separator icon="list" label="Layers">
          <div class="q-pa-md q-gutter-y-sm column">
            <q-toggle
              :label="`Measurements Layer ${ measurementsModel }`"
              :key="layers[1].id"
              v-on:input="showMapPanelLayer(layers)"
              :class="{ 'is-active': layers[1].visible }"
              color="teal"
              false-value="Not Selected"
              true-value="Selected"
              v-model="measurementsModel"
            />
            <q-toggle
              :label="`Powerlines Layer ${ powerlinesModel }`"
              :key="layers[0].id"
              v-on:input="showMapPanelLayer(layers)"
              :class="{ 'is-active': layers[0].visible }"
              color="teal"
              false-value="Not Selected"
              true-value="Selected"
              v-model="powerlinesModel"
            />
          </div>
        </q-expansion-item>
        <!-- // measurement, and powerlines layer -->

        <!-- // state -->
        <q-expansion-item expand-separator icon="list" label="State">
          <q-markup-table class="table is-fullwidth" dense>
            <tr>
              <th class="text-left">Map center</th>
              <td class="text-left" style="font-size:10px">{{ center[0]}}, {{ center[1] }}</td>
            </tr>
            <tr>
              <th class="text-left">Map zoom</th>
              <td class="text-left" style="font-size:10px">{{ zoom }}</td>
            </tr>
            <tr>
              <th class="text-left">Map rotation</th>
              <td class="text-left" style="font-size:10px">{{ rotation }}</td>
            </tr>
            <tr>
              <th class="text-left">Event coordinate</th>
              <td class="text-left" style="font-size:10px">{{ eventCoordinate[0] }}, {{ eventCoordinate[1] }}</td>
            </tr>
            <tr>
              <th class="text-left">Device coordinate</th>
              <td class="text-left" style="font-size:10px">{{ deviceCoordinate[0] }}, {{ deviceCoordinate[1] }}</td>
            </tr>
            <tr>
              <th class="text-left">Coordinate accuracy</th>
              <td class="text-left" style="font-size:10px">{{ coordinateAccuracy }} meters</td>
            </tr>
            <tr>
              <th class="text-left">Selected features</th>
              <td class="text-left" style="font-size:10px">{{ pid }}</td>
            </tr>
          </q-markup-table>
        </q-expansion-item>
        <!-- // state -->

        <!-- // legend -->
        <q-expansion-item expand-separator icon="list" label="Legend">
          <q-markup-table>
            <tr>
              <td><hr style=getPowerlinesStyle /></td>
              <td>Powerlines</td>
            </tr>
            <tr>
              <td><b>Source</b></td>
              <td>This data was derived from nothing.</td>
            </tr>
            <tr>
              <td><span class="dot"></span></td>
              <td>Test Measurments</td>
            </tr>
            <tr>
              <td><b>Source</b></td>
              <td>This data was derived from nothing.</td>
            </tr>
          </q-markup-table>
        </q-expansion-item>
        <!-- // legend -->

        <!-- // filter -->
        <q-expansion-item expand-separator icon="list" label="Filter">
          <q-markup-table class="table is-fullwidth">
            <tr>
              <td>
                <q-datetime-picker today-btn now-btn outlined label="Select Start DateTime" mode="datetime" color="teal"
                  v-model="starttimestamp" format24h clearable></q-datetime-picker>
              </td>
            </tr>
            <tr>
              <td>
                <q-datetime-picker today-btn now-btn outlined label="Select End DateTime" mode="datetime" color="teal"
                  v-model="endtimestamp" format24h clearable></q-datetime-picker>
              </td>
            </tr>
            <tr>
              <td>
                <q-btn color="teal" class="text-black" @click="filterMeasurements">Filter Measurements</q-btn>
              </td>
            </tr>
          </q-markup-table>
        </q-expansion-item>
        <!-- // filter -->

        <!-- // search -->
        <q-expansion-item expand-separator icon="list" label="Search">
          <q-markup-table class="table is-fullwidth">
            <tr>
              <td>
                <treeselect v-model="jobidsx" class="treeinput" :auto-load-root-options="false"
                  :options="searchjoptions"  :multiple="true" placeholder="Select Job ID" />
              </td>
            </tr>
            <tr>
              <td>
                <q-datetime-picker today-btn now-btn outlined label="Select Start DateTime" mode="datetime" color="teal"
                  v-model="starttimestampx" format24h clearable></q-datetime-picker>
              </td>
            </tr>
            <tr>
              <td>
                <q-datetime-picker today-btn now-btn outlined label="Select End DateTime" mode="datetime" color="teal"
                  v-model="endtimestampx" format24h clearable></q-datetime-picker>
              </td>
            </tr>
            <tr>
              <td>
                <q-btn color="teal" class="text-black" @click="searchMeasurements">Search Measurements</q-btn>
              </td>
            </tr>
           </q-markup-table>
        </q-expansion-item>
        <!-- // search -->
      </q-list>
    </q-drawer>
    <!--// left side drawer -->

    <!--// app map -->
    <vl-map v-if="mapVisible" class="map" ref="map" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
      @click="onMapClick" data-projection="EPSG:4326" @mounted="onMapMounted" :controls="false" style="height:1200px">
       <!--// map view aka ol.View -->
      <vl-view ref="view" :center.sync="center" :zoom.sync="zoom" :rotation.sync="rotation"></vl-view>

      <!--// click interactions -->
      <vl-interaction-select ref="selectInteraction" :features.sync="selectedFeatures" v-if="drawType === undefined">
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
              <div v-if="feature.id == undefined">
                <!--// Interactions drawing polygon to select measurements for bar plot -->
              </div>
              <div v-else>
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
              </div>
            </vl-overlay>
          </div>
          <!--// selected feature popup -->

          <!--// selected feature bar plot -->
          <div v-else-if="isBox === 'yes'">
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

      <!--// geolocation -->
      <vl-geoloc @update:position="onUpdatePosition" enableHighAccuracy="true" >
        <template slot-scope="geoloc">
          <vl-feature v-if="geoloc.position" id="position-feature">
            <vl-geom-point :coordinates="geoloc.position"></vl-geom-point>
            <vl-style-box>
              <vl-style-icon src="statics/marker.png" :scale="0.4" :anchor="[0.5, 1]"></vl-style-icon>
            </vl-style-box>
          </vl-feature>
        </template>
      </vl-geoloc>
      <vl-geoloc @update:accuracy="onUpdateAccuracy" enableHighAccuracy="true" >
        <template slot-scope="geoloc">
          <vl-feature v-if="geoloc.accuracy" id="accuracy-feature">
            <div :accuracy="geoloc.accuracy"></div>
          </vl-feature>
        </template>
      </vl-geoloc>
      <!--// geolocation -->

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

      <!--// draw components -->
      <vl-layer-vector id="draw-pane">
        <vl-source-vector ref="drawSource" ident="draw-target" :features.sync="drawnFeatures"></vl-source-vector>
      </vl-layer-vector>

      <vl-interaction-draw v-if="drawType" source="draw-target" :type="drawType"></vl-interaction-draw>
      <vl-interaction-modify source="draw-target"></vl-interaction-modify>
      <vl-interaction-snap source="draw-target" :priority="10"></vl-interaction-snap>
      <!--// draw components -->
    </vl-map>
    <!--// app map -->

    <!--// left side drawer buttons -->
    <div v-if="!authenticated">
      <q-page-sticky position="top-left" :offset="[22, 18]">
        <q-btn flat dense round icon="fas fa-sign-in-alt" class="bg-teal text-black" aria-label="Login" v-if="!authenticated" @click="logind"></q-btn>
      </q-page-sticky>
    </div>
    <div v-else-if="authenticated">
      <q-page-sticky position="top-left" :offset="[58, 18]">
        <q-btn flat dense round icon="fas fa-sign-out-alt" class="bg-teal text-black" aria-label="Logout" v-if="authenticated" @click="logoutd"></q-btn>
      </q-page-sticky>
      <q-page-sticky position="top-left" :offset="[18, 18]">
        <q-btn flat dense round icon="menu" class="bg-teal text-black" @click="leftDrawerOpen = !leftDrawerOpen" aria-label="Menu"></q-btn>
      </q-page-sticky>
    </div>
    <!--// left side drawer buttons -->

    <!--// ol map controls -->
    <q-page-sticky position="top-left" :offset="[18, 58]">
      <div id="ZoomTarget"></div>
    </q-page-sticky>
    <q-page-sticky position="bottom-left" :offset="[8, 38]">
      <div id="OverviewMapTarget"></div>
    </q-page-sticky>
    <q-page-sticky position="bottom-left" :offset="[15, 8]">
      <div id="ScaleTarget"></div>
    </q-page-sticky>
    <!--// ol map controls -->

    <!--// right side drawer button -->
    <q-page-sticky position="top-right" :offset="[18, 18]">
      <q-btn flat dense round icon="menu" class="bg-teal text-black" @click="rightDrawerOpen = !rightDrawerOpen" aria-label="Menu"></q-btn>
    </q-page-sticky>
    <q-page-sticky position="top-right" :offset="[18, 58]">
      <q-btn color="teal" class="text-black" @click="$q.fullscreen.toggle()" round :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'" />
    </q-page-sticky>
    <!--// right side drawer button -->

    <!--// select bar plot tool -->
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-fab icon="keyboard_arrow_up" direction="up" color="teal text-black">
        <q-fab-action color="teal" class="text-black" icon="fas fa-vector-square">
          <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
            <q-card color="white">
              <q-banner inline-actions>
                <div class="text-subtitle2">
                  Create Bar Plot of Selected Features
                </div>
                <template align="right" v-slot:action>
                  <q-btn flat round dense icon="close" color="teal" v-close-popup />
                </template>
              </q-banner>
              <q-separator />
              <q-card-section>
                <div v-if="drawnFeatures.length === 0">
                  <q-btn label="Draw Polygon Around Features" type="Point" color="teal" class="text-black" @click="drawType = 'polygon'">
                  </q-btn>
                </div>
                <div v-else>
                  <q-btn label="Create Bar Plot of Features" color="teal" class="text-black" @click="selectInDrawnPolygon">
                  </q-btn>
                </div>
              </q-card-section>
            </q-card>
          </q-popup-proxy>
        </q-fab-action>
      </q-fab>
    </q-page-sticky>
    <!--// select bar plot tool -->

    <!--// base layer map attribution -->
    <q-page-sticky position="bottom-left" :offset="[200, 38]">
      <div id="AttributionTarget"></div>
    </q-page-sticky>
    <!--// base layer map attribution -->
  </q-layout>
</template>

<script>
// quasar and vuelayers import
import { openURL, date } from 'quasar'
import { findPointOnSurface, writeGeoJsonFeature } from 'vuelayers/lib/ol-ext'
import { camelCase } from 'lodash'

// ol controls import
import ScaleLine from 'ol/control/ScaleLine'
import OverviewMap from 'ol/control/OverviewMap'
import Zoom from 'ol/control/Zoom'
import Attribution from 'ol/control/Attribution'

// other ol imports
import { Style, Stroke, Fill, Circle } from 'ol/style'
import { DEVICE_PIXEL_RATIO } from 'ol/has.js'
import DragBox from 'ol/interaction/DragBox'
import { platformModifierKeyOnly } from 'ol/events/condition.js'
import { toLonLat } from 'ol/proj.js'

// d3 barchart import
import d3Barchart from '../mixins/vue-d3-barchart'

// treeselect import
import { Treeselect, LOAD_ROOT_OPTIONS } from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'

// axios import
import axios from 'axios'

// const fs = require('fs')

// API service import
import { APIService } from '../http/APIService'
const apiService = new APIService()

// auth service import
import AuthService from '../auth/AuthService'
const auth = new AuthService()
const { login, logout, authenticated, authNotifier } = auth

// measurement import
import MeasurementList from './MeasurementList'

// EventBus import
import { EventBus } from '../mixins/event-bus.js'

// pubhost and secrets import
import pubhost from '../assets/pubhost.json'
import secrets from '../assets/secrets.json'
let gettoken = function () {
  return secrets[0].MB_KEY
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
    Treeselect,
    MeasurementList
  },
  data () {
    auth.handleAuthentication()
    authNotifier.on('authChange', authState => {
      this.authenticated = authState.authenticated
    })
    return {
      loading: undefined,
      caption: undefined,
      // map parameters
      center: [-73.851271, 40.725070],
      // center: [-79.0085632, 35.9415808],
      zoom: 15,
      rotation: 0,
      mapVisible: true,
      // authentication and drawers
      auth,
      authenticated,
      leftDrawerOpen: false,
      rightDrawerOpen: false,
      // data input attributes
      showCreateMessage: false,
      showUpdateMessage: false,
      creating: false,
      updating: false,
      // measurement data structure and associate attributs
      measurement: {
        'type': 'Feature',
        'properties': {
          'bore_id': null,
          'job_id': null,
          'device_id': null,
          'chemical_id': null,
          'concentration': null,
          'date': this.currentDate(),
          'time': this.currentTime(),
          'status': 'd',
          'comment': null
        },
        'geometry': {
          'type': 'Point',
          'coordinates': [null, null]
        }
      },
      longitude: null,
      latitude: null,
      measurements: '',
      measurementsModel: 'Selected',
      // measurement search and popup attributes
      searchtoptions: [],
      searchjoptions: [],
      starttimestamp: this.currentDate() + 'T' + this.currentTime(),
      endtimestamp: this.currentDate() + 'T' + this.currentTime(),
      starttimestampx: this.currentDate() + 'T' + this.currentTime(),
      endtimestampx: this.currentDate() + 'T' + this.currentTime(),
      toptions: null,
      jobids: undefined,
      jobidsx: undefined,
      joptions: null,
      pid: undefined,
      chemical_id: undefined,
      concentration: undefined,
      timestamp: undefined,
      // powerline attributes
      powerlinesModel: 'Selected',
      powerline: undefined,
      // stored and selected features
      storeFeatures: [],
      selectedFeatures: [],
      selectedFeaturesBarBox: [],
      isBox: undefined,
      // state attributes
      eventCoordinate: [NaN, NaN],
      deviceCoordinate: [NaN, NaN],
      coordinateAccuracy: undefined,
      boxCoordinate: undefined,
      // draw controls
      drawControls: [
        {
          type: 'point',
          label: 'Draw Point',
          icon: 'map-marker',
          stopClick: true
        },
        {
          type: 'polygon',
          label: 'Draw Polygon',
          icon: 'map-marker',
          stopClick: true
        },
        {
          type: undefined,
          label: 'Stop drawing',
          icon: 'times'
        }
      ],
      drawType: undefined,
      drawnFeatures: [],
      coordinates: [],
      // bar plot options
      barplotpoint: undefined,
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
      // baselayers config
      baselayer: 'osm',
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
    // search timestamp
    let that = this
    let turl = 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/timestamp/?format=json'
    axios.get(turl)
      .then(function (response) {
        that.searchtoptions = response.data
      })
      .catch(function (error) {
        console.log(error)
      })
    // search jobid
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
    // watch for selected features
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
    login,
    logout,
    logind: function () {
      login()
    },
    logoutd: function () {
      logout()
    },
    handleAuthentication: function () {
      auth.handleAuthentication()
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
        new ScaleLine({
          target: 'ScaleTarget'
        }),
        new OverviewMap({
          collapsed: false,
          collapsible: true,
          target: 'OverviewMapTarget'
        }),
        new Zoom({
          target: 'ZoomTarget'
        }),
        new Attribution({
          collapsed: false,
          collapsible: false,
          target: 'AttributionTarget'
        })
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
    selectInDrawnPolygon: function () {
      this.drawnFeatures = []
      this.selectedFeatures = []
      this.selectedFeaturesBarBox = []
      this.isBox = 'yes'
      // only use source that have chemical_id
      let vectorSource
      let i
      for (i = 0; i < this.$refs.layerSource.length; i++) {
        let features = this.$refs.layerSource[i].getFeatures()
        if (features[0].values_.chemical_id) {
          vectorSource = this.$refs.layerSource[i].$source
        }
      }
      const drawSource = this.$refs.drawSource.$source
      const extent = drawSource.getExtent()
      // console.log(extent)
      vectorSource.forEachFeatureIntersectingExtent(extent, feature => {
        feature = writeGeoJsonFeature(feature)
        this.selectedFeatures.push(feature)
        this.selectedFeaturesBarBox.push({ x: feature.properties['timestamp'], y: feature.properties['concentration'] })
        this.chemical_id = feature.properties['chemical_id']
        this.pid = this.chemical_id
      })
      this.drawType = undefined
      // console.log(this.$refs)
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
      // console.log(layers)
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
        this.eventCoordinate = event.coordinate
        let feature = features[0]
        if (feature.id_ !== undefined) {
          let properties = feature.getProperties()
          // alert('click')
          if (properties['chemical_id']) {
            this.pid = properties['chemical_id']
            this.chemical_id = this.pid
            this.concentration = properties['concentration']
            this.timestamp = properties['timestamp']
            this.selectedFeaturesBarBox = []
            this.selectedFeatures = []
            this.isBox = 'no'
          } else if (properties['powerline']) {
            this.pid = properties['powerline']
            this.powerline = this.pid
            this.concentration = undefined
            this.timestamp = undefined
            this.selectedFeaturesBarBox = []
            this.selectedFeatures = []
            this.isBox = 'no'
          }
        } else {
          // this.selectedFeaturesBarBox = []
          // this.selectedFeatures = []
          // this.isBox = 'no'
          // console.log(features)
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
    },
    searchMeasurements: function () {
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
    currentDate: function () {
      let timeStamp = Date.now()
      let formattedString = date.formatDate(timeStamp, 'YYYY-MM-DD')
      return formattedString
    },
    currentTime: function () {
      let timeStamp = Date.now()
      let formattedString = date.formatDate(timeStamp, 'HH:mm:ss')
      return formattedString
    },
    currentLocation: function () {
      // console.log(this.$refs.view)
      this.longitude = this.deviceCoordinate[0]
      this.latitude = this.deviceCoordinate[1]
    },
    selectLocation: function () {
      this.drawType = undefined
      this.longitude = this.eventCoordinate[0]
      this.latitude = this.eventCoordinate[1]
    },
    onUpdatePosition: function (coordinate) {
      this.deviceCoordinate = coordinate
    },
    onUpdateAccuracy: function (accuracy) {
      this.coordinateAccuracy = accuracy
    },
    onReset: function () {
      this.measurement.id = null
      this.measurement.properties.bore_id = null
      this.measurement.properties.job_id = null
      this.measurement.properties.device_id = null
      this.measurement.properties.chemical_id = null
      this.measurement.properties.concentration = null
      this.measurement.properties.comment = null
      this.measurement.properties.date = this.currentDate()
      this.measurement.properties.time = this.currentTime()
      this.longitude = null
      this.latitude = null
      this.measurement.geometry.coordinates = null
    },
    createMeasurement: function () {
      let coordinates = [parseFloat(this.longitude), parseFloat(this.latitude)]
      this.measurement.geometry.coordinates = coordinates
      this.creating = true
      apiService.createMeasurement(this.measurement).then((result) => {
        // console.log(result)
        // success
        if (result.status === 201) {
          this.measurement = result.data
          this.showCreateMessage = true
          let i
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.chemical_id) {
              this.$refs.layerSource[i].addFeature(this.measurement)
              this.$refs.drawSource.clearFeatures()
            }
          }
          // console.log(this.$refs.layerSource)
        }
        sleep(1000).then(() => {
          this.creating = false
        })
      })
    },
    updateMeasurement: function () {
      let coordinates = [parseFloat(this.longitude), parseFloat(this.latitude)]
      this.measurement.geometry.coordinates = coordinates
      // console.log('update measurement ' + JSON.stringify(this.measurement))
      this.updating = true
      apiService.updateMeasurement(this.measurement).then((result) => {
        // success
        if (result.status === 200) {
          this.measurement = result.data
          this.showUpdateMessage = true
          let i
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.chemical_id) {
              let feature = this.$refs.layerSource[i].getFeatureById(this.measurement.id)
              this.$refs.layerSource[i].removeFeature(feature)
              this.$refs.layerSource[i].addFeature(this.measurement)
              this.$refs.drawSource.clearFeatures()
            }
          }
          sleep(1000).then(() => {
            this.updating = false
          })
        }
      })
    },
    editMeasurement: function (measurement) {
      this.measurement = measurement
      this.longitude = measurement.geometry.coordinates[0]
      this.latitude = measurement.geometry.coordinates[1]
    },
    uploadFile: function (files) {
      let that = this
      that.loading = true
      let Uploader = this.$refs.uploader
      let reader = new FileReader()
      let file = files[0]
      reader.readAsText(file)
      reader.onerror = err => console.error(`Failed to read file: ${err}`)
      reader.onload = function () {
        let geojson = JSON.parse(reader.result)
        that.creating = true
        let i
        for (i = 0; i < geojson.features.length; i++) {
          apiService.createMeasurement(geojson.features[i]).then((result) => {
            if (result.status === 201) {
              that.measurement = result.data
              that.showCreateMessage = true
              let j
              for (j = 0; j < that.$refs.layerSource.length; j++) {
                let features = that.$refs.layerSource[j].getFeatures()
                if (features[0].values_.chemical_id) {
                  that.$refs.layerSource[j].addFeature(that.measurement)
                  that.$refs.drawSource.clearFeatures()
                }
              }
            }
            sleep(1000).then(() => {
              that.creating = false
            })
          })
        }
        Uploader.removeFile(file)
        sleep(2000).then(() => {
          that.loading = false
        })
      }
    }
  },
  mounted () {
    // Listen for the edit-measurement event and its payload.
    EventBus.$on('edit-measurement', measurement => {
      this.editMeasurement(measurement)
    })
    if (this.$route.params.id) {
      console.log(this.$route.params.id)
      apiService.getMeasurement(this.$route.params.id).then((measurement) => {
        this.measurement = measurement
      })
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

  .ol-control button:hover,
  .ol-control button:focus
    text-decoration: none
    background-color: rgba(0,128,128,0.8)

  .ol-scale-line
    background: rgba(0,128,128,0.8)

  a:hover
    font-weight:bold

  .Powerlines
    position: relative

  .map
    margin: 0
    padding: 0
    width: 100%
    height: 100%

  .view
    margin: 0
    padding: 0
    width: 100%
    height: 100%

  .feature-popup
    position: absolute
    left: -20px
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
    left: -20px
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

  .measurement-popup
    window-height: 100em

  .dot
    height: 15px;
    width: 15px;
    background-color: #84f542;
    border-radius: 50%;
    display: inline-block

  .chart
    display: inline-block
    width: 700px
    height: 200px
    margin-top: 0em

  .treeinput
    color: #025c5c

  .vue-treeselect__control
    height: 46px;
    border: 1px solid #b8b8b8;
    border-radius: 8px;

  .vue-treeselect:not(.vue-treeselect--disabled):not(.vue-treeselect--focused) .vue-treeselect__control:hover
    border-color: #919191;

  .vue-treeselect--open .vue-treeselect__control
    border-color: #2e2e2e;

  .vue-treeselect--focused:not(.vue-treeselect--open) .vue-treeselect__control
    border-color: #008080;
    box-shadow: 0 0 0 3px rgba(3, 155, 229, 0.1);

  .vue-treeselect__multi-value-item
    background: #6bcfcf;
    color: #025c5c;

  .vue-treeselect:not(.vue-treeselect--disabled) .vue-treeselect__multi-value-item:not(.vue-treeselect__multi-value-item- disabled):hover .vue-treeselect__multi-value-item:not(.vue-treeselect__multi-value-item-new) .vue-treeselect__multi-    value-item:not(.vue-treeselect__multi-value-item-new):hover
    background: #6bcfcf;
    color: #025c5c;

  .vue-treeselect__value-remove
    color: #025c5c;

  .vue-treeselect__label-container:hover .vue-treeselect__checkbox--unchecked
    border-color: #025c5c;
    background: #fff;

  .vue-treeselect__checkbox--indeterminate
    border-color: #025c5c;
    background: #025c5c;

  .vue-treeselect__label-container:hover .vue-treeselect__checkbox--indeterminate
    border-color: #025c5c;
    background: #025c5c;

  .vue-treeselect__checkbox--checked
    border-color: #025c5c;
    background: #025c5c;

  .vue-treeselect__label-container:hover .vue-treeselect__checkbox--checked
    border-color: #025c5c;
    background: #025c5c;

  .vue-treeselect__placeholder
    color: #787878;

</style>
