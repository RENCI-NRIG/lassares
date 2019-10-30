<template>
<q-page-container style="padding: 0px;">
  <q-page>
  <q-card class="measurement-card">
    <div class="q-pa-md" style="max-width: 1200px; max-height: 700px;">
      <q-card-section>
        <div class="text-h6">Measurements ({{numberOfMeasurements}})</div>
      </q-card-section>
      <q-card-section>
        <Loading :loading="loading"></Loading>
        <q-markup-table>
          <col width="80">
          <col width="80">
          <col width="80">
          <col width="80">
          <col width="80">
          <col width="100">
          <col width="80">
          <col width="50">
          <col width="150">
          <col width="130">
          <col width="50">
          <col width="50">
          <thead>
            <tr>
              <th>Bore ID</th>
              <th>Job ID</th>
              <th>Device ID</th>
              <th>Chemical ID</th>
              <th>Concentration</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
              <th>Comment</th>
              <th>Coordinates</th>
              <th>Delete</th>
              <th>Edit</th>
            </tr>
          </thead>
          <col width="80">
          <col width="80">
          <col width="80">
          <col width="80">
          <col width="80">
          <col width="100">
          <col width="80">
          <col width="50">
          <col width="150">
          <col width="130">
          <col width="50">
          <col width="50">
          <tbody>
            <tr v-for="measurement in measurements" v-bind:key="measurement.properties.bore_id" @click="selectMeasurement(measurement)">
              <td class="text-center">{{ measurement.properties.bore_id }}</td>
              <td class="text-center">{{ measurement.properties.job_id }}</td>
              <td class="text-center">{{ measurement.properties.device_id }}</td>
              <td class="text-center">{{ measurement.properties.chemical_id }}</td>
              <td class="text-center">{{ measurement.properties.concentration }}</td>
              <td class="text-center">{{ measurement.properties.date }}</td>
              <td class="text-center">{{ measurement.properties.time }}</td>
              <td class="text-center">{{ measurement.properties.status }}</td>
              <td class="text-center">{{ measurement.properties.comment }}</td>
              <td class="text-center">{{ measurement.geometry.coordinates[0].toFixed(2) +', ' + measurement.geometry.coordinates[1].toFixed(2) }}</td>
              <td class="text-center">
                <q-icon name="delete" color="teal" class="text-black" @click="deleteMeasurement(measurement)" />
              </td>
              <td class="text-center">
                <q-icon name="edit" color="teal" class="text-black" @click="editMeasurement(measurement)" />
              </td>
            </tr>
          </tbody>
        </q-markup-table>
      </q-card-section>
      <q-card-section>
        <div class="q-pa-lg flex flex-center">
          <q-pagination color="teal" v-model="current" :max="numberOfPages" @click="getPage()">
          </q-pagination>
        </div>
      </q-card-section>
    </div>
  </q-card>
  </q-page>
</q-page-container>
</template>

<script>
import { EventBus } from '../mixins/event-bus.js'
import { APIService } from '../http/APIService'
import Loading from './Loading'
const apiService = new APIService()

export default {
  name: 'MeasurementList',
  components: {
    Loading
  },
  data () {
    return {
      current: 1,
      selectedMeasurement: null,
      measurements: [],
      numberOfPages: 0,
      pages: [],
      numberOfMeasurements: 0,
      loading: false
    }
  },
  methods: {
    getMeasurements: function () {
      this.loading = true
      apiService.getMeasurements().then((page) => {
        this.measurements = page.data.features
        // console.log(this.measurements)
        // console.log(page)
        // console.log(page.nextlink)
        this.numberOfMeasurements = page.count
        this.numberOfPages = page.numpages
        if (this.numberOfPages) {
          for (var i = 1; i <= this.numberOfPages; i++) {
            const link = `/meas/api/measurements/?page=${i} `
            this.pages.push({ pageNumber: i, link: link })
          }
        }
        this.loading = false
      })
    },
    getPage: function () {
      this.loading = true
      apiService.getMeasurementsByURL('/meas/api/measurements/?page=' + this.current).then((page) => {
        // console.log(page.data)
        this.measurements = page.data.features
        this.loading = false
      })
    },
    editMeasurement: function (measurement) {
      // Send the event (click) on a channel (edit-measurement) with a payload (measurement)
      EventBus.$emit('edit-measurement', measurement)
    },
    deleteMeasurement: function (measurement) {
      console.log('deleting measurement: ' + JSON.stringify(measurement))
      apiService.deleteMeasurement(measurement).then((r) => {
        console.log(r)
        if (r.status === 204) {
          /* for(var i = this.measurements.length-1; i--;){
            console.log(this.measurements[i].bore_id)
            if (this.measurements[i].properties.bore_id === measurement.properties.bore_id)
            {
              console.log("deleting measurement " + this.measurements[i].properties.bore_id)
              this.measurements.properties.splice(i, 1)
            }
          } */
          alert('Measurement deleted')
          this.$router.go()
        }
      })
    },
    selectMeasurement: function (measurement) {
      this.selectedMeasurement = measurement
    }
  },
  mounted () {
    this.getMeasurements()
  }
}
</script>
<style lang="sass">
  .ml
    window-width: "50vw"

  .measurement-card
    fit

</style>
