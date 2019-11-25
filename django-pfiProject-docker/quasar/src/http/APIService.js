/* eslint-disable */
import axios from 'axios'
import AuthService from '../auth/AuthService'

import pubhost from '../assets/pubhost.json'
const API_URL = pubhost[0].PUBHOST_URL

export class APIService{
  constructor(){
      
  }
  getMeasurements() {
    const url = "https://" + API_URL + "/meas/api/measurements/"
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.get(url, { headers: headers }).then(response => response.data)
  }
  getMeasurementsByURL(link) {
    const url = `https://${API_URL}${link}`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.get(url, { headers: headers }).then(response => response.data)
  }
  getMeasurement(id) {
    const url = `https://${API_URL}/meas/api/measurements/${id}`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.get(url, { headers: headers }).then(response => response.data)
  }    
  deleteMeasurement(measurement) {
    const url = `https://${API_URL}/meas/api/measurements/${measurement.id}`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.delete(url, { headers: headers })
  }
  createMeasurement(measurement) {
    const url = `https://${API_URL}/meas/api/measurements/`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.post(url, measurement, { headers: headers })
  }
  updateMeasurement(measurement) {
    const url = `https://${API_URL}/meas/api/measurements/${measurement.id}`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.put(url, measurement, { headers: headers })
  }
  createPowerline(powerline) {
    const url = `https://${API_URL}/drf/api/powerlines/`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.post(url, powerline, { headers: headers })
  }
} 
