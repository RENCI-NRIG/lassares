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
    return axios.get(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }}).then(response => response.data)
  }
  getMeasurementsByURL(link) {
    const url = `https://${API_URL}${link}`
    return axios.get(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }}).then(response => response.data)
  }
  getMeasurement(id) {
    const url = `https://${API_URL}/meas/api/measurements/${id}`
    return axios.get(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }}).then(response => response.data)
  }    
  deleteMeasurement(measurement) {
    const url = `https://${API_URL}/meas/api/measurements/${measurement.id}`
    return axios.delete(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }})
  }
  createMeasurement(measurement) {
    const url = `https://${API_URL}/meas/api/measurements/`
    const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`}
    return axios.post(url,measurement,{headers: headers})
  }
  updateMeasurement(measurement) {
    const url = `https://${API_URL}/meas/api/measurements/${measurement.id}`
    const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`}
    return axios.put(url,measurement,{headers: headers})
  }    
} 
