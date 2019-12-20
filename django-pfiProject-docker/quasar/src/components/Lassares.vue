<template>
  <q-layout view="lhr lpr lfr">
    <!--// Left Drawer, check to see if authenticated -->
    <div v-if="!authenticated">
      <!-- If not authenticated do nothing -->
    </div>
    <div v-else-if="authenticated">
      <!-- If authenticated show drawer -->
      <q-drawer v-model="leftDrawerOpen" show-if-above bordered :content-style="{ backgroundColor: 'rgba(199, 235, 235, 0.5)' }">
        <!-- // measurement-list -->
        <q-card class="q-pa-md bg-teal-1" style="max-width: 300px">
          <q-btn-dropdown label="View List of Measurements" type="viewlist" color="teal" class="text-black">
            <q-list class="bg-teal-1">
              <q-item>
                <q-item-section>
                  <q-btn label="Mass Spectrometer" type="viewgcmv" color="teal" class="text-black">
                    <q-popup-proxy class="measurement-popup" transition-show="flip-up" transition-hide="flip-down">
                      <mscnt-list></mscnt-list>
                    </q-popup-proxy>
                  </q-btn>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-btn label="Gas Chromatograph" type="viewgcmv" color="teal" class="text-black">
                    <q-popup-proxy class="measurement-popup" transition-show="flip-up" transition-hide="flip-down">
                      <gcmv-list></gcmv-list>
                    </q-popup-proxy>
                  </q-btn>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </q-card>
        <!-- // measurement-list -->
        <q-space />
        <q-separator />
        <q-space />
        <!--// measurement-create -->
        <div class="q-pa-md" style="max-width: 300px">
          <q-card class="bg-teal-1">
            <div class="q-pa-md" style="max-width: 300px">
              <div class="text-subtitle2">Input Measurement Data</div>

              <q-form class="q-gutter-md">
                <q-input color="teal" filled v-model="measurement.properties.job_id" type="number" id="job_id" label="Job ID *" hint="ID of the job" lazy-rules
                  :rules="[ val => val !== null && val !== '' || 'Please type id', val => val > 0 && val < 100000 || 'Please type a correct id' ]" />

                <q-input color="teal" filled v-model="measurement.properties.bore_id" type="number" id="bore_id" label="Bore ID *" hint="ID of the bore hole" lazy-rules
                  :rules="[ val => val !== null && val !== '' || 'Please type id', val => val > 0 && val < 100000 || 'Please type a correct id' ]"/>

                <q-input color="teal" filled v-model="measurement.properties.chemical_id" id="chemical_id" label="Chemical ID *" hint="ID of chemical" lazy-rules
                  :rules="[ val => val && val.length > 0 || 'Please type something']"/>

                <q-select color="teal" filled v-model="measurement.properties.instrument" id="instrument" label="Instrument *" hint="Instrument being used" :options="devoptions" />

                <div v-if="measurement.properties.instrument == 'Mass Spectrometer'">
                  <q-input color="teal" filled v-model="measurement.properties.measurement_value" id="measurement_value" type="number" label="Count *" hint="Count of chemical" lazy-rules
                    :rules="[ val => val !== null && val !== '' || 'Please type count', val => val > 0 && val < 30000 || 'Please type correct chemical count' ]"/>
                </div>
                <div v-else-if="measurement.properties.instrument == 'Gas Chromatograph'">
                  <q-input color="teal" filled v-model="measurement.properties.measurement_value" id="measurement_value" type="number" label="Millivolt *" hint="Millivolt of measurement" lazy-rules
                    :rules="[ val => val !== null && val !== '' || 'Please type millivolt', val => val > 0 && val < 30000 || 'Please type correct millivolt' ]"/>
                </div>

                <q-input color="teal" filled v-model="measurement.properties.comment" id="comment" label="Comment *" hint="Comment" lazy-rules
                  :rules="[ val => val && val.length > 0 || 'Please type something']"/>

                <!-- // date selection -->
                <q-input color="teal" filled v-model="measurement.properties.date" id="date" label="Date *" hint="Date of measurement">
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
                        <q-date v-model="measurement.properties.date" mask="YYYY-MM-DD" color="teal" text-color="black" class="bg-teal-1">
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
                        <q-time now-btn v-model="measurement.properties.time" mask="HH:mm:ss" with-seconds format24h color="teal" text-color="black" class="bg-teal-1">
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
                        <q-card class="bg-teal-1">
                          <q-banner inline-actions class="bg-teal-1">
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
                            <q-btn label="Select Map Location" type="Point" color="teal" class="text-black" @click="drawType = 'point'" v-close-popup />
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
                        <q-card class="bg-teal-1">
                          <q-banner inline-actions class="bg-teal-1">
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
                            <q-btn label="Select Map Location" type="Point" color="teal" class="text-black" @click="drawType = 'point'" v-close-popup />
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
        <q-card class="q-pa-md teal bg-teal-1" style="max-width: 300px">
          <q-uploader label="Upload json data file" color="teal" text-color="black" flat bordered style="max-width: 250px"
            ref="uploader" accept=".json" :factory="uploadFile" dark />
        </q-card>
        <!-- // upload-file -->
      </q-drawer>
    </div>

    <!--// right side drawer -->
    <q-drawer side="right" v-model="rightDrawerOpen" show-if-above bordered content-class="teal bg-teal-1">
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
              :label="`Gas Chromatograph Layer ${ gcmvModel }`"
              :key="layers[2].id"
              v-on:input="showMapPanelLayer(layers)"
              :class="{ 'is-active': layers[2].visible }"
              color="teal"
              false-value="Not Selected"
              true-value="Selected"
              v-model="gcmvModel"
            />
            <q-toggle
              :label="`Mass Spectrometer Layer ${ mscntModel }`"
              :key="layers[1].id"
              v-on:input="showMapPanelLayer(layers)"
              :class="{ 'is-active': layers[1].visible }"
              color="teal"
              false-value="Not Selected"
              true-value="Selected"
              v-model="mscntModel"
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
          <q-markup-table class="table is-fullwidth bg-teal-1" dense>
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
          <q-markup-table class="bg-teal-1">
            <tr>
              <td><img :src=" 'statics/Powerline.png' "></td>
              <td>Powerlines</td>
            </tr>
            <tr>
              <td><b>Source</b></td>
              <td>This data was derived<br/> from nothing.</td>
            </tr>
            <tr>
              <td id="nested">
                <table class="mtable">
                  <tr>
                    <td style="padding:5px"><span class="msdot1"></span></td>
                    <td style="padding:5px"><span class="msdot2"></span></td>
                    <td style="padding:5px"><span class="msdot3"></span></td>
                  </tr>
                </table>
              </td>
              <td>Mass Spectrometer</td>
            </tr>
            <tr>
              <td><b>Source</b></td>
              <td>This data was derived<br/> from nothing.</td>
            </tr>
            <tr>
              <td id="nested">
                <table class="mtable">
                  <tr>
                    <td style="padding:5px"><span class="gcdot1"></span></td>
                    <td style="padding:5px"><span class="gcdot2"></span></td>
                    <td style="padding:5px"><span class="gcdot3"></span></td>
                  </tr>
                </table>
              </td>
              <td>Gas Chromatograph </td>
            </tr>
            <tr>
              <td><b>Source</b></td>
              <td>This data was derived<br/> from nothing.</td>
            </tr>
            <tr>
              <td><img :src=" 'statics/marker.png' " height="50" width="50"></td>
              <td>Current Location</td>
            </tr>
          </q-markup-table>
        </q-expansion-item>
        <!-- // legend -->

        <!-- // search -->
        <q-expansion-item expand-separator icon="list" label="Search Measurements">
          <q-markup-table class="table is-fullwidth bg-teal-1">
            <tr>
              <td>
                <q-select color="teal" filled v-model="measurement.properties.instrument" label="Type of Instrument"
                  id="instrument" hint="Instrument being used" :options="devoptions" />
              </td>
            </tr>
            <div v-if="measurement.properties.instrument == 'Mass Spectrometer'">
              <tr>
                <td>
                  <treeselect v-model="jobidsx" class="treeinput" :auto-load-root-options="false"
                    :options="searchmscntjoptions" :multiple="true" placeholder="Select Job ID" />
                </td>
              </tr>
            </div>
            <div v-else-if="measurement.properties.instrument == 'Gas Chromatograph'">
              <tr>
                <td>
                  <treeselect v-model="jobidsx" class="treeinput" :auto-load-root-options="false"
                    :options="searchgcmvjoptions" :multiple="true" placeholder="Select Job ID" />
                </td>
              </tr>
            </div>
            <tr>
              <td>
                <q-datetime-picker today-btn now-btn outlined label="Select Start DateTime" mode="datetime" color="teal"
                  v-model="starttimestampx" default-standard="iso" format24h clearable></q-datetime-picker>
              </td>
            </tr>
            <tr>
              <td>
                <q-datetime-picker today-btn now-btn outlined label="Select End DateTime" mode="datetime" color="teal"
                  v-model="endtimestampx" default-standard="iso" format24h clearable></q-datetime-picker>
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
                      Title: {{ ptitle }}<br>
                      Powerline: {{ powerline }}<br>
                      Voltage: {{ feature.properties['voltage'] }}<br>
                      Service Date: {{ feature.properties['service_date'] }}
                    </div>
                    <div v-else-if="pid == feature.properties['chemical_id']">
                      Job ID: {{ feature.properties['job_id'] }}<br>
                      Bore ID: {{ feature.properties['bore_id'] }}<br>
                      Chemical ID: {{ chemical_id }}<br>
                      Device ID: {{ feature.properties['instrument'] }}<br>
                      <div v-if="feature.properties['instrument'] == 'Mass Spectrometer'">
                        Count: {{ measurement_value }}<br>
                      </div>
                      <div v-else-if="feature.properties['instrument'] == 'Gas Chromatograph'">
                        Millivolt: {{ measurement_value }}<br>
                      </div>
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
                      <div v-if="feature.properties['instrument'] == 'Mass Spectrometer'">
                        {{ pid }} count
                      </div>
                      <div v-else-if="feature.properties['instrument'] == 'Gas Chromatograph'">
                        {{ pid }} millivolt
                      </div>
                    </b>
                    <template v-slot:action>
                      <q-btn flat round dense icon="close" @click="closeBarChart" />
                    </template>
                  </q-banner>
                  <table class="table is-fullwidth">
                    <div v-if="pid == chemical_id">
                      <div v-if="Object.keys(selectedFeaturesBarBox).length > 0">
                        <tr>
                          <div v-if="feature.properties['instrument'] == 'Mass Spectrometer'">
                            <td>x = Timestamp, y = Count</td>
                          </div>
                          <div v-else-if="feature.properties['instrument'] == 'Gas Chromatograph'">
                            <td>x = Timestamp, y = Millivolt</td>
                          </div>
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
      <vl-geoloc ref="geoloc" @update:position="onUpdatePosition" enableHighAccuracy="true" maximumAge="0" timeout="Infinity" >
        <template slot-scope="geoloc">
          <vl-feature v-if="geoloc.position" id="position-feature">
            <vl-geom-point :coordinates="geoloc.position"></vl-geom-point>
            <vl-style-box>
              <vl-style-icon src="statics/marker.png" :scale="0.4" :anchor="[0.5, 1]"></vl-style-icon>
            </vl-style-box>
          </vl-feature>
        </template>
      </vl-geoloc>
      <vl-geoloc @update:accuracy="onUpdateAccuracy" enableHighAccuracy="true" maximumAge="0" timeout="Infinity" >
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
        <vl-source-vector ref="drawSource" ident="draw-target"></vl-source-vector>
      </vl-layer-vector>

      <vl-interaction-draw v-if="drawType" @drawend="drawEnd" source="draw-target" :type="drawType"></vl-interaction-draw>
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
            <q-card class="bg-teal-1">
              <q-banner inline-actions class="bg-teal-1">
                <div class="text-subtitle2">
                  Create Bar Plot of Selected Features
                </div>
                <template align="right" v-slot:action>
                  <q-btn flat round dense icon="close" color="teal" v-close-popup />
                </template>
              </q-banner>
              <q-separator />
              <q-card-section>
                <q-select color="teal" filled v-model="measurement.properties.instrument" id="instrument" label="Instrument *" hint="Instrument being used" :options="devoptions" />
              </q-card-section>
              <q-card-section>
                <q-btn label="Draw Polygon Around Features" type="Polygon" color="teal" class="text-black" @click="drawType = 'polygon'" v-close-popup />
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
import { findPointOnSurface, writeGeoJsonFeature, loadingBBox } from 'vuelayers/lib/ol-ext'
import { camelCase } from 'lodash'

// ol controls import
import ScaleLine from 'ol/control/ScaleLine'
import OverviewMap from 'ol/control/OverviewMap'
import Zoom from 'ol/control/Zoom'
import Attribution from 'ol/control/Attribution'

// other ol imports
import { Style, Stroke, Fill, Circle } from 'ol/style'
import { DEVICE_PIXEL_RATIO } from 'ol/has.js'
import { toLonLat } from 'ol/proj.js'
// import Select from 'ol/interaction/Select.js'

// d3 barchart import
import d3Barchart from '../mixins/vue-d3-barchart'

// treeselect import
import { Treeselect } from '@riophae/vue-treeselect'
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
import mscntList from './mscntList'
import gcmvList from './gcmvList'

// EventBus import
import { EventBus } from '../mixins/event-bus.js'

// pubhost and secrets import
import pubhost from '../assets/pubhost.json'
import secrets from '../assets/secrets.json'
let gettoken = function () {
  return secrets[0].MB_KEY
}

// color values for measurement count
let count2color = function (measurementvalue) {
  let r = 0
  let g = 0
  let b = 0
  if (measurementvalue < 50) {
    g = 255
    b = Math.round(5.1 * measurementvalue)
  } else {
    b = 255
    g = Math.round(510 - 5.10 * measurementvalue)
  }
  let h = r * 0x1 + g * 0x100 + b * 0x10000
  return '#' + ('000000' + h.toString(16)).slice(-6)
}

let millivolt2color = function (measurementvalue) {
  let r = 0
  let g = 0
  let b = 0
  if (measurementvalue < 50) {
    g = 255
    r = Math.round(5.1 * measurementvalue)
  } else {
    r = 255
    g = Math.round(510 - 5.10 * measurementvalue)
  }
  let h = r * 0x1 + g * 0x100 + b * 0x10000
  return '#' + ('000000' + h.toString(16)).slice(-6)
}

// sleepy time for treeselections
const sleep = d => new Promise(resolve => setTimeout(resolve, d))

export default {
  name: 'Lassares',
  components: {
    d3Barchart,
    Treeselect,
    mscntList,
    gcmvList
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
      // center: [-73.845, 40.72],
      center: [NaN, NaN],
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
      param: 'mscnt',
      measurement: {
        'type': 'Feature',
        'properties': {
          'job_id': null,
          'bore_id': null,
          'instrument': 'Mass Spectrometer',
          'chemical_id': null,
          'measurement_value': null,
          'units': null,
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
      devoptions: [
        'Mass Spectrometer',
        'Gas Chromatograph'
      ],
      longitude: null,
      latitude: null,
      measurements: '',
      mscntModel: 'Selected',
      gcmvModel: 'Selected',
      // measurement search and popup attributes
      searchmscntjoptions: [],
      searchgcmvjoptions: [],
      starttimestamp: this.startDate() + 'T00:00:00',
      endtimestamp: this.endDate() + 'T00:00:00',
      starttimestampx: this.startDate() + 'T00:00:00',
      endtimestampx: this.endDate() + 'T00:00:00',
      toptions: null,
      jobids: undefined,
      jobidsx: undefined,
      joptions: null,
      pid: undefined,
      chemical_id: undefined,
      measurement_value: undefined,
      units: undefined,
      timestamp: undefined,
      // powerline attributes
      powerlines: {
        'type': 'Feature',
        'properties': {
          'title': undefined,
          'powerline': undefined,
          'voltage': undefined,
          'service_date': undefined
        },
        'geometry': {
          'type': 'MultiLineString',
          'coordinates': [null, null]
        }
      },
      powerlinesModel: 'Selected',
      ptitle: undefined,
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
            url: 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/powerline/?format=json'
          },
          style: [
            {
              cmp: 'vl-style-func',
              factory: this.getPowerlinesStyle
            }
          ]
        },
        {
          id: 'mscnt',
          title: 'Mass Spectrometer Count',
          cmp: 'vl-layer-vector',
          visible: true,
          source: {
            cmp: 'vl-source-vector',
            url (extent, starttimestampx, endtimestampx) {
              starttimestampx = '2018-10-01T00:00:00'
              endtimestampx = '2020-01-01T00:00:00'
              return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/mscnt/?format=json&timestamp__gte=' +
                starttimestampx.replace('T', ' ') + '&timestamp__lte=' + endtimestampx.replace('T', ' ') + '&in_bbox=' + extent.join(',').toString()
            },
            strategyFactory () {
              return loadingBBox
            }
          },
          style: [
            {
              cmp: 'vl-style-func',
              factory: this.mscntStyle
            }
          ]
        },
        {
          id: 'gcmv',
          title: 'Gas Chromatograph Millivolt',
          cmp: 'vl-layer-vector',
          visible: true,
          source: {
            cmp: 'vl-source-vector',
            url (extent, starttimestampx, endtimestampx) {
              starttimestampx = '2018-10-01T00:00:00'
              endtimestampx = '2020-01-01T00:00:00'
              return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/gcmv/?format=json&timestamp__gte=' +
                starttimestampx.replace('T', ' ') + '&timestamp__lte=' + endtimestampx.replace('T', ' ') + '&in_bbox=' + extent.join(',').toString()
            },
            strategyFactory () {
              return loadingBBox
            }
          },
          style: [
            {
              cmp: 'vl-style-func',
              factory: this.gcmvStyle
            }
          ]
        }
      ]
    }
  },
  created: function () {
    // get current location, and use it for map center
    this.$getLocation()
      .then(coordinates => {
        this.center = [coordinates.lng, coordinates.lat]
      })

    // search timestamp
    let that = this
    let sjurl = 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/mscntjobid/?format=json'
    axios.get(sjurl)
      .then(function (response) {
        that.searchmscntjoptions = response.data
      })
      .catch(function (error) {
        console.log(error)
      })
    // search jobid
    let cjurl = 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/gcmvjobid/?format=json'
    axios.get(cjurl)
      .then(function (response) {
        that.searchgcmvjoptions = response.data
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
    mscntStyle: function () {
      return feature => {
        return [
          new Style({
            image: new Circle({
              radius: (this.zoom / 2.6) + (feature.get('measurement_value') / 2),
              fill: new Fill({ color: count2color(feature.get('measurement_value') * 4.54) }), // 'rgba(245, 111, 66, 0.7)'
              stroke: new Stroke({
                color: 'rgb(145, 7, 4, 1)',
                width: 1
              })
            })
          })
        ]
      }
    },
    gcmvStyle: function () {
      return feature => {
        return [
          new Style({
            image: new Circle({
              radius: (this.zoom / 2.6) + (feature.get('measurement_value') / 2),
              fill: new Fill({ color: millivolt2color(feature.get('measurement_value') * 4.54) }), // 'rgba(245, 111, 66, 0.7)'
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
    },
    drawEnd: function (event) {
      if (this.drawType === 'point') {
        this.selectLocation(event)
      } else if (this.drawType === 'polygon') {
        this.selectInDrawnPolygon(event)
      }
    },
    selectInDrawnPolygon: function (event) {
      this.selectedFeatures = []
      this.selectedFeaturesBarBox = []
      this.isBox = 'yes'
      // only use source that have chemical_id
      let vectorSource
      let i
      for (i = 0; i < this.$refs.layerSource.length; i++) {
        let features = this.$refs.layerSource[i].getFeatures()
        if (features[0] !== undefined) {
          if (features[0].values_.instrument === this.measurement.properties.instrument) {
            vectorSource = this.$refs.layerSource[i].$source
          }
        }
      }
      const extent = event.feature.values_.geometry.extent_
      vectorSource.forEachFeatureIntersectingExtent(extent, feature => {
        feature = writeGeoJsonFeature(feature)
        this.selectedFeatures.push(feature)
        this.selectedFeaturesBarBox.push({ x: feature.properties['timestamp'], y: feature.properties['measurement_value'] })
        this.chemical_id = feature.properties['chemical_id']
        this.pid = this.chemical_id
      })
      this.drawType = undefined
      // console.log(event)
      // console.log(this.$refs)
      // var selectSource = Select.getLayer(event.feature).getSource()
      // selectSource.removeFeature(event.feature)
    },
    closeBarChart: function () {
      this.selectedFeatures = this.selectedFeatures.filter(f => f.id === 0)
      let drawFeatures = this.$refs.drawSource.getFeatures()
      this.$refs.drawSource.removeFeatures(drawFeatures)
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
      let glayer = this.layers[2]
      if (this.gcmvModel === 'Selected') {
        glayer.visible = true
      } else if (this.gcmvModel === 'Not Selected') {
        glayer.visible = false
      }

      let mlayer = this.layers[1]
      if (this.mscntModel === 'Selected') {
        mlayer.visible = true
      } else if (this.mscntModel === 'Not Selected') {
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
          if (properties['chemical_id']) {
            this.pid = properties['chemical_id']
            this.chemical_id = this.pid
            this.measurement_value = properties['measurement_value']
            this.units = properties['units']
            this.timestamp = properties['timestamp']
            this.selectedFeaturesBarBox = []
            this.selectedFeatures = []
            this.isBox = 'no'
          } else if (properties['powerline']) {
            this.pid = properties['powerline']
            this.ptitle = properties['title']
            this.powerline = this.pid
            this.measurement_value = undefined
            this.units = undefined
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
    MeasurementsURL: function (extent, instcode, starttimestampx, endtimestampx, jobidsx) {
      if (!jobidsx) {
        return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/' + instcode + '/?format=json&timestamp__gte=' + starttimestampx + '&timestamp__lte=' + endtimestampx + '&in_bbox=' + extent.join(',').toString()
      } else if (jobidsx) {
        if (starttimestampx) {
          if (jobidsx.length === 1) {
            return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/' + instcode + '/?format=json&timestamp__gte=' + starttimestampx + '&timestamp__lte=' + endtimestampx + '&job_id=' + jobidsx + '&in_bbox=' + extent.join(',').toString()
          } else if (jobidsx.length > 1) {
            return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/' + instcode + '/?format=json&timestamp__gte=' + starttimestampx + '&timestamp__lte=' + endtimestampx + '&job_id__in=' + jobidsx + '&in_bbox=' + extent.join(',').toString()
          } else if (jobidsx.length === 0) {
            return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/' + instcode + '/?format=json&timestamp__gte=' + starttimestampx + '&timestamp__lte=' + endtimestampx + '&in_bbox=' + extent.join(',').toString()
          } else {
            alert('this should not happen!')
            return 'this should not happen!'
          }
        } else if (!starttimestampx) {
          if (jobidsx.length === 1) {
            return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/' + instcode + '/?format=json&job_id=' + jobidsx + '&in_bbox=' + extent.join(',').toString()
          } else if (jobidsx.length > 1) {
            return 'https://' + pubhost[0].PUBHOST_URL + '/drf/api/' + instcode + '/?format=json&job_id__in=' + jobidsx + '&in_bbox=' + extent.join(',').toString()
          } else {
            alert(jobidsx.length)
            // alert('this should not happen, too!')
            return 'this should not happen, too!'
          }
        }
      }
    },
    // filter data only on the client side. Dependent on data available from the DRF server
    searchMeasurements: function () {
      let instcode
      if (this.measurement.properties.instrument === 'Mass Spectrometer') {
        instcode = 'mscnt'
      } else if (this.measurement.properties.instrument === 'Gas Chromatograph') {
        instcode = 'gcmv'
      }

      let extent = this.$refs.map.$map.getView().calculateExtent(this.$refs.map.$map.getSize())
      let sw = toLonLat([extent[0], extent[1]])
      let ne = toLonLat([extent[2], extent[3]])
      extent = [sw[0], sw[1], ne[0], ne[1]]

      if (this.starttimestampx && this.endtimestampx) {
        if (this.endtimestampx < this.starttimestampx) {
          this.$notification.open('You have to pick end timestep later than the start timestamp!')
        } else {
          this.starttimestampx = this.starttimestampx.replace('T', ' ')
          this.endtimestampx = this.endtimestampx.replace('T', ' ')
          let i
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.instrument === this.measurement.properties.instrument) {
              // url to get data from
              let url = this.MeasurementsURL(extent, instcode, this.starttimestampx, this.endtimestampx, this.jobidsx)
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
        } else if (this.jobidsx.length >= 1) {
          this.starttimestampx = this.starttimestampx.replace('T', ' ')
          this.endtimestampx = this.endtimestampx.replace('T', ' ')
          let i
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.instrument === this.measurement.properties.instrument) {
              let url = this.MeasurementsURL(extent, instcode, this.starttimestampx, this.endtimestampx, this.jobidsx)
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
    startDate: function () {
      let date = new Date()
      let year = date.getFullYear() - 1
      let month = date.getMonth()
      month = (month < 10 ? '0' : '') + month
      let day = date.getDate()
      day = (day < 10 ? '0' : '') + day
      let startDate = year.toString() + '-' + month.toString() + '-' + day.toString()
      return startDate
    },
    endDate: function () {
      let date = new Date()
      let year = date.getFullYear() + 1
      let month = date.getMonth()
      month = (month < 10 ? '0' : '') + month
      let day = date.getDate()
      day = (day < 10 ? '0' : '') + day
      let endDate = year.toString() + '-' + month.toString() + '-' + day.toString()
      return endDate
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
      console.log(this.$refs.geoloc)
      this.longitude = this.deviceCoordinate[0]
      this.latitude = this.deviceCoordinate[1]
    },
    selectLocation: function (event) {
      let coordinates = toLonLat(event.feature.values_.geometry.flatCoordinates)
      this.longitude = coordinates[0]
      this.latitude = coordinates[1]
      this.drawType = undefined
    },
    onUpdatePosition: function (coordinate) {
      this.deviceCoordinate = coordinate
      this.center = [this.deviceCoordinate[0], this.deviceCoordinate[1]]
    },
    onUpdateAccuracy: function (accuracy) {
      this.coordinateAccuracy = accuracy
    },
    onReset: function () {
      this.measurement.id = null
      this.measurement.properties.bore_id = null
      this.measurement.properties.job_id = null
      this.measurement.properties.instrument = null
      this.measurement.properties.chemical_id = null
      this.measurement.properties.measurement_value = null
      this.measurement.properties.units = null
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
      if (this.measurement.properties.instrument === 'Mass Spectrometer') {
        this.measurement.properties.units = 'count'
        this.param = 'mscnt'
      } else if (this.measurement.properties.instrument === 'Gas Chromatograph') {
        this.measurement.properties.units = 'mV'
        this.param = 'gcmv'
      } else {
        this.measurement.properties.units = 'none'
        this.param = 'none'
        alert('This will not work because you have an incorrect value for your units.')
      }
      this.creating = true
      apiService.createMeasurement(this.param, this.measurement).then((result) => {
        // console.log(result)
        // success
        if (result.status === 201) {
          this.measurement = result.data
          this.showCreateMessage = true
          let i
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.instrument) {
              if (features[0].values_.instrument === 'Mass Spectrometer') {
                if (this.measurement.properties.instrument === 'Mass Spectrometer') {
                  this.$refs.layerSource[i].addFeature(this.measurement)
                  let drawFeatures = this.$refs.drawSource.getFeatures()
                  this.$refs.drawSource.removeFeatures(drawFeatures)
                }
              } else if (features[0].values_.instrument === 'Gas Chromatograph') {
                if (this.measurement.properties.instrument === 'Gas Chromatograph') {
                  this.$refs.layerSource[i].addFeature(this.measurement)
                  let drawFeatures = this.$refs.drawSource.getFeatures()
                  this.$refs.drawSource.removeFeatures(drawFeatures)
                }
              }
            }
          }
          // console.log(this.$refs.layerSource)
        }
        sleep(1000).then(() => {
          this.creating = false
        })
      })
    },
    updateMeasurement: function (param) {
      let coordinates = [parseFloat(this.longitude), parseFloat(this.latitude)]
      this.measurement.geometry.coordinates = coordinates
      if (this.measurement.properties.instrument === 'Mass Spectrometer') {
        this.measurement.properties.units = 'count'
        this.param = 'mscnt'
      } else if (this.measurement.properties.instrument === 'Gas Chromatograph') {
        this.measurement.properties.units = 'mV'
        this.param = 'gcmv'
      } else {
        this.measurement.properties.units = 'none'
        this.param = 'none'
        alert('This will not work because you have an incorrect value for your units.')
      }
      this.updating = true
      apiService.updateMeasurement(this.param, this.measurement).then((result) => {
        // success
        if (result.status === 200) {
          this.measurement = result.data
          this.showUpdateMessage = true
          let i
          for (i = 0; i < this.$refs.layerSource.length; i++) {
            let features = this.$refs.layerSource[i].getFeatures()
            if (features[0].values_.instrument) {
              if (features[0].values_.instrument === 'Mass Spectrometer') {
                if (this.measurement.properties.instrument === 'Mass Spectrometer') {
                  let feature = this.$refs.layerSource[i].getFeatureById(this.measurement.id)
                  this.$refs.layerSource[i].removeFeature(feature)
                  this.$refs.layerSource[i].addFeature(this.measurement)
                  let drawFeatures = this.$refs.drawSource.getFeatures()
                  this.$refs.drawSource.removeFeatures(drawFeatures)
                }
              } else if (features[0].values_.instrument === 'Gas Chromatograph') {
                if (this.measurement.properties.instrument === 'Gas Chromatograph') {
                  let feature = this.$refs.layerSource[i].getFeatureById(this.measurement.id)
                  this.$refs.layerSource[i].removeFeature(feature)
                  this.$refs.layerSource[i].addFeature(this.measurement)
                  let drawFeatures = this.$refs.drawSource.getFeatures()
                  this.$refs.drawSource.removeFeatures(drawFeatures)
                }
              }
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
      Uploader.removeFile(files)
      reader.readAsText(file)
      reader.onerror = err => console.error(`Failed to read file: ${err}`)
      reader.onload = function () {
        let geojson = JSON.parse(reader.result)
        that.creating = true
        let i
        if (geojson.features[0].properties.chemical_id) {
          if (geojson.features[0].properties.instrument === 'Mass Spectrometer') {
            this.param = 'mscnt'
          } else if (geojson.features[0].properties.instrument === 'Gas Chromatograph') {
            this.param = 'gcmv'
          } else {
            this.param = 'none'
            alert('This will not work because you have an incorrect value for your units.')
          }
          for (i = 0; i < geojson.features.length; i++) {
            apiService.createMeasurement(this.param, geojson.features[i]).then((result) => {
              if (result.status === 201) {
                that.measurement = result.data
                that.showCreateMessage = true
                let j
                for (j = 0; j < that.$refs.layerSource.length; j++) {
                  let features = that.$refs.layerSource[j].getFeatures()
                  if (features[0].values_.chemical_id) {
                    that.$refs.layerSource[j].addFeature(that.measurement)
                  }
                }
              }
              sleep(1000).then(() => {
                that.creating = false
              })
            })
          }
        } else if (geojson.features[0].properties.powerline) {
          for (i = 0; i < geojson.features.length; i++) {
            apiService.createPowerline(geojson.features[i]).then((result) => {
              if (result.status === 201) {
                that.powerlines = result.data
                that.showCreateMessage = true
                let j
                for (j = 0; j < that.$refs.layerSource.length; j++) {
                  let features = that.$refs.layerSource[j].getFeatures()
                  if (features[0].values_.powerline) {
                    that.$refs.layerSource[j].addFeature(that.powerlines)
                  }
                }
              }
              sleep(1000).then(() => {
                that.creating = false
              })
            })
          }
        } else {
          alert('Incorrect data in your file.')
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
      apiService.getMeasurement(this.param, this.$route.params.id).then((measurement) => {
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

  .mtable
    border: 0px
    border-collapse: collapse
    border-spacing: 0px

  .msdot1
    height: 15px;
    width: 15px;
    background-color: #84f542;
    border-radius: 50%;
    display: inline-block

  .msdot2
    height: 20px;
    width: 20px;
    background-color: #ffff04;
    border-radius: 50%;
    display: inline-block

  .msdot3
    height: 25px;
    width: 25px;
    background-color: #f52701;
    border-radius: 50%;
    display: inline-block

  .gcdot1
    height: 15px;
    width: 15px;
    background-color: #00ff8c;
    border-radius: 50%;
    display: inline-block

  .gcdot2
    height: 20px;
    width: 20px;
    background-color: #00a4ff;
    border-radius: 50%;
    display: inline-block

  .gcdot3
    height: 25px;
    width: 25px;
    background-color: #062aff;
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
    background: #e0f2f1;

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

  .q-datetimepicker.q-card
    background: #e0f2f1;
    .q-tab-panels
      background: #e0f2f1;

  .q-input
    height: 4.0em;

  .q-select
    height: 4.0em;

</style>
