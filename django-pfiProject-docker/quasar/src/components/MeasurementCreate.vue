<template>
  <div class="q-pa-md" style="max-width: 600px">
    <q-card>
      <div class="q-pa-md" style="max-width: 600px">
        <div class="text-h6">Measurements</div>
        <div class="text-subtitle2">Input Data</div>

        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
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

          <q-input color="teal" filled v-model="measurement.properties.date" id="date" label="Date *" hint="Date of measurement">
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
                  <q-date v-model="measurement.properties.date" mask="YYYY-MM-DD" color="teal" text-color="black" />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>

          <q-input color="teal" filled v-model="measurement.properties.time" id="time" label="Time *" hint="Time of measurement" mask="fulltime" :rules="['fulltime']">
            <template v-slot:append>
              <q-icon name="access_time" class="cursor-pointer">
                <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
                  <q-time now-btn v-model="measurement.properties.time" with-seconds format12h color="teal" text-color="black" />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>

          <q-input color="teal" filled v-model="longitude" id="longitude" label="Longitude *" hint="Longitude of the bore hole" lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type the longitude']"/>
          <q-input color="teal" filled v-model="latitude" id="latitude" label="Latitude *" hint="Latitude of the bore hole" lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type the latitude']"/>

          <div>
            <q-btn label="Submit" type="submit" color="teal" class="text-black" v-if="!this.measurement.id" @click="createMeasurement()" >
              <span v-if="creating">Creating... Please wait </span>
            </q-btn>
            <q-btn label="Ubdate" type="submit" color="teal" class="text-black" v-if="this.measurement.id" @click="updateMeasurement()" >
              <span v-if="creating">Creating... Please wait </span>
            </q-btn>
            <q-btn label="Reset" type="reset" color="teal" flat class="q-ml-sm" @click="onReset()" />
          </div>
        </q-form>
        <q-space />
        <q-separator />
        <q-space />
        <q-btn label="Select Location" type="Point" color="teal" class="text-black" @click="drawType = 'point'">
        </q-btn>
        <q-btn label="Stop Selection" type="Point" color="teal" class="text-black" @click="drawType = undefined">
        </q-btn>
      </div>
    </q-card>
  </div>
 </template>

<script>
import { date } from 'quasar'
import { APIService } from '../http/APIService'
const apiService = new APIService()

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time))
}

export default {
  name: 'MeasurementCreate',
  components: {
  },
  data () {
    return {
      showCreateMessage: false,
      showUpdateMessage: false,
      showError: false,
      measurement: {
        'type': 'Feature',
        'properties': {
          'bore_id': null,
          'job_id': null,
          'device_id': null,
          'chemical_id': null,
          'concentration': null,
          'date': null,
          'time': null,
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
      creating: false,
      updating: false,
      drawControls: [
        {
          type: 'point',
          label: 'Draw Point',
          icon: 'map-marker'
        },
        {
          type: undefined,
          label: 'Stop drawing',
          icon: 'times'
        }
      ],
      drawType: undefined,
      drawnFeatures: []
    }
  },
  methods: {
    currentDate: function () {
      let timeStamp = Date.now()
      let formattedString = date.formatDate(timeStamp, 'YYYY-MM-DD')
      return formattedString
    },
    currentTime: function () {
      let timeStamp = Date.now()
      let formattedString = date.formatDate(timeStamp, 'HH:mm:ss.SSSZ')
      return formattedString
    },
    onSubmit: function () {
      this.$q.notify({
        color: 'red-5',
        textColor: 'black',
        icon: 'warning',
        message: this.currentTime()
      })
    },
    onReset: function () {
      this.measurement.properties.bore_id = null
      this.measurement.properties.job_id = null
      this.measurement.properties.device_id = null
      this.measurement.properties.chemical_id = null
      this.measurement.properties.concentration = null
      this.measurement.properties.comment = null
      this.measurement.properties.date = null
      this.measurement.properties.time = null
      this.longitude = null
      this.latitude = null
      this.measurement.geometry.coordinates = null
    },
    createMeasurement: function () {
      let coordinates = [parseFloat(this.longitude), parseFloat(this.latitude)]
      this.measurement.geometry.coordinates = coordinates
      // console.log(JSON.stringify(this.measurement))
      console.log(this.measurement)
      this.creating = true
      apiService.createMeasurement(this.measurement).then((result) => {
        // console.log(result)
        // success
        if (result.status === 201) {
          this.measurement = result.data
          this.showCreateMessage = true
        }
        sleep(1000).then(() => {
          this.creating = false
        })
      }) /*, (error) => {
        this.showError = true
        sleep(1000).then(() => {
          this.creating = false
        })
      }) */
    },
    updateMeasurement: function () {
      this.updating = true
      console.log('update measurement' + JSON.stringify(this.measurement))
      apiService.updateMeasurement(this.measurement).then((result) => {
        console.log(result)
        // success
        if (result.status === 200) {
          // this.measurement = {}
          this.showUpdateMessage = true
          sleep(1000).then(() => {
            this.updating = false
          })
        }
      }) /* , (error) => {
        this.showError = true
        sleep(1000).then(() => {
          this.updating = false
        })
      }) */
    }
  },
  mounted () {
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
  .aform
    margin-left:  auto
    width: 60%

</style>
