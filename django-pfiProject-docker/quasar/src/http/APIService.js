/* eslint-disable */
import axios from 'axios'
import AuthService from '../auth/AuthService'

import pubhost from '../assets/pubhost.json'
const API_URL = pubhost[0].PUBHOST_URL

export class APIService{
  constructor(){
      
  }
  getMeasurements(param) {
    const url = ${API_URL}/meas/api/${param}/`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.get(url, { headers: headers }).then(response => response.data)
  }
  getMeasurementsByURL(link) {
    const url = ${API_URL}${link}`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.get(url, { headers: headers }).then(response => response.data)
  }
  getMeasurement(param,id) {
    const url = ${API_URL}/meas/api/${param}/${id}`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.get(url, { headers: headers }).then(response => response.data)
  }    
  deleteMeasurement(param,measurement) {
    const url = ${API_URL}/meas/api/${param}/${measurement.id}`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.delete(url, { headers: headers })
  }
  createMeasurement(param,measurement) {
    const url = ${API_URL}/meas/api/${param}/`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.post(url, measurement, { headers: headers })
  }
  updateMeasurement(param,measurement) {
    const url = ${API_URL}/meas/api/${param}/${measurement.id}`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.put(url, measurement, { headers: headers })
  }
  createPowerline(powerline) {
    const url = ${API_URL}/drf/api/powerlines/`
    const headers = { Authorization: `Bearer ${AuthService.getAuthToken()}` }
    return axios.post(url, powerline, { headers: headers })
  }
} 
