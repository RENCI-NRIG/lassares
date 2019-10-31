<template>
  <q-page-container style="padding: 0px;">
    <q-page>
      <q-card class="measurement-card">
        <div class="q-pa-md" style="max-width: 1200px; max-height: 750px;">
          <q-banner inline-actions>
            <div class="text-subtitle2">
             Measurements ({{ numberOfMeasurements }})
            </div>
            <template align="right" v-slot:action>
              <q-btn flat round dense icon="close" color="teal" v-close-popup />
            </template>
          </q-banner>
          <q-card-section>
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
                  <th style="font-size:10px">Bore ID</th>
                  <th style="font-size:10px">Job ID</th>
                  <th style="font-size:10px">Device ID</th>
                  <th style="font-size:10px">Chemical ID</th>
                  <th style="font-size:10px">Concentration</th>
                  <th style="font-size:10px">Date</th>
                  <th style="font-size:10px">Time</th>
                  <th style="font-size:10px">Status</th>
                  <th style="font-size:10px">Comment</th>
                  <th style="font-size:10px">Coordinates</th>
                  <th style="font-size:10px">Delete</th>
                  <th style="font-size:10px">Edit</th>
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
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.bore_id }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.job_id }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.device_id }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.chemical_id }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.concentration }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.date }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.time }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.status }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.properties.comment }}</td>
                  <td class="text-center" style="font-size:10px">{{ measurement.geometry.coordinates[0].toFixed(2) +', ' +
                    measurement.geometry.coordinates[1].toFixed(2) }}</td>
                  <td class="text-center">
                    <q-btn flat round dense icon="delete" color="white" class="text-teal" @click="remove = true" />
                    <q-dialog v-model="remove" persistent>
                      <q-card>
                        <q-card-section class="row items-center">
                          <q-avatar icon="delete" color="teal" text-color="white" />
                          <span class="q-ml-sm">Are you sure you want to delete the data?</span>
                        </q-card-section>

                        <q-card-actions align="right">
                          <q-btn flat round dense label="Cancel" color="teal" v-close-popup />
                          <q-btn flat round dense label="Yes" color="teal" v-close-popup @click="deleteMeasurement(measurement)" />
                        </q-card-actions>
                      </q-card>
                    </q-dialog>
                  </td>
                  <td class="text-center">
                    <q-btn flat round dense icon="edit" color="white" class="text-teal" @click="editMeasurement(measurement)" v-close-popup />
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
          <q-inner-loading :showing="loading">
            <q-spinner-gears size="50px" color="teal" />
          </q-inner-loading>
        </div>
      </q-card>
    </q-page>
  </q-page-container>
</template>

<script>
import { EventBus } from '../mixins/event-bus.js'
import { APIService } from '../http/APIService'
const apiService = new APIService()

export default {
  name: 'MeasurementList',
  data () {
    return {
      current: 1,
      selectedMeasurement: null,
      measurements: [],
      numberOfPages: 0,
      pages: [],
      numberOfMeasurements: 0,
      loading: false,
      remove: false
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
        this.measurements = page.data.features
        this.loading = false
      })
    },
    editMeasurement: function (measurement) {
      // Send the event (click) on a channel (edit-measurement) with a payload (measurement)
      EventBus.$emit('edit-measurement', measurement)
    },
    deleteMeasurement: function (measurement) {
      apiService.deleteMeasurement(measurement).then((r) => {
        if (r.status === 204) {
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
